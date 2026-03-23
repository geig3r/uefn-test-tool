# uefn-test-tool

A minimal **UEFN-ready** Python package example designed to be **checked out directly into a project's `Content/Python/` directory**.

## Why the repo layout changed

The previous layout nested the runtime under `Content/Python/` *inside the repo*. That is awkward if you want to:

- clone the repo directly into `<YourProject>/Content/Python/`,
- run `git pull` from inside that Python directory,
- keep the Python tool as its own checkout inside the project.

With the new layout, the **repo root is the Python directory**.

That means if you clone this repo into:

```text
<YourProject>/Content/Python/
```

you will immediately get the correct runtime structure Unreal expects.

## Runtime layout after checkout

```text
<YourProject>/Content/Python/
  init_unreal.py
  uefn_test_tool/
    __init__.py
    menu.py
```

## Why it still would not register before

Unreal's startup behavior is:

1. execute `init_unreal.py` inside `Content/Python/`,
2. scan subfolders inside that same directory,
3. import package folders that contain `__init__.py`,
4. call `register()` if the package exposes it.

So the repo must line up with the **actual on-disk `Content/Python` layout**. If the repo adds another nested `Content/Python/` layer, the checkout is in the wrong place for direct use.

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

That is the workflow this flattened structure is designed for.

## Important clarification about `src/uefn_tooling`

The external package under `src/uefn_tooling` is still useful for **outside-the-editor** automation, but it is **not part of Unreal's auto-registration path**.

Only these runtime files matter for editor auto-loading:

- `init_unreal.py`
- `uefn_test_tool/__init__.py`
- `uefn_test_tool/menu.py`

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
