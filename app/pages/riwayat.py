# BUG FIX: file was completely empty (0 bytes)
# Halaman ini tidak direferensikan di router app.py saat ini.
# Riwayat prediksi sudah ditampilkan di halaman Visualization tab "Riwayat Prediksi".
# File ini dijaga sebagai placeholder agar tidak error jika diimport.

import streamlit as st

def show():
    st.markdown("""
    <div class="page-header">
        <h1>📋 Riwayat Prediksi</h1>
        <p class="subtitle">Semua prediksi yang telah dilakukan dalam sesi ini</p>
    </div>
    """, unsafe_allow_html=True)
    st.info("Halaman riwayat tersedia di tab **🎯 Riwayat Prediksi** pada halaman Visualization.")
