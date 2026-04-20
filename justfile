lint:
    python -m ruff check src tests

typecheck:
    python -m mypy src

test:
    python -m pytest

build:
    python -m build --no-isolation
    python -m twine check dist/*

verify:
    just lint
    just typecheck
    just test
    just build
