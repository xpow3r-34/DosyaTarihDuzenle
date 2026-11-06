"""Batch-edit file timestamps with drag-and-drop and ordered increments."""

from __future__ import annotations

import ctypes
import os
import sys
import tkinter as tk
from datetime import datetime, timedelta, timezone
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from PIL import Image, ImageTk
from tkinterdnd2 import DND_FILES, TkinterDnD

APP_VERSION = "1.3.2"
DATE_FORMAT = "%d.%m.%Y %H:%M:%S"
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp", ".tif", ".tiff"}


def windows_set_times(path: Path, value: datetime, creation: bool, modified: bool, accessed: bool) -> None:
    """Set selected timestamps using the Windows file handle API."""
    if os.name != "nt":
        raise OSError("Oluşturulma zamanı yalnızca Windows üzerinde desteklenir.")

    class FILETIME(ctypes.Structure):
        _fields_ = [("dwLowDateTime", ctypes.c_uint32), ("dwHighDateTime", ctypes.c_uint32)]

    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel32.CreateFileW.argtypes = [ctypes.c_wchar_p, ctypes.c_uint32, ctypes.c_uint32,
                                     ctypes.c_void_p, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_void_p]
    kernel32.CreateFileW.restype = ctypes.c_void_p
    kernel32.SetFileTime.argtypes = [ctypes.c_void_p, ctypes.POINTER(FILETIME),
                                     ctypes.POINTER(FILETIME), ctypes.POINTER(FILETIME)]
    kernel32.SetFileTime.restype = ctypes.c_int
    kernel32.CloseHandle.argtypes = [ctypes.c_void_p]
    kernel32.CloseHandle.restype = ctypes.c_int

    handle = kernel32.CreateFileW(str(path), 0x0100, 0x00000001 | 0x00000002 | 0x00000004,
                                  None, 3, 0x80, None)
    if handle == ctypes.c_void_p(-1).value:
        raise ctypes.WinError(ctypes.get_last_error())
    try:
        utc_value = value.astimezone(timezone.utc)
        ticks = int(utc_value.timestamp() * 10_000_000) + 116_444_736_000_000_000
        timestamp = FILETIME(ticks & 0xFFFFFFFF, (ticks >> 32) & 0xFFFFFFFF)
        null = ctypes.POINTER(FILETIME)()
        creation_ptr = ctypes.byref(timestamp) if creation else null
        access_ptr = ctypes.byref(timestamp) if accessed else null
        write_ptr = ctypes.byref(timestamp) if modified else null
        if not kernel32.SetFileTime(handle, creation_ptr, access_ptr, write_ptr):
            raise ctypes.WinError(ctypes.get_last_error())
    finally:
        kernel32.CloseHandle(handle)


