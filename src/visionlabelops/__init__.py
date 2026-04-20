from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version

from visionlabelops._version import __version__ as _fallback_version
from visionlabelops.api import (
    audit_dataset,
    compute_stats,
    convert_dataset,
    generate_report,
    preview_samples,
    read_dataset,
    split_dataset,
)

__all__ = [
    "__version__",
    "audit_dataset",
    "compute_stats",
    "convert_dataset",
    "generate_report",
    "preview_samples",
    "read_dataset",
    "split_dataset",
]

try:
    __version__ = version("visionlabelops")
except PackageNotFoundError:
    __version__ = _fallback_version
