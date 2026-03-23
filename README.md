# uefn-test-tool

A minimal **UEFN-ready** Python package example designed to be **checked out directly into a project's `Content/Python/` directory**.

## Exact repo structure

This repository currently contains these top-level files and folders:

```text
<YourProject>/Content/Python/
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
    test_loader.py
    test_tooling.py
  uefn_test_tool/
    __init__.py
    menu.py
```

So to be explicit: **`uefn_test_tool/` contains both `__init__.py` and `menu.py`.**

## Runtime-relevant files

Unreal only cares about these files for startup registration:

```text
<YourProject>/Content/Python/
  init_unreal.py
  uefn_test_tool/
    __init__.py
    menu.py
```

The other files (`README.md`, `src/`, `tests/`, `pyproject.toml`) are there for development/documentation and do not participate in editor auto-loading.

## Why the repo layout changed

The previous layout nested the runtime under `Content/Python/` *inside the repo*. That is awkward if you want to:

- clone the repo directly into `<YourProject>/Content/Python/`,
- run `git pull` from inside that Python directory,
- keep the Python tool as its own checkout inside the project.

With the new layout, the **repo root is the Python directory**.

## Why it still would not register before

Unreal's startup behavior is:

1. execute `init_unreal.py` inside `Content/Python/`,
2. scan subfolders inside that same directory,
3. import package folders that contain `__init__.py`,
4. call `register()` if the package exposes it.

So the repo must line up with the **actual on-disk `Content/Python` layout**.

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

## Checkout / pull workflow

If your real project is at:

```text
D:/Projects/MyIsland/
```

then the intended workflow is:

```bash
cd D:/Projects/MyIsland/Content/Python
git clone <this-repo> .
# later
cd D:/Projects/MyIsland/Content/Python
git pull
```

## Expected log output

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
