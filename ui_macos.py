# ============================================================
# ui.py  —  GUI Utama (macOS Sonoma Inspired Design)
# Sistem Informasi Akademik Mahasiswa
# CustomTkinter — Dark Mode Glassmorphism Theme
# ============================================================

import customtkinter as ctk
from tkinter import messagebox, ttk
import tkinter as tk
import db
import math
import random

# ============================================================
# TEMA - macOS Sonoma Dark Mode dengan Glassmorphism
# ============================================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Color Palette - Deep Navy/Purple/Blue/Pink Gradient Theme
C = {
    # Background gradients
    "bg_dark":       "#0a0e1a",        # Deep navy black
    "bg_gradient_1": "#0f1428",        # Dark navy
    "bg_gradient_2": "#1a1035",        # Deep purple
    "bg_gradient_3": "#0d1b3e",        # Navy blue
    
    # Glass panels
    "glass_bg":      "rgba(30, 35, 60, 0.65)",
    "glass_light":   "rgba(50, 55, 90, 0.45)",
    "glass_dark":    "rgba(20, 25, 45, 0.75)",
    "glass_border":  "rgba(100, 120, 180, 0.25)",
    
    # Accent colors
    "accent_blue":   "#3B82F6",        # Primary blue
    "accent_purple": "#8B5CF6",        # Purple
    "accent_pink":   "#EC4899",        # Pink accent
    "accent_cyan":   "#06B6D4",        # Cyan
    "accent_green":  "#10B981",        # Green
    "accent_yellow": "#F59E0B",        # Yellow/Orange
    "accent_red":    "#EF4444",        # Red
    
    # Text colors
    "text_primary":  "#F8FAFC",        # White-ish
    "text_secondary":"#94A3B8",        # Gray blue
    "text_muted":    "#64748B",        # Muted gray
    "text_glow":     "rgba(255,255,255,0.15)",
    
    # Status colors
    "success":       "#10B981",
    "warning":       "#F59E0B",
    "error":         "#EF4444",
    "info":          "#3B82F6",
}

# Typography - Modern SF Pro / Inter style
F_TITULO    = ("Inter", 28, "bold")
F_JUDUL     = ("Inter", 20, "bold")
F_SUBJUDUL  = ("Inter", 14, "semibold")
F_NORMAL    = ("Inter", 12)
F_SMALL     = ("Inter", 10)
F_TINY      = ("Inter", 9)
F_MONO      = ("JetBrains Mono", 10)

# Try to use system fonts if available
try:
    from tkinter import font
    available_fonts = font.families()
    if "SF Pro Display" in available_fonts:
        F_TITULO    = ("SF Pro Display", 28, "bold")
        F_JUDUL     = ("SF Pro Display", 20, "bold")
        F_SUBJUDUL  = ("SF Pro Display", 14, "bold")
        F_NORMAL    = ("SF Pro Display", 12)
        F_SMALL     = ("SF Pro Display", 10)
        F_TINY      = ("SF Pro Display", 9)
    elif "Inter" in available_fonts:
        pass  # Already using Inter
    else:
        # Fallback to Segoe UI or Helvetica
        F_TITULO    = ("Segoe UI", 28, "bold")
        F_JUDUL     = ("Segoe UI", 20, "bold")
        F_SUBJUDUL  = ("Segoe UI", 14, "bold")
        F_NORMAL    = ("Segoe UI", 12)
        F_SMALL     = ("Segoe UI", 10)
        F_TINY      = ("Segoe UI", 9)
except:
    pass

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def hex_to_rgba(hex_color: str, alpha: float = 1.0) -> str:
    """Convert hex color to rgba string for transparency effects."""
    try:
        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)
        return f"rgba({r}, {g}, {b}, {alpha})"
    except:
        return hex_color

def lighten(hex_color: str, factor: float = 0.2) -> str:
    """Lighten a hex color by a factor."""
    try:
        r = min(255, int(int(hex_color[1:3], 16) * (1 + factor)))
        g = min(255, int(int(hex_color[3:5], 16) * (1 + factor)))
        b = min(255, int(int(hex_color[5:7], 16) * (1 + factor)))
        return f"#{r:02x}{g:02x}{b:02x}"
    except:
        return hex_color

def darken(hex_color: str, factor: float = 0.2) -> str:
    """Darken a hex color by a factor."""
    try:
        r = max(0, int(int(hex_color[1:3], 16) * (1 - factor)))
        g = max(0, int(int(hex_color[3:5], 16) * (1 - factor)))
        b = max(0, int(int(hex_color[5:7], 16) * (1 - factor)))
        return f"#{r:02x}{g:02x}{b:02x}"
    except:
        return hex_color

def gradient_hex(color1: str, color2: str, factor: float = 0.5) -> str:
    """Create gradient between two colors."""
    try:
        r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
        r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)
        r = int(r1 + (r2 - r1) * factor)
        g = int(g1 + (g2 - g1) * factor)
        b = int(b1 + (b2 - b1) * factor)
        return f"#{r:02x}{g:02x}{b:02x}"
    except:
        return color1

# ============================================================
# ANIMATED BUTTON WITH HOVER EFFECTS
# ============================================================

class GlassButton(ctk.CTkButton):
    """Modern glassmorphic button with smooth hover animations."""
    
    def __init__(self, parent, text="", command=None, 
                 fg_color=None, hover_color=None,
                 width=140, height=42, corner_radius=12,
                 font=None, text_color=None,
                 border_width=1, border_color=None,
                 glow=False, **kwargs):
        
        self._glow = glow
        self._original_fg = fg_color or C["accent_blue"]
        self._hover_fg = hover_color or lighten(self._original_fg, 0.15)
        
        super().__init__(
            parent,
            text=text,
            command=command,
            width=width,
            height=height,
            corner_radius=corner_radius,
            font=font or F_NORMAL,
            text_color=text_color or "#FFFFFF",
            fg_color=self._original_fg,
            hover_color=self._hover_fg,
            border_width=border_width,
            border_color=border_color or "transparent",
            **kwargs
        )
        
        # Bind hover events for glow effect
        if glow:
            self.bind("<Enter>", self._on_enter)
            self.bind("<Leave>", self._on_leave)
    
    def _on_enter(self, event):
        if self._glow:
            self.configure(border_color=C["text_glow"], border_width=2)
    
    def _on_leave(self, event):
        if self._glow:
            self.configure(border_color="transparent", border_width=1)


# ============================================================
# GLASS CARD COMPONENT
# ============================================================

class GlassCard(ctk.CTkFrame):
    """Frosted glass card with subtle border and shadow effect."""
    
    def __init__(self, parent, width=None, height=None,
                 bg_color=None, border_color=None,
                 corner_radius=16, **kwargs):
        
        super().__init__(
            parent,
            width=width,
            height=height,
            corner_radius=corner_radius,
            fg_color=bg_color or "rgba(30, 35, 60, 0.5)",
            border_width=1,
            border_color=border_color or "rgba(100, 120, 180, 0.2)",
            **kwargs
        )
        
        # Add subtle inner glow on hover
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self._original_border = border_color or "rgba(100, 120, 180, 0.2)"
    
    def _on_enter(self, event):
        self.configure(border_color="rgba(150, 170, 220, 0.4)")
    
    def _on_leave(self, event):
        self.configure(border_color=self._original_border)


# ============================================================
# SIDEBAR NAVIGATION - macOS Settings Style
# ============================================================

class Sidebar(ctk.CTkFrame):
    """Modern sidebar navigation like macOS Settings."""

    MENU = [
        ("Dashboard",       "dashboard", "🏠"),
        ("Data Mahasiswa",  "mahasiswa", "👥"),
        ("Input Nilai",     "nilai", "📝"),
        ("Statistik",       "statistik", "📊"),
        ("Riwayat",         "riwayat", "📜"),
    ]

    def __init__(self, parent, on_navigate):
        super().__init__(parent,
            width=260, corner_radius=0,
            fg_color="rgba(15, 20, 40, 0.85)",
        )
        self.pack_propagate(False)
        self._nav = on_navigate
        self._btns = {}
        self._aktif = None
        self._build()

    def _build(self):
        # Logo section with gradient glow
        logo_frame = ctk.CTkFrame(self, fg_color="transparent")
        logo_frame.pack(fill="x", padx=24, pady=(32, 20))

        # App name with gradient effect
        logo_label = ctk.CTkLabel(logo_frame,
            text="✦ ARION",
            font=("Inter", 24, "bold"),
            text_color="#FFFFFF",
        )
        logo_label.pack(anchor="w")
        
        # Subtitle
        subtitle = ctk.CTkLabel(logo_frame,
            text="Student Portal",
            font=("Inter", 11),
            text_color=C["text_muted"],
        )
        subtitle.pack(anchor="w", pady=(0, 8))

        # Separator with gradient
        separator = ctk.CTkFrame(self, height=1, 
            fg_color="rgba(100, 120, 180, 0.3)")
        separator.pack(fill="x", padx=20, pady=(8, 16))

        # Navigation menu
        menu_frame = ctk.CTkFrame(self, fg_color="transparent")
        menu_frame.pack(fill="x", padx=16, pady=8)

        for label, key, icon in self.MENU:
            btn = ctk.CTkButton(
                menu_frame,
                text=f"  {icon}  {label}",
                anchor="w",
                width=220,
                height=44,
                font=("Inter", 12),
                fg_color="transparent",
                hover_color="rgba(60, 70, 110, 0.5)",
                text_color=C["text_secondary"],
                corner_radius=12,
                command=lambda k=key: self._klik(k),
            )
            btn.pack(fill="x", pady=3)
            self._btns[key] = btn

        # Bottom section - Logout
        bottom_sep = ctk.CTkFrame(self, height=1,
            fg_color="rgba(100, 120, 180, 0.3)")
        bottom_sep.pack(fill="x", padx=20, pady=(12, 8))

        logout_btn = ctk.CTkButton(
            self,
            text="  🚪  Logout",
            anchor="w",
            width=220,
            height=44,
            font=("Inter", 12),
            fg_color="transparent",
            hover_color="rgba(100, 40, 40, 0.5)",
            text_color="#F87171",
            corner_radius=12,
            command=lambda: self._nav("logout"),
        )
        logout_btn.pack(side="bottom", padx=16, pady=(0, 20), fill="x")

    def _klik(self, key: str):
        # Reset all buttons
        for k, b in self._btns.items():
            b.configure(
                fg_color="transparent", 
                text_color=C["text_secondary"],
                font=("Inter", 12)
            )
        
        # Highlight active button
        if key in self._btns:
            self._btns[key].configure(
                fg_color="rgba(60, 80, 140, 0.6)",
                text_color="#FFFFFF",
                font=("Inter", 12, "bold"),
            )
        
        self._aktif = key
        self._nav(key)

    def aktifkan(self, key: str):
        self._klik(key)


# ============================================================
# BASE PAGE CLASS
# ============================================================

class HalamanBase(ctk.CTkFrame):
    """Base class for all pages with consistent styling."""

    def __init__(self, parent):
        super().__init__(parent, corner_radius=0, 
            fg_color="transparent")

    def _header(self, judul: str, subjudul: str = ""):
        """Create page header with elegant typography."""
        hdr = ctk.CTkFrame(self, fg_color="transparent", 
            corner_radius=0, height=80)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        
        inner = ctk.CTkFrame(hdr, fg_color="transparent")
        inner.pack(side="left", padx=36, pady=16)
        
        ctk.CTkLabel(inner, text=judul, 
            font=F_JUDUL, 
            text_color=C["text_primary"]
        ).pack(anchor="w")
        
        if subjudul:
            ctk.CTkLabel(inner, text=subjudul, 
                font=F_SMALL, 
                text_color=C["text_muted"]
            ).pack(anchor="w", pady=(4, 0))
        
        # Bottom separator
        sep = ctk.CTkFrame(self, height=1, 
            fg_color="rgba(100, 120, 180, 0.2)")
        sep.pack(fill="x")

    def _card(self, parent, **kw):
        """Create a glass card container."""
        return GlassCard(parent,
            bg_color="rgba(25, 30, 55, 0.65)",
            border_color="rgba(100, 120, 180, 0.25)",
            corner_radius=16,
            **kw
        )


# ============================================================
# DASHBOARD PAGE
# ============================================================

