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
</style>
""")

# =======================
# FUNGSI UMUM
# =======================
def format_nilai(nilai):
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
# =======================
@st.cache_data
def load_data():
    df_dict = {}
    errors = []

    files = {
        "03-2025": "JPKA_ANALISA PK CIDB 03-2025.xlsx",
        "06-2025": "JPKA_ANALISA PK CIDB 06-2025.xlsx",
        "09-2025": "JPKA_ANALISA PK CIDB 09-2025.xlsx",
        "12-2025": "JPKA_ANALISA PK CIDB 12-2025.xlsx",
        "03-2026": "JPKA_ANALISA PK CIDB 03-2026.xlsx"
    }

    for q, filename in files.items():
        try:
            df = pd.read_excel(filename, sheet_name="All2")
            df = bersih_nama_column(df)

            if "KOD" in df.columns and "KOD1" not in df.columns:
                df = df.rename(columns={"KOD": "KOD1"})

            # Standardize nama column untuk dashboard.
            # Untuk fail 2026, column seperti BAJET 2026 / SASARAN Q1-26 / SEBENAR Q1-26
            # akan ditukar kepada nama standard yang digunakan oleh dashboard.
            rename_map = {
                "BAJET 2026": "BAJET 2025",
                "SASARAN Q1-26": "SASARAN Q1-25",
                "SEBENAR Q1-26": "SEBENAR Q1-25"
            }

            df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns and v not in df.columns})

            df["Sumber"] = q
            df["Quarter"] = q
            df["Tahun"] = int(q.split("-")[1])

            numeric_cols = ["BAJET 2025", "SASARAN Q1-25", "SEBENAR Q1-25"]
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
    filename = "GL ADV 03-2026 14052026.xlsx"

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
# SIDEBAR MENU UTAMA
# =======================
st.sidebar.markdown(
    dedent("""
    <h2 style="text-align:center; color:#1e40af; margin-bottom:20px;">
        📊 DASHBOARD CIDB
    </h2>
    """).strip(),
    unsafe_allow_html=True
)

menu = st.sidebar.radio(
    "Pilih Modul",
    options=["1. Belanja & Hasil", "2. Geran", "3. P&L", "4. Balance Sheet", "5. Cash Flow"],
    label_visibility="collapsed"
)

tajuk_utama = {
    "1. Belanja & Hasil": "📊 PRESTASI PERBELANJAAN DAN HASIL CIDB",
    "2. Geran": "📊 PRESTASI GERAN",
    "3. P&L": "📊 Profit & Lost",
    "4. Balance Sheet": "📊Balance Sheet",
    "5. Cash Flow": "📊 Cash Flow",
}

html(f"""
<h1 style="text-align:center; font-weight:bold; font-size:28px; color:#2c3e50;">
    {tajuk_utama.get(menu, "📊 DASHBOARD CIDB")}
