# Architecture

VisionLabelOps is organized as a small toolkit around a shared dataset model.

## Core shape

- `visionlabelops.types` defines the domain objects: datasets, images, annotations, categories, bounding boxes, polygons, and result payloads.
- `visionlabelops.io` handles reading and writing supported annotation formats.
- `visionlabelops.convert` transforms datasets between YOLO, COCO, and Labelme layouts.
- `visionlabelops.audit` inspects datasets for missing assets, unreadable images, and annotation issues.
- `visionlabelops.stats` computes counts and distributions.
- `visionlabelops.split` creates reproducible subsets.
- `visionlabelops.preview` renders contact sheets or sample previews.
- `visionlabelops.report` writes human-readable and machine-readable summaries.
- `visionlabelops.cli` exposes the user-facing command line entrypoint.

## Internal model

The package uses one shared detection-first model:

- `Dataset`
- `ImageRecord`
- `Annotation`
- `Category`
- `BBox`
- optional `Polygon`

Format adapters convert source structures into that model early. Downstream services do not re-parse raw source files.

## Data flow

1. A caller points the toolkit at an input path and declares the source format.
2. The reader normalizes the dataset into in-memory domain objects.
3. Downstream services operate on that shared model instead of format-specific structures.
4. Exporters write the result into a requested output directory or file.
5. The CLI wraps each service with a stable command, arguments, and exit code.

## Output conventions

- write commands require an explicit output directory
- non-dry-run write commands emit a `result.json`
- `convert` preserves the requested output format
- `split` materializes the source format into reproducible subsets
- `report` emits both Markdown and HTML
- `preview` emits per-sample overlays and a contact sheet

## Design goals

- Keep the data model small enough to understand without reading every parser.
- Avoid duplicating business rules across format adapters.
- Make errors explicit and actionable.
- Keep behavior deterministic when a seed is supplied.
- Favor Windows-compatible filesystem handling and subprocess behavior.
- Keep dependencies light enough for ordinary GitHub users to install.

## Clean-room references

The project references the general problem space covered by Datumaro, PyLabel, Supervision, Labelme, JSON2YOLO, and Ultralytics. The design here should stay independent and implementation-specific to VisionLabelOps.

## Notes for contributors

- Parser code should convert external file structures into the internal model as early as possible.
- Report and preview code should consume the shared model, not the raw source format.
- CLI commands should stay thin and delegate work to service functions.
