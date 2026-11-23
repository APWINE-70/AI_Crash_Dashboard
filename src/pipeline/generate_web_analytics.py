"""
Generate Pre-aggregated Analytical JSON for Next.js / React Web Dashboard
Processes 194,726 clean crash records into optimized web JSON models.
"""

import os
import json
import numpy as np
import pandas as pd


def generate_web_data(parquet_path: str, output_json_path: str):
    print(f"Reading {parquet_path}...")
    df = pd.read_parquet(parquet_path)
    total = len(df)
    print(f"Loaded {total:,} rows.")

    # 1. Summary KPIs
    injury_count = int((df["ACRS Report Type"] == "Injury Crash").sum())
    fatal_count = int((df["ACRS Report Type"] == "Fatal Crash").sum())
    prop_damage_count = int((df["ACRS Report Type"] == "Property Damage Crash").sum())
    night_count = int(df["Is_Dark_Environment"].sum())
    off_peak_count = int(df["Is_Off_Peak_Target"].sum())

    summary = {
        "total_records": total,
        "injury_count": injury_count,
        "fatal_count": fatal_count,
        "property_damage_count": prop_damage_count,
        "severe_count": injury_count + fatal_count,
        "severe_rate": round(((injury_count + fatal_count) / total) * 100, 2),
        "fatal_rate": round((fatal_count / total) * 100, 2),
        "night_count": night_count,
        "night_rate": round((night_count / total) * 100, 2),
        "off_peak_target_count": off_peak_count,
        "off_peak_rate": round((off_peak_count / total) * 100, 2),
    }

    # 2. Monthly Trend Time Series
    monthly = (
        df.groupby(["Year", "Month", "Month_Name"])
        .agg(
            total=("Report Number", "count"),
            severe=("Is_Severe_Crash", "sum"),
            fatal=("Is_Fatal_Crash", "sum"),
        )
        .reset_index()
    )
    monthly_trend = []
    for _, r in monthly.iterrows():
        monthly_trend.append({
            "date": f"{int(r['Year'])}-{int(r['Month']):02d}",
            "label": f"{r['Month_Name']} {int(r['Year'])}",
            "year": int(r['Year']),
            "month": int(r['Month']),
            "total": int(r["total"]),
            "severe": int(r["severe"]),
            "fatal": int(r["fatal"]),
        })

    # 3. Heatmap: Day of Week vs Hour
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    heat_matrix = (
        df.groupby(["DayOfWeek", "Hour"])
        .size()
        .unstack(fill_value=0)
        .reindex(day_order)
    )
    heatmap_data = {
        "days": day_order,
        "hours": list(range(24)),
        "matrix": [[int(val) for val in heat_matrix.loc[d].tolist()] for d in day_order],
    }

    # 4. Q1: Driver Distraction
    dist_agg = (
        df.groupby("Driver Distracted By")
        .agg(
            total=("Report Number", "count"),
            severe=("Is_Severe_Crash", "sum"),
            fatal=("Is_Fatal_Crash", "sum"),
        )
        .reset_index()
    )
    dist_agg["severe_rate"] = (dist_agg["severe"] / dist_agg["total"]) * 100
    dist_agg["fatal_rate"] = (dist_agg["fatal"] / dist_agg["total"]) * 100
    avg_severe_rate = summary["severe_rate"]
    dist_agg["relative_risk"] = dist_agg["severe_rate"] / avg_severe_rate

    dist_list = []
    for _, r in dist_agg.sort_values(by="total", ascending=False).iterrows():
        dist_list.append({
            "behavior": str(r["Driver Distracted By"]),
            "total": int(r["total"]),
            "severe": int(r["severe"]),
            "fatal": int(r["fatal"]),
            "severe_rate": round(float(r["severe_rate"]), 2),
            "fatal_rate": round(float(r["fatal_rate"]), 2),
            "relative_risk": round(float(r["relative_risk"]), 2),
        })

    # 5. Q2: Environmental & Nighttime Impact
    # Daylight vs Dark
    day_df = df[~df["Is_Dark_Environment"]]
    night_df = df[df["Is_Dark_Environment"]]

    day_fatal_rate = round((day_df["Is_Fatal_Crash"].mean()) * 100, 2)
    night_fatal_rate = round((night_df["Is_Fatal_Crash"].mean()) * 100, 2)
    relative_jump = round(((night_fatal_rate - day_fatal_rate) / day_fatal_rate) * 100, 1)

    top_cols = df["Collision Type"].value_counts().head(7).index.tolist()
    collision_comparison = []
    for col_type in top_cols:
        day_c = int((day_df["Collision Type"] == col_type).sum())
        night_c = int((night_df["Collision Type"] == col_type).sum())
        collision_comparison.append({
            "type": col_type,
            "day_count": day_c,
            "night_count": night_c,
            "night_ratio": round((night_c / (day_c + night_c)) * 100, 1) if (day_c + night_c) > 0 else 0,
        })

    # Surface conditions during night
    surface_night = (
        night_df.groupby("Surface Condition")
        .agg(
            total=("Report Number", "count"),
            severe=("Is_Severe_Crash", "sum"),
            fatal=("Is_Fatal_Crash", "sum"),
        )
        .reset_index()
    )
    surface_night["severe_rate"] = (surface_night["severe"] / surface_night["total"]) * 100
    surface_night_list = []
    for _, r in surface_night[surface_night["total"] > 100].sort_values(by="severe_rate", ascending=False).iterrows():
        surface_night_list.append({
            "surface": str(r["Surface Condition"]),
            "total": int(r["total"]),
            "severe": int(r["severe"]),
            "fatal": int(r["fatal"]),
            "severe_rate": round(float(r["severe_rate"]), 2),
        })

    # 6. Q3: Off-Peak Hotspots (10:00 - 16:00)
    off_df = df[df["Is_Off_Peak_Target"]]
    top_roads_df = (
        off_df[off_df["Road Name"] != "UNKNOWN ROAD"]
        .groupby("Road Name")
        .agg(
            total=("Report Number", "count"),
            severe=("Is_Severe_Crash", "sum"),
            fatal=("Is_Fatal_Crash", "sum"),
        )
        .reset_index()
        .sort_values(by="total", ascending=False)
        .head(10)
    )
    top_roads_list = []
    top_road_names = top_roads_df["Road Name"].tolist()
    for _, r in top_roads_df.iterrows():
        top_roads_list.append({
            "road": str(r["Road Name"]),
            "total": int(r["total"]),
            "severe": int(r["severe"]),
            "fatal": int(r["fatal"]),
            "severe_rate": round((r["severe"] / r["total"]) * 100, 2),
        })

    # Traffic controls on top roads
    tc_on_top = (
        off_df[off_df["Road Name"].isin(top_road_names)]
        .groupby("Traffic Control")
        .size()
        .reset_index(name="count")
        .sort_values(by="count", ascending=False)
        .head(6)
    )
    tc_list = []
    for _, r in tc_on_top.iterrows():
        tc_list.append({
            "control": str(r["Traffic Control"]),
            "count": int(r["count"]),
        })

    # 7. Data Dictionary
    dict_csv = r"C:\adisak\AI\data\processed\data_dictionary.csv"
    dict_list = []
    if os.path.exists(dict_csv):
        df_d = pd.read_csv(dict_csv)
        for _, r in df_d.iterrows():
            dict_list.append({
                "field": str(r["Field_Name"]),
                "type": str(r["Data_Type"]),
                "missing_pct": float(r["Missing_Percent"]),
                "description": str(r["Description"]),
                "sample": str(r["Sample_Values"]),
            })

    # 8. Sample Records (500 rows)
    sample_cols = [
        "Report Number", "Crash Date/Time", "ACRS Report Type", "Injury Severity",
        "Road Name", "Collision Type", "Weather", "Surface Condition",
        "Driver Distracted By", "Traffic Control", "Speed_Limit_Cleaned", "Year"
    ]
    sample_df = df[sample_cols].head(500)
    sample_records = sample_df.to_dict(orient="records")

    payload = {
        "summary": summary,
        "monthly_trend": monthly_trend,
        "heatmap": heatmap_data,
        "q1_distraction": dist_list,
        "q2_environment": {
            "day_fatal_rate": day_fatal_rate,
            "night_fatal_rate": night_fatal_rate,
            "relative_jump": relative_jump,
            "collision_comparison": collision_comparison,
            "surface_night": surface_night_list,
        },
        "q3_off_peak": {
            "top_roads": top_roads_list,
            "traffic_controls": tc_list,
        },
        "data_dictionary": dict_list,
        "sample_records": sample_records,
    }

    os.makedirs(os.path.dirname(output_json_path), exist_ok=True)
    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    size_kb = os.path.getsize(output_json_path) / 1024
    print(f"Generated {output_json_path} successfully ({size_kb:.2f} KB)!")


if __name__ == "__main__":
    parquet_in = r"C:\adisak\AI\data\processed\clean_crash_reports.parquet"
    json_out = r"C:\adisak\AI\public\data\web_analytics.json"
    generate_web_data(parquet_in, json_out)