class HalamanDashboard(HalamanBase):
    """Main dashboard with statistics and overview."""

    def __init__(self, parent):
        super().__init__(parent)
        self._header("Dashboard", "Welcome back, Admin")
        self._build()

    def _build(self):
        # Statistics row with gradient cards
        row1 = ctk.CTkFrame(self, fg_color="transparent")
        row1.pack(fill="x", padx=36, pady=(24, 12))

        self._cards = {}
        specs = [
            ("total", "Total Students", C["accent_blue"], "registered", "👥"),
            ("sudah_nilai", "Grades Submitted", C["accent_green"], "students", "✓"),
            ("rata_ipk", "Average GPA", C["accent_yellow"], "out of 4.00", "📈"),
            ("belum_nilai", "Pending Grades", C["accent_red"], "students", "⏳"),
        ]
        
        for col, (key, label, warna, satuan, icon) in enumerate(specs):
            card = GlassCard(row1, height=140,
                bg_color=f"rgba({int(warna[1:3], 16)}, {int(warna[3:5], 16)}, {int(warna[5:7], 16)}, 0.15)",
                border_color=f"rgba({int(warna[1:3], 16)}, {int(warna[3:5], 16)}, {int(warna[5:7], 16)}, 0.4)",
            )
            card.grid(row=0, column=col, padx=8, sticky="nsew")
            card.grid_propagate(False)
            row1.columnconfigure(col, weight=1)

            # Icon badge
            icon_bg = ctk.CTkFrame(card, width=50, height=50,
                corner_radius=12,
                fg_color=f"rgba({int(warna[1:3], 16)}, {int(warna[3:5], 16)}, {int(warna[5:7], 16)}, 0.25)")
            icon_bg.place(x=20, y=20)
            
            ctk.CTkLabel(icon_bg, text=icon, font=("Inter", 20)).place(relx=0.5, rely=0.5, anchor="center")

            # Label
            ctk.CTkLabel(card, text=label,
                font=("Inter", 10), text_color=C["text_muted"]
            ).place(x=20, y=78)

            # Value
            val_lbl = ctk.CTkLabel(card, text="0",
                font=("Inter", 32, "bold"), text_color=warna)
            val_lbl.place(x=20, y=98)

            # Unit
            ctk.CTkLabel(card, text=satuan,
                font=("Inter", 9), text_color=C["text_muted"]
            ).place(x=22, y=118)

            self._cards[key] = val_lbl

        # Second row - Best student & distribution
        row2 = ctk.CTkFrame(self, fg_color="transparent")
        row2.pack(fill="x", padx=36, pady=(0, 12))
        row2.columnconfigure(0, weight=2)
        row2.columnconfigure(1, weight=3)

        # Best student card
        info_card = GlassCard(row2, height=120,
            bg_color="rgba(40, 35, 70, 0.6)",
            border_color="rgba(140, 100, 200, 0.3)")
        info_card.grid(row=0, column=0, padx=(0, 8), sticky="nsew")
        info_card.grid_propagate(False)

        ctk.CTkLabel(info_card, text="⭐ TOP PERFORMER",
            font=("Inter", 9, "bold"), text_color=C["accent_purple"]
        ).place(x=20, y=16)
        
        self._lbl_best = ctk.CTkLabel(info_card, text="No data yet",
            font=("Inter", 14, "bold"), text_color=C["text_primary"])
        self._lbl_best.place(x=20, y=38)
        
        self._lbl_best_ipk = ctk.CTkLabel(info_card, text="",
            font=("Inter", 11), text_color=C["text_muted"])
        self._lbl_best_ipk.place(x=20, y=62)

        # Stats divider
        ctk.CTkFrame(info_card, width=1, 
            fg_color="rgba(100, 120, 180, 0.3)"
        ).place(relx=0.52, y=16, relheight=0.7)

        ctk.CTkLabel(info_card, text="HIGHEST GPA",
            font=("Inter", 9), text_color=C["text_muted"]
        ).place(relx=0.56, y=16)
        self._lbl_ipk_max = ctk.CTkLabel(info_card, text="0.00",
            font=("Inter", 22, "bold"), text_color=C["accent_green"])
        self._lbl_ipk_max.place(relx=0.56, y=38)

        ctk.CTkLabel(info_card, text="LOWEST GPA",
            font=("Inter", 9), text_color=C["text_muted"]
        ).place(relx=0.56, y=70)
        self._lbl_ipk_min = ctk.CTkLabel(info_card, text="0.00",
            font=("Inter", 22, "bold"), text_color=C["accent_red"])
        self._lbl_ipk_min.place(relx=0.56, y=90)

        # Grade distribution card
        dist_card = GlassCard(row2, height=120,
            bg_color="rgba(35, 40, 70, 0.6)",
            border_color="rgba(100, 120, 180, 0.25)")
        dist_card.grid(row=0, column=1, padx=(8, 0), sticky="nsew")
        dist_card.grid_propagate(False)

        ctk.CTkLabel(dist_card, text="📊 GRADE DISTRIBUTION",
            font=("Inter", 9, "bold"), text_color=C["text_muted"]
        ).place(x=20, y=16)

        self._dist_labels = {}
        predikat_specs = [
            ("Cumlaude", C["accent_purple"]),
            ("Excellent", C["accent_green"]),
            ("Good", C["accent_blue"]),
            ("Fair", C["accent_yellow"]),
            ("Needs Improvement", C["accent_red"]),
        ]
        
        for idx, (nama, warna) in enumerate(predikat_specs):
            ctk.CTkLabel(dist_card, text=nama,
                font=("Inter", 8), text_color=C["text_muted"]
            ).place(x=20 + idx * 115, y=40)
            lbl_val = ctk.CTkLabel(dist_card, text="0",
                font=("Inter", 20, "bold"), text_color=warna)
            lbl_val.place(x=20 + idx * 115, y=62)
            self._dist_labels[nama] = lbl_val

        # Recent activity section
        riwayat_card = GlassCard(self,
            bg_color="rgba(25, 30, 55, 0.65)",
            border_color="rgba(100, 120, 180, 0.25)")
        riwayat_card.pack(fill="both", expand=True, padx=36, pady=(0, 24))

        hdr_row = ctk.CTkFrame(riwayat_card, fg_color="transparent")
        hdr_row.pack(fill="x", padx=24, pady=(16, 0))
        ctk.CTkLabel(hdr_row, text="Recent Activity",
            font=F_SUBJUDUL, text_color=C["text_primary"]).pack(side="left")
        ctk.CTkLabel(hdr_row, text="Last 10 operations",
            font=F_TINY, text_color=C["text_muted"]).pack(side="right")

        col_hdr = ctk.CTkFrame(riwayat_card, 
            fg_color="rgba(40, 45, 75, 0.5)", height=32)
        col_hdr.pack(fill="x", padx=24, pady=(10, 0))
        col_hdr.pack_propagate(False)
        
        for txt, w in [("Time", 140), ("Action", 90), ("Details", 0)]:
            ctk.CTkLabel(col_hdr, text=txt, width=w,
                font=("Inter", 9, "bold"), text_color=C["text_muted"],
                anchor="w").pack(side="left", padx=(12, 0))

        self._riwayat_frame = ctk.CTkScrollableFrame(
            riwayat_card, fg_color="transparent")
        self._riwayat_frame.pack(fill="both", expand=True, 
            padx=24, pady=(6, 16))

        self.refresh()

    def refresh(self):
        stat = db.statistik()
        semua = db.get_semua()

        total = stat["total"]
        sudah = stat["sudah_nilai"]

        self._cards["total"].configure(text=str(total))
        self._cards["sudah_nilai"].configure(text=str(sudah))
        self._cards["rata_ipk"].configure(text=str(stat["rata_ipk"]))
        self._cards["belum_nilai"].configure(text=str(total - sudah))

        if stat["terbaik"] != "-":
            self._lbl_best.configure(text=stat["terbaik"])
            self._lbl_best_ipk.configure(text=f"GPA {stat['terbaik_ipk']:.2f}")
        else:
            self._lbl_best.configure(text="No data yet")
            self._lbl_best_ipk.configure(text="")

        ipk_vals = [db.ipk_mahasiswa(m) for m in semua if m["semester"]]
        if ipk_vals:
            self._lbl_ipk_max.configure(text=f"{max(ipk_vals):.2f}")
            self._lbl_ipk_min.configure(text=f"{min(ipk_vals):.2f}")
        else:
            self._lbl_ipk_max.configure(text="0.00")
            self._lbl_ipk_min.configure(text="0.00")

        dist = {"Cumlaude": 0, "Excellent": 0, "Good": 0, "Fair": 0, "Needs Improvement": 0}
        for m in semua:
            if m["semester"]:
                p = db.predikat(db.ipk_mahasiswa(m))
                # Map Indonesian predicates to English
                mapping = {
                    "Cumlaude": "Cumlaude",
                    "Sangat Baik": "Excellent",
                    "Baik": "Good",
                    "Cukup": "Fair",
                    "Perlu Perbaikan": "Needs Improvement"
                }
                eng_p = mapping.get(p, "Fair")
                if eng_p in dist:
                    dist[eng_p] += 1
        
        for nama, lbl in self._dist_labels.items():
            lbl.configure(text=str(dist.get(nama, 0)))

        aksi_warna = {
            "TAMBAH": C["accent_green"], 
            "HAPUS": C["accent_red"],
            "NILAI": C["accent_blue"],  
            "EDIT": C["accent_yellow"],
        }
        
        for w in self._riwayat_frame.winfo_children():
            w.destroy()
        
        for h in db.get_riwayat()[:10]:
            row = ctk.CTkFrame(self._riwayat_frame, 
                fg_color="transparent", height=36)
            row.pack(fill="x", pady=2)
            row.pack_propagate(False)
            
            warna_aksi = aksi_warna.get(h["aksi"], C["text_muted"])
            
            ctk.CTkLabel(row, text=h["waktu"], width=140,
                font=F_TINY, text_color=C["text_muted"], anchor="w"
            ).pack(side="left", padx=(8, 0))
            
            ctk.CTkLabel(row, text=h["aksi"], width=80,
                font=("Inter", 9, "bold"),
                text_color=warna_aksi, anchor="w"
            ).pack(side="left")
            
            ctk.CTkLabel(row, text=h["detail"],
                font=F_SMALL, text_color=C["text_secondary"], anchor="w"
            ).pack(side="left", padx=(8, 0))


