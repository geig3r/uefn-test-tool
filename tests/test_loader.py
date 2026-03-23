from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import types
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))


class FakeToolMenuEntry:
    def __init__(self, name: str, type: object):
        self.name = name
        self.type = type
        self.label = None
        self.tool_tip = None
        self.command = None

    def set_label(self, label: str) -> None:
        self.label = label

    def set_tool_tip(self, tool_tip: str) -> None:
        self.tool_tip = tool_tip

    def set_string_command(self, command_type: object, custom_type: str, string: str) -> None:
        self.command = (command_type, custom_type, string)


class FakeSubMenu:
    def __init__(self) -> None:
        self.entries: list[tuple[str, FakeToolMenuEntry]] = []

    def add_menu_entry(self, section_name: str, entry: FakeToolMenuEntry) -> None:
        self.entries.append((section_name, entry))


class FakeMainMenu:
    def __init__(self) -> None:
        self.submenus: list[FakeSubMenu] = []

    def add_sub_menu(self, **_: object) -> FakeSubMenu:
        submenu = FakeSubMenu()
        self.submenus.append(submenu)
        return submenu


class FakeToolMenusManager:
    def __init__(self) -> None:
        self.main_menu = FakeMainMenu()
        self.refreshed = False

    def extend_menu(self, name: str) -> FakeMainMenu:
        assert name == 'LevelEditor.MainMenu'
        return self.main_menu

    def refresh_all_widgets(self) -> None:
        self.refreshed = True


class FakeToolMenusAPI:
    def __init__(self, manager: FakeToolMenusManager) -> None:
        self.manager = manager

    def get(self) -> FakeToolMenusManager:
        return self.manager


class FakePaths:
    def __init__(self, content_dir: Path) -> None:
        self._content_dir = content_dir

    def project_content_dir(self) -> str:
        return str(self._content_dir) + '/'

    def project_dir(self) -> str:
        return str(self._content_dir.parent) + '/'

    def project_saved_dir(self) -> str:
        return str(self._content_dir.parent / 'Saved') + '/'


class LoaderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.python_dir = ROOT
        self.logs: list[str] = []
        self.warnings: list[str] = []
        self.errors: list[str] = []
        self.manager = FakeToolMenusManager()
        self.callbacks: dict[int, object] = {}
        self.next_handle = 1

        fake_unreal = types.ModuleType('unreal')
        fake_unreal.Paths = FakePaths(self.python_dir)
        fake_unreal.MultiBlockType = types.SimpleNamespace(MENU_ENTRY='MENU_ENTRY')
        fake_unreal.ToolMenuStringCommandType = types.SimpleNamespace(PYTHON='PYTHON')
        fake_unreal.ToolMenuEntry = FakeToolMenuEntry
        fake_unreal.ToolMenus = FakeToolMenusAPI(self.manager)
        fake_unreal.log = self.logs.append
        fake_unreal.log_warning = self.warnings.append
        fake_unreal.log_error = self.errors.append

        def register_slate_pre_tick_callback(callback: object) -> int:
            handle = self.next_handle
            self.next_handle += 1
            self.callbacks[handle] = callback
            return handle

        def unregister_slate_pre_tick_callback(handle: int) -> None:
            self.callbacks.pop(handle, None)

        fake_unreal.register_slate_pre_tick_callback = register_slate_pre_tick_callback
        fake_unreal.unregister_slate_pre_tick_callback = unregister_slate_pre_tick_callback
        sys.modules['unreal'] = fake_unreal

        content_python = str(self.python_dir)
        if content_python not in sys.path:
            sys.path.insert(0, content_python)

        self._purge_modules()

    def tearDown(self) -> None:
        self._purge_modules()
        sys.modules.pop('unreal', None)
        content_python = str(self.python_dir)
        if content_python in sys.path:
            sys.path.remove(content_python)

    def _purge_modules(self) -> None:
        for name in list(sys.modules):
            if name == 'uefn_test_tool' or name.startswith('uefn_test_tool.'):
                sys.modules.pop(name, None)

    def test_init_unreal_finds_and_registers_package(self) -> None:
        loader_path = ROOT / 'init_unreal.py'
        spec = importlib.util.spec_from_file_location('init_unreal_test', loader_path)
        module = importlib.util.module_from_spec(spec)
        assert spec and spec.loader
        spec.loader.exec_module(module)

        self.assertTrue(any('package(s) registered: uefn_test_tool' in message for message in self.logs))
        self.assertTrue(any('Menu registration scheduled.' in message for message in self.logs))
        self.assertEqual(self.errors, [])
        self.assertTrue(self.callbacks)

    def test_runtime_files_exist_in_repo_root(self) -> None:
        self.assertTrue((ROOT / 'init_unreal.py').exists())
        self.assertTrue((ROOT / 'uefn_test_tool' / '__init__.py').exists())
        self.assertTrue((ROOT / 'uefn_test_tool' / 'actions.py').exists())
        self.assertTrue((ROOT / 'uefn_test_tool' / 'asset_browser.py').exists())
        self.assertTrue((ROOT / 'uefn_test_tool' / 'menu.py').exists())

    def test_scheduled_menu_builds_entries(self) -> None:
        import uefn_test_tool

        uefn_test_tool.register()
        callback = next(iter(self.callbacks.values()))
        callback(0.0)

        self.assertTrue(any('Menu registered under LevelEditor.MainMenu.' in message for message in self.logs))
        self.assertTrue(self.manager.refreshed)
        submenu = self.manager.main_menu.submenus[0]
        labels = [entry.label for _, entry in submenu.entries]
        self.assertEqual(labels, ['Log Python Environment', 'Browse Selected Folder Assets', 'Reload Package'])


if __name__ == '__main__':
    unittest.main()
