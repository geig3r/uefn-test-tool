"""Simple, working asset-browser helpers for the UEFN test tool.

This is intentionally lightweight: it uses the existing Content Browser rather
than building a custom Slate window. The goal is to provide *working* asset
browsing behavior from Python with minimal moving parts.
"""

DEFAULT_FOLDER = "/Game"
MAX_SYNC_ASSETS = 50


def get_target_folder() -> str:
    import unreal

    selected_folders = list(unreal.EditorUtilityLibrary.get_selected_folder_paths())
    return selected_folders[0] if selected_folders else DEFAULT_FOLDER


def browse_selected_folder_assets() -> None:
    """Browse assets in the selected Content Browser folder.

    If no folder is selected, the function falls back to ``/Game``.
    The function then:
    1. queries assets with ``EditorAssetLibrary.list_assets()``,
    2. syncs the Content Browser to the folder,
    3. syncs the Content Browser to up to ``MAX_SYNC_ASSETS`` assets,
    4. logs what it found.
    """
    import unreal

    folder = get_target_folder()
    asset_paths = list(unreal.EditorAssetLibrary.list_assets(folder, recursive=False, include_folder=False))

    if not asset_paths:
        unreal.log_warning(f"[UEFN Test Tool] No assets found in folder: {folder}")
        unreal.EditorUtilityLibrary.sync_browser_to_folders([folder])
        return

    unreal.EditorUtilityLibrary.sync_browser_to_folders([folder])
    synced_paths = asset_paths[:MAX_SYNC_ASSETS]
    unreal.EditorAssetLibrary.sync_browser_to_objects(synced_paths)
    unreal.log(
        f"[UEFN Test Tool] Browsing {len(synced_paths)} asset(s) from {folder}: {', '.join(synced_paths[:5])}"
    )
