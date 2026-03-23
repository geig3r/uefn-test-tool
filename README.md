# uefn-test-tool

A minimal **UEFN-ready** Python package example.

## How to install this into a real UEFN project

This repo does **not** need `.uasset` files or other content assets. It is a **code-only Python tool**.

The minimum runtime that must end up inside your project is:

```text
<YourProject>/Content/Python/
  init_unreal.py
  uefn_test_tool/
    __init__.py
    menu.py
```

So to answer your question directly: **yes, you install Python files into the project**. There are no extra Unreal assets required for this starter.

### Option A — Clone this repo directly into `Content/Python`

If you want this repo itself to live inside the project and be updateable with `git pull`:

```bash
cd D:/Projects/MyIsland/Content/Python
git clone <this-repo> .
```

That gives Unreal the files it needs immediately:

- `init_unreal.py`
- `uefn_test_tool/__init__.py`
- `uefn_test_tool/menu.py`

### Option B — Copy only the runtime files into a project

If you want to keep this repo somewhere else and just install the runtime into a project, use the installer script:

```bash
python tools/install_runtime.py --project-dir D:/Projects/MyIsland
```

That command copies exactly these runtime files into `D:/Projects/MyIsland/Content/Python/`:

```text
Content/Python/init_unreal.py
Content/Python/uefn_test_tool/__init__.py
Content/Python/uefn_test_tool/menu.py
```

## Exact repo structure

This repository currently contains these top-level files and folders:

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
    test_install_runtime.py
    test_loader.py
    test_tooling.py
  tools/
    install_runtime.py
  uefn_test_tool/
    __init__.py
    menu.py
```

So to be explicit: **`uefn_test_tool/` contains both `__init__.py` and `menu.py`**. `menu.py` is not the only file.

## Which files Unreal actually uses

Unreal only cares about these runtime files for startup registration:

```text
<YourProject>/Content/Python/
  init_unreal.py
  uefn_test_tool/
    __init__.py
    menu.py
```

The other files (`README.md`, `src/`, `tests/`, `tools/`, `pyproject.toml`) are development/documentation helpers.

## What each runtime file does

### `init_unreal.py`

This is the generic startup loader. Unreal executes it automatically. It:

- treats the directory containing `init_unreal.py` as the active Python root,
- adds that directory to `sys.path`,
- scans package directories,
- imports them,
- calls `register()` if present.

### `uefn_test_tool/__init__.py`

This is the discoverable package entry point. It exports:

- `register()` for startup initialization,
- `describe_environment()` for logging project paths.

### `uefn_test_tool/menu.py`

This defers menu creation until the first Slate tick, then adds a small `UEFN Test Tool` submenu under `LevelEditor.MainMenu`.

## What should happen after install

On a successful startup, you should see something like:

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
- Example generic loader: <https://raw.githubusercontent.com/undergroundrap/UEFN-TOOLBELT/main/init_unreal.py>
