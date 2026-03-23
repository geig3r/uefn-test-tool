"""Small editor menu example for the UEFN test tool."""

_CALLBACK_HANDLE = None
_MENU_REGISTERED = False


def schedule_menu_registration() -> None:
    """Defer menu registration until Slate is available."""
    global _CALLBACK_HANDLE

    import unreal

    if _CALLBACK_HANDLE is not None:
        unreal.log("[UEFN Test Tool] Menu registration already scheduled.")
        return

    def _on_tick(_delta_time: float) -> None:
        global _CALLBACK_HANDLE
        try:
            build_menu()
        except Exception as _e:
            unreal.log_warning(f"[UEFN Test Tool] Menu registration failed: {_e}")
        finally:
            if _CALLBACK_HANDLE is not None:
                unreal.unregister_slate_pre_tick_callback(_CALLBACK_HANDLE)
                _CALLBACK_HANDLE = None

    _CALLBACK_HANDLE = unreal.register_slate_pre_tick_callback(_on_tick)
    unreal.log("[UEFN Test Tool] Menu registration scheduled.")


def build_menu() -> None:
    """Add a minimal submenu under the Level Editor main menu."""
    global _MENU_REGISTERED

    import unreal

    if _MENU_REGISTERED:
        unreal.log("[UEFN Test Tool] Menu already registered.")
        return

    tool_menus = unreal.ToolMenus.get()
    main_menu = tool_menus.extend_menu("LevelEditor.MainMenu")
    submenu = main_menu.add_sub_menu(
        owner="LevelEditor.MainMenu",
        section_name="UEFNTools",
        name="LevelEditor.MainMenu.UEFNTestTool",
        label="UEFN Test Tool",
        tool_tip="Starter Python hooks for UEFN / Unreal Editor projects.",
    )

    env_entry = unreal.ToolMenuEntry(
        name="UEFNTestTool.LogEnvironment",
        type=unreal.MultiBlockType.MENU_ENTRY,
    )
    env_entry.set_label("Log Python Environment")
    env_entry.set_tool_tip("Print project and Python loader paths to the Output Log.")
    env_entry.set_string_command(
        unreal.ToolMenuStringCommandType.PYTHON,
        custom_type="",
        string='import uefn_test_tool; import unreal; unreal.log(str(uefn_test_tool.describe_environment()))',
    )
    submenu.add_menu_entry("Startup", env_entry)

    reload_entry = unreal.ToolMenuEntry(
        name="UEFNTestTool.ReloadPackage",
        type=unreal.MultiBlockType.MENU_ENTRY,
    )
    reload_entry.set_label("Reload Package")
    reload_entry.set_tool_tip("Reload the package manually from the Python console.")
    reload_entry.set_string_command(
        unreal.ToolMenuStringCommandType.PYTHON,
        custom_type="",
        string='import importlib, uefn_test_tool; importlib.reload(uefn_test_tool); uefn_test_tool.register()',
    )
    submenu.add_menu_entry("Startup", reload_entry)

    tool_menus.refresh_all_widgets()
    _MENU_REGISTERED = True
    unreal.log("[UEFN Test Tool] Menu registered under LevelEditor.MainMenu.")
