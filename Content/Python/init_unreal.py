"""
UEFN Test Tool - Editor startup script.

This file is automatically executed by Unreal Engine when the editor loads
because it lives in a plugin's Content/Python/ directory and is named
init_unreal.py.
"""

import unreal
from uefn_test_tool import texture_picker

texture_picker.register_menu_entries()
