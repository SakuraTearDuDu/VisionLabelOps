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

## 2026-04-20 repository maturity hardening

- Changed: `src/visionlabelops/*`, `examples/*`, `tests/*`, `pyproject.toml`, `README.md`, `docs/*`, `.github/workflows/ci.yml`, `.pre-commit-config.yaml`, `justfile`
- Why: remove version drift risk, unify result serialization, standardize path-first public APIs, decouple examples from test fixtures, and strengthen cross-platform docs and CI
- Result: repository behavior, package metadata, examples, and automation surfaces are closer to a stable `v0.1.1` open-source release candidate
- Decision: use one source version file plus setuptools dynamic metadata instead of `setuptools-scm` to avoid a heavier release chain for a small repository
- Decision: keep public APIs path-first and reserve dataset-first usage for core service functions to reduce ambiguity between CLI and Python examples
- Decision: add a macOS smoke job so the existing macOS classifier remains honest; the cost is low and the public signal is worth it
- Deferred: broader YOLO layout flexibility remains a later candidate rather than a V1 hardening task, because this round prioritizes stable behavior over wider heuristics

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
