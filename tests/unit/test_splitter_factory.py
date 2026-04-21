"""Unit tests for splitter factory routing and validation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pytest

from libs.splitter.base_splitter import BaseSplitter
from libs.splitter.splitter_factory import SplitterFactory


class FakeSplitter(BaseSplitter):
    """Small fake splitter implementation used in factory tests."""

    def split(self, text: str, trace: Any | None = None) -> list[str]:
        self.validate_text(text)
        midpoint = max(1, min(len(text), self.chunk_size))
        return [text[:midpoint], text[midpoint:]] if len(text) > midpoint else [text]


@dataclass(slots=True)
class FakeSettings:
    """Minimal settings object exposing `.splitter` mapping."""

    splitter: dict[str, Any]


@pytest.fixture(autouse=True)
def reset_splitter_registry() -> None:
    """Ensure tests do not leak registered providers across cases."""
    SplitterFactory.clear_registry()
    yield
    SplitterFactory.clear_registry()


@pytest.mark.unit
def test_create_routes_by_provider_from_nested_mapping() -> None:
    SplitterFactory.register("recursive", FakeSplitter)

    splitter = SplitterFactory.create(
        {
            "splitter": {
                "provider": "recursive",
                "chunk_size": 128,
                "chunk_overlap": 16,
                "separator": "\n\n",
            }
        }
    )

    assert isinstance(splitter, FakeSplitter)
    assert splitter.chunk_size == 128
    assert splitter.chunk_overlap == 16
    assert splitter.options["separator"] == "\n\n"


@pytest.mark.unit
def test_create_accepts_direct_splitter_mapping() -> None:
    SplitterFactory.register("fixed", FakeSplitter)

    splitter = SplitterFactory.create(
        {"provider": "fixed", "chunk_size": 64, "chunk_overlap": 8}
    )

    assert isinstance(splitter, FakeSplitter)
    assert splitter.chunk_size == 64
    assert splitter.chunk_overlap == 8


@pytest.mark.unit
def test_create_accepts_object_settings() -> None:
    SplitterFactory.register("semantic", FakeSplitter)
    settings = FakeSettings(
        splitter={"provider": "semantic", "chunk_size": 256, "chunk_overlap": 32}
    )

    splitter = SplitterFactory.create(settings)

    assert isinstance(splitter, FakeSplitter)
    assert splitter.chunk_size == 256


@pytest.mark.unit
def test_create_raises_for_missing_provider() -> None:
    SplitterFactory.register("fixed", FakeSplitter)

    with pytest.raises(ValueError, match="splitter.provider"):
        SplitterFactory.create({"splitter": {}})


@pytest.mark.unit
def test_create_raises_for_unregistered_provider() -> None:
    SplitterFactory.register("fixed", FakeSplitter)

    with pytest.raises(ValueError, match="Registered providers: fixed"):
        SplitterFactory.create({"splitter": {"provider": "unknown"}})


@pytest.mark.unit
def test_register_raises_when_duplicate_provider_without_overwrite() -> None:
    SplitterFactory.register("recursive", FakeSplitter)

    with pytest.raises(ValueError, match="already registered"):
        SplitterFactory.register("recursive", FakeSplitter)


@pytest.mark.unit
def test_create_raises_for_non_integer_chunk_size() -> None:
    SplitterFactory.register("fixed", FakeSplitter)

    with pytest.raises(TypeError, match="splitter.chunk_size"):
        SplitterFactory.create(
            {"splitter": {"provider": "fixed", "chunk_size": "128", "chunk_overlap": 8}}
        )


@pytest.mark.unit
def test_create_raises_for_negative_chunk_size() -> None:
    SplitterFactory.register("fixed", FakeSplitter)

    with pytest.raises(ValueError, match="splitter.chunk_size"):
        SplitterFactory.create(
            {"splitter": {"provider": "fixed", "chunk_size": -1, "chunk_overlap": 0}}
        )


@pytest.mark.unit
def test_create_raises_when_chunk_overlap_is_not_smaller_than_chunk_size() -> None:
    SplitterFactory.register("fixed", FakeSplitter)

    with pytest.raises(ValueError, match="splitter.chunk_overlap"):
        SplitterFactory.create(
            {"splitter": {"provider": "fixed", "chunk_size": 64, "chunk_overlap": 64}}
        )
