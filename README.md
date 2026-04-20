# VisionLabelOps

[![CI](https://github.com/SakuraTearDuDu/VisionLabelOps/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/SakuraTearDuDu/VisionLabelOps/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/downloads/)

VisionLabelOps is a lightweight Python toolkit for computer vision dataset audit, conversion, statistics, splitting, preview, and report generation.

It is built for users who work with YOLO, COCO, and Labelme datasets and want a small, scriptable, installable project instead of a notebook-heavy workflow, a GUI labeler, or a training framework add-on.

![VisionLabelOps preview output](docs/assets/readme-preview.jpg)

## What it is

- Detection-first dataset tooling for `audit`, `convert`, `stats`, `split`, `preview`, and `report`
- Focused on YOLO detection, COCO detection, and Labelme JSON
- Usable from both a Python API and a `vlo` CLI
- Designed to stay narrower than Datumaro and more engineering-oriented than ad-hoc conversion scripts

## Why this project exists

There are strong reference projects in this space, but they optimize for different goals:

- Datumaro provides a broad dataset engineering framework and large format surface.
- PyLabel focuses on low-friction utility workflows for end users.
- Supervision has clean ideas for lightweight preview and visualization.
- Labelme defines JSON structures many teams already use.
- JSON2YOLO and Ultralytics define common YOLO conversion behavior expectations.

VisionLabelOps sits in the middle:

- narrower than Datumaro
- more engineering-focused than PyLabel
- more systematic than one-off conversion scripts
- easier to install and automate than a mixed notebook/script toolbox

## Support and scope

### Supported formats

- YOLO detection
- COCO detection
- Labelme JSON

### Stable V1 conversion guarantees

- Labelme -> YOLO
- Labelme -> COCO
- YOLO -> COCO
- COCO -> YOLO

### Known limitations

- VisionLabelOps is intentionally detection-first. It is not a segmentation, keypoint, tracking, GUI, web, or training framework project.
- Labelme support is limited to `rectangle` and `polygon`.
- COCO import skips `iscrowd=1` annotations.
- The current YOLO reader is intentionally narrow and stable rather than broadly heuristic.

## Install

### From a source checkout

Windows PowerShell:

```powershell
git clone https://github.com/SakuraTearDuDu/VisionLabelOps.git
cd VisionLabelOps
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .[dev]
```

Linux/macOS bash or zsh:

```bash
git clone https://github.com/SakuraTearDuDu/VisionLabelOps.git
cd VisionLabelOps
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .[dev]
```

### Minimal runtime install from the checkout

```bash
python -m pip install .
```

## Quick start

The repository includes a tiny example dataset in `examples/data/labelme-mini`.

### Inspect the example dataset

PowerShell:

```powershell
vlo stats --input .\examples\data\labelme-mini --format labelme --output .\tmp\stats --overwrite
vlo audit --input .\examples\data\labelme-mini --format labelme --output .\tmp\audit --overwrite
```

Bash:

```bash
vlo stats --input ./examples/data/labelme-mini --format labelme --output ./tmp/stats --overwrite
vlo audit --input ./examples/data/labelme-mini --format labelme --output ./tmp/audit --overwrite
```

### Preview and report

```bash
vlo preview --input ./examples/data/labelme-mini --format labelme --output ./tmp/preview --samples 2 --seed 7 --overwrite
vlo report --input ./examples/data/labelme-mini --format labelme --output ./tmp/report --overwrite
```

### Run the API example

```bash
python examples/basic_api.py
```

## CLI overview

```text
vlo audit --input --format --output [--overwrite] [--stdout-json] [--strict]
vlo convert --input --input-format --output --output-format [--overwrite] [--dry-run] [--stdout-json]
vlo stats --input --format --output [--overwrite] [--stdout-json]
vlo split --input --format --output --train --val --test --seed [--overwrite] [--dry-run] [--stdout-json]
vlo report --input --format --output [--audit-result ...] [--split-result ...] [--convert-result ...] [--overwrite] [--stdout-json]
vlo preview --input --format --output --samples --seed [--overwrite] [--stdout-json]
```

### CLI behavior

- write commands require an explicit output directory
- `--overwrite` is required before replacing a non-empty output directory
- `convert --dry-run` and `split --dry-run` do not create output directories or `result.json`
- non-dry-run commands write `result.json`
- result files include `schema_version` and `result_type`
- `--stdout-json` prints structured output for scripts and CI
- `audit --strict` returns a non-zero exit code when error-level issues are present

### Automation example

```bash
vlo audit \
  --input ./examples/data/labelme-mini \
  --format labelme \
  --output ./tmp/audit \
  --overwrite \
  --stdout-json \
  --strict
```

## Python API

```python
from pathlib import Path

from visionlabelops import audit_dataset, compute_stats, generate_report, read_dataset

dataset_root = Path("examples/data/labelme-mini")

dataset = read_dataset(dataset_root, "labelme")
stats = compute_stats(dataset_root, "labelme")
audit = audit_dataset(dataset_root, "labelme")
report = generate_report(
    input_path=dataset_root,
    input_format="labelme",
    output_path=Path("tmp/report"),
    audit_result=audit,
    overwrite=True,
)

print(dataset.image_count)
print(stats.annotation_count)
print(report.markdown_path)
```

The repository also includes [`examples/basic_api.py`](examples/basic_api.py) as a runnable example.

## Output conventions

- `audit` writes `result.json`
- `stats` writes `result.json`
- `convert` writes converted data plus `result.json`
- `split` writes the materialized split plus `result.json`
- `preview` writes sample overlays, `contact_sheet.jpg`, and `result.json`
- `report` writes `report.md`, `report.html`, and `result.json`

## Development

```bash
python -m venv .venv
python -m pip install -e .[dev]
pre-commit install
just verify
```

The underlying commands remain:

```bash
python -m ruff check src tests
python -m mypy src
python -m pytest
python -m build --no-isolation
python -m twine check dist/*
```

Additional project notes:

- [docs/quickstart.md](docs/quickstart.md)
- [docs/architecture.md](docs/architecture.md)
- [docs/reference_notes.md](docs/reference_notes.md)
- [docs/release_checklist.md](docs/release_checklist.md)

## FAQ

### Is this a fork of Datumaro, PyLabel, Labelme, JSON2YOLO, or Ultralytics?

No. VisionLabelOps is a clean-room implementation with its own codebase and package layout.

### Does this project support segmentation or keypoints?

Not as a V1 goal. Polygon geometry may be preserved when available, but the toolkit is detection-first.

### Is Windows supported?

Yes. The docs, CLI examples, and CI explicitly cover Windows, and the repository now includes Linux/macOS examples as well.

## License and reference boundaries

VisionLabelOps is released under the MIT License.

Reference projects were used for architecture, workflow, file format, and behavior research only:

- Datumaro: modular dataset operations and CLI shape
- PyLabel: low-friction conversion and utility workflow
- Supervision: preview and visualization ideas
- Labelme: JSON and shape semantics
- JSON2YOLO / Ultralytics: YOLO conversion behavior expectations

The project does not copy GPL / AGPL source code, mapping tables, or internal implementations from those repositories.
