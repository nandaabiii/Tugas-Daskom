# ============================================================
# ui.py  —  GUI Utama
# Sistem Informasi Akademik Mahasiswa
# macOS Sonoma Inspired Design - Dark Mode Glassmorphism
# CustomTkinter Compatible (HEX colors only, no rgba/CSS)
# ============================================================

import customtkinter as ctk
from tkinter import messagebox, ttk
import tkinter as tk
import db
import math

# ============================================================
# TEMA - macOS Dark Mode dengan Glassmorphism Effect
# Menggunakan HEX colors saja (compatible dengan CustomTkinter)
# ============================================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Palette warna dark mode dengan gradient navy → purple → pink aesthetic
C = {
    # Background gradients (simulasi glass dengan layered colors)
    "bg_dark":      "#0F1428",       # Deep navy background
    "bg_card":      "#1E233C",       # Card background (semi-transparent look)
    "bg_sidebar":   "#161B33",       # Sidebar background
    "bg_header":    "#1A1F35",       # Header background
    
    # Accent colors untuk gradient effect
    "accent_blue":  "#3B82F6",       # Bright blue
    "accent_purple":"#7C3AED",       # Purple
    "accent_pink":  "#EC4899",       # Pink
    "accent_cyan":  "#06B6D4",       # Cyan
    
    # Glass effect layers (simulasi transparansi dengan opacity visual)
    "glass_light":  "#2D3550",       # Light glass layer
    "glass_dark":   "#1F2540",       # Dark glass layer
    "glass_border": "#3D4560",       # Border untuk depth
    
    # Text colors
    "text_primary": "#F1F5F9",       # Primary text (white-ish)
    "text_secondary":"#94A3B8",      # Secondary text (gray)
    "text_muted":   "#64748B",       # Muted text
    
    # Status colors
    "success":      "#10B981",       # Green success
    "success_bg":   "#064E3B",       # Green background
    "warning":      "#F59E0B",       # Yellow warning
    "warning_bg":   "#78350F",       # Yellow background
    "danger":       "#EF4444",       # Red danger
    "danger_bg":    "#7F1D1D",       # Red background
    "info":         "#3B82F6",       # Blue info
    "info_bg":      "#1E3A8A",       # Blue background
    
    # UI elements
    "input_bg":     "#252D45",       # Input field background
    "input_border": "#3D4560",       # Input border
    "hover":        "#334155",       # Hover state
    "active":       "#475569",       # Active state
    "separator":    "#334155",       # Separator lines
}

# Typography - Modern clean fonts
F_JUDUL    = ("SF Pro Display", 24, "bold")
F_SUBJUDUL = ("SF Pro Display", 16, "bold")
F_NORMAL   = ("SF Pro Display", 13)
F_KECIL    = ("SF Pro Display", 11)
F_TABEL    = ("SF Pro Display", 12)
F_MONO     = ("Consolas", 11)

# Fallback fonts jika SF Pro tidak tersedia
FONT_FALLBACK = ("Segoe UI", 13)

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def _gelap(hex_color: str, amount: int = 25) -> str:
    """Membuat warna lebih gelap untuk hover effects."""
    try:
        r = max(0, min(255, int(hex_color[1:3], 16) - amount))
        g = max(0, min(255, int(hex_color[3:5], 16) - amount))
        b = max(0, min(255, int(hex_color[5:7], 16) - amount))
        return f"#{r:02x}{g:02x}{b:02x}"
    except Exception:
        return hex_color


def _terang(hex_color: str, amount: int = 25) -> str:
    """Membuat warna lebih terang untuk highlight."""
    try:
        r = min(255, int(hex_color[1:3], 16) + amount)
        g = min(255, int(hex_color[3:5], 16) + amount)
        b = min(255, int(hex_color[5:7], 16) + amount)
        return f"#{r:02x}{g:02x}{b:02x}"
    except Exception:
        return hex_color


def _entry(parent, placeholder="", show="", width=280):
    """Create modern rounded input field with glass effect."""
    entry = ctk.CTkEntry(
        parent, 
        width=width, 
        height=44,
        placeholder_text=placeholder,
        show=show,
        font=FONT_FALLBACK,
        corner_radius=12,
        border_width=1,
        border_color=C["input_border"],
        fg_color=C["input_bg"],
        text_color=C["text_primary"],
    )
    return entry


def _btn(parent, text, command, color=None, width=140, height=44, icon=""):
    """Create modern button with rounded corners and hover effect."""
    color = color or C["accent_blue"]
    btn = ctk.CTkButton(
        parent, 
        text=icon + " " + text if icon else text, 
        command=command,
        width=width, 
        height=height,
        font=("Segoe UI", 12, "bold"),
        fg_color=color,
        hover_color=_gelap(color, 20),
        corner_radius=12,
    )
    return btn


def _btn_ghost(parent, text, command, width=140, height=40):
    """Create ghost/outline button for secondary actions."""
    btn = ctk.CTkButton(
        parent,
        text=text,
        command=command,
        width=width,
        height=height,
        font=("Segoe UI", 11),
        fg_color="transparent",
        hover_color=C["hover"],
        corner_radius=10,
        border_width=1,
        border_color=C["glass_border"],
        text_color=C["text_primary"],
    )
    return btn


def _label(parent, text, font=None, color=None, anchor="w", wraplength=0):
    """Create label with proper styling."""
    return ctk.CTkLabel(
        parent, 
        text=text,
        font=font or FONT_FALLBACK,
        text_color=color or C["text_primary"],
        anchor=anchor,
        wraplength=wraplength,
    )


def _card(parent, corner_radius=16, pad=0, **kw):
    """Create glassmorphism card effect."""
    defaults = {
        "fg_color": C["bg_card"],
        "corner_radius": corner_radius,
        "border_width": 1,
        "border_color": C["glass_border"],
    }
    defaults.update(kw)
    return ctk.CTkFrame(parent, **defaults)


def _bind_enter_chain(entries: list):
    """Bind Enter key to navigate between fields."""
    for i, e in enumerate(entries):
        if i < len(entries) - 1:
            nxt = entries[i + 1]
            e.bind("<Return>", lambda ev, n=nxt: n.focus_set())


# ============================================================
# TREEVIEW STYLE - Modern Table Styling
# ============================================================

