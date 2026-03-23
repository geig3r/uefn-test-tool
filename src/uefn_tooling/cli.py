from __future__ import annotations

import argparse
import json
import sys

from .config import ToolConfig
from .uefn import UEFNTool


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="uefn-tool",
        description="External Python tooling scaffold for UEFN/Unreal Engine workflows.",
    )
    parser.add_argument(
        "--project-dir",
        default=".",
        help="Path to the root of the UEFN project. Defaults to the current directory.",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("detect", help="Print detected UEFN/URC/editor paths.")
    subparsers.add_parser("project-info", help="Summarize project files that Python can automate around.")

    urc_parser = subparsers.add_parser("urc", help="Pass through to urc2.exe.")
    urc_parser.add_argument("urc_args", nargs=argparse.REMAINDER, help="Arguments forwarded to urc2.exe.")

    launch_parser = subparsers.add_parser("launch", help="Print the editor command you would run.")
    launch_parser.add_argument("editor_args", nargs=argparse.REMAINDER, help="Additional editor arguments.")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    tool = UEFNTool(ToolConfig.from_env(args.project_dir))

    if args.command == "detect":
        print(json.dumps(tool.detect(), indent=2))
        return 0

    if args.command == "project-info":
        print(json.dumps(tool.project_summary(), indent=2))
        return 0

    if args.command == "urc":
        forwarded = list(args.urc_args)
        if forwarded and forwarded[0] == "--":
            forwarded = forwarded[1:]
        result = tool.run_urc(*forwarded, check=False)
        if result.stdout:
            print(result.stdout, end="")
        if result.stderr:
            print(result.stderr, file=sys.stderr, end="")
        return result.returncode

    if args.command == "launch":
        print(" ".join(tool.build_editor_launch_command(args.editor_args)))
        return 0

    parser.error(f"Unsupported command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
