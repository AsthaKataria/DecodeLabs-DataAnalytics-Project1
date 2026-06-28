# Data Cleaning & Preparation — DecodeLabs Internship, Project 1

E-commerce order data cleaned and audited for production readiness, completed as Project 1 of the DecodeLabs Data Analytics Industrial Training Kit (Batch 2026).

## Problem Statement

Raw transactional data is rarely analysis-ready. Before any dashboard or model can be trusted, the data must be checked for missing values, duplicate records, and inconsistent formatting. This project takes a raw 1,200-row e-commerce orders dataset and produces a verified, gold-standard cleaned version, with every change documented.

## Dataset

| | |
|---|---|
| Source | `data/raw/Dataset_for_Data_Analytics.xlsx` |
| Rows | 1,200 orders |
| Columns | OrderID, Date, CustomerID, Product, Quantity, UnitPrice, ShippingAddress, PaymentMethod, OrderStatus, TrackingNumber, ItemsInCart, CouponCode, ReferralSource, TotalPrice |

## Approach

1. **Duplicate audit** — checked all Order IDs and full rows for duplication
2. **Missing value handling** — `CouponCode` had 309 missing values (25.75%); imputed as the explicit category `"No Coupon"` rather than mean/median/mode, since the gap reflects a real business state (no coupon applied), not random missing data
3. **Format standardization** — dates converted to ISO 8601 (`YYYY-MM-DD`); currency fields rounded to 2 decimal places; text/ID fields trimmed and case-normalized
4. **Cross-validation** — recomputed `Quantity x UnitPrice` and checked it against `TotalPrice` for every row

## Results

| Check | Result |
|---|---|
| Duplicate Order IDs | 0 |
| Duplicate rows | 0 |
| Missing values (before) | 309 (CouponCode only) |
| Missing values (after) | 0 |
| Invalid date formats | 0 |
| TotalPrice calculation mismatches | 0 |

Meets the Project 2 verification gate: **0% error rate on unique identifiers and date formats.**

## Repo Structure

```
DecodeLabs-DataAnalytics-Project1/
├── data/
│   ├── raw/Dataset_for_Data_Analytics.xlsx          # original data
│   └── cleaned/Cleaned_Dataset_for_Data_Analytics.xlsx  # output
├── scripts/
│   └── clean_data.py        # reproducible cleaning pipeline
├── docs/
│   └── Change_Log_DecodeLabs_Project1.pdf  # audit / change log
├── requirements.txt
└── README.md
```

## How to Run

```bash
pip install -r requirements.txt
python scripts/clean_data.py
```

This regenerates `data/cleaned/Cleaned_Dataset_for_Data_Analytics.xlsx` and prints a JSON audit summary to the console.

## Tools

Python, pandas, openpyxl

## Author

Astha Kataria · [GitHub](https://github.com/AsthaKataria) · [LinkedIn](https://linkedin.com/in/asthakataria)
