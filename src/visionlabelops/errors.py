from __future__ import annotations


class VisionLabelOpsError(Exception):
    """Base error for VisionLabelOps."""


class DatasetFormatError(VisionLabelOpsError):
    """Raised when a dataset format is unsupported or malformed."""


class OutputPathError(VisionLabelOpsError):
    """Raised when an output path is invalid for the requested operation."""


class ValidationError(VisionLabelOpsError):
    """Raised when user-provided inputs fail validation."""
