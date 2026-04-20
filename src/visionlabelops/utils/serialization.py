from __future__ import annotations

import json
from dataclasses import asdict, is_dataclass
from enum import Enum
from pathlib import Path
from typing import Any

from visionlabelops.constants import RESULT_FILE_NAME, RESULT_SCHEMA_VERSION
from visionlabelops.errors import ValidationError
from visionlabelops.types import (
    AuditIssue,
    AuditResult,
    ConvertResult,
    DatasetFormat,
    PreviewResult,
    ReportResult,
    Severity,
    SplitResult,
    StatsResult,
)

ResultObject = AuditResult | StatsResult | ConvertResult | SplitResult | PreviewResult | ReportResult
ResultType = (
    type[AuditResult]
    | type[StatsResult]
    | type[ConvertResult]
    | type[SplitResult]
    | type[PreviewResult]
    | type[ReportResult]
)

_RESULT_TYPE_NAMES: dict[type[Any], str] = {
    AuditResult: "audit",
    StatsResult: "stats",
    ConvertResult: "convert",
    SplitResult: "split",
    PreviewResult: "preview",
    ReportResult: "report",
}
_RESULT_TYPES: dict[str, ResultType] = {name: result_type for result_type, name in _RESULT_TYPE_NAMES.items()}


def to_jsonable(value: Any) -> Any:
    if is_dataclass(value) and not isinstance(value, type):
        return to_jsonable(asdict(value))
    if isinstance(value, dict):
        return {str(key): to_jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [to_jsonable(item) for item in value]
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, Enum):
        return value.value
    return value


def _coerce_path(value: str | Path) -> Path:
    return Path(value)


def _deserialize_audit_result(payload: dict[str, Any]) -> AuditResult:
    return AuditResult(
        summary=payload["summary"],
        issues=[
            AuditIssue(
                code=item["code"],
                severity=Severity(item["severity"]),
                message=item["message"],
                location=item["location"],
            )
            for item in payload["issues"]
        ],
    )


def _deserialize_stats_result(payload: dict[str, Any]) -> StatsResult:
    return StatsResult(
        image_count=payload["image_count"],
        annotation_count=payload["annotation_count"],
        category_count=payload["category_count"],
        per_class_instances=payload["per_class_instances"],
        per_image_box_distribution=payload["per_image_box_distribution"],
        image_size_distribution=payload["image_size_distribution"],
        bbox_area_distribution=payload["bbox_area_distribution"],
    )


def _deserialize_convert_result(payload: dict[str, Any]) -> ConvertResult:
    return ConvertResult(
        input_format=DatasetFormat.from_value(payload["input_format"]),
        output_format=DatasetFormat.from_value(payload["output_format"]),
        output_path=_coerce_path(payload["output_path"]),
        image_count=payload["image_count"],
        annotation_count=payload["annotation_count"],
        categories=payload["categories"],
        dry_run=payload.get("dry_run", False),
    )


def _deserialize_split_result(payload: dict[str, Any]) -> SplitResult:
    return SplitResult(
        output_path=_coerce_path(payload["output_path"]),
        counts=payload["counts"],
        assignments=payload["assignments"],
        summary=payload["summary"],
        dry_run=payload.get("dry_run", False),
    )


def _deserialize_preview_result(payload: dict[str, Any]) -> PreviewResult:
    return PreviewResult(
        output_path=_coerce_path(payload["output_path"]),
        exported_files=[_coerce_path(path) for path in payload["exported_files"]],
        contact_sheet_path=_coerce_path(payload["contact_sheet_path"]),
    )


def _deserialize_report_result(payload: dict[str, Any]) -> ReportResult:
    return ReportResult(
        output_path=_coerce_path(payload["output_path"]),
        markdown_path=_coerce_path(payload["markdown_path"]),
        html_path=_coerce_path(payload["html_path"]),
    )


_DESERIALIZERS: dict[ResultType, Any] = {
    AuditResult: _deserialize_audit_result,
    StatsResult: _deserialize_stats_result,
    ConvertResult: _deserialize_convert_result,
    SplitResult: _deserialize_split_result,
    PreviewResult: _deserialize_preview_result,
    ReportResult: _deserialize_report_result,
}


def serialize_result(result: ResultObject) -> dict[str, Any]:
    result_type = type(result)
    if result_type not in _RESULT_TYPE_NAMES:
        raise ValidationError(f"Unsupported result object: {result_type!r}")
    payload = to_jsonable(result)
    payload["schema_version"] = RESULT_SCHEMA_VERSION
    payload["result_type"] = _RESULT_TYPE_NAMES[result_type]
    return payload


def deserialize_result(payload: dict[str, Any], expected_type: ResultType | None = None) -> ResultObject:
    raw_payload = dict(payload)
    schema_version = raw_payload.pop("schema_version", None)
    if schema_version is None:
        if expected_type is None:
            raise ValidationError("Legacy result payloads require an expected result type.")
        return _DESERIALIZERS[expected_type](raw_payload)
    if schema_version != RESULT_SCHEMA_VERSION:
        raise ValidationError(f"Unsupported result schema version: {schema_version}")

    result_type_name = raw_payload.pop("result_type", None)
    if not isinstance(result_type_name, str):
        raise ValidationError("Result payload is missing a valid result_type.")

    resolved_type = _RESULT_TYPES.get(result_type_name)
    if resolved_type is None:
        raise ValidationError(f"Unsupported result type: {result_type_name}")
    if expected_type is not None and resolved_type is not expected_type:
        raise ValidationError(
            f"Expected result type '{_RESULT_TYPE_NAMES[expected_type]}', got '{result_type_name}'."
        )
    return _DESERIALIZERS[resolved_type](raw_payload)


def load_result_file(path: Path | str, expected_type: ResultType | None = None) -> ResultObject:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValidationError("Result file must contain a JSON object.")
    return deserialize_result(payload, expected_type=expected_type)


def dump_result_file(output_dir: Path | str, result: ResultObject) -> Path:
    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)
    result_path = destination / RESULT_FILE_NAME
    result_path.write_text(json.dumps(serialize_result(result), indent=2), encoding="utf-8")
    return result_path
