from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import cast

from visionlabelops.types import AuditIssue, AuditResult, Dataset, Severity
from visionlabelops.utils.dataset_ops import class_instance_counts, image_annotation_counts, image_size_distribution
from visionlabelops.utils.image_ops import validate_image


def _issue(code: str, severity: Severity, message: str, location: str | Path) -> AuditIssue:
    return AuditIssue(code=code, severity=severity, message=message, location=str(location))


def run_audit(dataset: Dataset) -> AuditResult:
    issues: list[AuditIssue] = []
    metadata_issues = cast(list[dict[str, str]], dataset.metadata.get("read_issues", []))
    for item in metadata_issues:
        issues.append(
            _issue(
                code=item["code"],
                severity=Severity(item["severity"]),
                message=item["message"],
                location=item["location"],
            )
        )

    for location in cast(list[str], dataset.metadata.get("unmatched_images", [])):
        issues.append(
            _issue(
                "annotation-missing",
                Severity.WARNING,
                "Image file is missing an annotation file",
                location,
            )
        )

    for location in cast(list[str], dataset.metadata.get("unmatched_annotations", [])):
        issues.append(_issue("annotation-missing", Severity.WARNING, "Annotation file is missing for image", location))

    for name in cast(list[str], dataset.metadata.get("duplicate_file_names", [])):
        issues.append(_issue("duplicate-file-name", Severity.WARNING, "Duplicate file name detected", name))

    valid_category_ids = {category.index for category in dataset.categories}
    per_class = class_instance_counts(dataset)
    per_image_boxes = image_annotation_counts(dataset)
    image_sizes = image_size_distribution(dataset)

    for image in dataset.images:
        if image.path is None or not image.path.exists():
            issues.append(_issue("image-missing", Severity.ERROR, "Image file is missing", image.file_name))
            continue
        is_valid, error_message = validate_image(image.path)
        if not is_valid:
            issues.append(
                _issue(
                    "image-unreadable",
                    Severity.ERROR,
                    error_message or "Image cannot be read",
                    image.path,
                )
            )
            continue
        if not image.annotations:
            issues.append(_issue("empty-annotation", Severity.WARNING, "Image has no annotations", image.file_name))
        for annotation in image.annotations:
            if annotation.category_id not in valid_category_ids:
                issues.append(
                    _issue(
                        "invalid-category-id",
                        Severity.ERROR,
                        f"Category id {annotation.category_id} is outside declared categories",
                        image.file_name,
                    )
                )
            if not annotation.bbox.is_valid():
                issues.append(
                    _issue(
                        "bbox-invalid-size",
                        Severity.ERROR,
                        "Bounding box has non-positive size",
                        image.file_name,
                    )
                )
            if image.width and image.height and not annotation.bbox.is_within(image.width, image.height):
                issues.append(
                    _issue(
                        "bbox-out-of-bounds",
                        Severity.ERROR,
                        "Bounding box exceeds image boundaries",
                        image.file_name,
                    )
                )

    if len(dataset.categories) > 1 and per_class:
        total_instances = sum(per_class.values())
        dominant_count = max(per_class.values())
        if total_instances and dominant_count / total_instances >= 0.9:
            dominant_name = max(per_class, key=lambda category_name: per_class[category_name])
            issues.append(
                _issue(
                    "class-distribution-anomaly",
                    Severity.WARNING,
                    f"Class '{dominant_name}' dominates >= 90% of instances",
                    dataset.source_path,
                )
            )
        unused = [category.name for category in dataset.categories if per_class.get(category.name, 0) == 0]
        for category_name in unused:
            issues.append(
                _issue(
                    "class-unused",
                    Severity.WARNING,
                    f"Declared class '{category_name}' has no instances",
                    dataset.source_path,
                )
            )

    summary = {
        "image_count": dataset.image_count,
        "annotation_count": dataset.annotation_count,
        "category_count": len(dataset.categories),
        "issue_count": len(issues),
        "issues_by_severity": dict(Counter(issue.severity.value for issue in issues)),
        "per_class_instances": dict(per_class),
        "per_image_box_distribution": dict(per_image_boxes),
        "image_size_distribution": dict(image_sizes),
    }
    return AuditResult(summary=summary, issues=issues)
