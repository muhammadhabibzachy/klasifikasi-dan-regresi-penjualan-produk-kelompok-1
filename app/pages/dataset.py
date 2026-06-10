import streamlit as st
import pandas as pd
import os
import glob

# ── Konstanta ──────────────────────────────────────────────────────────────────
DATASET_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "dataset"))


# ── Cache & Data Loading ───────────────────────────────────────────────────────
@st.cache_data
def get_total_rows(path: str) -> int:
    ext = os.path.splitext(path)[1].lower()
    if ext == ".xlsx":
        return len(pd.read_excel(path, usecols=[0]))
    elif ext == ".zip":
        return len(pd.read_csv(path, usecols=[0], compression="zip"))
    else:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return sum(1 for _ in f) - 1

@st.cache_data
def load_dataset(path: str, nrows=None) -> pd.DataFrame:
    ext = os.path.splitext(path)[1].lower()
    if ext == ".xlsx":
        return pd.read_excel(path, nrows=nrows)
    elif ext == ".zip":
        # pandas bisa baca CSV di dalam zip langsung
        return pd.read_csv(path, nrows=nrows, compression="zip")
    else:
        return pd.read_csv(path, nrows=nrows)


@st.cache_data
def load_all_files() -> dict:
    csvs  = sorted(glob.glob(os.path.join(DATASET_DIR, "*.csv")))
    xlsxs = sorted(glob.glob(os.path.join(DATASET_DIR, "*.xlsx")))
    zips  = sorted(glob.glob(os.path.join(DATASET_DIR, "*.zip")))   # ← tambah ini
    result = {}
    for path in csvs + xlsxs + zips:                                 # ← tambah zips
        fname = os.path.basename(path)
        result[fname] = load_dataset(path, nrows=None)
    return result

@st.cache_data
def merge_all(dfs: dict) -> pd.DataFrame:
    key_map = {
        ("stores.csv",          "train.zip"):           ["store_nbr"],
        ("train.zip",           "transactions.csv"):    ["date", "store_nbr"],
        ("train.zip",           "oil.csv"):             ["date"],
        ("train.zip",           "holidays_events.csv"): ["date"],
    }
    ORDER = ["train.zip", "stores.csv", "transactions.csv", "oil.csv", "holidays_events.csv"]

    base_name = next((n for n in ORDER if n in dfs), list(dfs.keys())[0])
    merged    = dfs[base_name].copy()
    merged.columns = [
        f"{base_name.replace('.csv','')}.{c}" if c not in ["date", "store_nbr", "family"] else c
        for c in merged.columns
    ]
    joined = {base_name}
    for name in ORDER:
        if name in joined or name not in dfs:
            continue
        pair = (name, base_name) if (name, base_name) in key_map else (base_name, name)
        keys = key_map.get(pair, key_map.get((name, base_name), None))
        if keys is None:
            keys = list(set(merged.columns) & set(dfs[name].columns))
        if not keys:
            continue
        right    = dfs[name].copy()
        non_key  = [c for c in right.columns if c not in keys]
        right    = right.rename(columns={c: f"{name.replace('.csv','')}.{c}" for c in non_key})
        merged   = merged.merge(right, on=keys, how="left")
        joined.add(name)
    return merged


# ── Helper: Metric Card ────────────────────────────────────────────────────────
def _metric_card(label: str, value: str, color: str = "#38bdf8") -> str:
    return f"""
    <div style="background:rgba(255,255,255,0.12);border:1px solid rgba(255,255,255,0.22);
                border-top:3px solid {color};border-radius:10px;padding:1.1rem 1.4rem;min-width:0;
                backdrop-filter:blur(6px);-webkit-backdrop-filter:blur(6px)">
        <div style="color:rgba(255,255,255,0.65);font-size:0.78rem;letter-spacing:.05em;
                    text-transform:uppercase">{label}</div>
        <div style="color:#ffffff;font-size:1.7rem;font-weight:700;margin-top:4px;
                    white-space:nowrap;overflow:hidden;text-overflow:ellipsis"
             title="{value}">{value}</div>
    </div>"""


