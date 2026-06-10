import streamlit as st
import pandas as pd
import numpy as np
from datetime import date, timedelta
from prediksi import add_to_history

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.predictor import predict_sales

FAMILIES = [
    "AUTOMOTIVE", "CELEBRATION", "BREAD/BAKERY", "BOOKS", "BEVERAGES",
    "BEAUTY", "BABY CARE", "SEAFOOD", "SCHOOL AND OFFICE SUPPLIES",
    "PRODUCE", "PREPARED FOODS", "POULTRY", "PLAYERS AND ELECTRONICS",
    "PET SUPPLIES", "PERSONAL CARE", "MEATS", "MAGAZINES",
    "LIQUOR,WINE,BEER", "LINGERIE", "LAWN AND GARDEN", "LADIESWEAR",
    "HOME CARE", "HOME APPLIANCES", "CLEANING", "DAIRY", "DELI",
    "EGGS", "HOME AND KITCHEN II", "HOME AND KITCHEN I", "HARDWARE",
    "GROCERY II", "GROCERY I", "FROZEN FOODS",
]

# Bobot fitur (dari model — sesuaikan jika punya nilai aktual dari feature_importances_)
FEATURE_IMPORTANCE = {
    "oil_price":    0.312,
    "store_nbr":    0.278,
    "day_of_year":  0.187,
    "onpromotion":  0.143,
    "day_of_week":  0.080,
}

LAYOUT_BASE = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#ffffff"),
    margin=dict(l=20, r=20, t=40, b=20),
)