class TimestampApp(TkinterDnD.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title(f"Dosya Tarih Düzenle  |  v{APP_VERSION}")
        self.geometry("1120x700")
        self.minsize(800, 540)
        self.files: list[Path] = []
        self.thumbnail_refs: list[ImageTk.PhotoImage] = []
        self._build_ui()

    def _build_ui(self) -> None:
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)
        header = ttk.Frame(self, padding=(16, 14, 16, 8))
        header.grid(row=0, column=0, sticky="ew")
        ttk.Label(header, text="Dosya Tarih Düzenle", font=("Segoe UI", 18, "bold")).pack(anchor="w")
        ttk.Label(header, text="Dosyaları bırakın veya ekleyin; sıralama hedef tarihleri belirler.").pack(anchor="w", pady=(3, 0))

        settings = ttk.LabelFrame(self, text="Başlangıç zamanı ve uygulanacak alanlar", padding=12)
        settings.grid(row=1, column=0, sticky="ew", padx=16, pady=6)
        style = ttk.Style(self)
        style.configure("TimeField.TEntry", padding=(8, 6), font=("Segoe UI", 11))
        style.configure("FixedSeparator.TLabel", font=("Segoe UI", 12, "bold"), foreground="#64748b")
        now = datetime.now()
        date_fields = ttk.Frame(settings)
        date_fields.grid(row=0, column=0, sticky="w", padx=(0, 20))
        ttk.Label(date_fields, text="TARİH", font=("Segoe UI", 8, "bold"), foreground="#475569").pack(anchor="w", pady=(0, 4))
        date_row = ttk.Frame(date_fields)
        date_row.pack(anchor="w")
        self.day_var = tk.StringVar(value=f"{now.day:02d}")
        self.month_var = tk.StringVar(value=f"{now.month:02d}")
        self.year_var = tk.StringVar(value=f"{now.year:04d}")
        ttk.Entry(date_row, textvariable=self.day_var, width=3, justify="center", style="TimeField.TEntry").pack(side="left")
        ttk.Label(date_row, text=".", style="FixedSeparator.TLabel").pack(side="left", padx=4)
        ttk.Entry(date_row, textvariable=self.month_var, width=3, justify="center", style="TimeField.TEntry").pack(side="left")
        ttk.Label(date_row, text=".", style="FixedSeparator.TLabel").pack(side="left", padx=4)
        ttk.Entry(date_row, textvariable=self.year_var, width=5, justify="center", style="TimeField.TEntry").pack(side="left")

        time_fields = ttk.Frame(settings)
        time_fields.grid(row=0, column=1, sticky="w", padx=(0, 22))
        ttk.Label(time_fields, text="SAAT", font=("Segoe UI", 8, "bold"), foreground="#475569").pack(anchor="w", pady=(0, 4))
        time_row = ttk.Frame(time_fields)
        time_row.pack(anchor="w")
        self.hour_var = tk.StringVar(value=f"{now.hour:02d}")
        self.minute_var = tk.StringVar(value=f"{now.minute:02d}")
        self.second_var = tk.StringVar(value=f"{now.second:02d}")
        ttk.Entry(time_row, textvariable=self.hour_var, width=3, justify="center", style="TimeField.TEntry").pack(side="left")
        ttk.Label(time_row, text=":", style="FixedSeparator.TLabel").pack(side="left", padx=4)
        ttk.Entry(time_row, textvariable=self.minute_var, width=3, justify="center", style="TimeField.TEntry").pack(side="left")
        ttk.Label(time_row, text=":", style="FixedSeparator.TLabel").pack(side="left", padx=4)
        ttk.Entry(time_row, textvariable=self.second_var, width=3, justify="center", style="TimeField.TEntry").pack(side="left")

        increment_fields = ttk.Frame(settings)
        increment_fields.grid(row=0, column=2, sticky="w", padx=(0, 18))
        ttk.Label(increment_fields, text="Artış birimi").pack(anchor="w")
        self.increment_var = tk.StringVar(value="Saniye")
        ttk.Combobox(increment_fields, textvariable=self.increment_var, values=("Saniye", "Dakika"),
                     state="readonly", width=10).pack(anchor="w", pady=(3, 0))

        size_fields = ttk.Frame(settings)
        size_fields.grid(row=0, column=3, sticky="w", padx=(0, 18))
        ttk.Label(size_fields, text="Küçük resim boyutu (px)").pack(anchor="w")
        self.thumbnail_scale_var = tk.DoubleVar(value=48)
        self.thumbnail_scale = ttk.Scale(size_fields, from_=32, to=128, orient="horizontal", length=160,
                                         variable=self.thumbnail_scale_var)
        self.thumbnail_scale.pack(anchor="w", pady=(8, 0))

        options = ttk.Frame(settings)
        options.grid(row=0, column=4, sticky="w")
        ttk.Label(options, text="Zaman bilgileri").pack(anchor="w")
        checks = ttk.Frame(options)
        checks.pack(anchor="w", pady=(6, 0))
        self.creation_var = tk.BooleanVar(value=True)
        self.modified_var = tk.BooleanVar(value=True)
        self.accessed_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(checks, text="Oluşturulma", variable=self.creation_var).pack(side="left", padx=(0, 10))
        ttk.Checkbutton(checks, text="Değiştirilme", variable=self.modified_var).pack(side="left", padx=(0, 10))
        ttk.Checkbutton(checks, text="Son erişim", variable=self.accessed_var).pack(side="left")

        files_frame = ttk.LabelFrame(self, text="Dosyalar — sürükleyip buraya bırakabilir, sırasını değiştirebilirsiniz", padding=10)
        files_frame.grid(row=2, column=0, sticky="nsew", padx=16, pady=6)
        files_frame.columnconfigure(0, weight=1)
        files_frame.rowconfigure(0, weight=1)
        self.tree = ttk.Treeview(files_frame, columns=("path", "planned"), show=("tree", "headings"),
                                 selectmode="extended", height=10)
        self.tree.heading("#0", text="Önizleme / Dosya")
        self.tree.heading("path", text="Konum")
        self.tree.heading("planned", text="Uygulanacak tarih ve saat")
        self.tree.column("#0", width=230, anchor="w")
        self.tree.column("path", width=440, anchor="w")
        self.tree.column("planned", width=210, anchor="center")
        self.tree.tag_configure("image", foreground="#202020")
        style = ttk.Style(self)
        style.configure("Treeview", rowheight=round(self.thumbnail_scale_var.get()) + 12)
        scrollbar = ttk.Scrollbar(files_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree.drop_target_register(DND_FILES)
        self.tree.dnd_bind("<<Drop>>", self.on_drop)

        buttons = ttk.Frame(files_frame)
        buttons.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(9, 0))
        ttk.Button(buttons, text="Dosya ekle…", command=self.add_files).pack(side="left")
        ttk.Button(buttons, text="Seçilenleri kaldır", command=self.remove_selected).pack(side="left", padx=(8, 0))
        ttk.Button(buttons, text="Listeyi temizle", command=self.clear_files).pack(side="left", padx=(8, 0))
        ttk.Button(buttons, text="Yukarı taşı", command=lambda: self.move_selected(-1)).pack(side="left", padx=(22, 0))
        ttk.Button(buttons, text="Aşağı taşı", command=lambda: self.move_selected(1)).pack(side="left", padx=8)
        ttk.Button(buttons, text="Tarihleri uygula", command=self.apply).pack(side="right")
        self.status_var = tk.StringVar(value="Dosyaları sürükleyip listeye bırakın veya Dosya ekle'yi kullanın.")
        ttk.Label(self, textvariable=self.status_var, anchor="w", padding=(17, 5)).grid(row=3, column=0, sticky="ew")
        self.thumbnail_scale.bind("<ButtonRelease-1>", lambda _event: self.refresh_list())
        self.thumbnail_scale.bind("<KeyRelease>", lambda _event: self.refresh_list())
        for variable in (self.day_var, self.month_var, self.year_var, self.hour_var,
                         self.minute_var, self.second_var, self.increment_var):
            variable.trace_add("write", lambda *_: self.refresh_list())

    def add_paths(self, paths: list[str | Path]) -> None:
        known = {os.path.normcase(os.path.abspath(p)) for p in self.files}
        added = 0
        for item in paths:
            path = Path(item)
            key = os.path.normcase(os.path.abspath(path))
            if path.is_file() and key not in known:
                self.files.append(path)
                known.add(key)
                added += 1
        self.refresh_list()
        if added:
            self.status_var.set(f"{added} dosya eklendi; toplam {len(self.files)} dosya.")

    def on_drop(self, event: tk.Event) -> str:
        self.add_paths(self.tk.splitlist(event.data))
        return "break"

    def add_files(self) -> None:
        selected = filedialog.askopenfilenames(title="Tarihleri değiştirilecek dosyaları seçin")
        self.add_paths(list(selected))

    def remove_selected(self) -> None:
        indices = sorted((int(iid) for iid in self.tree.selection()), reverse=True)
        for index in indices:
            del self.files[index]
        self.refresh_list()

    def clear_files(self) -> None:
        self.files.clear()
        self.refresh_list()

    def move_selected(self, direction: int) -> None:
        selected_paths = {self.files[int(iid)] for iid in self.tree.selection()}
        if not selected_paths:
            return
        selected_indices = {i for i, path in enumerate(self.files) if path in selected_paths}
        if direction < 0:
            for index in range(1, len(self.files)):
                if index in selected_indices and index - 1 not in selected_indices:
                    self.files[index - 1], self.files[index] = self.files[index], self.files[index - 1]
                    selected_indices.remove(index)
                    selected_indices.add(index - 1)
        else:
            for index in range(len(self.files) - 2, -1, -1):
                if index in selected_indices and index + 1 not in selected_indices:
                    self.files[index], self.files[index + 1] = self.files[index + 1], self.files[index]
                    selected_indices.remove(index)
                    selected_indices.add(index + 1)
        self.refresh_list(selected_paths)

    def planned_time(self, start: datetime, index: int) -> datetime:
        amount = timedelta(seconds=index) if self.increment_var.get() == "Saniye" else timedelta(minutes=index)
        return start + amount

    def get_start_datetime(self) -> datetime:
        value = (f"{self.day_var.get()}.{self.month_var.get()}.{self.year_var.get()} "
                 f"{self.hour_var.get()}:{self.minute_var.get()}:{self.second_var.get()}")
        return datetime.strptime(value, DATE_FORMAT).astimezone()

    def refresh_list(self, selected_paths: set[Path] | None = None) -> None:
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.thumbnail_refs = []
        thumbnail_size = round(self.thumbnail_scale_var.get())
        ttk.Style(self).configure("Treeview", rowheight=thumbnail_size + 12)
        try:
            start = self.get_start_datetime()
            valid_date = True
        except ValueError:
            start = datetime.now().astimezone()
            valid_date = False
        for index, path in enumerate(self.files):
            planned = self.planned_time(start, index).strftime(DATE_FORMAT) if valid_date else "Tarih biçimini kontrol edin"
            thumbnail = None
            if path.suffix.lower() in IMAGE_EXTENSIONS:
                try:
                    with Image.open(path) as image:
                        image.thumbnail((thumbnail_size, thumbnail_size))
                        thumbnail = ImageTk.PhotoImage(image.copy())
                        self.thumbnail_refs.append(thumbnail)
                except (OSError, ValueError):
                    pass
            self.tree.insert("", "end", iid=str(index), text=path.name,
                             image=thumbnail if thumbnail else "", values=(str(path.parent), planned))
        if selected_paths:
            selection = [str(i) for i, path in enumerate(self.files) if path in selected_paths]
            self.tree.selection_set(selection)
        self.status_var.set(f"{len(self.files)} dosya listede. Artış birimi: {self.increment_var.get().lower()}.")

    def apply(self) -> None:
        if not self.files:
            messagebox.showinfo("Dosya seçilmedi", "Önce dosya ekleyin veya sürükleyip listeye bırakın.", parent=self)
            return
        if not any((self.creation_var.get(), self.modified_var.get(), self.accessed_var.get())):
            messagebox.showinfo("Zaman alanı seçilmedi", "Değiştirilecek en az bir zaman alanı seçin.", parent=self)
            return
        try:
            start = self.get_start_datetime()
        except ValueError:
            messagebox.showerror("Geçersiz tarih veya saat", "Tarih ve saat alanlarını kontrol edin.", parent=self)
            return
        unit = self.increment_var.get().lower()
        if not messagebox.askyesno("Tarihleri uygula", f"{len(self.files)} dosyanın seçilen zaman bilgileri güncellensin mi?\nArtış: {unit}", parent=self):
            return
        success = 0
        errors: list[str] = []
        for index, path in enumerate(self.files):
            try:
                windows_set_times(path, self.planned_time(start, index), self.creation_var.get(),
                                  self.modified_var.get(), self.accessed_var.get())
                success += 1
            except (OSError, ValueError) as exc:
                errors.append(f"{path.name}: {exc}")
        self.status_var.set(f"Uygulandı: {success}/{len(self.files)} dosya.")
        if errors:
            messagebox.showwarning("Bazı dosyalar güncellenemedi", f"{success} dosya güncellendi. Hatalar:\n\n" + "\n".join(errors[:12]), parent=self)
        else:
            messagebox.showinfo("Tamamlandı", f"{success} dosyanın zaman bilgileri güncellendi.", parent=self)


if __name__ == "__main__":
    if sys.version_info < (3, 10):
        raise SystemExit("Bu uygulama Python 3.10 veya üzerini gerektirir.")
    TimestampApp().mainloop()