def _style_tree():
    """Style Treeview untuk tampilan modern."""
    s = ttk.Style()
    s.theme_use("clam")
    
    # Configure Treeview
    s.configure("App.Treeview",
        background=C["bg_card"],
        foreground=C["text_primary"],
        fieldbackground=C["bg_card"],
        rowheight=48,
        font=("Segoe UI", 12),
        borderwidth=0,
    )
    
    # Configure Headings
    s.configure("App.Treeview.Heading",
        background=C["glass_dark"],
        foreground=C["text_primary"],
        font=("Segoe UI", 11, "bold"),
        borderwidth=0,
        relief="flat",
        padding=(0, 12),
    )
    
    # Selection colors
    s.map("App.Treeview",
        background=[("selected", C["accent_blue"])],
        foreground=[("selected", "#FFFFFF")]
    )
    
    # Scrollbar styling
    s.configure("Vertical.TScrollbar",
        background=C["glass_border"],
        troughcolor=C["bg_dark"],
        borderwidth=0,
        arrowcolor=C["text_secondary"],
    )
    s.configure("Horizontal.TScrollbar",
        background=C["glass_border"],
        troughcolor=C["bg_dark"],
        borderwidth=0,
        arrowcolor=C["text_secondary"],
    )


# ============================================================
# GRAFIK CANVAS - Chart Drawing Functions
# ============================================================

