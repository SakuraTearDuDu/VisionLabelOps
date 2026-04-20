# Quickstart

This guide uses the repository's built-in example dataset at `examples/data/labelme-mini` so you can validate the CLI and API without preparing your own data first.

## 1. Create the environment

Windows PowerShell:

```powershell
cd D:\github_test_VisionLabelOps
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .[dev]
```

Linux/macOS bash or zsh:

```bash
cd /path/to/VisionLabelOps
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .[dev]
```

## 2. Validate the installation

```bash
python -m visionlabelops --version
vlo --help
python examples/basic_api.py
```

## 3. Run a minimal audit + stats pass

```bash
vlo audit --input ./examples/data/labelme-mini --format labelme --output ./tmp/audit --overwrite
vlo stats --input ./examples/data/labelme-mini --format labelme --output ./tmp/stats --overwrite
```

Each non-dry-run command writes a `result.json` into the output directory and prints a short terminal summary.

## 4. Convert formats

```bash
vlo convert \
  --input ./examples/data/labelme-mini \
  --input-format labelme \
  --output ./tmp/converted-yolo \
  --output-format yolo \
  --overwrite
```

## 5. Split a dataset

```bash
vlo split \
  --input ./examples/data/labelme-mini \
  --format labelme \
  --output ./tmp/split \
  --train 0.7 \
  --val 0.2 \
  --test 0.1 \
  --seed 7 \
  --overwrite
```

## 6. Preview and report

```bash
vlo preview \
  --input ./examples/data/labelme-mini \
  --format labelme \
  --output ./tmp/preview \
  --samples 2 \
  --seed 7 \
  --overwrite

vlo report \
  --input ./examples/data/labelme-mini \
  --format labelme \
  --output ./tmp/report \
  --overwrite
```

## 7. Use script-friendly JSON output

```bash
vlo audit \
  --input ./examples/data/labelme-mini \
  --format labelme \
  --output ./tmp/audit-json \
  --overwrite \
  --stdout-json \
  --strict
```

## 8. Minimal Python API example

```python
from pathlib import Path

from visionlabelops import audit_dataset, compute_stats, read_dataset

dataset_root = Path("examples/data/labelme-mini")

dataset = read_dataset(dataset_root, "labelme")
stats = compute_stats(dataset_root, "labelme")
audit = audit_dataset(dataset_root, "labelme")

print(dataset.image_count)
print(stats.annotation_count)
print(audit.summary["issue_count"])
```

## Expected outputs

- `audit`: `result.json`
- `stats`: `result.json`
- `convert`: converted dataset + `result.json`
- `split`: split dataset materialization + `result.json`
- `preview`: annotated samples + `contact_sheet.jpg` + `result.json`
- `report`: `report.md` + `report.html` + `result.json`

`convert --dry-run` and `split --dry-run` do not create output directories or `result.json`.
