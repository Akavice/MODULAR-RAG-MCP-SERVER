"""Contract tests for BaseVectorStore and VectorStoreFactory."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pytest

from libs.vector_store.base_vector_store import BaseVectorStore, QueryMatch
from libs.vector_store.vector_store_factory import VectorStoreFactory


class FakeVectorStore(BaseVectorStore):
    """In-memory fake implementation for contract and factory tests."""

    def __init__(self, *, collection_name: str = "default", **options: Any) -> None:
        super().__init__(collection_name=collection_name, **options)
        self._records: dict[str, dict[str, Any]] = {}

    def upsert(self, records: list[dict[str, Any]], trace: Any | None = None) -> int:
        self.validate_records(records)
        for record in records:
            self._records[record["id"]] = {
                "id": record["id"],
                "vector": [float(value) for value in record["vector"]],
                "text": record.get("text", ""),
                "metadata": dict(record.get("metadata", {})),
            }
        return len(records)

    def query(
        self,
        vector: list[float],
        top_k: int = 5,
        filters: dict[str, Any] | None = None,
        trace: Any | None = None,
    ) -> list[QueryMatch]:
        self.validate_query_inputs(vector=vector, top_k=top_k, filters=filters)

        candidates = list(self._records.values())
        if filters:
            candidates = [
                item
                for item in candidates
                if all(item["metadata"].get(key) == value for key, value in filters.items())
            ]

        scored = []
        for item in candidates:
            score = sum(left * right for left, right in zip(item["vector"], vector))
            scored.append(
                {
                    "id": item["id"],
                    "score": float(score),
                    "text": item["text"],
                    "metadata": item["metadata"],
                }
            )

        scored.sort(key=lambda match: match["score"], reverse=True)
        return scored[:top_k]


@dataclass(slots=True)
class FakeSettings:
    """Minimal settings object exposing `.vector_store` mapping."""

    vector_store: dict[str, Any]


@pytest.fixture(autouse=True)
def reset_vector_store_registry() -> None:
    """Ensure tests do not leak registered providers across cases."""
    VectorStoreFactory.clear_registry()
    yield
    VectorStoreFactory.clear_registry()


@pytest.mark.unit
def test_upsert_returns_processed_count_for_valid_contract_shape() -> None:
    store = FakeVectorStore()
    records = [
        {
            "id": "doc-1",
            "vector": [0.1, 0.2, 0.3],
            "text": "hello",
            "metadata": {"source": "a"},
        },
        {"id": "doc-2", "vector": [0.3, 0.1, 0.0], "metadata": {"source": "b"}},
    ]

    inserted = store.upsert(records)

    assert inserted == 2


@pytest.mark.unit
def test_upsert_rejects_invalid_record_shape() -> None:
    store = FakeVectorStore()

    with pytest.raises(ValueError, match="valid id"):
        store.upsert([{"vector": [0.1, 0.2]}])


@pytest.mark.unit
def test_query_returns_expected_output_shape_and_respects_top_k() -> None:
    store = FakeVectorStore()
    store.upsert(
        [
            {"id": "doc-1", "vector": [1.0, 0.0], "metadata": {"source": "a"}},
            {"id": "doc-2", "vector": [0.5, 0.5], "metadata": {"source": "a"}},
            {"id": "doc-3", "vector": [0.0, 1.0], "metadata": {"source": "b"}},
        ]
    )

    matches = store.query(vector=[1.0, 0.0], top_k=2, filters={"source": "a"})

    assert len(matches) == 2
    assert matches[0]["id"] == "doc-1"
    assert isinstance(matches[0]["score"], float)
    assert isinstance(matches[0]["metadata"], dict)


@pytest.mark.unit
def test_query_rejects_invalid_query_shape() -> None:
    store = FakeVectorStore()

    with pytest.raises(TypeError, match="sequence"):
        store.query(vector="invalid", top_k=1)


@pytest.mark.unit
def test_factory_create_routes_by_provider_from_nested_mapping() -> None:
    VectorStoreFactory.register("fake", FakeVectorStore)

    store = VectorStoreFactory.create(
        {
            "vector_store": {
                "provider": "fake",
                "collection_name": "knowledge",
                "persist_directory": "data/db/chroma",
            }
        }
    )

    assert isinstance(store, FakeVectorStore)
    assert store.collection_name == "knowledge"
    assert store.options["persist_directory"] == "data/db/chroma"


@pytest.mark.unit
def test_factory_create_accepts_object_settings() -> None:
    VectorStoreFactory.register("fake", FakeVectorStore)
    settings = FakeSettings(
        vector_store={"provider": "fake", "collection_name": "default"}
    )

    store = VectorStoreFactory.create(settings)

    assert isinstance(store, FakeVectorStore)


@pytest.mark.unit
def test_factory_raises_for_missing_provider() -> None:
    VectorStoreFactory.register("fake", FakeVectorStore)

    with pytest.raises(ValueError, match="vector_store.provider"):
        VectorStoreFactory.create({"vector_store": {}})


@pytest.mark.unit
def test_factory_raises_for_unknown_provider() -> None:
    VectorStoreFactory.register("fake", FakeVectorStore)

    with pytest.raises(ValueError, match="Unsupported vector_store provider"):
        VectorStoreFactory.create({"vector_store": {"provider": "unknown-provider"}})


@pytest.mark.unit
def test_factory_register_rejects_duplicate_provider_without_overwrite() -> None:
    VectorStoreFactory.register("fake", FakeVectorStore)

    with pytest.raises(ValueError, match="already registered"):
        VectorStoreFactory.register("fake", FakeVectorStore)


@pytest.mark.unit
def test_factory_register_rejects_builtin_provider_without_overwrite() -> None:
    with pytest.raises(ValueError, match="reserved by built-in vector stores"):
        VectorStoreFactory.register("chroma", FakeVectorStore)


@pytest.mark.unit
@pytest.mark.parametrize("invalid_name", [None, 123, "   "])
def test_factory_raises_for_invalid_collection_name(invalid_name: Any) -> None:
    VectorStoreFactory.register("fake", FakeVectorStore)

    with pytest.raises((TypeError, ValueError), match="vector_store.collection_name"):
        VectorStoreFactory.create(
            {
                "vector_store": {
                    "provider": "fake",
                    "collection_name": invalid_name,
                }
            }
        )