class Chart:
    """Kumpulan fungsi statis untuk menggambar chart di Canvas tkinter."""

    @staticmethod
    def bar(canvas, data: list, colors: list = None,
            title: str = "", x_label: str = "", y_label: str = ""):
        """Bar chart horizontal."""
        canvas.delete("all")
        canvas.update_idletasks()
        W = canvas.winfo_width() or 400
        H = canvas.winfo_height() or 300

        if not data:
            canvas.create_text(W // 2, H // 2, text="Belum ada data",
                               fill=C["text_secondary"], font=F_KECIL)
            return

        PAD_L, PAD_R, PAD_T, PAD_B = 70, 24, 36, 48
        chart_w = W - PAD_L - PAD_R
        chart_h = H - PAD_T - PAD_B

        max_val = max(v for _, v in data) or 1
        n = len(data)
        gap = 6
        bar_h = max(10, (chart_h - gap * (n + 1)) // n)

        default_colors = [C["accent_blue"], C["success"], C["warning"], 
                          C["danger"], C["accent_purple"], C["accent_cyan"]] * 10
        colors = colors or default_colors

        # Title
        if title:
            canvas.create_text(PAD_L + chart_w // 2, 14, text=title,
                               font=("Segoe UI", 10, "bold"),
                               fill=C["text_primary"], anchor="center")

        # Grid lines
        grid_steps = 5
        for i in range(grid_steps + 1):
            gx = PAD_L + int(chart_w * i / grid_steps)
            gy1, gy2 = PAD_T, PAD_T + chart_h
            canvas.create_line(gx, gy1, gx, gy2,
                               fill=C["separator"], width=1, dash=(3, 3))
            val_label = int(max_val * i / grid_steps)
            canvas.create_text(gx, PAD_T + chart_h + 10,
                               text=str(val_label),
                               font=("Segoe UI", 8), fill=C["text_secondary"])

        # Bars
        for i, ((label, val), color) in enumerate(zip(data, colors)):
            y1 = PAD_T + gap + i * (bar_h + gap)
            y2 = y1 + bar_h
            bar_len = int(chart_w * val / max_val)

            # Background track
            canvas.create_rectangle(PAD_L, y1, PAD_L + chart_w, y2,
                                    fill=C["glass_dark"], outline="")
            # Bar
            if bar_len > 0:
                canvas.create_rectangle(PAD_L, y1, PAD_L + bar_len, y2,
                                        fill=color, outline="")
                # Rounded cap simulation
                canvas.create_oval(PAD_L + bar_len - 4, y1,
                                   PAD_L + bar_len + 4, y2,
                                   fill=color, outline="")

            # Label kiri
            canvas.create_text(PAD_L - 6, (y1 + y2) // 2,
                               text=label, font=("Segoe UI", 9),
                               fill=C["text_primary"], anchor="e")

            # Nilai di ujung bar
            if val > 0:
                canvas.create_text(PAD_L + bar_len + 8, (y1 + y2) // 2,
                                   text=str(val), font=("Segoe UI", 9, "bold"),
                                   fill=color, anchor="w")

    @staticmethod
    def column(canvas, data: list, colors: list = None, title: str = ""):
        """Column chart (bar vertikal)."""
        canvas.delete("all")
        canvas.update_idletasks()
        W = canvas.winfo_width() or 400
        H = canvas.winfo_height() or 300

        if not data:
            canvas.create_text(W // 2, H // 2, text="Belum ada data",
                               fill=C["text_secondary"], font=F_KECIL)
            return

        PAD_L, PAD_R, PAD_T, PAD_B = 40, 16, 36, 48
        chart_w = W - PAD_L - PAD_R
        chart_h = H - PAD_T - PAD_B

        max_val = max(v for _, v in data) or 1
        n = len(data)
        gap = 8
        bar_w = max(12, (chart_w - gap * (n + 1)) // n)

        default_colors = [C["accent_blue"], C["success"], C["warning"], 
                          C["danger"], C["accent_purple"], C["accent_cyan"]] * 10
        colors = colors or default_colors

        # Title
        if title:
            canvas.create_text(PAD_L + chart_w // 2, 14, text=title,
                               font=("Segoe UI", 10, "bold"),
                               fill=C["text_primary"], anchor="center")

        # Grid lines
        grid_steps = 4
        for i in range(grid_steps + 1):
            gy = PAD_T + chart_h - int(chart_h * i / grid_steps)
            canvas.create_line(PAD_L, gy, PAD_L + chart_w, gy,
                               fill=C["separator"], width=1, dash=(3, 3))
            val_label = int(max_val * i / grid_steps)
            canvas.create_text(PAD_L - 6, gy,
                               text=str(val_label),
                               font=("Segoe UI", 8), fill=C["text_secondary"],
                               anchor="e")

        # X axis
        canvas.create_line(PAD_L, PAD_T + chart_h,
                           PAD_L + chart_w, PAD_T + chart_h,
                           fill=C["glass_border"], width=1)

        for i, ((label, val), color) in enumerate(zip(data, colors)):
            x1 = PAD_L + gap + i * (bar_w + gap)
            x2 = x1 + bar_w
            bar_h_px = int(chart_h * val / max_val)
            y1 = PAD_T + chart_h - bar_h_px
            y2 = PAD_T + chart_h

            # Bar
            if bar_h_px > 0:
                canvas.create_rectangle(x1, y1, x2, y2,
                                        fill=color, outline="")

            # Label bawah
            canvas.create_text((x1 + x2) // 2, PAD_T + chart_h + 12,
                               text=label, font=("Segoe UI", 8),
                               fill=C["text_primary"], anchor="n")

            # Nilai di atas bar
            if val > 0:
                canvas.create_text((x1 + x2) // 2, y1 - 8,
                                   text=str(val),
                                   font=("Segoe UI", 8, "bold"),
                                   fill=color, anchor="s")

    @staticmethod
    def pie(canvas, data: list, colors: list = None, title: str = ""):
        """Pie chart."""
        canvas.delete("all")
        canvas.update_idletasks()
        W = canvas.winfo_width() or 400
        H = canvas.winfo_height() or 300

        total = sum(v for _, v in data if v > 0)
        if total == 0:
            canvas.create_text(W // 2, H // 2, text="Belum ada data",
                               fill=C["text_secondary"], font=F_KECIL)
            return

        default_colors = [C["accent_blue"], C["success"], C["warning"],
                          C["danger"], C["accent_purple"], C["accent_cyan"]] * 10
        colors = colors or default_colors

        cx = W * 0.38
        cy = H // 2
        r = min(cx - 20, H // 2 - 30)

        if title:
            canvas.create_text(W // 2, 14, text=title,
                               font=("Segoe UI", 10, "bold"),
                               fill=C["text_primary"], anchor="center")

        start = 0.0
        slices = [(label, val, color)
                  for (label, val), color in zip(data, colors)
                  if val > 0]

        for label, val, color in slices:
            extent = (val / total) * 360
            canvas.create_arc(cx - r, cy - r, cx + r, cy + r,
                              start=start, extent=extent,
                              fill=color, outline=C["bg_card"], width=2)
            start += extent

        # Legend kanan
        lx = cx * 2 + 16
        ly = H // 2 - len(slices) * 20
        for label, val, color in slices:
            pct = val / total * 100
            canvas.create_rectangle(lx, ly, lx + 14, ly + 14,
                                    fill=color, outline="")
            canvas.create_text(lx + 20, ly + 7,
                               text=f"{label}  {val} ({pct:.1f}%)",
                               font=("Segoe UI", 9), fill=C["text_primary"],
                               anchor="w")
            ly += 24

    @staticmethod
    def line(canvas, datasets: list, labels: list, title: str = ""):
        """Line chart multi-series."""
        canvas.delete("all")
        canvas.update_idletasks()
        W = canvas.winfo_width() or 400
        H = canvas.winfo_height() or 300

        all_vals = [v for _, _, vals in datasets for v in vals]
        if not all_vals:
            canvas.create_text(W // 2, H // 2, text="Belum ada data",
                               fill=C["text_secondary"], font=F_KECIL)
            return

        PAD_L, PAD_R, PAD_T, PAD_B = 50, 20, 36, 48
        chart_w = W - PAD_L - PAD_R
        chart_h = H - PAD_T - PAD_B

        max_val = max(all_vals) or 1
        min_val = 0
        n = len(labels)

        if title:
            canvas.create_text(PAD_L + chart_w // 2, 14, text=title,
                               font=("Segoe UI", 10, "bold"),
                               fill=C["text_primary"], anchor="center")

        # Grid
        grid_steps = 4
        for i in range(grid_steps + 1):
            gy = PAD_T + chart_h - int(chart_h * i / grid_steps)
            gval = min_val + (max_val - min_val) * i / grid_steps
            canvas.create_line(PAD_L, gy, PAD_L + chart_w, gy,
                               fill=C["separator"], width=1, dash=(3, 3))
            canvas.create_text(PAD_L - 6, gy,
                               text=f"{gval:.2f}",
                               font=("Segoe UI", 8), fill=C["text_secondary"],
                               anchor="e")

        # X labels
        if n > 1:
            for i, lbl in enumerate(labels):
                gx = PAD_L + int(chart_w * i / (n - 1))
                canvas.create_text(gx, PAD_T + chart_h + 12,
                                   text=lbl, font=("Segoe UI", 8),
                                   fill=C["text_secondary"])

        # Lines & dots
        for s_label, color, vals in datasets:
            if len(vals) < 2:
                continue
            points = []
            for i, v in enumerate(vals):
                gx = PAD_L + int(chart_w * i / (n - 1))
                gy = PAD_T + chart_h - int(chart_h * (v - min_val) / (max_val - min_val))
                points.append((gx, gy))

            # Line
            for i in range(len(points) - 1):
                x1, y1 = points[i]
                x2, y2 = points[i + 1]
                canvas.create_line(x1, y1, x2, y2, fill=color, width=2, smooth=True)

            # Dots
            for gx, gy in points:
                canvas.create_oval(gx - 4, gy - 4, gx + 4, gy + 4,
                                   fill=color, outline=C["bg_card"], width=2)

        # Legend
        lx = PAD_L + chart_w - 10
        ly = PAD_T + 6
        for s_label, color, _ in datasets:
            canvas.create_rectangle(lx - 90, ly, lx - 76, ly + 10,
                                    fill=color, outline="")
            canvas.create_text(lx - 70, ly + 5,
                               text=s_label, font=("Segoe UI", 8),
                               fill=C["text_primary"], anchor="w")
            ly += 18


# ============================================================
# SIDEBAR COMPONENT - macOS Settings Style
# ============================================================

class Sidebar(ctk.CTkFrame):
    """Modern sidebar navigation dengan macOS Settings aesthetic."""

    MENU = [
        ("Dashboard", "dashboard"),
        ("Data Mahasiswa", "mahasiswa"),
        ("Input Nilai", "nilai"),
        ("Statistik", "statistik"),
        ("Riwayat", "riwayat"),
    ]

    def __init__(self, parent, on_navigate):
        super().__init__(parent,
            width=240, corner_radius=0,
            fg_color=C["bg_sidebar"],
        )
        self.pack_propagate(False)
        self._nav = on_navigate
        self._btns = {}
        self._aktif = None
        self._build()

    def _build(self):
        # Logo section
        logo_frame = ctk.CTkFrame(self, fg_color="transparent")
        logo_frame.pack(fill="x", padx=20, pady=(28, 24))

        ctk.CTkLabel(logo_frame,
            text="✦ ARION",
            font=("Segoe UI", 22, "bold"),
            text_color="#FFFFFF",
        ).pack(anchor="w")
        
        ctk.CTkLabel(logo_frame,
            text="Student Portal",
            font=("Segoe UI", 10),
            text_color=C["accent_blue"],
        ).pack(anchor="w")

        # Separator
        ctk.CTkFrame(self, height=1, fg_color=C["separator"]).pack(fill="x", padx=16, pady=(8, 16))

        # Menu items
        menu_frame = ctk.CTkFrame(self, fg_color="transparent")
        menu_frame.pack(fill="x", padx=12, pady=8)

        icons = ["📊", "👨‍🎓", "📝", "📈", "📜"]
        
        for idx, (label, key) in enumerate(self.MENU):
            btn_frame = ctk.CTkFrame(menu_frame, fg_color="transparent")
            btn_frame.pack(fill="x", pady=2)
            
            b = ctk.CTkButton(
                btn_frame,
                text=f"  {icons[idx]}  {label}",
                anchor="w",
                width=210,
                height=44,
                font=("Segoe UI", 12),
                fg_color="transparent",
                hover_color=C["hover"],
                text_color=C["text_secondary"],
                corner_radius=10,
                command=lambda k=key: self._klik(k),
            )
            b.pack(fill="x")
            self._btns[key] = b

        # Logout button at bottom
        logout_frame = ctk.CTkFrame(self, fg_color="transparent")
        logout_frame.pack(side="bottom", fill="x", padx=12, pady=16)
        
        ctk.CTkButton(
            logout_frame,
            text="  🚪  Logout",
            anchor="w",
            width=210,
            height=44,
            font=("Segoe UI", 12),
            fg_color="transparent",
            hover_color=C["danger_bg"],
            text_color=C["danger"],
            corner_radius=10,
            command=lambda: self._nav("logout"),
        ).pack(fill="x")

    def _klik(self, key: str):
        for k, b in self._btns.items():
            b.configure(fg_color="transparent", text_color=C["text_secondary"], 
                       font=("Segoe UI", 12))
        if key in self._btns:
            self._btns[key].configure(
                fg_color=C["glass_light"],
                text_color="#FFFFFF",
                font=("Segoe UI", 12, "bold"),
            )
        self._aktif = key
        self._nav(key)

    def aktifkan(self, key: str):
        self._klik(key)


# ============================================================
# BASE PAGE CLASS
# ============================================================

class HalamanBase(ctk.CTkFrame):
    """Base class untuk semua halaman."""

    def __init__(self, parent):
        super().__init__(parent, corner_radius=0, fg_color=C["bg_dark"])

    def _header(self, judul: str, subjudul: str = ""):
        hdr = ctk.CTkFrame(self, fg_color=C["bg_header"], corner_radius=0, height=80)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        
        inner = ctk.CTkFrame(hdr, fg_color="transparent")
        inner.pack(side="left", padx=32, pady=16)
        
        ctk.CTkLabel(inner, text=judul, 
            font=("Segoe UI", 26, "bold"), 
            text_color=C["text_primary"]
        ).pack(anchor="w")
        
        if subjudul:
            ctk.CTkLabel(inner, text=subjudul, 
                font=("Segoe UI", 12), 
                text_color=C["text_secondary"]
            ).pack(anchor="w", pady=(4, 0))
        
        ctk.CTkFrame(self, height=1, fg_color=C["separator"]).pack(fill="x")

    def _card(self, parent, **kw):
        return ctk.CTkFrame(parent,
            fg_color=C["bg_card"],
            corner_radius=16,
            border_width=1,
            border_color=C["glass_border"],
            **kw
        )


# ============================================================
# DASHBOARD PAGE
# ============================================================

class HalamanDashboard(HalamanBase):

    def __init__(self, parent):
        super().__init__(parent)
        self._header("Dashboard", "Overview sistem akademik mahasiswa")
        self._build()

    def _build(self):
        # Stats cards row
        row1 = ctk.CTkFrame(self, fg_color="transparent")
        row1.pack(fill="x", padx=32, pady=(24, 16))

        self._cards = {}
        specs = [
            ("total", "Total Mahasiswa", C["accent_blue"], "👨‍🎓", "mahasiswa terdaftar"),
            ("sudah_nilai", "Sudah Input Nilai", C["success"], "✅", "mahasiswa"),
            ("rata_ipk", "Rata-rata IPK", C["warning"], "⭐", "dari 4.00"),
            ("belum_nilai", "Belum Input Nilai", C["danger"], "⏳", "mahasiswa"),
        ]
        
        for col, (key, label, warna, icon, satuan) in enumerate(specs):
            card = self._card(row1, height=140)
            card.grid(row=0, column=col, padx=8, sticky="nsew")
            card.grid_propagate(False)
            row1.columnconfigure(col, weight=1)

            # Gradient accent bar
            ctk.CTkFrame(card, width=6, fg_color=warna, corner_radius=0
                ).place(x=0, y=0, relheight=1)

            # Icon dan label
            ctk.CTkLabel(card, text=icon + "  " + label,
                font=("Segoe UI", 11), text_color=C["text_secondary"]
            ).place(x=24, y=18)

            # Value
            val_lbl = ctk.CTkLabel(card, text="0",
                font=("Segoe UI", 36, "bold"), text_color=warna)
            val_lbl.place(x=24, y=50)

            # Satuan
            ctk.CTkLabel(card, text=satuan,
                font=("Segoe UI", 9), text_color=C["text_muted"]
            ).place(x=26, y=110)

            self._cards[key] = val_lbl

        # Content area below stats
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=32, pady=(0, 24))

        # Left side - Top performers
        left_col = ctk.CTkFrame(content_frame, fg_color="transparent")
        left_col.pack(side="left", fill="both", expand=True)

        top_card = self._card(left_col)
        top_card.pack(fill="both", expand=True, pady=(0, 16))
        
        ctk.CTkLabel(top_card, text="🏆 Mahasiswa Berprestasi",
            font=("Segoe UI", 14, "bold"), text_color=C["text_primary"]
        ).pack(padx=20, pady=(16, 12))
        
        self._top_frame = ctk.CTkFrame(top_card, fg_color="transparent")
        self._top_frame.pack(fill="both", expand=True, padx=20, pady=(0, 16))

        # Right side - Grade distribution chart
        right_col = ctk.CTkFrame(content_frame, fg_color="transparent")
        right_col.pack(side="right", fill="both", expand=True, padx=(16, 0))

        chart_card = self._card(right_col)
        chart_card.pack(fill="both", expand=True)
        
        ctk.CTkLabel(chart_card, text="📊 Distribusi Nilai",
            font=("Segoe UI", 14, "bold"), text_color=C["text_primary"]
        ).pack(padx=20, pady=(16, 8))
        
        self._chart_canvas = ctk.Canvas(chart_card, 
            bg=C["bg_card"], 
            highlightthickness=0,
            width=400, 
            height=250
        )
        self._chart_canvas.pack(fill="both", expand=True, padx=20, pady=(0, 16))

    def refresh(self):
        stats = db.statistik()
        
        # Update stat cards
        self._cards["total"].configure(text=str(stats["total"]))
        self._cards["sudah_nilai"].configure(text=str(stats["sudah_nilai"]))
        self._cards["rata_ipk"].configure(text=f"{stats['rata_ipk']:.2f}")
        self._cards["belum_nilai"].configure(text=str(stats["total"] - stats["sudah_nilai"]))

        # Update top performers
        for w in self._top_frame.winfo_children():
            w.destroy()
        
        mhs_list = db.get_semua()
        if mhs_list:
            ipk_data = [(m["nama"], db.ipk_mahasiswa(m)) for m in mhs_list if m["semester"]]
            ipk_data.sort(key=lambda x: x[1], reverse=True)
            
            for i, (nama, ipk) in enumerate(ipk_data[:5]):
                row = ctk.CTkFrame(self._top_frame, fg_color=C["glass_dark"], corner_radius=10)
                row.pack(fill="x", pady=4)
                
                rank_colors = [C["warning"], C["accent_blue"], C["success"]]
                rank = f"#{i+1}"
                color = rank_colors[i] if i < 3 else C["text_muted"]
                
                ctk.CTkLabel(row, text=rank, 
                    font=("Segoe UI", 14, "bold"), 
                    text_color=color,
                    width=40, anchor="w"
                ).pack(side="left", padx=12, pady=10)
                
                ctk.CTkLabel(row, text=nama[:25], 
                    font=("Segoe UI", 11), 
                    text_color=C["text_primary"],
                    anchor="w"
                ).pack(side="left", padx=8, pady=10, fill="x", expand=True)
                
                ctk.CTkLabel(row, text=f"{ipk:.2f}", 
                    font=("Segoe UI", 12, "bold"), 
                    text_color=C["accent_blue"],
                    width=50, anchor="e"
                ).pack(side="right", padx=12, pady=10)

        # Update chart
        grade_dist = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0}
        for m in mhs_list:
            for smt in m.get("semester", {}).values():
                for mk in smt:
                    grade = mk.get("grade", "E")[0]
                    if grade in grade_dist:
                        grade_dist[grade] += 1
        
        chart_data = [(k, v) for k, v in grade_dist.items()]
        Chart.bar(self._chart_canvas, chart_data, title="")


# ============================================================
# MAHASISWA DATA PAGE
# ============================================================

class HalamanMahasiswa(HalamanBase):

    def __init__(self, parent, on_nilai):
        super().__init__(parent)
        self._on_nilai = on_nilai
        self._header("Data Mahasiswa", "Kelola data mahasiswa dan nilai")
        self._build()

    def _build(self):
        # Toolbar
        toolbar = ctk.CTkFrame(self, fg_color="transparent")
        toolbar.pack(fill="x", padx=32, pady=(20, 16))

        self._search_var = tk.StringVar()
        self._search_var.trace("w", lambda *args: self._cari())
        
        search_entry = ctk.CTkEntry(
            toolbar,
            placeholder_text="🔍 Cari NIM atau nama...",
            textvariable=self._search_var,
            width=320,
            height=44,
            corner_radius=12,
            border_width=1,
            border_color=C["input_border"],
            fg_color=C["input_bg"],
            text_color=C["text_primary"],
            font=("Segoe UI", 12),
        )
        search_entry.pack(side="left")

        ctk.CTkButton(
            toolbar,
            text="+ Tambah Mahasiswa",
            command=self._tambah_dialog,
            width=180,
            height=44,
            corner_radius=12,
            fg_color=C["accent_blue"],
            hover_color=_gelap(C["accent_blue"]),
            font=("Segoe UI", 12, "bold"),
        ).pack(side="right")

        # Table
        table_frame = self._card(self)
        table_frame.pack(fill="both", expand=True, padx=32, pady=(0, 24))

        columns = ("nim", "nama", "semester", "sks", "ipk", "aksi")
        self._tree = ttk.Treeview(table_frame, columns=columns, show="headings", 
                                   style="App.Treeview")
        
        self._tree.heading("nim", text="NIM")
        self._tree.heading("nama", text="Nama Lengkap")
        self._tree.heading("semester", text="Semester Terisi")
        self._tree.heading("sks", text="Total SKS")
        self._tree.heading("ipk", text="IPK")
        self._tree.heading("aksi", text="Aksi")
        
        self._tree.column("nim", width=140)
        self._tree.column("nama", width=280)
        self._tree.column("semester", width=150)
        self._tree.column("sks", width=80, anchor="center")
        self._tree.column("ipk", width=80, anchor="center")
        self._tree.column("aksi", width=180, anchor="center")

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self._tree.yview)
        self._tree.configure(yscrollcommand=vsb.set)

        self._tree.pack(side="left", fill="both", expand=True, padx=4, pady=4)
        vsb.pack(side="right", fill="y", pady=4)

    def _cari(self):
        keyword = self._search_var.get()
        for item in self._tree.get_children():
            self._tree.delete(item)
        
        results = db.cari(keyword) if keyword else db.get_semua()
        for m in results:
            ipk = db.ipk_mahasiswa(m)
            sks = db.total_sks(m)
            semester = db.semester_terisi(m)
            
            item_id = self._tree.insert("", "end", values=(
                m["nim"], m["nama"], semester, sks, f"{ipk:.2f}", ""
            ))
            
            # Add action buttons
            btn_frame = ctk.CTkFrame(self._tree, fg_color="transparent")
            btn_frame.pack(padx=4, pady=4)
            
            ctk.CTkButton(btn_frame, text="Nilai", width=60, height=28,
                fg_color=C["accent_blue"], corner_radius=8,
                font=("Segoe UI", 9),
                command=lambda nim=m["nim"]: self._on_nilai(nim)
            ).pack(side="left", padx=2)
            
            ctk.CTkButton(btn_frame, text="Edit", width=50, height=28,
                fg_color=C["warning"], corner_radius=8,
                font=("Segoe UI", 9),
                command=lambda nim=m["nim"], nama=m["nama"]: self._edit_dialog(nim, nama)
            ).pack(side="left", padx=2)
            
            ctk.CTkButton(btn_frame, text="Hapus", width=50, height=28,
                fg_color=C["danger"], corner_radius=8,
                font=("Segoe UI", 9),
                command=lambda nim=m["nim"]: self._hapus(nim)
            ).pack(side="left", padx=2)

    def _tambah_dialog(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Tambah Mahasiswa")
        dialog.geometry("420x320")
        dialog.configure(fg_color=C["bg_dark"])
        
        # Center dialog
        dialog.transient(self)
        dialog.grab_set()
        
        card = ctk.CTkFrame(dialog, fg_color=C["bg_card"], corner_radius=16)
        card.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(card, text="Tambah Mahasiswa Baru",
            font=("Segoe UI", 18, "bold"), text_color=C["text_primary"]
        ).pack(pady=(20, 8))
        
        ctk.CTkLabel(card, text="Masukkan data mahasiswa di bawah ini",
            font=("Segoe UI", 11), text_color=C["text_secondary"]
        ).pack(pady=(0, 24))
        
        ctk.CTkLabel(card, text="NIM", font=("Segoe UI", 11),
            text_color=C["text_secondary"], anchor="w"
        ).pack(fill="x", padx=32)
        e_nim = _entry(card, placeholder="Masukkan NIM", width=360)
        e_nim.pack(padx=32, pady=(4, 16))
        
        ctk.CTkLabel(card, text="Nama Lengkap", font=("Segoe UI", 11),
            text_color=C["text_secondary"], anchor="w"
        ).pack(fill="x", padx=32)
        e_nama = _entry(card, placeholder="Masukkan nama lengkap", width=360)
        e_nama.pack(padx=32, pady=(4, 24))
        
        _bind_enter_chain([e_nim, e_nama])
        
        def simpan():
            try:
                db.tambah_mahasiswa(e_nim.get(), e_nama.get())
                dialog.destroy()
                self.refresh()
                messagebox.showinfo("Berhasil", "Mahasiswa berhasil ditambahkan!")
            except ValueError as ve:
                messagebox.showerror("Error", str(ve))
        
        btn_frame = ctk.CTkFrame(card, fg_color="transparent")
        btn_frame.pack(pady=(0, 24))
        
        _btn(btn_frame, "Simpan", simpan, width=140).pack(side="left", padx=16)
        _btn_ghost(btn_frame, "Batal", dialog.destroy, width=140).pack(side="left")
        
        e_nim.focus_set()

    def _edit_dialog(self, nim, nama_lama):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Edit Mahasiswa")
        dialog.geometry("420x280")
        dialog.configure(fg_color=C["bg_dark"])
        
        dialog.transient(self)
        dialog.grab_set()
        
        card = ctk.CTkFrame(dialog, fg_color=C["bg_card"], corner_radius=16)
        card.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(card, text="Edit Data Mahasiswa",
            font=("Segoe UI", 18, "bold"), text_color=C["text_primary"]
        ).pack(pady=(20, 8))
        
        ctk.CTkLabel(card, text=f"NIM: {nim}", font=("Segoe UI", 11),
            text_color=C["accent_blue"]
        ).pack(pady=(0, 16))
        
        ctk.CTkLabel(card, text="Nama Lengkap", font=("Segoe UI", 11),
            text_color=C["text_secondary"], anchor="w"
        ).pack(fill="x", padx=32)
        e_nama = _entry(card, placeholder="Nama lengkap", width=360)
        e_nama.insert(0, nama_lama)
        e_nama.pack(padx=32, pady=(4, 24))
        
        def update():
            try:
                db.edit_mahasiswa(nim, e_nama.get())
                dialog.destroy()
                self.refresh()
                messagebox.showinfo("Berhasil", "Data berhasil diperbarui!")
            except ValueError as ve:
                messagebox.showerror("Error", str(ve))
        
        btn_frame = ctk.CTkFrame(card, fg_color="transparent")
        btn_frame.pack()
        
        _btn(btn_frame, "Update", update, width=140).pack(side="left", padx=16)
        _btn_ghost(btn_frame, "Batal", dialog.destroy, width=140).pack(side="left")
        
        e_nama.focus_set()
        e_nama.icursor(tk.END)

    def _hapus(self, nim):
        if messagebox.askyesno("Konfirmasi", "Yakin ingin menghapus mahasiswa ini?"):
            try:
                db.hapus_mahasiswa(nim)
                self.refresh()
                messagebox.showinfo("Berhasil", "Mahasiswa berhasil dihapus!")
            except ValueError as ve:
                messagebox.showerror("Error", str(ve))

    def refresh(self):
        self._cari()


# ============================================================
# NILAI INPUT PAGE
# ============================================================

class HalamanNilai(HalamanBase):

    def __init__(self, parent, on_selesai):
        super().__init__(parent)
        self._on_selesai = on_selesai
        self._nim_aktif = None
        self._header("Input Nilai", "Masukkan nilai mahasiswa per semester")
        self._build()

    def _build(self):
        # Info panel
        info_card = self._card(self)
        info_card.pack(fill="x", padx=32, pady=20)
        
        info_inner = ctk.CTkFrame(info_card, fg_color="transparent")
        info_inner.pack(fill="x", padx=24, pady=20)
        
        self._lbl_info = ctk.CTkLabel(info_inner, text="-",
            font=("Segoe UI", 14), text_color=C["text_primary"]
        )
        self._lbl_info.pack(anchor="w")
        
        # Semester selector
        sel_frame = ctk.CTkFrame(self, fg_color="transparent")
        sel_frame.pack(fill="x", padx=32, pady=(0, 16))
        
        ctk.CTkLabel(sel_frame, text="Pilih Semester:",
            font=("Segoe UI", 12), text_color=C["text_secondary"]
        ).pack(side="left", padx=4)
        
        self._sem_var = tk.StringVar(value="1")
        sem_options = ["1", "2", "3", "4", "5", "6"]
        
        for sem in sem_options:
            rb = ctk.CTkRadioButton(
                sel_frame,
                text=f"Smt {sem}",
                variable=self._sem_var,
                value=sem,
                command=self._load_form,
                fg_color=C["accent_blue"],
            )
            rb.pack(side="left", padx=8)

        # Form container
        self._form_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self._form_frame.pack(fill="both", expand=True, padx=32, pady=(0, 24))

        # Action buttons
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=32, pady=(0, 24))
        
        _btn(btn_frame, "💾 Simpan Nilai", self._simpan, 
            width=160, color=C["success"]
        ).pack(side="left")
        
        _btn_ghost(btn_frame, "← Kembali", self._kembali, width=140).pack(side="left", padx=12)

    def set_nim(self, nim: str):
        self._nim_aktif = nim
        mhs = next((m for m in db.get_semua() if m["nim"] == nim), None)
        if mhs:
            self._lbl_info.configure(text=f"{mhs['nama']} ({mhs['nim']})")
        self._load_form()

    def _load_form(self):
        for w in self._form_frame.winfo_children():
            w.destroy()
        
        if not self._nim_aktif:
            ctk.CTkLabel(self._form_frame, text="Pilih mahasiswa terlebih dahulu",
                font=("Segoe UI", 13), text_color=C["text_secondary"]
            ).pack(pady=40)
            return
        
        semester = int(self._sem_var.get())
        if semester not in db.KURIKULUM:
            return
        
        matkul_list = db.KURIKULUM[semester]
        mhs = next((m for m in db.get_semua() if m["nim"] == self._nim_aktif), None)
        
        # Load existing values if any
        existing = {}
        if mhs and str(semester) in mhs.get("semester", {}):
            for mk in mhs["semester"][str(semester)]:
                existing[mk["nama"]] = mk["nilai"]
        
        self._entries = {}
        
        for idx, (nama_mk, sks) in enumerate(matkul_list):
            row = self._card(self._form_frame)
            row.pack(fill="x", pady=6)
            
            ctk.CTkLabel(row, text=f"{idx+1}.",
                font=("Segoe UI", 12), text_color=C["text_muted"],
                width=30, anchor="w"
            ).pack(side="left", padx=(16, 8), pady=14)
            
            info_frame = ctk.CTkFrame(row, fg_color="transparent")
            info_frame.pack(side="left", fill="x", expand=True, pady=12)
            
            ctk.CTkLabel(info_frame, text=nama_mk,
                font=("Segoe UI", 12, "bold"), text_color=C["text_primary"],
                anchor="w"
            ).pack(anchor="w")
            
            ctk.CTkLabel(info_frame, text=f"{sks} SKS",
                font=("Segoe UI", 10), text_color=C["text_muted"],
                anchor="w"
            ).pack(anchor="w")
            
            entry = _entry(row, placeholder="0-100", width=100)
            if nama_mk in existing:
                entry.insert(0, str(int(existing[nama_mk])))
            entry.pack(side="right", padx=(0, 16), pady=12)
            
            self._entries[nama_mk] = entry

    def _simpan(self):
        if not self._nim_aktif:
            messagebox.showwarning("Peringatan", "Pilih mahasiswa terlebih dahulu!")
            return
        
        semester = int(self._sem_var.get())
        matkul_list = db.KURIKULUM[semester]
        
        try:
            nilai_list = []
            for nama_mk, _ in matkul_list:
                entry = self._entries.get(nama_mk)
                if entry:
                    val_str = entry.get().strip()
                    if not val_str:
                        raise ValueError(f"Nilai untuk {nama_mk} belum diisi!")
                    nilai = float(val_str)
                    if not (0 <= nilai <= 100):
                        raise ValueError(f"Nilai harus antara 0-100 untuk {nama_mk}")
                    nilai_list.append(nilai)
            
            db.simpan_nilai(self._nim_aktif, semester, nilai_list)
            self._on_selesai()
            messagebox.showinfo("Berhasil", "Nilai berhasil disimpan!")
        except ValueError as ve:
            messagebox.showerror("Error", str(ve))

    def _kembali(self):
        self._nim_aktif = None
        self._lbl_info.configure(text="-")
        self._load_form()
        self._on_selesai()


