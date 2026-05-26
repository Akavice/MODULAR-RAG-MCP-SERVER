"""Local persistent vector store with a Chroma-like interface."""

from __future__ import annotations

import json
import math
import re
from pathlib import Path
from typing import Any

from libs.vector_store.base_vector_store import BaseVectorStore, QueryMatch


class ChromaStore(BaseVectorStore):
    """Minimal local vector store backend persisted to disk as JSON."""

    def __init__(
        self,
        *,
        collection_name: str = "default",
        persist_directory: str = "data/db/chroma",
        distance_metric: str = "cosine",
        embedding_provider: str | None = None,
        embedding_model: str | None = None,
        embedding_dimension: int | None = None,
        **options: Any,
    ) -> None:
        super().__init__(collection_name=collection_name, **options)
        self.persist_directory = Path(persist_directory)
        self.distance_metric = distance_metric
        self._signature: dict[str, Any] = {}
        self._requested_signature = self._normalize_signature(
            provider=embedding_provider,
            model=embedding_model,
            dimension=embedding_dimension,
        )
        self.persist_directory.mkdir(parents=True, exist_ok=True)
        self._records: dict[str, dict[str, Any]] = {}
        self._collection_file = self.persist_directory / f"{self._safe_name(collection_name)}.json"
        self._load()
        self._initialize_signature_state()

    def upsert(self, records: list[dict[str, Any]], trace: Any | None = None) -> int:
        self.validate_records(records)
        expected_dim = self._get_expected_dimension()
        incoming_dims = {len(record["vector"]) for record in records}
        if len(incoming_dims) > 1:
            raise ValueError("vector dimension mismatch in upsert payload")
        incoming_dim = next(iter(incoming_dims))
        if expected_dim is not None and incoming_dim != expected_dim:
            raise ValueError(
                f"vector dimension mismatch: expected {expected_dim}, got {incoming_dim}"
            )
        self._set_signature_dimension_if_missing(incoming_dim)

        for record in records:
            metadata = record.get("metadata", {})
            if metadata is None:
                metadata = {}
            self._records[record["id"]] = {
                "id": record["id"],
                "vector": [float(value) for value in record["vector"]],
                "text": str(record.get("text", "")),
                "metadata": dict(metadata) if isinstance(metadata, dict) else dict(metadata),
            }
        self._persist()
        return len(records)

    def query(
        self,
        vector: list[float],
        top_k: int = 5,
        filters: dict[str, Any] | None = None,
        trace: Any | None = None,
    ) -> list[QueryMatch]:
        self.validate_query_inputs(vector=vector, top_k=top_k, filters=filters)
        query_vector = [float(value) for value in vector]
        expected_dim = self._get_expected_dimension()
        if expected_dim is not None and len(query_vector) != expected_dim:
            raise ValueError(
                f"query vector dimension mismatch: expected {expected_dim}, got {len(query_vector)}"
            )
        candidates = list(self._records.values())

        if filters:
            candidates = [
                item
                for item in candidates
                if all(item.get("metadata", {}).get(key) == value for key, value in filters.items())
            ]

        scored: list[QueryMatch] = []
        for item in candidates:
            item_vector = item.get("vector", [])
            if not isinstance(item_vector, list) or not item_vector:
                continue
            score = self._similarity(query_vector, item_vector)
            scored.append(
                {
                    "id": item["id"],
                    "score": float(score),
                    "text": item.get("text", ""),
                    "metadata": dict(item.get("metadata", {})),
                }
            )

        scored.sort(key=lambda match: (-match["score"], str(match["id"])))
        return scored[:top_k]

    def get_by_ids(self, ids: list[str]) -> list[dict[str, Any]]:
        if not isinstance(ids, list):
            raise TypeError("ids must be a list")
        output: list[dict[str, Any]] = []
        for index, item_id in enumerate(ids):
            if not isinstance(item_id, str) or not item_id.strip():
                raise ValueError(f"ids[{index}] must be a non-empty string")
            record = self._records.get(item_id)
            if not isinstance(record, dict):
                continue
            metadata = record.get("metadata", {})
            output.append(
                {
                    "id": str(record.get("id", item_id)),
                    "text": str(record.get("text", "")),
                    "metadata": dict(metadata) if isinstance(metadata, dict) else {},
                }
            )
        return output

    def _similarity(self, left: list[float], right: list[float]) -> float:
        if self.distance_metric != "cosine":
            # Default to dot product for unknown metrics to keep behavior deterministic.
            return float(sum(a * b for a, b in zip(left, right)))

        dot = float(sum(a * b for a, b in zip(left, right)))
        left_norm = math.sqrt(sum(a * a for a in left))
        right_norm = math.sqrt(sum(b * b for b in right))
        if left_norm == 0.0 or right_norm == 0.0:
            return 0.0
        return dot / (left_norm * right_norm)

    def _load(self) -> None:
        if not self._collection_file.exists():
            self._records = {}
            return
        try:
            payload = json.loads(self._collection_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            payload = {}
        if isinstance(payload, dict):
            records = payload.get("records", {})
            if isinstance(records, dict):
                self._records = {
                    str(key): value
                    for key, value in records.items()
                    if isinstance(value, dict)
                }
            signature = payload.get("signature")
            if isinstance(signature, dict):
                self._signature = dict(signature)

    def _persist(self) -> None:
        payload = {
            "collection_name": self.collection_name,
            "signature": self._signature,
            "records": self._records,
        }
        tmp_file = self._collection_file.with_suffix(".tmp")
        tmp_file.write_text(json.dumps(payload, ensure_ascii=True), encoding="utf-8")
        tmp_file.replace(self._collection_file)

    def _get_collection_dimension(self) -> int | None:
        if not self._records:
            return None
        dims = {
            len(item["vector"])
            for item in self._records.values()
            if isinstance(item, dict) and isinstance(item.get("vector"), list)
        }
        if not dims:
            return None
        if len(dims) > 1:
            raise ValueError("stored vector dimension mismatch in collection")
        return next(iter(dims))

    def _get_expected_dimension(self) -> int | None:
        signature_dim = self._signature.get("dimension")
        if isinstance(signature_dim, int):
            return signature_dim
        return self._get_collection_dimension()

    def _initialize_signature_state(self) -> None:
        stored = self._normalize_signature_from_dict(self._signature)
        requested = self._requested_signature
        records_dim = self._get_collection_dimension()

        if stored and requested:
            self._assert_signature_compatible(stored, requested)
            self._signature = self._merge_signatures(stored, requested)
        elif stored:
            self._signature = stored
        elif requested:
            self._signature = requested
        else:
            self._signature = {}

        if records_dim is not None:
            current_dim = self._signature.get("dimension")
            if current_dim is None:
                self._signature["dimension"] = records_dim
            elif current_dim != records_dim:
                raise ValueError(
                    "embedding signature mismatch: "
                    f"configured dimension {current_dim}, stored vectors {records_dim}"
                )

        if self._collection_file.exists() and self._signature != stored:
            self._persist()

    def _set_signature_dimension_if_missing(self, dimension: int) -> None:
        current = self._signature.get("dimension")
        if current is None:
            self._signature["dimension"] = dimension
        elif current != dimension:
            raise ValueError(
                f"embedding signature mismatch: expected dimension {current}, got {dimension}"
            )

    @staticmethod
    def _normalize_signature(
        *,
        provider: str | None,
        model: str | None,
        dimension: int | None,
    ) -> dict[str, Any]:
        signature: dict[str, Any] = {}
        if isinstance(provider, str) and provider.strip():
            signature["provider"] = provider.strip()
        if isinstance(model, str) and model.strip():
            signature["model"] = model.strip()
        if dimension is not None:
            if isinstance(dimension, bool) or not isinstance(dimension, int) or dimension <= 0:
                raise ValueError("embedding_signature.dimension must be a positive integer")
            signature["dimension"] = dimension
        return signature

    @staticmethod
    def _normalize_signature_from_dict(raw: dict[str, Any] | None) -> dict[str, Any]:
        if not isinstance(raw, dict):
            return {}
        return ChromaStore._normalize_signature(
            provider=raw.get("provider"),
            model=raw.get("model"),
            dimension=raw.get("dimension"),
        )

    @staticmethod
    def _assert_signature_compatible(
        stored: dict[str, Any],
        requested: dict[str, Any],
    ) -> None:
        for field in ("provider", "model", "dimension"):
            stored_value = stored.get(field)
            requested_value = requested.get(field)
            if stored_value is None or requested_value is None:
                continue
            if stored_value != requested_value:
                raise ValueError(
                    "embedding signature mismatch: "
                    f"{field} stored={stored_value} requested={requested_value}"
                )

    @staticmethod
    def _merge_signatures(left: dict[str, Any], right: dict[str, Any]) -> dict[str, Any]:
        merged = dict(left)
        merged.update(right)
        return merged

    @staticmethod
    def _safe_name(name: str) -> str:
        safe = re.sub(r"[^A-Za-z0-9._-]+", "_", name.strip())
        return safe or "default"
