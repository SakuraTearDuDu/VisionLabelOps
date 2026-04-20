# VisionLabelOps

VisionLabelOps is a lightweight Python toolkit for machine-vision dataset audit, conversion, statistics, splitting, reporting, and preview workflows.

It is designed for users who work with YOLO, COCO, and Labelme datasets and want a small, installable, scriptable project instead of a notebook-heavy workflow, a GUI labeler, or a training framework add-on.

## Why this project exists

There are strong reference projects in this space, but they each optimize for something slightly different:

- Datumaro provides a broad dataset engineering framework with a large format surface.
- PyLabel makes common conversion and dataset utility tasks easy for end users.
- Supervision offers clean ideas for lightweight preview and visualization.
- Labelme defines the JSON structures many teams already use.
- JSON2YOLO and Ultralytics define behavior expectations for YOLO conversion.

VisionLabelOps sits in the middle:

- narrower than Datumaro
- more engineering-focused than PyLabel
- more systematic than one-off conversion scripts
- cleaner to install and automate than a mixed notebook/script toolbox

## Differentiation

Compared with Datumaro, VisionLabelOps is intentionally smaller and focused on YOLO / COCO / Labelme detection workflows.

Compared with PyLabel, VisionLabelOps emphasizes a consistent CLI, typed Python API, tests, CI, and open-source repo hygiene.

Compared with ad-hoc conversion scripts, VisionLabelOps keeps audit, conversion, stats, split, report, and preview behind one shared internal model and one CLI entrypoint.

## Features

- `audit`: dataset quality checks and risk summaries
- `convert`: clean-room conversion between supported formats
- `stats`: image, annotation, class, box-count, size, and bbox-area summaries
- `split`: reproducible train/val/test materialization with a seed
- `report`: Markdown and HTML reports
- `preview`: sampled visual overlays and contact sheets
- Python API and CLI access to the same core workflows

## V1 format support

### Input / output formats

- YOLO detection
- COCO detection
- Labelme JSON

### Conversion paths

- Labelme -> YOLO
- Labelme -> COCO
- YOLO -> COCO
- COCO -> YOLO

### Labelme scope

V1 supports Labelme `rectangle` and `polygon` shapes only. Other shape types are reported during audit and cause conversion and split materialization to fail with a clear error.

### Conversion stability note

The stable, documented V1 conversion guarantees are:

- Labelme -> YOLO
- Labelme -> COCO
- YOLO -> COCO
- COCO -> YOLO

The package also includes a Labelme writer used by internal materialization workflows, but it is not advertised as a broader V1 conversion guarantee.

## Installation

### Standard install

```powershell
git clone https://github.com/SakuraTearDuDu/VisionLabelOps.git D:\VisionLabelOps
cd D:\VisionLabelOps
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .[dev]
```

### Minimal runtime install

```powershell
python -m pip install .
```

## Quick Start

### 1. Inspect a dataset

```powershell
vlo stats --input D:\data\labelme --format labelme --output D:\work\stats --overwrite
vlo audit --input D:\data\labelme --format labelme --output D:\work\audit --overwrite
```

### 2. Convert a dataset

```powershell
vlo convert `
  --input D:\data\labelme `
  --input-format labelme `
  --output D:\work\converted-yolo `
  --output-format yolo `
  --overwrite
```

### 3. Split a dataset

```powershell
vlo split `
  --input D:\data\labelme `
  --format labelme `
  --output D:\work\split `
  --train 0.7 `
  --val 0.2 `
  --test 0.1 `
  --seed 7 `
  --overwrite
```

### 4. Preview samples and generate a report

```powershell
vlo preview `
  --input D:\data\labelme `
  --format labelme `
  --output D:\work\preview `
  --samples 12 `
  --seed 7 `
  --overwrite

vlo report `
  --input D:\data\labelme `
  --format labelme `
  --output D:\work\report `
  --overwrite
```

## CLI reference

```text
vlo audit --input --format --output [--overwrite]
vlo convert --input --input-format --output --output-format [--overwrite] [--dry-run]
vlo stats --input --format --output [--overwrite]
vlo split --input --format --output --train --val --test --seed [--overwrite] [--dry-run]
vlo report --input --format --output [--audit-result ...] [--split-result ...] [--convert-result ...] [--overwrite]
vlo preview --input --format --output --samples --seed [--overwrite]
```

### CLI behavior

- write commands require an explicit output path
- `--overwrite` is required to replace a non-empty output directory
- if `--output` points to a file instead of a directory, the CLI exits with a readable error
- `convert` and `split` support `--dry-run`
- `--dry-run` prints a summary and does not create output directories or `result.json`
- non-dry-run commands write a machine-readable `result.json` into the output directory
- CLI stdout stays short and summary-oriented for scripting

## Python API examples

```python
from visionlabelops import (
    audit_dataset,
    compute_stats,
    convert_dataset,
    generate_report,
    preview_samples,
    read_dataset,
    split_dataset,
)