# ============================================================
# STATISTIK PAGE
# ============================================================

class HalamanStatistik(HalamanBase):

    def __init__(self, parent):
        super().__init__(parent)
        self._header("Statistik", "Analisis data akademik")
        self._build()

    def _build(self):
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=32, pady=24)

        # Top row - 2 charts
        top_row = ctk.CTkFrame(content, fg_color="transparent")
        top_row.pack(fill="both", expand=True)

        # Left - Grade distribution
        left_card = self._card(top_row)
        left_card.pack(side="left", fill="both", expand=True, padx=(0, 8))
        
        ctk.CTkLabel(left_card, text="📊 Distribusi Grade",
            font=("Segoe UI", 14, "bold"), text_color=C["text_primary"]
        ).pack(padx=20, pady=(16, 8))
        
        self._canvas_grade = ctk.Canvas(left_card, 
            bg=C["bg_card"], highlightthickness=0)
        self._canvas_grade.pack(fill="both", expand=True, padx=20, pady=(0, 16))

        # Right - Semester distribution
        right_card = self._card(top_row)
        right_card.pack(side="right", fill="both", expand=True, padx=(8, 0))
        
        ctk.CTkLabel(right_card, text="📈 Mahasiswa per Semester",
            font=("Segoe UI", 14, "bold"), text_color=C["text_primary"]
        ).pack(padx=20, pady=(16, 8))
        
        self._canvas_sem = ctk.Canvas(right_card, 
            bg=C["bg_card"], highlightthickness=0)
        self._canvas_sem.pack(fill="both", expand=True, padx=20, pady=(0, 16))

        # Bottom - Pie chart
        bottom_card = self._card(content)
        bottom_card.pack(fill="both", expand=True, pady=(16, 0))
        
        ctk.CTkLabel(bottom_card, text="🥧 Komposisi Kelulusan",
            font=("Segoe UI", 14, "bold"), text_color=C["text_primary"]
        ).pack(padx=20, pady=(16, 8))
        
        self._canvas_pie = ctk.Canvas(bottom_card, 
            bg=C["bg_card"], highlightthickness=0, height=280)
        self._canvas_pie.pack(fill="both", expand=True, padx=20, pady=(0, 16))

    def refresh(self):
        mhs_list = db.get_semua()
        
        # Grade distribution
        grade_dist = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0}
        for m in mhs_list:
            for smt in m.get("semester", {}).values():
                for mk in smt:
                    grade = mk.get("grade", "E")[0]
                    if grade in grade_dist:
                        grade_dist[grade] += 1
        
        Chart.bar(self._canvas_grade, [(k, v) for k, v in grade_dist.items()])

        # Semester distribution
        sem_count = {str(i): 0 for i in range(1, 7)}
        for m in mhs_list:
            for sem in m.get("semester", {}).keys():
                if sem in sem_count:
                    sem_count[sem] += 1
        
        Chart.column(self._canvas_sem, [(f"Smt {k}", v) for k, v in sem_count.items()])

        # Pass rate pie chart
        lulus = sum(1 for m in mhs_list if db.ipk_mahasiswa(m) >= 2.0)
        tidak_lulus = len(mhs_list) - lulus
        
        Chart.pie(self._canvas_pie, [
            ("Lulus", lulus),
            ("Tidak Lulus", tidak_lulus)
        ])


