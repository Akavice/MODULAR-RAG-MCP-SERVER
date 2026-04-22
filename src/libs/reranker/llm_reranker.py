"""LLM-based reranker implementation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from libs.llm.base_llm import BaseLLM
from libs.llm.llm_factory import LLMFactory
from libs.reranker.base_reranker import BaseReranker, RerankCandidate


class LLMReranker(BaseReranker):
    """Rerank candidates with an LLM and structured ranked-id output."""

    def __init__(
        self,
        *,
        llm: BaseLLM | None = None,
        llm_settings: dict[str, Any] | None = None,
        prompt_path: str = "config/prompts/rerank.txt",
        prompt_template: str | None = None,
        **options: Any,
    ) -> None:
        super().__init__(**options)
        self.prompt_path = prompt_path
        self.prompt_template = prompt_template
        self.llm = llm
        self.llm_settings = dict(llm_settings or {})

    def rerank(
        self,
        query: str,
        candidates: list[dict[str, Any]],
        trace: Any | None = None,
    ) -> list[RerankCandidate]:
        self.validate_inputs(query=query, candidates=candidates)
        if not candidates:
            return []

        llm = self._resolve_llm()
        prompt = self._build_prompt(query=query, candidates=candidates)
        response_text = llm.chat([{"role": "user", "content": prompt}])
        ranked_ids = self._parse_ranked_ids(response_text=response_text)
        return self._reorder_candidates(candidates=candidates, ranked_ids=ranked_ids)

    def _resolve_llm(self) -> BaseLLM:
        if self.llm is not None:
            return self.llm
        settings = self.llm_settings or {"provider": "openai"}
        return LLMFactory.create({"llm": settings})

    def _build_prompt(self, *, query: str, candidates: list[dict[str, Any]]) -> str:
        template = self.prompt_template or self._read_prompt_file()
        rendered_candidates = "\n".join(
            f"- id={item.get('id', '')} text={str(item.get('text', ''))}"
            for item in candidates
        )
        instructions = (
            "Return strict JSON only with shape: "
            '{"ranked_ids": ["id1", "id2", "..."]}'
        )
        return (
            f"{template.strip()}\n\n"
            f"{instructions}\n\n"
            f"Query:\n{query}\n\n"
            f"Candidates:\n{rendered_candidates}\n"
        )

    def _read_prompt_file(self) -> str:
        path = Path(self.prompt_path)
        if path.exists():
            content = path.read_text(encoding="utf-8").strip()
            if content:
                return content
        return "Rank candidates by relevance to the query."

    def _parse_ranked_ids(self, *, response_text: str) -> list[str]:
        payload = self._parse_json_payload(response_text)
        ranked_ids = payload.get("ranked_ids")
        if not isinstance(ranked_ids, list):
            raise ValueError("LLM reranker response schema invalid: missing ranked_ids")

        normalized: list[str] = []
        for index, item in enumerate(ranked_ids):
            if not isinstance(item, str) or not item.strip():
                raise ValueError(
                    f"LLM reranker response schema invalid: ranked_ids[{index}] must be a non-empty string"
                )
            normalized.append(item.strip())
        return normalized

    def _parse_json_payload(self, response_text: str) -> dict[str, Any]:
        raw = response_text.strip()
        if not raw:
            raise ValueError("LLM reranker response schema invalid: empty response")

        try:
            payload = json.loads(raw)
            if isinstance(payload, dict):
                return payload
        except json.JSONDecodeError:
            pass

        left = raw.find("{")
        right = raw.rfind("}")
        if left == -1 or right == -1 or right <= left:
            raise ValueError("LLM reranker response schema invalid: JSON object not found")
        try:
            payload = json.loads(raw[left : right + 1])
        except json.JSONDecodeError as exc:
            raise ValueError("LLM reranker response schema invalid: invalid JSON object") from exc
        if not isinstance(payload, dict):
            raise ValueError("LLM reranker response schema invalid: JSON root must be an object")
        return payload

    @staticmethod
    def _reorder_candidates(
        *,
        candidates: list[dict[str, Any]],
        ranked_ids: list[str],
    ) -> list[RerankCandidate]:
        id_to_indices: dict[str, list[int]] = {}
        for index, item in enumerate(candidates):
            candidate_id = str(item.get("id", "")).strip()
            if candidate_id:
                id_to_indices.setdefault(candidate_id, []).append(index)

        ordered: list[RerankCandidate] = []
        used_indices: set[int] = set()

        for item_id in ranked_ids:
            for index in id_to_indices.get(item_id, []):
                if index not in used_indices:
                    ordered.append(dict(candidates[index]))
                    used_indices.add(index)

        for index, item in enumerate(candidates):
            if index not in used_indices:
                ordered.append(dict(item))
                used_indices.add(index)

        return ordered
