"""Assemble multimodal (text + image) payload for MCP responses."""

from __future__ import annotations

import base64
from pathlib import Path
from typing import Any

from core.types import RetrievalResult


class MultimodalAssembler:
    """Append image blocks when retrieval results reference local images."""

    def assemble(
        self,
        base_payload: dict[str, Any],
        retrieval_results: list[RetrievalResult],
    ) -> dict[str, Any]:
        payload = dict(base_payload)
        content = payload.get("content")
        if not isinstance(content, list):
            content = []
            payload["content"] = content

        for item in retrieval_results:
            images = item.metadata.get("images")
            if not isinstance(images, list):
                continue
            for image in images:
                if not isinstance(image, dict):
                    continue
                path_value = image.get("path")
                if not isinstance(path_value, str) or not path_value.strip():
                    continue
                image_path = Path(path_value.strip())
                if not image_path.exists() or not image_path.is_file():
                    continue
                mime_type = self._guess_mime_type(image_path.suffix.lower())
                encoded = base64.b64encode(image_path.read_bytes()).decode("ascii")
                content.append(
                    {
                        "type": "image",
                        "mimeType": mime_type,
                        "data": encoded,
                    }
                )
        return payload

    @staticmethod
    def _guess_mime_type(suffix: str) -> str:
        if suffix == ".png":
            return "image/png"
        if suffix in (".jpg", ".jpeg"):
            return "image/jpeg"
        if suffix == ".webp":
            return "image/webp"
        return "application/octet-stream"
