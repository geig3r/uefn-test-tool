"""
init_unreal.py — auto-loaded by Unreal on startup.

Place this file and the other .py files from this repo into:
    <YourProject>/Content/Python/

Unreal will execute init_unreal.py automatically when the editor starts.
"""

import texture_picker
import asset_browser

texture_picker.register_menu_entries()
asset_browser.register_menu_entries()
