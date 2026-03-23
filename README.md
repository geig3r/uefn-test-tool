# uefn-test-tool

A minimal **UEFN-ready** Python package example.

## Why it was still not registering

The key issue is simple:

- Unreal auto-runs `Content/Python/init_unreal.py` on startup.
- That loader only scans **subfolders inside `Content/Python/`**.
- It only registers packages whose `__init__.py` exposes a callable `register()`.

So if your code only exists in `src/`, is only installed with `pip`, or does not expose `register()` from a package under `Content/Python/`, the loader will correctly print:

```text
[LOADER] No packages with register() found in Content/Python/.
```

That means the loader ran, but there was **nothing Unreal could register**.

## The runtime layout Unreal expects

```text
<YourProject>/Content/Python/
  init_unreal.py
  uefn_test_tool/
    __init__.py
    menu.py
```

## What each file does

### `Content/Python/init_unreal.py`

This is the generic startup loader. Unreal executes it automatically. It:

1. adds `Content/Python/` to `sys.path`,
2. scans each package directory,
3. imports the package,
4. calls `register()` if the package exposes it.

The loader in this repo now matches the generic pattern you pasted from your working setup / the Toolbelt example.

### `Content/Python/uefn_test_tool/__init__.py`

This is the actual package Unreal can discover. It exports:

- `register()` — the required startup hook,
- `describe_environment()` — a small helper the menu can call.

### `Content/Python/uefn_test_tool/menu.py`

This defers menu creation until the first Slate tick, then adds a small `UEFN Test Tool` submenu under `LevelEditor.MainMenu`.

## The important clarification about `src/uefn_tooling`

The external package under `src/uefn_tooling` is still useful for **outside-the-editor** automation, but it is **not part of Unreal's auto-registration path**.

That means:

- `src/uefn_tooling` will not auto-load in UEFN,
- `pyproject.toml` will not make UEFN discover your tool,
- only files under your actual project's `Content/Python/` folder participate in this startup loader flow.

## What to copy into your actual UEFN project

Copy these files into the real project you open in UEFN:

```text
<YourProject>/Content/Python/init_unreal.py
<YourProject>/Content/Python/uefn_test_tool/__init__.py
<YourProject>/Content/Python/uefn_test_tool/menu.py
```

Then restart the editor.

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