# ── ERD ────────────────────────────────────────────────────────────────────────
def _show_erd():
    import plotly.graph_objects as go

    schemas = {
        "train.zip":           {"kolom": ["date","store_nbr","family","sales","onpromotion"],             "pk": [],            "fk": ["store_nbr","date","family"], "color": "#38bdf8"},
        "stores.csv":          {"kolom": ["store_nbr","city","state","type","cluster"],                    "pk": ["store_nbr"], "fk": [],                            "color": "#34d399"},
        "oil.csv":             {"kolom": ["date","dcoilwtico"],                                            "pk": ["date"],      "fk": [],                            "color": "#fb923c"},
        "holidays_events.csv": {"kolom": ["date","type","locale","locale_name","description","transferred"],"pk": [],           "fk": ["date"],                      "color": "#818cf8"},
        "transactions.csv":    {"kolom": ["date","store_nbr","transactions"],                              "pk": [],            "fk": ["date","store_nbr"],          "color": "#f472b6"},
    }
    positions = {
        "train.zip":           (0.5, 0.5),
        "stores.csv":          (0.0, 0.5),
        "oil.csv":             (0.5, 1.0),
        "holidays_events.csv": (1.0, 1.0),
        "transactions.csv":    (0.0, 1.0),
    }
    relations = [
        ("stores.csv",          "train.zip",           "store_nbr"),
        ("stores.csv",          "transactions.csv",    "store_nbr"),
        ("oil.csv",             "train.zip",           "date"),
        ("oil.csv",             "transactions.csv",    "date"),
        ("oil.csv",             "holidays_events.csv", "date"),
        ("holidays_events.csv", "train.zip",           "date"),
        ("transactions.csv",    "train.zip",           "date, store_nbr"),
    ]

    edge_x, edge_y, annotations = [], [], []
    for src, dst, via in relations:
        x0, y0 = positions[src]; x1, y1 = positions[dst]
        edge_x += [x0, x1, None]; edge_y += [y0, y1, None]
        annotations.append(dict(
            x=(x0+x1)/2, y=(y0+y1)/2, text=f"<i>{via}</i>", showarrow=False,
            font=dict(size=10, color="#a8c8ff"), bgcolor="rgba(12,92,229,0.7)", borderpad=3
        ))

    node_x, node_y, node_text, node_colors, node_hover = [], [], [], [], []
    for name, (x, y) in positions.items():
        s = schemas[name]
        node_x.append(x); node_y.append(y)
        node_text.append(f"<b>{name}</b>")
        node_colors.append(s["color"])
        pk_str   = ", ".join(s["pk"]) if s["pk"] else "—"
        fk_str   = ", ".join(s["fk"]) if s["fk"] else "—"
        cols_str = "<br>".join([
            f"  {'🔑' if c in s['pk'] else '🔗' if c in s['fk'] else '·'} <b>{c}</b>"
            for c in s["kolom"]
        ])
        node_hover.append(f"<b>{name}</b><br>PK: {pk_str}<br>FK: {fk_str}<br>─────<br>{cols_str}")

    fig = go.Figure(data=[
        go.Scatter(x=edge_x, y=edge_y, mode="lines",
                   line=dict(width=1.5, color="rgba(255,255,255,0.25)", dash="dot"), hoverinfo="none"),
        go.Scatter(x=node_x, y=node_y, mode="markers+text", text=node_text,
                   textposition="top center", textfont=dict(size=12, color="#ffffff"),
                   marker=dict(size=40, color=node_colors,
                               line=dict(width=2, color="rgba(255,255,255,0.2)"), symbol="square"),
                   hovertext=node_hover, hoverinfo="text",
                   hoverlabel=dict(bgcolor="#0a3fa8", bordercolor="#4a8aff",
                                   font=dict(color="#e8f0fe", size=11))),
    ], layout=go.Layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", showlegend=False,
        margin=dict(l=40, r=40, t=40, b=40), height=500,
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-0.2, 1.2]),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[0.3, 1.2]),
        annotations=annotations, hovermode="closest",
    ))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.markdown("### Detail Kolom per File")
    cols_leg = st.columns(3)
    for idx, (name, s) in enumerate(schemas.items()):
        with cols_leg[idx % 3]:
            kolom_html = "".join([
                f"<div style='padding:3px 0;font-size:.82rem'>"
                f"{'🔑' if c in s['pk'] else '🔗' if c in s['fk'] else '·'} "
                f"<span style='color:{'#fde68a' if c in s['pk'] else '#c4b5fd' if c in s['fk'] else 'rgba(255,255,255,0.80)'}'>"
                f"{c}</span></div>"
                for c in s["kolom"]
            ])
            st.markdown(f"""
            <div style='background:rgba(255,255,255,0.12);border:1px solid rgba(255,255,255,0.22);
                        border-left:3px solid {s["color"]};border-radius:10px;
                        padding:1rem;margin-bottom:1rem;
                        backdrop-filter:blur(6px);-webkit-backdrop-filter:blur(6px)'>
                <div style='color:#ffffff;font-weight:700;font-size:.95rem;margin-bottom:8px'>{name}</div>
                {kolom_html}
            </div>""", unsafe_allow_html=True)


