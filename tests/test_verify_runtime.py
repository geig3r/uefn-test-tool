from __future__ import annotations

from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.install_runtime import install_runtime
from tools.verify_runtime import main, verify_runtime


class VerifyRuntimeTests(unittest.TestCase):
    def test_verify_runtime_reports_missing_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp)
            _, missing = verify_runtime(project_root)
            self.assertTrue(missing)
            self.assertIn(Path('Content/Python/init_unreal.py'), missing)

    def test_verify_runtime_passes_after_install(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp)
            install_runtime(project_root)
            _, missing = verify_runtime(project_root)
            self.assertEqual(missing, [])
            code = main(['--project-dir', tmp])
            self.assertEqual(code, 0)


if __name__ == '__main__':
    unittest.main()
