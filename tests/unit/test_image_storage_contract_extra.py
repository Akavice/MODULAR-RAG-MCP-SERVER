"""Additional contract tests for ImageStorage edge behavior."""

from __future__ import annotations

from pathlib import Path

import pytest

from ingestion.storage.image_storage import ImageStorage


@pytest.mark.unit
def test_save_image_rejects_negative_page_num(tmp_path: Path) -> None:
    storage = ImageStorage(
        image_root=str(tmp_path / "images"),
        db_path=str(tmp_path / "db" / "image_index.db"),
    )

    with pytest.raises(ValueError, match="page_num must be a non-negative integer"):
        storage.save_image(
            image_id="img_neg",
            content=b"abc",
            collection="kb",
            page_num=-1,
        )


@pytest.mark.unit
def test_upsert_existing_image_id_removes_old_file_when_path_changes(tmp_path: Path) -> None:
    storage = ImageStorage(
        image_root=str(tmp_path / "images"),
        db_path=str(tmp_path / "db" / "image_index.db"),
    )
    first = storage.save_image(
        image_id="img_move",
        content=b"v1",
        collection="c1",
        suffix=".png",
    )
    second = storage.save_image(
        image_id="img_move",
        content=b"v2",
        collection="c2",
        suffix=".jpg",
    )

    assert first != second
    assert not Path(first).exists()
    assert Path(second).exists()
    assert storage.get_path("img_move") == second


@pytest.mark.unit
def test_save_image_rejects_bool_page_num(tmp_path: Path) -> None:
    storage = ImageStorage(
        image_root=str(tmp_path / "images"),
        db_path=str(tmp_path / "db" / "image_index.db"),
    )

    with pytest.raises(TypeError, match="page_num must be an integer when provided"):
        storage.save_image(
            image_id="img_bool",
            content=b"abc",
            collection="kb",
            page_num=True,  # type: ignore[arg-type]
        )


@pytest.mark.unit
def test_upsert_same_path_does_not_delete_current_file(tmp_path: Path) -> None:
    storage = ImageStorage(
        image_root=str(tmp_path / "images"),
        db_path=str(tmp_path / "db" / "image_index.db"),
    )
    first = storage.save_image(
        image_id="img_same",
        content=b"v1",
        collection="c1",
        suffix=".png",
    )
    second = storage.save_image(
        image_id="img_same",
        content=b"v2",
        collection="c1",
        suffix=".png",
    )

    assert first == second
    assert Path(second).exists()
    assert Path(second).read_bytes() == b"v2"
