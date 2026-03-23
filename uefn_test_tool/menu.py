"""Small editor menu example for the UEFN test tool.

Important: this module only builds the menu and routes commands to other
modules. It is not the asset browser itself.
"""

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


def _add_python_entry(submenu, *, name: str, label: str, tool_tip: str, command: str) -> None:
    import unreal

    entry = unreal.ToolMenuEntry(
        name=name,
        type=unreal.MultiBlockType.MENU_ENTRY,
    )
    entry.set_label(label)
    entry.set_tool_tip(tool_tip)
    entry.set_string_command(
        unreal.ToolMenuStringCommandType.PYTHON,
        custom_type="",
        string=command,
    )
    submenu.add_menu_entry("Startup", entry)


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

    _add_python_entry(
        submenu,
        name="UEFNTestTool.LogEnvironment",
        label="Log Python Environment",
        tool_tip="Print project and Python loader paths to the Output Log.",
        command='import uefn_test_tool.actions as actions; actions.log_environment()',
    )
    _add_python_entry(
        submenu,
        name="UEFNTestTool.BrowseSelectedFolderAssets",
        label="Browse Selected Folder Assets",
        tool_tip="Use the selected Content Browser folder, or /Game if none is selected, and sync the browser to its assets.",
        command='import uefn_test_tool.asset_browser as asset_browser; asset_browser.browse_selected_folder_assets()',
    )
    _add_python_entry(
        submenu,
        name="UEFNTestTool.ReloadPackage",
        label="Reload Package",
        tool_tip="Reload the package manually from the Python console.",
        command='import uefn_test_tool.actions as actions; actions.reload_package()',
    )

    tool_menus.refresh_all_widgets()
    _MENU_REGISTERED = True
    unreal.log("[UEFN Test Tool] Menu registered under LevelEditor.MainMenu.")
