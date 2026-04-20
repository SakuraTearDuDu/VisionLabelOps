from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from visionlabelops.api import (
    audit_dataset,
    compute_stats,
    generate_report,
    preview_samples,
    split_dataset,
)
from visionlabelops.cli import main as cli_main
from visionlabelops.errors import OutputPathError, ValidationError
from visionlabelops.types import DatasetFormat


def test_audit_stats_preview_report_and_split_pipeline(supported_labelme_dataset_dir: Path, tmp_path: Path) -> None:
    audit_result = audit_dataset(supported_labelme_dataset_dir, DatasetFormat.LABELME)
    stats_result = compute_stats(supported_labelme_dataset_dir, DatasetFormat.LABELME)
    preview_result = preview_samples(
        input_path=supported_labelme_dataset_dir,
        input_format=DatasetFormat.LABELME,
        output_path=tmp_path / "preview",
        samples=2,
        seed=7,
    )
    split_result = split_dataset(
        input_path=supported_labelme_dataset_dir,
        input_format=DatasetFormat.LABELME,
        output_path=tmp_path / "split",
        train_ratio=0.5,
        val_ratio=0.25,
        test_ratio=0.25,
        seed=7,
    )
    report_result = generate_report(
        input_path=supported_labelme_dataset_dir,
        input_format=DatasetFormat.LABELME,
        output_path=tmp_path / "report",
        audit_result=audit_result,
        split_result=split_result,
    )

    assert audit_result.summary["image_count"] == 2
    assert stats_result.image_count == 2
    assert preview_result.exported_count == 2
    assert (tmp_path / "preview" / "contact_sheet.jpg").exists()
    assert (tmp_path / "split" / "train").exists()
    assert report_result.markdown_path.exists()
    assert report_result.html_path.exists()


def test_audit_detects_missing_and_corrupt_images(audit_problem_dir: Path) -> None:
    audit_result = audit_dataset(audit_problem_dir, DatasetFormat.LABELME)

    issue_codes = {issue.code for issue in audit_result.issues}
    assert "image-missing" in issue_codes
    assert "image-unreadable" in issue_codes


def test_cli_smoke(labelme_dataset_dir: Path, tmp_path: Path) -> None:
    output_dir = tmp_path / "cli-stats"
    command = [
        sys.executable,
        "-m",
        "visionlabelops.cli",
        "stats",
        "--input",
        str(labelme_dataset_dir),
        "--format",
        "labelme",
        "--output",
        str(output_dir),
        "--overwrite",
    ]

    result = subprocess.run(command, check=False, capture_output=True, text=True)

    assert result.returncode == 0, result.stderr
    assert "images=3" in result.stdout

    payload = json.loads((output_dir / "result.json").read_text(encoding="utf-8"))
    assert payload["image_count"] == 3


def test_cli_full_command_suite(supported_labelme_dataset_dir: Path, tmp_path: Path) -> None:
    audit_dir = tmp_path / "audit"
    stats_dir = tmp_path / "stats"
    preview_dir = tmp_path / "preview"
    report_dir = tmp_path / "report"
    convert_dir = tmp_path / "converted-yolo"
    split_dir = tmp_path / "split"

    assert cli_main(
        ["audit", "--input", str(supported_labelme_dataset_dir), "--format", "labelme", "--output", str(audit_dir)]
    ) == 0
    assert cli_main(
        ["stats", "--input", str(supported_labelme_dataset_dir), "--format", "labelme", "--output", str(stats_dir)]
    ) == 0
    assert cli_main(
        [
            "convert",
            "--input",
            str(supported_labelme_dataset_dir),
            "--input-format",
            "labelme",
            "--output",
            str(convert_dir),
            "--output-format",
            "yolo",
        ]
    ) == 0
    assert cli_main(
        [
            "split",
            "--input",
            str(supported_labelme_dataset_dir),
            "--format",
            "labelme",
            "--output",
            str(split_dir),
            "--train",
            "0.5",
            "--val",
            "0.25",
            "--test",
            "0.25",
            "--seed",
            "7",
        ]
    ) == 0
    assert cli_main(
        [
            "preview",
            "--input",
            str(supported_labelme_dataset_dir),
            "--format",
            "labelme",
            "--output",
            str(preview_dir),
            "--samples",
            "2",
            "--seed",
            "7",
        ]
    ) == 0
    assert cli_main(
        [
            "report",
            "--input",
            str(supported_labelme_dataset_dir),
            "--format",
            "labelme",
            "--output",
            str(report_dir),
            "--audit-result",
            str(audit_dir / "result.json"),
            "--split-result",
            str(split_dir / "result.json"),
            "--convert-result",
            str(convert_dir / "result.json"),
        ]
    ) == 0

    assert (audit_dir / "result.json").exists()
    assert (stats_dir / "result.json").exists()
    assert (convert_dir / "result.json").exists()
    assert (split_dir / "result.json").exists()
    assert (preview_dir / "result.json").exists()
    assert (report_dir / "result.json").exists()


def test_cli_dry_run_does_not_create_output(
    supported_labelme_dataset_dir: Path,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    convert_dir = tmp_path / "dry-run-convert"
    split_dir = tmp_path / "dry-run-split"

    assert cli_main(
        [
            "convert",
            "--input",
            str(supported_labelme_dataset_dir),
            "--input-format",
            "labelme",
            "--output",
            str(convert_dir),
            "--output-format",
            "yolo",
            "--dry-run",
        ]
    ) == 0
    convert_output = capsys.readouterr()
    assert "dry-run" in convert_output.out
    assert not convert_dir.exists()

    assert cli_main(
        [
            "split",
            "--input",
            str(supported_labelme_dataset_dir),
            "--format",
            "labelme",
            "--output",
            str(split_dir),
            "--train",
            "0.5",
            "--val",
            "0.25",
            "--test",
            "0.25",
            "--seed",
            "7",
            "--dry-run",
        ]
    ) == 0
    split_output = capsys.readouterr()
    assert "dry-run" in split_output.out
    assert not split_dir.exists()


def test_split_rejects_invalid_ratios(supported_labelme_dataset_dir: Path, tmp_path: Path) -> None:
    with pytest.raises(ValidationError):
        split_dataset(
            input_path=supported_labelme_dataset_dir,
            input_format=DatasetFormat.LABELME,
            output_path=tmp_path / "split-invalid",
            train_ratio=0.7,
            val_ratio=0.2,
            test_ratio=0.2,
            seed=7,
        )


def test_cli_rejects_existing_nonempty_output_without_overwrite(
    supported_labelme_dataset_dir: Path,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    output_dir = tmp_path / "stats-existing"
    output_dir.mkdir()
    (output_dir / "stale.txt").write_text("stale", encoding="utf-8")

    exit_code = cli_main(
        ["stats", "--input", str(supported_labelme_dataset_dir), "--format", "labelme", "--output", str(output_dir)]
    )
    captured = capsys.readouterr()

    assert exit_code == 2
    assert "already exists and is not empty" in captured.err
    assert (output_dir / "stale.txt").exists()


def test_output_path_file_raises_clear_error(supported_labelme_dataset_dir: Path, tmp_path: Path) -> None:
    output_file = tmp_path / "not-a-directory.txt"
    output_file.write_text("content", encoding="utf-8")

    with pytest.raises(OutputPathError):
        preview_samples(
            input_path=supported_labelme_dataset_dir,
            input_format=DatasetFormat.LABELME,
            output_path=output_file,
            samples=1,
            seed=7,
        )
