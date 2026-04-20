from __future__ import annotations

from collections import Counter
from pathlib import Path

from PIL import Image

from visionlabelops.constants import DEFAULT_SUBSET, IMAGE_EXTENSIONS
from visionlabelops.io.common import copy_image, load_json, write_json
from visionlabelops.types import Annotation, BBox, Category, Dataset, DatasetFormat, ImageRecord, Polygon


def _resolve_labelme_image(json_path: Path, payload: dict) -> tuple[Path | None, int | None, int | None]:
    image_path_value = payload.get("imagePath")
    candidate = json_path.parent / image_path_value if image_path_value else None
    if candidate and candidate.exists():
        try:
            with Image.open(candidate) as image:
                width, height = image.size
            return candidate, width, height
        except Exception:
            return candidate, payload.get("imageWidth"), payload.get("imageHeight")

    return candidate, payload.get("imageWidth"), payload.get("imageHeight")


def read_labelme_dataset(path: Path) -> Dataset:
    path = path.resolve()
    json_files = [path] if path.is_file() else sorted(path.glob("*.json"))
    images: list[ImageRecord] = []
    category_names: set[str] = set()
    read_issues: list[dict[str, str]] = []
    image_to_json: dict[str, str] = {}

    for json_path in json_files:
        payload = load_json(json_path)
        image_path, width, height = _resolve_labelme_image(json_path, payload)
        image_name = payload.get("imagePath") or f"{json_path.stem}.jpg"
        annotations: list[Annotation] = []
        for shape in payload.get("shapes", []):
            label = shape["label"]
            category_names.add(label)
            shape_type = shape.get("shape_type", "polygon")
            points = [tuple(point) for point in shape.get("points", [])]
            if shape_type == "rectangle" and len(points) == 2:
                (x1, y1), (x2, y2) = points
                bbox = BBox(min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2))
                polygon = None
            elif shape_type == "polygon" and len(points) >= 3:
                polygon = Polygon(tuple(points))
                bbox = polygon.bbox
            else:
                read_issues.append(
                    {
                        "code": "unsupported-shape",
                        "severity": "warning",
                        "message": f"Unsupported Labelme shape_type '{shape_type}'",
                        "location": str(json_path),
                    }
                )
                continue
            annotations.append(
                Annotation(
                    category_id=-1,
                    category_name=label,
                    bbox=bbox,
                    polygon=polygon,
                    source_id=shape.get("group_id"),
                )
            )

        image_to_json[image_name] = str(json_path)
        images.append(
            ImageRecord(
                id=json_path.stem,
                file_name=image_name,
                path=image_path,
                width=width,
                height=height,
                annotations=annotations,
                subset=DEFAULT_SUBSET,
                annotation_path=json_path,
            )
        )

    categories = [Category(index=index, name=name) for index, name in enumerate(sorted(category_names))]
    name_to_id = {category.name: category.index for category in categories}
    for image in images:
        for annotation in image.annotations:
            annotation.category_id = name_to_id[annotation.category_name]

    root_dir = path.parent if path.is_file() else path
    image_files = [item for item in root_dir.iterdir() if item.is_file() and item.suffix.lower() in IMAGE_EXTENSIONS]
    unmatched_images = [str(item) for item in image_files if item.name not in image_to_json]
    duplicate_names = [name for name, count in Counter(image.file_name for image in images).items() if count > 1]

    return Dataset(
        format=DatasetFormat.LABELME,
        root_dir=root_dir,
        images=images,
        categories=categories,
        source_path=path,
        metadata={
            "read_issues": read_issues,
            "unmatched_images": unmatched_images,
            "unmatched_annotations": [],
            "duplicate_file_names": duplicate_names,
        },
    )


def write_labelme_dataset(dataset: Dataset, output_path: Path) -> None:
    for image in dataset.images:
        subset_dir = output_path / image.subset
        if image.path is not None and image.path.exists():
            copy_image(image.path, subset_dir / image.file_name)
        payload: dict[str, object] = {
            "version": "5.0.0",
            "flags": {},
            "shapes": [],
            "imagePath": image.file_name,
            "imageData": None,
            "imageHeight": image.height,
            "imageWidth": image.width,
        }
        for annotation in image.annotations:
            if annotation.polygon is not None:
                points = [list(point) for point in annotation.polygon.points]
                shape_type = "polygon"
            else:
                points = [
                    [annotation.bbox.xmin, annotation.bbox.ymin],
                    [annotation.bbox.xmax, annotation.bbox.ymax],
                ]
                shape_type = "rectangle"
            shapes = payload["shapes"]
            assert isinstance(shapes, list)
            shapes.append(
                {
                    "label": annotation.category_name,
                    "points": points,
                    "group_id": annotation.source_id,
                    "shape_type": shape_type,
                    "flags": {},
                }
            )
        write_json(subset_dir / f"{Path(image.file_name).stem}.json", payload)