def show():
    st.markdown("""
    <div class="page-header">
        <h1>Prediksi Dengan Input Manual</h1>
        <p class="subtitle">Estimasi penjualan berdasarkan toko, tanggal, harga minyak, dan promo</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Form Input Prediksi")
    st.markdown("Isi parameter berikut untuk mendapatkan estimasi penjualan.")

    col1, col2 = st.columns(2)
    with col1:
        store_nbr  = st.number_input("Nomor Toko (1–54)", min_value=1, max_value=54, step=1)
        date_input = st.date_input(
            "Tanggal Prediksi (max 14 hari ke depan)",
            value=date.today(),
            min_value=date.today(),
            max_value=date.today() + timedelta(days=14),
        )
    with col2:
        oil_price = st.number_input(
            "Harga Minyak (USD/barrel)",
            min_value=0.0, max_value=300.0,
            value=75.0, step=0.5,
            help="Harga minyak mentah WTI. Rata-rata historis sekitar 50–90 USD."
        )
        onpromotion = st.radio("Apakah produk sedang Promo?", ["Tidak", "Ya"])

    st.markdown("---")
    btn = st.button("Jalankan Prediksi", type="primary", use_container_width=True)
    if not btn:
        return

    # ── Proses prediksi ───────────────────────────────────────────────────────
    with st.spinner("Memproses prediksi untuk semua kategori..."):
        hasil_list = []
        for fam in FAMILIES:
            try:
                r = predict_sales(store_nbr, fam, date_input, onpromotion)
                if r["terjual"]:
                    hasil_list.append({
                        "family":   fam,
                        "estimasi": round(r["estimasi_unit"], 2),
                        "log_pred": round(r["log_pred"], 6),
                    })
            except Exception:
                continue

    st.markdown("---")

    if not hasil_list:
        st.error("Tidak ada kategori produk yang terprediksi terjual pada parameter ini.")
        st.info("Saran: Coba ubah tanggal, nomor toko, atau aktifkan promo.")
        return

    df_result = pd.DataFrame(hasil_list).sort_values("estimasi", ascending=False)

    add_to_history(
        mode="Manual",
        inputs={
            "store_nbr":   store_nbr,
            "date":        str(date_input),
            "oil_price":   oil_price,
            "onpromotion": onpromotion,
        },
        result=df_result,
    )

    total_estimasi = df_result["estimasi"].sum()
    total_terjual  = len(df_result)
    tidak_terjual  = len(FAMILIES) - total_terjual

    st.success(f"**{total_terjual} kategori** terprediksi terjual — total estimasi **{total_estimasi:,.2f} unit**")

    # ── Kartu ringkasan ───────────────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    cards = [
        (c1, "", "Toko",          f"Store #{store_nbr}",         "#7dd3fc"),
        (c2, "",  "Harga Minyak",  f"${oil_price:.1f}/barrel",   "#fcd34d"),
        (c3, "", "Tanggal",        str(date_input),               "#6ee7b7"),
        (c4, "", "Total Estimasi", f"{total_estimasi:,.2f} unit", "#c4b5fd"),
    ]
    for col, icon, label, value, color in cards:
        with col:
            st.markdown(f"""
            <div style="background:rgba(255,255,255,0.15);border:1px solid rgba(255,255,255,0.30);
                        border-top:3px solid {color};border-radius:12px;padding:1rem;
                        text-align:center;margin-bottom:0.5rem;">
                <div style="font-size:1.6rem;margin-bottom:4px">{icon}</div>
                <div style="color:rgba(255,255,255,0.55);font-size:0.72rem;
                            text-transform:uppercase;letter-spacing:0.08em">{label}</div>
                <div style="color:{color};font-weight:700;font-size:0.95rem;
                            margin-top:6px;word-break:break-word">{value}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # ── Tabs ──────────────────────────────────────────────────────────────────
    tab1, tab2, tab3 = st.tabs(["Hasil", "Fitur Penting", "Detail"])

    # ── Tab 1: Bar chart top 10 ───────────────────────────────────────────────
    with tab1:
        import plotly.graph_objects as go

        st.markdown("### Top 10 Kategori Estimasi Tertinggi")
        df_top = df_result.head(10)

        fig_bar = go.Figure(go.Bar(
            x=df_top["estimasi"],
            y=df_top["family"],
            orientation="h",
            marker=dict(
                color=df_top["estimasi"],
                colorscale=[[0, "#ff9721"], [1, "#ffcf6f"]],
            ),
            text=[f"{v:,.2f}" for v in df_top["estimasi"]],
            textposition="outside",
            textfont=dict(color="#ffffff", size=10),
            hovertemplate="<b>%{y}</b><br>%{x:,.2f} unit<extra></extra>",
        ))
        fig_bar.update_layout(
            **LAYOUT_BASE,
            height=400,
            xaxis=dict(
                gridcolor="rgba(255,255,255,0.1)",
                title="Estimasi Unit",
                tickfont=dict(color="#ffffff"),
                title_font=dict(color="#ffffff"),
            ),
            yaxis=dict(
                gridcolor="rgba(255,255,255,0.1)",
                autorange="reversed",
                tickfont=dict(color="#ffffff"),
            ),
        )
        st.plotly_chart(fig_bar, use_container_width=True)

        # ── Pie chart terjual vs tidak ────────────────────────────────────────
        st.markdown("### Perbandingan Kategori Terjual vs Tidak")
        fig_pie = go.Figure(go.Pie(
            labels=["Terjual", "Tidak Terjual"],
            values=[total_terjual, tidak_terjual],
            hole=0.45,
            marker=dict(colors=["#6ee7b7", "#475569"]),
            textfont=dict(color="#ffffff", size=13),
            hovertemplate="<b>%{label}</b><br>%{value} kategori (%{percent})<extra></extra>",
        ))
        fig_pie.update_layout(
            **LAYOUT_BASE,
            height=320,
            legend=dict(
                font=dict(color="#ffffff"),
                bgcolor="rgba(0,0,0,0)",
            ),
            annotations=[dict(
                text=f"<b>{total_terjual}</b><br>terjual",
                x=0.5, y=0.5,
                font=dict(size=14, color="#ffffff"),
                showarrow=False,
            )],
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    # ── Tab 2: Feature importance ─────────────────────────────────────────────
    with tab2:
        import plotly.graph_objects as go

        st.markdown("### Fitur Paling Berpengaruh dalam Prediksi")
        st.markdown(
            "<div style='color:rgba(255,255,255,0.6);font-size:0.85rem;margin-bottom:1rem'>"
            "Berdasarkan bobot fitur model (feature importance). "
            "Semakin panjang bar, semakin besar pengaruh fitur terhadap hasil prediksi."
            "</div>", unsafe_allow_html=True
        )

        fi_df = pd.DataFrame(
            list(FEATURE_IMPORTANCE.items()),
            columns=["Fitur", "Importance"]
        ).sort_values("Importance", ascending=True)

        # Highlight fitur yang diinput user
        user_features = {
            "oil_price":   oil_price,
            "store_nbr":   store_nbr,
            "onpromotion": onpromotion,
            "day_of_year": date_input.timetuple().tm_yday,
            "day_of_week": date_input.weekday(),
        }

        bar_colors = []
        for f in fi_df["Fitur"]:
            if f in ["oil_price", "store_nbr", "onpromotion"]:
                bar_colors.append("#7dd3fc")   # biru — diinput user
            else:
                bar_colors.append("#c4b5fd")   # ungu — derived dari tanggal

        fig_fi = go.Figure(go.Bar(
            x=fi_df["Importance"],
            y=fi_df["Fitur"],
            orientation="h",
            marker=dict(color=bar_colors),
            text=[f"{v*100:.1f}%" for v in fi_df["Importance"]],
            textposition="outside",
            textfont=dict(color="#ffffff", size=11),
            hovertemplate="<b>%{y}</b><br>Importance: %{x:.3f}<extra></extra>",
        ))
        fig_fi.update_layout(
            **LAYOUT_BASE,
            height=350,
            xaxis=dict(
                gridcolor="rgba(255,255,255,0.1)",
                title="Feature Importance",
                tickformat=".0%",
                tickfont=dict(color="#ffffff"),
                title_font=dict(color="#ffffff"),
            ),
            yaxis=dict(
                gridcolor="rgba(255,255,255,0.1)",
                tickfont=dict(color="#ffffff"),
            ),
        )
        st.plotly_chart(fig_fi, use_container_width=True)

        # Legenda warna
        st.markdown("""
        <div style="display:flex;gap:1.5rem;flex-wrap:wrap;margin-top:0.25rem">
            <div style="display:flex;align-items:center;gap:6px;font-size:0.8rem;color:rgba(255,255,255,0.7)">
                <div style="width:12px;height:12px;border-radius:3px;background:#7dd3fc"></div>
                Diinput langsung oleh pengguna
            </div>
            <div style="display:flex;align-items:center;gap:6px;font-size:0.8rem;color:rgba(255,255,255,0.7)">
                <div style="width:12px;height:12px;border-radius:3px;background:#c4b5fd"></div>
                Diturunkan dari tanggal
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Kartu nilai input aktual
        st.markdown("---")
        st.markdown("### Nilai Input yang Kamu Masukkan")
        fi_cols = st.columns(len(user_features))
        feat_meta = {
            "oil_price":   ("", "Oil Price",    f"${oil_price:.1f}",             "#fcd34d"),
            "store_nbr":   ("", "Store",        f"#{store_nbr}",                 "#7dd3fc"),
            "onpromotion": ("", "Promo",        onpromotion,                     "#6ee7b7"),
            "day_of_year": ("", "Hari ke-",     str(date_input.timetuple().tm_yday), "#c4b5fd"),
            "day_of_week": ("", "Hari (0=Sen)", str(date_input.weekday()),        "#f9a8d4"),
        }
        for i, (feat, (icon, label, val, color)) in enumerate(feat_meta.items()):
            with fi_cols[i]:
                importance_pct = f"{FEATURE_IMPORTANCE[feat]*100:.1f}%"
                st.markdown(f"""
                <div style="background:rgba(255,255,255,0.12);border:1px solid rgba(255,255,255,0.2);
                            border-top:3px solid {color};border-radius:10px;
                            padding:0.75rem;text-align:center">
                    <div style="font-size:1.3rem">{icon}</div>
                    <div style="color:rgba(255,255,255,0.5);font-size:0.65rem;
                                text-transform:uppercase;letter-spacing:0.06em;margin-top:2px">{label}</div>
                    <div style="color:{color};font-weight:700;font-size:0.9rem;margin-top:4px">{val}</div>
                    <div style="color:rgba(255,255,255,0.4);font-size:0.7rem;margin-top:2px">
                        bobot {importance_pct}
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # ── Tab 3: Detail tabel ───────────────────────────────────────────────────
    with tab3:
        st.markdown("### Semua Kategori yang Terprediksi Terjual")
        df_tampil = df_result.rename(columns={
            "family":   "Kategori Produk",
            "estimasi": "Estimasi Unit",
            "log_pred": "Log Pred",
        })
        st.dataframe(df_tampil, use_container_width=True, hide_index=True)
        st.caption(f"Total {total_terjual} dari {len(FAMILIES)} kategori terprediksi terjual.")

        st.markdown(" ")
        col_dl1, _ = st.columns(2)
        with col_dl1:
            csv_out = df_tampil.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="Download Hasil sebagai CSV",
                data=csv_out,
                file_name=f"hasil_prediksi_manual_{date.today()}.csv",
                mime="text/csv",
                use_container_width=True,
            )
