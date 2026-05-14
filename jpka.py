import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO

# =======================
# TETAPAN
# =======================
st.set_page_config(page_title="PRESTASI PERBELANJAAN DAN HASIL CIDB", layout="wide")

hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .block-container {padding: 1rem 2rem;}
    .card { background-color: #f8f9fa; border-left: 5px solid #2c3e50; padding: 1.3rem; border-radius: 10px; box-shadow: 3px 3px 12px rgba(0,0,0,0.08); text-align:center; }
    .metric-row { display: flex; justify-content: space-between; margin: 8px 0; font-size: 14px; }
    .metric-label { color: #555; font-weight: 500; }
    .metric-value { font-weight: bold; }
    .traffic-circle {
        width: 95px; height: 95px; border-radius: 50%; display: flex; align-items: center; justify-content: center;
        font-size: 32px; font-weight: bold; color: white; margin: 8px auto 6px; box-shadow: 0 6px 12px rgba(0,0,0,0.3);
        cursor: pointer;
    }
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.markdown("""
    <h1 style='text-align:center; font-weight:bold; font-size:28px; color:#2c3e50;'>
        📊 PRESTASI PERBELANJAAN DAN HASIL CIDB
    </h1>
""", unsafe_allow_html=True)

# =======================
# FUNGSI
# =======================
def format_nilai(nilai):
    nilai = float(nilai)
    if nilai >= 1_000_000:
        return f"RM {nilai/1_000_000:.1f} Juta"
    elif nilai >= 1_000:
        return f"RM {nilai/1_000:.1f} Ribu"
    else:
        return f"RM {nilai:.0f}"

def hitung_prestasi(sebenar, sasaran):
    if sasaran == 0: return 0.0
    return (sebenar / sasaran) * 100

def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Summary')
    output.seek(0)
    return output

# =======================
# LOAD DATA
# =======================
@st.cache_data
def load_data():
    df_dict = {}
    files = {
        "03-2025": "JPKA_ANALISA PK CIDB 03-2025.xlsx",
        "06-2025": "JPKA_ANALISA PK CIDB 06-2025.xlsx",
        "09-2025": "JPKA_ANALISA PK CIDB 09-2025.xlsx",
        "12-2025": "JPKA_ANALISA PK CIDB 12-2025.xlsx"
    }
    for q, filename in files.items():
        try:
            df = pd.read_excel(filename, sheet_name="All2")
            df.columns = df.columns.str.strip()
            if "KOD" in df.columns and "KOD1" not in df.columns:
                df = df.rename(columns={"KOD": "KOD1"})
            df["Sumber"] = q
            df["Quarter"] = q
            df["Tahun"] = 2025
            df_dict[q] = df
        except Exception as e:
            st.error(f"❌ Gagal load {q}: {e}")
    return df_dict

df_dict = load_data()
if not df_dict:
    st.stop()

# =======================
# SIDEBAR
# =======================
with st.sidebar:
    st.markdown("### 🔎 PILIHAN PENAPIS")
    pilih_quarter = st.multiselect("Pilih Quarter",
                                   ["03-2025", "06-2025", "09-2025", "12-2025"],
                                   default=["12-2025"])
    
    dfs = [df_dict[q] for q in pilih_quarter if q in df_dict]
    df_tapis = pd.concat(dfs, ignore_index=True)
    df_tapis.columns = df_tapis.columns.str.strip()

    senarai_ptj = sorted(df_tapis["PTJ"].dropna().astype(str).unique().tolist())
    pilih_ptj = st.multiselect("Pilih PTJ", senarai_ptj, default=senarai_ptj)
    df_tapis = df_tapis[df_tapis["PTJ"].isin(pilih_ptj)]

    senarai_ptj1 = sorted(df_tapis["PTJ1"].dropna().astype(str).unique().tolist())
    pilih_ptj1 = st.multiselect("Pilih PTJ1", senarai_ptj1, default=senarai_ptj1)
    df_tapis_ptj1 = df_tapis[df_tapis["PTJ1"].isin(pilih_ptj1)]

    senarai_kategori = sorted(df_tapis_ptj1["Kategori"].dropna().astype(str).unique().tolist())
    pilih_kategori = st.multiselect("Pilih Kategori", senarai_kategori, default=senarai_kategori)
    df_kat = df_tapis_ptj1[df_tapis_ptj1["Kategori"].isin(pilih_kategori)]

    senarai_desc = sorted(df_kat["DESC"].dropna().astype(str).unique().tolist())
    pilih_desc = st.multiselect("Pilih DESC", senarai_desc, default=senarai_desc)
    df_desc = df_kat[df_kat["DESC"].isin(pilih_desc)]

    senarai_kod1 = sorted(df_desc["KOD1"].dropna().astype(str).unique().tolist())
    pilih_kod1 = st.multiselect("Pilih KOD1", senarai_kod1, default=senarai_kod1)

# =======================
# DATA AKHIR
# =======================
df_akhir = df_desc[df_desc["KOD1"].isin(pilih_kod1)].copy()
df_akhir["Jenis_Belanja"] = df_akhir["Kategori"].apply(lambda x:
    "Mengurus" if "Mengurus" in str(x) else "Program" if "Program" in str(x) else
    "Modal" if "Modal" in str(x) else "Hasil" if "Hasil" in str(x) else "Lain-lain")

# TRAFFIC LIGHT
# =======================
st.markdown("### 🚦 STATUS PRESTASI PTJ1")
if not df_akhir.empty:
    df_akhir["Prestasi_%"] = df_akhir.apply(lambda row: hitung_prestasi(row["SEBENAR Q1-25"], row["SASARAN Q1-25"]), axis=1)
    
    df_group = df_akhir.groupby("PTJ1").agg({
        "SASARAN Q1-25": "sum", "SEBENAR Q1-25": "sum"
    }).reset_index()
    
    df_group["Prestasi_%"] = df_group.apply(lambda row: hitung_prestasi(row["SEBENAR Q1-25"], row["SASARAN Q1-25"]), axis=1)
    
    hebat = len(df_group[df_group["Prestasi_%"] > 95])
    bagus = len(df_group[(df_group["Prestasi_%"] >= 85) & (df_group["Prestasi_%"] <= 94.99)])
    usaha = len(df_group[df_group["Prestasi_%"] < 85])
    total = len(df_group)
    
    total_sebenar = df_akhir["SEBENAR Q1-25"].sum()
    total_sasaran = df_akhir["SASARAN Q1-25"].sum()
    pencapaian = hitung_prestasi(total_sebenar, total_sasaran)
    pencapaian_int = round(pencapaian)

    col1, col2, col3, col4 = st.columns([1,1,1,1.2])
    
    if 'show_drill' not in st.session_state:
        st.session_state.show_drill = None
        st.session_state.drill_title = ""

    with col1:
        if st.button("🟢", key="hebat_btn"):
            st.session_state.show_drill = "hebat"
            st.session_state.drill_title = "Senarai PTJ1 Hebat (> 95%)"
        st.markdown(f"""
        <div style="text-align:center">
            <strong style="color:black; font-size:15px;">> 95%</strong><br>
            <div class="traffic-circle" style="background-color:#27ae60;">{hebat}</div>
            <h4 style="color:#27ae60;">Hebat!</h4>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        if st.button("🟡", key="bagus_btn"):
            st.session_state.show_drill = "bagus"
            st.session_state.drill_title = "Senarai PTJ1 Bagus (85% - 94%)"
        st.markdown(f"""
        <div style="text-align:center">
            <strong style="color:black; font-size:15px;">85% - 94%</strong><br>
            <div class="traffic-circle" style="background-color:#f1c40f; color:#2c3e50;">{bagus}</div>
            <h4 style="color:#f1c40f;">Bagus!</h4>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        if st.button("🔴", key="usaha_btn"):
            st.session_state.show_drill = "usaha"
            st.session_state.drill_title = "Senarai PTJ1 Usaha Lagi (< 85%)"
        st.markdown(f"""
        <div style="text-align:center">
            <strong style="color:black; font-size:15px;">< 85%</strong><br>
            <div class="traffic-circle" style="background-color:#e74c3c;">{usaha}</div>
            <h4 style="color:#e74c3c;">Usaha lagi!</h4>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div style="text-align:center; padding-top:15px;">
            <h1 style="margin:0;color:#2c3e50;font-size:2.2em;">{total}</h1>
            <h5 style="margin:0;color:#2c3e50;">Jumlah PTJ1</h5>
            <hr style="margin:8px 0;">
            <p style="margin:3px 0;"><strong>SASARAN</strong> 100%</p>
            <p style="margin:3px 0;"><strong>PRESTASI</strong> {pencapaian_int}%</p>
            <h3 style="color:#27ae60;">PENCAPAIAN {pencapaian_int}%</h3>
        </div>
        """, unsafe_allow_html=True)

    if st.session_state.show_drill:
        st.subheader(st.session_state.drill_title)
        if st.session_state.show_drill == "hebat":
            df_show = df_group[df_group["Prestasi_%"] > 95].sort_values("Prestasi_%", ascending=False)
        elif st.session_state.show_drill == "bagus":
            df_show = df_group[(df_group["Prestasi_%"] >= 85) & (df_group["Prestasi_%"] <= 94.99)].sort_values("Prestasi_%", ascending=False)
        else:
            df_show = df_group[df_group["Prestasi_%"] < 85].sort_values("Prestasi_%", ascending=False)
        
        if not df_show.empty:
            st.dataframe(df_show[["PTJ1", "Prestasi_%"]].round(2), use_container_width=True, hide_index=True)
        if st.button("❌ Tutup Senarai", type="primary"):
            st.session_state.show_drill = None
            st.rerun()

# =======================
# DRILL DOWN SECTIONS
# =======================

# 1. Ringkasan Keseluruhan (Cards)
with st.expander("📋 RINGKASAN KESELURUHAN", expanded=False):
    if not df_akhir.empty:
        for q in pilih_quarter:
            df_q = df_akhir[df_akhir["Quarter"] == q]
            with st.expander(f"Quarter {q}", expanded=True):
                col_k1, col_k2, col_k3, col_k4 = st.columns(4)
                for jenis, tajuk, col in [("Mengurus","BELANJA MENGURUS",col_k1),
                                         ("Program","BELANJA PROGRAM",col_k2),
                                         ("Modal","BELANJA MODAL",col_k3),
                                         ("Hasil","HASIL",col_k4)]:
                    b = df_q[df_q["Jenis_Belanja"]==jenis]["BAJET 2025"].sum()
                    s = df_q[df_q["Jenis_Belanja"]==jenis]["SASARAN Q1-25"].sum()
                    se = df_q[df_q["Jenis_Belanja"]==jenis]["SEBENAR Q1-25"].sum()
                    with col:
                        st.markdown(f"""<div class="card"><h4>{tajuk}</h4>
                        <div class="metric-row"><span class="metric-label">Bajet</span><span style="color:#2C7DA6;">{format_nilai(b)}</span></div>
                        <div class="metric-row"><span class="metric-label">Sasaran</span><span style="color:#E08E4E;">{format_nilai(s)}</span></div>
                        <div class="metric-row"><span class="metric-label">Sebenar</span><span style="color:#2E8B6D;">{format_nilai(se)}</span></div></div>""",
                        unsafe_allow_html=True)
    else:
        st.info("Tiada data")


# =======================
# CARTA 1: PERBANDINGAN MENGIKUT KATEGORI
# =======================
with st.expander("📊 CARTA 1: PERBANDINGAN MENGIKUT KATEGORI", expanded=False):
    if not df_akhir.empty:
        df_akhir["BAJET_JT"] = df_akhir["BAJET 2025"] / 1_000_000
        df_akhir["SASARAN_JT"] = df_akhir["SASARAN Q1-25"] / 1_000_000
        df_akhir["SEBENAR_JT"] = df_akhir["SEBENAR Q1-25"] / 1_000_000

        if len(pilih_quarter) > 1:
            cols = st.columns(len(pilih_quarter))
            for i, q in enumerate(pilih_quarter):
                df_q = df_akhir[df_akhir["Quarter"] == q]
                df_c1 = df_q.groupby("Kategori", as_index=False).agg({"BAJET_JT":"sum", "SASARAN_JT":"sum", "SEBENAR_JT":"sum"})
                with cols[i]:
                    st.markdown(f"**Quarter {q}**")
                    fig = px.bar(df_c1, x="Kategori", y=["BAJET_JT", "SASARAN_JT", "SEBENAR_JT"],
                                 barmode="group", height=520,
                                 color_discrete_sequence=['#2C7DA6', '#E08E4E', '#2E8B6D'])
                    for trace in fig.data:
                        trace.text = [format_nilai(x * 1_000_000) for x in trace.y]
                        trace.textposition = 'outside'
                    st.plotly_chart(fig, use_container_width=True)
        else:
            df_c1 = df_akhir.groupby("Kategori", as_index=False).agg({"BAJET_JT":"sum", "SASARAN_JT":"sum", "SEBENAR_JT":"sum"})
            fig1 = px.bar(df_c1, x="Kategori", y=["BAJET_JT", "SASARAN_JT", "SEBENAR_JT"],
                          barmode="group", height=550,
                          color_discrete_sequence=['#2C7DA6', '#E08E4E', '#2E8B6D'])
            for trace in fig1.data:
                trace.text = [format_nilai(x * 1_000_000) for x in trace.y]
                trace.textposition = 'outside'
            st.plotly_chart(fig1, use_container_width=True)

# =======================
# CARTA 2: JUMLAH SEBENAR MENGIKUT QUARTER (BARU)
# =======================
with st.expander("📊 CARTA 2: JUMLAH SEBENAR MENGIKUT QUARTER", expanded=False):
    if not df_akhir.empty:
        df_total = df_akhir.groupby("Quarter")["SEBENAR Q1-25"].sum().reset_index()
        df_total = df_total.sort_values("Quarter")
        
        fig_total = px.bar(df_total, x="Quarter", y="SEBENAR Q1-25",
                           title="Jumlah Sebenar Mengikut Quarter",
                           labels={"SEBENAR Q1-25": "Jumlah Sebenar (RM)"},
                           text=df_total["SEBENAR Q1-25"].apply(format_nilai))
        
        fig_total.update_traces(textposition='outside', marker_color='#2E8B6D')
        fig_total.update_layout(height=600, yaxis_title="Jumlah Sebenar (RM)")
        
        st.plotly_chart(fig_total, use_container_width=True)

# =======================
# CARTA 3: PRESTASI MENGIKUT DESC
# =======================
with st.expander("📊 CARTA 3: PRESTASI MENGIKUT DESC", expanded=False):
    if not df_akhir.empty:
        if len(pilih_quarter) > 1:
            cols = st.columns(len(pilih_quarter))
            for i, q in enumerate(pilih_quarter):
                df_q = df_akhir[df_akhir["Quarter"] == q]
                df_c2 = df_q.groupby("DESC", as_index=False).agg({"SASARAN Q1-25":"sum", "SEBENAR Q1-25":"sum"}).sort_values("SEBENAR Q1-25", ascending=False).head(20)
                with cols[i]:
                    st.markdown(f"**Quarter {q}**")
                    fig2 = px.bar(df_c2, y="DESC", x=["SASARAN Q1-25", "SEBENAR Q1-25"],
                                  orientation='h', barmode="group", height=700,
                                  color_discrete_sequence=['#E08E4E', '#2E8B6D'])
                    for trace in fig2.data:
                        trace.text = [format_nilai(x) for x in trace.x]
                        trace.textposition = 'outside'
                    fig2.update_layout(yaxis=dict(categoryorder='array', categoryarray=df_c2["DESC"].tolist()))
                    st.plotly_chart(fig2, use_container_width=True)
        else:
            df_c2 = df_akhir.groupby("DESC", as_index=False).agg({"SASARAN Q1-25":"sum", "SEBENAR Q1-25":"sum"}).sort_values("SEBENAR Q1-25", ascending=False).head(20)
            fig2 = px.bar(df_c2, y="DESC", x=["SASARAN Q1-25", "SEBENAR Q1-25"],
                          orientation='h', barmode="group", height=700,
                          color_discrete_sequence=['#E08E4E', '#2E8B6D'])
            for trace in fig2.data:
                trace.text = [format_nilai(x) for x in trace.x]
                trace.textposition = 'outside'
            fig2.update_layout(yaxis=dict(categoryorder='array', categoryarray=df_c2["DESC"].tolist()))
            st.plotly_chart(fig2, use_container_width=True)

# =======================
# CARTA 4: PRESTASI MENGIKUT PTJ1
# =======================
with st.expander("📈 CARTA 4: PRESTASI MENGIKUT PTJ1", expanded=False):
    if not df_akhir.empty:
        df_c3 = df_akhir.groupby("PTJ1", as_index=False).agg({"SASARAN Q1-25": "sum", "SEBENAR Q1-25": "sum"})
        df_c3["Prestasi_%"] = df_c3.apply(lambda row: hitung_prestasi(row["SEBENAR Q1-25"], row["SASARAN Q1-25"]), axis=1)
        df_c3 = df_c3.sort_values(by="Prestasi_%", ascending=False).reset_index(drop=True)
        
        fig3 = go.Figure()
        fig3.add_trace(go.Bar(x=df_c3["PTJ1"], y=df_c3["Prestasi_%"], name="Prestasi",
                              marker_color="#2E8B6D", text=df_c3["Prestasi_%"].round(0).astype(int).astype(str) + "%", textposition="inside"))
        fig3.add_trace(go.Scatter(x=df_c3["PTJ1"], y=[100]*len(df_c3), name="Sasaran 100%",
                                  line=dict(color="#E08E4E", width=3, dash="dash"), mode="lines"))
        fig3.add_trace(go.Scatter(x=df_c3["PTJ1"], y=df_c3["Prestasi_%"], name="Pencapaian",
                                  line=dict(color="#C44D4D", width=4), mode="lines+markers+text",
                                  text=df_c3["Prestasi_%"].round(0).astype(int).astype(str) + "%",
                                  textposition="top center"))
        
        fig3.update_layout(height=700, title="CARTA 4: Prestasi Mengikut PTJ1",
                           xaxis_title="PTJ1", yaxis_title="Peratusan (%)", yaxis=dict(range=[0, 140]),
                           legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="center", x=0.5),
                           xaxis_tickangle=-45, template="plotly_white")
        st.plotly_chart(fig3, use_container_width=True)

# =======================
# SUMMARY
# =======================
with st.expander("📋 SUMMARY KESELURUHAN - BOLEH DOWNLOAD EXCEL", expanded=False):
    if not df_akhir.empty:
        summary = df_akhir.groupby(["PTJ1", "Kategori", "DESC", "Quarter"]).agg({
            "BAJET 2025": "sum", "SASARAN Q1-25": "sum", "SEBENAR Q1-25": "sum"
        }).reset_index()
        summary["Prestasi_%"] = summary.apply(lambda row: hitung_prestasi(row["SEBENAR Q1-25"], row["SASARAN Q1-25"]), axis=1)
        summary = summary.round(2)
        st.dataframe(summary, use_container_width=True, hide_index=True)
        
        excel_file = to_excel(summary)
        st.download_button("📥 Download Summary sebagai Excel", data=excel_file,
                           file_name=f"Summary_CIDB_{'_'.join(pilih_quarter)}.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                           use_container_width=True)

st.caption(f"Quarter: {', '.join(pilih_quarter)} • Dashboard CIDB JPKA")