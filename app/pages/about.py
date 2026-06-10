import streamlit as st


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

    /* ── Kartu konten utama ── */
    .card {
        background: rgba(255,255,255,0.10) !important;
        border: 1px solid rgba(255,255,255,0.22) !important;
        border-radius: 14px; padding: 1.4rem 1.75rem;
        color: #e8f0fe !important; line-height: 1.75; font-size: 0.97rem;
        backdrop-filter: blur(6px); -webkit-backdrop-filter: blur(6px);
        margin-bottom: 1rem;
    }
    .card p  { color: #e8f0fe !important; margin-bottom: 0.75rem; }
    .card p:last-child { margin-bottom: 0; }
    .card strong { color: #ffffff !important; font-weight: 600; }
    .card h4 {
        color: #7dd3fc !important; font-size: 1.05rem !important;
        font-weight: 700 !important; margin-bottom: 0.75rem;
        font-family: 'Courier New', monospace !important;
    }
    .card ul { color: #e8f0fe !important; padding-left: 1.25rem; margin: 0.5rem 0; }
    .card li { margin-bottom: 0.4rem; }
    .card table { width: 100%; border-collapse: collapse; }
    .card td { padding: 9px 12px; border-bottom: 1px solid rgba(255,255,255,0.08); }
    .card tr:last-child td { border-bottom: none; }
    .card tr:nth-child(even) { background: rgba(255,255,255,0.05); }

    /* ── Step item (alur pemrosesan) ── */
    .step-item {
        display: flex;
        align-items: flex-start;
        gap: 1rem;
        background: rgba(255,255,255,0.10);
        border: 1px solid rgba(255,255,255,0.22);
        border-left: 3px solid #7dd3fc;
        border-radius: 10px;
        padding: 0.9rem 1.1rem;
        margin-bottom: 0.6rem;
        backdrop-filter: blur(6px);
        -webkit-backdrop-filter: blur(6px);
    }
    .step-item strong { color: #ffffff !important; font-size: 0.95rem; }
    .step-item small  { color: #a8c8ff !important; font-size: 0.83rem; }
    .step-num {
        min-width: 28px; height: 28px;
        background: rgba(125,211,252,0.2);
        border: 1px solid rgba(125,211,252,0.4);
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        color: #7dd3fc !important; font-weight: 700; font-size: 0.82rem;
        flex-shrink: 0;
    }

    /* ── Tech card ── */
    .tech-card {
        background: rgba(255,255,255,0.10);
        border: 1px solid rgba(255,255,255,0.22);
        border-radius: 12px;
        padding: 1rem 1.1rem;
        margin-bottom: 0.75rem;
        backdrop-filter: blur(6px);
        -webkit-backdrop-filter: blur(6px);
        line-height: 1.6;
    }
    .tech-card strong { color: #7dd3fc !important; font-size: 0.95rem; }
    .tech-card small  { color: #a8c8ff !important; font-size: 0.82rem; }

    /* ── Tabs ── */
    [data-testid="stTabs"] button {
        color: rgba(255,255,255,0.65) !important; font-weight: 500 !important;
    }
    [data-testid="stTabs"] button[aria-selected="true"] {
        color: #ffffff !important; border-bottom: 2px solid #ffffff !important;
    }

    hr { border-color: rgba(255,255,255,0.18) !important; margin: 1.25rem 0 !important; }

    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #0a50cc; }
    ::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.3); border-radius: 3px; }
    </style>
    """, unsafe_allow_html=True)


def show():
    inject_css()

    st.markdown("""
    <div class="page-header">
        <h1>Tentang</h1>
        <p class="subtitle">Penjelasan alur, dataset, dan teknologi yang digunakan</p>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["Alur", "Dataset", "Teknologi"])

    # ── Tab 1: Metode ─────────────────────────────────────────────────────────
    with tab1:
        st.markdown("## Alur Pemrosesan")
        steps = [
            ("1", "Data Collection",     "Dataset Favorita Store Sales dari Kaggle"),
            ("2", "Feature Engineering", "Ekstraksi fitur waktu, lag sales, rolling mean, store & event lookup"),
            ("3", "Preprocessing",       "Label encoding, handling missing values, type casting"),
            ("4", "Model Training",      "LightGBM (klasifikasi) + XGBoost (regresi log1p sales)"),
            ("5", "Evaluation",          "Classification report, RMSE, RMSLE"),
            ("6", "Deployment",          "Streamlit web app dengan form input interaktif"),
        ]
        for num, title, desc in steps:
            st.markdown(f"""
            <div class="step-item">
                <div class="step-num">{num}</div>
                <div>
                    <strong>{title}</strong><br>
                    <small>{desc}</small>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ── Tab 2: Dataset ────────────────────────────────────────────────────────
    with tab2:
        st.markdown("## Informasi Dataset")
        st.markdown("""
        <div class="card">
            <table>
                <tr>
                    <td style="color:rgba(255,255,255,0.6);width:180px">Nama Dataset</td>
                    <td><strong>Corporación Favorita Grocery Sales</strong></td>
                </tr>
                <tr>
                    <td style="color:rgba(255,255,255,0.6)">Sumber</td>
                    <td>Kaggle Competition</td>
                </tr>
                <tr>
                    <td style="color:rgba(255,255,255,0.6)">File Utama</td>
                    <td>train.csv, test.csv, stores.csv, oil.csv, holidays_events.csv</td>
                </tr>
                <tr>
                    <td style="color:rgba(255,255,255,0.6)">Jumlah Toko</td>
                    <td>54 toko di Ekuador</td>
                </tr>
            </table>
        </div>
        """, unsafe_allow_html=True)

    # ── Tab 3: Teknologi ──────────────────────────────────────────────────────
    with tab3:
        st.markdown("## Teknologi yang Digunakan")
        techs = [
            ("Python",        "Bahasa pemrograman utama"),
            ("LightGBM",      "Model klasifikasi (Stage 1)"),
            ("XGBoost",       "Model regresi (Stage 2)"),
            ("Streamlit",     "Framework aplikasi web"),
            ("Pandas/NumPy",  "Manipulasi & analisis data"),
            ("Matplotlib",    "Visualisasi grafik"),
        ]
        tc1, tc2, tc3 = st.columns(3)
        for i, (name, desc) in enumerate(techs):
            col = [tc1, tc2, tc3][i % 3]
            with col:
                st.markdown(f"""
                <div class="tech-card">
                    <strong>{name}</strong><br>
                    <small>{desc}</small>
                </div>
                """, unsafe_allow_html=True)


if __name__ == "__main__":
    show()