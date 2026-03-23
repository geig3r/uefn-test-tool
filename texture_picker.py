"""
Texture Picker
==============
Quickly grab weapon texture asset names for use in the UMG editor.

Before: Open Reference Viewer → Show Asset Path → manually copy last element
After:  Right-click asset in Content Browser → Copy Asset Name → done
"""

import subprocess
import unreal


def _get_selected_asset_name() -> str | None:
    """Return the short name of the first selected Content Browser asset.

    Unreal asset paths look like:
        /Game/Weapons/Textures/T_Rifle.T_Rifle

    This returns the last element — the part after the dot — e.g. T_Rifle.
    Calling asset.get_name() gives this directly without any string splitting.
    """
    selected = unreal.EditorUtilityLibrary.get_selected_assets()
    if not selected:
        unreal.log_warning("[UEFN Test Tool] No asset selected in Content Browser.")
        return None
    return selected[0].get_name()


def _copy_to_clipboard(text: str) -> bool:
    """Copy text to the OS clipboard. Returns True on success."""
    try:
        platform = unreal.SystemLibrary.get_platform_name()
        if platform == "Windows":
            subprocess.run(["clip"], input=text.encode("utf-8"), check=True)
        elif platform == "Mac":
            subprocess.run(["pbcopy"], input=text.encode("utf-8"), check=True)
        else:
            # Linux — try xclip then xsel
            for cmd in [
                ["xclip", "-selection", "clipboard"],
                ["xsel", "--clipboard", "--input"],
            ]:
                try:
                    subprocess.run(cmd, input=text.encode("utf-8"), check=True)
                    break
                except FileNotFoundError:
                    continue
            else:
                return False
        return True
    except Exception as e:
        unreal.log_warning(f"[UEFN Test Tool] Clipboard copy failed: {e}")
        return False


def copy_selected_asset_name():
    """Menu command: copies the selected asset's short name to clipboard."""
    name = _get_selected_asset_name()
    if name is None:
        return

    success = _copy_to_clipboard(name)
    if success:
        unreal.log(f"[UEFN Test Tool] Copied to clipboard: {name}")
    else:
        # Fallback: show in a dialog so the user can copy manually
        unreal.EditorDialog.show_message(
            title="Asset Name",
            message=name,
            message_type=unreal.AppMsgType.OK,
        )
        unreal.log(f"[UEFN Test Tool] Asset name: {name}  (clipboard unavailable)")


def register_menu_entries():
    """Register tool entries in the Content Browser right-click context menu."""
    menus = unreal.ToolMenus.get()

    menu = menus.extend_menu("ContentBrowser.AssetContextMenu")
    section = menu.add_section(
        "UEFNTestTools",
        label=unreal.Text("UEFN Test Tools"),
    )

    entry = unreal.ToolMenuEntry(
        name="UEFNTestTool_CopyAssetName",
        type=unreal.MultiBlockType.MENU_ENTRY,
        insert_position=unreal.ToolMenuInsert("", unreal.ToolMenuInsertType.DEFAULT),
    )
    entry.set_label("Copy Asset Name")
    entry.set_tool_tip(
        "Copies the short asset name to clipboard.\n"
        "Example: /Game/Weapons/T_Rifle.T_Rifle  →  T_Rifle"
    )
    entry.set_string_command(
        type=unreal.ToolMenuStringCommandType.PYTHON,
        custom_type="",
        string=(
            "from uefn_test_tool import texture_picker; "
            "texture_picker.copy_selected_asset_name()"
        ),
    )
    section.add_entry(entry)

    menus.refresh_all_widgets()
    unreal.log("[UEFN Test Tool] Menus registered.")
