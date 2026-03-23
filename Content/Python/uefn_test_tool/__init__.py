"""Minimal UEFN package discovered by ``Content/Python/init_unreal.py``."""

_REGISTERED = False
__version__ = "0.3.0"


def describe_environment():
    import unreal

    return {
        "project_content_dir": unreal.Paths.project_content_dir(),
        "project_dir": unreal.Paths.project_dir(),
        "project_saved_dir": unreal.Paths.project_saved_dir(),
        "python_root": unreal.Paths.project_content_dir() + "Python/",
        "package_version": __version__,
    }


def register() -> None:
    """Generic loader entry point called by ``init_unreal.py`` on startup."""
    global _REGISTERED

    import unreal

    if _REGISTERED:
        unreal.log("[UEFN Test Tool] register() called again; package already initialized.")
        return

    from .menu import schedule_menu_registration

    _REGISTERED = True
    unreal.log(f"[UEFN Test Tool] Registering package v{__version__}.")
    unreal.log(f"[UEFN Test Tool] Environment: {describe_environment()}")
    schedule_menu_registration()
