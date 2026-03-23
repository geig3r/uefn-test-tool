# uefn-test-tool

A minimal **UEFN-ready** Python package example.

## Where to find it in UEFN

Based on the menu screenshot you shared, the right place for this tool is **directly inside the existing Python section of the Tools menu**, not inside a nested submenu.

So after restart, look here:

```text
Tools > Python
```

You should see these three direct menu items:

1. `UEFN Test Tool: Log Python Environment`
2. `UEFN Test Tool: Browse Selected Folder Assets`
3. `UEFN Test Tool: Reload Package`

If the runtime loads correctly, the log should now say:

```text
[LOADER] ✓ 1 package(s) registered: uefn_test_tool
[UEFN Test Tool] Menu entries registered under Tools > Python.
```

## How to use it

### Browse assets

1. Open the **Content Browser**.
2. Click a folder, for example `/Game` or one of your project folders.
3. Open **Tools > Python > UEFN Test Tool: Browse Selected Folder Assets**.
4. The tool will sync the Content Browser to that folder and up to 50 assets from it.
5. If no folder is selected, it falls back to `/Game`.

### Log environment

Use **Tools > Python > UEFN Test Tool: Log Python Environment** to print the detected project and Python paths to the Output Log.

### Reload the package

Use **Tools > Python > UEFN Test Tool: Reload Package** after editing the Python files so you do not have to restart the editor every time.

## What the runtime package contains

```text
<YourProject>/Content/Python/
  init_unreal.py
  uefn_test_tool/
    __init__.py
    actions.py
    asset_browser.py
    menu.py
```

## What the asset browser does right now

The current `asset_browser.py` is intentionally simple, but it is working code, not a placeholder.

When you click **UEFN Test Tool: Browse Selected Folder Assets**, it:

1. reads the currently selected Content Browser folder,
2. falls back to `/Game` if nothing is selected,
3. gathers asset paths from that folder,
4. syncs the Content Browser to the folder,
5. syncs the Content Browser to up to 50 assets from that folder,
6. logs what it found.

So this is a lightweight Content Browser integration, not a full custom asset-browser window.

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

## Reference reviewed

- Example repo: <https://github.com/undergroundrap/UEFN-TOOLBELT>
- Epic docs for Editor Asset / Editor Utility APIs used to make the browser action work:
  - <https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/EditorAssetLibrary?application_version=4.27>
  - <https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/EditorUtilityLibrary?application_version=5.4>
