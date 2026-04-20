# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Changed

- Centralized package versioning around one source file and dynamic setuptools metadata.
- Standardized public high-level APIs on path-first inputs while keeping dataset-first core services.
- Added schema versioning and centralized result serialization / deserialization for CLI result files.
- Reworked repository examples to use `examples/data/labelme-mini` instead of test fixtures.
- Rewrote README and quickstart docs for cross-platform usage and automation-oriented examples.
- Hardened CI with coverage thresholds, `twine check`, real built-wheel smoke, and macOS smoke coverage.
- Added `pre-commit` and `justfile` for faster contributor verification loops.

## [0.1.0] - 2026-04-20

### Added

- Initial public release of VisionLabelOps.
- Detection-first dataset readers and writers for YOLO, COCO, and Labelme.
- Unified `vlo` CLI for `audit`, `convert`, `stats`, `split`, `report`, and `preview`.
- Python API entrypoints for dataset read, audit, stats, conversion, split, preview, and report generation.
- Markdown and HTML report generation.
- Test suite, CI workflow, and packaging configuration for editable installs and built artifacts.

### Changed

- Standardized output-directory protection so all write commands require `--overwrite` before replacing a non-empty output directory.
- Made API defaults non-destructive by defaulting `overwrite=False`.
- Aligned `convert --dry-run` and `split --dry-run` so they do not write `result.json` or create output directories.
- Added split-ratio validation and clearer CLI error handling.
- Hardened YOLO parsing so invalid numeric fields are reported as read issues instead of aborting the whole dataset load.

### Known limitations

- V1 is intentionally detection-first and is not a segmentation, keypoint, tracking, GUI, or training framework project.
- Labelme support is limited to `rectangle` and `polygon`.
- COCO import skips `iscrowd=1` annotations and only preserves simple polygon segmentations.
- The stable, documented V1 conversion guarantees are Labelme -> YOLO, Labelme -> COCO, YOLO -> COCO, and COCO -> YOLO.
