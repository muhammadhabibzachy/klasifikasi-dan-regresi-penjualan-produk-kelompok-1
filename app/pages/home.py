import streamlit as st


# ── CSS Global ──────────────────────────────────────────────────────────────
def inject_css():
    st.markdown("""
    <style>
                
    /* ── Import Font ── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    /* ── Reset & Font Global ── */
    html, body, [class*="css"], * {
        font-family: 'Inter', sans-serif !important;
    }
    .menu .container-xxl[data-v-5af006b8] {
        background-color: var(--secondary-background-color) !important;
        border-radius: .5rem;
    }
    /* ── Latar Belakang Halaman ── */
    .stApp {
        background-color: #0c5ce5 !important;
    }

    /* ── Navbar / Header Streamlit ── */
    header[data-testid="stHeader"] {
        background-color: fffff !important;
        border-bottom: 1px solid #e0e7f5 !important;
        box-shadow: 0 2px 12px rgba(12, 92, 229, 0.10) !important;
    }

    /* Ikon & tombol di navbar */
    header[data-testid="stHeader"] button,
    header[data-testid="stHeader"] svg {
        color: #0c5ce5 !important;
        fill: #0c5ce5 !important;
    }

    /* ── Sidebar ── */
    section[data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #ccdaf8 !important;
    }
    section[data-testid="stSidebar"] * {
        color: #1a3a6e !important;
    }
    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] .stRadio label {
        color: #0c5ce5 !important;
        font-weight: 600 !important;
    }

    /* ── Konten Utama (main block) ── */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 3rem !important;
    }

    /* ── Page Header ── */
    .page-header {
        text-align: center;
        padding: 2.5rem 1rem 1.5rem;
    }
    .page-header h1 {
        color: #ffffff !important;
        font-size: 1.9rem !important;
        font-weight: 1500 !important;
        letter-spacing: -0.3px;
        line-height: 1.3;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        color: #a8c8ff !important;
        font-size: 1.05rem;
        font-weight: 500;
        margin-top: 0.25rem;
    }

    /* ── Kartu Deskripsi ── */
    .card {
        background: rgba(255, 255, 255, 0.10) !important;
        border: 1px solid rgba(255, 255, 255, 0.22) !important;
        border-radius: 14px;
        padding: 1.4rem 1.75rem;
        color: #e8f0fe !important;
        line-height: 1.75;
        font-size: 0.97rem;
        backdrop-filter: blur(6px);
        -webkit-backdrop-filter: blur(6px);
    }
    .card p {
        color: #e8f0fe !important;
        margin-bottom: 0.75rem;
    }
    .card p:last-child {
        margin-bottom: 0;
    }
    .card strong {
        color: #ffffff !important;
        font-weight: 600;
    }

    /* ── Heading Markdown (## ...) ── */
    .stMarkdown h2 {
        color: #ffffff !important;
        font-size: 1.25rem !important;
        font-weight: 600 !important;
        margin-top: 1.5rem !important;
        margin-bottom: 0.6rem !important;
        border-left: 4px solid rgba(255,255,255,0.5);
        padding-left: 0.75rem;
    }

    /* ── Kartu Anggota ── */
    .member-card {
        background: rgba(255, 255, 255, 0.10) !important;
        border: 1px solid rgba(255, 255, 255, 0.5) !important;
        border-radius: 12px;
        padding: 1.2rem 1rem;
        text-align: center;
        transition: transform 0.15s ease, background 0.15s ease;
    }
    .member-card:hover {
        background: rgba(255, 255, 255, 0.20) !important;
        transform: translateY(-2px);
    }
    .member-avatar {
        width: 52px;
        height: 52px;
        border-radius: 50%;
        background: rgba(255,255,255,0.25);
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 0.75rem;
        font-size: 1.2rem;
        font-weight: 700;
        color: #ffffff;
        border: 2px solid rgba(255,255,255,0.4);
    }
    .member-no {
        font-size: 0.72rem;
        font-weight: 600;
        color: #a8c8ff !important;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 4px;
    }
    .member-name {
        color: #ffffff !important;
        font-weight: 600;
        font-size: 0.95rem;
        margin-bottom: 4px;
    }
    .member-nim {
        color: #c0d8ff !important;
        font-size: 0.82rem;
    }

    /* ── Divider ── */
    hr {
        border-color: rgba(255,255,255,0.15) !important;
        margin: 1.5rem 0 !important;
    }

    /* ── Scrollbar ── */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #0a50cc; }
    ::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.3); border-radius: 3px; }
    </style>
    """, unsafe_allow_html=True)


# ── Halaman Utama ────────────────────────────────────────────────────────────
def show():
    inject_css()

    with st.container():
        # Header
        st.markdown("""
        <div style="padding: 1.5rem 2rem 0.5rem;">
            <div class="page-header">
                <h1>SISTEM KLASIFIKASI DAN REGRESI PENJUALAN PRODUK</h1>
                <p class="subtitle">Kelompok 1 &nbsp;·&nbsp; DTMG03</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div style="padding: 0 2rem;">', unsafe_allow_html=True)

        # ── Deskripsi ─────────────────────────────────────────────────────
        st.markdown("## Deskripsi")
        st.markdown("""
        <div class="card">
            <p>
            Proyek ini merupakan implementasi Algoritma Klasifikasi dengan menggunakan model
            <strong>LightGBM</strong> dan Algoritma Regresi dengan menggunakan model <strong>XGBoost</strong>
            sebagai bagian dari proyek Ujian Akhir Semester mata kuliah Data Mining.
            </p>
            <p>
            Sistem ini memungkinkan pengguna untuk melakukan prediksi penjualan secara mudah
            berdasarkan fitur yang dimasukkan dan menyajikan eksplorasi data dan visualisasi
            model secara detail.
            </p>
        </div>
        """, unsafe_allow_html=True)

        # ── Anggota Tim ───────────────────────────────────────────────────
        st.markdown("## Anggota TIM")

        members = [
            {"no": "01", "nama": "Zeplin Zeperson Hutauruk", "nim": "24051214088"},
            {"no": "02", "nama": "Muhammad Habib Zachy",     "nim": "24051214085"},
        ]

        cols = st.columns(len(members))
        for col, m in zip(cols, members):
            # Inisial dari nama
            initials = "".join([w[0].upper() for w in m["nama"].split()[:2]])
            with col:
                st.markdown(f"""
                <div class="member-card">
                    <div class="member-avatar">{initials}</div>
                    <div class="member-no">Anggota {m['no']}</div>
                    <div class="member-name">{m['nama']}</div>
                    <div class="member-nim">NIM: {m['nim']}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)


# ── Jalankan langsung ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    show()