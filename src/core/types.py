"""Shared core data contracts for ingestion and retrieval pipelines."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any, TypedDict


IMAGE_PLACEHOLDER_TEMPLATE = "[IMAGE: {image_id}]"


class ImageMetadata(TypedDict, total=False):
    """Image metadata entry embedded in document/chunk metadata."""

    id: str
    path: str
    page: int
    text_offset: int
    text_length: int
    position: dict[str, Any]


Metadata = dict[str, Any]
SparseVector = dict[str, float]


def make_image_placeholder(image_id: str) -> str:
    """Build canonical image placeholder token for document text."""
    if not isinstance(image_id, str) or not image_id.strip():
        raise ValueError("image_id must be a non-empty string")
    return IMAGE_PLACEHOLDER_TEMPLATE.format(image_id=image_id.strip())


def _require_non_empty_string(value: Any, *, field_name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must not be empty")
    return normalized


def _validate_metadata(metadata: Any) -> Metadata:
    if not isinstance(metadata, dict):
        raise TypeError("metadata must be a mapping")
    source_path = metadata.get("source_path")
    if not isinstance(source_path, str) or not source_path.strip():
        raise ValueError("metadata.source_path must be a non-empty string")
    _validate_images(metadata.get("images"))
    return dict(metadata)


def _validate_images(images: Any) -> None:
    if images is None:
        return
    if not isinstance(images, list):
        raise TypeError("metadata.images must be a list when provided")

    for index, item in enumerate(images):
        if not isinstance(item, dict):
            raise TypeError(f"metadata.images[{index}] must be a mapping")

        image_id = item.get("id")
        image_path = item.get("path")
        if not isinstance(image_id, str) or not image_id.strip():
            raise ValueError(f"metadata.images[{index}].id must be a non-empty string")
        if not isinstance(image_path, str) or not image_path.strip():
            raise ValueError(f"metadata.images[{index}].path must be a non-empty string")

        page = item.get("page")
        if page is not None and (not isinstance(page, int) or isinstance(page, bool) or page < 0):
            raise ValueError(f"metadata.images[{index}].page must be a non-negative integer")

        text_offset = item.get("text_offset")
        if text_offset is not None and (
            not isinstance(text_offset, int) or isinstance(text_offset, bool) or text_offset < 0
        ):
            raise ValueError(
                f"metadata.images[{index}].text_offset must be a non-negative integer"
            )

        text_length = item.get("text_length")
        if text_length is not None and (
            not isinstance(text_length, int) or isinstance(text_length, bool) or text_length < 0
        ):
            raise ValueError(
                f"metadata.images[{index}].text_length must be a non-negative integer"
            )

        position = item.get("position")
        if position is not None and not isinstance(position, dict):
            raise TypeError(f"metadata.images[{index}].position must be a mapping")


def _validate_dense_vector(vector: Any) -> list[float] | None:
    if vector is None:
        return None
    if not isinstance(vector, list):
        raise TypeError("dense_vector must be a list when provided")
    normalized: list[float] = []
    for index, value in enumerate(vector):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError(f"dense_vector[{index}] must be numeric")
        numeric = float(value)
        if not math.isfinite(numeric):
            raise ValueError(f"dense_vector[{index}] must be finite")
        normalized.append(numeric)
    return normalized


def _validate_sparse_vector(vector: Any) -> SparseVector | None:
    if vector is None:
        return None
    if not isinstance(vector, dict):
        raise TypeError("sparse_vector must be a mapping when provided")

    normalized: SparseVector = {}
    for key, value in vector.items():
        if not isinstance(key, str) or not key.strip():
            raise TypeError("sparse_vector keys must be non-empty strings")
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError(f"sparse_vector['{key}'] must be numeric")
        numeric = float(value)
        if not math.isfinite(numeric):
            raise ValueError(f"sparse_vector['{key}'] must be finite")
        normalized[key] = numeric
    return normalized


@dataclass(slots=True)
class Document:
    """Canonical raw document representation produced by loaders."""

    id: str
    text: str
    metadata: Metadata

    def __post_init__(self) -> None:
        self.id = _require_non_empty_string(self.id, field_name="id")
        if not isinstance(self.text, str):
            raise TypeError("text must be a string")
        self.metadata = _validate_metadata(self.metadata)

    def to_dict(self) -> dict[str, Any]:
        return {"id": self.id, "text": self.text, "metadata": dict(self.metadata)}

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> Document:
        if not isinstance(payload, dict):
            raise TypeError("payload must be a mapping")
        return cls(
            id=payload.get("id"),
            text=payload.get("text", ""),
            metadata=payload.get("metadata", {}),
        )


@dataclass(slots=True)
class Chunk:
    """Canonical text chunk representation between split/transform/index stages."""

    id: str
    text: str
    metadata: Metadata
    start_offset: int
    end_offset: int
    source_ref: str | None = None

    def __post_init__(self) -> None:
        self.id = _require_non_empty_string(self.id, field_name="id")
        if not isinstance(self.text, str):
            raise TypeError("text must be a string")
        self.metadata = _validate_metadata(self.metadata)
        if not isinstance(self.start_offset, int) or isinstance(self.start_offset, bool):
            raise TypeError("start_offset must be an integer")
        if not isinstance(self.end_offset, int) or isinstance(self.end_offset, bool):
            raise TypeError("end_offset must be an integer")
        if self.start_offset < 0 or self.end_offset < 0:
            raise ValueError("start_offset/end_offset must be non-negative")
        if self.end_offset < self.start_offset:
            raise ValueError("end_offset must be greater than or equal to start_offset")
        if self.source_ref is not None and (
            not isinstance(self.source_ref, str) or not self.source_ref.strip()
        ):
            raise ValueError("source_ref must be a non-empty string when provided")

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "text": self.text,
            "metadata": dict(self.metadata),
            "start_offset": self.start_offset,
            "end_offset": self.end_offset,
            "source_ref": self.source_ref,
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> Chunk:
        if not isinstance(payload, dict):
            raise TypeError("payload must be a mapping")
        return cls(
            id=payload.get("id"),
            text=payload.get("text", ""),
            metadata=payload.get("metadata", {}),
            start_offset=payload.get("start_offset", 0),
            end_offset=payload.get("end_offset", 0),
            source_ref=payload.get("source_ref"),
        )


@dataclass(slots=True)
class ChunkRecord:
    """Chunk storage/retrieval carrier with optional dense/sparse vectors."""

    id: str
    text: str
    metadata: Metadata
    dense_vector: list[float] | None = None
    sparse_vector: SparseVector | None = None

    def __post_init__(self) -> None:
        self.id = _require_non_empty_string(self.id, field_name="id")
        if not isinstance(self.text, str):
            raise TypeError("text must be a string")
        self.metadata = _validate_metadata(self.metadata)
        self.dense_vector = _validate_dense_vector(self.dense_vector)
        self.sparse_vector = _validate_sparse_vector(self.sparse_vector)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "text": self.text,
            "metadata": dict(self.metadata),
            "dense_vector": list(self.dense_vector) if self.dense_vector is not None else None,
            "sparse_vector": dict(self.sparse_vector) if self.sparse_vector is not None else None,
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> ChunkRecord:
        if not isinstance(payload, dict):
            raise TypeError("payload must be a mapping")
        return cls(
            id=payload.get("id"),
            text=payload.get("text", ""),
            metadata=payload.get("metadata", {}),
            dense_vector=payload.get("dense_vector"),
            sparse_vector=payload.get("sparse_vector"),
        )
