# Data Cleaning & Reconciliation Audit Report
**Execution Timestamp**: 2026-11-22 20:09:21
**Source Dataset**: `C:\adisak\2_provincial_crash_practice.csv`
**Processed Output**: `C:\adisak\AI\data\processed\clean_crash_reports.parquet`

---

## 1. Volume & Completeness Audit
- **Total Initial Records**: 194,726 rows
- **Total Final Records**: 194,726 rows (100% record retention, zero drop)
- **Primary Key (`Report Number`) Uniqueness**: 194,726 / 194,726 (100.0% Unique, Zero duplicates)
- **Total Columns**: 39 initial $\rightarrow$ 55 final (+16 engineered features)

---

## 2. Missing Value Imputation Reconciliation

| Field Name | Missing Before (Count) | % Before | Missing After (Count) | % After | Imputation Strategy |
| :--- | :---: | :---: | :---: | :---: | :--- |
| `Driver Substance Abuse` | 21,416 | 11.00% | 0 | 0.00% | Imputed as `'UNKNOWN'` |
| `Driver At Fault` | 7,715 | 3.96% | 0 | 0.00% | Imputed as `'UNKNOWN'` |
| `Driver Distracted By` | 0 | 0.00% | 0 | 0.00% | Imputed as `'UNKNOWN'` |
| `Weather` | 13,656 | 7.01% | 0 | 0.00% | Imputed as `'UNKNOWN / NOT REPORTED'` |
| `Surface Condition` | 19,441 | 9.98% | 0 | 0.00% | Imputed as `'UNKNOWN / NOT REPORTED'` |
| `Traffic Control` | 25,429 | 13.06% | 0 | 0.00% | Imputed as `'UNKNOWN / NOT REPORTED'` |

---

## 3. Outlier Mitigation Reconciliation

### A. Vehicle Year
- **Initial Range**: Min `0`, Max `9999`
- **Anomalous Records Detected**: 2,336 records (1.20%)
- **Mitigation Method**: Placed in `Vehicle_Year_Cleaned` with invalid years (<=1960 or >2025) transformed to null, and `Vehicle_Age` capped at [0, 45] for valid years.
- **Valid Vehicle Age Statistics**: Mean 9.2 years, Median 9.0 years.

### B. Speed Limit
- **Initial Range**: Min `0`, Max `65`
- **Zero Speed Records**: 2,920 records (1.50%)
- **Mitigation Method**: Maintained original `Speed Limit` for auditability; created `Speed_Limit_Cleaned` where 0 mph is imputed with median route type speed (Median: 35 mph).
- **Cleaned Speed Limit Statistics**: Mean 37.5 mph, Median 35.0 mph.

---

## 4. Derived Target Metrics
- **Property Damage Crashes**: 131,786 (67.68%)
- **Injury Crashes**: 61,566 (31.62%)
- **Fatal Crashes**: 1,374 (0.71%)
- **Nighttime Crashes**: 48,767 (25.04%)
- **Target Off-Peak Crashes (10 AM - 4 PM)**: 63,574 (32.65%)

Pipeline completed in 26.20 seconds.
