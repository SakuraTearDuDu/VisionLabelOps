from __future__ import annotations

from collections import Counter
from pathlib import Path

import yaml

from visionlabelops.constants import IMAGE_EXTENSIONS
from visionlabelops.io.common import copy_image
from visionlabelops.types import Annotation, BBox, Category, Dataset, DatasetFormat, ImageRecord
from visionlabelops.utils.image_ops import load_image_size
from visionlabelops.utils.pathing import find_image_by_stem


def _load_names(payload: dict) -> list[str]:
    names = payload.get("names", [])
    if isinstance(names, dict):
        return [names[key] for key in sorted(names, key=lambda item: int(item))]
    return list(names)


def read_yolo_dataset(path: Path) -> Dataset:
    path = path.resolve()
    data_yaml_path = path if path.is_file() else path / "data.yaml"
    payload = yaml.safe_load(data_yaml_path.read_text(encoding="utf-8"))
    root_dir = data_yaml_path.parent
    names = _load_names(payload)
    categories = [Category(index=index, name=name) for index, name in enumerate(names)]
    read_issues: list[dict[str, str]] = []
    unmatched_annotations: list[str] = []
    images: list[ImageRecord] = []
    seen_files: Counter[str] = Counter()

    for subset in ("train", "val", "test"):
        subset_path_value = payload.get(subset)
        if not subset_path_value:
            continue
        image_dir = (root_dir / subset_path_value).resolve()
        if not image_dir.exists():
            read_issues.append(
                {
                    "code": "image-dir-missing",
                    "severity": "error",
                    "message": f"Declared YOLO image directory does not exist for split '{subset}'",
                    "location": str(image_dir),
                }
            )
            continue
        labels_dir = image_dir.parent.parent / "labels" / image_dir.name
        image_files = [item for item in sorted(image_dir.iterdir()) if item.suffix.lower() in IMAGE_EXTENSIONS]
        for image_path in image_files:
            width, height = load_image_size(image_path)
            label_path = labels_dir / f"{image_path.stem}.txt"
            annotations: list[Annotation] = []
            if label_path.exists():
                lines = [line.strip() for line in label_path.read_text(encoding="utf-8").splitlines() if line.strip()]
                for line_number, line in enumerate(lines, start=1):
                    parts = line.split()
                    if len(parts) != 5:
                        read_issues.append(
                            {
                                "code": "invalid-yolo-line",
                                "severity": "error",
                                "message": f"Expected 5 fields, found {len(parts)}",
                                "location": f"{label_path}:{line_number}",
                            }
                        )
                        continue
                    try:
                        category_id = int(float(parts[0]))
                        x_center, y_center, box_width, box_height = [float(value) for value in parts[1:]]
                    except ValueError:
                        read_issues.append(
                            {
                                "code": "invalid-yolo-value",
                                "severity": "error",
                                "message": "YOLO line contains non-numeric values",
                                "location": f"{label_path}:{line_number}",
                            }
                        )
                        continue
                    if category_id < 0 or category_id >= len(categories):
                        read_issues.append(
                            {
                                "code": "invalid-category-id",
                                "severity": "error",
                                "message": f"Category id {category_id} is outside names range",
                                "location": f"{label_path}:{line_number}",
                            }
                        )
                        continue
                    xmin = (x_center - box_width / 2.0) * width
                    ymin = (y_center - box_height / 2.0) * height
                    xmax = (x_center + box_width / 2.0) * width
                    ymax = (y_center + box_height / 2.0) * height
                    annotations.append(
                        Annotation(
                            category_id=category_id,
                            category_name=categories[category_id].name,
                            bbox=BBox(xmin=xmin, ymin=ymin, xmax=xmax, ymax=ymax),
                        )
                    )
            else:
                unmatched_annotations.append(str(label_path))

            images.append(
                ImageRecord(
                    id=f"{subset}:{image_path.stem}",
                    file_name=image_path.name,
                    path=image_path,
                    width=width,
                    height=height,
                    annotations=annotations,
                    subset=subset,
                    annotation_path=label_path,
                )
            )
            seen_files[image_path.name] += 1

        if labels_dir.exists():
            for label_path in sorted(labels_dir.glob("*.txt")):
                image_path = find_image_by_stem(image_dir, label_path.stem)
                if image_path is None:
                    read_issues.append(
                        {
                            "code": "image-missing",
                            "severity": "error",
                            "message": "YOLO label file does not have a matching image",
                            "location": str(label_path),
                        }
                    )

    return Dataset(
        format=DatasetFormat.YOLO,
        root_dir=root_dir,
        images=images,
        categories=categories,
        source_path=path,
        metadata={
            "read_issues": read_issues,
            "unmatched_images": [],
            "unmatched_annotations": unmatched_annotations,
            "duplicate_file_names": [name for name, count in seen_files.items() if count > 1],
        },
    )


def write_yolo_dataset(dataset: Dataset, output_path: Path) -> None:
    for subset in sorted({image.subset for image in dataset.images}):
        (output_path / "images" / subset).mkdir(parents=True, exist_ok=True)
        (output_path / "labels" / subset).mkdir(parents=True, exist_ok=True)

    for image in dataset.images:
        subset = image.subset
        if image.path is not None and image.path.exists():
            copy_image(image.path, output_path / "images" / subset / image.file_name)
        label_path = output_path / "labels" / subset / f"{Path(image.file_name).stem}.txt"
        lines: list[str] = []
        if image.width and image.height:
            for annotation in image.annotations:
                x_center, y_center, box_width, box_height = annotation.bbox.to_yolo(image.width, image.height)
                lines.append(
                    f"{annotation.category_id} {x_center:.10f} {y_center:.10f} {box_width:.10f} {box_height:.10f}"
                )
        label_path.write_text("\n".join(lines), encoding="utf-8")

    names = {category.index: category.name for category in dataset.categories}
    subsets = sorted({image.subset for image in dataset.images})
    payload: dict[str, object] = {"path": ".", "names": names}
    for subset in subsets:
        payload[subset] = f"images/{subset}"
    (output_path / "data.yaml").write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")
