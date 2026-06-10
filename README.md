# Two-Stage Modeling untuk Prediksi Penjualan pada Perusahaan Ritel

## Project Overview

Ketidakakuratan prediksi penjualan pada perusahaan ritel berskala besar dapat mengakibatkan *overstock* maupun *stockout* yang berdampak langsung pada biaya operasional dan kepuasan pelanggan. Tantangan ini semakin kompleks pada dataset ritel yang memiliki proporsi nilai nol (*zero-sales*) yang tinggi — di mana model regresi tunggal (*single-regime*) cenderung menghasilkan prediksi yang bias karena tidak memisahkan kondisi "ada penjualan" dan "tidak ada penjualan".

Penelitian ini menerapkan pendekatan **two-stage modeling** pada dataset [Corporación Favorita Grocery Sales Forecasting](https://www.kaggle.com/competitions/favorita-grocery-sales-forecasting) dari Kaggle. Pendekatan ini memisahkan proses prediksi menjadi dua tahap berurutan:

1. **Stage 1 — Klasifikasi**: Memprediksi apakah suatu kombinasi toko, produk, dan tanggal akan menghasilkan penjualan (*is_sold*).
2. **Stage 2 — Regresi**: Memprediksi jumlah penjualan aktual hanya pada kombinasi yang diprediksi memiliki penjualan.

Pendekatan ini terbukti lebih unggul dibandingkan regresi tunggal, sejalan dengan penelitian Rožanec & Mladenić (2022) yang menunjukkan peningkatan akurasi signifikan pada data dengan pola *intermittent demand*, serta Purnomo et al. (2026) yang membuktikan penurunan MAE dari 0,193 (single-regime) menjadi 0,136 (two-stage).

**Referensi Utama**:
- [1] Rožanec, J. M., Fortuna, B., & Mladenić, D., "Reframing Demand Forecasting: A Two-Fold Approach for Lumpy and Intermittent Demand," *Sustainability*, vol. 14, no. 15, hal. 9295, 2022.
- [2] Purnomo, S., et al., "From zero sales to survival: Forecast-triggered decision-making in ecotourism MSMEs," *Shirkah: Journal of Economics and Business*, vol. 11, no. 1, hal. 1–19, 2026.
- [3] Wang, C.-C., "Dynamic Dual-Phase Forecasting Model for New Product Demand Using Machine Learning and Statistical Control," *Mathematics*, vol. 13, no. 10, hal. 1613, 2025.

## Business Understanding

### Problem Statements

- Bagaimana cara membangun model yang mampu memprediksi apakah suatu produk akan terjual pada toko dan tanggal tertentu?
- Bagaimana cara memprediksi jumlah penjualan secara akurat pada produk yang diprediksi akan terjual?
- Fitur apa saja yang paling berpengaruh terhadap keputusan model, termasuk apakah faktor ekonomi makro seperti harga minyak mentah memengaruhi pola pembelian konsumen di Ekuador?

### Goals

- Mengimplementasikan pendekatan *two-stage modeling* yang menggabungkan model klasifikasi dan regresi secara berurutan.
- Membandingkan beberapa algoritma pada masing-masing tahap untuk menemukan model terbaik.
- Menerapkan analisis SHAP untuk menginterpretasi kontribusi setiap fitur terhadap prediksi model (*explainability*).

### Solution Statements

- **Stage 1**: Melatih dan membandingkan Logistic Regression, Random Forest, XGBoost, LightGBM, dan CatBoost untuk klasifikasi `is_sold`. Model terbaik dipilih berdasarkan F1-Score dan Recall.
- **Stage 2**: Melatih dan membandingkan Linear Regression, Random Forest, Decision Tree, dan XGBoost untuk regresi jumlah `sales`. Model terbaik dipilih berdasarkan RMSE, MAE, R², dan MAPE.
- Output dari Stage 1 (prediksi `is_sold = 1`) digunakan sebagai filter input Stage 2.

## Data Understanding

Dataset: [Corporación Favorita Grocery Sales Forecasting — Kaggle](https://www.kaggle.com/competitions/favorita-grocery-sales-forecasting)

Dataset berisi data historis penjualan ratusan toko ritel Corporación Favorita di Ekuador. Terdiri dari beberapa file yang digabungkan menjadi satu dataframe:

| File | Jumlah Baris | Deskripsi |
|---|---|---|
| `train.csv` | ~125 juta | Data historis penjualan per toko, produk, dan tanggal |
| `test.csv` | ~3,4 juta | Data untuk prediksi akhir |
| `transactions.csv` | ~83 ribu | Jumlah transaksi per toko per hari |
| `stores.csv` | 54 | Informasi toko (kota, tipe, kluster) |
| `oil.csv` | ~1.219 | Harga minyak mentah harian (*dcoilwtico*) |
| `holidays_events.csv` | 350 | Hari libur nasional, regional, lokal, dan event khusus |

Berikut adalah atribut dataset setelah proses merge:

| No | Atribut | Deskripsi |
|---|---|---|
| 1 | `id` | Kode unik setiap transaksi |
| 2 | `date` | Tanggal transaksi |
| 3 | `store_nbr` | Kode unik toko |
| 4 | `family` | Kategori produk |
| 5 | `sales` | Jumlah penjualan produk (target regresi) |
| 6 | `onpromotion` | Jumlah produk yang sedang dalam promosi |
| 7 | `city` | Kota lokasi toko |
| 8 | `state` | Provinsi/wilayah toko |
| 9 | `type_x` | Tipe/kategori toko |
| 10 | `cluster` | Kelompok toko berdasarkan karakteristik tertentu |
| 11 | `transactions` | Jumlah transaksi per toko per hari |
| 12 | `dcoilwtico` | Harga minyak mentah harian |
| 13 | `type_y` | Tipe event/hari libur |
| 14 | `locale` | Cakupan hari libur (nasional/regional/lokal) |
| 15 | `transferred` | Status hari libur yang dipindahkan |

## Data Preparation

### 1. Penanganan Missing Values

Kolom event yang kosong (hari tanpa event) diisi dengan nilai default:

```python
df['type_y']      = df['type_y'].fillna('None')
df['locale']      = df['locale'].fillna('None')
df['transferred'] = df['transferred'].fillna('False')
```

Harga minyak menggunakan forward fill + backward fill untuk mengisi hari-hari libur/akhir pekan yang tidak memiliki data:

```python
df['dcoilwtico'] = df['dcoilwtico'].ffill().bfill()
```

### 2. Feature Selection

Kolom yang dihapus beserta alasannya:

| Kolom | Alasan |
|---|---|
| `id` | Tidak informatif secara prediktif |
| `description` | 93 nilai unik, terlalu granular |
| `locale_name` | Sudah terwakili oleh `locale` |
| `transactions` | Data leakage (tidak tersedia pada data test) |
| `sales` | Hanya digunakan di Stage 2; dihapus di Stage 1 untuk menghindari leakage |

### 3. Pembuatan Label Biner (Stage 1)

```python
df['is_sold'] = (df['sales'] > 0).astype(int)
# is_sold = 1 → ada penjualan (sales > 0)
# is_sold = 0 → tidak ada penjualan (sales = 0)
```

### 4. Feature Engineering

**Fitur Waktu:**

```python
df['day_of_week']  = df['date'].dt.dayofweek
df['month']        = df['date'].dt.month
df['day_of_month'] = df['date'].dt.day
df['year']         = df['date'].dt.year
df['week_of_year'] = df['date'].dt.isocalendar().week.astype(int)
```

**Lag Features & Rolling Statistics** (khusus Stage 2):

Fitur historis penjualan dihitung per kombinasi `store_nbr` + `family` untuk menangkap pola temporal:

```python
df['sales_lag_1']  = df.groupby(['store_nbr', 'family'])['sales'].shift(1)
df['sales_lag_7']  = df.groupby(['store_nbr', 'family'])['sales'].shift(7)
df['sales_lag_14'] = df.groupby(['store_nbr', 'family'])['sales'].shift(14)

df['sales_rolling_mean_7']  = df.groupby(['store_nbr', 'family'])['sales'] \
                                .transform(lambda x: x.shift(1).rolling(7).mean())
df['sales_rolling_mean_14'] = df.groupby(['store_nbr', 'family'])['sales'] \
                                .transform(lambda x: x.shift(1).rolling(14).mean())
```

Lag features mengambil nilai penjualan pada T−1, T−7, dan T−14, sedangkan rolling statistics menghitung rata-rata penjualan dalam jendela 7 dan 14 hari terakhir. Keduanya menggunakan `.shift(1)` untuk menghindari data leakage.

**Transformasi Target (Stage 2):**

Target `sales` ditransformasikan ke skala logaritmik untuk mengatasi distribusi yang sangat skewed:

```python
y_train = np.log1p(df[df['date'] < cutoff]['sales'])
# Prediksi akhir dikembalikan: np.expm1(y_pred)
```

### 5. Train/Test Split (Time-Based)

Pemisahan data menggunakan time-based split untuk menghindari data leakage temporal:

- **Training set**: 1 Januari 2013 – 31 Mei 2017 (~85% data)
- **Testing set**: 1 Juni 2017 – 15 Agustus 2017 (~15% data)

```python
cutoff = pd.Timestamp('2017-06-01')
```

## Modeling

### Stage 1 — Klasifikasi (`is_sold`)

Lima algoritma dilatih dan dibandingkan:

- **Logistic Regression** — baseline linear, menggunakan pipeline dengan `OneHotEncoder` + `StandardScaler` dan `RandomizedSearchCV` untuk tuning hyperparameter `C` dan `class_weight`.
- **Random Forest** — `n_estimators=100`, `max_depth=10`, `min_samples_leaf=50`.
- **LightGBM** — `n_estimators=300`, `learning_rate=0.05`, `num_leaves=31`, `min_child_samples=50`, dengan early stopping.
- **XGBoost** — `n_estimators=300`, `learning_rate=0.05`, `max_depth=6`, dengan early stopping.
- **CatBoost** — `iterations=300`, `learning_rate=0.05`, `depth=6`, `eval_metric='F1'`, dengan early stopping.

### Stage 2 — Regresi (`sales`)

Empat algoritma dilatih dan dibandingkan (hanya pada baris dengan `sales > 0`):

- **Linear Regression** — baseline, menggunakan pipeline dengan `OneHotEncoder`.
- **Random Forest** — `n_estimators=100`, `max_depth=10`, `min_samples_leaf=50`.
- **Decision Tree** — `max_depth=10`, `min_samples_leaf=50`.
- **XGBoost** — `n_estimators=300`, `learning_rate=0.05`, `max_depth=6`, `min_child_weight=50`, `tree_method='hist'`, dengan early stopping.

## Evaluation

### Stage 1 — Hasil Evaluasi Klasifikasi

Metrik: Accuracy, Recall, dan F1-Score

| Algoritma | Set | Accuracy | Recall | F1-Score |
|---|---|---|---|---|
| Logistic Regression | Test | 0.90 | 0.97 | 0.94 |
| | Train | 0.85 | 0.91 | 0.89 |
| Random Forest | Test | 0.89 | 0.97 | 0.94 |
| | Train | 0.85 | 0.96 | 0.90 |
| XGBoost | Test | 0.96 | 0.97 | 0.96 |
| | Train | 0.92 | 0.96 | 0.94 |
| CatBoost | Test | 0.93 | 0.95 | 0.96 |
| | Train | 0.94 | 0.96 | 0.95 |
| **LightGBM** | **Test** | **0.94** | **0.98** | **0.97** |
| | Train | 0.94 | 0.97 | 0.96 |

**Model terbaik: LightGBM** — dipilih berdasarkan F1-Score tertinggi (0.97) dan Recall tertinggi (0.98). Meskipun XGBoost memiliki Accuracy lebih tinggi (0.96), F1-Score dianggap lebih penting karena mengukur keseimbangan antara kemampuan mendeteksi penjualan dan ketepatan prediksi. Seluruh model tidak mengalami overfitting, dengan selisih accuracy train-test berkisar 0.10%–0.39%.

**SHAP Feature Importance (LightGBM):** Fitur `onpromotion` merupakan faktor paling dominan, diikuti `family`, `year`, `store_nbr`, `type_x`, `city`, dan `dcoilwtico`. Kehadiran `dcoilwtico` menunjukkan bahwa kondisi ekonomi makro Ekuador yang dipengaruhi industri perminyakan berpengaruh terhadap perilaku pembelian konsumen.

### Stage 2 — Hasil Evaluasi Regresi

Metrik: RMSE, MAE, R², MAPE (prediksi dikembalikan ke skala asli dengan `expm1`)

| Algoritma | RMSE | MAE | R² | MAPE |
|---|---|---|---|---|
| Linear Regression | 6739.05 | 630.89 | -21.38 | 0.77 |
| Decision Tree | 291.15 | 83.22 | 0.95 | 0.36 |
| Random Forest | 273.84 | 77.53 | 0.96 | 0.35 |
| **XGBoost** | **246.21** | **68.69** | **0.97** | **0.33** |

**Model terbaik: XGBoost** — RMSE terendah (246.21), MAE terendah (68.69), R² tertinggi (0.97), dan MAPE terendah (0.33). Linear Regression menghasilkan R² = −21.38 yang mengkonfirmasi bahwa pola penjualan bersifat nonlinear, sehingga model berbasis pohon keputusan (*tree-based*) jauh lebih sesuai.

**SHAP Feature Importance (XGBoost):** Fitur historis penjualan mendominasi — `sales_rolling_mean_7`, `sales_lag_1`, `sales_lag_7`, dan `sales_lag_14` merupakan faktor utama. Fitur `onpromotion` berpengaruh namun dengan magnitude lebih kecil dibanding fitur lag. Fitur temporal `day_of_week` dan `day_of_month` menunjukkan adanya pola musiman. Fitur `dcoilwtico` turut muncul sebagai fitur penting, mengindikasikan hubungan antara harga minyak dan pola konsumsi masyarakat Ekuador.

## Conclusion

1. Pendekatan *two-stage modeling* berhasil diimplementasikan dengan menggabungkan model klasifikasi (Stage 1) dan regresi (Stage 2) secara berurutan untuk memprediksi penjualan pada dataset Corporación Favorita.

2. Pada Stage 1, **LightGBM** terpilih sebagai model terbaik dengan F1-Score 97% dan Recall 98%, menunjukkan kemampuan optimal dalam mendeteksi kejadian penjualan dan meminimalkan risiko *false negative* yang dapat menyebabkan hilangnya peluang penjualan.

3. Pada Stage 2, **XGBoost** terpilih sebagai model terbaik dengan RMSE 246.21, MAE 68.69, R² 0.97, dan MAPE 0.33. Nilai R² Linear Regression yang mencapai −21.38 menegaskan bahwa hubungan antarvariabel tidak bersifat linear sehingga model berbasis pohon lebih tepat digunakan.

4. Analisis SHAP mengungkap bahwa fitur historis penjualan (*rolling mean* dan *lag features*) merupakan faktor paling berpengaruh pada Stage 2, sedangkan fitur promosi (`onpromotion`) dan karakteristik toko paling berpengaruh pada Stage 1. Harga minyak mentah (`dcoilwtico`) terbukti berpengaruh pada kedua tahap, mengindikasikan adanya hubungan antara kondisi ekonomi makro Ekuador dan perilaku konsumsi masyarakat.

5. Model diimplementasikan ke dalam aplikasi peramalan penjualan berbasis **Streamlit** untuk mendukung pengambilan keputusan operasional secara langsung oleh pengguna.

## Requirements

```
pandas
numpy
scikit-learn
lightgbm
xgboost
catboost
shap
matplotlib
seaborn
joblib
```

Install semua dependency:

```bash
pip install pandas numpy scikit-learn lightgbm xgboost catboost shap matplotlib seaborn joblib
```

Notebook dijalankan di **Google Colab** dengan data tersimpan di Google Drive pada path `/content/drive/MyDrive/Data Mining/`.

## Dataset

Dataset dapat diakses secara publik melalui Kaggle:
[https://www.kaggle.com/competitions/favorita-grocery-sales-forecasting](https://www.kaggle.com/competitions/favorita-grocery-sales-forecasting)

## Referensi

- Fildes, R., Ma, S., & Kolassa, S., "Retail forecasting: Research and practice," *International Journal of Forecasting*, vol. 38, no. 4, pp. 1283–1318, 2022.
- Rožanec, J. M., Fortuna, B., & Mladenić, D., "Reframing Demand Forecasting: A Two-Fold Approach for Lumpy and Intermittent Demand," *Sustainability*, vol. 14, no. 15, hal. 9295, 2022.
- Purnomo, S., Nurmalitasari, Nurchim, & Nugroho, N. T., "From zero sales to survival: Forecast-triggered decision-making in ecotourism MSMEs," *Shirkah: Journal of Economics and Business*, vol. 11, no. 1, hal. 1–19, 2026.
- Wang, C.-C., "Dynamic Dual-Phase Forecasting Model for New Product Demand Using Machine Learning and Statistical Control," *Mathematics*, vol. 13, no. 10, hal. 1613, 2025.
- Chen, T. & Guestrin, C., "XGBoost: A Scalable Tree Boosting System," *Proc. KDD'16*, 2016, hal. 785–794.
- Lundberg, S. & Lee, S.-I., "A Unified Approach to Interpreting Model Predictions," *NeurIPS*, hal. 4768–4777, 2017.
- Cerqueira, V., Moniz, N., & Soares, C., "VEST: automatic feature engineering for forecasting," *Machine Learning*, vol. 113, hal. 4523–4545, 2024.
