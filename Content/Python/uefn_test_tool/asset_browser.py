"""
Asset Browser
=============
Browse UEFN built-in assets by category, copy names to clipboard,
or export a full category list to CSV.

Opens via: Tools → UEFN Test Tools → Open Asset Browser
"""

import csv
import os
import tempfile
import unreal

try:
    from PySide2 import QtWidgets, QtCore, QtGui
    from PySide2.QtCore import Qt
except ImportError:
    from PySide6 import QtWidgets, QtCore, QtGui
    from PySide6.QtCore import Qt

from uefn_test_tool.texture_picker import _copy_to_clipboard

# ---------------------------------------------------------------------------
# Category definitions: display name → Content Browser path
# Adjust these paths to match your project's Fortnite asset structure.
# ---------------------------------------------------------------------------
CATEGORIES = {
    "Weapons":      "/Fortnite/Weapons",
    "Items":        "/Fortnite/Items",
    "Characters":   "/Fortnite/Characters",
    "Environment":  "/Fortnite/Environment",
    "UI":           "/Fortnite/UI",
}


# ---------------------------------------------------------------------------
# Asset Registry helpers
# ---------------------------------------------------------------------------

def _list_assets(folder_path: str) -> list[tuple[str, str]]:
    """Return [(asset_name, object_path), ...] for all assets under folder_path."""
    registry = unreal.AssetRegistry.get()
    ar_filter = unreal.ARFilter(
        package_paths=[folder_path],
        recursive_paths=True,
    )
    assets = registry.get_assets(ar_filter)
    return sorted(
        [(str(a.asset_name), str(a.object_path)) for a in assets],
        key=lambda x: x[0].lower(),
    )


# ---------------------------------------------------------------------------
# Qt window
# ---------------------------------------------------------------------------

class AssetBrowserWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("UEFN Asset Browser")
        self.setMinimumSize(520, 640)
        self._all_assets: list[tuple[str, str]] = []
        self._active_category: str = next(iter(CATEGORIES))
        self._setup_ui()
        self._load_category(self._active_category)

    def _setup_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.setSpacing(6)

        # --- Category buttons ---
        category_bar = QtWidgets.QHBoxLayout()
        category_bar.setSpacing(4)
        self._category_group = QtWidgets.QButtonGroup(self)
        self._category_group.setExclusive(True)
        for i, name in enumerate(CATEGORIES):
            btn = QtWidgets.QPushButton(name)
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, c=name: self._load_category(c))
            self._category_group.addButton(btn)
            category_bar.addWidget(btn)
            if i == 0:
                btn.setChecked(True)
        layout.addLayout(category_bar)

        # --- Search ---
        self._search = QtWidgets.QLineEdit()
        self._search.setPlaceholderText("Filter assets…")
        self._search.setClearButtonEnabled(True)
        self._search.textChanged.connect(self._filter_list)
        layout.addWidget(self._search)

        # --- Asset count label ---
        self._count_label = QtWidgets.QLabel("")
        self._count_label.setStyleSheet("color: gray; font-size: 11px;")
        layout.addWidget(self._count_label)

        # --- Asset list ---
        self._list = QtWidgets.QListWidget()
        self._list.setAlternatingRowColors(True)
        self._list.itemClicked.connect(self._on_select)
        self._list.itemDoubleClicked.connect(self._copy_item)
        layout.addWidget(self._list)

        # --- Selected asset display ---
        selected_row = QtWidgets.QHBoxLayout()
        self._selected_label = QtWidgets.QLineEdit()
        self._selected_label.setReadOnly(True)
        self._selected_label.setPlaceholderText("Select an asset…")
        self._selected_label.setStyleSheet("font-size: 13px; font-weight: bold;")
        selected_row.addWidget(self._selected_label)

        copy_btn = QtWidgets.QPushButton("Copy Name")
        copy_btn.setFixedWidth(90)
        copy_btn.clicked.connect(self._copy_selected)
        selected_row.addWidget(copy_btn)
        layout.addLayout(selected_row)

        # --- CSV export ---
        export_btn = QtWidgets.QPushButton("Export Category to CSV…")
        export_btn.clicked.connect(self._export_csv)
        layout.addWidget(export_btn)

    # --- Data loading ---

    def _load_category(self, category: str):
        self._active_category = category
        self._search.clear()
        self._all_assets = _list_assets(CATEGORIES[category])
        self._populate_list(self._all_assets)

    def _filter_list(self, text: str):
        if not text:
            self._populate_list(self._all_assets)
        else:
            q = text.lower()
            self._populate_list([(n, p) for n, p in self._all_assets if q in n.lower()])

    def _populate_list(self, assets: list[tuple[str, str]]):
        self._list.clear()
        for name, path in assets:
            item = QtWidgets.QListWidgetItem(name)
            item.setData(Qt.UserRole, name)
            item.setToolTip(path)
            self._list.addItem(item)
        count = len(assets)
        total = len(self._all_assets)
        self._count_label.setText(
            f"{count} asset{'s' if count != 1 else ''}"
            + (f" (filtered from {total})" if count != total else "")
        )

    # --- Actions ---

    def _on_select(self, item: QtWidgets.QListWidgetItem):
        self._selected_label.setText(item.data(Qt.UserRole))

    def _copy_item(self, item: QtWidgets.QListWidgetItem):
        name = item.data(Qt.UserRole)
        self._selected_label.setText(name)
        self._do_copy(name)

    def _copy_selected(self):
        items = self._list.selectedItems()
        if items:
            self._do_copy(items[0].data(Qt.UserRole))

    def _do_copy(self, name: str):
        if _copy_to_clipboard(name):
            unreal.log(f"[UEFN Test Tool] Copied: {name}")

    def _export_csv(self):
        """Write the current category's assets to a CSV file and open it."""
        if not self._all_assets:
            QtWidgets.QMessageBox.information(
                self, "Nothing to export", "No assets loaded in this category."
            )
            return

        # Ask user where to save
        default_name = f"uefn_{self._active_category.lower()}_assets.csv"
        path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self,
            "Export to CSV",
            os.path.join(os.path.expanduser("~"), default_name),
            "CSV files (*.csv)",
        )
        if not path:
            return

        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Asset Name", "Object Path"])
            writer.writerows(self._all_assets)

        unreal.log(f"[UEFN Test Tool] Exported {len(self._all_assets)} assets to {path}")

        # Open the file so the user can import it into a spreadsheet
        import subprocess, sys
        if sys.platform == "win32":
            os.startfile(path)
        elif sys.platform == "darwin":
            subprocess.run(["open", path])
        else:
            subprocess.run(["xdg-open", path])


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

_window = None  # module-level ref keeps Qt from garbage-collecting the window


def open_asset_browser():
    global _window
    _window = AssetBrowserWindow()
    _window.show()
    _window.raise_()


def register_menu_entries():
    """Register 'Open Asset Browser' under Tools → UEFN Test Tools."""
    menus = unreal.ToolMenus.get()

    menu = menus.extend_menu("MainFrame.MainMenu.Tools")
    section = menu.add_section(
        "UEFNTestTools",
        label=unreal.Text("UEFN Test Tools"),
    )

    entry = unreal.ToolMenuEntry(
        name="UEFNTestTool_OpenAssetBrowser",
        type=unreal.MultiBlockType.MENU_ENTRY,
        insert_position=unreal.ToolMenuInsert("", unreal.ToolMenuInsertType.DEFAULT),
    )
    entry.set_label("Open Asset Browser")
    entry.set_tool_tip(
        "Browse UEFN built-in assets by category.\n"
        "Click an asset to copy its name, or export the full list to CSV."
    )
    entry.set_string_command(
        type=unreal.ToolMenuStringCommandType.PYTHON,
        custom_type="",
        string=(
            "from uefn_test_tool import asset_browser; "
            "asset_browser.open_asset_browser()"
        ),
    )
    section.add_entry(entry)

    menus.refresh_all_widgets()
