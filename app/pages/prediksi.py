import streamlit as st
import sys, os
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))


# ── Inject CSS ─────────────────────────────────────────────────────────────────
def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"], * {
        font-family: 'Inter', sans-serif !important;
    }

    .stApp {
        background-color: #0c5ce5 !important;
    }

    /* ── Header ── */
    header[data-testid="stHeader"],
    header[data-testid="stHeader"] > div,
    .stAppHeader {
        background-color: #ffffff !important;
        border-bottom: 1px solid #e0e7f5 !important;
        box-shadow: 0 2px 12px rgba(12,92,229,0.10) !important;
    }
    header[data-testid="stHeader"] button svg,
    header[data-testid="stHeader"] svg {
        fill: #0c5ce5 !important;
        color: #0c5ce5 !important;
    }
    #stDecoration { display: none !important; }

    /* ── Sidebar ── */
    section[data-testid="stSidebar"],
    section[data-testid="stSidebar"] > div {
        background-color: #ffffff !important;
        border-right: 1px solid #ccdaf8 !important;
    }
    section[data-testid="stSidebar"] * {
        color: #1a3a6e !important;
    }

    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 3rem !important;
    }

    /* ── Page header ── */
    .page-header {
        text-align: center;
        padding: 2rem 1rem 1.25rem;
        margin-bottom: 0.5rem;
    }
    .page-header h1 {
        color: #ffffff !important;
        font-size: 1.9rem !important;
        font-weight: 700 !important;
        letter-spacing: -0.3px;
        line-height: 1.3;
        text-shadow: 0 2px 12px rgba(0,0,0,0.18);
        margin-bottom: 0.5rem;
    }
    .subtitle {
        color: #a8c8ff !important;
        font-size: 1.05rem;
        font-weight: 500;
        margin-top: 0.25rem;
    }

    /* ── Headings ── */
    .stMarkdown h2, .stMarkdown h3, h2, h3 {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    .stMarkdown h3 {
        font-size: 1.2rem !important;
        border-left: 4px solid rgba(255,255,255,0.5);
        padding-left: 0.75rem;
        margin-top: 1.5rem !important;
    }

    /* ── Kartu mode prediksi ── */
    .mode-card {
        background: rgba(255,255,255,0.12);
        border: 1px solid rgba(255,255,255,0.22);
        border-radius: 16px;
        padding: 2rem;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        min-height: 300px;
        transition: background 0.2s ease;
    }
    .mode-card:hover {
        background: rgba(255,255,255,0.18);
    }

    /* ── Expander ── */
    [data-testid="stExpander"] {
        background: rgba(255,255,255,0.12) !important;
        border: 1px solid rgba(255,255,255,0.22) !important;
        border-radius: 10px !important;
        overflow: visible !important;
        position: relative !important;
        z-index: 1 !important;
    }
    [data-testid="stExpander"] summary {
        color: #ffffff !important;
        font-weight: 600 !important;
        padding: 0.75rem 1rem !important;
        position: relative !important;
        z-index: 2 !important;
    }
    [data-testid="stExpander"] summary:hover {
        background: rgba(255,255,255,0.08) !important;
        border-radius: 10px !important;
    }
    /* FIX: sembunyikan teks fallback "keyboard_arrow_right/down" */
    [data-testid="stExpander"] summary [data-testid="stExpanderToggleIcon"] {
        font-size: 0 !important;
        color: transparent !important;
        width: 20px !important;
        height: 20px !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    /* Tampilkan SVG di dalam icon span tetap normal */
    [data-testid="stExpander"] summary [data-testid="stExpanderToggleIcon"] svg {
        font-size: initial !important;
        color: initial !important;
        fill: #ffffff !important;
        width: 20px !important;
        height: 20px !important;
    }
    /* Ikon panah SVG langsung */
    [data-testid="stExpander"] summary svg {
        fill: #ffffff !important;
        color: #ffffff !important;
    }
    [data-testid="stExpander"] > div {
        position: relative !important;
        z-index: 1 !important;
    }
    /* Teks di dalam expander */
    [data-testid="stExpander"] p,
    [data-testid="stExpander"] td,
    [data-testid="stExpander"] th,
    [data-testid="stExpander"] li {
        color: #e2eeff !important;
    }
    /* Sembunyikan HANYA span yang berisi teks keyboard_arrow — bukan semua span */
    [data-testid="stExpander"] summary span:not([data-testid]):not([class]) {
        font-family: 'Material Symbols Rounded', 'Material Icons', sans-serif !important;
        font-size: 20px !important;
        color: #ffffff !important;
    }
    [data-testid="stExpander"] strong {
        color: #ffffff !important;
    }
    [data-testid="stExpander"] code {
        background: rgba(255,255,255,0.15) !important;
        color: #c4b5fd !important;
        border-radius: 4px !important;
        padding: 1px 5px !important;
    }
    /* Tabel di dalam expander */
    [data-testid="stExpander"] table {
        background: rgba(255,255,255,0.05) !important;
        border-radius: 8px !important;
        overflow: hidden !important;
    }
    [data-testid="stExpander"] th {
        background: rgba(255,255,255,0.12) !important;
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    [data-testid="stExpander"] tr:nth-child(even) td {
        background: rgba(255,255,255,0.04) !important;
    }

    /* ── File uploader — putih transparan ── */
    [data-testid="stFileUploader"] {
        background: rgba(255,255,255,0.15) !important;
        border: 2px dashed rgba(255,255,255,0.45) !important;
        border-radius: 12px !important;
        padding: 0.5rem !important;
        transition: background 0.2s ease, border-color 0.2s ease !important;
    }
    [data-testid="stFileUploader"]:hover {
        background: rgba(255,255,255,0.22) !important;
        border-color: rgba(255,255,255,0.7) !important;
    }
    /* Area drop dalam uploader */
    [data-testid="stFileUploader"] > div,
    [data-testid="stFileUploaderDropzone"] {
        background: transparent !important;
        border: none !important;
    }
    /* Teks "Drag and drop" dll */
    [data-testid="stFileUploader"] span,
    [data-testid="stFileUploader"] p,
    [data-testid="stFileUploaderDropzoneInstructions"] span {
        color: #ffffff !important;
        font-weight: 500 !important;
    }
    /* Tombol Browse files */
    [data-testid="stFileUploader"] button,
    [data-testid="stBaseButton-secondary"] {
        background: rgba(255,255,255,0.2) !important;
        border: 1px solid rgba(255,255,255,0.5) !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        border-radius: 6px !important;
    }
    [data-testid="stFileUploader"] button:hover {
        background: rgba(255,255,255,0.32) !important;
    }
    /* Icon upload */
    [data-testid="stFileUploaderDropzoneInstructions"] svg {
        fill: rgba(255,255,255,0.7) !important;
    }

    /* ── Tombol ── */
    .stButton > button {
        border-radius: 8px !important;
        font-weight: 500 !important;
    }
    .stButton > button[kind="primary"],
    .stButton > button[data-testid="baseButton-primary"] {
        background: linear-gradient(90deg, #f59e0b, #fbbf24) !important;
        border: none !important;
        color: #1a1a1a !important;
        font-weight: 600 !important;
    }
    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(90deg, #fbbf24, #fcd34d) !important;
    }
    .stButton > button[kind="secondary"],
    .stButton > button {
        background: rgba(255,255,255,0.12) !important;
        border: 1px solid rgba(255,255,255,0.3) !important;
        color: #ffffff !important;
    }
    .stButton > button:hover {
        background: rgba(255,255,255,0.20) !important;
    }

    /* ── Alert ── */
    [data-testid="stAlert"] {
        background: rgba(255,255,255,0.10) !important;
        border: 1px solid rgba(255,255,255,0.25) !important;
        border-radius: 10px !important;
    }
    [data-testid="stAlert"] p,
    [data-testid="stAlert"] span,
    [data-testid="stAlert"] * {
        color: #ffffff !important;
        font-weight: 600 !important;
    }

    /* ── Divider ── */
    hr {
        border-color: rgba(255,255,255,0.18) !important;
        margin: 1.25rem 0 !important;
    }

    /* ── Scrollbar ── */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #0a50cc; }
    ::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.3); border-radius: 3px; }
    </style>
    """, unsafe_allow_html=True)


# ── Riwayat helpers ────────────────────────────────────────────────────────────
def _init_history():
    if "prediction_history" not in st.session_state:
        st.session_state.prediction_history = []


def add_to_history(mode: str, inputs: dict, result):
    _init_history()
    entry = {
        "id":        len(st.session_state.prediction_history) + 1,
        "timestamp": datetime.now().strftime("%d %b %Y, %H:%M:%S"),
        "mode":      mode,
        "inputs":    inputs,
        "result":    result,
    }
    st.session_state.prediction_history.insert(0, entry)
    if len(st.session_state.prediction_history) > 50:
        st.session_state.prediction_history.pop()


def _clear_history():
    st.session_state.prediction_history = []


# ── Komponen riwayat ───────────────────────────────────────────────────────────
def _show_history():
    _init_history()
    history = st.session_state.prediction_history

    st.markdown("---")
    st.markdown("### Riwayat Prediksi")

    if not history:
        st.markdown("""
        <div style="background:rgba(255,255,255,0.08);border:1px dashed rgba(255,255,255,0.25);
                    border-radius:12px;padding:2rem;text-align:center;
                    color:rgba(255,255,255,0.5);font-size:0.9rem">
            Belum ada riwayat prediksi.<br>
            <span style="font-size:0.8rem;color:rgba(255,255,255,0.35)">
                Riwayat akan muncul setelah kamu melakukan prediksi.
            </span>
        </div>
        """, unsafe_allow_html=True)
        return

    col_title, col_clear = st.columns([5, 1])
    with col_clear:
        if st.button("Hapus Semua", key="clear_history", use_container_width=True):
            _clear_history()
            st.rerun()

    MODE_COLOR = {"Upload File": "#7dd3fc", "Manual": "#6ee7b7"}

    for entry in history:
        color = MODE_COLOR.get(entry["mode"], "#c4b5fd")
        result = entry["result"]
        if hasattr(result, "shape"):
            result_str = f"DataFrame {result.shape[0]} baris × {result.shape[1]} kolom"
        elif isinstance(result, (int, float)):
            result_str = f"{result:,.4f}"
        else:
            result_str = str(result)[:120]

        inputs_html = " &nbsp;·&nbsp; ".join(
            f"<span style='color:rgba(255,255,255,0.5)'>{k}:</span> "
            f"<span style='color:rgba(255,255,255,0.85)'>{v}</span>"
            for k, v in list(entry["inputs"].items())[:5]
        )
        if len(entry["inputs"]) > 5:
            inputs_html += f" &nbsp;·&nbsp; <span style='color:rgba(255,255,255,0.35)'>+{len(entry['inputs'])-5} lainnya</span>"

        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.10);border:1px solid rgba(255,255,255,0.18);
                    border-left:3px solid {color};border-radius:10px;
                    padding:0.9rem 1.2rem;margin-bottom:0.6rem;">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.4rem">
                <div>
                    <span style="background:rgba(255,255,255,0.15);color:{color};
                                 font-size:0.7rem;font-weight:700;padding:2px 8px;
                                 border-radius:20px;letter-spacing:.05em;
                                 text-transform:uppercase;margin-right:8px">{entry['mode']}</span>
                    <span style="color:rgba(255,255,255,0.45);font-size:0.75rem">
                        #{entry['id']} &nbsp;·&nbsp; {entry['timestamp']}
                    </span>
                </div>
            </div>
            <div style="font-size:0.78rem;color:rgba(255,255,255,0.5);margin-bottom:0.3rem">
                Input: {inputs_html}
            </div>
            <div style="font-size:0.85rem">
                <span style="color:rgba(255,255,255,0.5)">Hasil: </span>
                <span style="color:{color};font-weight:600">{result_str}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    total    = len(history)
    n_file   = sum(1 for e in history if e["mode"] == "Upload File")
    n_manual = sum(1 for e in history if e["mode"] == "Manual")

    st.markdown(f"""
    <div style="display:flex;gap:1rem;margin-top:0.5rem;flex-wrap:wrap">
        <div style="background:rgba(255,255,255,0.10);border:1px solid rgba(255,255,255,0.2);
                    border-radius:8px;padding:0.5rem 1rem;font-size:0.8rem;color:rgba(255,255,255,0.6)">
            Total: <span style="color:#ffffff;font-weight:700">{total}</span>
        </div>
        <div style="background:rgba(255,255,255,0.10);border:1px solid rgba(255,255,255,0.2);
                    border-radius:8px;padding:0.5rem 1rem;font-size:0.8rem;color:rgba(255,255,255,0.6)">
            Upload File: <span style="color:#7dd3fc;font-weight:700">{n_file}</span>
        </div>
        <div style="background:rgba(255,255,255,0.10);border:1px solid rgba(255,255,255,0.2);
                    border-radius:8px;padding:0.5rem 1rem;font-size:0.8rem;color:rgba(255,255,255,0.6)">
            Input Manual: <span style="color:#6ee7b7;font-weight:700">{n_manual}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ── Main ───────────────────────────────────────────────────────────────────────
def show():
    inject_css()
    _init_history()

    if "prediksi_mode" not in st.session_state:
        st.session_state.prediksi_mode = None

    if st.session_state.prediksi_mode is None:
        _show_landing()
    elif st.session_state.prediksi_mode == "file":
        _back_btn()
        import prediksi_file as p
        p.show()
    elif st.session_state.prediksi_mode == "simple":
        _back_btn()
        import prediksi_inputfitur as p
        p.show()


def _back_btn():
    if st.button("← Kembali ke Pilihan Mode", key="back_prediksi"):
        st.session_state.prediksi_mode = None
        st.rerun()


def _show_landing():
    st.markdown("""
    <div class="page-header">
        <h1>Prediksi Penjualan</h1>
        <p class="subtitle">Pilih mode prediksi yang sesuai kebutuhanmu</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown("""
        <div class="mode-card">
            <div style="color:#ffffff;font-size:1.5rem;font-weight:700;margin-bottom:0.75rem">
                Mode Upload File
            </div>
            <div style="color:rgba(255,255,255,0.7);font-size:0.85rem;margin-bottom:0.75rem">
                Prediksi untuk banyak baris sekaligus dari file CSV
            </div>
            <div style="color:rgba(255,255,255,0.45);font-size:0.8rem;line-height:1.8">
                Kolom wajib:<br>
                <span style="color:#c4b5fd">store_nbr</span> · 
                <span style="color:#c4b5fd">date</span> · 
                <span style="color:#c4b5fd">oil_price</span> · 
                <span style="color:#c4b5fd">onpromotion</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(" ")
        if st.button("Gunakan Mode Upload File", key="btn_file",
                     type="primary", use_container_width=True):
            st.session_state.prediksi_mode = "file"
            st.rerun()

    with col2:
        st.markdown("""
        <div class="mode-card">
            <div style="color:#ffffff;font-size:1.5rem;font-weight:700;margin-bottom:0.75rem">
                Mode Input Manual
            </div>
            <div style="color:rgba(255,255,255,0.7);font-size:0.85rem;margin-bottom:0.75rem">
                Masukkan nilai fitur satu per satu untuk prediksi cepat
            </div>
            <div style="color:rgba(255,255,255,0.45);font-size:0.8rem;line-height:1.8">
                Fitur:<br>
                <span style="color:#c4b5fd">store_nbr</span> · 
                <span style="color:#c4b5fd">date</span> · 
                <span style="color:#c4b5fd">oil_price</span> · 
                <span style="color:#c4b5fd">onpromotion</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(" ")
        if st.button("Gunakan Mode Input Manual", key="btn_simple",
                     type="primary", use_container_width=True):
            st.session_state.prediksi_mode = "simple"
            st.rerun()

    _show_history()


