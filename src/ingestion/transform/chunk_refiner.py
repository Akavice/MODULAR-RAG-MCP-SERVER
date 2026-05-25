"""Chunk refinement transform with rule-based cleanup and optional LLM rewrite."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from core.types import Chunk
from ingestion.transform.base_transform import BaseTransform
from libs.llm.base_llm import BaseLLM
from libs.llm.llm_factory import LLMFactory


_DEFAULT_PROMPT_PATH = "config/prompts/chunk_refinement.txt"
_DEFAULT_PROMPT_TEMPLATE = (
    "Clean and refine the following text while preserving meaning. "
    "Remove obvious OCR noise and layout artifacts.\n\n{text}"
)
_HTML_COMMENT_PATTERN = re.compile(r"<!--[\s\S]*?-->")
_WHITESPACE_PATTERN = re.compile(r"[ \t]+")
_MARKER_LINE_PATTERN = re.compile(r"^\s*([*_=~-])\1{2,}\s*$")
_PAGE_NOISE_PATTERNS = (
    re.compile(r"^\s*page\s+\d+(\s*(?:/|of)\s*\d+)?\s*$", re.IGNORECASE),
    re.compile(r"^\s*\d+\s*(?:/|of)\s*\d+\s*$", re.IGNORECASE),
)
_CODE_FENCE_PATTERN = re.compile(r"(```[\s\S]*?```)")


class ChunkRefiner(BaseTransform):
    """Refine chunks with deterministic cleanup and optional LLM enhancement."""

    def __init__(
        self,
        settings: Any,
        llm: BaseLLM | None = None,
        prompt_path: str | None = None,
    ) -> None:
        self.settings = settings
        self._use_llm = self._resolve_use_llm(settings)
        self._prompt_path = prompt_path or self._resolve_prompt_path(settings)
        self._prompt_template = self._load_prompt(self._prompt_path)
        self._llm = llm
        self._llm_resolution_error: str | None = None
        self._last_llm_error: str | None = None

    def transform(self, chunks: list[Chunk], trace: Any | None = None) -> list[Chunk]:
        self.validate_chunks(chunks)

        refined_chunks: list[Chunk] = []
        llm_refined_count = 0
        rule_refined_count = 0
        fallback_count = 0

        for chunk in chunks:
            try:
                refined_chunk, refined_by = self._refine_chunk(chunk, trace=trace)
            except Exception as exc:
                fallback_count += 1
                refined_chunk = self._with_metadata(
                    chunk,
                    text=chunk.text,
                    refined_by="rule",
                    fallback_reason=f"chunk_processing_failed: {exc}",
                )
                refined_by = "rule"

            if refined_by == "llm":
                llm_refined_count += 1
            else:
                rule_refined_count += 1
                if refined_chunk.metadata.get("refine_fallback_reason"):
                    fallback_count += 1

            refined_chunks.append(refined_chunk)

        if trace is not None and hasattr(trace, "record_stage"):
            trace.record_stage(
                "transform_chunk_refiner",
                chunk_count=len(chunks),
                llm_enabled=self._use_llm,
                llm_refined_count=llm_refined_count,
                rule_refined_count=rule_refined_count,
                fallback_count=fallback_count,
            )
        return refined_chunks

    def _refine_chunk(self, chunk: Chunk, *, trace: Any | None = None) -> tuple[Chunk, str]:
        rule_text = self._rule_based_refine(chunk.text)
        if not self._use_llm:
            return (
                self._with_metadata(
                    chunk,
                    text=rule_text,
                    refined_by="rule",
                    fallback_reason=None,
                ),
                "rule",
            )

        llm_text = self._llm_refine(rule_text, trace)
        if llm_text is None:
            return (
                self._with_metadata(
                    chunk,
                    text=rule_text,
                    refined_by="rule",
                    fallback_reason=self._last_llm_error or self._llm_resolution_error,
                ),
                "rule",
            )
        return (
            self._with_metadata(
                chunk,
                text=llm_text,
                refined_by="llm",
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

    def _rule_based_refine(self, text: str) -> str:
        if not isinstance(text, str):
            raise TypeError("chunk text must be a string")
        if not text:
            return ""

        normalized = text.replace("\r\n", "\n").replace("\r", "\n")
        parts = _CODE_FENCE_PATTERN.split(normalized)
        cleaned_parts: list[str] = []
        for index, part in enumerate(parts):
            if index % 2 == 1:
                cleaned_parts.append(part)
                continue
            cleaned_parts.append(self._clean_text_segment(part))
        merged = ""
        for part in cleaned_parts:
            if not part:
                continue
            if merged and not merged.endswith("\n") and not part.startswith("\n"):
                merged += "\n"
            merged += part
        return merged.strip()

    def _clean_text_segment(self, text: str) -> str:
        without_comments = _HTML_COMMENT_PATTERN.sub("", text)
        lines = without_comments.split("\n")
        output_lines: list[str] = []
        pending_blank = False

        for line in lines:
            compacted = _WHITESPACE_PATTERN.sub(" ", line).strip()
            if self._is_page_noise_line(compacted):
                continue
            if _MARKER_LINE_PATTERN.match(compacted):
                continue

            if not compacted:
                if output_lines and not pending_blank:
                    output_lines.append("")
                    pending_blank = True
                continue

            output_lines.append(compacted)
            pending_blank = False

        while output_lines and output_lines[-1] == "":
            output_lines.pop()
        return "\n".join(output_lines)

    @staticmethod
    def _is_page_noise_line(line: str) -> bool:
        if not line:
            return False
        return any(pattern.match(line) for pattern in _PAGE_NOISE_PATTERNS)

    def _llm_refine(self, text: str, trace: Any | None = None) -> str | None:
        self._last_llm_error = None
        llm = self._resolve_llm()
        if llm is None:
            self._last_llm_error = self._llm_resolution_error or "llm_not_available"
            return None

        prompt = self._render_prompt(text)
        try:
            response = llm.chat([{"role": "user", "content": prompt}])
            if not isinstance(response, str):
                self._last_llm_error = "llm_response_invalid_type"
                return None
            refined = response.strip()
            if not refined:
                self._last_llm_error = "llm_response_empty"
                return None
            return refined
        except Exception as exc:
            self._last_llm_error = f"llm_refine_failed: {exc}"
            if trace is not None and hasattr(trace, "record_stage"):
                trace.record_stage(
                    "transform_chunk_refiner_llm_error",
                    error=str(exc),
                )
            return None

    def _render_prompt(self, text: str) -> str:
        template = self._prompt_template
        if "{text}" in template:
            return template.replace("{text}", text)
        return f"{template.rstrip()}\n\n{text}"

    def _load_prompt(self, prompt_path: str | None = None) -> str:
        path_value = prompt_path or _DEFAULT_PROMPT_PATH
        if not isinstance(path_value, str):
            raise TypeError("prompt_path must be a string when provided")

        path = Path(path_value)
        if path.exists():
            content = path.read_text(encoding="utf-8").strip()
            if content:
                return content
        return _DEFAULT_PROMPT_TEMPLATE

    @staticmethod
    def _resolve_use_llm(settings: Any) -> bool:
        section = ChunkRefiner._extract_chunk_refiner_settings(settings)
        value = section.get("use_llm", False)
        if isinstance(value, bool):
            return value
        return bool(value)

    @staticmethod
    def _resolve_prompt_path(settings: Any) -> str:
        section = ChunkRefiner._extract_chunk_refiner_settings(settings)
        value = section.get("prompt_path")
        if isinstance(value, str) and value.strip():
            return value.strip()
        return _DEFAULT_PROMPT_PATH

    @staticmethod
    def _extract_chunk_refiner_settings(settings: Any) -> dict[str, Any]:
        if isinstance(settings, dict):
            ingestion = settings.get("ingestion")
        else:
            ingestion = getattr(settings, "ingestion", None)

        if isinstance(ingestion, dict):
            chunk_refiner = ingestion.get("chunk_refiner")
            if isinstance(chunk_refiner, dict):
                return dict(chunk_refiner)
        return {}

    @staticmethod
    def _with_metadata(
        chunk: Chunk,
        *,
        text: str,
        refined_by: str,
        fallback_reason: str | None,
    ) -> Chunk:
        metadata = dict(chunk.metadata)
        metadata["refined_by"] = refined_by
        if fallback_reason:
            metadata["refine_fallback_reason"] = fallback_reason
        else:
            metadata.pop("refine_fallback_reason", None)
        return Chunk(
            id=chunk.id,
            text=text,
            metadata=metadata,
            start_offset=chunk.start_offset,
            end_offset=chunk.end_offset,
            source_ref=chunk.source_ref,
        )
