from __future__ import annotations

from pathlib import Path

from jinja2 import Template

from visionlabelops.audit.service import run_audit
from visionlabelops.constants import DEFAULT_HTML_TEMPLATE, PROJECT_NAME, resource_path
from visionlabelops.stats.service import compute_dataset_stats
from visionlabelops.types import AuditResult, Dataset, ReportResult, SplitResult
from visionlabelops.utils.serialization import to_jsonable


def _load_template() -> Template:
    template_path = resource_path(DEFAULT_HTML_TEMPLATE)
    return Template(template_path.read_text(encoding="utf-8"))


def render_report(
    dataset: Dataset,
    output_path: Path,
    audit_result: AuditResult | None = None,
    split_result: SplitResult | None = None,
    convert_summary: dict[str, object] | None = None,
) -> ReportResult:
    audit_result = audit_result or run_audit(dataset)
    stats_result = compute_dataset_stats(dataset)
    summary = {
        "project": PROJECT_NAME,
        "dataset_format": dataset.format.value,
        "dataset_root": str(dataset.root_dir),
        "image_count": dataset.image_count,
        "annotation_count": dataset.annotation_count,
        "category_count": len(dataset.categories),
        "stats": to_jsonable(stats_result),
        "audit": to_jsonable(audit_result),
        "split": to_jsonable(split_result) if split_result else None,
        "convert": convert_summary,
    }

    markdown_lines = [
        f"# {PROJECT_NAME} Report",
        "",
        "## Dataset Overview",
        f"- Format: `{dataset.format.value}`",
        f"- Images: {dataset.image_count}",
        f"- Annotations: {dataset.annotation_count}",
        f"- Categories: {len(dataset.categories)}",
        "",
        "## Audit Summary",
        f"- Issues: {audit_result.summary['issue_count']}",
        f"- Severity counts: {audit_result.summary['issues_by_severity']}",
        "",
        "## Class Statistics",
    ]
    for name, count in stats_result.per_class_instances.items():
        markdown_lines.append(f"- {name}: {count}")
    markdown_lines.extend(["", "## Risk Items"])
    for issue in audit_result.issues[:20]:
        markdown_lines.append(f"- [{issue.severity.value}] {issue.code}: {issue.message} ({issue.location})")
    if split_result is not None:
        markdown_lines.extend(["", "## Split Summary"])
        for split, count in split_result.counts.items():
            markdown_lines.append(f"- {split}: {count}")
    if convert_summary is not None:
        markdown_lines.extend(["", "## Conversion Summary", f"- Output: {convert_summary.get('output_path')}"])

    output_path.mkdir(parents=True, exist_ok=True)
    markdown_path = output_path / "report.md"
    html_path = output_path / "report.html"
    markdown_path.write_text("\n".join(markdown_lines), encoding="utf-8")
    html_path.write_text(_load_template().render(summary=summary), encoding="utf-8")
    return ReportResult(output_path=output_path.resolve(), markdown_path=markdown_path, html_path=html_path)
