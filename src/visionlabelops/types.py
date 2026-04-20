from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path


class DatasetFormat(str, Enum):
    YOLO = "yolo"
    COCO = "coco"
    LABELME = "labelme"

    @classmethod
    def from_value(cls, value: str | DatasetFormat) -> DatasetFormat:
        if isinstance(value, DatasetFormat):
            return value
        normalized = value.strip().lower()
        return cls(normalized)


class Severity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


@dataclass(frozen=True)
class Category:
    index: int
    name: str
    original_id: int | None = None


@dataclass(frozen=True)
class BBox:
    xmin: float
    ymin: float
    xmax: float
    ymax: float

    @classmethod
    def from_xywh(cls, x: float, y: float, width: float, height: float) -> BBox:
        return cls(xmin=x, ymin=y, xmax=x + width, ymax=y + height)

    @property
    def width(self) -> float:
        return self.xmax - self.xmin

    @property
    def height(self) -> float:
        return self.ymax - self.ymin

    @property
    def area(self) -> float:
        return max(self.width, 0.0) * max(self.height, 0.0)

    def to_xywh(self) -> tuple[float, float, float, float]:
        return self.xmin, self.ymin, self.width, self.height

    def to_yolo(self, width: int, height: int) -> tuple[float, float, float, float]:
        x_center = ((self.xmin + self.xmax) / 2.0) / width
        y_center = ((self.ymin + self.ymax) / 2.0) / height
        box_width = self.width / width
        box_height = self.height / height
        return x_center, y_center, box_width, box_height

    def is_valid(self) -> bool:
        return self.width > 0 and self.height > 0

    def is_within(self, width: int, height: int) -> bool:
        return self.xmin >= 0 and self.ymin >= 0 and self.xmax <= width and self.ymax <= height


@dataclass(frozen=True)
class Polygon:
    points: tuple[tuple[float, float], ...]

    @property
    def bbox(self) -> BBox:
        xs = [point[0] for point in self.points]
        ys = [point[1] for point in self.points]
        return BBox(min(xs), min(ys), max(xs), max(ys))

    def normalized(self, width: int, height: int) -> list[float]:
        values: list[float] = []
        for x, y in self.points:
            values.extend([x / width, y / height])
        return values


@dataclass
class Annotation:
    category_id: int
    category_name: str
    bbox: BBox
    polygon: Polygon | None = None
    source_id: int | str | None = None
    iscrowd: bool = False


@dataclass
class ImageRecord:
    id: str
    file_name: str
    path: Path | None
    width: int | None
    height: int | None
    annotations: list[Annotation] = field(default_factory=list)
    subset: str = "default"
    annotation_path: Path | None = None


@dataclass
class Dataset:
    format: DatasetFormat
    root_dir: Path
    images: list[ImageRecord]
    categories: list[Category]
    source_path: Path
    metadata: dict[str, object] = field(default_factory=dict)

    @property
    def category_map(self) -> dict[int, Category]:
        return {category.index: category for category in self.categories}

    @property
    def image_count(self) -> int:
        return len(self.images)

    @property
    def annotation_count(self) -> int:
        return sum(len(image.annotations) for image in self.images)


@dataclass
class AuditIssue:
    code: str
    severity: Severity
    message: str
    location: str


@dataclass
class AuditResult:
    summary: dict[str, object]
    issues: list[AuditIssue]


@dataclass
class StatsResult:
    image_count: int
    annotation_count: int
    category_count: int
    per_class_instances: dict[str, int]
    per_image_box_distribution: dict[str, int]
    image_size_distribution: dict[str, int]
    bbox_area_distribution: dict[str, int]


@dataclass
class ConvertResult:
    input_format: DatasetFormat
    output_format: DatasetFormat
    output_path: Path
    image_count: int
    annotation_count: int
    categories: list[str]
    dry_run: bool = False


@dataclass
class SplitResult:
    output_path: Path
    counts: dict[str, int]
    assignments: dict[str, list[str]]
    summary: dict[str, object]
    dry_run: bool = False


@dataclass
class PreviewResult:
    output_path: Path
    exported_files: list[Path]
    contact_sheet_path: Path

    @property
    def exported_count(self) -> int:
        return len(self.exported_files)


@dataclass
class ReportResult:
    output_path: Path
    markdown_path: Path
    html_path: Path
