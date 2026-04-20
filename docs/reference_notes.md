# Reference Notes

VisionLabelOps is a clean-room project. The repositories below were studied for workflow shape, file-format behavior, and product positioning only.

## Primary reference

### Datumaro

- Borrowed ideas:
  - normalize source datasets into one internal representation
  - keep CLI verbs task-oriented
  - separate format IO from dataset operations
- Explicitly not copied:
  - large plugin ecosystem
  - broad format matrix
  - platform-scale architecture
- License note:
  - repository metadata indicates MIT, but VisionLabelOps still avoids source copying

## Secondary references

### PyLabel

- Borrowed ideas:
  - approachable dataset utility workflow
  - conversion / analysis / split ergonomics
- Explicitly not copied:
  - dataframe-centric internals
  - notebook-heavy usage style
- License note:
  - repository metadata indicates MIT; ideas were used, not implementation

### Supervision

- Borrowed ideas:
  - lightweight preview / annotator composition
  - simple dataset utility boundaries
- Explicitly not copied:
  - video, tracking, model connector, and cloud-oriented scope
- License note:
  - MIT, but still treated as behavior / design reference only

## Spec reference

### Labelme

- Used for:
  - JSON field expectations
  - `rectangle` and `polygon` semantics
  - one-image / one-JSON layout expectations
- Explicitly not copied:
  - Qt GUI code
  - app structure
  - internal implementation files
- License risk:
  - GPL-3.0, so VisionLabelOps only uses publicly documented file-format behavior

## Behavior reference

### JSON2YOLO / Ultralytics

- Used for:
  - YOLO detection text conventions
  - COCO -> YOLO bbox normalization expectations
  - class-indexing behavior context
- Explicitly not copied:
  - AGPL conversion code
  - helper functions
  - hardcoded mappings taken verbatim from source
- License risk:
  - AGPL-3.0, so VisionLabelOps only follows behavior-level expectations and reimplements logic independently

## License risk and mitigation strategy

- GPL / AGPL repositories were treated as format / behavior references only.
- VisionLabelOps does not copy source files, large code blocks, mapping tables, or internal helpers from those projects.
- The project keeps its own package layout, service boundaries, naming, and documentation structure.

## VisionLabelOps differentiation

- lighter than Datumaro
- more engineering-oriented than PyLabel
- more unified than ad-hoc script bundles
- more installable and testable than a mixed notebook workflow
- focused on audit / convert / stats / split / report / preview instead of labeling GUIs or training stacks