# ============================================================
# STUDENT DATA PAGE
# ============================================================

class HalamanMahasiswa(HalamanBase):
    """Student management page with modern table."""

    def __init__(self, parent, on_nilai):
        super().__init__(parent)
        self._on_nilai = on_nilai
        self._header("Students", "Manage registered students")
        self._style_tree()
        self._build()
        self.refresh()

    def _style_tree(self):
        """Style Treeview with modern dark theme."""
        s = ttk.Style()
        s.theme_use("clam")
        
        s.configure("App.Treeview",
            background="rgba(25, 30, 55, 0.5)",
            foreground=C["text_primary"],
            fieldbackground="rgba(25, 30, 55, 0.5)",
            rowheight=48,
            font=("Inter", 11),
            borderwidth=0,
        )
        
        s.configure("App.Treeview.Heading",
            background="rgba(40, 45, 75, 0.8)",
            foreground=C["text_secondary"],
            font=("Inter", 10, "bold"),
            borderwidth=0,
            relief="flat",
            padding=(0, 12),
        )
        
        s.map("App.Treeview",
            background=[("selected", "rgba(60, 80, 140, 0.6)")],
            foreground=[("selected", "#FFFFFF")]
        )

    def _build(self):
        toolbar = ctk.CTkFrame(self, fg_color="transparent")
        toolbar.pack(fill="x", padx=36, pady=16)

        # Search box with modern styling
        self._search_var = ctk.StringVar()
        self._search_var.trace_add("write", lambda *_: self.refresh())
        
        search_frame = GlassCard(toolbar, height=42,
            bg_color="rgba(30, 35, 60, 0.7)",
            border_color="rgba(100, 120, 180, 0.3)")
        search_frame.pack(side="left")
        
        search_icon = ctk.CTkLabel(search_frame, text="🔍",
            font=("Inter", 14), text_color=C["text_muted"])
        search_icon.place(x=12, y=11)
        
        search = ctk.CTkEntry(
            search_frame, width=280, height=42,
            placeholder_text="Search by NIM or name...",
            textvariable=self._search_var,
            font=F_NORMAL,
            corner_radius=12,
            fg_color="transparent",
            text_color=C["text_primary"],
            border_width=0,
        )
        search.place(x=38, y=0)

        # Action buttons
        GlassButton(toolbar, "➕ Add", self._form_tambah, 
            width=110, fg_color=C["accent_blue"], glow=True
        ).pack(side="right", padx=(6, 0))
        
        GlassButton(toolbar, "✏️ Edit", self._form_edit, 
            width=90, fg_color=C["accent_yellow"], glow=True
        ).pack(side="right", padx=6)
        
        GlassButton(toolbar, "📝 Grade", self._ke_nilai, 
            width=90, fg_color=C["accent_green"], glow=True
        ).pack(side="right", padx=6)
        
        GlassButton(toolbar, "🗑️ Delete", self._hapus, 
            width=80, fg_color=C["accent_red"], glow=True
        ).pack(side="right")

        # Modern table container
        tbl_frame = GlassCard(self,
            bg_color="rgba(25, 30, 55, 0.65)",
            border_color="rgba(100, 120, 180, 0.25)")
        tbl_frame.pack(fill="both", expand=True, padx=36, pady=(0, 24))

        cols = ("nim", "nama", "semester_terisi", "ipk", "total_sks", "predikat")
        self._tree = ttk.Treeview(tbl_frame, columns=cols, show="headings",
            style="App.Treeview", selectmode="browse")

        hdrs = {
            "nim": ("NIM", 130),
            "nama": ("Full Name", 280),
            "semester_terisi": ("Semester", 120),
            "ipk": ("GPA", 80),
            "total_sks": ("Credits", 100),
            "predikat": ("Grade", 150),
        }
        
        for col, (head, w) in hdrs.items():
            self._tree.heading(col, text=head, anchor="center")
            anc = "center" if col not in ("nama",) else "w"
            self._tree.column(col, width=w, anchor=anc, minwidth=80)

        vsb = ttk.Scrollbar(tbl_frame, orient="vertical", command=self._tree.yview)
        self._tree.configure(yscrollcommand=vsb.set)
        self._tree.pack(side="left", fill="both", expand=True, padx=(1, 0), pady=1)
        vsb.pack(side="right", fill="y")

        # Color tags for grades
        self._tree.tag_configure("cumlaude", foreground=C["accent_purple"])
        self._tree.tag_configure("sangat", foreground=C["accent_green"])
        self._tree.tag_configure("baik", foreground=C["accent_blue"])
        self._tree.tag_configure("cukup", foreground=C["accent_yellow"])
        self._tree.tag_configure("perlu", foreground=C["accent_red"])

        self._tree.bind("<Double-1>", lambda e: self._detail())

        self._sbar = ctk.CTkLabel(self, text="", 
            font=F_TINY, text_color=C["text_muted"])
        self._sbar.pack(anchor="w", padx=36, pady=(0, 8))

    def refresh(self):
        for i in self._tree.get_children():
            self._tree.delete(i)

        keyword = self._search_var.get()
        rows = db.cari(keyword) if keyword else db.get_semua()

        tag_map = {
            "Cumlaude": "cumlaude",
            "Sangat Baik": "sangat",
            "Baik": "baik",
            "Cukup": "cukup",
            "Perlu Perbaikan": "perlu",
        }

        for m in rows:
            ipk = db.ipk_mahasiswa(m)
            pred = db.predikat(ipk)
            self._tree.insert("", "end", iid=m["nim"], values=(
                m["nim"],
                m["nama"],
                db.semester_terisi(m),
                f"{ipk:.2f}",
                db.total_sks(m),
                pred,
            ), tags=(tag_map.get(pred, ""),))

        self._sbar.configure(
            text=f"Showing {len(rows)} of {db.statistik()['total']} students")

    def _selected_nim(self) -> str | None:
        sel = self._tree.selection()
        if not sel:
            messagebox.showwarning("Notice", "Please select a student first.")
            return None
        return sel[0]

    def _form_tambah(self):
        win = ctk.CTkToplevel(self)
        win.title("Add Student")
        win.geometry("440x320")
        win.resizable(False, False)
        win.grab_set()
        
        # Style the window
        win.configure(fg_color="rgba(15, 20, 40, 0.95)")

        ctk.CTkLabel(win, text="Add New Student",
            font=F_SUBJUDUL, text_color=C["text_primary"]
        ).pack(pady=(28, 20))

        # Styled entry frames
        e_nim = ctk.CTkEntry(win, width=320, height=44,
            placeholder_text="Student ID (NIM)",
            font=F_NORMAL, corner_radius=12,
            fg_color="rgba(30, 35, 60, 0.7)",
            border_color="rgba(100, 120, 180, 0.3)",
            text_color=C["text_primary"],
        )
        e_nim.pack(pady=8)
        
        e_nama = ctk.CTkEntry(win, width=320, height=44,
            placeholder_text="Full Name",
            font=F_NORMAL, corner_radius=12,
            fg_color="rgba(30, 35, 60, 0.7)",
            border_color="rgba(100, 120, 180, 0.3)",
            text_color=C["text_primary"],
        )
        e_nama.pack(pady=8)

        def simpan(*_):
            try:
                db.tambah_mahasiswa(e_nim.get(), e_nama.get())
                self.refresh()
                win.destroy()
                messagebox.showinfo("Success", "Student added successfully.")
            except ValueError as err:
                messagebox.showerror("Error", str(err))

        e_nama.bind("<Return>", simpan)
        
        GlassButton(win, "Save", simpan, 
            width=320, fg_color=C["accent_blue"], glow=True
        ).pack(pady=24)
        e_nim.focus_set()

    def _form_edit(self):
        nim = self._selected_nim()
        if not nim: return
        semua = db.get_semua()
        mhs = next((m for m in semua if m["nim"] == nim), None)
        if not mhs: return

        win = ctk.CTkToplevel(self)
        win.title("Edit Name")
        win.geometry("440x260")
        win.resizable(False, False)
        win.grab_set()
        win.configure(fg_color="rgba(15, 20, 40, 0.95)")

        ctk.CTkLabel(win, text=f"Edit Name — ID {nim}",
            font=F_SUBJUDUL, text_color=C["text_primary"]
        ).pack(pady=(28, 20))

        e_nama = ctk.CTkEntry(win, width=320, height=44,
            placeholder_text="Full Name",
            font=F_NORMAL, corner_radius=12,
            fg_color="rgba(30, 35, 60, 0.7)",
            border_color="rgba(100, 120, 180, 0.3)",
            text_color=C["text_primary"],
        )
        e_nama.pack(pady=8)
        e_nama.insert(0, mhs["nama"])

        def simpan(*_):
            try:
                db.edit_nama(nim, e_nama.get())
                self.refresh()
                win.destroy()
                messagebox.showinfo("Success", "Name updated successfully.")
            except ValueError as err:
                messagebox.showerror("Error", str(err))

        e_nama.bind("<Return>", simpan)
        
        GlassButton(win, "Update", simpan, 
            width=320, fg_color=C["accent_yellow"], glow=True
        ).pack(pady=24)
        e_nama.focus_set()

    def _ke_nilai(self):
        nim = self._selected_nim()
        if nim:
            self._on_nilai(nim)

    def _detail(self):
        nim = self._selected_nim()
        if not nim: return
        
        semua = db.get_semua()
        mhs = next((m for m in semua if m["nim"] == nim), None)
        if not mhs: return

        win = ctk.CTkToplevel(self)
        win.title("Student Details")
        win.geometry("500x400")
        win.resizable(False, False)
        win.grab_set()
        win.configure(fg_color="rgba(15, 20, 40, 0.95)")

        ctk.CTkLabel(win, text="Student Profile",
            font=F_SUBJUDUL, text_color=C["text_primary"]
        ).pack(pady=(28, 20))

        info_frame = GlassCard(win, width=420, height=280,
            bg_color="rgba(30, 35, 60, 0.7)")
        info_frame.pack(pady=12)
        info_frame.pack_propagate(False)

        ipk = db.ipk_mahasiswa(mhs)
        pred = db.predikat(ipk)

        details = [
            ("Student ID", mhs["nim"]),
            ("Full Name", mhs["nama"]),
            ("Semester", db.semester_terisi(mhs)),
            ("GPA", f"{ipk:.2f}"),
            ("Total Credits", db.total_sks(mhs)),
            ("Grade", pred),
        ]

        for i, (label, value) in enumerate(details):
            y_pos = 20 + i * 42
            ctk.CTkLabel(info_frame, text=label,
                font=F_SMALL, text_color=C["text_muted"]
            ).place(x=24, y=y_pos)
            ctk.CTkLabel(info_frame, text=value,
                font=("Inter", 12, "bold"), text_color=C["text_primary"]
            ).place(x=180, y=y_pos)

        GlassButton(win, "Close", win.destroy,
            width=140, fg_color=C["accent_blue"], glow=True
        ).pack(pady=20)

    def _hapus(self):
        nim = self._selected_nim()
        if not nim: return
        
        confirm = messagebox.askyesno("Confirm Delete",
            f"Are you sure you want to delete student {nim}?\nThis action cannot be undone.")
        if confirm:
            db.hapus_mahasiswa(nim)
            self.refresh()
            messagebox.showinfo("Success", "Student deleted successfully.")


