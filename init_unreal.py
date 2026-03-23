"""
UEFN Test Tool - Editor startup script.

This file is automatically executed by Unreal Engine when the editor loads
because it lives in the project's Content/Python/ directory and is named
init_unreal.py.
"""

import sys
import os

# Ensure this script's directory is on sys.path so the uefn_test_tool package
# can be found whether this script runs via auto-startup or the `py` command.
_this_dir = os.path.dirname(os.path.abspath(__file__))
if _this_dir not in sys.path:
    sys.path.insert(0, _this_dir)

import unreal
from uefn_test_tool import texture_picker, asset_browser

texture_picker.register_menu_entries()
asset_browser.register_menu_entries()
