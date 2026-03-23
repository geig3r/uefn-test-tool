"""
Asset Browser
=============
Browse UEFN built-in assets by category, copy names to clipboard,
or export a full category list to CSV.

Opens via: Tools → UEFN Test Tools → Open Asset Browser
"""

import csv
import os
import subprocess
import tkinter as tk
import unreal

from texture_picker import _copy_to_clipboard

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

BG      = "#080812"
PBG     = "#111125"
FG      = "#d0d0e0"
ACC     = "#e94560"
ENTRY_BG = "#1a1a35"


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
# Tkinter window
# ---------------------------------------------------------------------------

class AssetBrowserWindow:
    def __init__(self):
        self._all_assets: list[tuple[str, str]] = []
        self._active_category: str = next(iter(CATEGORIES))
        self._tick_handle = None

        self.root = tk.Tk()
        self.root.title("UEFN Asset Browser")
        self.root.geometry("520x640")
        self.root.configure(bg=BG)
        self.root.attributes("-topmost", True)

        self._build_ui()
        self._load_category(self._active_category)
        self._start_tick()

    # --- UI construction ---

    def _build_ui(self):
        # Category buttons
        cat_frame = tk.Frame(self.root, bg=PBG)
        cat_frame.pack(fill="x", padx=0, pady=0)
        self._cat_buttons: dict[str, tk.Button] = {}
        for name in CATEGORIES:
            btn = tk.Button(
                cat_frame, text=name, bg=PBG, fg="#888",
                font=("Segoe UI", 9), relief="flat", cursor="hand2",
                activebackground=ACC, activeforeground="white",
                command=lambda n=name: self._load_category(n),
            )
            btn.pack(side="left", padx=2, pady=6, ipady=4, ipadx=6)
            self._cat_buttons[name] = btn

        # Search
        search_frame = tk.Frame(self.root, bg=BG)
        search_frame.pack(fill="x", padx=10, pady=(8, 0))
        tk.Label(search_frame, text="Filter:", fg="#666", bg=BG,
                 font=("Segoe UI", 9)).pack(side="left")
        self._search_var = tk.StringVar()
        self._search_var.trace_add("write", lambda *_: self._filter_list())
        tk.Entry(
            search_frame, textvariable=self._search_var,
            bg=ENTRY_BG, fg=FG, insertbackground=FG,
            font=("Segoe UI", 9), relief="flat",
        ).pack(side="left", fill="x", expand=True, padx=(6, 0))

        # Count label
        self._count_var = tk.StringVar(value="")
        tk.Label(self.root, textvariable=self._count_var, fg="#555",
                 bg=BG, font=("Segoe UI", 8), anchor="w").pack(
            fill="x", padx=10, pady=(4, 0))

        # Asset listbox
        list_frame = tk.Frame(self.root, bg=BG)
        list_frame.pack(fill="both", expand=True, padx=10, pady=(4, 0))

        sb = tk.Scrollbar(list_frame, orient="vertical")
        self._listbox = tk.Listbox(
            list_frame, yscrollcommand=sb.set,
            bg="#0c0c1a", fg=FG, selectbackground=ACC, selectforeground="white",
            font=("Segoe UI", 9), relief="flat", bd=0,
            activestyle="none",
        )
        sb.config(command=self._listbox.yview)
        sb.pack(side="right", fill="y")
        self._listbox.pack(side="left", fill="both", expand=True)
        self._listbox.bind("<<ListboxSelect>>", self._on_select)
        self._listbox.bind("<Double-Button-1>", self._on_double_click)

        # Selected asset + copy button
        sel_frame = tk.Frame(self.root, bg=BG)
        sel_frame.pack(fill="x", padx=10, pady=8)
        self._selected_var = tk.StringVar(value="")
        tk.Entry(
            sel_frame, textvariable=self._selected_var,
            bg=ENTRY_BG, fg="white", font=("Segoe UI", 11, "bold"),
            relief="flat", state="readonly",
        ).pack(side="left", fill="x", expand=True)
        tk.Button(
            sel_frame, text="Copy Name", bg=ACC, fg="white",
            font=("Segoe UI", 9, "bold"), relief="flat", cursor="hand2",
            command=self._copy_selected,
        ).pack(side="left", padx=(6, 0), ipady=4, ipadx=8)

        # CSV export
        tk.Button(
            self.root, text="Export Category to CSV…",
            bg=PBG, fg=FG, font=("Segoe UI", 9), relief="flat", cursor="hand2",
            command=self._export_csv,
        ).pack(pady=(0, 10), ipady=5)

    # --- Data ---

    def _load_category(self, category: str):
        self._active_category = category
        self._search_var.set("")
        # Highlight active button
        for name, btn in self._cat_buttons.items():
            btn.configure(fg="white" if name == category else "#888",
                          bg=ACC if name == category else PBG)
        self._all_assets = _list_assets(CATEGORIES[category])
        self._populate_list(self._all_assets)

    def _filter_list(self):
        q = self._search_var.get().strip().lower()
        if q:
            filtered = [(n, p) for n, p in self._all_assets if q in n.lower()]
        else:
            filtered = self._all_assets
        self._populate_list(filtered)

    def _populate_list(self, assets: list[tuple[str, str]]):
        self._listbox.delete(0, tk.END)
        for name, _ in assets:
            self._listbox.insert(tk.END, name)
        count = len(assets)
        total = len(self._all_assets)
        self._count_var.set(
            f"{count} asset{'s' if count != 1 else ''}"
            + (f"  (filtered from {total})" if count != total else "")
        )
        # Keep track of the filtered list so double-click can resolve paths
        self._visible_assets = assets

    # --- Actions ---

    def _on_select(self, _event=None):
        sel = self._listbox.curselection()
        if sel:
            self._selected_var.set(self._visible_assets[sel[0]][0])

    def _on_double_click(self, _event=None):
        self._on_select()
        self._copy_selected()

    def _copy_selected(self):
        name = self._selected_var.get()
        if name:
            if _copy_to_clipboard(name):
                unreal.log(f"[UEFN Test Tool] Copied: {name}")

    def _export_csv(self):
        if not self._all_assets:
            return

        from tkinter import filedialog
        default_name = f"uefn_{self._active_category.lower()}_assets.csv"
        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            initialfile=default_name,
            title="Export to CSV",
        )
        if not path:
            return

        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Asset Name", "Object Path"])
            writer.writerows(self._all_assets)

        unreal.log(f"[UEFN Test Tool] Exported {len(self._all_assets)} assets to {path}")

        import sys
        if sys.platform == "win32":
            os.startfile(path)
        elif sys.platform == "darwin":
            subprocess.run(["open", path])
        else:
            subprocess.run(["xdg-open", path])

    # --- Tick (drives Tkinter event loop inside UE main thread) ---

    def _start_tick(self):
        def on_tick(_dt):
            try:
                if not self.root.winfo_exists():
                    self._stop_tick()
                    return
                self.root.update()
            except tk.TclError:
                self._stop_tick()

        self._tick_handle = unreal.register_slate_post_tick_callback(on_tick)
        unreal.log("[UEFN Test Tool] Asset Browser opened.")

    def _stop_tick(self):
        if self._tick_handle:
            unreal.unregister_slate_post_tick_callback(self._tick_handle)
            self._tick_handle = None
        unreal.log("[UEFN Test Tool] Asset Browser closed.")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

_window: AssetBrowserWindow | None = None  # module-level ref prevents GC


def open_asset_browser():
    global _window
    _window = AssetBrowserWindow()


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
        string="import asset_browser; asset_browser.open_asset_browser()",
    )
    section.add_entry(entry)

    menus.refresh_all_widgets()
