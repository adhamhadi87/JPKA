import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
from textwrap import dedent

# =======================
# TETAPAN PAGE
# =======================
st.set_page_config(
    page_title="PRESTASI PERBELANJAAN DAN HASIL CIDB",
    layout="wide"
)


def html(kod_html):
    st.markdown(dedent(kod_html).strip(), unsafe_allow_html=True)


html("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
.block-container {padding: 1rem 2rem;}
.card {
    background-color: #ffffff;
    border-left: 5px solid #2c3e50;
    padding: 1.3rem;
    border-radius: 10px;
    box-shadow: 3px 3px 12px rgba(0,0,0,0.08);
    text-align:center;
    min-height: 165px;
}
.metric-row {
    display: flex;
    justify-content: space-between;
    margin: 8px 0;
    font-size: 14px;
    gap: 14px;
}
.metric-label {color: #555; font-weight: 500;}
.metric-value {font-weight: bold;}
.traffic-circle {
    width: 95px;
    height: 95px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 32px;
    font-weight: bold;
    color: white;
    margin: 8px auto 6px;
    box-shadow: 0 6px 12px rgba(0,0,0,0.3);
}
.stApp {
    background: linear-gradient(135deg, #f5f7fa 0%, #e4e5e6 100%);
}

/* =========================================================
   SOFT CORPORATE GLASSMORPHISM THEME
   ========================================================= */

/* Main app background */
.stApp {
    background:
        radial-gradient(circle at top left, rgba(59,130,246,0.18), transparent 34%),
        radial-gradient(circle at top right, rgba(14,165,233,0.14), transparent 32%),
        linear-gradient(135deg, #eef4ff 0%, #f8fbff 45%, #e8f0fb 100%) !important;
}

/* Main page spacing */
.block-container {
    padding-top: 1.1rem !important;
    padding-bottom: 2rem !important;
}

/* Global headings */
h1, h2, h3 {
    letter-spacing: -0.3px;
}

/* Sidebar glass */
section[data-testid="stSidebar"] {
    background:
        linear-gradient(180deg, rgba(15,23,42,0.92) 0%, rgba(30,58,138,0.88) 55%, rgba(15,23,42,0.92) 100%) !important;
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    border-right: 1px solid rgba(255,255,255,0.16);
}

section[data-testid="stSidebar"] * {
    color: #f8fafc !important;
}

/* Sidebar filter glass boxes */
section[data-testid="stSidebar"] .stMultiSelect,
section[data-testid="stSidebar"] .stSelectbox,
section[data-testid="stSidebar"] .stRadio {
    background: rgba(255,255,255,0.10) !important;
    border: 1px solid rgba(255,255,255,0.16) !important;
    border-radius: 18px !important;
    padding: 11px 11px 9px 11px !important;
    margin-bottom: 12px !important;
    box-shadow: 0 10px 28px rgba(0,0,0,0.18);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
}

/* Select input inside sidebar */
section[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background: rgba(255,255,255,0.96) !important;
    border-radius: 12px !important;
    border: 1px solid rgba(255,255,255,0.38) !important;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.30);
}

section[data-testid="stSidebar"] [data-baseweb="select"] span,
section[data-testid="stSidebar"] [data-baseweb="select"] input {
    color: #0f172a !important;
}

/* Sidebar buttons */
section[data-testid="stSidebar"] button {
    border-radius: 999px !important;
    background: rgba(255,255,255,0.14) !important;
    border: 1px solid rgba(255,255,255,0.28) !important;
    color: #ffffff !important;
    font-weight: 700 !important;
    box-shadow: 0 8px 18px rgba(0,0,0,0.14);
}

section[data-testid="stSidebar"] button:hover {
    background: rgba(255,255,255,0.24) !important;
    border-color: rgba(255,255,255,0.55) !important;
}

/* Main KPI/card glass */
.card {
    background: rgba(255,255,255,0.72) !important;
    border: 1px solid rgba(255,255,255,0.68) !important;
    border-left: 5px solid rgba(37,99,235,0.76) !important;
    border-radius: 20px !important;
    box-shadow: 0 14px 34px rgba(15,23,42,0.10) !important;
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
}

/* Streamlit metric cards */
div[data-testid="stMetric"] {
    background: rgba(255,255,255,0.70);
    border: 1px solid rgba(255,255,255,0.68);
    border-radius: 20px;
    padding: 16px 18px;
    box-shadow: 0 14px 34px rgba(15,23,42,0.10);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
}

/* Expander as glass chart container */
div[data-testid="stExpander"] {
    background: rgba(255,255,255,0.62) !important;
    border: 1px solid rgba(255,255,255,0.68) !important;
    border-radius: 20px !important;
    box-shadow: 0 14px 34px rgba(15,23,42,0.10);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    overflow: hidden;
}

div[data-testid="stExpander"] details summary {
    background: rgba(255,255,255,0.42) !important;
    border-radius: 18px !important;
    font-weight: 700 !important;
}

/* Tables/dataframes glass feel */
div[data-testid="stDataFrame"] {
    background: rgba(255,255,255,0.70);
    border: 1px solid rgba(255,255,255,0.70);
    border-radius: 18px;
    box-shadow: 0 10px 24px rgba(15,23,42,0.08);
    overflow: hidden;
}

/* Plotly chart wrapper */
div[data-testid="stPlotlyChart"] {
    background: rgba(255,255,255,0.56);
    border: 1px solid rgba(255,255,255,0.62);
    border-radius: 20px;
    padding: 8px;
    box-shadow: 0 14px 30px rgba(15,23,42,0.09);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
}

/* Traffic light circles softer glass */
.traffic-circle {
    box-shadow:
        0 12px 28px rgba(0,0,0,0.20),
        inset 0 1px 0 rgba(255,255,255,0.35) !important;
    border: 1px solid rgba(255,255,255,0.35);
}

/* Download / action buttons */
.stDownloadButton button,
.stButton button {
    border-radius: 999px !important;
    background: linear-gradient(90deg, #1d4ed8, #2563eb) !important;
    color: white !important;
    border: 1px solid rgba(255,255,255,0.42) !important;
    box-shadow: 0 10px 24px rgba(37,99,235,0.25);
    font-weight: 700 !important;
}

.stDownloadButton button:hover,
.stButton button:hover {
    transform: translateY(-1px);
    box-shadow: 0 14px 30px rgba(37,99,235,0.32);
}

/* Inputs in main area */
div[data-baseweb="select"] > div,
div[data-baseweb="input"] {
    border-radius: 12px !important;
}

/* Hide default Streamlit details noise smoother */
hr {
    border-color: rgba(148,163,184,0.30) !important;
}


/* ===== SIDEBAR SCROLL BEHAVIOUR ===== */
/* Buang sticky/freeze behaviour sidebar navigation */
section[data-testid="stSidebar"] > div {
    position: relative !important;
}

section[data-testid="stSidebar"] div[data-testid="stVerticalBlock"] {
    position: relative !important;
    top: auto !important;
}

/* Sidebar ikut scroll sekali */
section[data-testid="stSidebar"] {
    overflow-y: auto !important;
}



/* ===== FIX REFRESH BUTTON / SIDEBAR BUTTON SCROLL ===== */
/* Pastikan button dalam sidebar termasuk Refresh Data Excel tidak fixed/freeze */
section[data-testid="stSidebar"] .stButton,
section[data-testid="stSidebar"] .stButton button {
    position: relative !important;
    top: auto !important;
    right: auto !important;
    bottom: auto !important;
    transform: none !important;
    z-index: auto !important;
}

/* Collapse sidebar button biarkan default Streamlit supaya tidak lari bawah */
button[aria-label*="Collapse"],
button[aria-label*="collapse"],
button[aria-label*="Expand"],
button[aria-label*="expand"],
[data-testid="stSidebarCollapseButton"],
[data-testid="collapsedControl"] {
    position: unset !important;
    top: unset !important;
    right: unset !important;
    bottom: unset !important;
    transform: unset !important;
}

/* Sidebar content scroll normal */
section[data-testid="stSidebar"] {
    overflow-y: auto !important;
}


/* ===== CENTER SIDEBAR COLLAPSE BUTTON ===== */
[data-testid="collapsedControl"] {
    top: 50vh !important;
    transform: translateY(-50%) !important;
    z-index: 99999 !important;
}

[data-testid="stSidebarCollapseButton"] {
    top: 50vh !important;
    transform: translateY(-50%) !important;
    z-index: 99999 !important;
}

</style>
""")

# =======================
# FUNGSI UMUM
# =======================
def format_nilai(nilai):
    """
    Format nombor kepada ringkasan RM.
    Contoh:
    130107903 -> RM 130.1 Juta
    """
    nilai = pd.to_numeric(nilai, errors="coerce")

    if pd.isna(nilai):
        nilai = 0.0

    tanda = "-" if nilai < 0 else ""
    nilai_abs = abs(float(nilai))

    if nilai_abs >= 1_000_000_000:
        return f"{tanda}RM {nilai_abs / 1_000_000_000:.1f} Bilion"

    if nilai_abs >= 1_000_000:
        return f"{tanda}RM {nilai_abs / 1_000_000:.1f} Juta"

    if nilai_abs >= 1_000:
        return f"{tanda}RM {nilai_abs / 1_000:.1f} Ribu"

    return f"{tanda}RM {nilai_abs:.0f}"


def format_comma(nilai):
    """
    Format nombor dengan comma tanpa decimal.
    Contoh: 1234567 -> 1,234,567
    """
    nilai = pd.to_numeric(nilai, errors="coerce")

    if pd.isna(nilai):
        nilai = 0

    return f"{nilai:,.0f}"


def format_comma_no_decimal(nilai):
    """
    Format nombor dengan comma tanpa decimal.
    """
    nilai = pd.to_numeric(nilai, errors="coerce")

    if pd.isna(nilai):
        nilai = 0

    return f"{nilai:,.0f}"


def dataframe_comma_style(df, money_cols=None, percent_cols=None):
    """
    Tukar column numeric tertentu kepada comma style untuk paparan report.
    """
    df_show = df.copy()

    if money_cols is None:
        money_cols = []

    if percent_cols is None:
        percent_cols = []

    for col in money_cols:
        if col in df_show.columns:
            df_show[col] = df_show[col].apply(format_comma)

    for col in percent_cols:
        if col in df_show.columns:
            df_show[col] = (
                pd.to_numeric(df_show[col], errors="coerce")
                .fillna(0)
                .map(lambda x: f"{x:,.2f}%")
            )

    return df_show


def hitung_prestasi(sebenar, sasaran):
    sebenar = pd.to_numeric(sebenar, errors="coerce")
    sasaran = pd.to_numeric(sasaran, errors="coerce")

    if pd.isna(sebenar):
        sebenar = 0.0
    if pd.isna(sasaran) or sasaran == 0:
        return 0.0

    return (sebenar / sasaran) * 100


def to_excel(df, sheet_name="Summary"):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name=sheet_name[:31])
    output.seek(0)
    return output


def to_excel_multi(sheets):
    """
    Download beberapa dataframe dalam satu fail Excel.
    sheets = {"NamaSheet": dataframe}
    """
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        for sheet_name, df_sheet in sheets.items():
            safe_sheet_name = str(sheet_name)[:31]
            df_sheet.to_excel(writer, index=False, sheet_name=safe_sheet_name)
    output.seek(0)
    return output


def bersih_nama_column(df):
    df = df.copy()
    df.columns = df.columns.astype(str).str.strip()
    return df


def clean_numeric_series(series):
    if pd.api.types.is_numeric_dtype(series):
        return pd.to_numeric(series, errors="coerce").fillna(0)

    return (
        series.astype(str)
        .str.replace("RM", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.replace(" ", "", regex=False)
        .pipe(pd.to_numeric, errors="coerce")
        .fillna(0)
    )


def pastikan_numeric(df, columns):
    df = df.copy()
    for col in columns:
        if col in df.columns:
            df[col] = clean_numeric_series(df[col])
    return df


def unique_sorted(series):
    return sorted(series.dropna().astype(str).unique().tolist())



def kemas_label_bajet(trace):
    """Tukar nama legend chart kepada label ringkas."""
    trace.name = (
        str(trace.name)
        .replace("BAJET_JT", "Bajet")
        .replace("SASARAN_JT", "Bajet Qtr")
        .replace("SEBENAR_JT", "Sebenar")
        .replace("BAJET 2025", "Bajet")
        .replace("SASARAN Q1-25", "Bajet Qtr")
        .replace("SEBENAR Q1-25", "Sebenar")
    )
    return trace


def rename_summary_columns(df):
    """Tukar nama column output kepada label ringkas."""
    return df.rename(columns={
        "PTJ1": "PTJ",
        "DESC": "Item",
        "Quarter": "Tempoh",
        "KOD1": "Kod Item",
        "BAJET 2025": "Bajet",
        "SASARAN Q1-25": "Bajet Qtr",
        "SEBENAR Q1-25": "Sebenar 03-2026",
        "SEBENAR 03-2025": "Sebenar 03-2025"
    })



def apply_geran_arrow_labels(fig, orientation="v", threshold_ratio=0.18):
    """
    Label Geran:
    - Text mendatar.
    - Nilai kecil/bertindih dialihkan kepada annotation dengan arrow.
    - Text asal untuk nilai tersebut disembunyikan supaya tidak overlap.
    """
    try:
        for trace in fig.data:
            if getattr(trace, "type", "") != "bar":
                continue

            is_horizontal = orientation == "h" or getattr(trace, "orientation", None) == "h"

            vals = list(trace.x) if is_horizontal else list(trace.y)
            cats = list(trace.y) if is_horizontal else list(trace.x)

            if not vals:
                continue

            numeric_vals = [
                abs(float(pd.to_numeric(v, errors="coerce")))
                for v in vals
                if not pd.isna(pd.to_numeric(v, errors="coerce"))
            ]

            if not numeric_vals:
                continue

            max_val = max(numeric_vals)
            if max_val <= 0:
                continue

            text_list = list(trace.text) if trace.text is not None else [
                format_nilai(v) for v in vals
            ]

            new_text = list(text_list)

            for i, val in enumerate(vals):
                val_num = pd.to_numeric(val, errors="coerce")

                if pd.isna(val_num) or float(val_num) == 0:
                    continue

                # Nilai kecil berpotensi bertindih, jadi guna arrow.
                if abs(float(val_num)) <= max_val * threshold_ratio:
                    label = str(text_list[i]) if i < len(text_list) else format_nilai(val_num)

                    if is_horizontal:
                        fig.add_annotation(
                            x=float(val_num),
                            y=cats[i],
                            text=label,
                            showarrow=True,
                            arrowhead=2,
                            arrowsize=0.8,
                            arrowwidth=1,
                            arrowcolor="rgba(80,80,80,0.70)",
                            ax=55 + ((i % 3) * 18),
                            ay=0,
                            font=dict(
                                size=11,
                                color="black",
                                family="Arial"
                            ),
                            bgcolor="rgba(255,255,255,0.88)",
                            bordercolor="rgba(120,120,120,0.35)",
                            borderwidth=0.5,
                            borderpad=2
                        )
                    else:
                        fig.add_annotation(
                            x=cats[i],
                            y=float(val_num),
                            text=label,
                            showarrow=True,
                            arrowhead=2,
                            arrowsize=0.8,
                            arrowwidth=1,
                            arrowcolor="rgba(80,80,80,0.70)",
                            ax=0,
                            ay=-35 - ((i % 4) * 14),
                            font=dict(
                                size=11,
                                color="black",
                                family="Arial"
                            ),
                            bgcolor="rgba(255,255,255,0.88)",
                            bordercolor="rgba(120,120,120,0.35)",
                            borderwidth=0.5,
                            borderpad=2
                        )

                    if i < len(new_text):
                        new_text[i] = ""

            trace.text = new_text
            trace.texttemplate = "%{text}"
            trace.textposition = "outside"
            trace.textangle = 0
            trace.cliponaxis = False
            trace.constraintext = "none"
            trace.textfont = dict(
                size=11,
                color="black",
                family="Arial"
            )

        fig.update_layout(
            margin=dict(t=170, b=160, l=90, r=110),
            uniformtext_minsize=7,
            uniformtext_mode="show"
        )

        fig.update_xaxes(automargin=True)
        fig.update_yaxes(automargin=True)

    except Exception:
        pass

    return fig



def apply_chart_text_style(fig, size=12, angle=0):
    """
    Paksa nilai/amount keluar pada semua bar chart.
    Tidak apply kepada scatter/line.
    """
    for trace in fig.data:
        if getattr(trace, "type", "") == "bar":
            orientasi = getattr(trace, "orientation", None)

            values = list(trace.x) if orientasi == "h" else list(trace.y)
            current_text = list(trace.text) if trace.text is not None else []

            if not current_text or all(str(x).strip().lower() in ["", "none", "nan", "null"] for x in current_text):
                fallback_text = []

                for val in values:
                    val_num = pd.to_numeric(val, errors="coerce")

                    if pd.isna(val_num):
                        fallback_text.append("")
                    elif abs(float(val_num)) >= 1_000:
                        fallback_text.append(format_nilai(val_num))
                    else:
                        fallback_text.append(f"{float(val_num):,.2f}")

                trace.text = fallback_text

            trace.texttemplate = "%{text}"
            trace.textposition = "outside"
            trace.textangle = angle
            trace.cliponaxis = False
            trace.constraintext = "none"
            trace.textfont = dict(
                size=size,
                family="Arial",
                color="black"
            )

    fig.update_layout(
        margin=dict(t=180, b=150, l=90, r=100),
        uniformtext_minsize=6,
        uniformtext_mode="show"
    )

    fig.update_xaxes(automargin=True)
    fig.update_yaxes(automargin=True)

    return fig


def detect_amount_column(df):
    calon = [
        "Amount in local currency", "AMOUNT IN LOCAL CURRENCY",
        "JUMLAH", "Jumlah", "AMAUN", "Amaun", "AMOUNT", "Amount",
        "NILAI", "Nilai", "BAKI", "Baki", "BALANCE", "Balance",
        "DEBIT", "Debit", "KREDIT", "Kredit", "CREDIT", "Credit",
        "RM", "TOTAL", "Total"
    ]

    for col in calon:
        if col in df.columns:
            return col

    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    if numeric_cols:
        return numeric_cols[0]

    for col in df.columns:
        converted = clean_numeric_series(df[col])
        if converted.abs().sum() > 0:
            return col

    return None


# =======================
# LOAD DATA BELANJA & HASIL
# Nota:
# - Belanja & Hasil kini guna SATU fail Excel sahaja:
#   JPKA_ANALISA PK CIDB 03-2026.xlsx
# - Comparison Carta 2 menggunakan column dalam fail yang sama:
#   SEBENAR 03-2025
# =======================
def load_data():
    df_dict = {}
    errors = []

    files = {
        "03-2026": "JPKA_ANALISA PK CIDB 03-2026.xlsx"
    }

    for q, filename in files.items():
        try:
            df = pd.read_excel(filename, sheet_name="All2")
            df = bersih_nama_column(df)

            if "KOD" in df.columns and "KOD1" not in df.columns:
                df = df.rename(columns={"KOD": "KOD1"})

            # Standardize nama column untuk dashboard.
            # Nama dalaman lama dikekalkan supaya chart/slicer sedia ada masih jalan:
            # BAJET 2025       = Bajet tahunan 2026
            # SASARAN Q1-25    = Bajet/Sasaran 03-2026
            # SEBENAR Q1-25    = Sebenar 03-2026
            rename_map = {
                "BAJET 2026": "BAJET 2025",
                "Bajet 2026": "BAJET 2025",
                "BAJET2026": "BAJET 2025",

                "SASARAN Q1-26": "SASARAN Q1-25",
                "SASARAN 03-2026": "SASARAN Q1-25",
                "BAJET 03-2026": "SASARAN Q1-25",
                "BAJET QTR": "SASARAN Q1-25",

                "SEBENAR Q1-26": "SEBENAR Q1-25",
                "SEBENAR 03-2026": "SEBENAR Q1-25",

                "SEBENAR Q1-25": "SEBENAR 03-2025",
                "SEBENAR 03-2025": "SEBENAR 03-2025"
            }

            # Rename hanya jika target belum wujud supaya column tidak tertimpa.
            safe_rename = {}
            for old_col, new_col in rename_map.items():
                if old_col in df.columns:
                    if old_col == new_col or new_col not in df.columns:
                        safe_rename[old_col] = new_col

            df = df.rename(columns=safe_rename)

            # Fallback jika column comparison belum ada.
            # Untuk file baru, column ini sepatutnya memang wujud.
            if "SEBENAR 03-2025" not in df.columns:
                df["SEBENAR 03-2025"] = 0

            df["Sumber"] = q
            df["Quarter"] = q
            df["Tahun"] = int(q.split("-")[1])

            numeric_cols = [
                "BAJET 2025",
                "SASARAN Q1-25",
                "SEBENAR Q1-25",
                "SEBENAR 03-2025"
            ]
            df = pastikan_numeric(df, numeric_cols)

            df_dict[q] = df

        except Exception as e:
            errors.append(f"{q} - {filename}: {e}")

    return df_dict, errors


# =======================
# LOAD DATA GERAN - WORKSHEET DATA SAHAJA
# Nota: tidak guna cache supaya perubahan Excel terus dibaca semula.
# =======================
def load_data_geran():
    filename = "GL ADV 03-2026 14052026.XLSX"

    try:
        df_data = pd.read_excel(filename, sheet_name="DATA")
        df_data = bersih_nama_column(df_data)
        return df_data, ""

    except Exception as e:
        return pd.DataFrame(), f"{filename}: {e}"


# =======================
# PREPARE DATA
# =======================
df_dict, belanja_errors = load_data()
df_geran, geran_error = load_data_geran()

# =======================
# MENU UTAMA DI MAIN PAGE
# =======================
html("""
<div style="
    text-align:center;
    padding:18px 18px 10px 18px;
    border-radius:24px;
    background:rgba(255,255,255,0.55);
    border:1px solid rgba(255,255,255,0.72);
    margin-bottom:12px;
    box-shadow:0 14px 34px rgba(15,23,42,0.10);
    backdrop-filter:blur(16px);
    -webkit-backdrop-filter:blur(16px);
">
    <div style="font-size:38px; line-height:1;">📊</div>
    <h1 style="margin:8px 0 2px 0; font-weight:800; font-size:30px; color:#1e293b;">
        PRESTASI KEWANGAN CIDB
    </h1>
    <p style="margin:0; color:#64748b; font-size:13px;">
        Dashboard Prestasi Kewangan
    </p>
</div>
""")

menu_label = st.pills(
    "Pilih Modul",
    options=["Belanja & Hasil", "Geran", "P&L", "Balance Sheet", "Cash Flow"],
    default="Belanja & Hasil",
    label_visibility="collapsed"
)

menu_map = {
    "Belanja & Hasil": "1. Belanja & Hasil",
    "Geran": "2. Geran",
    "P&L": "3. P&L",
    "Balance Sheet": "4. Balance Sheet",
    "Cash Flow": "5. Cash Flow",
}

menu = menu_map.get(menu_label, "1. Belanja & Hasil")

tajuk_utama = {
    "1. Belanja & Hasil": "📊 PRESTASI PERBELANJAAN DAN HASIL CIDB",
    "2. Geran": "📊 PRESTASI GERAN",
    "3. P&L": "📊 Profit & Loss",
    "4. Balance Sheet": "📊 Balance Sheet",
    "5. Cash Flow": "📊 Cash Flow",
}

html(f"""
<h2 style="text-align:center; font-weight:700; font-size:22px; color:#334155; margin-top:8px; margin-bottom:16px;">
    {tajuk_utama.get(menu, "📊 PRESTASI KEWANGAN CIDB")}
</h2>
""")

st.sidebar.markdown("### 🔎 Slicer / Filter")
st.sidebar.markdown("---")
if st.sidebar.button("🔄 Refresh Data Excel"):
    st.rerun()



# =======================
# MENU 1: BELANJA & HASIL
# =======================
if menu == "1. Belanja & Hasil":
    if not df_dict:
        st.error("Data Belanja & Hasil tidak berjaya dimuatkan.")
        if belanja_errors:
            with st.expander("Lihat detail error file", expanded=True):
                for err in belanja_errors:
                    st.write(f"- {err}")
        st.stop()

    quarters_available = [q for q in ["03-2026"] if q in df_dict]

    with st.sidebar:
        st.markdown("### 🔎 PILIHAN ")

    # Tempoh global tidak dipaparkan sebagai slicer.
    # Dashboard utama auto guna tempoh terkini.
    # Carta 2 masih ada filter comparison tempoh sendiri.
    pilih_quarter = ["03-2026"] if "03-2026" in quarters_available else quarters_available[-1:]

    if not pilih_quarter:
        st.warning("Tiada tempoh data tersedia.")
        st.stop()

    dfs = [df_dict[q] for q in pilih_quarter if q in df_dict]
    if not dfs:
        st.warning("Tiada data untuk Quarter yang dipilih.")
        st.stop()

    df_tapis = pd.concat(dfs, ignore_index=True)
    df_tapis = bersih_nama_column(df_tapis)

    required_cols = [
        "PTJ", "PTJ1", "Kategori", "DESC", "KOD1",
        "BAJET 2025", "SASARAN Q1-25", "SEBENAR Q1-25", "SEBENAR 03-2025", "Quarter"
    ]
    missing_cols = [col for col in required_cols if col not in df_tapis.columns]
    if missing_cols:
        st.error("Column berikut tiada dalam data Belanja & Hasil:")
        st.write(missing_cols)
        st.stop()

    # =======================
    # EXCEL-STYLE CONNECTED SLICER - FINAL V2
    #
    # Default:
    # - Semua slicer selected all.
    #
    # Rule:
    # - Pejabat tak boleh kosong. Jika clear, auto pilih semua Pejabat.
    # - PTJ tak boleh kosong. Options ikut Pejabat. Jika clear, auto pilih semua PTJ berkaitan Pejabat.
    # - Kategori at least 1 selected. Jika clear, auto pilih semua Kategori berkaitan Pejabat/PTJ.
    # - Item boleh clear dan refer Kategori.
    # - Kod Item boleh clear dan refer Item.
    # - Contoh pilih Kategori = Hasil:
    #   Pejabat/PTJ/Item/Kod Item auto tinggal dan auto selected yang berkaitan.
    # =======================

    def _as_list(value):
        if value is None:
            return []
        if isinstance(value, list):
            return value
        return [value]

    def _unique_col(df_source, col):
        if col not in df_source.columns:
            return []
        return unique_sorted(df_source[col])

    def _filter_df(df_source, filters):
        df_temp = df_source.copy()
        for col, vals in filters.items():
            vals = _as_list(vals)
            if vals and col in df_temp.columns:
                df_temp = df_temp[df_temp[col].astype(str).isin(vals)]
        return df_temp

    def _set_all_from_df(df_related):
        """Auto select semua slicer mengikut dataframe berkaitan."""
        st.session_state["belanja_pejabat_final2"] = _unique_col(df_related, "PTJ")
        st.session_state["belanja_ptj_final2"] = _unique_col(df_related, "PTJ1")
        st.session_state["belanja_kategori_final2"] = _unique_col(df_related, "Kategori")
        st.session_state["belanja_item_final2"] = _unique_col(df_related, "DESC")
        st.session_state["belanja_kod_item_final2"] = _unique_col(df_related, "KOD1")

    def _set_child_slicers_preserve_kategori(df_related):
        """
        Auto-sync slicer anak tanpa reset pilihan Kategori user.
        Contoh: jika Kategori = Hasil, ubah/clear PTJ tidak akan tukar balik
        kepada semua kategori selagi Hasil masih wujud dalam konteks data baharu.
        """
        if df_related.empty:
            return

        kategori_current = _as_list(st.session_state.get("belanja_kategori_final2", []))
        kategori_valid = _unique_col(df_related, "Kategori")

        kategori_keep = [x for x in kategori_current if x in set(kategori_valid)]

        if kategori_current and kategori_keep:
            kategori_vals = kategori_keep
            df_kategori = _filter_df(df_related, {"Kategori": kategori_vals})
        else:
            kategori_vals = kategori_valid
            df_kategori = df_related.copy()

        if df_kategori.empty:
            df_kategori = df_related.copy()
            kategori_vals = _unique_col(df_kategori, "Kategori")

        st.session_state["belanja_pejabat_final2"] = _unique_col(df_kategori, "PTJ")
        st.session_state["belanja_ptj_final2"] = _unique_col(df_kategori, "PTJ1")
        st.session_state["belanja_kategori_final2"] = kategori_vals
        st.session_state["belanja_item_final2"] = _unique_col(df_kategori, "DESC")
        st.session_state["belanja_kod_item_final2"] = _unique_col(df_kategori, "KOD1")

    def _base_df():
        return st.session_state.get("_belanja_slicer_base_df_v2", pd.DataFrame())

    def _sync_from_pejabat():
        df_base = _base_df()
        if df_base.empty:
            return

        pejabat_vals = _as_list(st.session_state.get("belanja_pejabat_final2", []))
        if not pejabat_vals:
            pejabat_vals = _unique_col(df_base, "PTJ")
            st.session_state["belanja_pejabat_final2"] = pejabat_vals

        df_related = _filter_df(df_base, {"PTJ": pejabat_vals})
        if df_related.empty:
            df_related = df_base.copy()

        _set_child_slicers_preserve_kategori(df_related)

    def _sync_from_ptj():
        df_base = _base_df()
        if df_base.empty:
            return

        pejabat_vals = _as_list(st.session_state.get("belanja_pejabat_final2", []))
        if not pejabat_vals:
            pejabat_vals = _unique_col(df_base, "PTJ")
            st.session_state["belanja_pejabat_final2"] = pejabat_vals

        df_by_pejabat = _filter_df(df_base, {"PTJ": pejabat_vals})

        ptj_vals = _as_list(st.session_state.get("belanja_ptj_final2", []))
        valid_ptj = _unique_col(df_by_pejabat, "PTJ1")
        ptj_vals = [x for x in ptj_vals if x in set(valid_ptj)]

        if not ptj_vals:
            ptj_vals = valid_ptj
            st.session_state["belanja_ptj_final2"] = ptj_vals

        df_related = _filter_df(df_by_pejabat, {"PTJ1": ptj_vals})
        if df_related.empty:
            df_related = df_by_pejabat.copy()

        _set_child_slicers_preserve_kategori(df_related)

    def _sync_from_kategori():
        df_base = _base_df()
        if df_base.empty:
            return

        kategori_vals = _as_list(st.session_state.get("belanja_kategori_final2", []))

        # Kategori wajib at least 1. Jika clear, auto pilih semua kategori.
        if not kategori_vals:
            kategori_vals = _unique_col(df_base, "Kategori")
            st.session_state["belanja_kategori_final2"] = kategori_vals

        df_related = _filter_df(df_base, {"Kategori": kategori_vals})
        if df_related.empty:
            df_related = df_base.copy()

        # Pilih kategori user kekal, slicer lain auto ikut kategori.
        # Item/Kod Item auto selected semua yang berkaitan bila kategori dipilih.
        st.session_state["belanja_pejabat_final2"] = _unique_col(df_related, "PTJ")
        st.session_state["belanja_ptj_final2"] = _unique_col(df_related, "PTJ1")
        st.session_state["belanja_kategori_final2"] = kategori_vals
        st.session_state["belanja_item_final2"] = _unique_col(df_related, "DESC")
        st.session_state["belanja_kod_item_final2"] = _unique_col(df_related, "KOD1")

    def _sync_from_item():
        df_base = _base_df()
        if df_base.empty:
            return

        kategori_vals = _as_list(st.session_state.get("belanja_kategori_final2", []))
        if not kategori_vals:
            kategori_vals = _unique_col(df_base, "Kategori")
            st.session_state["belanja_kategori_final2"] = kategori_vals

        df_by_kategori = _filter_df(df_base, {"Kategori": kategori_vals})

        item_vals = _as_list(st.session_state.get("belanja_item_final2", []))
        valid_item = _unique_col(df_by_kategori, "DESC")
        item_vals = [x for x in item_vals if x in set(valid_item)]

        # Item boleh clear.
        # Jika clear, maksudnya All Item untuk kategori dipilih.
        if item_vals:
            df_related = _filter_df(df_by_kategori, {"DESC": item_vals})
        else:
            df_related = df_by_kategori.copy()

        if df_related.empty:
            df_related = df_by_kategori.copy()

        st.session_state["belanja_pejabat_final2"] = _unique_col(df_related, "PTJ")
        st.session_state["belanja_ptj_final2"] = _unique_col(df_related, "PTJ1")
        st.session_state["belanja_kategori_final2"] = _unique_col(df_related, "Kategori")
        st.session_state["belanja_item_final2"] = item_vals

        # Kod Item WAJIB refer Item yang selected.
        # Bila Item dipilih semula selepas clear, Kod Item auto select semua kod berkaitan Item itu.
        # Jika Item kosong, Kod Item ikut semua kod dalam kategori.
        st.session_state["belanja_kod_item_final2"] = _unique_col(df_related, "KOD1")

    def _sync_from_kod_item():
        df_base = _base_df()
        if df_base.empty:
            return

        kategori_vals = _as_list(st.session_state.get("belanja_kategori_final2", []))
        if not kategori_vals:
            kategori_vals = _unique_col(df_base, "Kategori")
            st.session_state["belanja_kategori_final2"] = kategori_vals

        item_vals = _as_list(st.session_state.get("belanja_item_final2", []))
        kod_vals = _as_list(st.session_state.get("belanja_kod_item_final2", []))

        # Kod Item refer kepada Item.
        # Jika Item kosong, guna konteks Kategori sebagai fallback.
        if item_vals:
            df_by_context = _filter_df(df_base, {"DESC": item_vals})
        else:
            df_by_context = _filter_df(df_base, {"Kategori": kategori_vals})

        valid_kod = _unique_col(df_by_context, "KOD1")
        kod_vals = [x for x in kod_vals if x in set(valid_kod)]

        # Kod Item boleh clear.
        # Jika clear, maksudnya All Kod Item untuk Item dipilih.
        if kod_vals:
            df_related = _filter_df(df_by_context, {"KOD1": kod_vals})
        else:
            df_related = df_by_context.copy()

        if df_related.empty:
            df_related = df_by_context.copy()

        st.session_state["belanja_pejabat_final2"] = _unique_col(df_related, "PTJ")
        st.session_state["belanja_ptj_final2"] = _unique_col(df_related, "PTJ1")
        st.session_state["belanja_kategori_final2"] = _unique_col(df_related, "Kategori")
        st.session_state["belanja_item_final2"] = [
            x for x in item_vals
            if x in set(_unique_col(df_related, "DESC"))
        ]
        st.session_state["belanja_kod_item_final2"] = kod_vals

    with st.sidebar:
        df_slicer_base = df_tapis.copy()
        st.session_state["_belanja_slicer_base_df_v2"] = df_slicer_base

        full_pejabat = _unique_col(df_slicer_base, "PTJ")
        full_ptj = _unique_col(df_slicer_base, "PTJ1")
        full_kategori = _unique_col(df_slicer_base, "Kategori")
        full_item = _unique_col(df_slicer_base, "DESC")
        full_kod_item = _unique_col(df_slicer_base, "KOD1")

        if "belanja_final2_slicer_initialized" not in st.session_state:
            st.session_state["belanja_pejabat_final2"] = full_pejabat
            st.session_state["belanja_ptj_final2"] = full_ptj
            st.session_state["belanja_kategori_final2"] = full_kategori
            st.session_state["belanja_item_final2"] = full_item
            st.session_state["belanja_kod_item_final2"] = full_kod_item
            st.session_state["belanja_final2_slicer_initialized"] = True

        # Clean invalid values after tempoh change.
        valid_map = {
            "belanja_pejabat_final2": full_pejabat,
            "belanja_ptj_final2": full_ptj,
            "belanja_kategori_final2": full_kategori,
            "belanja_item_final2": full_item,
            "belanja_kod_item_final2": full_kod_item,
        }

        for key_v, options_v in valid_map.items():
            current_v = _as_list(st.session_state.get(key_v, []))
            cleaned_v = [x for x in current_v if x in set(options_v)]
            st.session_state[key_v] = cleaned_v

        # Mandatory defaults if accidentally empty.
        if not st.session_state.get("belanja_pejabat_final2", []):
            st.session_state["belanja_pejabat_final2"] = full_pejabat

        pejabat_vals_for_ptj = _as_list(st.session_state.get("belanja_pejabat_final2", []))
        df_for_ptj = _filter_df(df_slicer_base, {"PTJ": pejabat_vals_for_ptj})
        opt_ptj = _unique_col(df_for_ptj, "PTJ1")

        if not st.session_state.get("belanja_ptj_final2", []):
            st.session_state["belanja_ptj_final2"] = opt_ptj

        if not st.session_state.get("belanja_kategori_final2", []):
            st.session_state["belanja_kategori_final2"] = full_kategori

        # Options render:
        pejabat_selected = _as_list(st.session_state.get("belanja_pejabat_final2", []))
        df_parent_pejabat = _filter_df(df_slicer_base, {"PTJ": pejabat_selected})
        opt_ptj = _unique_col(df_parent_pejabat, "PTJ1")

        ptj_selected = _as_list(st.session_state.get("belanja_ptj_final2", []))
        ptj_selected = [x for x in ptj_selected if x in set(opt_ptj)]
        if not ptj_selected:
            ptj_selected = opt_ptj
            st.session_state["belanja_ptj_final2"] = ptj_selected

        df_parent = _filter_df(df_parent_pejabat, {"PTJ1": ptj_selected})

        kategori_selected = _as_list(st.session_state.get("belanja_kategori_final2", []))
        kategori_selected = [x for x in kategori_selected if x in set(_unique_col(df_parent, "Kategori"))]
        if not kategori_selected:
            kategori_selected = _unique_col(df_parent, "Kategori")
            st.session_state["belanja_kategori_final2"] = kategori_selected

        # Item/Kod options refer Kategori.
        # Item boleh clear = All Item.
        # Kod Item boleh clear = All Kod Item.
        # Kod Item options ikut Kategori & Item jika Item dipilih.
        item_selected = _as_list(st.session_state.get("belanja_item_final2", []))
        kod_selected = _as_list(st.session_state.get("belanja_kod_item_final2", []))

        df_by_kategori = _filter_df(df_parent, {"Kategori": kategori_selected})

        opt_item = _unique_col(df_by_kategori, "DESC")
        item_selected = [x for x in item_selected if x in set(opt_item)]
        st.session_state["belanja_item_final2"] = item_selected

        # Kod Item options refer kepada Item.
        # Jika Item kosong, fallback kepada Kategori supaya options masih wujud.
        df_for_kod_options = (
            _filter_df(df_parent, {"DESC": item_selected})
            if item_selected
            else df_by_kategori
        )

        opt_kod = _unique_col(df_for_kod_options, "KOD1")
        kod_selected = [x for x in kod_selected if x in set(opt_kod)]

        # Jika Item ada selected tetapi Kod Item kosong/stale,
        # auto pilih semua Kod Item yang berkaitan dengan Item selected.
        if item_selected and not kod_selected:
            kod_selected = opt_kod

        st.session_state["belanja_kod_item_final2"] = kod_selected

        # Susunan slicer:
        # Kategori -> Pejabat -> PTJ -> Item -> Kod Item
        st.multiselect(
            "Pilih Kategori",
            _unique_col(df_parent, "Kategori"),
            key="belanja_kategori_final2",
            on_change=_sync_from_kategori,
            placeholder="Pilih Kategori"
        )

        st.multiselect(
            "Pilih Pejabat",
            full_pejabat,
            key="belanja_pejabat_final2",
            on_change=_sync_from_pejabat,
            placeholder="Pilih Pejabat"
        )

        # PTJ Pills - boleh pilih banyak PTJ tanpa Ctrl.
        def _sync_from_ptj_pills():
            ptj_pills = _as_list(st.session_state.get("ptj_pills_multi_final2", []))

            if not ptj_pills:
                return

            df_base_pills = _base_df()

            pejabat_vals = _as_list(st.session_state.get("belanja_pejabat_final2", []))
            if not pejabat_vals:
                pejabat_vals = _unique_col(df_base_pills, "PTJ")

            df_ptj_pills = _filter_df(
                df_base_pills,
                {
                    "PTJ": pejabat_vals,
                    "PTJ1": ptj_pills
                }
            )

            if df_ptj_pills.empty:
                return

            # Preserve Kategori semasa jika masih valid dalam PTJ yang dipilih.
            st.session_state["belanja_ptj_final2"] = ptj_pills
            _set_child_slicers_preserve_kategori(df_ptj_pills)
            st.session_state["belanja_ptj_final2"] = [
                x for x in ptj_pills
                if x in set(_unique_col(df_ptj_pills, "PTJ1"))
            ]

        st.pills(
            "⚡ Pilih PTJ",
            options=opt_ptj,
            selection_mode="multi",
            key="ptj_pills_multi_final2",
            on_change=_sync_from_ptj_pills
        )

        st.multiselect(
            "Pilih PTJ (Multi Select)",
            opt_ptj,
            key="belanja_ptj_final2",
            on_change=_sync_from_ptj,
            placeholder="Pilih PTJ"
        )

        # Item Pills - boleh pilih banyak item tanpa Ctrl.
        def _sync_from_item_pills():
            item_pills = _as_list(st.session_state.get("item_pills_multi_final2", []))

            if not item_pills:
                return

            df_base_pills = _base_df()

            kategori_pills = _as_list(st.session_state.get("belanja_kategori_final2", []))
            if not kategori_pills:
                kategori_pills = _unique_col(df_base_pills, "Kategori")

            df_item_pills = _filter_df(
                df_base_pills,
                {
                    "Kategori": kategori_pills,
                    "DESC": item_pills
                }
            )

            if df_item_pills.empty:
                return

            st.session_state["belanja_item_final2"] = item_pills
            st.session_state["belanja_kod_item_final2"] = _unique_col(df_item_pills, "KOD1")
            st.session_state["belanja_pejabat_final2"] = _unique_col(df_item_pills, "PTJ")
            st.session_state["belanja_ptj_final2"] = _unique_col(df_item_pills, "PTJ1")
            st.session_state["belanja_kategori_final2"] = _unique_col(df_item_pills, "Kategori")

        st.pills(
            "⚡ Pilih Item",
            options=opt_item,
            selection_mode="multi",
            key="item_pills_multi_final2",
            on_change=_sync_from_item_pills
        )

        st.multiselect(
            "Pilih Item (Multi Select)",
            opt_item,
            key="belanja_item_final2",
            on_change=_sync_from_item,
            placeholder="Semua Item"
        )

        # Kod Item Pills - boleh pilih banyak kod tanpa Ctrl.
        def _sync_from_kod_pills():
            kod_pills = _as_list(st.session_state.get("kod_pills_multi_final2", []))

            if not kod_pills:
                return

            df_base_pills = _base_df()

            item_vals = _as_list(st.session_state.get("belanja_item_final2", []))
            kategori_vals = _as_list(st.session_state.get("belanja_kategori_final2", []))

            filters = {"KOD1": kod_pills}
            if item_vals:
                filters["DESC"] = item_vals
            elif kategori_vals:
                filters["Kategori"] = kategori_vals

            df_kod_pills = _filter_df(df_base_pills, filters)

            if df_kod_pills.empty:
                return

            st.session_state["belanja_kod_item_final2"] = kod_pills
            st.session_state["belanja_item_final2"] = _unique_col(df_kod_pills, "DESC")
            st.session_state["belanja_pejabat_final2"] = _unique_col(df_kod_pills, "PTJ")
            st.session_state["belanja_ptj_final2"] = _unique_col(df_kod_pills, "PTJ1")
            st.session_state["belanja_kategori_final2"] = _unique_col(df_kod_pills, "Kategori")

        st.pills(
            "⚡ Pilih Kod Item",
            options=opt_kod,
            selection_mode="multi",
            key="kod_pills_multi_final2",
            on_change=_sync_from_kod_pills
        )

        st.multiselect(
            "Pilih Kod Item (Multi Select)",
            opt_kod,
            key="belanja_kod_item_final2",
            on_change=_sync_from_kod_item,
            placeholder="Semua Kod Item"
        )

        if st.button("♻️ Reset Slicer Belanja & Hasil", key="reset_slicer_belanja_final2"):
            for key in [
                "belanja_pejabat_final2",
                "belanja_ptj_final2",
                "belanja_kategori_final2",
                "belanja_item_final2",
                "belanja_kod_item_final2",
                "ptj_pills_multi_final2",
                "item_pills_multi_final2",
                "kod_pills_multi_final2",
                "belanja_final2_slicer_initialized",
                "belanja_pejabat_final",
                "belanja_ptj_final",
                "belanja_kategori_final",
                "belanja_item_final",
                "belanja_kod_item_final",
                "belanja_final_slicer_initialized",
            ]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

    pilih_ptj = _as_list(st.session_state.get("belanja_pejabat_final2", []))
    pilih_ptj1 = _as_list(st.session_state.get("belanja_ptj_final2", []))
    pilih_kategori = _as_list(st.session_state.get("belanja_kategori_final2", []))
    pilih_desc = _as_list(st.session_state.get("belanja_item_final2", []))
    pilih_kod1 = _as_list(st.session_state.get("belanja_kod_item_final2", []))

    # Mandatory safety.
    if not pilih_ptj:
        pilih_ptj = _unique_col(df_tapis, "PTJ")
        st.session_state["belanja_pejabat_final2"] = pilih_ptj

    df_tapis = df_tapis[
        df_tapis["PTJ"].astype(str).isin(pilih_ptj)
    ].copy()

    opt_ptj_final = _unique_col(df_tapis, "PTJ1")
    if not pilih_ptj1:
        pilih_ptj1 = opt_ptj_final
        st.session_state["belanja_ptj_final2"] = pilih_ptj1

    df_tapis = df_tapis[
        df_tapis["PTJ1"].astype(str).isin(pilih_ptj1)
    ].copy()

    opt_kategori_final = _unique_col(df_tapis, "Kategori")
    if not pilih_kategori:
        pilih_kategori = opt_kategori_final
        st.session_state["belanja_kategori_final2"] = pilih_kategori

    df_tapis = df_tapis[
        df_tapis["Kategori"].astype(str).isin(pilih_kategori)
    ].copy()

    # Item boleh clear = All Item.
    if pilih_desc:
        df_tapis = df_tapis[
            df_tapis["DESC"].astype(str).isin(pilih_desc)
        ].copy()

    # Kod Item boleh clear = All Kod Item, dan refer Item.
    if pilih_kod1:
        df_tapis = df_tapis[
            df_tapis["KOD1"].astype(str).isin(pilih_kod1)
        ].copy()

    if df_tapis.empty:
        st.warning("Tiada data selepas tapisan dibuat.")
        st.stop()

    df_akhir = df_tapis.copy()
    df_akhir["Jenis_Belanja"] = df_akhir["Kategori"].apply(
        lambda x:
        "Mengurus" if "Mengurus" in str(x) else
        "Program" if "Program" in str(x) else
        "Modal" if "Modal" in str(x) else
        "Hasil" if "Hasil" in str(x) else
        "Lain-lain"
    )

    st.markdown("### 🚦 STATUS PRESTASI PTJ")

    df_akhir["Prestasi_%"] = df_akhir.apply(
        lambda row: hitung_prestasi(row["SEBENAR Q1-25"], row["SASARAN Q1-25"]),
        axis=1
    )

    df_group = df_akhir.groupby("PTJ1", as_index=False).agg({
        "BAJET 2025": "sum",
        "SASARAN Q1-25": "sum",
        "SEBENAR Q1-25": "sum"
    })

    # Prestasi_% lama dikekalkan untuk status lampu / drilldown.
    # Formula lama: Sebenar / Sasaran
    df_group["Prestasi_%"] = df_group.apply(
        lambda row: hitung_prestasi(row["SEBENAR Q1-25"], row["SASARAN Q1-25"]),
        axis=1
    )

    # Formula baharu untuk Carta 4:
    # % Prestasi   = SEBENAR / BAJET
    # % Sasaran    = SASARAN / BAJET
    # % Pencapaian = SEBENAR / SASARAN

    # Jika BAJET kosong / 0:
    # - Papar nilai graf = 0%
    # - Papar nota #DIV/0! pada label

    df_group["Nota_DIV0"] = df_group["BAJET 2025"].apply(
        lambda x: "#DIV/0!" if pd.to_numeric(x, errors="coerce") in [0, 0.0] else ""
    )

    df_group["% Prestasi"] = df_group.apply(
        lambda row: 0
        if pd.to_numeric(row["BAJET 2025"], errors="coerce") in [0, 0.0]
        else hitung_prestasi(row["SEBENAR Q1-25"], row["BAJET 2025"]),
        axis=1
    )

    df_group["% Sasaran"] = df_group.apply(
        lambda row: 0
        if pd.to_numeric(row["BAJET 2025"], errors="coerce") in [0, 0.0]
        else hitung_prestasi(row["SASARAN Q1-25"], row["BAJET 2025"]),
        axis=1
    )

    df_group["% Pencapaian"] = df_group.apply(
        lambda row: 0
        if pd.to_numeric(row["SASARAN Q1-25"], errors="coerce") in [0, 0.0]
        else hitung_prestasi(row["SEBENAR Q1-25"], row["SASARAN Q1-25"]),
        axis=1
    )

    hebat = len(df_group[df_group["Prestasi_%"] > 95])
    bagus = len(df_group[(df_group["Prestasi_%"] >= 85) & (df_group["Prestasi_%"] <= 94.99)])
    usaha = len(df_group[df_group["Prestasi_%"] < 85])
    total = len(df_group)

    total_bajet = df_akhir["BAJET 2025"].sum()
    total_sebenar = df_akhir["SEBENAR Q1-25"].sum()
    total_sasaran = df_akhir["SASARAN Q1-25"].sum()

    # Area traffic light:
    # SASARAN    = Sasaran / Bajet
    # PRESTASI   = Sebenar / Bajet
    # PENCAPAIAN = Sebenar / Sasaran
    sasaran_pct = hitung_prestasi(total_sasaran, total_bajet)
    prestasi_pct = hitung_prestasi(total_sebenar, total_bajet)
    pencapaian = hitung_prestasi(total_sebenar, total_sasaran)

    sasaran_int = round(sasaran_pct)
    prestasi_int = round(prestasi_pct)
    pencapaian_int = round(pencapaian)

    col1, col2, col3, col4 = st.columns([1, 1, 1, 1.2])

    if "show_drill_belanja" not in st.session_state:
        st.session_state.show_drill_belanja = None
        st.session_state.drill_title_belanja = ""

    with col1:
        if st.button("🟢", key="hebat_btn"):
            st.session_state.show_drill_belanja = "hebat"
            st.session_state.drill_title_belanja = "Senarai PTJ1 Hebat (> 95%)"
        html(f"""
        <div style="text-align:center">
            <strong style="color:black; font-size:15px;">&gt; 95%</strong><br>
            <div class="traffic-circle" style="background-color:#27ae60;">{hebat}</div>
            <h4 style="color:#27ae60;">Hebat!</h4>
        </div>
        """)

    with col2:
        if st.button("🟡", key="bagus_btn"):
            st.session_state.show_drill_belanja = "bagus"
            st.session_state.drill_title_belanja = "Senarai PTJ1 Bagus (85% - 94%)"
        html(f"""
        <div style="text-align:center">
            <strong style="color:black; font-size:15px;">85% - 94%</strong><br>
            <div class="traffic-circle" style="background-color:#f1c40f; color:#2c3e50;">{bagus}</div>
            <h4 style="color:#f1c40f;">Bagus!</h4>
        </div>
        """)

    with col3:
        if st.button("🔴", key="usaha_btn"):
            st.session_state.show_drill_belanja = "usaha"
            st.session_state.drill_title_belanja = "Senarai PTJ1 Usaha Lagi (< 85%)"
        html(f"""
        <div style="text-align:center">
            <strong style="color:black; font-size:15px;">&lt; 85%</strong><br>
            <div class="traffic-circle" style="background-color:#e74c3c;">{usaha}</div>
            <h4 style="color:#e74c3c;">Usaha lagi!</h4>
        </div>
        """)

    with col4:
        html(f"""
        <div style="text-align:center; padding-top:15px;">
            <h1 style="margin:0;color:#2c3e50;font-size:2.2em;">{total}</h1>
            <h5 style="margin:0;color:#2c3e50;">Jumlah PTJ</h5>
            <hr style="margin:8px 0;">
            <p style="margin:3px 0;"><strong>SASARAN</strong> {sasaran_int}%</p>
            <p style="margin:3px 0;"><strong>PRESTASI</strong> {prestasi_int}%</p>
            <h3 style="color:#27ae60;">PENCAPAIAN {pencapaian_int}%</h3>
        </div>
        """)

    if st.session_state.show_drill_belanja:
        st.subheader(st.session_state.drill_title_belanja)
        if st.session_state.show_drill_belanja == "hebat":
            df_show = df_group[df_group["Prestasi_%"] > 95].sort_values("Prestasi_%", ascending=False)
        elif st.session_state.show_drill_belanja == "bagus":
            df_show = df_group[
                (df_group["Prestasi_%"] >= 85) &
                (df_group["Prestasi_%"] <= 94.99)
            ].sort_values("Prestasi_%", ascending=False)
        else:
            df_show = df_group[df_group["Prestasi_%"] < 85].sort_values("Prestasi_%", ascending=False)

        if not df_show.empty:
            st.dataframe(df_show[["PTJ1", "Prestasi_%"]].rename(columns={"PTJ1": "PTJ"}).round(2), use_container_width=True, hide_index=True)
        else:
            st.info("Tiada rekod untuk kategori ini.")

        if st.button("❌ Tutup Senarai", type="primary"):
            st.session_state.show_drill_belanja = None
            st.rerun()

    with st.expander("📋 RINGKASAN KESELURUHAN", expanded=False):
        for q in pilih_quarter:
            df_q = df_akhir[df_akhir["Quarter"] == q]
            with st.expander(f"Tempoh {q}", expanded=True):
                col_k1, col_k2, col_k3, col_k4 = st.columns(4)
                jenis_list = [
                    ("Mengurus", "BELANJA MENGURUS", col_k1),
                    ("Program", "BELANJA PROGRAM", col_k2),
                    ("Modal", "BELANJA MODAL", col_k3),
                    ("Hasil", "HASIL", col_k4)
                ]
                for jenis, tajuk, col in jenis_list:
                    b = df_q[df_q["Jenis_Belanja"] == jenis]["BAJET 2025"].sum()
                    s = df_q[df_q["Jenis_Belanja"] == jenis]["SASARAN Q1-25"].sum()
                    se = df_q[df_q["Jenis_Belanja"] == jenis]["SEBENAR Q1-25"].sum()
                    with col:
                        html(f"""
                        <div class="card">
                            <h4 style="text-align:center; color:#2c3e50;">{tajuk}</h4>
                            <div class="metric-row">
                                <span class="metric-label">Bajet</span>
                                <span style="font-weight:bold; color:#2C7DA6;">{format_nilai(b)}</span>
                            </div>
                            <div class="metric-row">
                                <span class="metric-label">Bajet Qtr</span>
                                <span style="font-weight:bold; color:#E08E4E;">{format_nilai(s)}</span>
                            </div>
                            <div class="metric-row">
                                <span class="metric-label">Sebenar</span>
                                <span style="font-weight:bold; color:#2E8B6D;">{format_nilai(se)}</span>
                            </div>
                        </div>
                        """)

    with st.expander("📊 CARTA 1: PERBANDINGAN  KATEGORI", expanded=False):
        df_chart = df_akhir.copy()
        df_chart["BAJET_JT"] = df_chart["BAJET 2025"] / 1_000_000
        df_chart["SASARAN_JT"] = df_chart["SASARAN Q1-25"] / 1_000_000
        df_chart["SEBENAR_JT"] = df_chart["SEBENAR Q1-25"] / 1_000_000

        if len(pilih_quarter) > 1:
            cols = st.columns(len(pilih_quarter))
            for i, q in enumerate(pilih_quarter):
                df_q = df_chart[df_chart["Quarter"] == q]
                df_c1 = df_q.groupby("Kategori", as_index=False).agg({
                    "BAJET_JT": "sum",
                    "SASARAN_JT": "sum",
                    "SEBENAR_JT": "sum"
                })
                with cols[i]:
                    st.markdown(f"**Tempoh {q}**")
                    fig = px.bar(
                        df_c1,
                        x="Kategori",
                        y=["BAJET_JT", "SASARAN_JT", "SEBENAR_JT"],
                        barmode="group",
                        height=620,
                        labels={
                            "Kategori": "Kategori",
                            "value": "Nilai",
                            "variable": "Jenis"
                        },
                        color_discrete_sequence=["#2C7DA6", "#E08E4E", "#2E8B6D"]
                    )
                    for trace in fig.data:
                        kemas_label_bajet(trace)
                        trace.text = [format_nilai(x * 1_000_000) for x in trace.y]
                    apply_chart_text_style(fig, size=11, angle=-15)
                    st.plotly_chart(fig, use_container_width=True)
        else:
            df_c1 = df_chart.groupby("Kategori", as_index=False).agg({
                "BAJET_JT": "sum",
                "SASARAN_JT": "sum",
                "SEBENAR_JT": "sum"
            })
            fig1 = px.bar(
                df_c1,
                x="Kategori",
                y=["BAJET_JT", "SASARAN_JT", "SEBENAR_JT"],
                barmode="group",
                height=650,
                labels={
                    "Kategori": "Kategori",
                    "value": "Nilai",
                    "variable": "Jenis"
                },
                color_discrete_sequence=["#2C7DA6", "#E08E4E", "#2E8B6D"]
            )
            for trace in fig1.data:
                kemas_label_bajet(trace)
                trace.text = [format_nilai(x * 1_000_000) for x in trace.y]
            apply_chart_text_style(fig1, size=12, angle=0)
            st.plotly_chart(fig1, use_container_width=True)

    with st.expander("📊 CARTA 2: PERBANDINGAN SEBENAR 03-2026 VS 03-2025", expanded=False):
        # =======================
        # CARTA 2 - COMPARISON DALAM SATU FAIL EXCEL
        # Fail: JPKA_ANALISA PK CIDB 03-2026.xlsx
        # Column semasa : SEBENAR Q1-25 / SEBENAR 03-2026
        # Column sebelum: SEBENAR 03-2025
        # =======================
        df_compare = df_akhir.copy()

        if "SEBENAR 03-2025" not in df_compare.columns:
            st.warning("Column SEBENAR 03-2025 tidak dijumpai dalam data Excel.")
        else:
            nilai_2026 = pd.to_numeric(
                df_compare["SEBENAR Q1-25"],
                errors="coerce"
            ).fillna(0).sum()

            nilai_2025 = pd.to_numeric(
                df_compare["SEBENAR 03-2025"],
                errors="coerce"
            ).fillna(0).sum()

            df_total_chart = pd.DataFrame({
                "Tempoh": ["03-2025", "03-2026"],
                "Jumlah Sebenar": [nilai_2025, nilai_2026]
            })

            fig_total = px.bar(
                df_total_chart,
                x="Tempoh",
                y="Jumlah Sebenar",
                labels={
                    "Jumlah Sebenar": "Jumlah Sebenar (RM)",
                    "Tempoh": "Tempoh"
                },
                text=df_total_chart["Jumlah Sebenar"].apply(format_nilai)
            )

            warna_carta2 = ["#E08E4E", "#2E8B6D"]

            fig_total.update_traces(
                marker_color=warna_carta2,
                text=df_total_chart["Jumlah Sebenar"].apply(format_nilai)
            )

            apply_chart_text_style(fig_total, size=12, angle=0)

            # =======================
            # NOTA PERBANDINGAN
            # Formula:
            # ((SEBENAR 03-2026 / SEBENAR 03-2025) * 100) - 100
            # =======================
            if nilai_2025 != 0:
                peratus_banding = (nilai_2026 / nilai_2025) * 100
                gauge_delta = peratus_banding - 100

                if gauge_delta > 0:
                    label_banding = f"+{gauge_delta:.0f}%"
                    warna_gauge = "#16a34a"
                    arah_label = "meningkat"
                elif gauge_delta < 0:
                    label_banding = f"{gauge_delta:.0f}%"
                    warna_gauge = "#dc2626"
                    arah_label = "menurun"
                else:
                    label_banding = "0%"
                    warna_gauge = "#f59e0b"
                    arah_label = "tiada perubahan"
            else:
                label_banding = "#DIV/0!"
                warna_gauge = "#64748b"
                arah_label = "tidak dapat dikira"

            y_max_chart = max(
                pd.to_numeric(df_total_chart["Jumlah Sebenar"], errors="coerce").fillna(0).max(),
                1
            )

            fig_total.add_annotation(
                x=0.5,
                y=y_max_chart * 1.14,
                xref="paper",
                yref="y",
                text=f"03-2026 berbanding 03-2025: {label_banding} ({arah_label})",
                showarrow=False,
                font=dict(
                    size=15,
                    color=warna_gauge,
                    family="Arial Black"
                ),
                bgcolor="rgba(255,255,255,0.92)",
                bordercolor=warna_gauge,
                borderwidth=1.5,
                borderpad=8
            )

            fig_total.update_layout(
                height=650,
                xaxis_title="Tempoh",
                yaxis_title="Jumlah Sebenar (RM)",
                margin=dict(t=150, b=100, l=90, r=90),
                template="plotly_white"
            )

            st.plotly_chart(fig_total, use_container_width=True)

            df_compare_show = pd.DataFrame({
                "Perkara": [
                    "Sebenar 03-2025",
                    "Sebenar 03-2026",
                    "Perubahan RM",
                    "Perubahan %"
                ],
                "Nilai": [
                    format_comma(nilai_2025),
                    format_comma(nilai_2026),
                    format_comma(nilai_2026 - nilai_2025),
                    label_banding
                ]
            })

            st.dataframe(
                df_compare_show,
                use_container_width=True,
                hide_index=True
            )

    with st.expander("📊 CARTA 3: PRESTASI  ITEM", expanded=False):
        if len(pilih_quarter) > 1:
            cols = st.columns(len(pilih_quarter))
            for i, q in enumerate(pilih_quarter):
                df_q = df_akhir[df_akhir["Quarter"] == q]
                df_c2 = (
                    df_q.groupby("DESC", as_index=False)
                    .agg({"SASARAN Q1-25": "sum", "SEBENAR Q1-25": "sum"})
                    .sort_values("SEBENAR Q1-25", ascending=False)
                    .head(20)
                )
                with cols[i]:
                    st.markdown(f"**Tempoh {q}**")
                    fig2 = px.bar(
                        df_c2,
                        y="DESC",
                        x=["SASARAN Q1-25", "SEBENAR Q1-25"],
                        orientation="h",
                        barmode="group",
                        height=760,
                        labels={
                            "DESC": "Item",
                            "value": "Nilai",
                            "variable": "Jenis"
                        },
                        color_discrete_sequence=["#E08E4E", "#2E8B6D"]
                    )
                    for trace in fig2.data:
                        kemas_label_bajet(trace)
                        trace.text = [format_nilai(x) for x in trace.x]
                    apply_chart_text_style(fig2, size=10, angle=0)
                    max_x = max([max(list(t.x)) for t in fig2.data if len(list(t.x)) > 0]) if fig2.data else 0
                    fig2.update_layout(
                        yaxis=dict(categoryorder="array", categoryarray=df_c2["DESC"].tolist()),
                        xaxis_range=[0, max_x * 1.25 if max_x else None]
                    )
                    st.plotly_chart(fig2, use_container_width=True)
        else:
            df_c2 = (
                df_akhir.groupby("DESC", as_index=False)
                .agg({"SASARAN Q1-25": "sum", "SEBENAR Q1-25": "sum"})
                .sort_values("SEBENAR Q1-25", ascending=False)
                .head(20)
            )
            fig2 = px.bar(
                df_c2,
                y="DESC",
                x=["SASARAN Q1-25", "SEBENAR Q1-25"],
                orientation="h",
                barmode="group",
                height=760,
                labels={
                    "DESC": "Item",
                    "value": "Nilai",
                    "variable": "Jenis"
                },
                color_discrete_sequence=["#E08E4E", "#2E8B6D"]
            )
            for trace in fig2.data:
                kemas_label_bajet(trace)
                trace.text = [format_nilai(x) for x in trace.x]
            apply_chart_text_style(fig2, size=12, angle=0)
            max_x = max([max(list(t.x)) for t in fig2.data if len(list(t.x)) > 0]) if fig2.data else 0
            fig2.update_layout(
                yaxis=dict(categoryorder="array", categoryarray=df_c2["DESC"].tolist()),
                xaxis_range=[0, max_x * 1.25 if max_x else None]
            )
            st.plotly_chart(fig2, use_container_width=True)



    with st.expander("📊 CARTA 4: BY KOD ITEM", expanded=False):
        df_by_kod_item = (
            df_akhir.groupby(["KOD1"], as_index=False)
            .agg({
                "SEBENAR Q1-25": "sum"
            })
        )

        df_by_kod_item["SEBENAR_JT"] = df_by_kod_item["SEBENAR Q1-25"] / 1_000_000

        df_by_kod_item = (
            df_by_kod_item
            .sort_values("SEBENAR Q1-25", ascending=False)
            .head(25)
        )

        # Warna selang-seli soft & pekat ala 3D corporate
        warna_bars_kod_item = []
        for i in range(len(df_by_kod_item)):
            if i % 2 == 0:
                warna_bars_kod_item.append("rgba(125,211,252,0.78)")  # soft blue
            else:
                warna_bars_kod_item.append("rgba(14,165,233,0.95)")   # deep blue

        fig_by_kod_item = px.bar(
            df_by_kod_item,
            y="KOD1",
            x="SEBENAR_JT",
            orientation="h",
            height=850,
            text=df_by_kod_item["SEBENAR Q1-25"].apply(format_nilai),
            labels={
                "KOD1": "Kod Item",
                "SEBENAR_JT": "Sebenar"
            }
        )

        fig_by_kod_item.update_traces(
            marker_color=warna_bars_kod_item
        )

        fig_by_kod_item.update_traces(
            textposition="outside",
            cliponaxis=False,
            constraintext="none",
            textfont=dict(
                size=11,
                color="#0f172a",
                family="Arial Black"
            ),
            marker=dict(
                line=dict(
                    color="rgba(255,255,255,0.78)",
                    width=1.5
                )
            ),
            opacity=0.96,
            name="Sebenar",

            # effect ala 3D/glow
            hovertemplate="<b>%{y}</b><br>Sebenar: %{text}<extra></extra>"
        )

        max_x_kod_item = (
            df_by_kod_item["SEBENAR_JT"].max()
            if not df_by_kod_item.empty
            else 0
        )

        fig_by_kod_item.update_layout(
            title="Carta By Kod Item - Sebenar",
            yaxis=dict(
                categoryorder="array",
                categoryarray=df_by_kod_item["KOD1"].tolist()
            ),
            xaxis_range=[0, max_x_kod_item * 1.30 if max_x_kod_item else None],
            xaxis_title="Sebenar",
            yaxis_title="Kod Item",
            legend_title_text="Jenis",
            template="plotly_white",
            paper_bgcolor="rgba(255,255,255,0)",
            plot_bgcolor="rgba(241,245,249,0.82)",
            font=dict(
                family="Arial",
                color="#334155"
            ),
            title_font=dict(
                size=22,
                color="#0f172a",
                family="Arial Black"
            ),
            margin=dict(t=120, b=120, l=180, r=120),
            showlegend=False
        )

        st.plotly_chart(fig_by_kod_item, use_container_width=True)

    with st.expander("📈 CARTA 5: PRESTASI  PTJ", expanded=False):
        # Formula Carta 5:
        # % Prestasi   = SEBENAR / BAJET
        # % Sasaran    = SASARAN / BAJET
        # % Pencapaian = SEBENAR / SASARAN
        #
        # Rule DIV/0:
        # - Jika BAJET kosong/0, Prestasi dan Sasaran tidak dikira.
        # - Jika SASARAN kosong/0, Pencapaian tidak dikira.
        # - Papar #DIV/0! sahaja, bukan 0% atau nilai melampau.

        df_c3 = df_group.copy()

        # Pastikan numeric.
        df_c3["BAJET 2025"] = pd.to_numeric(
            df_c3["BAJET 2025"],
            errors="coerce"
        ).fillna(0)

        df_c3["SASARAN Q1-25"] = pd.to_numeric(
            df_c3["SASARAN Q1-25"],
            errors="coerce"
        ).fillna(0)

        df_c3["SEBENAR Q1-25"] = pd.to_numeric(
            df_c3["SEBENAR Q1-25"],
            errors="coerce"
        ).fillna(0)

        # Flag divide by zero.
        df_c3["Is_DIV0_Bajet"] = df_c3["BAJET 2025"] <= 0
        df_c3["Is_DIV0_Sasaran"] = df_c3["SASARAN Q1-25"] <= 0

        # Kiraan sebenar.
        df_c3["% Prestasi"] = df_c3.apply(
            lambda row: None
            if row["Is_DIV0_Bajet"]
            else hitung_prestasi(row["SEBENAR Q1-25"], row["BAJET 2025"]),
            axis=1
        )

        df_c3["% Sasaran"] = df_c3.apply(
            lambda row: None
            if row["Is_DIV0_Bajet"]
            else hitung_prestasi(row["SASARAN Q1-25"], row["BAJET 2025"]),
            axis=1
        )

        df_c3["% Pencapaian"] = df_c3.apply(
            lambda row: None
            if row["Is_DIV0_Sasaran"]
            else hitung_prestasi(row["SEBENAR Q1-25"], row["SASARAN Q1-25"]),
            axis=1
        )

        # Display value untuk chart.
        # None akan sembunyikan bar/line supaya tidak nampak 0%.
        df_c3["% Prestasi_Display"] = df_c3["% Prestasi"]
        df_c3["% Sasaran_Display"] = df_c3["% Sasaran"]
        df_c3["% Pencapaian_Display"] = df_c3["% Pencapaian"]

        # Label.
        df_c3["Label Prestasi"] = df_c3.apply(
            lambda row: "#DIV/0!"
            if row["Is_DIV0_Bajet"]
            else f'{int(round(row["% Prestasi"]))}%',
            axis=1
        )

        df_c3["Label Sasaran"] = df_c3.apply(
            lambda row: "#DIV/0!"
            if row["Is_DIV0_Bajet"]
            else f'{int(round(row["% Sasaran"]))}%',
            axis=1
        )

        df_c3["Label Pencapaian"] = df_c3.apply(
            lambda row: "#DIV/0!"
            if row["Is_DIV0_Sasaran"]
            else f'{int(round(row["% Pencapaian"]))}%',
            axis=1
        )

        # Susun ikut pencapaian tertinggi.
        # DIV/0 diletakkan bawah sekali.
        df_c3["_sort_pencapaian"] = pd.to_numeric(
            df_c3["% Pencapaian"],
            errors="coerce"
        ).fillna(-1)

        df_c3 = df_c3.sort_values(
            by="_sort_pencapaian",
            ascending=False
        ).reset_index(drop=True)

        left_y_max_value = 0
        right_y_max_value = 0

        if not df_c3.empty:
            valid_left_values = pd.concat([
                pd.to_numeric(df_c3["% Prestasi"], errors="coerce"),
                pd.to_numeric(df_c3["% Sasaran"], errors="coerce")
            ]).dropna()

            if not valid_left_values.empty:
                left_y_max_value = valid_left_values.max()

            valid_right_values = pd.to_numeric(
                df_c3["% Pencapaian"],
                errors="coerce"
            ).dropna()

            if not valid_right_values.empty:
                right_y_max_value = valid_right_values.max()

        left_y_max = max(
            40,
            int(left_y_max_value) + 10 if left_y_max_value > 0 else 40
        )

        right_y_max = max(
            140,
            int(right_y_max_value) + 20 if right_y_max_value > 0 else 140
        )

        fig3 = go.Figure()

        # Bar Prestasi - Axis kiri.
        fig3.add_trace(go.Bar(
            x=df_c3["PTJ1"],
            y=df_c3["% Prestasi_Display"],
            name="Prestasi (Sebenar/Bajet)",
            marker_color="#8ED04F",
            text=df_c3.apply(
                lambda row: ""
                if row["Is_DIV0_Bajet"]
                else row["Label Prestasi"],
                axis=1
            ),
            textposition="inside",
            insidetextanchor="middle",
            textfont=dict(
                size=12,
                color="black",
                family="Arial"
            ),
            yaxis="y",
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Prestasi: %{y:.2f}%<br>"
                "<extra></extra>"
            )
        ))

        # Line Sasaran - Axis kiri.
        fig3.add_trace(go.Scatter(
            x=df_c3["PTJ1"],
            y=df_c3["% Sasaran_Display"],
            name="Sasaran (Sasaran/Bajet)",
            line=dict(color="#FFB000", width=3, dash="dash"),
            marker=dict(size=7),
            mode="lines+markers+text",
            text=df_c3.apply(
                lambda row: ""
                if row["Is_DIV0_Bajet"]
                else row["Label Sasaran"],
                axis=1
            ),
            textposition="top center",
            textfont=dict(
                size=11,
                color="black",
                family="Arial"
            ),
            yaxis="y",
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Sasaran: %{y:.2f}%<br>"
                "<extra></extra>"
            )
        ))

        # Line Pencapaian - Axis kanan sahaja.
        fig3.add_trace(go.Scatter(
            x=df_c3["PTJ1"],
            y=df_c3["% Pencapaian_Display"],
            name="Pencapaian (Sebenar/Sasaran)",
            line=dict(color="red", width=4),
            marker=dict(size=7),
            mode="lines+markers+text",
            text=df_c3.apply(
                lambda row: ""
                if row["Is_DIV0_Sasaran"]
                else row["Label Pencapaian"],
                axis=1
            ),
            textposition="top center",
            textfont=dict(
                size=11,
                color="black",
                family="Arial"
            ),
            yaxis="y2",
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Pencapaian: %{y:.2f}%<br>"
                "<extra></extra>"
            )
        ))

        # Manual annotation #DIV/0!.
        # Jika Bajet 0, letak annotation untuk Prestasi/Sasaran.
        # Jika Sasaran 0, letak annotation untuk Pencapaian.
        div0_rows = df_c3[
            (df_c3["Is_DIV0_Bajet"]) |
            (df_c3["Is_DIV0_Sasaran"])
        ].copy()

        for _, row in div0_rows.iterrows():
            fig3.add_annotation(
                x=row["PTJ1"],
                y=max(left_y_max * 0.06, 2),
                text="#DIV/0!",
                showarrow=False,
                yref="y",
                font=dict(
                    size=12,
                    color="black",
                    family="Arial"
                ),
                bgcolor="rgba(255,255,255,0.90)",
                bordercolor="rgba(0,0,0,0.25)",
                borderwidth=1,
                borderpad=2
            )

        fig3.update_layout(
            height=780,
            xaxis=dict(
                title="PTJ",
                tickangle=-45,
                automargin=True
            ),
            yaxis=dict(
                title="Prestasi & Sasaran (%)",
                range=[0, left_y_max],
                ticksuffix="%",
                showgrid=True,
                zeroline=True
            ),
            yaxis2=dict(
                title="Pencapaian (%)",
                range=[0, right_y_max],
                ticksuffix="%",
                overlaying="y",
                side="right",
                showgrid=False,
                zeroline=False
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.28,
                xanchor="center",
                x=0.5
            ),
            template="plotly_white",
            margin=dict(t=120, b=180, l=80, r=90),
            uniformtext_minsize=8,
            uniformtext_mode="show"
        )

        fig3.update_traces(
            cliponaxis=False
        )

        st.plotly_chart(fig3, use_container_width=True)


    
    with st.expander("📈 CARTA 6: PRESTASI PTJ (JUMLAH SEBENAR)", expanded=False):

        df_c6 = df_group.copy()

        df_c6["BAJET 2025"] = pd.to_numeric(
            df_c6["BAJET 2025"],
            errors="coerce"
        ).fillna(0)

        df_c6["SASARAN Q1-25"] = pd.to_numeric(
            df_c6["SASARAN Q1-25"],
            errors="coerce"
        ).fillna(0)

        df_c6["SEBENAR Q1-25"] = pd.to_numeric(
            df_c6["SEBENAR Q1-25"],
            errors="coerce"
        ).fillna(0)

        df_c6["% Sasaran"] = df_c6.apply(
            lambda row: None
            if row["BAJET 2025"] <= 0
            else hitung_prestasi(row["SASARAN Q1-25"], row["BAJET 2025"]),
            axis=1
        )

        df_c6["% Pencapaian"] = df_c6.apply(
            lambda row: None
            if row["SASARAN Q1-25"] <= 0
            else hitung_prestasi(row["SEBENAR Q1-25"], row["SASARAN Q1-25"]),
            axis=1
        )

        df_c6["Jumlah Sebenar"] = df_c6["SEBENAR Q1-25"]

        df_c6 = df_c6.sort_values(
            by="Jumlah Sebenar",
            ascending=False
        ).reset_index(drop=True)

        fig6 = go.Figure()

        # Bar Hijau = Jumlah Sebenar
        fig6.add_trace(go.Bar(
            x=df_c6["PTJ1"],
            y=df_c6["Jumlah Sebenar"],
            name="Jumlah Sebenar",
            marker_color="#8ED04F",
            text=df_c6["Jumlah Sebenar"].apply(lambda x: f"{x:,.0f}"),
            textposition="inside",
            insidetextanchor="middle",
            textfont=dict(
                size=11,
                color="black",
                family="Arial"
            ),
            yaxis="y",
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Jumlah Sebenar: %{text}<br>"
                "<extra></extra>"
            )
        ))

        # Line Sasaran
        fig6.add_trace(go.Scatter(
            x=df_c6["PTJ1"],
            y=df_c6["% Sasaran"],
            name="Sasaran (%)",
            line=dict(color="#FFB000", width=3, dash="dash"),
            marker=dict(size=7),
            mode="lines+markers+text",
            text=df_c6["% Sasaran"].apply(
                lambda x: "" if pd.isna(x) else f"{x:.0f}%"
            ),
            textposition="top center",
            textfont=dict(
                size=10,
                color="black",
                family="Arial"
            ),
            yaxis="y2"
        ))

        # Line Pencapaian Merah
        fig6.add_trace(go.Scatter(
            x=df_c6["PTJ1"],
            y=df_c6["% Pencapaian"],
            name="Pencapaian (%)",
            line=dict(color="red", width=4),
            marker=dict(size=7),
            mode="lines+markers+text",
            text=df_c6["% Pencapaian"].apply(
                lambda x: "" if pd.isna(x) else f"{x:.0f}%"
            ),
            textposition="top center",
            textfont=dict(
                size=10,
                color="black",
                family="Arial"
            ),
            yaxis="y2"
        ))

        left_max = df_c6["Jumlah Sebenar"].max()

        right_max = max(
            pd.to_numeric(df_c6["% Sasaran"], errors="coerce").max(),
            pd.to_numeric(df_c6["% Pencapaian"], errors="coerce").max()
        )

        fig6.update_layout(
            height=780,
            template="plotly_white",
            xaxis=dict(
                title="PTJ",
                tickangle=-45,
                automargin=True
            ),
            yaxis=dict(
                title="Jumlah Sebenar (RM)",
                range=[0, left_max * 1.20 if left_max else 1]
            ),
            yaxis2=dict(
                title="Prestasi (%)",
                overlaying="y",
                side="right",
                ticksuffix="%",
                range=[0, right_max * 1.20 if right_max else 100],
                showgrid=False
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.25,
                xanchor="center",
                x=0.5
            ),
            margin=dict(t=120, b=180, l=90, r=90)
        )

        fig6.update_traces(
            cliponaxis=False
        )

        st.plotly_chart(fig6, use_container_width=True)


    with st.expander("📋 SUMMARY KESELURUHAN", expanded=False):
        summary = df_akhir.groupby(["PTJ1", "Kategori", "DESC", "Quarter"], as_index=False).agg({
            "BAJET 2025": "sum",
            "SASARAN Q1-25": "sum",
            "SEBENAR Q1-25": "sum",
            "SEBENAR 03-2025": "sum"
        })
        summary["Prestasi_%"] = summary.apply(
            lambda row: hitung_prestasi(row["SEBENAR Q1-25"], row["SASARAN Q1-25"]),
            axis=1
        )
        summary = summary.round(2)
        summary = rename_summary_columns(summary)

        # Tambah row JUMLAH di bawah sekali.
        # Belanja & Hasil: jumlahkan semua nilai Bajet, Sasaran dan Sebenar.
        jumlah_summary = {
            "PTJ": "JUMLAH",
            "Kategori": "",
            "Item": "",
            "Tempoh": "",
            "Bajet": pd.to_numeric(summary["Bajet"], errors="coerce").fillna(0).sum(),
            "Bajet Qtr": pd.to_numeric(summary["Bajet Qtr"], errors="coerce").fillna(0).sum(),
            "Sebenar 03-2026": pd.to_numeric(summary["Sebenar 03-2026"], errors="coerce").fillna(0).sum(),
            "Sebenar 03-2025": pd.to_numeric(summary["Sebenar 03-2025"], errors="coerce").fillna(0).sum(),
            "Prestasi_%": hitung_prestasi(
                pd.to_numeric(summary["Sebenar 03-2026"], errors="coerce").fillna(0).sum(),
                pd.to_numeric(summary["Bajet Qtr"], errors="coerce").fillna(0).sum()
            )
        }

        summary = pd.concat(
            [summary, pd.DataFrame([jumlah_summary])],
            ignore_index=True
        )

        # Paparan summary dengan comma style pada semua nilai numeric.
        summary_show = dataframe_comma_style(
            summary,
            money_cols=["Bajet", "Bajet Qtr", "Sebenar 03-2026", "Sebenar 03-2025"],
            percent_cols=["Prestasi_%"]
        )

        st.dataframe(
            summary_show,
            use_container_width=True,
            hide_index=True
        )

        # Download kekal raw numeric supaya masih boleh dikira dalam Excel.
        excel_file = to_excel(summary)
        st.download_button(
            "📥 Download Summary sebagai Excel",
            data=excel_file,
            file_name=f"Summary_CIDB_{'_'.join(pilih_quarter)}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

    st.caption("Tempoh: 03-2026 • Comparison Carta 2 menggunakan column SEBENAR 03-2025 • Prestasi Kewangan CIDB JPKA")

# =======================
# MENU 2: GERAN - SLICER DARI WORKSHEET DATA COLUMN NAMA DAN LEGEND
# =======================
elif menu == "2. Geran":
    st.markdown("## 🧾 MODUL GERAN")
    if df_geran.empty:
        st.error("Data Geran tidak berjaya dimuatkan.")
        if geran_error:
            st.info(geran_error)
        st.stop()

    df_geran_work = df_geran.copy()

    nama_col = "NAMA"
    nama_short_col = "NAMA1"
    legend_col = "LEGEND"
    ptj_col = "PTJ"

    if nama_col not in df_geran_work.columns:
        st.error("Column NAMA tidak dijumpai dalam worksheet DATA.")
        st.write("Column yang ada:", df_geran_work.columns.tolist())
        st.stop()

    if nama_short_col not in df_geran_work.columns:
        st.error("Column NAMA1 tidak dijumpai dalam worksheet DATA.")
        st.write("Column yang ada:", df_geran_work.columns.tolist())
        st.stop()

    if legend_col not in df_geran_work.columns:
        st.error("Column LEGEND tidak dijumpai dalam worksheet DATA.")
        st.write("Column yang ada:", df_geran_work.columns.tolist())
        st.stop()

    if ptj_col not in df_geran_work.columns:
        st.error("Column PTJ tidak dijumpai dalam worksheet DATA.")
        st.write("Column yang ada:", df_geran_work.columns.tolist())
        st.stop()

    amount_col = detect_amount_column(df_geran_work)
    if amount_col is not None:
        df_geran_work[amount_col] = clean_numeric_series(df_geran_work[amount_col])

        # Buang semua nilai negatif untuk keseluruhan Modul Geran.
        # Ini digunakan untuk KPI, slicer, carta dan jadual DATA GERAN.
        df_geran_work = df_geran_work[df_geran_work[amount_col] >= 0].copy()

    df_geran_tapis = df_geran_work.copy()

    # =======================
    # SLICER GERAN - STABLE FULL CONNECTION
    #
    # Prinsip:
    # 1. Jika PTJ berubah    -> NAMA & LEGEND auto isi ikut PTJ.
    # 2. Jika NAMA berubah   -> PTJ & LEGEND auto isi ikut NAMA.
    # 3. Jika LEGEND berubah -> PTJ & NAMA auto isi ikut LEGEND.
    # 4. Pills hanya tunjuk item yang belum berada dalam multiselect.
    # 5. Jika item dikeluarkan dari multiselect, item itu muncul semula dalam pills.
    #
    # Nota penting:
    # - Logic ini tidak guna "options bertapis terlalu ketat" untuk pills,
    #   supaya item yang dikeluarkan sentiasa boleh muncul semula.
    # =======================
    def _geran_as_list(value):
        if value is None:
            return []
        if isinstance(value, list):
            return value
        return [value]

    def _geran_unique_col(df_source, col):
        if col not in df_source.columns:
            return []
        return unique_sorted(df_source[col])

    def _geran_filter_df(df_source, filters):
        df_temp = df_source.copy()
        for col, vals in filters.items():
            vals = _geran_as_list(vals)
            if vals and col in df_temp.columns:
                df_temp = df_temp[df_temp[col].astype(str).isin(vals)]
        return df_temp

    def _geran_base_df():
        return st.session_state.get("_geran_slicer_base_df_stable", pd.DataFrame())

    def _geran_force_pills_key(col_name):
        return f"_geran_force_pills_{col_name}"

    def _geran_prev_key(col_name):
        return f"_geran_prev_{col_name}"

    def _geran_track_removed(col_name, current_vals):
        """
        Simpan item yang dikeluarkan dari multiselect supaya ia muncul semula dalam pills.
        """
        prev_vals = set(_geran_as_list(st.session_state.get(_geran_prev_key(col_name), [])))
        curr_vals = set(_geran_as_list(current_vals))
        removed = sorted(list(prev_vals - curr_vals))

        if removed:
            forced_key = _geran_force_pills_key(col_name)
            forced_existing = set(_geran_as_list(st.session_state.get(forced_key, [])))
            st.session_state[forced_key] = sorted(list(forced_existing.union(removed)))

    def _geran_build_pills_options(all_options, selected_vals, col_name):
        selected_set = set(_geran_as_list(selected_vals))
        forced_key = _geran_force_pills_key(col_name)
        forced_vals = [
            x for x in _geran_as_list(st.session_state.get(forced_key, []))
            if x in set(all_options) and x not in selected_set
        ]

        base_vals = [
            x for x in all_options
            if x not in selected_set
        ]

        return unique_sorted(pd.Series(list(dict.fromkeys(base_vals + forced_vals))))

    def _geran_remove_from_forced(col_name, vals):
        forced_key = _geran_force_pills_key(col_name)
        vals_set = set(_geran_as_list(vals))
        forced_vals = [
            x for x in _geran_as_list(st.session_state.get(forced_key, []))
            if x not in vals_set
        ]
        st.session_state[forced_key] = forced_vals

    def _sync_geran_from_ptj():
        df_base = _geran_base_df()
        if df_base.empty:
            return

        ptj_vals = _geran_as_list(st.session_state.get("geran_ptj_final", []))
        _geran_track_removed("ptj", ptj_vals)

        df_ctx = (
            _geran_filter_df(df_base, {ptj_col: ptj_vals})
            if ptj_vals else df_base.copy()
        )

        st.session_state["geran_nama_final"] = _geran_unique_col(df_ctx, nama_col)
        st.session_state["geran_legend_final"] = _geran_unique_col(df_ctx, legend_col)

    def _sync_geran_from_nama():
        df_base = _geran_base_df()
        if df_base.empty:
            return

        nama_vals = _geran_as_list(st.session_state.get("geran_nama_final", []))
        _geran_track_removed("nama", nama_vals)

        df_ctx = (
            _geran_filter_df(df_base, {nama_col: nama_vals})
            if nama_vals else df_base.copy()
        )

        st.session_state["geran_ptj_final"] = _geran_unique_col(df_ctx, ptj_col)
        st.session_state["geran_legend_final"] = _geran_unique_col(df_ctx, legend_col)

    def _sync_geran_from_legend():
        df_base = _geran_base_df()
        if df_base.empty:
            return

        legend_vals = _geran_as_list(st.session_state.get("geran_legend_final", []))
        _geran_track_removed("legend", legend_vals)

        df_ctx = (
            _geran_filter_df(df_base, {legend_col: legend_vals})
            if legend_vals else df_base.copy()
        )

        st.session_state["geran_ptj_final"] = _geran_unique_col(df_ctx, ptj_col)
        st.session_state["geran_nama_final"] = _geran_unique_col(df_ctx, nama_col)

    with st.sidebar:
        st.markdown("### 🔎  GERAN")

        df_geran_slicer_base = df_geran_tapis.copy()
        st.session_state["_geran_slicer_base_df_stable"] = df_geran_slicer_base

        full_geran_ptj = _geran_unique_col(df_geran_slicer_base, ptj_col)
        full_geran_nama = _geran_unique_col(df_geran_slicer_base, nama_col)
        full_geran_legend = _geran_unique_col(df_geran_slicer_base, legend_col)

        if "geran_stable_slicer_initialized" not in st.session_state:
            st.session_state["geran_ptj_final"] = full_geran_ptj
            st.session_state["geran_nama_final"] = full_geran_nama
            st.session_state["geran_legend_final"] = full_geran_legend
            st.session_state["_geran_prev_ptj"] = full_geran_ptj
            st.session_state["_geran_prev_nama"] = full_geran_nama
            st.session_state["_geran_prev_legend"] = full_geran_legend
            st.session_state["_geran_force_pills_ptj"] = []
            st.session_state["_geran_force_pills_nama"] = []
            st.session_state["_geran_force_pills_legend"] = []
            st.session_state["geran_stable_slicer_initialized"] = True

        # Bersihkan selected value yang sudah tiada dalam data.
        st.session_state["geran_ptj_final"] = [
            x for x in _geran_as_list(st.session_state.get("geran_ptj_final", []))
            if x in set(full_geran_ptj)
        ]
        st.session_state["geran_nama_final"] = [
            x for x in _geran_as_list(st.session_state.get("geran_nama_final", []))
            if x in set(full_geran_nama)
        ]
        st.session_state["geran_legend_final"] = [
            x for x in _geran_as_list(st.session_state.get("geran_legend_final", []))
            if x in set(full_geran_legend)
        ]

        # PTJ pills
        opt_ptj_pills = _geran_build_pills_options(
            full_geran_ptj,
            st.session_state.get("geran_ptj_final", []),
            "ptj"
        )

        def _sync_geran_ptj_pills():
            ptj_pills = _geran_as_list(st.session_state.get("geran_ptj_pills_multi", []))
            if not ptj_pills:
                return

            current_ptj = _geran_as_list(st.session_state.get("geran_ptj_final", []))
            st.session_state["geran_ptj_final"] = sorted(list(set(current_ptj + ptj_pills)))
            st.session_state["geran_ptj_pills_multi"] = []
            _geran_remove_from_forced("ptj", ptj_pills)
            _sync_geran_from_ptj()

        st.pills(
            "⚡ Pilih PTJ",
            options=opt_ptj_pills,
            selection_mode="multi",
            key="geran_ptj_pills_multi",
            on_change=_sync_geran_ptj_pills
        )

        st.multiselect(
            "Pilih PTJ (Multi Select)",
            full_geran_ptj,
            key="geran_ptj_final",
            on_change=_sync_geran_from_ptj,
            placeholder="Semua PTJ"
        )

        # NAMA pills
        opt_nama_pills = _geran_build_pills_options(
            full_geran_nama,
            st.session_state.get("geran_nama_final", []),
            "nama"
        )

        def _sync_geran_nama_pills():
            nama_pills = _geran_as_list(st.session_state.get("geran_nama_pills_multi", []))
            if not nama_pills:
                return

            current_nama = _geran_as_list(st.session_state.get("geran_nama_final", []))
            st.session_state["geran_nama_final"] = sorted(list(set(current_nama + nama_pills)))
            st.session_state["geran_nama_pills_multi"] = []
            _geran_remove_from_forced("nama", nama_pills)
            _sync_geran_from_nama()

        st.pills(
            "⚡ Pilih NAMA",
            options=opt_nama_pills,
            selection_mode="multi",
            key="geran_nama_pills_multi",
            on_change=_sync_geran_nama_pills
        )

        st.multiselect(
            "Pilih NAMA (Multi Select)",
            full_geran_nama,
            key="geran_nama_final",
            on_change=_sync_geran_from_nama,
            placeholder="Semua NAMA"
        )

        # LEGEND pills
        opt_legend_pills = _geran_build_pills_options(
            full_geran_legend,
            st.session_state.get("geran_legend_final", []),
            "legend"
        )

        def _sync_geran_legend_pills():
            legend_pills = _geran_as_list(st.session_state.get("geran_legend_pills_multi", []))
            if not legend_pills:
                return

            current_legend = _geran_as_list(st.session_state.get("geran_legend_final", []))
            st.session_state["geran_legend_final"] = sorted(list(set(current_legend + legend_pills)))
            st.session_state["geran_legend_pills_multi"] = []
            _geran_remove_from_forced("legend", legend_pills)
            _sync_geran_from_legend()

        st.pills(
            "⚡ Pilih LEGEND",
            options=opt_legend_pills,
            selection_mode="multi",
            key="geran_legend_pills_multi",
            on_change=_sync_geran_legend_pills
        )

        st.multiselect(
            "Pilih LEGEND (Multi Select)",
            full_geran_legend,
            key="geran_legend_final",
            on_change=_sync_geran_from_legend,
            placeholder="Semua LEGEND"
        )

        if st.button("♻️ Reset Slicer Geran", key="reset_slicer_geran_stable"):
            for key in [
                "geran_ptj_final",
                "geran_nama_final",
                "geran_legend_final",
                "geran_ptj_pills_multi",
                "geran_nama_pills_multi",
                "geran_legend_pills_multi",
                "geran_stable_slicer_initialized",
                "_geran_slicer_base_df_stable",
                "_geran_prev_ptj",
                "_geran_prev_nama",
                "_geran_prev_legend",
                "_geran_force_pills_ptj",
                "_geran_force_pills_nama",
                "_geran_force_pills_legend",
                "geran_full_slicer_initialized",
                "_geran_slicer_base_df_full",
            ]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

        # Simpan state terkini sebagai previous untuk detect remove pada rerun seterusnya.
        st.session_state["_geran_prev_ptj"] = _geran_as_list(st.session_state.get("geran_ptj_final", []))
        st.session_state["_geran_prev_nama"] = _geran_as_list(st.session_state.get("geran_nama_final", []))
        st.session_state["_geran_prev_legend"] = _geran_as_list(st.session_state.get("geran_legend_final", []))

    pilih_ptj_geran = _geran_as_list(st.session_state.get("geran_ptj_final", []))
    pilih_nama = _geran_as_list(st.session_state.get("geran_nama_final", []))
    pilih_legend = _geran_as_list(st.session_state.get("geran_legend_final", []))

    if pilih_ptj_geran:
        df_geran_tapis = df_geran_tapis[
            df_geran_tapis[ptj_col].astype(str).isin(pilih_ptj_geran)
        ].copy()

    if pilih_nama:
        df_geran_tapis = df_geran_tapis[
            df_geran_tapis[nama_col].astype(str).isin(pilih_nama)
        ].copy()

    if pilih_legend:
        df_geran_tapis = df_geran_tapis[
            df_geran_tapis[legend_col].astype(str).isin(pilih_legend)
        ].copy()

    if df_geran_tapis.empty:
        st.warning("Tiada data Geran selepas tapisan dibuat.")
        st.stop()

    # KPI Geran:
    # Column LEGEND menentukan kategori:
    # - PEMBERIAN
    # - PERBELANJAAN
    # - BYR BALIK
    # Nilai dikira menggunakan column "Amount in local currency"
    if amount_col is None:
        st.error("Column Amount in local currency / amaun tidak dijumpai untuk kira KPI Geran.")
        st.stop()

    legend_upper = df_geran_tapis[legend_col].astype(str).str.strip().str.upper()

    jumlah_pemberian = df_geran_tapis.loc[
        legend_upper.eq("PEMBERIAN"),
        amount_col
    ].sum()

    jumlah_perbelanjaan = df_geran_tapis.loc[
        legend_upper.eq("PERBELANJAAN"),
        amount_col
    ].sum()

    jumlah_bayar_balik = df_geran_tapis.loc[
        legend_upper.isin(["BYR BALIK", "BAYAR BALIK"]),
        amount_col
    ].sum()

    # KPI Baki Geran = Pemberian - Perbelanjaan - Bayar Balik
    baki_geran = (
        jumlah_pemberian
        - jumlah_perbelanjaan
        - jumlah_bayar_balik
    )

    col_g1, col_g2, col_g3, col_g4 = st.columns(4)

    with col_g1:
        st.metric("Jumlah Pemberian", format_nilai(jumlah_pemberian))

    with col_g2:
        st.metric("Jumlah Perbelanjaan", format_nilai(jumlah_perbelanjaan))

    with col_g3:
        st.metric("Jumlah Bayar Balik", format_nilai(jumlah_bayar_balik))

    with col_g4:
        st.metric("BAKI GERAN", format_nilai(baki_geran))

    # =======================
    # DATA UNTUK CARTA GERAN
    # =======================
    if amount_col is None:
        st.error("Column Amount in local currency / amaun tidak dijumpai untuk bina Carta Geran.")
        st.stop()

    # CARTA 1:
    # NAMA vs PEMBERIAN, PERBELANJAAN dan BYR BALIK.
    # Nilai negatif diabaikan.
    df_chart_geran = df_geran_tapis.copy()
    df_chart_geran[amount_col] = clean_numeric_series(df_chart_geran[amount_col])
    df_chart_geran = df_chart_geran[df_chart_geran[amount_col] >= 0].copy()
    df_chart_geran["_LEGEND_UPPER"] = df_chart_geran[legend_col].astype(str).str.strip().str.upper()

    df_chart_geran = df_chart_geran[
        df_chart_geran["_LEGEND_UPPER"].isin(["PEMBERIAN", "PERBELANJAAN", "BYR BALIK", "BAYAR BALIK"])
    ].copy()

    df_chart_geran["_LEGEND_UPPER"] = df_chart_geran["_LEGEND_UPPER"].replace({
        "BAYAR BALIK": "BYR BALIK"
    })

    df_nama_legend = (
        df_chart_geran
        .pivot_table(
            index=nama_short_col,
            columns="_LEGEND_UPPER",
            values=amount_col,
            aggfunc="sum",
            fill_value=0
        )
        .reset_index()
    )

    for col in ["PEMBERIAN", "PERBELANJAAN", "BYR BALIK"]:
        if col not in df_nama_legend.columns:
            df_nama_legend[col] = 0

    df_nama_legend["Jumlah"] = (
        df_nama_legend["PEMBERIAN"]
        + df_nama_legend["PERBELANJAAN"]
        + df_nama_legend["BYR BALIK"]
    )

    df_nama_legend["BAKI GERAN"] = (
        df_nama_legend["PEMBERIAN"]
        - df_nama_legend["PERBELANJAAN"]
        - df_nama_legend["BYR BALIK"]
    )

    df_nama_legend = df_nama_legend.sort_values("Jumlah", ascending=False)

    # =======================
    # CARTA 1
    # =======================
    fig_geran_nama = px.bar(
        df_nama_legend,
        x=nama_short_col,
        y=["PEMBERIAN", "PERBELANJAAN", "BYR BALIK"],
        barmode="group",
        title=" ",
        labels={
            "value": "Jumlah",
            "variable": "Jenis",
            nama_short_col: "NAMA1"
        },
        height=600,
        color_discrete_map={
            "PEMBERIAN": "#f6d365",
            "PERBELANJAAN": "#f4978e",
            "BYR BALIK": "#95d5b2"
        }
    )

    warna_trace = {
        "PEMBERIAN": "#f6d365",
        "PERBELANJAAN": "#f4978e",
        "BYR BALIK": "#95d5b2"
    }

    for trace in fig_geran_nama.data:
        trace.text = [format_nilai(x) for x in trace.y]

        if trace.name in warna_trace:
            trace.marker.color = warna_trace[trace.name]

    apply_chart_text_style(fig_geran_nama, size=11, angle=0)

    fig_geran_nama.update_layout(
        xaxis_title=" ",
        xaxis_tickangle=-45,
        yaxis_title="Jumlah",
        legend_title_text="Jenis",
        template="plotly_white"
    )

    # =======================
    # CARTA 2
    # Baki Geran = PEMBERIAN - PERBELANJAAN - BYR BALIK
    # =======================
    df_baki_geran = df_nama_legend.copy()
    df_baki_geran = df_baki_geran.sort_values("BAKI GERAN", ascending=False)

    fig_baki = px.bar(
        df_baki_geran,
        x=nama_short_col,
        y="BAKI GERAN",
        text=df_baki_geran["BAKI GERAN"].apply(format_nilai),
        title=" ",
        color_discrete_sequence=["#bde0fe"]
    )

    apply_chart_text_style(fig_baki, size=11, angle=0)

    fig_baki.update_layout(
        height=600,
        xaxis_title=" ",
        xaxis_tickangle=-45,
        yaxis_title="Baki Geran",
        template="plotly_white"
    )

    # =======================
    # PAPAR CARTA 1 DAN 2 BERSEBELAHAN
    # =======================
    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.markdown("### 📊 Carta 1: Geran")

        # Sembunyikan bar yang nilainya 0.
        try:
            for trace in fig_geran_nama.data:
                if getattr(trace, "type", "") == "bar":
                    vals = list(trace.y) if getattr(trace, "orientation", None) != "h" else list(trace.x)

                    # Tukar nilai 0 kepada None supaya bar tidak dipaparkan.
                    vals_filtered = [
                        None if pd.to_numeric(v, errors="coerce") == 0 else v
                        for v in vals
                    ]

                    if getattr(trace, "orientation", None) == "h":
                        trace.x = vals_filtered
                    else:
                        trace.y = vals_filtered

        except Exception:
            pass

        fig_geran_nama = apply_geran_arrow_labels(
            fig_geran_nama,
            orientation="v",
            threshold_ratio=0.18
        )

        st.plotly_chart(
            fig_geran_nama,
            use_container_width=True
        )

    with col_chart2:
        st.markdown("### 📊 Carta 2: Baki Geran")
        st.plotly_chart(
            fig_baki,
            use_container_width=True
        )

    # =======================
    # CARTA 3 GERAN -  PTJ
    # =======================
    st.markdown("### 📊 Carta 3: Prestasi  PTJ")

    if ptj_col in df_chart_geran.columns:

        df_ptj = (
            df_chart_geran
            .groupby([ptj_col, "_LEGEND_UPPER"], as_index=False)[amount_col]
            .sum()
        )

        fig_ptj = px.bar(
            df_ptj,
            x=ptj_col,
            y=amount_col,
            color="_LEGEND_UPPER",
            barmode="group",
            labels={
                ptj_col: "PTJ",
                amount_col: "Jumlah",
                "_LEGEND_UPPER": "Jenis"
            },
            height=650,
            color_discrete_map={
                "PEMBERIAN": "#f6d365",
                "PERBELANJAAN": "#f4978e",
                "BYR BALIK": "#95d5b2"
            }
        )

        for trace in fig_ptj.data:
            trace.text = [format_nilai(x) for x in trace.y]

            if trace.name in warna_trace:
                trace.marker.color = warna_trace[trace.name]

        apply_chart_text_style(fig_ptj, size=11, angle=0)

        fig_ptj.update_layout(
            xaxis_tickangle=-45,
            template="plotly_white",
            yaxis_title="Jumlah",
            legend_title_text="Jenis"
        )

        st.plotly_chart(
            fig_ptj,
            use_container_width=True
        )

    else:
        st.warning("Column PTJ tidak dijumpai dalam data Geran.")

    # =======================
    # DATA GERAN  SUSUNAN EXCEL
    # Susunan column:
    # PTJ | NAMA | LEGEND | JUMLAH
    # =======================
    df_data_carta_geran_gabung = (
        df_chart_geran
        .groupby([ptj_col, nama_col, legend_col], as_index=False)[amount_col]
        .sum()
        .rename(columns={
            ptj_col: "PTJ",
            nama_col: "NAMA",
            legend_col: "LEGEND",
            amount_col: "JUMLAH"
        })
    )

    # Kekalkan susunan column seperti Excel
    df_data_carta_geran_gabung = df_data_carta_geran_gabung[
        ["PTJ", "NAMA", "LEGEND", "JUMLAH"]
    ]

    # Susunan row ikut Excel: PTJ -> NAMA -> LEGEND
    df_data_carta_geran_gabung = df_data_carta_geran_gabung.sort_values(
        by=["PTJ", "NAMA", "LEGEND"],
        ascending=[True, True, True]
    ).reset_index(drop=True)

    # Tambah row JUMLAH di bawah sekali.
    # Geran: JUMLAH = PEMBERIAN - PERBELANJAAN - BAYAR BALIK.
    legend_total_upper = df_chart_geran[legend_col].astype(str).str.strip().str.upper()
    jumlah_pemberian_data = df_chart_geran.loc[
        legend_total_upper.eq("PEMBERIAN"),
        amount_col
    ].sum()
    jumlah_perbelanjaan_data = df_chart_geran.loc[
        legend_total_upper.eq("PERBELANJAAN"),
        amount_col
    ].sum()
    jumlah_bayar_balik_data = df_chart_geran.loc[
        legend_total_upper.isin(["BYR BALIK", "BAYAR BALIK"]),
        amount_col
    ].sum()

    jumlah_bersih_geran = (
        jumlah_pemberian_data
        - jumlah_perbelanjaan_data
        - jumlah_bayar_balik_data
    )

    df_data_carta_geran_gabung = pd.concat(
        [
            df_data_carta_geran_gabung,
            pd.DataFrame([{
                "PTJ": "JUMLAH",
                "NAMA": "",
                "LEGEND": "PEMBERIAN - PERBELANJAAN - BAYAR BALIK",
                "JUMLAH": jumlah_bersih_geran
            }])
        ],
        ignore_index=True
    )

    with st.expander("📄 DATA CARTA GERAN", expanded=False):
        df_data_carta_geran_show = dataframe_comma_style(
            df_data_carta_geran_gabung,
            money_cols=["JUMLAH"]
        )

        st.dataframe(
            df_data_carta_geran_show,
            use_container_width=True,
            hide_index=True
        )

        # Download kekal raw numeric dalam satu sheet sahaja.
        excel_data_carta = to_excel(
            df_data_carta_geran_gabung,
            sheet_name="DATA_CARTA_GERAN"
        )

        st.download_button(
            "📥 Download Data Carta Geran",
            data=excel_data_carta,
            file_name="Data_Carta_Geran.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

# =======================
# MENU LAIN
# =======================
elif menu == "3. P&L":

    with st.sidebar:
        st.markdown("### 🔎  P&L")
        pilihan_pl = st.radio(
            "Pilih Paparan",
            [
                "Prestasi Hasil & Belanja CIDB",
                "Pecahan Belanja CIDB",
                "Surplus/(Defisit) Prestasi Bajet CIDB"
            ],
            index=0
        )

    # =======================
    # P&L - DATA RASMI JADUAL 6
    # Rujukan: 4.0 PRESTASI KEWANGAN CIDB
    # Jadual 6: Ringkasan Hasil dan Perbelanjaan Sehingga 31 Mac 2026
    # =======================

    def kira_prestasi(sebenar, asas):
        sebenar = pd.to_numeric(sebenar, errors="coerce")
        asas = pd.to_numeric(asas, errors="coerce")
        if pd.isna(sebenar) or pd.isna(asas) or asas == 0:
            return None
        return (sebenar / asas) * 100

    def label_pct(nilai):
        nilai = pd.to_numeric(nilai, errors="coerce")
        if pd.isna(nilai):
            return "-"
        return f"{nilai:.0f}%"

    def format_juta_2(nilai):
        nilai = pd.to_numeric(nilai, errors="coerce")
        if pd.isna(nilai):
            nilai = 0
        return f"{nilai / 1_000_000:,.2f}"

    df_pl_jadual6 = pd.DataFrame({
        "PERKARA": [
            "Hasil",
            "Belanja program industri",
            "Belanja mengurus",
            "Jumlah perbelanjaan",
            "Untung sebelum cukai dan zakat",
            "Cukai",
            "Zakat",
            "Untung selepas cukai dan zakat",
            "Belanja Modal",
            "Jumlah Perbelanjaan",
            "Lebihan/(Kurangan) Pendapatan Termasuk S/Nilai & H.Ragu",
            "(-) S/Nilai & H. Ragu",
            "Lebihan/(Kurangan) Pendapatan Tidak Termasuk S/Nilai & H.Ragu",
        ],
        "BAJET 2026": [
            485_000_000,
            205_000_000,
            189_000_000,
            394_000_000,
            91_000_000,
            8_000_000,
            1_000_000,
            82_000_000,
            91_000_000,
            485_000_000,
            0,
            24_600_000,
            24_600_000,
        ],
        "BAJET 03-2026": [
            120_730_700,
            30_858_400,
            39_205_700,
            70_064_100,
            50_666_600,
            0,
            0,
            50_666_600,
            3_324_400,
            73_388_500,
            47_342_200,
            6_000_000,
            53_342_200,
        ],
        "SEBENAR 03-2026": [
            130_107_903,
            28_262_263,
            35_170_017,
            63_432_280,
            66_675_622,
            0,
            0,
            66_675_622,
            2_755_188,
            66_187_468,
            63_920_434,
            5_865_129,
            69_785_563,
        ],
        "SEBENAR 03-2025": [
            109_523_154,
            25_014_879,
            32_782_537,
            57_797_416,
            51_725_738,
            0,
            0,
            51_725_738,
            1_042_041,
            58_839_457,
            50_683_697,
            5_828_867,
            56_512_564,
        ],
    })

    # Kira peratus ikut formula Jadual 6.
    df_pl_jadual6["Prestasi Bajet 03-2026"] = df_pl_jadual6.apply(
        lambda row: kira_prestasi(row["SEBENAR 03-2026"], row["BAJET 03-2026"]),
        axis=1
    )
    df_pl_jadual6["Prestasi Bajet 2026"] = df_pl_jadual6.apply(
        lambda row: kira_prestasi(row["SEBENAR 03-2026"], row["BAJET 2026"]),
        axis=1
    )
    df_pl_jadual6["Prestasi 03-26 vs 03-25"] = df_pl_jadual6.apply(
        lambda row: kira_prestasi(row["SEBENAR 03-2026"], row["SEBENAR 03-2025"]),
        axis=1
    )

    # Paparan utama P&L: Hasil, Jumlah Perbelanjaan dan lebihan.
    df_pl = pd.DataFrame({
        "PERKARA": [
            "HASIL",
            "JUMLAH PERBELANJAAN",
            "LEBIHAN/(KURANGAN) PENDAPATAN TIDAK TERMASUK S/NILAI & H.RAGU"
        ],
        "BAJET 2026": [
            485_000_000,
            485_000_000,
            24_600_000,
        ],
        "BAJET 03-2026": [
            120_730_700,
            73_388_500,
            53_342_200,
        ],
        "SEBENAR 03-2026": [
            130_107_903,
            66_187_468,
            69_785_563,
        ],
        "SEBENAR 03-2025": [
            109_523_154,
            58_839_457,
            56_512_564,
        ],
    })

    df_pecahan_belanja = pd.DataFrame({
        "KATEGORI": [
            "Belanja program industri",
            "Belanja mengurus",
            "Belanja Modal"
        ],
        "BAJET 2026": [205_000_000, 189_000_000, 91_000_000],
        "BAJET 03-2026": [30_858_400, 39_205_700, 3_324_400],
        "SEBENAR 03-2026": [28_262_263, 35_170_017, 2_755_188],
        "SEBENAR 03-2025": [25_014_879, 32_782_537, 1_042_041],
        "Prestasi Bajet 03-2026": [92, 90, 83],
        "Prestasi Bajet 2026": [14, 19, 3],
        "Prestasi 03-26 vs 03-25": [113, 107, 264],
    })

    # =======================
    # KPI RINGKAS
    # =======================
    hasil_row = df_pl[df_pl["PERKARA"] == "HASIL"].iloc[0]
    belanja_row = df_pl[df_pl["PERKARA"] == "JUMLAH PERBELANJAAN"].iloc[0]
    lebihan_row = df_pl[df_pl["PERKARA"].str.contains("LEBIHAN", na=False)].iloc[0]

    col_pl1, col_pl2, col_pl3, col_pl4 = st.columns(4)
    with col_pl1:
        st.metric(
            "Hasil Sebenar 03-2026",
            format_nilai(hasil_row["SEBENAR 03-2026"]),
            f'{label_pct(kira_prestasi(hasil_row["SEBENAR 03-2026"], hasil_row["BAJET 03-2026"]))} vs Bajet 03-2026'
        )
    with col_pl2:
        st.metric(
            "Jumlah Perbelanjaan",
            format_nilai(belanja_row["SEBENAR 03-2026"]),
            f'{label_pct(kira_prestasi(belanja_row["SEBENAR 03-2026"], belanja_row["BAJET 03-2026"]))} vs Bajet 03-2026'
        )
    with col_pl3:
        st.metric(
            "Lebihan Pendapatan",
            format_nilai(lebihan_row["SEBENAR 03-2026"]),
            f'{format_nilai(lebihan_row["SEBENAR 03-2026"] - lebihan_row["SEBENAR 03-2025"])} vs 03-2025'
        )
    with col_pl4:
        st.metric(
            "Untung Selepas Cukai & Zakat",
            format_nilai(66_675_622),
            f'{format_nilai(66_675_622 - 51_725_738)} vs 03-2025'
        )

    st.markdown(f"### 📊 {pilihan_pl}")

    if pilihan_pl == "Prestasi Hasil & Belanja CIDB":

        df_chart_pl = df_pl[
            df_pl["PERKARA"].isin(["HASIL", "JUMLAH PERBELANJAAN"])
        ].copy()

        df_chart_pl = df_chart_pl.melt(
            id_vars="PERKARA",
            value_vars=["BAJET 2026", "BAJET 03-2026", "SEBENAR 03-2026", "SEBENAR 03-2025"],
            var_name="JENIS",
            value_name="NILAI"
        )

        df_chart_pl["NILAI"] = pd.to_numeric(df_chart_pl["NILAI"], errors="coerce").fillna(0)
        df_chart_pl["NILAI_JUTA"] = df_chart_pl["NILAI"] / 1_000_000
        df_chart_pl["LABEL"] = df_chart_pl["NILAI_JUTA"].map(lambda x: f"{x:,.2f}")

        y_max = df_chart_pl["NILAI_JUTA"].max()

        fig_pl = px.bar(
            df_chart_pl,
            x="JENIS",
            y="NILAI_JUTA",
            color="PERKARA",
            barmode="group",
            text="LABEL",
            height=720,
            color_discrete_map={
                "HASIL": "#d8b4d8",
                "JUMLAH PERBELANJAAN": "#e8742f"
            },
            labels={
                "JENIS": "",
                "NILAI_JUTA": "Juta",
                "PERKARA": ""
            },
            title="PRESTASI HASIL & PERBELANJAAN CIDB SEHINGGA 31 MAC 2026"
        )

        fig_pl.update_traces(
            texttemplate="%{text}",
            textposition="outside",
            cliponaxis=False,
            constraintext="none",
            textfont=dict(size=14, color="black", family="Arial")
        )

        fig_pl.update_layout(
            template="plotly_white",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.25,
                xanchor="center",
                x=0.5
            ),
            margin=dict(t=160, b=150, l=90, r=90),
            xaxis_title="",
            yaxis_title="Juta",
            xaxis_tickangle=0,
            yaxis_range=[0, y_max * 1.25 if y_max else 1],
            uniformtext_minsize=7,
            uniformtext_mode="show"
        )

        st.plotly_chart(fig_pl, use_container_width=True)




        df_data_pilihan = df_pl_jadual6.copy()
        sheet_name = "JADUAL6_PL"

    elif pilihan_pl == "Pecahan Belanja CIDB":

        df_belanja_chart = df_pecahan_belanja.melt(
            id_vars="KATEGORI",
            value_vars=["BAJET 2026", "BAJET 03-2026", "SEBENAR 03-2026", "SEBENAR 03-2025"],
            var_name="JENIS",
            value_name="NILAI"
        )

        df_belanja_chart["NILAI"] = pd.to_numeric(df_belanja_chart["NILAI"], errors="coerce").fillna(0)
        df_belanja_chart["NILAI_JUTA"] = df_belanja_chart["NILAI"] / 1_000_000
        df_belanja_chart["LABEL"] = df_belanja_chart["NILAI_JUTA"].map(lambda x: f"{x:,.2f}")

        y_max = df_belanja_chart["NILAI_JUTA"].max()

        fig_belanja = px.bar(
            df_belanja_chart,
            x="KATEGORI",
            y="NILAI_JUTA",
            color="JENIS",
            barmode="group",
            text="LABEL",
            height=720,
            color_discrete_sequence=["#d8b4d8", "#e8742f", "#8fd17f", "#7aa6c2"],
            labels={
                "KATEGORI": "",
                "NILAI_JUTA": "Juta",
                "JENIS": ""
            },
            title="PECAHAN BELANJA CIDB SEHINGGA 31 MAC 2026"
        )

        fig_belanja.update_traces(
            texttemplate="%{text}",
            textposition="outside",
            cliponaxis=False,
            constraintext="none",
            textfont=dict(size=13, color="black", family="Arial")
        )

        fig_belanja.update_layout(
            template="plotly_white",
            margin=dict(t=160, b=150, l=90, r=90),
            xaxis_tickangle=0,
            yaxis_title="Juta",
            yaxis_range=[0, y_max * 1.30 if y_max else 1],
            uniformtext_minsize=7,
            uniformtext_mode="show"
        )

        st.plotly_chart(fig_belanja, use_container_width=True)

        df_belanja_pct = df_pecahan_belanja.melt(
            id_vars="KATEGORI",
            value_vars=["Prestasi Bajet 03-2026", "Prestasi Bajet 2026", "Prestasi 03-26 vs 03-25"],
            var_name="JENIS",
            value_name="PERATUS"
        )




        df_data_pilihan = df_pecahan_belanja.copy()
        sheet_name = "PECAHAN_BELANJA"

    else:

        df_surplus = df_pl[
            df_pl["PERKARA"].str.contains("LEBIHAN", na=False)
        ].copy()

        df_surplus_chart = df_surplus.melt(
            id_vars="PERKARA",
            value_vars=["BAJET 2026", "BAJET 03-2026", "SEBENAR 03-2026", "SEBENAR 03-2025"],
            var_name="JENIS",
            value_name="NILAI"
        )

        df_surplus_chart["NILAI"] = pd.to_numeric(df_surplus_chart["NILAI"], errors="coerce").fillna(0)
        df_surplus_chart["NILAI_JUTA"] = df_surplus_chart["NILAI"] / 1_000_000
        df_surplus_chart["LABEL"] = df_surplus_chart["NILAI_JUTA"].map(lambda x: f"{x:,.2f}")

        fig_surplus = px.bar(
            df_surplus_chart,
            x="JENIS",
            y="NILAI_JUTA",
            text="LABEL",
            height=720,
            color="JENIS",
            color_discrete_map={
                "BAJET 2026": "#d9534f",
                "BAJET 03-2026": "#a8d5a2",
                "SEBENAR 03-2026": "#2e8b57",
                "SEBENAR 03-2025": "#5cb85c"
            },
            labels={
                "JENIS": "",
                "NILAI_JUTA": "Juta"
            },
            title="LEBIHAN/(KURANGAN) PENDAPATAN TIDAK TERMASUK S/NILAI & H.RAGU"
        )

        fig_surplus.update_traces(
            texttemplate="%{text}",
            textposition="outside",
            cliponaxis=False,
            constraintext="none",
            textfont=dict(size=14, color="black", family="Arial")
        )

        min_y = df_surplus_chart["NILAI_JUTA"].min()
        max_y = df_surplus_chart["NILAI_JUTA"].max()

        fig_surplus.update_layout(
            template="plotly_white",
            showlegend=False,
            margin=dict(t=170, b=150, l=90, r=90),
            xaxis_tickangle=0,
            yaxis_title="Juta",
            yaxis_range=[
                min_y * 1.35 if min_y < 0 else 0,
                max_y * 1.30 if max_y > 0 else 1
            ],
            uniformtext_minsize=7,
            uniformtext_mode="show"
        )

        st.plotly_chart(fig_surplus, use_container_width=True)

        df_untung = df_pl_jadual6[
            df_pl_jadual6["PERKARA"].isin([
                "Untung sebelum cukai dan zakat",
                "Untung selepas cukai dan zakat",
                "Lebihan/(Kurangan) Pendapatan Termasuk S/Nilai & H.Ragu",
                "(-) S/Nilai & H. Ragu",
                "Lebihan/(Kurangan) Pendapatan Tidak Termasuk S/Nilai & H.Ragu"
            ])
        ].copy()

        df_untung_chart = df_untung.melt(
            id_vars="PERKARA",
            value_vars=["BAJET 2026", "BAJET 03-2026", "SEBENAR 03-2026", "SEBENAR 03-2025"],
            var_name="JENIS",
            value_name="NILAI"
        )
        df_untung_chart["NILAI_JUTA"] = pd.to_numeric(df_untung_chart["NILAI"], errors="coerce").fillna(0) / 1_000_000
        df_untung_chart["LABEL"] = df_untung_chart["NILAI_JUTA"].map(lambda x: f"{x:,.2f}")




        df_data_pilihan = df_pl_jadual6.copy()
        sheet_name = "SURPLUS_DEFISIT"

    st.markdown("### 📋 Data P&L - Jadual 6")

    df_show = df_data_pilihan.copy()

    money_cols = [
        "BAJET 2026", "BAJET 03-2026", "SEBENAR 03-2026", "SEBENAR 03-2025"
    ]
    percent_cols = [
        "Prestasi Bajet 03-2026", "Prestasi Bajet 2026", "Prestasi 03-26 vs 03-25"
    ]

    for col in money_cols:
        if col in df_show.columns:
            df_show[col] = pd.to_numeric(df_show[col], errors="coerce").fillna(0).apply(format_comma)

    for col in percent_cols:
        if col in df_show.columns:
            df_show[col] = pd.to_numeric(df_show[col], errors="coerce").map(
                lambda x: "-" if pd.isna(x) else f"{x:.0f}%"
            )

    # Papar '-' untuk Cukai/Zakat yang tiada nilai sasaran/sebenar dalam jadual asal.
    if "PERKARA" in df_show.columns:
        cukai_zakat_mask = df_show["PERKARA"].astype(str).isin(["Cukai", "Zakat"])
        for col in ["BAJET 03-2026", "SEBENAR 03-2026", "SEBENAR 03-2025"]:
            if col in df_show.columns:
                df_show.loc[cukai_zakat_mask, col] = "-"
        for col in percent_cols:
            if col in df_show.columns:
                df_show.loc[cukai_zakat_mask, col] = "-"

    st.dataframe(df_show, use_container_width=True, hide_index=True)

    excel_pl = to_excel(df_data_pilihan, sheet_name=sheet_name)

    st.download_button(
        "📥 Download Data P&L Excel",
        data=excel_pl,
        file_name="Data_PL_Jadual6_CIDB.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )

elif menu == "4. Balance Sheet":

    # =======================
    # BALANCE SHEET
    # Rujukan Word:
    # Jadual 7: Penyata Kedudukan Kewangan pada 31 Mac 2026
    #
    # Data sebenar daripada Word:
    # 03-2026 dan 2025
    # =======================

    st.markdown("### 📊 PENYATA KEDUDUKAN KEWANGAN CIDB PADA 03-2026")

    df_bs = pd.DataFrame({
        "PERKARA": [
            "ASET 2025",
            "LIABILITI & A.BERSIH 2025",
            "ASET 03-2026",
            "LIABILITI & A.BERSIH 03-2026"
        ],

        "ASET BERSIH (RM)": [
            0,
            1140889719,
            0,
            1207565341
        ],

        "BUKAN SEMASA (RM)": [
            493358471,
            35235965,
            490248527,
            35061911
        ],

        "SEMASA (RM)": [
            742014399,
            59247186,
            764763086,
            12384361
        ],

        "JUMLAH": [
            1235372870,
            1235372870,
            1255011613,
            1255011613
        ]
    })

    # =======================
    # CARTA BALANCE SHEET
    # =======================
    df_bs_chart = df_bs.copy()

    for col in ["ASET BERSIH (RM)", "BUKAN SEMASA (RM)", "SEMASA (RM)", "JUMLAH"]:
        df_bs_chart[col] = pd.to_numeric(
            df_bs_chart[col],
            errors="coerce"
        ).fillna(0)

    df_bs_chart_juta = df_bs_chart.copy()

    for col in ["ASET BERSIH (RM)", "BUKAN SEMASA (RM)", "SEMASA (RM)", "JUMLAH"]:
        df_bs_chart_juta[col] = df_bs_chart_juta[col] / 1_000_000

    fig_bs = go.Figure()

    warna_bs = {
        "ASET BERSIH (RM)": "#b7e4a8",
        "BUKAN SEMASA (RM)": "#ef7130",
        "SEMASA (RM)": "#7ec8e3"
    }

    for col in ["ASET BERSIH (RM)", "BUKAN SEMASA (RM)", "SEMASA (RM)"]:
        fig_bs.add_trace(
            go.Bar(
                x=df_bs_chart_juta["PERKARA"],
                y=df_bs_chart_juta[col],
                name=col,
                marker_color=warna_bs[col],
                text=[
                    "-" if nilai == 0 else f"{nilai:,.2f}"
                    for nilai in df_bs_chart_juta[col]
                ],
                textposition="inside",
                insidetextanchor="middle",
                textfont=dict(
                    size=13,
                    color="#2c3e50",
                    family="Arial"
                ),
                hovertemplate=(
                    "<b>%{x}</b><br>"
                    + col
                    + ": RM %{customdata:,.2f}<extra></extra>"
                ),
                customdata=df_bs_chart[col]
            )
        )

    # Label jumlah di atas setiap stacked bar
    fig_bs.add_trace(
        go.Scatter(
            x=df_bs_chart_juta["PERKARA"],
            y=df_bs_chart_juta["JUMLAH"],
            mode="text",
            text=[
                f"{nilai:,.2f}"
                for nilai in df_bs_chart_juta["JUMLAH"]
            ],
            textposition="top center",
            textfont=dict(
                size=16,
                color="black",
                family="Arial"
            ),
            name="Jumlah",
            showlegend=False,
            hoverinfo="skip"
        )
    )

    fig_bs.update_layout(
        title="PENYATA KEDUDUKAN KEWANGAN CIDB PADA 03-2026",
        barmode="stack",
        height=720,
        template="plotly_white",
        margin=dict(t=100, b=140, l=80, r=60),
        xaxis=dict(
            title="",
            tickangle=0,
            automargin=True
        ),
        yaxis=dict(
            title="Juta",
            rangemode="tozero"
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.22,
            xanchor="center",
            x=0.5
        ),
        uniformtext_minsize=8,
        uniformtext_mode="show"
    )

    st.plotly_chart(
        fig_bs,
        use_container_width=True
    )

    # =======================
    # DATA BALANCE SHEET
    # =======================
    st.markdown("### 📋 Data Balance Sheet")

    df_bs_show = df_bs.copy()

    for col in ["ASET BERSIH (RM)", "BUKAN SEMASA (RM)", "SEMASA (RM)", "JUMLAH"]:
        df_bs_show[col] = (
            pd.to_numeric(df_bs_show[col], errors="coerce")
            .fillna(0)
            .apply(format_comma)
        )

    df_bs_show.loc[
        df_bs["ASET BERSIH (RM)"] == 0,
        "ASET BERSIH (RM)"
    ] = "-"

    st.dataframe(
        df_bs_show,
        use_container_width=True,
        hide_index=True
    )

    excel_bs = to_excel(
        df_bs,
        sheet_name="BALANCE_SHEET"
    )

    st.download_button(
        "📥 Download Balance Sheet Excel",
        data=excel_bs,
        file_name="Balance_Sheet_CIDB.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )

elif menu == "5. Cash Flow":

    # =======================
    # CASH FLOW
    # Rujukan Word:
    # Jadual 8: Penyata Aliran Tunai bagi tahun kewangan berakhir 31 Mac 2026
    #
    # Data diekstrak daripada Word:
    # 03-2026 dan 2025
    # =======================

    st.markdown("### 📊 PENYATA ALIRAN TUNAI CIDB 03-2026")

    df_cf = pd.DataFrame({
        "PERKARA": [
            "SEBENAR 2025",
            "SEBENAR 03-2026"
        ],

        "BAKI TUNAI AWAL (RM)": [
            608091383,
            693799652
        ],

        "AKT. OPERASI (RM)": [
            108433429,
            5401283
        ],

        "AKT. PELABURAN (RM)": [
            -22725160,
            3730999
        ],

        "AKT. PEMBIAYAAN (RM)": [
            0,
            0
        ],

        "PENGURANGAN/PENAMBAHAN BERSIH (RM)": [
            85708269,
            9132282
        ],

        "BAKI TUNAI AKHIR (RM)": [
            693799652,
            702931934
        ]
    })

    # =======================
    # CARTA CASH FLOW
    # Ikut gaya contoh: horizontal bar untuk
    # Baki Tunai Awal, Aktiviti Operasi, Aktiviti Pelaburan, Baki Tunai Akhir.
    # =======================
    df_cf_chart = df_cf.copy()

    chart_cols = [
        "BAKI TUNAI AKHIR (RM)",
        "AKT. PELABURAN (RM)",
        "AKT. OPERASI (RM)",
        "BAKI TUNAI AWAL (RM)"
    ]

    for col in chart_cols:
        df_cf_chart[col] = (
            pd.to_numeric(df_cf_chart[col], errors="coerce")
            .fillna(0)
            / 1_000_000
        )

    fig_cf = go.Figure()

    warna_cf = {
        "BAKI TUNAI AKHIR (RM)": "#3b821f",
        "AKT. PELABURAN (RM)": "#20dbe0",
        "AKT. OPERASI (RM)": "#ffc000",
        "BAKI TUNAI AWAL (RM)": "#00f29a"
    }

    for col in chart_cols:
        fig_cf.add_trace(
            go.Bar(
                y=df_cf_chart["PERKARA"],
                x=df_cf_chart[col],
                name=col,
                orientation="h",
                marker_color=warna_cf[col],
                text=[
                    f"{x:,.2f}"
                    for x in df_cf_chart[col]
                ],
                textposition="outside",
                textfont=dict(
                    size=14,
                    color="#3b3b3b",
                    family="Arial"
                ),
                hovertemplate=(
                    "<b>%{y}</b><br>"
                    + col
                    + ": RM %{customdata:,.2f}<extra></extra>"
                ),
                customdata=df_cf[col]
            )
        )

    fig_cf.update_layout(
        title="PENYATA ALIRAN TUNAI CIDB 03-2026",
        template="plotly_white",
        barmode="group",
        height=720,
        margin=dict(
            t=100,
            b=130,
            l=140,
            r=80
        ),
        xaxis=dict(
            title="Juta",
            zeroline=True,
            tickformat=","
        ),
        yaxis=dict(
            title="",
            categoryorder="array",
            categoryarray=[
                "SEBENAR 2025",
                "SEBENAR 03-2026"
            ]
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.25,
            xanchor="center",
            x=0.5
        ),
        uniformtext_minsize=8,
        uniformtext_mode="show"
    )

    st.plotly_chart(
        fig_cf,
        use_container_width=True
    )

    # =======================
    # DATA CASH FLOW
    # =======================
    st.markdown("### 📋 Data Cash Flow")

    df_cf_show = df_cf.copy()

    for col in [
        "BAKI TUNAI AWAL (RM)",
        "AKT. OPERASI (RM)",
        "AKT. PELABURAN (RM)",
        "AKT. PEMBIAYAAN (RM)",
        "PENGURANGAN/PENAMBAHAN BERSIH (RM)",
        "BAKI TUNAI AKHIR (RM)"
    ]:
        df_cf_show[col] = (
            pd.to_numeric(df_cf_show[col], errors="coerce")
            .fillna(0)
            .apply(format_comma)
        )

    st.dataframe(
        df_cf_show,
        use_container_width=True,
        hide_index=True
    )

    excel_cf = to_excel(
        df_cf,
        sheet_name="CASH_FLOW"
    )

    st.download_button(
        "📥 Download Cash Flow Excel",
        data=excel_cf,
        file_name="Cash_Flow_CIDB.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )

