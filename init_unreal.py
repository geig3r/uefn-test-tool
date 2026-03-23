"""
UEFN Test Tool - Editor startup script.

This file is automatically executed by Unreal Engine when the editor loads
because it lives in the project's Content/Python/ directory and is named
init_unreal.py.
"""

import sys
import os

# Add the uefn-test-tool folder to sys.path so its modules can be imported
# directly (Python cannot import names containing hyphens as a package).
_this_dir = os.path.dirname(os.path.abspath(__file__))
_tool_dir = os.path.join(_this_dir, "uefn-test-tool")
if _tool_dir not in sys.path:
    sys.path.insert(0, _tool_dir)

import unreal
import texture_picker, asset_browser

texture_picker.register_menu_entries()
asset_browser.register_menu_entries()
