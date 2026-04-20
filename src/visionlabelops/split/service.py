from __future__ import annotations

import math
import random
from collections import Counter
from copy import deepcopy
from pathlib import Path

from visionlabelops.convert.service import convert_dataset_to_format
from visionlabelops.errors import ValidationError
from visionlabelops.types import Dataset, ImageRecord, SplitResult


def _target_counts(total: int, ratios: dict[str, float]) -> dict[str, int]:
    raw = {split: ratios[split] * total for split in ratios}
    counts = {split: int(raw[split]) for split in ratios}
    remainder = total - sum(counts.values())
    for split, _ in sorted(raw.items(), key=lambda item: item[1] - int(item[1]), reverse=True):
        if remainder <= 0:
            break
        counts[split] += 1
        remainder -= 1
    return counts


def _validate_ratios(ratios: dict[str, float]) -> None:
    if any(value < 0 for value in ratios.values()):
        raise ValidationError("Split ratios must be non-negative.")
    total = sum(ratios.values())
    if not math.isclose(total, 1.0, abs_tol=1e-6):
        raise ValidationError("Split ratios must sum to 1.0.")


def _split_images(dataset: Dataset, ratios: dict[str, float], seed: int) -> dict[str, list[ImageRecord]]:
    rng = random.Random(seed)
    totals = _target_counts(len(dataset.images), ratios)
    per_class_total: Counter[int] = Counter()
    for image in dataset.images:
        for annotation in image.annotations:
            per_class_total[annotation.category_id] += 1

    assignments: dict[str, list[ImageRecord]] = {split: [] for split in ratios}
    current_class_counts: dict[str, Counter[int]] = {split: Counter() for split in ratios}
    remaining_capacity = totals.copy()

    scored_images: list[tuple[float, float, ImageRecord]] = []
    for image in dataset.images:
        category_ids = {annotation.category_id for annotation in image.annotations}
        rarity = sum(1.0 / max(per_class_total[category_id], 1) for category_id in category_ids)
        scored_images.append((rarity, rng.random(), image))
    scored_images.sort(key=lambda item: (item[0], item[1]), reverse=True)

    for _, _, image in scored_images:
        category_ids = {annotation.category_id for annotation in image.annotations}
        best_split = None
        best_score = float("-inf")
        for split, capacity in remaining_capacity.items():
            if capacity <= 0:
                continue
            desired = totals[split]
            capacity_score = capacity / max(desired, 1)
            label_score = 0.0
            for category_id in category_ids:
                target_class_count = ratios[split] * per_class_total[category_id]
                deficit = target_class_count - current_class_counts[split][category_id]
                label_score += deficit / max(target_class_count, 1.0)
            total_score = (label_score * 2.0) + capacity_score
            if total_score > best_score:
                best_score = total_score
                best_split = split
        if best_split is None:
            best_split = next(split for split, capacity in remaining_capacity.items() if capacity > 0)
        clone = deepcopy(image)
        clone.subset = best_split
        assignments[best_split].append(clone)
        remaining_capacity[best_split] -= 1
        for annotation in clone.annotations:
            current_class_counts[best_split][annotation.category_id] += 1
    return assignments


def split_dataset_materialized(
    dataset: Dataset,
    output_path: Path,
    train_ratio: float,
    val_ratio: float,
    test_ratio: float,
    seed: int,
    dry_run: bool = False,
) -> SplitResult:
    ratios = {"train": train_ratio, "val": val_ratio, "test": test_ratio}
    _validate_ratios(ratios)
    assignments = _split_images(dataset, ratios, seed)
    split_dataset = deepcopy(dataset)
    split_dataset.images = [image for group in assignments.values() for image in group]

    if not dry_run:
        convert_dataset_to_format(split_dataset, dataset.format, output_path, dry_run=False)

    counts = {split: len(images) for split, images in assignments.items()}
    manifest = {split: [image.file_name for image in images] for split, images in assignments.items()}
    return SplitResult(
        output_path=output_path.resolve(),
        counts=counts,
        assignments=manifest,
        summary={"seed": seed, "ratios": ratios},
        dry_run=dry_run,
    )
