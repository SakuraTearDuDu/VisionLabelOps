from __future__ import annotations

from pathlib import Path

IMAGE_EXTENSIONS = {".bmp", ".jpeg", ".jpg", ".png", ".tif", ".tiff", ".webp"}
DEFAULT_BBOX_AREA_BINS = (0.01, 0.05, 0.15, 0.3, 0.5, 1.0)
DEFAULT_PREVIEW_COLUMNS = 2
DEFAULT_HTML_TEMPLATE = "report_template.html.j2"
PROJECT_NAME = "VisionLabelOps"
DEFAULT_SUBSET = "default"
RESULT_FILE_NAME = "result.json"


def resource_path(name: str) -> Path:
    return Path(__file__).parent / "resources" / name
