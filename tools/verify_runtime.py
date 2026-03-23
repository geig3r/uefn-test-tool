from __future__ import annotations

import argparse
from pathlib import Path

EXPECTED_FILES = [
    Path('Content/Python/init_unreal.py'),
    Path('Content/Python/uefn_test_tool/__init__.py'),
    Path('Content/Python/uefn_test_tool/actions.py'),
    Path('Content/Python/uefn_test_tool/asset_browser.py'),
    Path('Content/Python/uefn_test_tool/menu.py'),
]


def verify_runtime(project_dir: str | Path) -> tuple[Path, list[Path]]:
    project_root = Path(project_dir).expanduser().resolve()
    missing = [relative for relative in EXPECTED_FILES if not (project_root / relative).exists()]
    return project_root, missing


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description='Verify that the UEFN Python runtime files exist in a project.',
    )
    parser.add_argument(
        '--project-dir',
        required=True,
        help='Path to the UEFN project root (the folder that contains Content/).',
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    project_root, missing = verify_runtime(args.project_dir)
    if missing:
        print(f'Missing runtime files under: {project_root}')
        for path in missing:
            print(f' - {path.as_posix()}')
        return 1

    print(f'Runtime files verified under: {project_root}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
