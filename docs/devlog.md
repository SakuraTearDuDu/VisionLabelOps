# Devlog

## Workspace rule

All writes for this repository must stay within `D:\github_test_VisionLabelOps`.

## Current baseline

- Repository docs and metadata are being drafted from scratch.
- Initial implementation and test scaffolding now exist under `src/`, `tests/`, and `.github/`.

## 2026-04-20

- Changed: `src/visionlabelops/*`, `tests/*`, `pyproject.toml`, `.github/workflows/ci.yml`, `README.md`, `docs/*`
- Why: create the V1 package, CLI, format adapters, services, tests, packaging, and open-source docs
- Result: repository is installable, testable, and ready for local validation entirely inside `D:\github_test_VisionLabelOps`

## 2026-04-20 release-candidate hardening

- Changed: `src/visionlabelops/*`, `tests/*`, `pyproject.toml`, `.gitignore`, `MANIFEST.in`, `README.md`, `CHANGELOG.md`, `docs/*`, `.github/workflows/ci.yml`
- Why: fix release-candidate blockers around overwrite safety, dry-run semantics, split validation, packaging completeness, and publish-facing docs/CI consistency
- Result: release behavior, packaging artifacts, and public docs are aligned for first-public-release preparation

## Notes for future entries

- Record only work done inside this workspace.
- Include the date, the affected files, and the reason for the change.
- Call out any assumptions about dataset formats, CLI behavior, or Windows path handling.

## Template

```text
YYYY-MM-DD
- Changed: file paths
- Why: short reason
- Result: short outcome
```
