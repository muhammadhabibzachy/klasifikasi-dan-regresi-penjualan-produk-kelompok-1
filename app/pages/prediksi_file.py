import streamlit as st
import pandas as pd
import numpy as np
import io
from datetime import date, timedelta
from utils.predictor import predict_sales
from prediksi import add_to_history

REQUIRED_COLS = {"store_nbr", "date", "oil_price", "onpromotion"}

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

def _validate(df: pd.DataFrame):
    """Validasi kolom dan tipe data. Return (ok, pesan_error)."""
    missing = REQUIRED_COLS - set(df.columns)
    if missing:
        return False, f"Kolom tidak lengkap. Kolom yang kurang: **{', '.join(missing)}**"

    try:
        df["store_nbr"] = pd.to_numeric(df["store_nbr"], errors="raise").astype(int)
        if not df["store_nbr"].between(1, 54).all():
            return False, "Nilai `store_nbr` harus antara 1–54."
    except Exception:
        return False, "Kolom `store_nbr` harus berisi angka bulat (1–54)."

    try:
        df["date"] = pd.to_datetime(df["date"]).dt.date
    except Exception:
        return False, "Kolom `date` tidak dapat diparse. Gunakan format YYYY-MM-DD."

    try:
        df["oil_price"] = pd.to_numeric(df["oil_price"], errors="raise").astype(float)
        if (df["oil_price"] < 0).any():
            return False, "Nilai `oil_price` tidak boleh negatif."
    except Exception:
        return False, "Kolom `oil_price` harus berisi angka desimal (contoh: 75.5)."

    valid_promo = {"ya", "tidak", "yes", "no", "1", "0", "true", "false"}
    sample = df["onpromotion"].astype(str).str.lower().unique()
    if not all(v in valid_promo for v in sample):
        return False, f"Kolom `onpromotion` hanya boleh berisi: Ya/Tidak/1/0. Ditemukan: {list(sample)}"

    return True, ""


def _normalize_promo(val) -> str:
    """Normalisasi berbagai format promo ke 'Ya' atau 'Tidak'."""
    v = str(val).strip().lower()
    return "Ya" if v in {"ya", "yes", "1", "true"} else "Tidak"


def _template_csv() -> bytes:
    df = pd.DataFrame({
        "store_nbr":    [1, 2, 3],
        "date":         ["2024-01-15", "2024-01-16", "2024-01-17"],
        "oil_price":    [75.5, 76.0, 74.8],
        "onpromotion":  ["Ya", "Tidak", "Ya"],
    })
    return df.to_csv(index=False).encode("utf-8")


