# 快速开始

[English](quickstart.md) | **简体中文**

本指南使用仓库内置的演示数据集 `examples/data/labelme-mini`，方便你在不准备自有数据的情况下，先验证 VisionLabelOps 的 CLI 和 API 链路。

## 1. 创建环境

Windows PowerShell：

```powershell
cd D:\github_test_VisionLabelOps
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .[dev]
```

Linux/macOS bash 或 zsh：

```bash
cd /path/to/VisionLabelOps
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .[dev]
```

## 2. 验证安装

```bash
python -m visionlabelops --version
vlo --help
python examples/basic_api.py
```

## 3. 跑通最小工作流

```bash
vlo stats --input ./examples/data/labelme-mini --format labelme --output ./tmp/stats --overwrite
vlo audit --input ./examples/data/labelme-mini --format labelme --output ./tmp/audit --overwrite
vlo preview --input ./examples/data/labelme-mini --format labelme --output ./tmp/preview --samples 2 --seed 7 --overwrite
```

## 4. 生成报告

```bash
vlo report --input ./examples/data/labelme-mini --format labelme --output ./tmp/report --overwrite
```

## 5. 使用适合自动化的 JSON 输出

```bash
vlo audit \
  --input ./examples/data/labelme-mini \
  --format labelme \
  --output ./tmp/audit-json \
  --overwrite \
  --stdout-json \
  --strict
```

## 6. 试一遍转换与划分

```bash
vlo convert \
  --input ./examples/data/labelme-mini \
  --input-format labelme \
  --output ./tmp/converted-yolo \
  --output-format yolo \
  --overwrite

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

## 7. 最小 Python API 示例

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

## 输出约定

- `audit`：`result.json`
- `stats`：`result.json`
- `convert`：转换后的数据集 + `result.json`
- `split`：划分后的数据集 + `result.json`
- `preview`：标注预览图 + `contact_sheet.jpg` + `result.json`
- `report`：`report.md` + `report.html` + `result.json`

`convert --dry-run` 和 `split --dry-run` 不会创建输出目录，也不会写入 `result.json`。

## 范围提醒

- VisionLabelOps 当前是 detection-first 工具包，不是 segmentation、keypoint、tracking、GUI、Web 或训练框架项目。
- Labelme 当前只支持 `rectangle` 和 `polygon`。
- COCO 导入会跳过 `iscrowd=1`。
