# UEFN Test Tool

A UEFN/Unreal Editor Python plugin for speeding up common development workflows.

## Installation

1. Copy this folder into your UEFN project's `Plugins/` directory:
   ```
   YourProject/Plugins/uefn_test_tool/
   ```
2. Open your project in UEFN — the plugin will activate automatically.
3. Make sure **Python Script Plugin** and **Editor Scripting Utilities** are enabled under Edit → Plugins.

## Tools

### Copy Asset Name (Texture Picker)

Replaces the manual workflow of:
> Reference Viewer → Show Asset Path → copy last element

**Usage:** Right-click any asset in the Content Browser → **UEFN Test Tools → Copy Asset Name**

The short asset name (e.g. `T_WeapRifle`) is copied to your clipboard, ready to paste into the UMG editor.

## Project Structure

```
uefn_test_tool/
├── Content/
│   └── Python/
│       ├── init_unreal.py              # Auto-runs at editor startup
│       └── uefn_test_tool/
│           ├── __init__.py
│           └── texture_picker.py       # Copy Asset Name tool
└── uefn_test_tool.uplugin
```
