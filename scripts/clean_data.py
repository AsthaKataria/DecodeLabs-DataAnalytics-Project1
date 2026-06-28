"""
Data Cleaning & Preparation - DecodeLabs Internship Project 1
Author: Astha Kataria

Cleans the raw e-commerce orders dataset:
  1. Removes duplicate records (by OrderID and full-row)
  2. Handles missing values (CouponCode -> "No Coupon")
  3. Standardizes date format to ISO 8601
  4. Enforces 2-decimal precision on currency fields
  5. Trims/normalizes text and ID fields
  6. Cross-validates Quantity * UnitPrice against TotalPrice

Run:
    python scripts/clean_data.py
Output:
    data/cleaned/Cleaned_Dataset_for_Data_Analytics.xlsx
"""

import json
import os
import pandas as pd

RAW_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "raw", "Dataset_for_Data_Analytics.xlsx")
OUT_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "cleaned", "Cleaned_Dataset_for_Data_Analytics.xlsx")


def clean(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    report = {"total_rows_before": len(df)}

    # 1. Duplicate audit
    report["duplicate_order_ids"] = int(df["OrderID"].duplicated().sum())
    report["full_duplicate_rows"] = int(df.duplicated().sum())
    df = df.drop_duplicates(subset="OrderID", keep="first")
    df = df.drop_duplicates(keep="first")

    # 2. Missing values
    report["missing_before"] = df.isnull().sum().to_dict()
    df["CouponCode"] = df["CouponCode"].fillna("No Coupon")
    report["missing_after"] = df.isnull().sum().to_dict()

    # 3. Text standardization
    text_cols = ["Product", "ShippingAddress", "PaymentMethod", "OrderStatus", "CouponCode", "ReferralSource"]
    for c in text_cols:
        df[c] = df[c].astype(str).str.strip()
    for c in ["OrderID", "CustomerID", "TrackingNumber"]:
        df[c] = df[c].astype(str).str.strip().str.upper()

    # 4. Date standardization -> ISO 8601
    df["Date"] = pd.to_datetime(df["Date"]).dt.date

    # 5. Numeric precision
    df["UnitPrice"] = df["UnitPrice"].round(2)
    df["TotalPrice"] = df["TotalPrice"].round(2)

    # 6. Cross-validate TotalPrice
    calc = (df["Quantity"] * df["UnitPrice"]).round(2)
    mismatches = (calc - df["TotalPrice"]).abs() > 0.01
    report["total_price_mismatches"] = int(mismatches.sum())

    report["total_rows_after"] = len(df)
    return df, report


if __name__ == "__main__":
    raw_df = pd.read_excel(RAW_PATH)
    cleaned_df, audit_report = clean(raw_df)
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    cleaned_df.to_excel(OUT_PATH, index=False)
    print(json.dumps(audit_report, indent=2, default=str))
