# Release Checklist

Before publishing a release:

- verify `python -m pytest`
- verify `python -m pytest --cov=visionlabelops --cov-report=term-missing --cov-fail-under=92`
- verify `python -m ruff check src tests`
- verify `python -m mypy src`
- verify `python -m build --no-isolation`
- verify `python -m twine check dist/*`
- verify install-from-wheel smoke for the generated `dist/*.whl`
- verify install-from-sdist smoke for the generated `dist/*.tar.gz`
- verify `vlo --help`
- verify `vlo --version`
- verify the README minimum CLI path (`stats`, `audit`, and `report`) against a real sample dataset
- verify `examples/basic_api.py`
- verify the repository example dataset under `examples/data/labelme-mini`
- verify README install and quickstart commands against the current CLI
- review `CHANGELOG.md`
- confirm reference / license notes still describe the current codebase accurately
- confirm no generated files outside `D:\github_test_VisionLabelOps` were used during local validation
