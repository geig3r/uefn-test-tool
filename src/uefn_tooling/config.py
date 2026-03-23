from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os
import platform


DEFAULT_WINDOWS_UEFN_DIR = Path(r"C:/Program Files/Epic Games/Fortnite")
DEFAULT_WINDOWS_URC = DEFAULT_WINDOWS_UEFN_DIR / "FortniteGame/Binaries/Win64/urc2.exe"
DEFAULT_WINDOWS_EDITOR = DEFAULT_WINDOWS_UEFN_DIR / "FortniteGame/Binaries/Win64/UnrealEditorFortnite-Win64-Shipping.exe"


@dataclass(slots=True)
class ToolConfig:
    """Runtime configuration for the external tooling wrapper."""

    project_dir: Path
    uefn_install_dir: Path | None = None
    urc_exe: Path | None = None
    editor_exe: Path | None = None

    @classmethod
    def from_env(cls, project_dir: str | os.PathLike[str]) -> "ToolConfig":
        project_path = Path(project_dir).expanduser().resolve()
        install_dir = _optional_path(os.getenv("UEFN_INSTALL_DIR"))
        urc_exe = _optional_path(os.getenv("UEFN_URC_EXE"))
        editor_exe = _optional_path(os.getenv("UEFN_EDITOR_EXE"))

        if platform.system() == "Windows":
            install_dir = install_dir or DEFAULT_WINDOWS_UEFN_DIR
            urc_exe = urc_exe or DEFAULT_WINDOWS_URC
            editor_exe = editor_exe or DEFAULT_WINDOWS_EDITOR

        return cls(
            project_dir=project_path,
            uefn_install_dir=install_dir,
            urc_exe=urc_exe,
            editor_exe=editor_exe,
        )

    def summary(self) -> dict[str, str | bool | None]:
        return {
            "project_dir": str(self.project_dir),
            "project_exists": self.project_dir.exists(),
            "uefn_install_dir": _path_text(self.uefn_install_dir),
            "uefn_install_exists": _path_exists(self.uefn_install_dir),
            "urc_exe": _path_text(self.urc_exe),
            "urc_exists": _path_exists(self.urc_exe),
            "editor_exe": _path_text(self.editor_exe),
            "editor_exists": _path_exists(self.editor_exe),
        }


def _optional_path(raw: str | None) -> Path | None:
    return Path(raw).expanduser() if raw else None


def _path_text(path: Path | None) -> str | None:
    return str(path) if path else None


def _path_exists(path: Path | None) -> bool | None:
    return path.exists() if path else None