# ============================================================
# RIWAYAT PAGE
# ============================================================

class HalamanRiwayat(HalamanBase):

    def __init__(self, parent):
        super().__init__(parent)
        self._header("Riwayat Aktivitas", "Log aktivitas sistem")
        self._build()

    def _build(self):
        table_card = self._card(self)
        table_card.pack(fill="both", expand=True, padx=32, pady=24)

        columns = ("waktu", "aksi", "detail")
        self._tree = ttk.Treeview(table_card, columns=columns, show="headings",
                                   style="App.Treeview")
        
        self._tree.heading("waktu", text="Waktu")
        self._tree.heading("aksi", text="Aksi")
        self._tree.heading("detail", text="Detail")
        
        self._tree.column("waktu", width=160)
        self._tree.column("aksi", width=120)
        self._tree.column("detail", width=600)

        vsb = ttk.Scrollbar(table_card, orient="vertical", command=self._tree.yview)
        self._tree.configure(yscrollcommand=vsb.set)

        self._tree.pack(side="left", fill="both", expand=True, padx=4, pady=4)
        vsb.pack(side="right", fill="y", pady=4)

    def refresh(self):
        for item in self._tree.get_children():
            self._tree.delete(item)
        
        riwayat = db.get_riwayat()
        for r in riwayat:
            self._tree.insert("", "end", values=(
                r["waktu"], r["aksi"], r["detail"]
            ))


