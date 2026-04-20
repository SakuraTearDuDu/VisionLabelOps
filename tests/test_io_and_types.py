from __future__ import annotations

from pathlib import Path

from visionlabelops.api import convert_dataset, read_dataset
from visionlabelops.errors import DatasetFormatError
from visionlabelops.types import DatasetFormat


def test_read_labelme_dataset_derives_bbox_and_polygon(labelme_dataset_dir: Path) -> None:
    dataset = read_dataset(labelme_dataset_dir, DatasetFormat.LABELME)

    assert dataset.format is DatasetFormat.LABELME
    assert len(dataset.images) == 3
    assert [category.name for category in dataset.categories] == ["bird", "cat", "dog"]

    sample1 = next(image for image in dataset.images if image.file_name == "sample1.jpg")
    assert sample1.width == 32
    assert sample1.height == 24
    assert sample1.annotations[0].bbox.xmin == 4.0
    assert sample1.annotations[0].bbox.xmax == 20.0

    sample2 = next(image for image in dataset.images if image.file_name == "sample2.jpg")
    assert sample2.annotations[0].polygon is not None
    assert len(sample2.annotations[0].polygon.points) == 4


def test_read_yolo_dataset_parses_normalized_boxes(yolo_dataset_dir: Path) -> None:
    dataset = read_dataset(yolo_dataset_dir, DatasetFormat.YOLO)

    assert dataset.format is DatasetFormat.YOLO
    assert [category.name for category in dataset.categories] == ["cat", "dog"]
    assert {image.subset for image in dataset.images} == {"train", "val"}

    train_image = next(image for image in dataset.images if image.subset == "train")
    assert train_image.annotations[0].bbox.width == 16.0
    assert round(train_image.annotations[0].bbox.height, 4) == 13.0


def test_read_coco_dataset_preserves_polygon_when_available(coco_dataset_dir: Path) -> None:
    dataset = read_dataset(coco_dataset_dir / "annotations.json", DatasetFormat.COCO)

    assert dataset.format is DatasetFormat.COCO
    assert len(dataset.images) == 2
    polygon_image = next(image for image in dataset.images if image.file_name.endswith("sample2.jpg"))
    assert polygon_image.annotations[0].polygon is not None
    assert polygon_image.annotations[0].bbox.width == 16.0


def test_convert_labelme_to_yolo_and_coco(supported_labelme_dataset_dir: Path, tmp_path: Path) -> None:
    yolo_out = tmp_path / "converted-yolo"
    coco_out = tmp_path / "converted-coco"

    yolo_result = convert_dataset(
        input_path=supported_labelme_dataset_dir,
        input_format=DatasetFormat.LABELME,
        output_path=yolo_out,
        output_format=DatasetFormat.YOLO,
    )
    coco_result = convert_dataset(
        input_path=supported_labelme_dataset_dir,
        input_format=DatasetFormat.LABELME,
        output_path=coco_out,
        output_format=DatasetFormat.COCO,
    )

    assert yolo_result.image_count == 2
    assert (yolo_out / "data.yaml").exists()
    assert (yolo_out / "labels" / "default" / "sample1.txt").exists()

    assert coco_result.annotation_count >= 2
    assert (coco_out / "annotations.json").exists()


def test_convert_rejects_unsupported_labelme_shapes(labelme_dataset_dir: Path, tmp_path: Path) -> None:
    try:
        convert_dataset(
            input_path=labelme_dataset_dir,
            input_format=DatasetFormat.LABELME,
            output_path=tmp_path / "converted-yolo",
            output_format=DatasetFormat.YOLO,
        )
    except DatasetFormatError as exc:
        assert "unsupported shape types" in str(exc)
    else:  # pragma: no cover - defensive guard
        raise AssertionError("Expected conversion to reject unsupported Labelme shapes")


def test_read_yolo_dataset_tolerates_non_numeric_values(yolo_dataset_dir: Path) -> None:
    (yolo_dataset_dir / "labels" / "train" / "sample1.txt").write_text("cat nope 0.5 0.5 0.5", encoding="utf-8")

    dataset = read_dataset(yolo_dataset_dir, DatasetFormat.YOLO)

    read_issues = dataset.metadata["read_issues"]
    assert any(item["code"] == "invalid-yolo-value" for item in read_issues)
    train_image = next(image for image in dataset.images if image.subset == "train")
    assert train_image.annotations == []
