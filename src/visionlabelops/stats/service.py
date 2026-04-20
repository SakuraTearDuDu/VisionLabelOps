from __future__ import annotations

from collections import Counter

from visionlabelops.config import StatsConfig
from visionlabelops.types import Dataset, StatsResult
from visionlabelops.utils.dataset_ops import (
    bbox_area_ratios,
    class_instance_counts,
    image_annotation_counts,
    image_size_distribution,
)


def _bucket_area_ratios(ratios: list[float], bins: tuple[float, ...]) -> dict[str, int]:
    counter: Counter[str] = Counter()
    for ratio in ratios:
        lower_bound = 0.0
        assigned = False
        for upper_bound in bins:
            if ratio <= upper_bound:
                counter[f"{lower_bound:.2f}-{upper_bound:.2f}"] += 1
                assigned = True
                break
            lower_bound = upper_bound
        if not assigned:
            counter[f">{bins[-1]:.2f}"] += 1
    return dict(counter)


def compute_dataset_stats(dataset: Dataset, config: StatsConfig | None = None) -> StatsResult:
    config = config or StatsConfig()
    return StatsResult(
        image_count=dataset.image_count,
        annotation_count=dataset.annotation_count,
        category_count=len(dataset.categories),
        per_class_instances=dict(class_instance_counts(dataset)),
        per_image_box_distribution=dict(image_annotation_counts(dataset)),
        image_size_distribution=dict(image_size_distribution(dataset)),
        bbox_area_distribution=_bucket_area_ratios(bbox_area_ratios(dataset), config.area_bins),
    )