# ── Inject CSS ─────────────────────────────────────────────────────────────────
def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"], * { font-family: 'Inter', sans-serif !important; }

    .stApp { background-color: #0c5ce5 !important; }

    header[data-testid="stHeader"],
    header[data-testid="stHeader"] > div,
    header[data-testid="stHeader"] > div > div,
    .stAppHeader, div[data-testid="stToolbar"] {
        background-color: #ffffff !important;
        background: #ffffff !important;
        border-bottom: 1px solid #e0e7f5 !important;
        box-shadow: 0 2px 12px rgba(12,92,229,0.10) !important;
    }
    header[data-testid="stHeader"] button svg,
    header[data-testid="stHeader"] svg {
        fill: #0c5ce5 !important; color: #0c5ce5 !important;
    }
    div[style*="background-color: rgb(13, 27, 46)"],
    header [style*="background-color"] {
        background-color: #ffffff !important; background: #ffffff !important;
    }
    #stDecoration { display: none !important; }

    section[data-testid="stSidebar"],
    section[data-testid="stSidebar"] > div {
        background-color: #ffffff !important;
        border-right: 1px solid #ccdaf8 !important;
    }
    section[data-testid="stSidebar"] * { color: #1a3a6e !important; }

    .block-container { padding-top: 2rem !important; padding-bottom: 3rem !important; }

    .page-header { text-align: center; padding: 2rem 1rem 1.25rem; margin-bottom: 0.5rem; }
    .page-header h1 {
        color: #ffffff !important; font-size: 1.9rem !important;
        font-weight: 700 !important; letter-spacing: -0.3px; line-height: 1.3;
        text-shadow: 0 2px 12px rgba(0,0,0,0.18); margin-bottom: 0.5rem;
    }
    .subtitle { color: #a8c8ff !important; font-size: 1.05rem; font-weight: 500; }

    .stMarkdown h2, .stMarkdown h3, h2, h3 { color: #ffffff !important; font-weight: 600 !important; }
    .stMarkdown h2 {
        font-size: 1.2rem !important;
        border-left: 4px solid rgba(255,255,255,0.5);
        padding-left: 0.75rem; margin-top: 1.5rem !important;
    }
    .stMarkdown h3 { font-size: 1.1rem !important; }

    .card {
        background: rgba(255,255,255,0.10) !important;
        border: 1px solid rgba(255,255,255,0.22) !important;
        border-radius: 14px; padding: 1.4rem 1.75rem;
        color: #e8f0fe !important; line-height: 1.75; font-size: 0.97rem;
        backdrop-filter: blur(6px); -webkit-backdrop-filter: blur(6px);
    }
    .card p { color: #e8f0fe !important; margin-bottom: 0.75rem; }
    .card p:last-child { margin-bottom: 0; }
    .card strong { color: #ffffff !important; font-weight: 600; }

    [data-testid="stDataFrame"] {
        background: rgba(255,255,255,0.08) !important;
        border-radius: 10px; overflow: hidden;
    }
    [data-testid="stDataFrame"] * { color: #e8f0fe !important; }

    .stSelectbox label, .stSlider label, .stRadio label, label {
        color: #ffffff !important; font-weight: 500 !important;
    }
    .stSelectbox > div > div {
        background: rgba(255,255,255,0.12) !important;
        border: 1px solid rgba(255,255,255,0.25) !important;
        border-radius: 8px !important; color: #ffffff !important;
    }

    [data-testid="stTabs"] button {
        color: rgba(255,255,255,0.65) !important; font-weight: 500 !important;
    }
    [data-testid="stTabs"] button[aria-selected="true"] {
        color: #ffffff !important; border-bottom: 2px solid #ffffff !important;
    }

    [data-testid="stAlert"] {
        background: rgba(255,255,255,0.15) !important;
        border: 1px solid rgba(255,255,255,0.25) !important;
        border-radius: 10px !important;
    }
    [data-testid="stAlert"] p,
    [data-testid="stAlert"] span,
    [data-testid="stAlert"] * { color: #ffffff !important; font-weight: 600 !important; }

    hr { border-color: rgba(255,255,255,0.18) !important; margin: 1.25rem 0 !important; }

    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #0a50cc; }
    ::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.3); border-radius: 3px; }
    </style>
    """, unsafe_allow_html=True)


# ── Main ───────────────────────────────────────────────────────────────────────
def show():
    inject_css()

    if not os.path.exists(DATASET_DIR):
        st.error(f"Folder dataset tidak ditemukan: `{DATASET_DIR}`")
        st.info("Sesuaikan `DATASET_DIR` di baris atas file ini dengan path yang benar.")
        return

    st.markdown("""
    <div class="page-header">
        <h1>Dataset Overview</h1>
        <p class="subtitle">Informasi, statistik, dan visualisasi dataset</p>
    </div>
    """, unsafe_allow_html=True)

    all_dfs = load_all_files()

    if not all_dfs:
        st.warning(f"Tidak ada file CSV/XLSX di: `{DATASET_DIR}`")
        return

    st.markdown("### Pilih Dataset")
    mode_options = ["— Pilih file —"] + sorted(all_dfs.keys()) + ["Gabungan Semua Dataset"]
    col_sel, col_info = st.columns([2, 3])

    with col_sel:
        selected = st.selectbox(
            "Dataset yang ingin dilihat",
            options=mode_options,
            index=0,
            help="Pilih satu file atau 'Gabungan' untuk merge semua dataset."
        )

    with col_info:
        if selected == "Gabungan Semua Dataset":
            st.success(f"Menggabungkan **{len(all_dfs)}** file: {', '.join(sorted(all_dfs.keys()))}")
        elif selected != "— Pilih file —":
            df_prev = all_dfs[selected]
            st.success(f"**{selected}** — {df_prev.shape[0]:,} baris × {df_prev.shape[1]} kolom")

    # ── Tampilkan ringkasan jika belum memilih file ────────────────────────────
    if selected == "— Pilih file —":
        st.markdown("---")
        st.markdown("### Ringkasan Semua File")
        summary_rows = []
        for fname, df in sorted(all_dfs.items()):
            summary_rows.append({
                "File":           fname,
                "Baris":          f"{df.shape[0]:,}",
                "Kolom":          df.shape[1],
                "Missing Values": int(df.isnull().sum().sum()),
                "Kolom Numerik":  len(df.select_dtypes("number").columns),
                "Kolom Teks":     len(df.select_dtypes("object").columns),
            })
        st.dataframe(pd.DataFrame(summary_rows), use_container_width=True, hide_index=True)
        return

    # ── Load data sesuai pilihan ───────────────────────────────────────────────
    is_merged = selected == "Gabungan Semua Dataset"

    if is_merged:
        with st.spinner("Menggabungkan dataset..."):
            df = merge_all(all_dfs)
        mode_label  = "Gabungan"
        badge_color = "#34d399"
        total_rows  = df.shape[0]
    else:
        df          = all_dfs[selected]
        mode_label  = selected
        badge_color = "#38bdf8"
        path_file   = os.path.join(DATASET_DIR, selected)
        total_rows  = get_total_rows(path_file)

    # ── Metric Cards ──────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### Informasi Raw Dataset")
    label_file = mode_label[:20] + ("…" if len(mode_label) > 20 else "")
    cards_html = "".join([
        _metric_card("File",           label_file,              badge_color),
        _metric_card("Total Baris",    f"{total_rows:,}",       "#38bdf8"),
        _metric_card("Preview Dimuat", f"{df.shape[0]:,}",      "#7dd3fc"),
        _metric_card("Kolom",          str(df.shape[1]),         "#34d399"),
        _metric_card("Missing Values", str(int(df.isnull().sum().sum())), "#fb923c"),
    ])
    st.markdown(
        f"<div style='display:grid;grid-template-columns:repeat(5,1fr);gap:1rem;margin-bottom:1.5rem'>"
        f"{cards_html}</div>",
        unsafe_allow_html=True
    )

    # ── Tabs: berbeda untuk merged vs single file ──────────────────────────────
    if is_merged:
        tab_preview, tab_stats, tab_erd = st.tabs(["Preview Data", "Statistik", "ERD"])
    else:
        tab_preview, tab_stats, tab_vis, tab_erd = st.tabs(
            ["Preview Data", "Statistik", "Visualisasi", "ERD"]
        )

    # ── Tab: Preview ──────────────────────────────────────────────────────────
    with tab_preview:
        st.markdown("### Preview Data")
        n_preview = st.slider("Jumlah baris yang ditampilkan", min_value=5, max_value=min(500, df.shape[0]), value=10, step=5)
        st.dataframe(df.head(n_preview), use_container_width=True)

    # ── Tab: Statistik ────────────────────────────────────────────────────────
    with tab_stats:
        st.markdown("### Statistik Deskriptif")
        num_df = df.select_dtypes("number")
        if not num_df.empty:
            st.dataframe(num_df.describe().T, use_container_width=True)
        else:
            st.info("Tidak ada kolom numerik pada dataset ini.")

        st.markdown("### Missing Values per Kolom")
        missing = df.isnull().sum()
        missing = missing[missing > 0].reset_index()
        if not missing.empty:
            missing.columns = ["Kolom", "Jumlah Missing"]
            missing["Persentase (%)"] = (missing["Jumlah Missing"] / len(df) * 100).round(2)
            st.dataframe(missing, use_container_width=True, hide_index=True)
        else:
            st.success("Tidak ada missing values!")

    # ── Tab: Visualisasi (hanya untuk single file) ────────────────────────────
    if not is_merged:
        with tab_vis:
            st.markdown("### Visualisasi Data")
            num_cols = df.select_dtypes("number").columns.tolist()
            cat_cols = df.select_dtypes("object").columns.tolist()
            v1, v2   = st.columns(2)
            with v1:
                if num_cols:
                    sel = st.selectbox("Distribusi kolom numerik", num_cols, key="num_vis")
                    st.bar_chart(df[sel].value_counts().sort_index())
                else:
                    st.info("Tidak ada kolom numerik.")
            with v2:
                if cat_cols:
                    sel2 = st.selectbox("Distribusi kolom kategorikal", cat_cols, key="cat_vis")
                    st.bar_chart(df[sel2].value_counts())
                else:
                    st.info("Tidak ada kolom kategorikal.")

    # ── Tab: ERD ──────────────────────────────────────────────────────────────
    with tab_erd:
        st.markdown("### Relasi Antar Dataset (ERD)")
        st.markdown("Diagram relasi antar file CSV berdasarkan kolom yang sama.")
        _show_erd()