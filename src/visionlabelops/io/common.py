from __future__ import annotations

import json
import shutil
from pathlib import Path

from visionlabelops.types import Category, Dataset


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def copy_image(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def sorted_categories(dataset: Dataset) -> list[Category]:
    return sorted(dataset.categories, key=lambda category: category.index)
