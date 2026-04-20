from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from visionlabelops import __version__
from visionlabelops.api import (
    audit_dataset,
    compute_stats,
    convert_dataset,
    generate_report,
    preview_samples,
    split_dataset,
)
from visionlabelops.errors import VisionLabelOpsError
from visionlabelops.types import AuditResult, ConvertResult, DatasetFormat, SplitResult
from visionlabelops.utils.pathing import ensure_output_path, write_result_file


def _format_arg(value: str) -> DatasetFormat:
    return DatasetFormat.from_value(value)


def _load_result(path: str | None, result_type: type[AuditResult] | type[ConvertResult] | type[SplitResult]):
    if not path:
        return None
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if result_type is AuditResult:
        from visionlabelops.types import AuditIssue, Severity

        issues = [
            AuditIssue(
                code=item["code"],
                severity=Severity(item["severity"]),
                message=item["message"],
                location=item["location"],
            )
            for item in payload["issues"]
        ]
        return AuditResult(summary=payload["summary"], issues=issues)
    if result_type is SplitResult:
        return SplitResult(
            output_path=Path(payload["output_path"]),
            counts=payload["counts"],
            assignments=payload["assignments"],
            summary=payload["summary"],
            dry_run=payload.get("dry_run", False),
        )
    if result_type is ConvertResult:
        return ConvertResult(
            input_format=DatasetFormat.from_value(payload["input_format"]),
            output_format=DatasetFormat.from_value(payload["output_format"]),
            output_path=Path(payload["output_path"]),
            image_count=payload["image_count"],
            annotation_count=payload["annotation_count"],
            categories=payload["categories"],
            dry_run=payload.get("dry_run", False),
        )
    return None


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="vlo", description="VisionLabelOps CLI")
    parser.add_argument("--version", action="version", version=__version__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    audit = subparsers.add_parser("audit", help="Audit a dataset")
    audit.add_argument("--input", required=True)
    audit.add_argument("--format", required=True, type=_format_arg)
    audit.add_argument("--output", required=True)
    audit.add_argument("--overwrite", action="store_true")

    convert = subparsers.add_parser("convert", help="Convert a dataset")
    convert.add_argument("--input", required=True)
    convert.add_argument("--input-format", required=True, type=_format_arg)
    convert.add_argument("--output", required=True)
    convert.add_argument("--output-format", required=True, type=_format_arg)
    convert.add_argument("--overwrite", action="store_true")
    convert.add_argument("--dry-run", action="store_true")

    stats = subparsers.add_parser("stats", help="Compute dataset statistics")
    stats.add_argument("--input", required=True)
    stats.add_argument("--format", required=True, type=_format_arg)
    stats.add_argument("--output", required=True)
    stats.add_argument("--overwrite", action="store_true")

    split = subparsers.add_parser("split", help="Split a dataset")
    split.add_argument("--input", required=True)
    split.add_argument("--format", required=True, type=_format_arg)
    split.add_argument("--output", required=True)
    split.add_argument("--train", required=True, type=float)
    split.add_argument("--val", required=True, type=float)
    split.add_argument("--test", required=True, type=float)
    split.add_argument("--seed", required=True, type=int)
    split.add_argument("--overwrite", action="store_true")
    split.add_argument("--dry-run", action="store_true")

    report = subparsers.add_parser("report", help="Generate a dataset report")
    report.add_argument("--input", required=True)
    report.add_argument("--format", required=True, type=_format_arg)
    report.add_argument("--output", required=True)
    report.add_argument("--audit-result")
    report.add_argument("--split-result")
    report.add_argument("--convert-result")
    report.add_argument("--overwrite", action="store_true")

    preview = subparsers.add_parser("preview", help="Render preview samples")
    preview.add_argument("--input", required=True)
    preview.add_argument("--format", required=True, type=_format_arg)
    preview.add_argument("--output", required=True)
    preview.add_argument("--samples", required=True, type=int)
    preview.add_argument("--seed", required=True, type=int)
    preview.add_argument("--overwrite", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    try:
        args = build_parser().parse_args(argv)
        if args.command == "audit":
            audit_result = audit_dataset(args.input, args.format)
            output_dir = ensure_output_path(Path(args.output), overwrite=args.overwrite)
            write_result_file(output_dir, audit_result)
            print(
                f"images={audit_result.summary['image_count']} "
                f"annotations={audit_result.summary['annotation_count']} "
                f"issues={audit_result.summary['issue_count']}"
            )
            return 0
        if args.command == "convert":
            convert_result = convert_dataset(
                input_path=args.input,
                input_format=args.input_format,
                output_path=args.output,
                output_format=args.output_format,
                overwrite=args.overwrite,
                dry_run=args.dry_run,
            )
            if not args.dry_run:
                write_result_file(Path(args.output), convert_result)
            prefix = "dry-run " if args.dry_run else ""
            print(
                f"{prefix}images={convert_result.image_count} annotations={convert_result.annotation_count} "
                f"{convert_result.input_format.value}->{convert_result.output_format.value}"
            )
            return 0
        if args.command == "stats":
            stats_result = compute_stats(args.input, args.format)
            output_dir = ensure_output_path(Path(args.output), overwrite=args.overwrite)
            write_result_file(output_dir, stats_result)
            print(
                f"images={stats_result.image_count} "
                f"annotations={stats_result.annotation_count} "
                f"categories={stats_result.category_count}"
            )
            return 0
        if args.command == "split":
            split_result = split_dataset(
                input_path=args.input,
                input_format=args.format,
                output_path=args.output,
                train_ratio=args.train,
                val_ratio=args.val,
                test_ratio=args.test,
                seed=args.seed,
                overwrite=args.overwrite,
                dry_run=args.dry_run,
            )
            if not args.dry_run:
                write_result_file(Path(args.output), split_result)
            prefix = "dry-run " if args.dry_run else ""
            print(prefix + " ".join(f"{split}={count}" for split, count in split_result.counts.items()))
            return 0
        if args.command == "report":
            audit_result = _load_result(args.audit_result, AuditResult)
            split_result = _load_result(args.split_result, SplitResult)
            convert_result = _load_result(args.convert_result, ConvertResult)
            report_result = generate_report(
                input_path=args.input,
                input_format=args.format,
                output_path=args.output,
                audit_result=audit_result,
                split_result=split_result,
                convert_result=convert_result,
                overwrite=args.overwrite,
            )
            write_result_file(Path(args.output), report_result)
            print(f"markdown={report_result.markdown_path} html={report_result.html_path}")
            return 0
        if args.command == "preview":
            preview_result = preview_samples(
                input_path=args.input,
                input_format=args.format,
                output_path=args.output,
                samples=args.samples,
                seed=args.seed,
                overwrite=args.overwrite,
            )
            write_result_file(Path(args.output), preview_result)
            print(f"exported={preview_result.exported_count} contact_sheet={preview_result.contact_sheet_path.name}")
            return 0
        return 1
    except (VisionLabelOpsError, ValueError, FileNotFoundError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
