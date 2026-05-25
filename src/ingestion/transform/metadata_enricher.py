"""Metadata enrichment transform with rule-based and optional LLM enhancement."""

from __future__ import annotations

import json
import re
from typing import Any

from core.types import Chunk
from ingestion.transform.base_transform import BaseTransform
from libs.llm.base_llm import BaseLLM
from libs.llm.llm_factory import LLMFactory


_STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "has",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "that",
    "the",
    "to",
    "was",
    "were",
    "will",
    "with",
}
_WORD_PATTERN = re.compile(r"[A-Za-z][A-Za-z0-9_-]{1,}")
_SENTENCE_SPLIT_PATTERN = re.compile(r"(?<=[.!?])\s+")


class MetadataEnricher(BaseTransform):
    """Populate chunk metadata with title/summary/tags, optionally via LLM."""

    def __init__(
        self,
        settings: Any,
        llm: BaseLLM | None = None,
    ) -> None:
        self.settings = settings
        self._use_llm = self._resolve_use_llm(settings)
        self._llm = llm
        self._llm_resolution_error: str | None = None
        self._last_llm_error: str | None = None

    def transform(self, chunks: list[Chunk], trace: Any | None = None) -> list[Chunk]:
        self.validate_chunks(chunks)

        output: list[Chunk] = []
        llm_enriched_count = 0
        rule_enriched_count = 0
        fallback_count = 0

        for chunk in chunks:
            try:
                enriched_chunk, enriched_by = self._enrich_chunk(chunk, trace=trace)
            except Exception as exc:
                enriched_chunk = self._with_metadata(
                    chunk,
                    metadata_patch=self._safe_rule_metadata(chunk.text),
                    enriched_by="rule",
                    fallback_reason=f"chunk_processing_failed: {exc}",
                )
                enriched_by = "rule"

            if enriched_by == "llm":
                llm_enriched_count += 1
            else:
                rule_enriched_count += 1
                if enriched_chunk.metadata.get("metadata_fallback_reason"):
                    fallback_count += 1

            output.append(enriched_chunk)

        if trace is not None and hasattr(trace, "record_stage"):
            trace.record_stage(
                "transform_metadata_enricher",
                chunk_count=len(chunks),
                llm_enabled=self._use_llm,
                llm_enriched_count=llm_enriched_count,
                rule_enriched_count=rule_enriched_count,
                fallback_count=fallback_count,
            )
        return output

    def _enrich_chunk(self, chunk: Chunk, *, trace: Any | None = None) -> tuple[Chunk, str]:
        rule_metadata = self._rule_based_metadata(chunk.text)
        if not self._use_llm:
            return (
                self._with_metadata(
                    chunk,
                    metadata_patch=rule_metadata,
                    enriched_by="rule",
                    fallback_reason=None,
                ),
                "rule",
            )

        llm_metadata = self._llm_metadata(chunk.text, trace=trace)
        if llm_metadata is None:
            return (
                self._with_metadata(
                    chunk,
                    metadata_patch=rule_metadata,
                    enriched_by="rule",
                    fallback_reason=self._last_llm_error or self._llm_resolution_error,
                ),
                "rule",
            )

        return (
            self._with_metadata(
                chunk,
                metadata_patch=llm_metadata,
                enriched_by="llm",
                fallback_reason=None,
            ),
            "llm",
        )

    def _resolve_llm(self) -> BaseLLM | None:
        if not self._use_llm:
            return None
        if self._llm is not None:
            return self._llm
        if self._llm_resolution_error is not None:
            return None
        try:
            self._llm = LLMFactory.create(self.settings)
            return self._llm
        except Exception as exc:
            self._llm_resolution_error = f"llm_init_failed: {exc}"
            return None

    def _rule_based_metadata(self, text: str) -> dict[str, Any]:
        if not isinstance(text, str):
            raise TypeError("chunk text must be a string")

        normalized = re.sub(r"\s+", " ", text).strip()
        if not normalized:
            return {
                "title": "Untitled chunk",
                "summary": "No textual content available.",
                "tags": ["general"],
            }

        title = self._build_title(normalized)
        summary = self._build_summary(normalized)
        tags = self._build_tags(normalized)
        return {"title": title, "summary": summary, "tags": tags}

    def _safe_rule_metadata(self, text: str) -> dict[str, Any]:
        try:
            return self._rule_based_metadata(text)
        except Exception:
            return {
                "title": "Untitled chunk",
                "summary": "No textual content available.",
                "tags": ["general"],
            }

    def _llm_metadata(self, text: str, *, trace: Any | None = None) -> dict[str, Any] | None:
        self._last_llm_error = None
        llm = self._resolve_llm()
        if llm is None:
            self._last_llm_error = self._llm_resolution_error or "llm_not_available"
            return None

        prompt = (
            "Generate metadata JSON for the text. Return JSON only with keys: "
            '{"title": str, "summary": str, "tags": [str, ...]}.\n\nText:\n'
            f"{text}"
        )
        try:
            response = llm.chat([{"role": "user", "content": prompt}])
            parsed = self._parse_llm_payload(response)
            return self._validate_metadata_payload(parsed)
        except Exception as exc:
            self._last_llm_error = f"llm_metadata_failed: {exc}"
            if trace is not None and hasattr(trace, "record_stage"):
                trace.record_stage("transform_metadata_enricher_llm_error", error=str(exc))
            return None

    @staticmethod
    def _parse_llm_payload(response: Any) -> dict[str, Any]:
        if not isinstance(response, str):
            raise TypeError("LLM metadata response must be a string")
        raw = response.strip()
        if not raw:
            raise ValueError("LLM metadata response is empty")

        try:
            payload = json.loads(raw)
            if isinstance(payload, dict):
                return payload
        except json.JSONDecodeError:
            pass

        left = raw.find("{")
        right = raw.rfind("}")
        if left == -1 or right == -1 or right <= left:
            raise ValueError("LLM metadata response does not contain a JSON object")
        payload = json.loads(raw[left : right + 1])
        if not isinstance(payload, dict):
            raise ValueError("LLM metadata JSON root must be an object")
        return payload

    @staticmethod
    def _validate_metadata_payload(payload: dict[str, Any]) -> dict[str, Any]:
        title = payload.get("title")
        summary = payload.get("summary")
        tags = payload.get("tags")

        if not isinstance(title, str) or not title.strip():
            raise ValueError("LLM metadata missing valid title")
        if not isinstance(summary, str) or not summary.strip():
            raise ValueError("LLM metadata missing valid summary")
        if not isinstance(tags, list):
            raise ValueError("LLM metadata missing valid tags list")

        clean_tags: list[str] = []
        for item in tags:
            if not isinstance(item, str) or not item.strip():
                continue
            tag = item.strip().lower()
            if tag not in clean_tags:
                clean_tags.append(tag)

        if not clean_tags:
            raise ValueError("LLM metadata tags must contain at least one non-empty tag")

        return {
            "title": title.strip(),
            "summary": summary.strip(),
            "tags": clean_tags[:8],
        }

    @staticmethod
    def _build_title(text: str) -> str:
        first_sentence = _SENTENCE_SPLIT_PATTERN.split(text, maxsplit=1)[0].strip()
        if not first_sentence:
            return "Untitled chunk"
        if len(first_sentence) <= 72:
            return first_sentence
        truncated = first_sentence[:72].rstrip()
        return f"{truncated}..."

    @staticmethod
    def _build_summary(text: str) -> str:
        sentences = [s.strip() for s in _SENTENCE_SPLIT_PATTERN.split(text) if s.strip()]
        if not sentences:
            return "No textual content available."
        summary = " ".join(sentences[:2]).strip()
        if len(summary) <= 220:
            return summary
        return f"{summary[:220].rstrip()}..."

    @staticmethod
    def _build_tags(text: str) -> list[str]:
        counts: dict[str, int] = {}
        for token in _WORD_PATTERN.findall(text.lower()):
            if token in _STOP_WORDS:
                continue
            counts[token] = counts.get(token, 0) + 1
        if not counts:
            return ["general"]
        ranked = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
        return [token for token, _ in ranked[:8]]

    @staticmethod
    def _resolve_use_llm(settings: Any) -> bool:
        section = MetadataEnricher._extract_metadata_enricher_settings(settings)
        value = section.get("use_llm", False)
        if isinstance(value, bool):
            return value
        return bool(value)

    @staticmethod
    def _extract_metadata_enricher_settings(settings: Any) -> dict[str, Any]:
        if isinstance(settings, dict):
            ingestion = settings.get("ingestion")
        else:
            ingestion = getattr(settings, "ingestion", None)

        if isinstance(ingestion, dict):
            metadata_enricher = ingestion.get("metadata_enricher")
            if isinstance(metadata_enricher, dict):
                return dict(metadata_enricher)
        return {}

    @staticmethod
    def _with_metadata(
        chunk: Chunk,
        *,
        metadata_patch: dict[str, Any],
        enriched_by: str,
        fallback_reason: str | None,
    ) -> Chunk:
        metadata = dict(chunk.metadata)
        metadata.update(metadata_patch)
        metadata["metadata_enriched_by"] = enriched_by
        if fallback_reason:
            metadata["metadata_fallback_reason"] = fallback_reason
        else:
            metadata.pop("metadata_fallback_reason", None)
        return Chunk(
            id=chunk.id,
            text=chunk.text,
            metadata=metadata,
            start_offset=chunk.start_offset,
            end_offset=chunk.end_offset,
            source_ref=chunk.source_ref,
        )