# ============================================================
# GRADE INPUT PAGE
# ============================================================

class HalamanNilai(HalamanBase):
    """Grade input page with modern form design."""

    def __init__(self, parent, on_back):
        super().__init__(parent)
        self._on_back = on_back
        self._header("Input Grades", "Enter course grades")
        self._current_nim = None
        self._entries = {}
        self._build()

    def _build(self):
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=36, pady=20)

        # Student selector
        selector_frame = GlassCard(content, height=60,
            bg_color="rgba(30, 35, 60, 0.7)")
        selector_frame.pack(fill="x", pady=(0, 20))
        selector_frame.pack_propagate(False)

        ctk.CTkLabel(selector_frame, text="Select Student:",
            font=F_NORMAL, text_color=C["text_secondary"]
        ).pack(side="left", padx=20, pady=18)

        self._student_var = ctk.StringVar()
        self._student_combo = ctk.CTkOptionMenu(
            selector_frame,
            variable=self._student_var,
            command=self._load_student,
            width=300,
            height=40,
            corner_radius=10,
            fg_color="rgba(40, 45, 75, 0.8)",
            button_color="rgba(60, 70, 110, 0.8)",
            button_hover_color="rgba(80, 90, 140, 0.8)",
            text_color=C["text_primary"],
            font=F_NORMAL,
        )
        self._student_combo.pack(side="left", padx=16, pady=10)

        # Grade entry form
        form_card = GlassCard(content,
            bg_color="rgba(30, 35, 60, 0.7)",
            border_color="rgba(100, 120, 180, 0.25)")
        form_card.pack(fill="both", expand=True)

        subjects = [
            ("Mathematics", "math"),
            ("Physics", "physics"),
            ("Programming", "programming"),
            ("Electronics", "electronics"),
            ("Robotics", "robotics"),
            ("Automation", "automation"),
        ]

        for i, (subject, key) in enumerate(subjects):
            row = ctk.CTkFrame(form_card, fg_color="transparent", height=50)
            row.pack(fill="x", padx=24, pady=6)
            row.pack_propagate(False)

            ctk.CTkLabel(row, text=subject,
                font=F_NORMAL, text_color=C["text_primary"], width=180, anchor="w"
            ).pack(side="left")

            entry = ctk.CTkEntry(row, width=100, height=38,
                placeholder_text="0-100",
                font=F_NORMAL, corner_radius=10,
                fg_color="rgba(40, 45, 75, 0.8)",
                border_color="rgba(100, 120, 180, 0.3)",
                text_color=C["text_primary"],
            )
            entry.pack(side="left", padx=16)
            self._entries[key] = entry

        # Action buttons
        btn_frame = ctk.CTkFrame(form_card, fg_color="transparent")
        btn_frame.pack(fill="x", padx=24, pady=20)

        GlassButton(btn_frame, "← Back", self._on_back,
            width=100, fg_color="rgba(60, 70, 100, 0.8)", glow=True
        ).pack(side="left")

        GlassButton(btn_frame, "💾 Save Grades", self._simpan,
            width=160, fg_color=C["accent_green"], glow=True
        ).pack(side="right")

    def refresh(self):
        semua = db.get_semua()
        students = [f"{m['nim']} - {m['nama']}" for m in semua]
        self._student_combo.configure(values=students)
        if students:
            self._student_var.set(students[0])
            self._load_student(students[0])

    def _load_student(self, selection):
        if not selection:
            return
        
        nim = selection.split(" - ")[0]
        self._current_nim = nim
        
        mhs = db.get_mahasiswa(nim)
        if mhs and mhs["nilai"]:
            for key, entry in self._entries.items():
                entry.delete(0, "end")
                entry.insert(0, str(mhs["nilai"].get(key, "")))

    def _simpan(self):
        if not self._current_nim:
            messagebox.showwarning("Notice", "Please select a student first.")
            return

        nilai = {}
        for key, entry in self._entries.items():
            try:
                val = entry.get().strip()
                if val:
                    n = float(val)
                    if n < 0 or n > 100:
                        raise ValueError
                    nilai[key] = n
            except ValueError:
                messagebox.showerror("Error", 
                    f"Invalid grade for {key}. Please enter 0-100.")
                return

        if not nilai:
            messagebox.showwarning("Notice", "Please enter at least one grade.")
            return

        db.input_nilai(self._current_nim, nilai)
        messagebox.showinfo("Success", "Grades saved successfully.")
        self.refresh()


