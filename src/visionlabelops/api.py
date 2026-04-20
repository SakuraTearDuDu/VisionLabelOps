from __future__ import annotations

from pathlib import Path
from typing import Any

from visionlabelops.audit.service import run_audit
from visionlabelops.convert.service import convert_dataset_to_format
from visionlabelops.errors import DatasetFormatError
from visionlabelops.io import read_coco_dataset, read_labelme_dataset, read_yolo_dataset
from visionlabelops.preview.service import generate_preview
from visionlabelops.report.service import render_report
from visionlabelops.split.service import split_dataset_materialized
from visionlabelops.stats.service import compute_dataset_stats
from visionlabelops.types import (
    AuditResult,
    ConvertResult,
    Dataset,
    DatasetFormat,
    PreviewResult,
    ReportResult,
    SplitResult,
    StatsResult,
)
from visionlabelops.utils.pathing import ensure_output_path


def _resolve_format(dataset_format: DatasetFormat | str) -> DatasetFormat:
    try:
        return DatasetFormat.from_value(dataset_format)
    except ValueError as exc:
        raise DatasetFormatError(f"Unsupported dataset format: {dataset_format}") from exc


def _require_format(dataset_format: DatasetFormat | str | None, argument_name: str) -> DatasetFormat | str:
    if dataset_format is None:
        raise DatasetFormatError(f"{argument_name} is required when reading a dataset from path.")
    return dataset_format


def read_dataset(input_path: Path | str, dataset_format: DatasetFormat | str) -> Dataset:
    input_path = Path(input_path).resolve()
    format_enum = _resolve_format(dataset_format)
    if format_enum is DatasetFormat.LABELME:
        return read_labelme_dataset(input_path)
    if format_enum is DatasetFormat.YOLO:
        return read_yolo_dataset(input_path)
    if format_enum is DatasetFormat.COCO:
        return read_coco_dataset(input_path)
    raise DatasetFormatError(f"Unsupported dataset format: {format_enum}")


def audit_dataset(input_path: Path | str, input_format: DatasetFormat | str) -> AuditResult:
    return run_audit(read_dataset(input_path, _require_format(input_format, "input_format")))


def compute_stats(input_path: Path | str, input_format: DatasetFormat | str) -> StatsResult:
    return compute_dataset_stats(read_dataset(input_path, _require_format(input_format, "input_format")))


def convert_dataset(
    input_path: Path | str,
    input_format: DatasetFormat | str,
    output_path: Path | str,
    output_format: DatasetFormat | str,
    overwrite: bool = False,
    dry_run: bool = False,
) -> ConvertResult:
    dataset = read_dataset(input_path, input_format)
    output_dir = Path(output_path)
    if not dry_run:
        ensure_output_path(output_dir, overwrite=overwrite)
    return convert_dataset_to_format(dataset, _resolve_format(output_format), output_dir, dry_run=dry_run)


def split_dataset(
    input_path: Path | str,
    input_format: DatasetFormat | str,
    output_path: Path | str,
    train_ratio: float,
    val_ratio: float,
    test_ratio: float,
    seed: int,
    overwrite: bool = False,
    dry_run: bool = False,
) -> SplitResult:
    dataset = read_dataset(input_path, input_format)
    output_dir = Path(output_path)
    if not dry_run:
        ensure_output_path(output_dir, overwrite=overwrite)
    return split_dataset_materialized(
        dataset=dataset,
        output_path=output_dir,
        train_ratio=train_ratio,
        val_ratio=val_ratio,
        test_ratio=test_ratio,
        seed=seed,
        dry_run=dry_run,
    )


def preview_samples(
    input_path: Path | str,
    input_format: DatasetFormat | str,
    output_path: Path | str,
    samples: int,
    seed: int,
    overwrite: bool = False,
) -> PreviewResult:
    dataset = read_dataset(input_path, input_format)
    output_dir = ensure_output_path(Path(output_path), overwrite=overwrite)
    return generate_preview(dataset, output_dir, samples=samples, seed=seed)


def generate_report(
    input_path: Path | str,
    input_format: DatasetFormat | str,
    output_path: Path | str,
    audit_result: AuditResult | None = None,
    split_result: SplitResult | None = None,
    convert_result: ConvertResult | None = None,
    overwrite: bool = False,
) -> ReportResult:
    dataset = read_dataset(input_path, input_format)
    output_dir = ensure_output_path(Path(output_path), overwrite=overwrite)
    convert_summary: dict[str, Any] | None = None
    if convert_result is not None:
        convert_summary = {
            "input_format": convert_result.input_format.value,
            "output_format": convert_result.output_format.value,
            "output_path": str(convert_result.output_path),
            "image_count": convert_result.image_count,
            "annotation_count": convert_result.annotation_count,
        }
    return render_report(
        dataset,
        output_dir,
        audit_result=audit_result,
        split_result=split_result,
        convert_summary=convert_summary,
    )
