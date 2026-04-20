from __future__ import annotations

import subprocess
import sys
from importlib.metadata import version
from pathlib import Path

from visionlabelops import __version__


def test_package_version_matches_installed_metadata() -> None:
    assert __version__ == version("visionlabelops")


def test_module_version_flag_matches_package_version() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "visionlabelops", "--version"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == __version__


def test_basic_api_example_uses_repository_example_data() -> None:
    example_path = Path("examples/basic_api.py")
    source = example_path.read_text(encoding="utf-8")

    assert "tests/fixtures" not in source
    assert "labelme-mini" in source
