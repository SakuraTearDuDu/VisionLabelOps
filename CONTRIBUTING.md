# Contributing

Thanks for helping improve VisionLabelOps.

## What this project is for

VisionLabelOps is meant to stay focused on dataset audit, conversion, statistics, splitting, reporting, and preview workflows for YOLO, COCO, and Labelme data.

## Before you change anything

- Keep changes small and easy to review.
- Prefer Windows-friendly commands and paths.
- Preserve the clean-room stance in docs and user-facing text.
- Avoid broad refactors unless they support the dataset workflow directly.

## Working expectations

- Update or add tests when behavior changes.
- Keep CLI output predictable and script-friendly.
- Favor clear error messages over silent fallback behavior.
- Keep documentation synchronized with the supported commands and file formats.

## Local verification

```bash
python -m venv .venv
python -m pip install -e .[dev]
pre-commit install
just verify
```

If you prefer not to use `just`, run the underlying commands directly:

```bash
python -m ruff check src tests
python -m mypy src
python -m pytest
python -m build --no-isolation
python -m twine check dist/*
```

## Documentation changes

If you are editing documentation only, keep examples concrete and aligned with the actual package names, file paths, and CLI entrypoints used by the repository.

## Pull request checklist

- The change has a clear purpose.
- The docs or code match the intended dataset workflow.
- Any new behavior is covered by tests or a verification note.
- The result remains portable on Windows.
