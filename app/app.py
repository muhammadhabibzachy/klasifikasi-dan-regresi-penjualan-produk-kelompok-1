import streamlit as st
import sys, os
from streamlit_option_menu import option_menu

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)

st.set_page_config(
    page_title="Klasifikasi — Kelompok 1",
    layout="wide",
    initial_sidebar_state="collapsed",
)

css_path = os.path.join(os.path.dirname(__file__), "assets", "style.css")
if os.path.exists(css_path):
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    html, body, [class*="css"] {
        font-family: Merriweather, serif;
    }
    [data-testid="stToolbar"]        { display: none !important; }
    [data-testid="stDecoration"]     { display: none !important; }
    [data-testid="stSidebar"]        { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }
    header[data-testid="stHeader"]   { display: none !important; height: 0 !important; }
    #MainMenu                        { display: none !important; }
    footer                           { display: none !important; }

    .stApp                           { margin-top: 0 !important; padding-top: 0 !important; }
    .appview-container               { padding-top: 0 !important; margin-top: 0 !important; }
    section[data-testid="stMain"]    { padding-top: 0 !important; }
    section[data-testid="stMain"] > div { padding-top: 0 !important; }
    div[class*="stMainBlockContainer"] { padding-top: 0 !important; margin-top: 0 !important; }

    .block-container {
        padding-top: 0 !important;
        margin-top: 0 !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
        max-width: 100% !important;
    }

    /* Padding konten halaman agar tidak mepet */
    .page-content {
        padding: 1.5rem 3rem;
        max-width: 1200px;
        margin: 0 auto;
    }
</style>
""", unsafe_allow_html=True)

# ── Session state ──────────────────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "home"

pages = {
    "Home":             ("home",          "house"),
    "Dataset Overview": ("dataset",       "table"),
    "Prediksi":         ("prediksi",      "graph-up"),
    "Tentang":          ("about",         "info-circle"),
}

labels = list(pages.keys())
keys   = [v[0] for v in pages.values()]
icons  = [v[1] for v in pages.values()]

current_index = keys.index(st.session_state.page) if st.session_state.page in keys else 0

# ── Top Navbar ─────────────────────────────────────────────────────────────────
selected_label = option_menu(
    menu_title=None,
    options=labels,
    icons=icons,
    default_index=current_index,
    orientation="horizontal",
    styles={
        "container": {
            "background-color": "#0d1b2e",
            "padding": "6px 24px",
            "margin": "0px",
            "width": "auto",
            "border-radius": "0px",
        },
        "icon": {
            "color": "#5bc4e0",
            "font-size": "16px",
        },
        "nav-link": {
            "color": "#8ba8c0",
            "font-size": "14px",
            "border-radius": "8px",
            "padding": "8px 20px",
            "--hover-color": "rgba(255,255,255,0.08)",
        },
        "nav-link-selected": {
            "background-color": "#2a6fdb",
            "color": "white",
            "font-weight": "500",
        },
    }
)

# ── Update halaman ─────────────────────────────────────────────────────────────
selected_key = pages[selected_label][0]
if st.session_state.page != selected_key:
    st.session_state.page = selected_key
    st.rerun()

# ── Router ─────────────────────────────────────────────────────────────────────
page = st.session_state.page

_, col_main, _ = st.columns([1, 10, 1])   # margin kiri kanan otomatis
with col_main:
    if page == "home":
        from pages import home as p; p.show()
    elif page == "dataset":
        from pages import dataset as p; p.show()
    elif page == "prediksi":
        from pages import prediksi as p; p.show()
    elif page == "about":
        from pages import about as p; p.show()