dataset = read_dataset(r"D:\data\labelme", "labelme")
stats = compute_stats(dataset)
audit = audit_dataset(dataset)

convert_dataset(
    input_path=r"D:\data\labelme",
    input_format="labelme",
    output_path=r"D:\work\converted-coco",
    output_format="coco",
    overwrite=True,
)

split_dataset(
    input_path=r"D:\data\labelme",
    input_format="labelme",
    output_path=r"D:\work\split",
    train_ratio=0.7,
    val_ratio=0.2,
    test_ratio=0.1,
    seed=7,
    overwrite=True,
)

preview_samples(
    input_path=r"D:\data\labelme",
    input_format="labelme",
    output_path=r"D:\work\preview",
    samples=8,
    seed=7,
    overwrite=True,
)

generate_report(
    input_path=r"D:\data\labelme",
    input_format="labelme",
    output_path=r"D:\work\report",
    audit_result=audit,
    overwrite=True,
)
```

The repository includes [examples/basic_api.py](examples/basic_api.py) as a small runnable example.

## Supported dataset layout notes

### YOLO

- expects `data.yaml`
- reads `images/<split>` and `labels/<split>`
- writes normalized `class x_center y_center width height`

### COCO

- expects `annotations.json` or a direct JSON path
- writes `images/<split>/...` and `annotations.json`
- uses detection-first COCO output with `bbox`, `area`, `category_id`, and `iscrowd`
- skips `iscrowd=1` annotations during import
- preserves only simple polygon segmentations when present; V1 is not a full segmentation toolchain

### Labelme

- expects one JSON file per image or a directory of JSON files
- reads `imagePath`, `imageHeight`, `imageWidth`, and `shapes`
- supports `rectangle` and `polygon`

## Report outputs

`vlo report` generates:

- `report.md`
- `report.html`
- `result.json`

The report includes:

- dataset overview
- audit summary
- class statistics
- risk list
- optional split summary
- optional conversion summary

## Known limitations

- V1 is intentionally detection-first and does not aim to be a segmentation, keypoint, tracking, training, GUI, or web platform project.
- Labelme support is limited to `rectangle` and `polygon`.
- COCO import skips `iscrowd=1` annotations.
- Only simple polygon segmentations are preserved when available.
- The stable V1 conversion guarantees are limited to Labelme -> YOLO, Labelme -> COCO, YOLO -> COCO, and COCO -> YOLO.

## Quality checks in V1

The audit path includes checks for:

- missing images
- missing annotation files where relevant
- unreadable / corrupt images
- empty annotations
- invalid category ids
- unsupported Labelme shape types
- invalid bbox sizes
- bbox out-of-bounds
- duplicate file names
- class distribution anomalies
- basic dataset size and annotation distribution summaries

## FAQ

### Is this a fork of Datumaro, PyLabel, Labelme, JSON2YOLO, or Ultralytics?

No. VisionLabelOps is a clean-room implementation with its own codebase and package layout.

### Does this project support segmentation or keypoints?

Not as a V1 project goal. Polygon geometry may be preserved when available, but the toolkit is detection-first.

### Why is Labelme support limited to `rectangle` and `polygon`?

That keeps V1 stable, testable, and aligned with the most common detection workflows.

### Is Windows supported?

Yes. The CLI, docs, and CI include Windows-friendly paths and command verification.

## Development

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -e .[dev]
python -m ruff check src tests
python -m mypy src
python -m pytest
python -m build --no-isolation
```

Additional project notes:

- [docs/architecture.md](docs/architecture.md)
- [docs/quickstart.md](docs/quickstart.md)
- [docs/reference_notes.md](docs/reference_notes.md)
- [docs/release_checklist.md](docs/release_checklist.md)

## Roadmap

- harden audit coverage for malformed datasets
- improve report richness and issue grouping
- add more examples and smoke datasets
- expand support only if it preserves the toolkit's narrow scope

## License and reference boundaries

VisionLabelOps is released under the MIT License.

Reference projects were used for architecture, workflow, file format, and behavior research only:

- Datumaro: modular dataset operations and CLI shape
- PyLabel: low-friction conversion and utility workflow
- Supervision: preview / visualization ideas
- Labelme: JSON and shape semantics
- JSON2YOLO / Ultralytics: YOLO conversion behavior expectations

The project does not copy GPL / AGPL source code, mapping tables, or internal implementations from those repositories.
