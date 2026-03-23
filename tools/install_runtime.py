from __future__ import annotations

import argparse
from pathlib import Path
import shutil

RUNTIME_FILES = ["init_unreal.py"]
RUNTIME_DIRS = ["uefn_test_tool"]
REPO_ROOT = Path(__file__).resolve().parents[1]


def install_runtime(project_dir: str | Path, *, clean: bool = True) -> Path:
    project_root = Path(project_dir).expanduser().resolve()
    python_dir = project_root / "Content" / "Python"
    python_dir.mkdir(parents=True, exist_ok=True)

    for filename in RUNTIME_FILES:
        shutil.copy2(REPO_ROOT / filename, python_dir / filename)

    for dirname in RUNTIME_DIRS:
        source_dir = REPO_ROOT / dirname
        target_dir = python_dir / dirname
        if clean and target_dir.exists():
            shutil.rmtree(target_dir)
        shutil.copytree(source_dir, target_dir, dirs_exist_ok=not clean)

    return python_dir


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Install the runtime Python files into a UEFN project's Content/Python directory.",
    )
    parser.add_argument(
        "--project-dir",
        required=True,
        help="Path to the UEFN project root (the folder that contains Content/).",
    )
    parser.add_argument(
        "--no-clean",
        action="store_true",
        help="Do not remove an existing target package directory before copying.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    python_dir = install_runtime(args.project_dir, clean=not args.no_clean)
    print(f"Installed runtime files to: {python_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
