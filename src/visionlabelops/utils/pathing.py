from __future__ import annotations

import shutil
from pathlib import Path

from visionlabelops.constants import IMAGE_EXTENSIONS
from visionlabelops.errors import OutputPathError
from visionlabelops.types import AuditResult, ConvertResult, PreviewResult, ReportResult, SplitResult, StatsResult
from visionlabelops.utils.serialization import dump_result_file


def ensure_output_path(path: Path, overwrite: bool = False) -> Path:
    path = path.resolve()
    if path.exists() and not path.is_dir():
        raise OutputPathError(f"Output path must be a directory: {path}")
    if path.exists() and any(path.iterdir()) and not overwrite:
        raise OutputPathError(f"Output path already exists and is not empty: {path}")
    if path.exists() and overwrite:
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def write_result_file(
    output_dir: Path,
    payload: AuditResult | StatsResult | ConvertResult | SplitResult | PreviewResult | ReportResult,
) -> Path:
    return dump_result_file(output_dir, payload)


def find_image_by_stem(directory: Path, stem: str) -> Path | None:
    for extension in IMAGE_EXTENSIONS:
        candidate = directory / f"{stem}{extension}"
        if candidate.exists():
            return candidate
    return None