def show():
    st.markdown("""
    <div class="page-header">
        <h1>Prediksi Dengan Upload File</h1>
        <p class="subtitle">Upload file CSV atau Excel — prediksi dijalankan untuk setiap baris data</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Panduan format (HTML native — hindari st.expander agar tidak ada bug icon) ──
    st.markdown("""
    <details open style="
        background: rgba(255,255,255,0.12);
        border: 1px solid rgba(255,255,255,0.22);
        border-radius: 10px;
        padding: 0;
        margin-bottom: 0.5rem;
    ">
        <summary style="
            cursor: pointer;
            padding: 0.75rem 1rem;
            font-weight: 600;
            font-size: 1rem;
            color: #ffffff;
            list-style: none;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            border-radius: 10px;
            user-select: none;
        ">
            ▶ Panduan Format File
        </summary>
        <div style="padding: 0 1rem 1rem 1rem; color: #e2eeff;">
            <p style="margin-bottom:0.75rem">
                File harus memiliki <strong style="color:#ffffff">tepat 4 kolom</strong> 
                berikut (nama kolom harus sama persis):
            </p>
            <table style="width:100%;border-collapse:collapse;font-size:0.88rem">
                <thead>
                    <tr style="background:rgba(255,255,255,0.12)">
                        <th style="padding:8px 12px;text-align:left;color:#ffffff;font-weight:700;border-bottom:1px solid rgba(255,255,255,0.15)">Kolom</th>
                        <th style="padding:8px 12px;text-align:left;color:#ffffff;font-weight:700;border-bottom:1px solid rgba(255,255,255,0.15)">Tipe</th>
                        <th style="padding:8px 12px;text-align:left;color:#ffffff;font-weight:700;border-bottom:1px solid rgba(255,255,255,0.15)">Keterangan</th>
                    </tr>
                </thead>
                <tbody>
                    <tr style="border-bottom:1px solid rgba(255,255,255,0.08)">
                        <td style="padding:8px 12px"><code style="background:rgba(255,255,255,0.15);color:#c4b5fd;padding:2px 6px;border-radius:4px">store_nbr</code></td>
                        <td style="padding:8px 12px;color:#94a3b8">Integer</td>
                        <td style="padding:8px 12px">Nomor toko, nilai 1–54</td>
                    </tr>
                    <tr style="border-bottom:1px solid rgba(255,255,255,0.08);background:rgba(255,255,255,0.04)">
                        <td style="padding:8px 12px"><code style="background:rgba(255,255,255,0.15);color:#c4b5fd;padding:2px 6px;border-radius:4px">date</code></td>
                        <td style="padding:8px 12px;color:#94a3b8">Date</td>
                        <td style="padding:8px 12px">Format <code style="background:rgba(255,255,255,0.15);color:#6ee7b7;padding:2px 5px;border-radius:4px">YYYY-MM-DD</code> (contoh: 2024-01-15)</td>
                    </tr>
                    <tr style="border-bottom:1px solid rgba(255,255,255,0.08)">
                        <td style="padding:8px 12px"><code style="background:rgba(255,255,255,0.15);color:#c4b5fd;padding:2px 6px;border-radius:4px">oil_price</code></td>
                        <td style="padding:8px 12px;color:#94a3b8">Float</td>
                        <td style="padding:8px 12px">Harga minyak USD/barrel (contoh: 75.5)</td>
                    </tr>
                    <tr style="background:rgba(255,255,255,0.04)">
                        <td style="padding:8px 12px"><code style="background:rgba(255,255,255,0.15);color:#c4b5fd;padding:2px 6px;border-radius:4px">onpromotion</code></td>
                        <td style="padding:8px 12px;color:#94a3b8">String</td>
                        <td style="padding:8px 12px">Isi dengan <code style="background:rgba(255,255,255,0.15);color:#6ee7b7;padding:2px 5px;border-radius:4px">Ya</code> atau <code style="background:rgba(255,255,255,0.15);color:#6ee7b7;padding:2px 5px;border-radius:4px">Tidak</code> (boleh juga <code style="background:rgba(255,255,255,0.15);color:#6ee7b7;padding:2px 5px;border-radius:4px">1</code>/<code style="background:rgba(255,255,255,0.15);color:#6ee7b7;padding:2px 5px;border-radius:4px">0</code>)</td>
                    </tr>
                </tbody>
            </table>
            <p style="margin-top:0.75rem;color:rgba(255,255,255,0.6);font-size:0.85rem">
                Format file yang didukung: 
                <strong style="color:#ffffff">CSV</strong> 
                <code style="background:rgba(255,255,255,0.15);color:#7dd3fc;padding:2px 5px;border-radius:4px">.csv</code> 
                dan 
                <strong style="color:#ffffff">Excel</strong> 
                <code style="background:rgba(255,255,255,0.15);color:#7dd3fc;padding:2px 5px;border-radius:4px">.xlsx</code>
            </p>
        </div>
    </details>
    """, unsafe_allow_html=True)

    st.markdown("---")

    uploaded = st.file_uploader(
        "Upload file CSV atau Excel",
        type=["csv", "xlsx"],
        help="Pastikan file memiliki 4 kolom: store_nbr, date, oil_price, onpromotion"
    )

    if uploaded is None:
        st.info("Silakan upload file.")
        return

    try:
        if uploaded.name.endswith(".xlsx"):
            df = pd.read_excel(uploaded)
        else:
            df = pd.read_csv(uploaded)
    except Exception as e:
        st.error(f"Gagal membaca file: {e}")
        return

    ok, err_msg = _validate(df.copy())
    if not ok:
        st.error(f"File tidak valid: {err_msg}")
        st.markdown("""
        <div style="background:#1e1e2e;border:1px solid #ef4444;border-radius:12px;padding:1rem;margin-top:1rem">
            <p style="color:#94a3b8;font-size:0.9rem;margin:0">
            Pastikan nama kolom <strong style="color:#38bdf8">store_nbr</strong>, 
            <strong style="color:#34d399">date</strong>, 
            <strong style="color:#fb923c">oil_price</strong>, 
            <strong style="color:#818cf8">onpromotion</strong> sudah benar dan tipe datanya sesuai.
            </p>
        </div>
        """, unsafe_allow_html=True)
        return

    df["date"]        = pd.to_datetime(df["date"]).dt.date
    df["store_nbr"]   = df["store_nbr"].astype(int)
    df["oil_price"]   = df["oil_price"].astype(float)
    df["onpromotion"] = df["onpromotion"].apply(_normalize_promo)

    st.success(f"File valid — {len(df)} baris data ditemukan.")

    if "show_preview" not in st.session_state:
        st.session_state.show_preview = False
    if st.button(
        "Sembunyikan Preview" if st.session_state.show_preview else "Tampilkan Preview Data",
        key="toggle_preview"
    ):
        st.session_state.show_preview = not st.session_state.show_preview
    if st.session_state.show_preview:
        st.dataframe(df, use_container_width=True, hide_index=True)

    st.markdown("---")

    btn = st.button("Jalankan Prediksi Semua Baris", type="primary", use_container_width=True)

    if not btn:
        return

    results = []
    progress = st.progress(0, text="Memproses prediksi...")
    total_rows = len(df)

    for i, row in df.iterrows():
        row_results = []
        for fam in FAMILIES:
            try:
                r = predict_sales(
                    int(row["store_nbr"]),
                    fam,
                    row["date"],
                    row["onpromotion"],
                )
                if r["terjual"]:
                    row_results.append(r["estimasi_unit"])
            except Exception:
                continue

        total_est = sum(row_results)
        terjual   = len(row_results)

        results.append({
            "store_nbr":        int(row["store_nbr"]),
            "date":             str(row["date"]),
            "oil_price":        row["oil_price"],
            "onpromotion":      row["onpromotion"],
            "kategori_terjual": terjual,
            "total_estimasi":   round(total_est, 2),
            "status":           "Terjual" if terjual > 0 else "Tidak Terjual",
        })

        progress.progress((i + 1) / total_rows,
                          text=f"Memproses baris {i + 1} dari {total_rows}...")

    progress.empty()

    df_result = pd.DataFrame(results)

    # ── Simpan ke riwayat ─────────────────────────────────────────────────────
    add_to_history(
        mode="Upload File",
        inputs={
            "filename":        uploaded.name,
            "jumlah_baris":    len(df),
            "toko":            f"{df['store_nbr'].nunique()} toko unik",
            "rentang_tanggal": f"{df['date'].min()} s/d {df['date'].max()}",
        },
        result=df_result,
    )
    # ─────────────────────────────────────────────────────────────────────────

    st.markdown("---")
    st.markdown("### Hasil Prediksi")

    total_baris     = len(df_result)
    baris_terjual   = (df_result["status"] == "Terjual").sum()
    total_unit      = df_result["total_estimasi"].sum()
    rata_unit       = df_result[df_result["total_estimasi"] > 0]["total_estimasi"].mean()

    c1, c2, c3, c4 = st.columns(4)
    cards = [
        (c1, "", "Total Baris",     f"{total_baris} baris",         "#38bdf8"),
        (c2, "", "Baris Terjual",   f"{baris_terjual} baris",       "#34d399"),
        (c3, "", "Total Estimasi",  f"{total_unit:,.2f} unit",      "#818cf8"),
        (c4, "", "Rata-rata/Baris", f"{rata_unit:,.2f} unit",       "#fb923c"),
    ]
    for col, icon, label, value, color in cards:
        with col:
            st.markdown(f"""
            <div style='background:rgba(255,255,255,0.12);border:1px solid rgba(255,255,255,0.22);border-top:3px solid {color};border-radius:12px;
                        padding:1rem;text-align:center;margin-bottom:0.5rem'>
                <div style='font-size:1.8rem'>{icon}</div>
                <div style='color:rgba(255,255,255,0.65);font-size:0.72rem;
                            letter-spacing:0.08em;margin-top:4px'>{label}</div>
                <div style='color:{color};font-weight:700;font-size:0.95rem;
                            margin-top:4px'>{value}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    tab1, tab2 = st.tabs(["Hasil", "Detail"])

    with tab1:
        import plotly.graph_objects as go

        LAYOUT_BASE = dict(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#94a3b8"),
            margin=dict(l=20, r=20, t=40, b=20),
        )

        st.markdown("### Estimasi Total per Baris Data")
        fig = go.Figure(go.Bar(
            x=[f"Baris {i+1}" for i in range(len(df_result))],
            y=df_result["total_estimasi"],
            marker=dict(
                color=df_result["total_estimasi"],
                colorscale=[[0, "#1e3a5f"], [1, "#38bdf8"]],
            ),
            text=[f"{v:,.1f}" for v in df_result["total_estimasi"]],
            textposition="outside",
            textfont=dict(color="#e2e8f0", size=10),
            hovertemplate="<b>%{x}</b><br>%{y:,.2f} unit<extra></extra>",
        ))
        fig.update_layout(
            **LAYOUT_BASE,
            height=380,
            xaxis=dict(gridcolor="#1e293b"),
            yaxis=dict(gridcolor="#1e293b", title="Total Estimasi Unit"),
        )
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.markdown("### Detail Semua Baris")
        st.dataframe(df_result, use_container_width=True, hide_index=True)

        csv_out = df_result.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download Hasil Prediksi (CSV)",
            data=csv_out,
            file_name="hasil_prediksi.csv",
            mime="text/csv",
        )