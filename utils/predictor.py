import os
import pickle
import joblib          # FIX: lgbm_model.pkl & label_encoders.pkl disimpan dengan joblib
import pandas as pd
import numpy as np
import streamlit as st
from utils.preprocessing import build_features

UTILS_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR  = os.path.abspath(os.path.join(UTILS_DIR, ".."))

CLF_PATH = os.path.join(BASE_DIR, "model", "lgbm_model.pkl")
REG_PATH = os.path.join(BASE_DIR, "model", "xgboost_model.pkl")
ENC_PATH = os.path.join(BASE_DIR, "model", "label_encoders.pkl")

def _smart_load(path):
    """Coba pickle dulu, fallback ke joblib. Handles file disimpan dengan cara berbeda."""
    try:
        with open(path, "rb") as f:
            return pickle.load(f)
    except Exception:
        return joblib.load(path)

@st.cache_resource
def load_models():
    missing = [n for p, n in [(CLF_PATH, "lgbm_model.pkl"),
                               (REG_PATH, "xgboost_model.pkl"),
                               (ENC_PATH, "label_encoders.pkl")] if not os.path.exists(p)]
    if missing:
        raise FileNotFoundError(f"File model tidak ditemukan di folder 'model/': {', '.join(missing)}")

    clf_model      = _smart_load(CLF_PATH)   # joblib (LGBMClassifier)
    reg_model      = _smart_load(REG_PATH)   # pickle (XGBRegressor)
    label_encoders = _smart_load(ENC_PATH)   # joblib (dict of LabelEncoder)
    return clf_model, reg_model, label_encoders


def encode_features(df, encoders):
    df_encoded = df.copy()
    cat_cols = ["family", "city", "state", "type_x", "type_y", "locale", "transferred"]

    for col in cat_cols:
        if col in encoders:
            le      = encoders[col]
            val_str = str(df_encoded[col].iloc[0])
            df_encoded[col] = le.transform([val_str])[0] if val_str in le.classes_ else 0

    # Paksa tipe data numerik
    for col in cat_cols:
        df_encoded[col] = df_encoded[col].astype(int)

    for col in ["store_nbr", "cluster", "onpromotion",
                "day_of_week", "month", "day_of_month", "year", "week_of_year"]:
        df_encoded[col] = df_encoded[col].astype(int)

    for col in ["dcoilwtico", "sales_lag_1", "sales_lag_7", "sales_lag_14",
                "sales_rolling_mean_7", "sales_rolling_mean_14"]:
        df_encoded[col] = df_encoded[col].astype(float)

    return df_encoded


def _get_feature_names(model, fallback):
    if hasattr(model, "feature_name_"):
        return list(model.feature_name_)
    if hasattr(model, "feature_names_in_"):
        return list(model.feature_names_in_)
    return fallback


def predict_sales(store_nbr, family, date_input, onpromotion):
    # 1. Bangun fitur
    df_raw = build_features(store_nbr, family, date_input, onpromotion)

    # 2. Load model
    clf_model, reg_model, encoders = load_models()

    # 3. Encoding
    df_encoded = encode_features(df_raw, encoders)

    # 4. Deteksi nama fitur dari model
    clf_fallback = [
        "store_nbr", "family", "onpromotion", "city", "state", "type_x", "cluster",
        "dcoilwtico", "type_y", "locale", "transferred",
        "day_of_week", "month", "day_of_month", "year", "week_of_year"
    ]
    reg_fallback = clf_fallback + [
        "sales_lag_1", "sales_lag_7", "sales_lag_14",
        "sales_rolling_mean_7", "sales_rolling_mean_14"
    ]
    clf_features = _get_feature_names(clf_model, clf_fallback)
    reg_features = _get_feature_names(reg_model, reg_fallback)

    # === STAGE 1: KLASIFIKASI ===
    try:
        X_clf = df_encoded[clf_features]
    except KeyError as e:
        st.error("⚠️ Mismatch kolom pada Model Klasifikasi!")
        st.write(f"**Diminta model:** {clf_features}")
        st.write(f"**Tersedia:** {list(df_encoded.columns)}")
        raise e

    is_sold = clf_model.predict(X_clf)[0]
    if is_sold == 0:
        return {
            "terjual": False,
            "estimasi_unit": 0.0,
            "log_pred": 0.0,
            "klasifikasi": 0,
        }

    # === STAGE 2: REGRESI ===
    try:
        X_reg = df_encoded[reg_features]
    except KeyError as e:
        st.error("⚠️ Mismatch kolom pada Model Regresi!")
        st.write(f"**Diminta model:** {reg_features}")
        st.write(f"**Tersedia:** {list(df_encoded.columns)}")
        raise e

    log_sales_pred = reg_model.predict(X_reg)[0]
    sales_pred = max(0.0, float(np.expm1(log_sales_pred)))
    return {
        "terjual": True,
        "estimasi_unit": sales_pred,
        "log_pred": float(log_sales_pred),
        "klasifikasi": int(is_sold),
    }