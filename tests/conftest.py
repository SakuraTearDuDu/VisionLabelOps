from __future__ import annotations

import shutil
from pathlib import Path

import pytest
from PIL import Image

FIXTURES_DIR = Path(__file__).parent / "fixtures"


def _write_image(path: Path, color: tuple[int, int, int]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    Image.new("RGB", (32, 24), color=color).save(path)


@pytest.fixture()
def labelme_dataset_dir(tmp_path: Path) -> Path:
    target = tmp_path / "labelme"
    shutil.copytree(FIXTURES_DIR / "labelme", target)
    _write_image(target / "sample1.jpg", (200, 20, 20))
    _write_image(target / "sample2.jpg", (20, 200, 20))
    _write_image(target / "unsupported.jpg", (20, 20, 200))
    return target


@pytest.fixture()
def supported_labelme_dataset_dir(tmp_path: Path) -> Path:
    target = tmp_path / "labelme-supported"
    target.mkdir()
    shutil.copy2(FIXTURES_DIR / "labelme" / "sample1.json", target / "sample1.json")
    shutil.copy2(FIXTURES_DIR / "labelme" / "sample2.json", target / "sample2.json")
    _write_image(target / "sample1.jpg", (200, 20, 20))
    _write_image(target / "sample2.jpg", (20, 200, 20))
    return target


@pytest.fixture()
def yolo_dataset_dir(tmp_path: Path) -> Path:
    target = tmp_path / "yolo"
    shutil.copytree(FIXTURES_DIR / "yolo", target)
    _write_image(target / "images" / "train" / "sample1.jpg", (200, 20, 20))
    _write_image(target / "images" / "val" / "sample2.jpg", (20, 200, 20))
    return target


@pytest.fixture()
def coco_dataset_dir(tmp_path: Path) -> Path:
    target = tmp_path / "coco"
    target.mkdir()
    shutil.copy2(FIXTURES_DIR / "coco" / "annotations.json", target / "annotations.json")
    _write_image(target / "images" / "train" / "sample1.jpg", (200, 20, 20))
    _write_image(target / "images" / "val" / "sample2.jpg", (20, 200, 20))
    return target


@pytest.fixture()
def audit_problem_dir(tmp_path: Path) -> Path:
    target = tmp_path / "audit-problem"
    shutil.copytree(FIXTURES_DIR / "labelme", target)
    _write_image(target / "sample1.jpg", (200, 20, 20))
    shutil.copy2(FIXTURES_DIR / "corrupt_image.jpg", target / "sample2.jpg")
    return target