# ============================================================
# STATISTICS PAGE
# ============================================================

class HalamanStatistik(HalamanBase):
    """Statistics page with animated charts."""

    def __init__(self, parent):
        super().__init__(parent)
        self._header("Statistics", "Academic performance analytics")
        self._build()

    def _build(self):
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=36, pady=20)

        # Chart type selector
        selector_frame = ctk.CTkFrame(content, fg_color="transparent")
        selector_frame.pack(fill="x", pady=(0, 16))

        self._chart_var = ctk.StringVar(value="bar")
        
        chart_types = [
            ("Bar Chart", "bar"),
            ("Column Chart", "column"),
            ("Pie Chart", "pie"),
            ("Line Chart", "line"),
        ]

        for label, value in chart_types:
            rb = ctk.CTkRadioButton(
                selector_frame,
                text=label,
                variable=self._chart_var,
                value=value,
                command=self._update_chart,
                font=F_SMALL,
                text_color=C["text_secondary"],
                fg_color=C["accent_blue"],
            )
            rb.pack(side="left", padx=12)

        # Chart container
        self._chart_card = GlassCard(content,
            bg_color="rgba(25, 30, 55, 0.65)",
            border_color="rgba(100, 120, 180, 0.25)")
        self._chart_card.pack(fill="both", expand=True)

        self._canvas = tk.Canvas(self._chart_card,
            bg="rgba(20, 25, 50, 0.5)",
            highlightthickness=0)
        self._canvas.pack(fill="both", expand=True, padx=20, pady=20)

        self._update_chart()

    def _update_chart(self):
        self._canvas.delete("all")
        
        chart_type = self._chart_var.get()
        semua = db.get_semua()
        
        if not semua:
            self._canvas.create_text(
                self._canvas.winfo_width() // 2,
                self._canvas.winfo_height() // 2,
                text="No data available",
                fill=C["text_muted"],
                font=("Inter", 14)
            )
            return

        # Prepare data
        data = []
        for m in semua[:10]:  # Limit to 10 for display
            ipk = db.ipk_mahasiswa(m)
            data.append((m["nama"][:15], round(ipk, 2)))

        colors = [
            C["accent_blue"], C["accent_purple"], C["accent_pink"],
            C["accent_cyan"], C["accent_green"], C["accent_yellow"],
            C["accent_red"], "#6366F1", "#8B5CF6", "#EC4899"
        ]

        if chart_type == "bar":
            self._draw_bar(data, colors)
        elif chart_type == "column":
            self._draw_column(data, colors)
        elif chart_type == "pie":
            self._draw_pie(data, colors)
        elif chart_type == "line":
            self._draw_line(data, colors)

    def _draw_bar(self, data, colors):
        canvas = self._canvas
        canvas.update_idletasks()
        W = canvas.winfo_width() or 600
        H = canvas.winfo_height() or 400

        PAD_L, PAD_R, PAD_T, PAD_B = 100, 30, 50, 60
        chart_w = W - PAD_L - PAD_R
        chart_h = H - PAD_T - PAD_B

        if not data:
            return

        max_val = max(v for _, v in data) or 4.0
        n = len(data)
        gap = 8
        bar_h = max(15, (chart_h - gap * (n + 1)) // n)

        # Title
        canvas.create_text(PAD_L + chart_w // 2, 20, 
            text="Student GPA Comparison",
            font=("Inter", 14, "bold"),
            fill=C["text_primary"], anchor="center")

        # Bars
        for i, ((label, val), color) in enumerate(zip(data, colors)):
            y1 = PAD_T + gap + i * (bar_h + gap)
            y2 = y1 + bar_h
            bar_len = int(chart_w * val / max_val) if max_val > 0 else 0

            # Background track
            canvas.create_rectangle(PAD_L, y1, PAD_L + chart_w, y2,
                fill="rgba(50, 55, 90, 0.3)", outline="")
            
            # Bar with gradient effect
            canvas.create_rectangle(PAD_L, y1, PAD_L + bar_len, y2,
                fill=color, outline="")

            # Label
            canvas.create_text(PAD_L - 8, (y1 + y2) // 2,
                text=label, font=("Inter", 9),
                fill=C["text_secondary"], anchor="e")

            # Value
            if val > 0:
                canvas.create_text(PAD_L + bar_len + 10, (y1 + y2) // 2,
                    text=f"{val:.2f}", font=("Inter", 10, "bold"),
                    fill=color, anchor="w")

    def _draw_column(self, data, colors):
        canvas = self._canvas
        canvas.update_idletasks()
        W = canvas.winfo_width() or 600
        H = canvas.winfo_height() or 400

        PAD_L, PAD_R, PAD_T, PAD_B = 60, 30, 50, 80
        chart_w = W - PAD_L - PAD_R
        chart_h = H - PAD_T - PAD_B

        if not data:
            return

        max_val = max(v for _, v in data) or 4.0
        n = len(data)
        gap = 12
        bar_w = max(20, (chart_w - gap * (n + 1)) // n)

        # Title
        canvas.create_text(PAD_L + chart_w // 2, 20,
            text="Student GPA Comparison",
            font=("Inter", 14, "bold"),
            fill=C["text_primary"], anchor="center")

        # Grid lines
        for i in range(5):
            gy = PAD_T + chart_h - int(chart_h * i / 4)
            canvas.create_line(PAD_L, gy, PAD_L + chart_w, gy,
                fill="rgba(100, 120, 180, 0.2)", width=1, dash=(3, 3))
            val_label = max_val * i / 4
            canvas.create_text(PAD_L - 8, gy,
                text=f"{val_label:.1f}",
                font=("Inter", 8), fill=C["text_muted"], anchor="e")

        # Columns
        for i, ((label, val), color) in enumerate(zip(data, colors)):
            x1 = PAD_L + gap + i * (bar_w + gap)
            x2 = x1 + bar_w
            bar_h_px = int(chart_h * val / max_val) if max_val > 0 else 0
            y1 = PAD_T + chart_h - bar_h_px
            y2 = PAD_T + chart_h

            if bar_h_px > 0:
                canvas.create_rectangle(x1, y1, x2, y2,
                    fill=color, outline="")

            # Label
            canvas.create_text((x1 + x2) // 2, PAD_T + chart_h + 16,
                text=label, font=("Inter", 8),
                fill=C["text_secondary"], anchor="n")

            # Value
            if val > 0:
                canvas.create_text((x1 + x2) // 2, y1 - 8,
                    text=f"{val:.2f}",
                    font=("Inter", 9, "bold"),
                    fill=color, anchor="s")

    def _draw_pie(self, data, colors):
        canvas = self._canvas
        canvas.update_idletasks()
        W = canvas.winfo_width() or 600
        H = canvas.winfo_height() or 400

        total = sum(v for _, v in data if v > 0)
        if total == 0:
            return

        cx = W * 0.4
        cy = H // 2
        r = min(cx - 30, H // 2 - 40)

        # Title
        canvas.create_text(W // 2, 20,
            text="GPA Distribution",
            font=("Inter", 14, "bold"),
            fill=C["text_primary"], anchor="center")

        start = 0.0
        slices = [(label, val, color)
                  for (label, val), color in zip(data, colors)
                  if val > 0]

        for label, val, color in slices:
            extent = (val / total) * 360
            canvas.create_arc(cx - r, cy - r, cx + r, cy + r,
                start=start, extent=extent,
                fill=color, outline="rgba(30, 35, 60, 1)", width=2)
            start += extent

        # Legend
        lx = cx * 2 + 30
        ly = H // 2 - len(slices) * 22
        for label, val, color in slices:
            pct = val / total * 100
            canvas.create_rectangle(lx, ly, lx + 14, ly + 14,
                fill=color, outline="")
            canvas.create_text(lx + 20, ly + 7,
                text=f"{label} ({pct:.1f}%)",
                font=("Inter", 9), fill=C["text_secondary"],
                anchor="w")
            ly += 22

    def _draw_line(self, data, colors):
        canvas = self._canvas
        canvas.update_idletasks()
        W = canvas.winfo_width() or 600
        H = canvas.winfo_height() or 400

        PAD_L, PAD_R, PAD_T, PAD_B = 60, 30, 50, 60
        chart_w = W - PAD_L - PAD_R
        chart_h = H - PAD_T - PAD_B

        if not data:
            return

        max_val = max(v for _, v in data) or 4.0
        n = len(data)

        # Title
        canvas.create_text(PAD_L + chart_w // 2, 20,
            text="GPA Trend",
            font=("Inter", 14, "bold"),
            fill=C["text_primary"], anchor="center")

        # Grid
        for i in range(5):
            gy = PAD_T + chart_h - int(chart_h * i / 4)
            canvas.create_line(PAD_L, gy, PAD_L + chart_w, gy,
                fill="rgba(100, 120, 180, 0.2)", width=1, dash=(3, 3))

        # Line
        points = []
        for i, (label, val) in enumerate(data):
            gx = PAD_L + int(chart_w * i / (n - 1)) if n > 1 else PAD_L + chart_w // 2
            gy = PAD_T + chart_h - int(chart_h * val / max_val)
            points.append((gx, gy))

            # Label
            canvas.create_text(gx, PAD_T + chart_h + 16,
                text=label, font=("Inter", 8),
                fill=C["text_secondary"], anchor="n")

        # Draw line segments
        color = colors[0]
        for i in range(len(points) - 1):
            x1, y1 = points[i]
            x2, y2 = points[i + 1]
            canvas.create_line(x1, y1, x2, y2, fill=color, width=3, smooth=True)

        # Draw points
        for gx, gy in points:
            canvas.create_oval(gx - 5, gy - 5, gx + 5, gy + 5,
                fill=color, outline="rgba(30, 35, 60, 1)", width=2)

    def refresh(self):
        self._update_chart()


# ============================================================
# HISTORY PAGE
# ============================================================

class HalamanRiwayat(HalamanBase):
    """Activity history page."""

    def __init__(self, parent):
        super().__init__(parent)
        self._header("Activity Log", "System operation history")
        self._build()

    def _build(self):
        content = GlassCard(self,
            bg_color="rgba(25, 30, 55, 0.65)",
            border_color="rgba(100, 120, 180, 0.25)")
        content.pack(fill="both", expand=True, padx=36, pady=24)

        # Column headers
        col_hdr = ctk.CTkFrame(content,
            fg_color="rgba(40, 45, 75, 0.6)", height=40)
        col_hdr.pack(fill="x", padx=20, pady=(16, 0))
        col_hdr.pack_propagate(False)

        for txt, w in [("Timestamp", 160), ("Action", 100), ("Details", 0)]:
            ctk.CTkLabel(col_hdr, text=txt, width=w,
                font=("Inter", 10, "bold"), text_color=C["text_muted"],
                anchor="w").pack(side="left", padx=(16, 0))

        self._history_frame = ctk.CTkScrollableFrame(
            content, fg_color="transparent")
        self._history_frame.pack(fill="both", expand=True, 
            padx=20, pady=(8, 16))

        self.refresh()

    def refresh(self):
        for w in self._history_frame.winfo_children():
            w.destroy()

        aksi_warna = {
            "TAMBAH": C["accent_green"],
            "HAPUS": C["accent_red"],
            "NILAI": C["accent_blue"],
            "EDIT": C["accent_yellow"],
        }

        for h in db.get_riwayat():
            row = GlassCard(self._history_frame, height=44,
                bg_color="rgba(35, 40, 70, 0.4)")
            row.pack(fill="x", pady=3)
            row.pack_propagate(False)

            warna_aksi = aksi_warna.get(h["aksi"], C["text_muted"])

            ctk.CTkLabel(row, text=h["waktu"], width=160,
                font=F_SMALL, text_color=C["text_muted"], anchor="w"
            ).place(x=16, y=12)

            ctk.CTkLabel(row, text=h["aksi"], width=90,
                font=("Inter", 10, "bold"),
                text_color=warna_aksi, anchor="w"
            ).place(x=170, y=12)

            ctk.CTkLabel(row, text=h["detail"],
                font=F_SMALL, text_color=C["text_secondary"], anchor="w"
            ).place(x=270, y=12)


# ============================================================
# MAIN APP CLASS
# ============================================================

class App(ctk.CTk):
    """Main application window with macOS-inspired design."""

    def __init__(self):
        super().__init__()

        # Window configuration
        self.title("✦ ARION - Student Portal")
        self.geometry("1400x900")
        self.minsize(1200, 700)

        # Configure main window background with gradient
        self.configure(fg_color=C["bg_dark"])

        # Create gradient background canvas
        self._create_background()

        # Main container
        self._container = ctk.CTkFrame(self, fg_color="transparent")
        self._container.pack(fill="both", expand=True, padx=0, pady=0)

        # Initialize pages
        self._pages = {}
        self._current_page = None

        # Setup layout
        self._setup_layout()

        # Navigate to login
        self._show_login()

    def _create_background(self):
        """Create animated gradient background."""
        self._bg_canvas = tk.Canvas(self, 
            highlightthickness=0, 
            bg=C["bg_dark"])
        self._bg_canvas.place(x=0, y=0, relwidth=1, relheight=1)

        # Draw gradient rectangles
        colors = [C["bg_gradient_1"], C["bg_gradient_2"], C["bg_gradient_3"]]
        for i, color in enumerate(colors):
            y_start = i * 0.4
            y_end = y_start + 0.5
            self._bg_canvas.create_rectangle(
                0, int(self.winfo_height() * y_start),
                self.winfo_width(), int(self.winfo_height() * y_end),
                fill=color, outline=""
            )

    def _setup_layout(self):
        """Setup main layout with sidebar and content area."""
        # Clear container
        for widget in self._container.winfo_children():
            widget.destroy()

        # Sidebar
        self._sidebar = Sidebar(self._container, self._navigate)
        self._sidebar.pack(side="left", fill="y")

        # Content area
        self._content_frame = ctk.CTkFrame(self._container, 
            fg_color="transparent")
        self._content_frame.pack(side="right", fill="both", expand=True)

        # Initialize pages
        self._pages["dashboard"] = HalamanDashboard(self._content_frame)
        self._pages["mahasiswa"] = HalamanMahasiswa(self._content_frame, self._go_nilai)
        self._pages["nilai"] = HalamanNilai(self._content_frame, lambda: self._navigate("mahasiswa"))
        self._pages["statistik"] = HalamanStatistik(self._content_frame)
        self._pages["riwayat"] = HalamanRiwayat(self._content_frame)

    def _show_login(self):
        """Show login screen."""
        for widget in self._container.winfo_children():
            widget.destroy()

        login_frame = ctk.CTkFrame(self._container, fg_color="transparent")
        login_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Login card
        login_card = GlassCard(login_frame, width=420, height=380,
            bg_color="rgba(25, 30, 55, 0.85)",
            border_color="rgba(100, 120, 180, 0.3)")
        login_card.pack()
        login_card.pack_propagate(False)

        # Logo
        ctk.CTkLabel(login_card, text="✦ ARION",
            font=("Inter", 32, "bold"), text_color="#FFFFFF"
        ).pack(pady=(40, 8))

        ctk.CTkLabel(login_card, text="Student Portal",
            font=("Inter", 12), text_color=C["text_muted"]
        ).pack(pady=(0, 30))

        # Username
        username_entry = ctk.CTkEntry(login_card, width=320, height=46,
            placeholder_text="Username",
            font=F_NORMAL, corner_radius=12,
            fg_color="rgba(40, 45, 75, 0.7)",
            border_color="rgba(100, 120, 180, 0.3)",
            text_color=C["text_primary"],
        )
        username_entry.pack(pady=8)
        username_entry.insert(0, "admin")

        # Password
        password_entry = ctk.CTkEntry(login_card, width=320, height=46,
            placeholder_text="Password",
            show="•",
            font=F_NORMAL, corner_radius=12,
            fg_color="rgba(40, 45, 75, 0.7)",
            border_color="rgba(100, 120, 180, 0.3)",
            text_color=C["text_primary"],
        )
        password_entry.pack(pady=8)
        password_entry.insert(0, "123")

        def do_login(*args):
            if username_entry.get() == "admin" and password_entry.get() == "123":
                self._setup_layout()
                self._navigate("dashboard")
            else:
                messagebox.showerror("Login Failed", "Invalid credentials.\nDefault: admin / 123")

        password_entry.bind("<Return>", do_login)

        # Login button
        GlassButton(login_card, "Sign In", do_login,
            width=320, height=46, 
            fg_color=C["accent_blue"], glow=True
        ).pack(pady=28)

        # Hint
        ctk.CTkLabel(login_card, text="Default: admin / 123",
            font=F_TINY, text_color=C["text_muted"]
        ).pack()

    def _navigate(self, page_key: str):
        """Navigate to a page."""
        if page_key == "logout":
            self._show_login()
            return

        if self._current_page:
            self._current_page.pack_forget()

        if page_key in self._pages:
            self._pages[page_key].pack(fill="both", expand=True)
            self._pages[page_key].refresh()
            self._current_page = self._pages[page_key]
            self._sidebar.aktifkan(page_key)

    def _go_nilai(self, nim: str):
        """Go to grade input page for specific student."""
        self._navigate("nilai")
        if hasattr(self._pages["nilai"], "_student_combo"):
            semua = db.get_semua()
            mhs = next((m for m in semua if m["nim"] == nim), None)
            if mhs:
                selection = f"{nim} - {mhs['nama']}"
                self._pages["nilai"]._student_var.set(selection)
                self._pages["nilai"]._load_student(selection)


# ============================================================
# RUN APP
# ============================================================

if __name__ == "__main__":
    app = App()
    app.mainloop()
