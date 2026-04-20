from __future__ import annotations

import math
from collections.abc import Iterable
from pathlib import Path

from PIL import Image, ImageColor, ImageDraw, ImageFont

from visionlabelops.types import ImageRecord


def load_image_size(path: Path) -> tuple[int, int]:
    with Image.open(path) as image:
        return image.size


def validate_image(path: Path) -> tuple[bool, str | None]:
    try:
        with Image.open(path) as image:
            image.verify()
        return True, None
    except Exception as exc:  # pragma: no cover - library specific messages differ
        return False, str(exc)


def render_preview(image: ImageRecord, destination: Path) -> Path:
    if image.path is None:
        raise FileNotFoundError(f"Image path missing for {image.file_name}")
    with Image.open(image.path).convert("RGB") as scene:
        canvas = scene.copy()
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.load_default()
    palette = ["#ef4444", "#10b981", "#3b82f6", "#f59e0b", "#8b5cf6", "#ec4899"]
    for index, annotation in enumerate(image.annotations):
        color = ImageColor.getrgb(palette[index % len(palette)])
        bbox = annotation.bbox
        draw.rectangle([bbox.xmin, bbox.ymin, bbox.xmax, bbox.ymax], outline=color, width=2)
        if annotation.polygon is not None:
            draw.polygon(annotation.polygon.points, outline=color, width=2)
        draw.text((bbox.xmin + 2, max(bbox.ymin - 12, 0)), annotation.category_name, fill=color, font=font)
    destination.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(destination)
    return destination


def create_contact_sheet(image_paths: Iterable[Path], destination: Path, columns: int = 2) -> Path:
    images = [Image.open(path).convert("RGB") for path in image_paths]
    try:
        if not images:
            blank = Image.new("RGB", (320, 240), color=(255, 255, 255))
            blank.save(destination)
            return destination
        width = max(image.width for image in images)
        height = max(image.height for image in images)
        rows = math.ceil(len(images) / columns)
        sheet = Image.new("RGB", (width * columns, height * rows), color=(250, 250, 250))
        for index, image in enumerate(images):
            x = (index % columns) * width
            y = (index // columns) * height
            sheet.paste(image, (x, y))
        destination.parent.mkdir(parents=True, exist_ok=True)
        sheet.save(destination)
        return destination
    finally:
        for image in images:
            image.close()
