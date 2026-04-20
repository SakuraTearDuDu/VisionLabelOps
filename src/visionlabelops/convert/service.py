from __future__ import annotations

from pathlib import Path
from typing import cast

from visionlabelops.errors import DatasetFormatError
from visionlabelops.io import write_coco_dataset, write_labelme_dataset, write_yolo_dataset
from visionlabelops.types import ConvertResult, Dataset, DatasetFormat


def _assert_convertible(dataset: Dataset) -> None:
    if dataset.format is not DatasetFormat.LABELME:
        return
    read_issues = cast(list[dict[str, str]], dataset.metadata.get("read_issues", []))
    unsupported = [item for item in read_issues if isinstance(item, dict) and item.get("code") == "unsupported-shape"]
    if unsupported:
        raise DatasetFormatError(
            "Cannot convert Labelme datasets with unsupported shape types. "
            "Supported shape types are: rectangle, polygon."
        )


def convert_dataset_to_format(
    dataset: Dataset,
    output_format: DatasetFormat,
    output_path: Path,
    dry_run: bool = False,
) -> ConvertResult:
    output_path = output_path.resolve()
    _assert_convertible(dataset)
    if not dry_run:
        if output_format is DatasetFormat.YOLO:
            write_yolo_dataset(dataset, output_path)
        elif output_format is DatasetFormat.COCO:
            write_coco_dataset(dataset, output_path)
        elif output_format is DatasetFormat.LABELME:
            write_labelme_dataset(dataset, output_path)

    return ConvertResult(
        input_format=dataset.format,
        output_format=output_format,
        output_path=output_path,
        image_count=dataset.image_count,
        annotation_count=dataset.annotation_count,
        categories=[category.name for category in dataset.categories],
        dry_run=dry_run,
    )
