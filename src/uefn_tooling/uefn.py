from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import subprocess
from typing import Iterable

from .config import ToolConfig


@dataclass(slots=True)
class CommandResult:
    args: list[str]
    returncode: int
    stdout: str
    stderr: str


class UEFNTool:
    """External automation helpers for UEFN projects.

    Important: UEFN gameplay/editor extensibility is *not* exposed through the
    same Python API that Unreal Engine editor scripting uses. This class wraps
    file-based workflows and the Unreal Revision Control CLI instead.
    """

    def __init__(self, config: ToolConfig):
        self.config = config

    def detect(self) -> dict[str, str | bool | None]:
        return self.config.summary()

    def find_project_file(self) -> Path | None:
        matches = sorted(self.config.project_dir.glob("*.uefnproject"))
        return matches[0] if matches else None

    def project_summary(self) -> dict[str, object]:
        project_file = self.find_project_file()
        verse_files = sorted(self.config.project_dir.rglob("*.verse"))
        plugin_files = sorted(self.config.project_dir.rglob("*.uplugin"))
        return {
            "project_file": str(project_file) if project_file else None,
            "verse_file_count": len(verse_files),
            "plugin_file_count": len(plugin_files),
            "verse_files": [str(path.relative_to(self.config.project_dir)) for path in verse_files[:25]],
            "plugin_files": [str(path.relative_to(self.config.project_dir)) for path in plugin_files[:25]],
        }

    def read_project_metadata(self) -> dict[str, object] | None:
        project_file = self.find_project_file()
        if not project_file:
            return None
        return json.loads(project_file.read_text(encoding="utf-8"))

    def run_urc(self, *args: str, check: bool = True) -> CommandResult:
        if not self.config.urc_exe:
            raise FileNotFoundError(
                "UEFN_URC_EXE is not configured. Point it at urc2.exe from your Fortnite install."
            )
        if not self.config.urc_exe.exists():
            raise FileNotFoundError(f"URC executable does not exist: {self.config.urc_exe}")

        completed = subprocess.run(
            [str(self.config.urc_exe), *args],
            cwd=self.config.project_dir,
            text=True,
            capture_output=True,
            check=False,
        )
        if check and completed.returncode != 0:
            raise RuntimeError(completed.stderr.strip() or completed.stdout.strip())
        return CommandResult(
            args=[str(self.config.urc_exe), *args],
            returncode=completed.returncode,
            stdout=completed.stdout,
            stderr=completed.stderr,
        )

    def build_urc_command(self, *args: str) -> list[str]:
        if not self.config.urc_exe:
            raise FileNotFoundError("UEFN_URC_EXE is not configured.")
        return [str(self.config.urc_exe), *args]

    def build_editor_launch_command(self, extra_args: Iterable[str] = ()) -> list[str]:
        if not self.config.editor_exe:
            raise FileNotFoundError(
                "UEFN_EDITOR_EXE is not configured. Point it at UnrealEditorFortnite-Win64-Shipping.exe."
            )
        project_file = self.find_project_file()
        if not project_file:
            raise FileNotFoundError("No .uefnproject file found in the configured project directory.")
        return [str(self.config.editor_exe), str(project_file), *extra_args]
