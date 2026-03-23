# UEFN Test Tool

Editor utilities to speed up UEFN development workflows.

> **Requires UEFN 40.00 or later** — Python scripting was added as an experimental feature in the March 19, 2026 release.

## Installation

### 1. Enable Python in UEFN

Open your project, then:

- **Edit → Editor Preferences → Experimental** → enable **Python Editor Script Plugin** → restart UEFN

### 2. Copy the Python files into your project

Copy the contents of `Content/Python/` from this repo into your project's `Content/Python/` folder:

```
YourProject/
└── Content/
    └── Python/
        ├── init_unreal.py          ← auto-runs at editor startup
        └── uefn_test_tool/
            ├── __init__.py
            ├── texture_picker.py
            └── asset_browser.py
```

### 3. Restart UEFN

Check the **Output Log** (Window → Output Log) for:
```
[UEFN Test Tool] Menus registered.
```

If you see that, everything is working.

## Tools

### Copy Asset Name

Replaces the manual workflow of:
> Reference Viewer → Show Asset Path → copy last element

**Usage:** Right-click any asset in the Content Browser → **UEFN Test Tools → Copy Asset Name**

The short asset name (e.g. `T_WeapRifle`) is copied to your clipboard.

---

### Asset Browser

Browse built-in Fortnite assets by category with a searchable list.

**Usage:** Tools → UEFN Test Tools → Open Asset Browser

- Select a category (Weapons, Items, Characters, etc.)
- Filter by name
- Click to select, double-click to copy asset name
- **Export to CSV** — saves the full category list for use in spreadsheets

> **Note:** The category paths (e.g. `/Fortnite/Weapons`) may need to be adjusted to match your project's actual asset structure. Edit `CATEGORIES` in `asset_browser.py` if assets aren't showing up.

> **UI framework:** The Asset Browser uses Tkinter (Python standard library), the same approach used by [uefn-device-graph](https://github.com/ImmatureGamer/uefn-device-graph). No extra dependencies required.
