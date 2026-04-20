from __future__ import annotations

from dataclasses import dataclass

from visionlabelops.constants import DEFAULT_BBOX_AREA_BINS, DEFAULT_PREVIEW_COLUMNS


@dataclass(frozen=True)
class PreviewConfig:
    columns: int = DEFAULT_PREVIEW_COLUMNS
    padding: int = 12
    label_padding: int = 6


@dataclass(frozen=True)
class StatsConfig:
    area_bins: tuple[float, ...] = DEFAULT_BBOX_AREA_BINS
