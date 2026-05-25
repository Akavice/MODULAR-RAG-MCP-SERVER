"""Image captioning transform with graceful fallback behavior."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from core.types import Chunk
from ingestion.transform.base_transform import BaseTransform
from libs.llm.base_vision_llm import BaseVisionLLM
from libs.llm.llm_factory import LLMFactory


_DEFAULT_PROMPT_PATH = "config/prompts/image_captioning.txt"
_DEFAULT_PROMPT_TEMPLATE = (
    "Describe the image in the context of the surrounding document content.\n"
    "Focus on factual details useful for retrieval.\n\n"
    "Image ID: {image_id}\n"
    "Chunk Context:\n{chunk_text}"
)


class ImageCaptioner(BaseTransform):
    """Generate image captions for chunks containing image references."""

    def __init__(
        self,
        settings: Any,
        vision_llm: BaseVisionLLM | None = None,
        prompt_path: str | None = None,
    ) -> None:
        self.settings = settings
        self._enabled = self._resolve_enabled(settings)
        self._prompt_template = self._load_prompt(prompt_path or self._resolve_prompt_path(settings))
        self._vision_llm = vision_llm
        self._vision_llm_init_error: str | None = None

    def transform(self, chunks: list[Chunk], trace: Any | None = None) -> list[Chunk]:
        self.validate_chunks(chunks)

        output: list[Chunk] = []
        captioned_count = 0
        unprocessed_count = 0

        for chunk in chunks:
            if not self._enabled:
                output.append(self._mark_unprocessed_if_images(chunk, "captioning_disabled"))
                if chunk.metadata.get("image_refs"):
                    unprocessed_count += 1
                continue

            refs = self._extract_image_refs(chunk)
            if not refs:
                output.append(chunk)
                continue

            llm = self._resolve_vision_llm()
            if llm is None:
                output.append(
                    self._mark_unprocessed_if_images(
                        chunk, self._vision_llm_init_error or "vision_llm_not_available"
                    )
                )
                unprocessed_count += 1
                continue

            try:
                captioned_chunk, captions = self._caption_chunk(chunk, refs=refs, llm=llm)
                if captions:
                    captioned_count += 1
                else:
                    unprocessed_count += 1
                output.append(captioned_chunk)
            except Exception as exc:
                output.append(
                    self._mark_unprocessed_if_images(
                        chunk,
                        f"captioning_failed: {exc}",
                    )
                )
                unprocessed_count += 1

        if trace is not None and hasattr(trace, "record_stage"):
            trace.record_stage(
                "transform_image_captioner",
                chunk_count=len(chunks),
                enabled=self._enabled,
                captioned_count=captioned_count,
                unprocessed_count=unprocessed_count,
            )
        return output

    def _caption_chunk(
        self,
        chunk: Chunk,
        *,
        refs: list[str],
        llm: BaseVisionLLM,
    ) -> tuple[Chunk, dict[str, str]]:
        captions: dict[str, str] = {}
        images = chunk.metadata.get("images")
        image_by_id: dict[str, dict[str, Any]] = {}
        if isinstance(images, list):
            for item in images:
                if not isinstance(item, dict):
                    continue
                image_id = item.get("id")
                if isinstance(image_id, str) and image_id.strip():
                    image_by_id[image_id.strip()] = item

        for image_id in refs:
            image_item = image_by_id.get(image_id)
            if not image_item:
                continue
            image_path = image_item.get("path")
            if not isinstance(image_path, str) or not image_path.strip():
                continue
            prompt = self._render_prompt(chunk_text=chunk.text, image_id=image_id)
            response = llm.chat_with_image(prompt, image_path.strip())
            text = response.get("text") if isinstance(response, dict) else None
            if isinstance(text, str) and text.strip():
                captions[image_id] = text.strip()

        if not captions:
            return self._mark_unprocessed_if_images(chunk, "no_caption_generated"), captions

        metadata = dict(chunk.metadata)
        metadata["image_captions"] = dict(captions)
        metadata["captioned_by"] = "vision_llm"
        metadata.pop("has_unprocessed_images", None)
        metadata.pop("image_caption_fallback_reason", None)
        return (
            Chunk(
                id=chunk.id,
                text=chunk.text,
                metadata=metadata,
                start_offset=chunk.start_offset,
                end_offset=chunk.end_offset,
                source_ref=chunk.source_ref,
            ),
            captions,
        )

    def _resolve_vision_llm(self) -> BaseVisionLLM | None:
        if self._vision_llm is not None:
            return self._vision_llm
        if self._vision_llm_init_error is not None:
            return None
        try:
            self._vision_llm = LLMFactory.create_vision_llm(self.settings)
            return self._vision_llm
        except Exception as exc:
            self._vision_llm_init_error = f"vision_llm_init_failed: {exc}"
            return None

    def _render_prompt(self, *, chunk_text: str, image_id: str) -> str:
        template = self._prompt_template
        rendered = template.replace("{chunk_text}", chunk_text).replace("{image_id}", image_id)
        if rendered == template:
            return f"{template.rstrip()}\n\nImage ID: {image_id}\nChunk Context:\n{chunk_text}"
        return rendered

    @staticmethod
    def _extract_image_refs(chunk: Chunk) -> list[str]:
        refs = chunk.metadata.get("image_refs")
        if not isinstance(refs, list):
            return []
        result: list[str] = []
        for item in refs:
            if isinstance(item, str) and item.strip():
                result.append(item.strip())
        return result

    @staticmethod
    def _mark_unprocessed_if_images(chunk: Chunk, reason: str) -> Chunk:
        metadata = dict(chunk.metadata)
        refs = metadata.get("image_refs")
        has_refs = isinstance(refs, list) and any(isinstance(x, str) and x.strip() for x in refs)
        if has_refs:
            metadata["has_unprocessed_images"] = True
            metadata["image_caption_fallback_reason"] = reason
        return Chunk(
            id=chunk.id,
            text=chunk.text,
            metadata=metadata,
            start_offset=chunk.start_offset,
            end_offset=chunk.end_offset,
            source_ref=chunk.source_ref,
        )

    def _load_prompt(self, prompt_path: str) -> str:
        path = Path(prompt_path)
        if path.exists():
            content = path.read_text(encoding="utf-8").strip()
            if content:
                return content
        return _DEFAULT_PROMPT_TEMPLATE

    @staticmethod
    def _resolve_enabled(settings: Any) -> bool:
        section = ImageCaptioner._extract_image_captioner_settings(settings)
        raw = section.get("use_vision_llm", section.get("enabled", False))
        if isinstance(raw, bool):
            return raw
        return bool(raw)

    @staticmethod
    def _resolve_prompt_path(settings: Any) -> str:
        section = ImageCaptioner._extract_image_captioner_settings(settings)
        value = section.get("prompt_path")
        if isinstance(value, str) and value.strip():
            return value.strip()
        return _DEFAULT_PROMPT_PATH

    @staticmethod
    def _extract_image_captioner_settings(settings: Any) -> dict[str, Any]:
        if isinstance(settings, dict):
            ingestion = settings.get("ingestion")
        else:
            ingestion = getattr(settings, "ingestion", None)
        if isinstance(ingestion, dict):
            section = ingestion.get("image_captioner")
            if isinstance(section, dict):
                return dict(section)
        return {}
