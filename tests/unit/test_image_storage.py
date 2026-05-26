"""Unit tests for ImageStorage."""

from __future__ import annotations

from pathlib import Path

import pytest

from ingestion.storage.image_storage import ImageStorage


@pytest.mark.unit
def test_save_and_get_path_persist_mapping(tmp_path: Path) -> None:
    image_root = tmp_path / "images"
    db_path = tmp_path / "db" / "image_index.db"
    storage = ImageStorage(image_root=str(image_root), db_path=str(db_path))

    saved = storage.save_image(
        image_id="img_001",
        content=b"\x89PNG\r\n\x1a\nfake",
        collection="kb",
        doc_hash="doc_a",
        page_num=1,
    )

    assert Path(saved).exists()
    assert storage.get_path("img_001") == saved

    # Reopen to verify persistence.
    reopened = ImageStorage(image_root=str(image_root), db_path=str(db_path))
    assert reopened.get_path("img_001") == saved


@pytest.mark.unit
def test_list_images_supports_collection_and_doc_hash_filters(tmp_path: Path) -> None:
    storage = ImageStorage(
        image_root=str(tmp_path / "images"),
        db_path=str(tmp_path / "db" / "image_index.db"),
    )
    storage.save_image(
        image_id="img_1",
        content=b"one",
        collection="a",
        doc_hash="doc_x",
        page_num=1,
    )
    storage.save_image(
        image_id="img_2",
        content=b"two",
        collection="a",
        doc_hash="doc_y",
        page_num=2,
    )
    storage.save_image(
        image_id="img_3",
        content=b"three",
        collection="b",
        doc_hash="doc_x",
        page_num=3,
    )

    in_a = storage.list_images(collection="a")
    assert [item["image_id"] for item in in_a] == ["img_1", "img_2"]

    in_doc_x = storage.list_images(doc_hash="doc_x")
    assert [item["image_id"] for item in in_doc_x] == ["img_1", "img_3"]


@pytest.mark.unit
def test_delete_image_removes_mapping_and_file(tmp_path: Path) -> None:
    storage = ImageStorage(
        image_root=str(tmp_path / "images"),
        db_path=str(tmp_path / "db" / "image_index.db"),
    )
    path = storage.save_image(
        image_id="img_del",
        content=b"abc",
        collection="kb",
        doc_hash="doc_z",
    )
    assert Path(path).exists()

    deleted = storage.delete_image("img_del")

    assert deleted is True
    assert storage.get_path("img_del") is None
    assert not Path(path).exists()


@pytest.mark.unit
def test_delete_images_by_collection_and_doc_hash(tmp_path: Path) -> None:
    storage = ImageStorage(
        image_root=str(tmp_path / "images"),
        db_path=str(tmp_path / "db" / "image_index.db"),
    )
    storage.save_image(image_id="i1", content=b"1", collection="c1", doc_hash="d1")
    storage.save_image(image_id="i2", content=b"2", collection="c1", doc_hash="d2")
    storage.save_image(image_id="i3", content=b"3", collection="c2", doc_hash="d1")

    removed = storage.delete_images(collection="c1")
    assert removed == 2
    assert [item["image_id"] for item in storage.list_images()] == ["i3"]

    removed_doc = storage.delete_images(doc_hash="d1")
    assert removed_doc == 1
    assert storage.list_images() == []


@pytest.mark.unit
def test_save_image_validates_input_contract(tmp_path: Path) -> None:
    storage = ImageStorage(
        image_root=str(tmp_path / "images"),
        db_path=str(tmp_path / "db" / "image_index.db"),
    )

    with pytest.raises(TypeError, match="image_id must be a string"):
        storage.save_image(  # type: ignore[arg-type]
            image_id=123,
            content=b"x",
            collection="kb",
        )
    with pytest.raises(ValueError, match="content must not be empty"):
        storage.save_image(image_id="x", content=b"", collection="kb")
    with pytest.raises(ValueError, match="suffix contains invalid characters"):
        storage.save_image(image_id="x", content=b"x", collection="kb", suffix="../png")


@pytest.mark.unit
def test_save_image_upserts_existing_image_id(tmp_path: Path) -> None:
    storage = ImageStorage(
        image_root=str(tmp_path / "images"),
        db_path=str(tmp_path / "db" / "image_index.db"),
    )
    first = storage.save_image(
        image_id="dup",
        content=b"v1",
        collection="kb",
        doc_hash="d1",
    )
    second = storage.save_image(
        image_id="dup",
        content=b"v2",
        collection="kb",
        doc_hash="d2",
    )

    assert first == second
    assert Path(second).read_bytes() == b"v2"
    rows = storage.list_images(collection="kb")
    assert len(rows) == 1
    assert rows[0]["doc_hash"] == "d2"