</h1>
""")

st.sidebar.markdown("---")

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

    quarters_available = [q for q in ["03-2025", "06-2025", "09-2025", "12-2025", "03-2026"] if q in df_dict]

    with st.sidebar:
        st.markdown("### 🔎 PILIHAN PENAPIS")
        default_quarter = ["03-2026"] if "03-2026" in quarters_available else (["12-2025"] if "12-2025" in quarters_available else quarters_available[:1])
        pilih_quarter = st.multiselect("Pilih Quarter", quarters_available, default=default_quarter)

    if not pilih_quarter:
        st.warning("Sila pilih sekurang-kurangnya satu Quarter.")
        st.stop()

    dfs = [df_dict[q] for q in pilih_quarter if q in df_dict]
    if not dfs:
        st.warning("Tiada data untuk Quarter yang dipilih.")
        st.stop()

    df_tapis = pd.concat(dfs, ignore_index=True)
    df_tapis = bersih_nama_column(df_tapis)

    required_cols = [
        "PTJ", "PTJ1", "Kategori", "DESC", "KOD1",
        "BAJET 2025", "SASARAN Q1-25", "SEBENAR Q1-25", "Quarter"
    ]
    missing_cols = [col for col in required_cols if col not in df_tapis.columns]
    if missing_cols:
        st.error("Column berikut tiada dalam data Belanja & Hasil:")
        st.write(missing_cols)
        st.stop()

    with st.sidebar:
        senarai_ptj = unique_sorted(df_tapis["PTJ"])
        pilih_ptj = st.multiselect("Pilih PTJ", senarai_ptj, default=senarai_ptj)
        df_tapis = df_tapis[df_tapis["PTJ"].astype(str).isin(pilih_ptj)]

        senarai_ptj1 = unique_sorted(df_tapis["PTJ1"])
        pilih_ptj1 = st.multiselect("Pilih PTJ1", senarai_ptj1, default=senarai_ptj1)
        df_tapis = df_tapis[df_tapis["PTJ1"].astype(str).isin(pilih_ptj1)]

        senarai_kategori = unique_sorted(df_tapis["Kategori"])
        pilih_kategori = st.multiselect("Pilih Kategori", senarai_kategori, default=senarai_kategori)
        df_tapis = df_tapis[df_tapis["Kategori"].astype(str).isin(pilih_kategori)]

        senarai_desc = unique_sorted(df_tapis["DESC"])
        pilih_desc = st.multiselect("Pilih DESC", senarai_desc, default=senarai_desc)
        df_tapis = df_tapis[df_tapis["DESC"].astype(str).isin(pilih_desc)]

        senarai_kod1 = unique_sorted(df_tapis["KOD1"])
        pilih_kod1 = st.multiselect("Pilih KOD1", senarai_kod1, default=senarai_kod1)
        df_tapis = df_tapis[df_tapis["KOD1"].astype(str).isin(pilih_kod1)]

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

    st.markdown("### 🚦 STATUS PRESTASI PTJ1")

    df_akhir["Prestasi_%"] = df_akhir.apply(
        lambda row: hitung_prestasi(row["SEBENAR Q1-25"], row["SASARAN Q1-25"]),
        axis=1
    )

    df_group = df_akhir.groupby("PTJ1", as_index=False).agg({
        "SASARAN Q1-25": "sum",
        "SEBENAR Q1-25": "sum"
    })

    df_group["Prestasi_%"] = df_group.apply(
        lambda row: hitung_prestasi(row["SEBENAR Q1-25"], row["SASARAN Q1-25"]),
        axis=1
    )

    hebat = len(df_group[df_group["Prestasi_%"] > 95])
    bagus = len(df_group[(df_group["Prestasi_%"] >= 85) & (df_group["Prestasi_%"] <= 94.99)])
    usaha = len(df_group[df_group["Prestasi_%"] < 85])
    total = len(df_group)

    total_sebenar = df_akhir["SEBENAR Q1-25"].sum()
    total_sasaran = df_akhir["SASARAN Q1-25"].sum()
    pencapaian = hitung_prestasi(total_sebenar, total_sasaran)
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
            <h5 style="margin:0;color:#2c3e50;">Jumlah PTJ1</h5>
            <hr style="margin:8px 0;">
            <p style="margin:3px 0;"><strong>SASARAN</strong> 100%</p>
            <p style="margin:3px 0;"><strong>PRESTASI</strong> {pencapaian_int}%</p>
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
            st.dataframe(df_show[["PTJ1", "Prestasi_%"]].round(2), use_container_width=True, hide_index=True)
        else:
            st.info("Tiada rekod untuk kategori ini.")

        if st.button("❌ Tutup Senarai", type="primary"):
            st.session_state.show_drill_belanja = None
            st.rerun()

    with st.expander("📋 RINGKASAN KESELURUHAN", expanded=False):
        for q in pilih_quarter:
            df_q = df_akhir[df_akhir["Quarter"] == q]
            with st.expander(f"Quarter {q}", expanded=True):
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
                                <span class="metric-label">Sasaran</span>
                                <span style="font-weight:bold; color:#E08E4E;">{format_nilai(s)}</span>
                            </div>
                            <div class="metric-row">
                                <span class="metric-label">Sebenar</span>
                                <span style="font-weight:bold; color:#2E8B6D;">{format_nilai(se)}</span>
                            </div>
                        </div>
                        """)

    with st.expander("📊 CARTA 1: PERBANDINGAN MENGIKUT KATEGORI", expanded=False):
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
                    st.markdown(f"**Quarter {q}**")
                    fig = px.bar(
                        df_c1,
                        x="Kategori",
                        y=["BAJET_JT", "SASARAN_JT", "SEBENAR_JT"],
                        barmode="group",
                        height=520,
                        # PEMBERIAN = Kuning
        # PERBELANJAAN = Merah
        # BYR BALIK = Hijau
        # Warna soft / pastel
        color_discrete_sequence=["#f6d365", "#f4978e", "#95d5b2"]
                    )
                    for trace in fig.data:
                        trace.text = [format_nilai(x * 1_000_000) for x in trace.y]
                        trace.textposition = "outside"
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
                height=550,
                color_discrete_sequence=["#2C7DA6", "#E08E4E", "#2E8B6D"]
            )
            for trace in fig1.data:
                trace.text = [format_nilai(x * 1_000_000) for x in trace.y]
                trace.textposition = "outside"
            st.plotly_chart(fig1, use_container_width=True)

    with st.expander("📊 CARTA 2: JUMLAH SEBENAR MENGIKUT QUARTER", expanded=False):
        df_total = df_akhir.groupby("Quarter", as_index=False)["SEBENAR Q1-25"].sum()
        df_total = df_total.sort_values("Quarter")
        fig_total = px.bar(
            df_total,
            x="Quarter",
            y="SEBENAR Q1-25",
            title="Jumlah Sebenar Mengikut Quarter",
            labels={"SEBENAR Q1-25": "Jumlah Sebenar (RM)"},
            text=df_total["SEBENAR Q1-25"].apply(format_nilai)
        )
        fig_total.update_traces(textposition="outside", marker_color="#2E8B6D")
        fig_total.update_layout(height=600, yaxis_title="Jumlah Sebenar (RM)")
        st.plotly_chart(fig_total, use_container_width=True)

    with st.expander("📊 CARTA 3: PRESTASI MENGIKUT DESC", expanded=False):
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
                    st.markdown(f"**Quarter {q}**")
                    fig2 = px.bar(
                        df_c2,
                        y="DESC",
                        x=["SASARAN Q1-25", "SEBENAR Q1-25"],
                        orientation="h",
                        barmode="group",
                        height=700,
                        color_discrete_sequence=["#E08E4E", "#2E8B6D"]
                    )
                    for trace in fig2.data:
                        trace.text = [format_nilai(x) for x in trace.x]
                        trace.textposition = "outside"
                    fig2.update_layout(yaxis=dict(categoryorder="array", categoryarray=df_c2["DESC"].tolist()))
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
                height=700,
                color_discrete_sequence=["#E08E4E", "#2E8B6D"]
            )
            for trace in fig2.data:
                trace.text = [format_nilai(x) for x in trace.x]
                trace.textposition = "outside"
            fig2.update_layout(yaxis=dict(categoryorder="array", categoryarray=df_c2["DESC"].tolist()))
            st.plotly_chart(fig2, use_container_width=True)

    with st.expander("📈 CARTA 4: PRESTASI MENGIKUT PTJ1", expanded=False):
        df_c3 = df_group.sort_values(by="Prestasi_%", ascending=False).reset_index(drop=True)
        y_max = max(140, int(df_c3["Prestasi_%"].max()) + 20 if not df_c3.empty else 140)

        fig3 = go.Figure()
        fig3.add_trace(go.Bar(
            x=df_c3["PTJ1"],
            y=df_c3["Prestasi_%"],
            name="Prestasi",
            marker_color="#2E8B6D",
            text=df_c3["Prestasi_%"].round(0).astype(int).astype(str) + "%",
            textposition="inside"
        ))
        fig3.add_trace(go.Scatter(
            x=df_c3["PTJ1"],
            y=[100] * len(df_c3),
            name="Sasaran 100%",
            line=dict(color="#E08E4E", width=3, dash="dash"),
            mode="lines"
        ))
        fig3.add_trace(go.Scatter(
            x=df_c3["PTJ1"],
            y=df_c3["Prestasi_%"],
            name="Pencapaian",
            line=dict(color="#C44D4D", width=4),
            mode="lines+markers+text",
            text=df_c3["Prestasi_%"].round(0).astype(int).astype(str) + "%",
            textposition="top center"
        ))
        fig3.update_layout(
            height=700,
            title="CARTA 4: Prestasi Mengikut PTJ1",
            xaxis_title="PTJ1",
            yaxis_title="Peratusan (%)",
            yaxis=dict(range=[0, y_max]),
            legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="center", x=0.5),
            xaxis_tickangle=-45,
            template="plotly_white"
        )
        st.plotly_chart(fig3, use_container_width=True)

    with st.expander("📋 SUMMARY KESELURUHAN - BOLEH DOWNLOAD EXCEL", expanded=False):
        summary = df_akhir.groupby(["PTJ1", "Kategori", "DESC", "Quarter"], as_index=False).agg({
            "BAJET 2025": "sum",
            "SASARAN Q1-25": "sum",
            "SEBENAR Q1-25": "sum"
        })
        summary["Prestasi_%"] = summary.apply(
            lambda row: hitung_prestasi(row["SEBENAR Q1-25"], row["SASARAN Q1-25"]),
            axis=1
        )
        summary = summary.round(2)
        st.dataframe(summary, use_container_width=True, hide_index=True)

        excel_file = to_excel(summary)
        st.download_button(
            "📥 Download Summary sebagai Excel",
            data=excel_file,
            file_name=f"Summary_CIDB_{'_'.join(pilih_quarter)}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

    st.caption(f"Quarter: {', '.join(pilih_quarter)} • Dashboard CIDB JPKA")

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
    legend_col = "LEGEND"

    if nama_col not in df_geran_work.columns:
        st.error("Column NAMA tidak dijumpai dalam worksheet DATA.")
        st.write("Column yang ada:", df_geran_work.columns.tolist())
        st.stop()

    if legend_col not in df_geran_work.columns:
        st.error("Column LEGEND tidak dijumpai dalam worksheet DATA.")
        st.write("Column yang ada:", df_geran_work.columns.tolist())
        st.stop()

    amount_col = detect_amount_column(df_geran_work)
    if amount_col is not None:
        df_geran_work[amount_col] = clean_numeric_series(df_geran_work[amount_col])

        # Buang semua nilai negatif untuk keseluruhan Modul Geran.
        # Ini digunakan untuk KPI, slicer, carta dan jadual DATA GERAN.
        df_geran_work = df_geran_work[df_geran_work[amount_col] >= 0].copy()

    df_geran_tapis = df_geran_work.copy()

    with st.sidebar:
        st.markdown("### 🔎 PENAPIS GERAN")

        senarai_nama = unique_sorted(df_geran_tapis[nama_col])
        pilih_nama = st.multiselect(
            "Pilih NAMA",
            senarai_nama,
            default=senarai_nama,
            key="geran_slicer_nama"
        )
        df_geran_tapis = df_geran_tapis[df_geran_tapis[nama_col].astype(str).isin(pilih_nama)]

        senarai_legend = unique_sorted(df_geran_tapis[legend_col])
        pilih_legend = st.multiselect(
            "Pilih LEGEND",
            senarai_legend,
            default=senarai_legend,
            key="geran_slicer_legend"
        )
        df_geran_tapis = df_geran_tapis[df_geran_tapis[legend_col].astype(str).isin(pilih_legend)]

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

    col_g1, col_g2, col_g3 = st.columns(3)

    with col_g1:
        st.metric("Jumlah Pemberian", format_nilai(jumlah_pemberian))

    with col_g2:
        st.metric("Jumlah Perbelanjaan", format_nilai(jumlah_perbelanjaan))

    with col_g3:
        st.metric("Jumlah Bayar Balik", format_nilai(jumlah_bayar_balik))

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
            index=nama_col,
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
        x=nama_col,
        y=["PEMBERIAN", "PERBELANJAAN", "BYR BALIK"],
        barmode="group",
        title="NAMA vs PEMBERIAN, PERBELANJAAN dan BYR BALIK",
        labels={
            "value": "Jumlah Amount in local currency",
            "variable": "LEGEND",
            nama_col: "NAMA"
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
        trace.textposition = "outside"

        if trace.name in warna_trace:
            trace.marker.color = warna_trace[trace.name]

    fig_geran_nama.update_layout(
        xaxis_tickangle=-45,
        yaxis_title="Jumlah Amount in local currency",
        legend_title_text="LEGEND",
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
        x=nama_col,
        y="BAKI GERAN",
        text=df_baki_geran["BAKI GERAN"].apply(format_nilai),
        title="Baki Geran = Pemberian - Perbelanjaan - Bayar Balik",
        color_discrete_sequence=["#bde0fe"]
    )

    fig_baki.update_traces(
        textposition="outside"
    )

    fig_baki.update_layout(
        height=600,
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
    # DATA CARTA GERAN + DOWNLOAD EXCEL
    # =======================
    df_data_carta_geran = df_nama_legend[[nama_col, "PEMBERIAN", "PERBELANJAAN", "BYR BALIK", "Jumlah"]].copy()

    df_data_carta_geran["BAKI GERAN"] = (
        df_data_carta_geran["PEMBERIAN"]
        - df_data_carta_geran["PERBELANJAAN"]
        - df_data_carta_geran["BYR BALIK"]
    )

    with st.expander("📄 DATA CARTA GERAN", expanded=False):
        st.dataframe(
            df_data_carta_geran,
            use_container_width=True,
            hide_index=True
        )

        excel_data_carta = to_excel(
            df_data_carta_geran,
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
    st.info("Modul P&L belum dibangunkan.")

elif menu == "4. Balance Sheet":
    st.info("Modul Balance Sheet belum dibangunkan.")

elif menu == "5. Cash Flow":
    st.info("Modul Cash Flow belum dibangunkan.")
