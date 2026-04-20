# VisionLabelOps v0.1.1

## Summary

VisionLabelOps v0.1.1 is a repository hardening and showcase polish release for teams working with detection-first computer vision datasets. It keeps the project focused on YOLO, COCO, and Labelme workflows while improving packaging consistency, GitHub presentation, bilingual documentation, and release readiness.

## Highlights

- Repository maturity hardening across packaging, CI, examples, and public API consistency
- Polished GitHub showcase with a clearer README front page and reusable README/social preview assets
- Simplified Chinese README and quickstart entry points
- Clearer bilingual navigation and release-facing documentation assets
- Stable detection-first scope, without expanding into a broader platform

## Current support

- YOLO detection
- COCO detection
- Labelme JSON
- `audit`, `convert`, `stats`, `split`, `preview`, `report`
- Unified CLI and Python API

## Known limitations

- Detection-first scope only
- Not a segmentation, keypoint, tracking, GUI, web platform, or training framework project
- Labelme currently supports `rectangle` and `polygon` only
- COCO import skips `iscrowd=1`
- The YOLO reader intentionally remains narrow and stable instead of broadly heuristic

## Getting started

- Install from the repository checkout:
  - `python -m venv .venv`
  - `python -m pip install -e .[dev]`
- Start with the repository example dataset at `examples/data/labelme-mini`
- Main entry points:
  - `README.md`
  - `README.zh-CN.md`
  - `docs/quickstart.md`
  - `docs/quickstart.zh-CN.md`

## Closing note

This release represents the first polished public shape of VisionLabelOps: focused, lightweight, scriptable, and engineered for repeatable dataset operations rather than platform sprawl.