# ============================================================
# LOGIN PAGE - Modern Glass Card Design
# ============================================================

class HalamanLogin(ctk.CTkFrame):

    def __init__(self, parent, on_login):
        super().__init__(parent, fg_color=C["bg_dark"])
        self._on_login = on_login
        self._build()

    def _build(self):
        # Background gradient effect using layered frames
        gradient_top = ctk.CTkFrame(self, fg_color=C["accent_blue"], height=4)
        gradient_top.pack(fill="x")
        
        gradient_mid = ctk.CTkFrame(self, fg_color=C["accent_purple"], height=4)
        gradient_mid.pack(fill="x")
        
        gradient_bot = ctk.CTkFrame(self, fg_color=C["accent_pink"], height=4)
        gradient_bot.pack(fill="x")

        # Main content
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True)

        # Login card
        card = ctk.CTkFrame(main_frame,
            fg_color=C["bg_card"],
            corner_radius=24,
            border_width=1,
            border_color=C["glass_border"],
        )
        card.place(relx=0.5, rely=0.5, anchor="center", width=420, height=520)

        # Logo/icon
        ctk.CTkLabel(card, text="✦",
            font=("Segoe UI", 48), text_color=C["accent_blue"]
        ).place(relx=0.5, rely=0.15, anchor="center")

        ctk.CTkLabel(card, text="ARION",
            font=("Segoe UI", 28, "bold"), text_color=C["text_primary"]
        ).place(relx=0.5, rely=0.24, anchor="center")

        ctk.CTkLabel(card,
            text="Student Portal\nAutomation Robotics Information Online Network",
            font=("Segoe UI", 11), text_color=C["text_secondary"],
            justify="center"
        ).place(relx=0.5, rely=0.32, anchor="center")

        # Form fields
        form_y = 0.42
        
        ctk.CTkLabel(card, text="Username",
            font=("Segoe UI", 11), text_color=C["text_secondary"]
        ).place(relx=0.15, rely=form_y, anchor="w")
        
        self._e_user = _entry(card, placeholder="admin", width=300)
        self._e_user.place(relx=0.15, rely=form_y + 0.05, anchor="w")

        ctk.CTkLabel(card, text="Password",
            font=("Segoe UI", 11), text_color=C["text_secondary"]
        ).place(relx=0.15, rely=form_y + 0.13, anchor="w")
        
        self._e_pass = _entry(card, placeholder="••••", show="*", width=300)
        self._e_pass.place(relx=0.15, rely=form_y + 0.18, anchor="w")

        _bind_enter_chain([self._e_user, self._e_pass])
        self._e_pass.bind("<Return>", lambda e: self._login())

        # Login button
        login_btn = ctk.CTkButton(card,
            text="Masuk ke Sistem",
            command=self._login,
            width=300,
            height=48,
            corner_radius=12,
            fg_color=C["accent_blue"],
            hover_color=_gelap(C["accent_blue"]),
            font=("Segoe UI", 13, "bold"),
        )
        login_btn.place(relx=0.15, rely=form_y + 0.32, anchor="w")

        # Error label
        self._lbl_err = ctk.CTkLabel(card, text="",
            font=("Segoe UI", 10), text_color=C["danger"]
        )
        self._lbl_err.place(relx=0.15, rely=form_y + 0.43, anchor="w")

        self._e_user.focus_set()

    def _login(self):
        u = self._e_user.get().strip()
        p = self._e_pass.get()
        if db.cek_login(u, p):
            self._on_login()
        else:
            self._lbl_err.configure(text="⚠ Username atau password salah.")


