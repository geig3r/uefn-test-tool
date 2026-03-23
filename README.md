# uefn-test-tool

A minimal **UEFN-ready** Python package example.

## Short answer to your question

**No** — `menu.py` is **not** the asset browser.

But unlike the previous version, `asset_browser.py` now has **real working behavior**.

In this repo now:

- `menu.py` = menu registration / menu entries
- `actions.py` = simple callable actions used by the menu
- `asset_browser.py` = real asset-browsing helpers that use Unreal's Content Browser APIs

## What the asset browser does right now

The current `asset_browser.py` is intentionally simple, but it is no longer a placeholder.

When you click **Browse Selected Folder Assets** from the `UEFN Test Tool` menu, it:

1. reads the currently selected Content Browser folder,
2. falls back to `/Game` if nothing is selected,
3. gathers asset paths from that folder,
4. syncs the Content Browser to the folder,
5. syncs the Content Browser to up to 50 assets from that folder,
6. logs what it found.

So yes: there is now actual working asset-browsing functionality, but it is a **lightweight Content Browser integration**, not a full custom browser window yet.

## Runtime package layout

```text
<YourProject>/Content/Python/
  init_unreal.py
  uefn_test_tool/
    __init__.py
    actions.py
    asset_browser.py
    menu.py
```

## What each file does

- `init_unreal.py` — Unreal startup loader
- `uefn_test_tool/__init__.py` — package entry point with `register()`
- `uefn_test_tool/menu.py` — builds the menu only
- `uefn_test_tool/actions.py` — handles environment logging and reload
- `uefn_test_tool/asset_browser.py` — reads selected folders and syncs the Content Browser to actual assets

## Menu items you get

After installation, the tool currently gives you:

1. `Log Python Environment`
2. `Browse Selected Folder Assets`
3. `Reload Package`

## Install it into a project

### Option 1: Copy the runtime files into your project automatically

```bash
python tools/install_runtime.py --project-dir D:/Projects/MyIsland
```

### Option 2: Clone this repo directly into `Content/Python`

```bash
cd D:/Projects/MyIsland/Content/Python
git clone <this-repo> .
```

## Verify the install

```bash
python tools/verify_runtime.py --project-dir D:/Projects/MyIsland
```

## Exact repo structure

```text
<repo root>/
  .gitignore
  README.md
  init_unreal.py
  pyproject.toml
  src/
    uefn_tooling/
      __init__.py
      cli.py
      config.py
      uefn.py
  tests/
    test_asset_browser.py
    test_install_runtime.py
    test_loader.py
    test_tooling.py
    test_verify_runtime.py
  tools/
    install_runtime.py
    verify_runtime.py
  uefn_test_tool/
    __init__.py
    actions.py
    asset_browser.py
    menu.py
```

## What should happen after install

When UEFN starts, it should run `init_unreal.py`, import `uefn_test_tool`, call `register()`, and log something like this:

```text
[UEFN Test Tool] Registering package v0.3.0.
[UEFN Test Tool] Environment: {...}
[UEFN Test Tool] Menu registration scheduled.
[LOADER] ✓ 1 package(s) registered: uefn_test_tool
```

And once the menu is built:

```text
[UEFN Test Tool] Menu registered under LevelEditor.MainMenu.
```

## Reference reviewed

- Example repo: <https://github.com/undergroundrap/UEFN-TOOLBELT>
- Epic docs for Asset Registry / Editor Asset APIs used to make the browser action work:
  - <https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/AssetRegistry>
  - <https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/EditorAssetLibrary?application_version=4.27>
  - <https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/EditorUtilityLibrary?application_version=5.4>
