# VisionLabelOps 0.1.0 Release Notes

## Highlights

- First public release of VisionLabelOps.
- Unified Python API and `vlo` CLI for dataset audit, conversion, statistics, splitting, reporting, and preview.
- Detection-first support for YOLO, COCO, and Labelme workflows.
- CI, tests, packaging, and Windows-friendly documentation included from the first release.

## Stable V1 scope

- `audit`
- `convert`
- `stats`
- `split`
- `report`
- `preview`

## Supported conversion guarantees

- Labelme -> YOLO
- Labelme -> COCO
- YOLO -> COCO
- COCO -> YOLO

## Important limitations

- Detection-first only.
- Labelme supports `rectangle` and `polygon` only.
- COCO import skips `iscrowd=1`.
- Unsupported Labelme shapes are reported during audit and rejected during conversion/materialization.
