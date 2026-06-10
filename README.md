<<<<<<< HEAD
# UAS Data Mining — NamaKelompok

Aplikasi prediksi berbasis **Streamlit** untuk Ujian Akhir Semester Data Mining.

## 📁 Struktur Folder

```
UAS_DataMining_NamaKelompok/
├── dataset/                  ← Letakkan file CSV di sini
├── notebook/
│   └── analysis.ipynb        ← Notebook EDA & pelatihan model
├── model/
│   ├── model.pkl             ← Model terlatih (di-generate dari notebook)
│   └── features.json         ← Metadata fitur (di-generate dari notebook)
└── app/
    ├── app.py                ← Entry point Streamlit
    ├── pages/
    │   ├── home.py
    │   ├── eda.py
    │   ├── prediction.py
    │   ├── evaluation.py
    │   └── about.py
    └── assets/
        └── style.css
```

## 🚀 Cara Menjalankan

### 1. Install Dependencies

```bash
pip install streamlit scikit-learn pandas numpy matplotlib seaborn
```

### 2. Siapkan Dataset

Letakkan file CSV dataset di folder `dataset/`, contoh: `dataset/data.csv`

### 3. Latih Model

Jalankan notebook `notebook/analysis.ipynb` dari awal hingga akhir.  
Notebook akan otomatis menyimpan `model/model.pkl` dan `model/features.json`.

### 4. Jalankan Aplikasi

```bash
cd app
streamlit run app.py
```

Aplikasi akan terbuka di browser: `http://localhost:8501`

## 📋 Fitur Aplikasi

| Halaman | Deskripsi |
|---------|-----------|
| 🏠 Beranda | Halaman utama & petunjuk penggunaan |
| 📊 Eksplorasi Data | Pratinjau dataset, statistik, missing values, distribusi |
| 🤖 Prediksi | Input fitur → hasil prediksi + probabilitas |
| 📈 Evaluasi Model | Akurasi, confusion matrix, classification report |
| ℹ️ Tentang | Info kelompok & teknologi |
=======
# klasifikasi-dan-regresi-penjualan-produk-kelompok-1
>>>>>>> 95c9f95f9236e2ae7341d7968d68c52a2a1cbe4f