# ============================================================
# MAIN APPLICATION CLASS
# ============================================================

class App(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("ARION - Student Portal")
        self.geometry("1366x768")
        self.minsize(1100, 700)
        self.configure(fg_color=C["bg_dark"])
        
        _style_tree()
        self._tampil_login()

    def _tampil_login(self):
        self._bersih()
        HalamanLogin(self, self._setelah_login).pack(fill="both", expand=True)

    def _setelah_login(self):
        self._bersih()
        self._bangun_shell()
        self._sidebar.aktifkan("dashboard")

    def _bangun_shell(self):
        self._sidebar = Sidebar(self, self._navigasi)
        self._sidebar.pack(side="left", fill="y")

        self._area = ctk.CTkFrame(self, corner_radius=0, fg_color=C["bg_dark"])
        self._area.pack(side="left", fill="both", expand=True)

        self._dash = HalamanDashboard(self._area)
        self._mhs = HalamanMahasiswa(self._area, on_nilai=self._buka_nilai)
        self._nilai = HalamanNilai(self._area, on_selesai=self._selesai_nilai)
        self._statistik = HalamanStatistik(self._area)
        self._riwayat = HalamanRiwayat(self._area)

        self._halaman_aktif = None

    def _navigasi(self, key: str):
        if key == "logout":
            if messagebox.askyesno("Logout", "Yakin ingin keluar dari sistem?"):
                self._tampil_login()
            return

        mapping = {
            "dashboard": self._dash,
            "mahasiswa": self._mhs,
            "nilai": self._nilai,
            "statistik": self._statistik,
            "riwayat": self._riwayat,
        }

        target = mapping.get(key)
        if not target or target is self._halaman_aktif:
            return

        if self._halaman_aktif:
            self._halaman_aktif.pack_forget()

        target.pack(fill="both", expand=True)
        self._halaman_aktif = target

        if key == "dashboard":
            self._dash.refresh()
        if key == "mahasiswa":
            self._mhs.refresh()
        if key == "statistik":
            self._statistik.refresh()
        if key == "riwayat":
            self._riwayat.refresh()

    def _buka_nilai(self, nim: str):
        self._sidebar.aktifkan("nilai")
        self._nilai.set_nim(nim)

    def _selesai_nilai(self):
        self._dash.refresh()
        self._mhs.refresh()

    def _bersih(self):
        for w in self.winfo_children():
            w.destroy()
