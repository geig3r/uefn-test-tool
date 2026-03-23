from __future__ import annotations

from pathlib import Path
import sys
import types
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


class AssetBrowserTests(unittest.TestCase):
    def setUp(self) -> None:
        self.logs: list[str] = []
        self.warnings: list[str] = []
        self.synced_folders: list[list[str]] = []
        self.synced_assets: list[list[str]] = []

        fake_unreal = types.ModuleType('unreal')
        fake_unreal.log = self.logs.append
        fake_unreal.log_warning = self.warnings.append
        fake_unreal.EditorUtilityLibrary = types.SimpleNamespace(
            get_selected_folder_paths=lambda: ['/Game/TestFolder'],
            sync_browser_to_folders=lambda folders: self.synced_folders.append(list(folders)),
        )
        fake_unreal.EditorAssetLibrary = types.SimpleNamespace(
            list_assets=lambda folder, recursive=False, include_folder=False: [
                f'{folder}/AssetA',
                f'{folder}/AssetB',
            ],
            sync_browser_to_objects=lambda asset_paths: self.synced_assets.append(list(asset_paths)),
        )
        sys.modules['unreal'] = fake_unreal
        sys.modules.pop('uefn_test_tool.asset_browser', None)

    def tearDown(self) -> None:
        sys.modules.pop('unreal', None)
        sys.modules.pop('uefn_test_tool.asset_browser', None)

    def test_browse_selected_folder_assets_syncs_folder_and_assets(self) -> None:
        from uefn_test_tool import asset_browser

        asset_browser.browse_selected_folder_assets()

        self.assertEqual(self.synced_folders, [['/Game/TestFolder']])
        self.assertEqual(self.synced_assets, [['/Game/TestFolder/AssetA', '/Game/TestFolder/AssetB']])
        self.assertTrue(any('Browsing 2 asset(s) from /Game/TestFolder' in message for message in self.logs))


if __name__ == '__main__':
    unittest.main()
