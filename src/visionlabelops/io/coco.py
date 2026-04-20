from __future__ import annotations

from collections import Counter, defaultdict
from pathlib import Path

from visionlabelops.io.common import copy_image, load_json, write_json
from visionlabelops.types import Annotation, BBox, Category, Dataset, DatasetFormat, ImageRecord, Polygon
from visionlabelops.utils.image_ops import load_image_size


def read_coco_dataset(path: Path) -> Dataset:
    path = path.resolve()
    annotations_path = path if path.is_file() else path / "annotations.json"
    root_dir = annotations_path.parent
    payload = load_json(annotations_path)
    categories = [
        Category(index=index, name=category["name"], original_id=category["id"])
        for index, category in enumerate(sorted(payload.get("categories", []), key=lambda item: item["id"]))
    ]
    category_id_map = {category.original_id: category for category in categories}
    annotations_by_image: dict[int, list[Annotation]] = defaultdict(list)
    read_issues: list[dict[str, str]] = []

    for annotation_payload in payload.get("annotations", []):
        if annotation_payload.get("iscrowd", 0):
            continue
        original_category_id = annotation_payload["category_id"]
        if original_category_id not in category_id_map:
            read_issues.append(
                {
                    "code": "invalid-category-id",
                    "severity": "error",
                    "message": f"Unknown category id {original_category_id}",
                    "location": str(annotations_path),
                }
            )
            continue
        category = category_id_map[original_category_id]
        bbox = BBox.from_xywh(*[float(value) for value in annotation_payload["bbox"]])
        segmentation = annotation_payload.get("segmentation")
        polygon = None
        if isinstance(segmentation, list) and segmentation and isinstance(segmentation[0], list):
            points = segmentation[0]
            if len(points) >= 6 and len(points) % 2 == 0:
                polygon = Polygon(tuple((points[index], points[index + 1]) for index in range(0, len(points), 2)))
        annotations_by_image[annotation_payload["image_id"]].append(
            Annotation(
                category_id=category.index,
                category_name=category.name,
                bbox=bbox,
                polygon=polygon,
                source_id=annotation_payload.get("id"),
            )
        )

    images: list[ImageRecord] = []
    seen_files: Counter[str] = Counter()
    for image_payload in payload.get("images", []):
        file_name = image_payload["file_name"]
        image_path = root_dir / "images" / file_name
        width = image_payload.get("width")
        height = image_payload.get("height")
        if image_path.exists() and (width is None or height is None):
            width, height = load_image_size(image_path)
        subset = Path(file_name).parts[0] if len(Path(file_name).parts) > 1 else "default"
        images.append(
            ImageRecord(
                id=str(image_payload["id"]),
                file_name=Path(file_name).name,
                path=image_path,
                width=width,
                height=height,
                annotations=annotations_by_image.get(image_payload["id"], []),
                subset=subset,
                annotation_path=annotations_path,
            )
        )
        seen_files[Path(file_name).name] += 1

    return Dataset(
        format=DatasetFormat.COCO,
        root_dir=root_dir,
        images=images,
        categories=categories,
        source_path=path,
        metadata={
            "read_issues": read_issues,
            "unmatched_images": [],
            "unmatched_annotations": [],
            "duplicate_file_names": [name for name, count in seen_files.items() if count > 1],
        },
    )


def write_coco_dataset(dataset: Dataset, output_path: Path) -> None:
    categories = [{"id": category.index + 1, "name": category.name} for category in dataset.categories]
    images_payload: list[dict[str, object]] = []
    annotations_payload: list[dict[str, object]] = []
    annotation_id = 1
    for image_id, image in enumerate(dataset.images, start=1):
        relative_file_name = f"{image.subset}/{image.file_name}" if image.subset else image.file_name
        if image.path is not None and image.path.exists():
            copy_image(image.path, output_path / "images" / relative_file_name)
        images_payload.append(
            {
                "id": image_id,
                "file_name": relative_file_name,
                "width": image.width,
                "height": image.height,
            }
        )
        for annotation in image.annotations:
            x, y, width, height = annotation.bbox.to_xywh()
            payload = {
                "id": annotation_id,
                "image_id": image_id,
                "category_id": annotation.category_id + 1,
                "bbox": [x, y, width, height],
                "area": annotation.bbox.area,
                "iscrowd": 0,
            }
            if annotation.polygon is not None:
                payload["segmentation"] = [[value for point in annotation.polygon.points for value in point]]
            annotations_payload.append(payload)
            annotation_id += 1

    write_json(
        output_path / "annotations.json",
        {"images": images_payload, "annotations": annotations_payload, "categories": categories},
    )
