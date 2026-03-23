def register() -> None:
    """Called automatically by init_unreal.py on editor startup."""
    _schedule_menus()


def _schedule_menus() -> None:
    """Defer menu building to the first Slate tick.

    init_unreal.py runs before the menu bar exists — ToolMenus.get()
    must not be called until Slate is fully constructed.
    """
    import unreal

    _done = False

    def _on_tick(dt: float) -> None:
        nonlocal _done
        if _done:
            return
        _done = True
        try:
            from . import texture_picker, asset_browser
            texture_picker.register_menu_entries()
            asset_browser.register_menu_entries()
        except Exception as e:
            unreal.log_warning(f"[UEFN Test Tool] Menu registration failed: {e}")
        finally:
            unreal.unregister_slate_pre_tick_callback(_handle)

    _handle = unreal.register_slate_pre_tick_callback(_on_tick)
