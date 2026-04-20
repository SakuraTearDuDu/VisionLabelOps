# VisionLabelOps

> Detection-first dataset tooling for audit, conversion, statistics, splits, previews, and reports.

**English** | [简体中文](README.zh-CN.md)

[![CI](https://github.com/SakuraTearDuDu/VisionLabelOps/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/SakuraTearDuDu/VisionLabelOps/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/downloads/)

![VisionLabelOps hero banner](docs/assets/readme-hero.svg)

VisionLabelOps is a lightweight Python toolkit for computer vision dataset audit, conversion, statistics, splitting, preview, and report generation. It is designed for teams that work with YOLO, COCO, and Labelme datasets and want something smaller than a full dataset platform, but more structured than one-off scripts.

## Highlights

- 🔎 **Focused, not sprawling**: detection-first scope with explicit boundaries instead of a broad plugin platform.
- ⚙️ **Unified CLI + API**: the same workflows are available from `vlo` and from importable Python helpers.
- 🧪 **Automation-friendly**: structured result files, `--stdout-json`, CI validation, and reproducible example data.
- 🧼 **Clean-room and GitHub-friendly**: clear reference boundaries, typed Python package layout, tests, docs, and release-ready metadata.

## Start Here

- Read the [Quick Start](docs/quickstart.md) if you want the fastest path from clone to first command.
- Use the repository example dataset at [`examples/data/labelme-mini`](examples/data/labelme-mini) to try the CLI immediately.
- Jump to [Results Preview](#results-preview) if you want to see what the toolkit produces.

## Support At A Glance

| Area | Current V1 support |
| --- | --- |
| Formats | YOLO detection, COCO detection, Labelme JSON |
| Stable conversions | Labelme -> YOLO, Labelme -> COCO, YOLO -> COCO, COCO -> YOLO |
| Core workflows | `audit`, `convert`, `stats`, `split`, `preview`, `report` |
| Usage style | Python API + `vlo` CLI |
| Example data | `examples/data/labelme-mini` |

## Core Capabilities

| Command | What it gives you | Typical output |
| --- | --- | --- |
| `vlo audit` | dataset quality checks and risk summary | `result.json` |
| `vlo convert` | clean-room format conversion | converted dataset + `result.json` |
| `vlo stats` | size, class, and box distribution summary | `result.json` |
| `vlo split` | reproducible train/val/test materialization | split dataset + `result.json` |
| `vlo preview` | sampled overlays and contact sheets | annotated images + `contact_sheet.jpg` |
| `vlo report` | markdown + HTML summary package | `report.md`, `report.html`, `result.json` |

## Results Preview

Real repository artifacts, generated from `examples/data/labelme-mini`.

| Preview overlays | CLI and report workflow |
| --- | --- |
| ![Preview contact sheet](docs/assets/readme-preview.jpg) | ![CLI workflow preview](docs/assets/readme-cli-preview.png) |

For GitHub repository sharing outside the README, a social preview asset is also prepared at [`docs/assets/social-preview.png`](docs/assets/social-preview.png).

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

### Minimal runtime install

```bash
python -m pip install .
```

## Quick Start

### Minimal CLI path

```bash
vlo stats --input ./examples/data/labelme-mini --format labelme --output ./tmp/stats --overwrite
vlo audit --input ./examples/data/labelme-mini --format labelme --output ./tmp/audit --overwrite
vlo preview --input ./examples/data/labelme-mini --format labelme --output ./tmp/preview --samples 2 --seed 7 --overwrite
```

### Script-friendly mode

```bash
vlo audit \
  --input ./examples/data/labelme-mini \
  --format labelme \
  --output ./tmp/audit-json \
  --overwrite \
  --stdout-json \
  --strict
```

### Runnable API example

```bash
python examples/basic_api.py
```

For the full setup path and platform-specific notes, see [docs/quickstart.md](docs/quickstart.md).

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

## Scope Boundaries

### What this repository is

- A lightweight toolkit for dataset audit, conversion, summary statistics, splitting, previews, and reports.
- A detection-first package aimed at YOLO / COCO / Labelme workflows.
- A clean-room implementation with a narrow, testable feature surface.

### What this repository is not

- Not a segmentation, keypoint, tracking, or training framework project.
- Not a GUI labeling application.
- Not a web service or cloud platform.
- Not a broad dataset format compatibility layer.

### Known limitations

- Labelme support is limited to `rectangle` and `polygon`.
- COCO import skips `iscrowd=1` annotations.
- The YOLO reader intentionally favors a narrow, stable layout over heuristic compatibility sprawl.

## Why this project exists

There are strong reference projects in this area, but they optimize for different goals:

- Datumaro is broader and more platform-like.
- PyLabel is lightweight and user-friendly, but less centered on unified repo engineering.
- Supervision contributes strong ideas around preview and visualization.

VisionLabelOps is intentionally in between: lighter than a broad dataset platform, more structured than ad-hoc scripts, and easier to automate than a notebook-first workflow.

## FAQ

### Is this a fork of Datumaro, PyLabel, Labelme, JSON2YOLO, or Ultralytics?

No. VisionLabelOps is a clean-room implementation with its own package layout, tests, and documentation.

### Does this project support segmentation or keypoints?

Not as a V1 goal. Polygon geometry may be preserved where relevant, but the project remains detection-first.

### Is Windows supported?

Yes. The CLI, docs, and CI explicitly cover Windows, while installation and quick start examples are also provided for Linux/macOS.

## Development Notes

```bash
python -m venv .venv
python -m pip install -e .[dev]
pre-commit install
just verify
```

Useful docs:

- [Quick Start](docs/quickstart.md)
- [Architecture](docs/architecture.md)
- [Reference Notes](docs/reference_notes.md)
- [Release Checklist](docs/release_checklist.md)
- [GitHub Showcase Checklist](docs/github_showcase_checklist.md)

## License and reference boundaries

VisionLabelOps is released under the [MIT License](LICENSE).

Reference repositories were used for architecture, workflow, file-format, and behavior research only:

- Datumaro for modular dataset operations and task-oriented CLI structure
- PyLabel for approachable conversion and analysis workflow ideas
- Supervision for preview and visualization direction
- Labelme for JSON and shape semantics
- JSON2YOLO / Ultralytics for YOLO conversion behavior expectations

The project does not copy GPL / AGPL source code, mapping tables, or internal implementations from those repositories.
