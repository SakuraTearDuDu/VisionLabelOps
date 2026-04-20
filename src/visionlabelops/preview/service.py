from __future__ import annotations

import random
from pathlib import Path

from visionlabelops.config import PreviewConfig
from visionlabelops.types import Dataset, PreviewResult
from visionlabelops.utils.image_ops import create_contact_sheet, render_preview


def generate_preview(
    dataset: Dataset,
    output_path: Path,
    samples: int,
    seed: int,
    config: PreviewConfig | None = None,
) -> PreviewResult:
    config = config or PreviewConfig()
    rng = random.Random(seed)
    candidates = [image for image in dataset.images if image.path is not None and image.path.exists()]
    selected = rng.sample(candidates, k=min(samples, len(candidates))) if candidates else []
    preview_dir = output_path / "samples"
    exported_files: list[Path] = []
    for image in selected:
        destination = preview_dir / f"{image.subset}_{Path(image.file_name).stem}.jpg"
        exported_files.append(render_preview(image, destination))
    contact_sheet_path = create_contact_sheet(exported_files, output_path / "contact_sheet.jpg", columns=config.columns)
    return PreviewResult(
        output_path=output_path.resolve(),
        exported_files=exported_files,
        contact_sheet_path=contact_sheet_path,
    )
