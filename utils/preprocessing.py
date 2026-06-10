import os
import pandas as pd
import numpy as np
from datetime import timedelta   # BUG FIX: timedelta was used but never imported

# Jalur berdasarkan posisi file ini (utils/)
UTILS_DIR  = os.path.dirname(os.path.abspath(__file__))
BASE_DIR   = os.path.abspath(os.path.join(UTILS_DIR, ".."))

# BUG FIX: folder was "data" but actual folder is "dataset"
STORES_PATH   = os.path.join(BASE_DIR, "dataset", "stores.csv")
OIL_PATH      = os.path.join(BASE_DIR, "dataset", "oil.csv")
HOLIDAYS_PATH = os.path.join(BASE_DIR, "dataset", "holidays_events.csv")
TRAIN_PATH    = os.path.join(BASE_DIR, "dataset", "train.csv")

# Cache datasets agar tidak dibaca ulang setiap prediksi
_cache = {}

def load_datasets():
    """Load dan cache semua dataset pendukung."""
    if _cache:
        return _cache["stores"], _cache["oil"], _cache["event"], _cache["train"]

    stores = pd.read_csv(STORES_PATH)

    oil = pd.read_csv(OIL_PATH, parse_dates=["date"])
    oil = oil.sort_values("date").reset_index(drop=True)

    event = pd.read_csv(HOLIDAYS_PATH, parse_dates=["date"])

    # BUG FIX: train.csv is 121MB — only load needed columns to save memory
    train = pd.read_csv(
        TRAIN_PATH,
        usecols=["date", "store_nbr", "family", "sales"],
        parse_dates=["date"],
        dtype={"store_nbr": "int16", "sales": "float32"}
    )

    _cache["stores"] = stores
    _cache["oil"]    = oil
    _cache["event"]  = event
    _cache["train"]  = train

    return stores, oil, event, train


def build_features(store_nbr, family, date_input, onpromotion):
    # BUG FIX: function previously called load_datasets() which was undefined,
    # AND also tried to read stores/oil/event twice (once directly, once via load_datasets)
    stores, oil, event, train = load_datasets()

    date_dt = pd.to_datetime(date_input)

    # --- 1. Ekstrak Waktu ---
    day_of_week  = date_dt.dayofweek
    month        = date_dt.month
    day_of_month = date_dt.day
    year         = date_dt.year
    week_of_year = date_dt.isocalendar().week

    # --- 2. Lookup Store ---
    store_info = stores[stores["store_nbr"] == store_nbr]
    if not store_info.empty:
        city   = store_info["city"].values[0]
        state  = store_info["state"].values[0]
        type_x = store_info["type"].values[0]
        cluster = int(store_info["cluster"].values[0])
    else:
        city, state, type_x, cluster = "Unknown", "Unknown", "Unknown", 0

    # --- 3. Lookup Oil (lag 1 hari) ---
    date_yesterday = date_dt - timedelta(days=1)
    oil_past = oil[oil["date"] <= date_yesterday].dropna(subset=["dcoilwtico"])
    if not oil_past.empty:
        dcoilwtico = float(oil_past["dcoilwtico"].iloc[-1])
    else:
        dcoilwtico = float(oil["dcoilwtico"].mean())

    # --- 4. Lookup Events ---
    event_day = event[event["date"] == date_dt]
    if not event_day.empty:
        # BUG FIX: original code used "type_y" but holidays_events.csv has column "type"
        type_y     = str(event_day["type"].values[0])
        locale     = str(event_day["locale"].values[0])
        transferred = str(event_day["transferred"].values[0])
    else:
        type_y, locale, transferred = "None", "None", "False"

    # --- 5. Lookup Historical Sales untuk Lag Features ---
    past_sales = train[
        (train["store_nbr"] == store_nbr) &
        (train["family"] == family) &
        (train["date"] < date_dt)
    ].sort_values("date")

    sales_lag_1 = sales_lag_7 = sales_lag_14 = 0.0
    sales_rolling_mean_7 = sales_rolling_mean_14 = 0.0

    if len(past_sales) >= 1:
        sales_lag_1 = float(past_sales["sales"].iloc[-1])
    if len(past_sales) >= 7:
        sales_lag_7          = float(past_sales["sales"].iloc[-7])
        sales_rolling_mean_7 = float(past_sales["sales"].iloc[-7:].mean())
    if len(past_sales) >= 14:
        sales_lag_14          = float(past_sales["sales"].iloc[-14])
        sales_rolling_mean_14 = float(past_sales["sales"].iloc[-14:].mean())

    # --- 6. Satukan menjadi DataFrame ---
    features = {
        "store_nbr":             [store_nbr],
        "family":                [family],
        "onpromotion":           [1 if onpromotion in ["Ya", "Yes", 1, True] else 0],
        "city":                  [city],
        "state":                 [state],
        "type_x":                [type_x],
        "cluster":               [cluster],
        "dcoilwtico":            [dcoilwtico],
        "type_y":                [type_y],
        "locale":                [locale],
        "transferred":           [transferred],
        "day_of_week":           [day_of_week],
        "month":                 [month],
        "day_of_month":          [day_of_month],
        "year":                  [year],
        "week_of_year":          [week_of_year],
        "sales_lag_1":           [sales_lag_1],
        "sales_lag_7":           [sales_lag_7],
        "sales_lag_14":          [sales_lag_14],
        "sales_rolling_mean_7":  [sales_rolling_mean_7],
        "sales_rolling_mean_14": [sales_rolling_mean_14],
    }

    return pd.DataFrame(features)
