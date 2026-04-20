# Quickstart

These examples assume Windows PowerShell and a local checkout at `D:\github_test_VisionLabelOps`.

## 1. Create the local environment

```powershell
cd D:\github_test_VisionLabelOps
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .[dev]
```

## 2. Validate the installation

```powershell
vlo --help
python -m pytest
```

## 3. Run a minimal audit + stats pass

```powershell
vlo audit `
  --input D:\data\labelme `
  --format labelme `
  --output D:\work\audit `
  --overwrite

vlo stats `
  --input D:\data\labelme `
  --format labelme `
  --output D:\work\stats `
  --overwrite
```

Each non-dry-run command writes a `result.json` into the output directory and prints a short terminal summary.

## 4. Convert formats

```powershell
vlo convert `
  --input D:\data\labelme `
  --input-format labelme `
  --output D:\work\converted-yolo `
  --output-format yolo `
  --overwrite
```

## 5. Split a dataset

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

## 6. Preview and report

```powershell
vlo preview `
  --input D:\data\labelme `
  --format labelme `
  --output D:\work\preview `
  --samples 8 `
  --seed 7 `
  --overwrite

vlo report `
  --input D:\data\labelme `
  --format labelme `
  --output D:\work\report `
  --overwrite
```

## 7. Minimal Python API example

```python
from visionlabelops import audit_dataset, compute_stats, read_dataset

dataset = read_dataset(r"D:\data\labelme", "labelme")
stats = compute_stats(dataset)
audit = audit_dataset(dataset)

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
