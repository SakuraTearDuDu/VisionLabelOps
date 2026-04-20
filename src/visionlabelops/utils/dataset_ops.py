from __future__ import annotations

from collections import Counter, defaultdict

from visionlabelops.types import Dataset, ImageRecord


def image_annotation_counts(dataset: Dataset) -> Counter[str]:
    return Counter(str(len(image.annotations)) for image in dataset.images)


def class_instance_counts(dataset: Dataset) -> Counter[str]:
    counter: Counter[str] = Counter()
    for image in dataset.images:
        for annotation in image.annotations:
            counter[annotation.category_name] += 1
    return counter


def image_size_distribution(dataset: Dataset) -> Counter[str]:
    counter: Counter[str] = Counter()
    for image in dataset.images:
        if image.width is not None and image.height is not None:
            counter[f"{image.width}x{image.height}"] += 1
    return counter


def bbox_area_ratios(dataset: Dataset) -> list[float]:
    ratios: list[float] = []
    for image in dataset.images:
        if not image.width or not image.height:
            continue
        image_area = image.width * image.height
        for annotation in image.annotations:
            ratios.append(annotation.bbox.area / image_area if image_area else 0.0)
    return ratios


def subset_groups(dataset: Dataset) -> dict[str, list[ImageRecord]]:
    groups: dict[str, list[ImageRecord]] = defaultdict(list)
    for image in dataset.images:
        groups[image.subset].append(image)
    return dict(groups)
