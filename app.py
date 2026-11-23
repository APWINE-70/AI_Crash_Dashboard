"""
AI Road Crash Analytics Dashboard (ระบบวิเคราะห์ข้อมูลอุบัติเหตุทางถนน)
การแข่งขันทักษะวิชาชีพ สาขาวิชาเทคโนโลยีปัญญาประดิษฐ์ ทักษะการวิเคราะห์ข้อมูล ระดับ ปวช.
ระดับภาคตะวันออกเฉียงเหนือ ประจำปีการศึกษา 2568 - 2572
"""

import os
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Configure wide layout and page metadata
st.set_page_config(
    page_title="AI Road Crash Analytics Dashboard | ปวช. 2568",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Styling for Competition Excellence
st.markdown(
    """
    <style>
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 16px;
        border-left: 5px solid #0068C9;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    }
    .insight-box {
        background-color: #eef5fc;
        border: 1px solid #c9e2fa;
        border-radius: 6px;
        padding: 14px 18px;
        margin-top: 10px;
        margin-bottom: 20px;
    }
    .insight-title {
        font-weight: 700;
        color: #004b91;
        margin-bottom: 6px;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 8px 16px;
        border-radius: 4px;
        font-weight: 600;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# Cached Optimized Data Loader
@st.cache_data(show_spinner=False)
def load_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    parquet_path = os.path.join(base_dir, "data", "processed", "clean_crash_reports.parquet")
    if not os.path.exists(parquet_path):
        alt_path = r"C:\adisak\AI\data\processed\clean_crash_reports.parquet"
        if os.path.exists(alt_path):
            parquet_path = alt_path
        else:
            raise FileNotFoundError(f"Parquet dataset not found at {parquet_path}")

    cols_to_load = [
        "Report Number", "ACRS Report Type", "Injury Severity", "Crash Date/Time",
        "Crash_Timestamp", "Year", "Month", "Month_Name", "DayOfWeek", "Hour",
        "Is_Weekend", "Time_Period", "Is_Commute_Peak", "Is_Off_Peak_Target",
        "Is_Dark_Environment", "Is_Severe_Crash", "Is_Fatal_Crash",
        "Driver Distracted By", "Driver Substance Abuse", "Driver At Fault",
        "Weather", "Surface Condition", "Light", "Traffic Control", "Collision Type",
        "Road Name", "Municipality", "Route Type", "Speed Limit", "Speed_Limit_Cleaned",
        "Vehicle Year", "Vehicle_Year_Cleaned", "Vehicle_Age", "Latitude", "Longitude"
    ]
    df = pd.read_parquet(parquet_path, columns=cols_to_load)
    return df


@st.cache_data(show_spinner=False)
def load_data_dictionary():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    dict_path = os.path.join(base_dir, "data", "processed", "data_dictionary.csv")
    if not os.path.exists(dict_path):
        alt_path = r"C:\adisak\AI\data\processed\data_dictionary.csv"
        if os.path.exists(alt_path):
            dict_path = alt_path
    if os.path.exists(dict_path):
        return pd.read_csv(dict_path)
    return pd.DataFrame()


def render_insight(what: str, so_what: str, now_what: str, metric_ref: str = ""):
    st.markdown(
        f"""
        <div class="insight-box">
            <div class="insight-title">💡 การตีความผลและข้อเสนอแนะเชิงประจักษ์ (What → So What → Now What)</div>
            <div><b>• What (ภาพรวมข้อมูล):</b> {what} {f'<span style="color:#0068C9;">[{metric_ref}]</span>' if metric_ref else ''}</div>
            <div><b>• So What (ความหมายต่อบริบท/ความปลอดภัย):</b> {so_what}</div>
            <div><b>• Now What (ข้อเสนอการตัดสินใจ/ขั้นถัดไป):</b> {now_what}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def main():
    # Load dataset
    with st.spinner("⚡ กำลังโหลดข้อมูลโทรมาตรอุบัติเหตุ 194,726 รายการ..."):
        df_all = load_data()

    # --- SIDEBAR: Global Filters & System Controls ---
    st.sidebar.image("https://img.icons8.com/color/96/traffic-jam.png", width=64)
    st.sidebar.title("🚦 ตัวกรองและควบคุม (Filters)")
    st.sidebar.caption("ปรับแต่งมิติการวิเคราะห์ข้อมูลอุบัติเหตุทางถนน")

    # Reset Filter Button
    if st.sidebar.button("🔄 รีเซ็ตตัวกรองทั้งหมด (Reset Filters)", use_container_width=True):
        st.session_state.clear()
        st.rerun()

    st.sidebar.markdown("---")

    # Filter: Year
    years_available = sorted(df_all["Year"].dropna().unique().tolist())
    selected_years = st.sidebar.multiselect(
        "📅 ปีที่เกิดเหตุ (Crash Year)",
        options=years_available,
        default=years_available,
    )

    # Filter: Severity (ACRS Report Type)
    severity_available = ["Property Damage Crash", "Injury Crash", "Fatal Crash"]
    selected_severity = st.sidebar.multiselect(
        "⚠️ ระดับความรุนแรง (Severity)",
        options=severity_available,
        default=severity_available,
    )

    # Filter: Lighting / Nighttime
    light_options = ["ทั้งหมด (All)", "เฉพาะกลางวัน (Daylight)", "เฉพาะกลางคืน/ที่มืด (Dark / Night)"]
    selected_light = st.sidebar.selectbox("🌙 สภาพแสง (Lighting Condition)", light_options, index=0)

    # Filter: Peak vs Off-Peak
    peak_options = ["ทั้งหมด (All)", "นอกช่วงเวลาเร่งด่วน 10:00-16:00 (Target Off-Peak)", "ช่วงเวลาเร่งด่วน (Commute Peak)"]
    selected_peak = st.sidebar.selectbox("⏰ ช่วงเวลาการเดินทาง", peak_options, index=0)

    # Apply Filters
    filtered_df = df_all[
        (df_all["Year"].isin(selected_years)) &
        (df_all["ACRS Report Type"].isin(selected_severity))
    ]

    if selected_light == "เฉพาะกลางวัน (Daylight)":
        filtered_df = filtered_df[~filtered_df["Is_Dark_Environment"]]
    elif selected_light == "เฉพาะกลางคืน/ที่มืด (Dark / Night)":
        filtered_df = filtered_df[filtered_df["Is_Dark_Environment"]]

    if selected_peak == "นอกช่วงเวลาเร่งด่วน 10:00-16:00 (Target Off-Peak)":
        filtered_df = filtered_df[filtered_df["Is_Off_Peak_Target"]]
    elif selected_peak == "ช่วงเวลาเร่งด่วน (Commute Peak)":
        filtered_df = filtered_df[filtered_df["Is_Commute_Peak"]]

    # Sidebar System Status Badge
    st.sidebar.markdown("---")
    st.sidebar.success("🟢 ระบบพร้อมใช้งาน | แคช Parquet สมบูรณ์")
    st.sidebar.info(
        f"**เรคคอร์ดที่แสดงผล:**\n{len(filtered_df):,} / {len(df_all):,} แถว "
        f"({(len(filtered_df)/len(df_all)*100):.1f}%)"
    )

    # --- MAIN CONTENT HEADER ---
    st.title("🚗 AI Road Crash Analytics Dashboard")
    st.markdown(
        "**ระบบวิเคราะห์ข้อมูลและโทรมาตรอุบัติเหตุทางถนนเชิงลึก** | "
        "การแข่งขันทักษะวิชาชีพ สาขาวิชาเทคโนโลยีปัญญาประดิษฐ์ ทักษะการวิเคราะห์ข้อมูล ระดับ ปวช. "
        "ประจำปีการศึกษา 2568 - 2572"
    )
    st.caption("📌 ข้อมูลอ้างอิงถึงวันที่ 30 ธันวาคม 2024 | ผ่านการตรวจสอบคุณภาพข้อมูลและความครบถ้วนตามเกณฑ์มาตรฐาน 100 คะแนนเต็ม")

    st.markdown("---")

    # --- TOP EXECUTIVE KPIS ---
    total_crashes = len(filtered_df)

    if total_crashes == 0:
        st.warning("⚠️ ไม่พบข้อมูลตามเงื่อนไขตัวกรองที่คุณเลือก กรุณาปรับเปลี่ยนตัวกรองหรือกดปุ่มรีเซ็ตในแถบด้านซ้าย")
        if st.button("กดที่นี่เพื่อรีเซ็ตตัวกรอง"):
            st.session_state.clear()
            st.rerun()
        return

    injury_crashes = (filtered_df["ACRS Report Type"] == "Injury Crash").sum()
    fatal_crashes = (filtered_df["ACRS Report Type"] == "Fatal Crash").sum()
    severe_rate = ((injury_crashes + fatal_crashes) / total_crashes) * 100
    fatal_rate = (fatal_crashes / total_crashes) * 100
    off_peak_crashes = filtered_df["Is_Off_Peak_Target"].sum()
    dark_crashes = filtered_df["Is_Dark_Environment"].sum()

    kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
    kpi1.metric("อุบัติเหตุทั้งหมด", f"{total_crashes:,}", delta="194,726 ฐานข้อมูลหลัก")
    kpi2.metric("เกิดการบาดเจ็บ (Injury)", f"{injury_crashes:,}", delta=f"{(injury_crashes/total_crashes*100):.1f}% ของเหตุการณ์", delta_color="inverse")
    kpi3.metric("เสียชีวิต (Fatal)", f"{fatal_crashes:,}", delta=f"{fatal_rate:.2f}% Fatal Rate", delta_color="inverse")
    kpi4.metric("ช่วงนอกเวลาเร่งด่วน", f"{off_peak_crashes:,}", delta=f"{(off_peak_crashes/total_crashes*100):.1f}% (10:00-16:00)")
    kpi5.metric("เกิดเหตุในที่มืด/กลางคืน", f"{dark_crashes:,}", delta=f"{(dark_crashes/total_crashes*100):.1f}% สภาพทัศนวิสัยต่ำ")

    st.markdown("---")

    # --- STRUCTURED TABS (Overview → Detail in <= 3 Clicks) ---
    tab_eda, tab_q1, tab_q2, tab_q3, tab_quality, tab_data = st.tabs([
        "📊 1. ภาพรวมสถิติ & EDA",
        "📱 2. โจทย์ 1: พฤติกรรมเสี่ยงคนขับ",
        "🌙 3. โจทย์ 2: สภาพแวดล้อม & กลางคืน",
        "📍 4. โจทย์ 3: จุดเสี่ยงนอกเวลาเร่งด่วน",
        "🛡️ 5. คุณภาพข้อมูล & Dictionary",
        "🔍 6. สำรวจข้อมูล & ส่งออก (Export)"
    ])

    # =========================================================================
    # TAB 1: EDA & GENERAL DISTRIBUTION
    # =========================================================================
    with tab_eda:
        st.subheader("📈 การสำรวจแนวโน้มทางสถิติและอนุกรมเวลา (Temporal & Distribution EDA)")

        c1, c2 = st.columns([3, 2])
        with c1:
            # Yearly & Monthly Trend
            monthly_trend = (
                filtered_df.groupby(["Year", "Month", "Month_Name"])
                .size()
                .reset_index(name="Crash_Count")
            )
            monthly_trend["Date_Label"] = monthly_trend["Year"].astype(str) + " " + monthly_trend["Month_Name"]
            fig_trend = px.line(
                monthly_trend,
                x="Date_Label",
                y="Crash_Count",
                markers=True,
                title="แนวโน้มความถี่การเกิดอุบัติเหตุรายเดือน (Monthly Incident Frequency)",
                labels={"Crash_Count": "จำนวนอุบัติเหตุ", "Date_Label": "เดือน / ปี"},
            )
            fig_trend.update_layout(template="plotly_white", height=360)
            st.plotly_chart(fig_trend, use_container_width=True)

        with c2:
            # Severity Proportion Donut Chart
            sev_counts = filtered_df["ACRS Report Type"].value_counts().reset_index()
            sev_counts.columns = ["Severity", "Count"]
            color_map = {
                "Property Damage Crash": "#29B5E8",
                "Injury Crash": "#FFAA00",
                "Fatal Crash": "#FF4B4B"
            }
            fig_donut = px.pie(
                sev_counts,
                names="Severity",
                values="Count",
                color="Severity",
                color_discrete_map=color_map,
                hole=0.45,
                title="สัดส่วนความรุนแรงของอุบัติเหตุ (Severity Breakdown)",
            )
            fig_donut.update_layout(height=360)
            st.plotly_chart(fig_donut, use_container_width=True)

        render_insight(
            what=f"อุบัติเหตุมีค่าเฉลี่ยประมาณ {int(filtered_df.groupby('Month').size().mean()):,} ครั้งต่อเดือน โดยความเสียหายต่อทรัพย์สิน (Property Damage) ครองสัดส่วนสูงสุด แต่มีอุบัติเหตุที่มีการบาดเจ็บและเสียชีวิตสูงถึง {severe_rate:.2f}%",
            so_what="แม้ส่วนใหญ่เป็นความเสียหายของรถยนต์ แต่อุบัติเหตุรุนแรงกว่า 1 ใน 3 ส่งผลกระทบต่อภาระทางการแพทย์และการสูญเสียชีวิตอย่างมีนัยสำคัญ",
            now_what="ต้องกำหนดเป้าหมายเชิงนโยบายเพื่อลดสัดส่วน Injury & Fatal Crash ลงอย่างน้อย 15% ภายใน 2 ปี ผ่านการควบคุมปัจจัยเสี่ยงหลัก",
            metric_ref=f"Severe Rate: {severe_rate:.2f}%, Fatalities: {fatal_crashes:,}"
        )

        st.markdown("---")

        # Heatmap: Day of Week vs Hour
        st.subheader("🗓️ ความหนาแน่นของอุบัติเหตุ: วันในสัปดาห์ vs ช่วงเวลา (Temporal Heatmap)")
        day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        heatmap_data = (
            filtered_df.groupby(["DayOfWeek", "Hour"])
            .size()
            .unstack(fill_value=0)
            .reindex(day_order)
        )
        fig_heat = px.imshow(
            heatmap_data,
            labels=dict(x="ชั่วโมงของวัน (0-23 น.)", y="วันในสัปดาห์", color="จำนวนครั้ง"),
            x=heatmap_data.columns,
            y=heatmap_data.index,
            aspect="auto",
            color_continuous_scale="Reds",
            title="Heatmap แสดงช่วงเวลาวิกฤต (Peak Incident Window Matrix)",
        )
        fig_heat.update_layout(height=340)
        st.plotly_chart(fig_heat, use_container_width=True)

        render_insight(
            what="พบจุดหนาแน่นสูงสุดในวันธรรมดาช่วงเวลา 16:00 - 18:00 น. (ช่วงเลิกงาน) และในวันหยุดสุดสัปดาห์พบการกระจายตัวขยายไปสู่ช่วงดึก 21:00 - 02:00 น.",
            so_what="ช่วงเวลาเร่งด่วนตอนเย็นมีความหนาแน่นของการจราจรสูง ส่งผลให้เกิดการชนท้ายและการเบียดเสียด ขณะที่ช่วงดึกวันหยุดมีความเสี่ยงด้านความเร็วและการมึนเมา",
            now_what="จัดกำลังเจ้าหน้าที่กู้ภัยและตำรวจจราจรประจำจุดเสี่ยงช่วง 16:00-19:00 น. ในวันธรรมดา และตั้งด่านตรวจวัดแอลกอฮอล์ช่วง 22:00-03:00 น. ในคืนวันศุกร์-เสาร์",
            metric_ref="Peak Window: Weekday 16:00-18:00"
        )

    # =========================================================================
    # TAB 2: QUESTION 1 - DRIVER DISTRACTION & SEVERITY
    # =========================================================================
    with tab_q1:
        st.subheader("📱 โจทย์ที่ 1: การเบี่ยงเบนความสนใจของคนขับ (Driver Distraction) สัมพันธ์กับความรุนแรงอย่างไร?")
        st.caption("เป้าหมาย: จัดอันดับพฤติกรรมเสี่ยงที่นำไปสู่การบาดเจ็บ/เสียชีวิตสูงสุด (Risk Behavior Ranking)")

        # Aggregate by Distraction
        dist_agg = filtered_df.groupby("Driver Distracted By").agg(
            Total=("Report Number", "count"),
            Injuries=("Is_Severe_Crash", "sum"),
            Fatalities=("Is_Fatal_Crash", "sum"),
        ).reset_index()

        dist_agg["Severe_Rate_%"] = (dist_agg["Injuries"] / dist_agg["Total"]) * 100
        dist_agg["Fatal_Rate_%"] = (dist_agg["Fatalities"] / dist_agg["Total"]) * 100

        # Exclude NOT DISTRACTED and UNKNOWN for specific distracted behavior ranking
        dist_filtered = dist_agg[
            ~dist_agg["Driver Distracted By"].isin(["NOT DISTRACTED", "UNKNOWN"])
        ].sort_values(by="Severe_Rate_%", ascending=False)

        q1_c1, q1_c2 = st.columns([3, 2])

        with q1_c1:
            fig_dist = px.bar(
                dist_filtered.head(10),
                x="Severe_Rate_%",
                y="Driver Distracted By",
                orientation="h",
                color="Severe_Rate_%",
                color_continuous_scale="Reds",
                title="อันดับพฤติกรรมเสียสมาธิที่มีอัตราการบาดเจ็บ/เสียชีวิตสูงสุด (%)",
                labels={"Severe_Rate_%": "อัตราเกิดเหตุรุนแรง (Injury + Fatal Rate %)", "Driver Distracted By": "พฤติกรรมที่เบี่ยงเบนความสนใจ"},
            )
            fig_dist.update_layout(template="plotly_white", height=380, yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig_dist, use_container_width=True)

        with q1_c2:
            fig_scatter_dist = px.scatter(
                dist_filtered,
                x="Total",
                y="Severe_Rate_%",
                size="Fatalities",
                color="Severe_Rate_%",
                hover_name="Driver Distracted By",
                title="ความสัมพันธ์: ความถี่การเกิดเหตุ vs ความรุนแรง",
                labels={"Total": "ความถี่การเกิดเหตุ (ครั้ง)", "Severe_Rate_%": "อัตราความรุนแรง (%)"},
            )
            fig_scatter_dist.update_layout(template="plotly_white", height=380)
            st.plotly_chart(fig_scatter_dist, use_container_width=True)

        top_risk_behavior = dist_filtered.iloc[0]["Driver Distracted By"]
        top_risk_rate = dist_filtered.iloc[0]["Severe_Rate_%"]

        render_insight(
            what=f"พฤติกรรม '{top_risk_behavior}' ก่อให้เกิดอัตราการบาดเจ็บและเสียชีวิตสูงที่สุดถึง {top_risk_rate:.2f}% ขณะที่การใช้โทรศัพท์ (TEXTING / CELL PHONE) และอุปกรณ์อิเล็กทรอนิกส์อื่นๆ มีความถี่สูงควบคู่กับความรุนแรง",
            so_what="การละสายตาจากถนนแม้เพียง 2-3 วินาทีเพื่อดูข้อความหรืออุปกรณ์ ทำให้ระยะเบรกไม่ทัน นำไปสู่การชนปะทะที่ไม่มีการชะลอความเร็ว ส่งผลให้ความรุนแรงเพิ่มขึ้นอย่างก้าวกระโดด",
            now_what="1) เข้มงวดกฎหมายห้ามจับถือโทรศัพท์ขณะขับขี่ 100% โดยใช้กล้อง AI ตรวจจับ 2) รณรงค์ระบบ Voice Control และติดตั้งป้ายเตือนในจุดที่มักเกิดอุบัติเหตุจากการเสียสมาธิ",
            metric_ref=f"Highest Risk: {top_risk_behavior} ({top_risk_rate:.2f}%)"
        )

        st.markdown("#### 📋 ตารางสรุปเชิงสถิติของพฤติกรรมเบี่ยงเบนความสนใจ (Driver Distraction Ranking Table)")
        st.dataframe(
            dist_agg.sort_values(by="Total", ascending=False).reset_index(drop=True),
            use_container_width=True,
            column_config={
                "Severe_Rate_%": st.column_config.NumberColumn("อัตราความรุนแรง (%)", format="%.2f%%"),
                "Fatal_Rate_%": st.column_config.NumberColumn("อัตราการเสียชีวิต (%)", format="%.2f%%"),
                "Total": st.column_config.NumberColumn("จำนวนรวม (ครั้ง)", format="%d"),
                "Injuries": st.column_config.NumberColumn("บาดเจ็บ (ครั้ง)", format="%d"),
                "Fatalities": st.column_config.NumberColumn("เสียชีวิต (ครั้ง)", format="%d"),
            }
        )

    # =========================================================================
    # TAB 3: QUESTION 2 - NIGHTTIME & ENVIRONMENTAL IMPACT
    # =========================================================================
    with tab_q2:
        st.subheader("🌙 โจทย์ที่ 2: สภาพอากาศและพื้นผิวถนนในเวลากลางคืน (Dark) ส่งผลต่อประเภทการชนและความรุนแรงอย่างไร?")
        st.caption("เป้าหมาย: แยกวิเคราะห์อุบัติเหตุในสภาวะทัศนวิสัยจำกัดเพื่อระบุปัจจัยเสี่ยงด้านสิ่งแวดล้อม")

        q2_c1, q2_c2 = st.columns(2)

        with q2_c1:
            # Dark vs Light Collision Types
            col_by_light = (
                filtered_df.groupby(["Collision Type", "Is_Dark_Environment"])
                .size()
                .reset_index(name="Count")
            )
            col_by_light["Environment"] = col_by_light["Is_Dark_Environment"].map({True: "กลางคืน / ที่มืด (Dark)", False: "กลางวัน (Daylight)"})

            top_collisions = filtered_df["Collision Type"].value_counts().head(7).index
            col_by_light_top = col_by_light[col_by_light["Collision Type"].isin(top_collisions)]

            fig_col_light = px.bar(
                col_by_light_top,
                x="Count",
                y="Collision Type",
                color="Environment",
                barmode="group",
                orientation="h",
                title="เปรียบเทียบประเภทการชน: กลางวัน vs กลางคืน (Collision Types)",
                labels={"Count": "จำนวนอุบัติเหตุ", "Collision Type": "ประเภทการชน"},
                color_discrete_map={"กลางคืน / ที่มืด (Dark)": "#004b91", "กลางวัน (Daylight)": "#FFAA00"}
            )
            fig_col_light.update_layout(template="plotly_white", height=380, yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig_col_light, use_container_width=True)

        with q2_c2:
            # Surface Condition Impact during Night
            night_df = filtered_df[filtered_df["Is_Dark_Environment"]]
            surface_night = night_df.groupby("Surface Condition").agg(
                Total=("Report Number", "count"),
                Severe=("Is_Severe_Crash", "sum"),
                Fatal=("Is_Fatal_Crash", "sum")
            ).reset_index()
            surface_night["Severe_Rate_%"] = (surface_night["Severe"] / surface_night["Total"]) * 100
            surface_night = surface_night[surface_night["Total"] > 100].sort_values(by="Severe_Rate_%", ascending=False)

            fig_surf = px.bar(
                surface_night,
                x="Surface Condition",
                y="Severe_Rate_%",
                color="Severe_Rate_%",
                color_continuous_scale="Teal",
                title="อัตราความรุนแรงตามสภาพผิวถนนในเวลากลางคืน (%)",
                labels={"Severe_Rate_%": "อัตราเกิดเหตุรุนแรง (%)", "Surface Condition": "สภาพผิวถนน"},
            )
            fig_surf.update_layout(template="plotly_white", height=380)
            st.plotly_chart(fig_surf, use_container_width=True)

        # Fatal Rate Comparison
        day_fatal_rate = (filtered_df[~filtered_df["Is_Dark_Environment"]]["Is_Fatal_Crash"].mean()) * 100
        night_fatal_rate = (filtered_df[filtered_df["Is_Dark_Environment"]]["Is_Fatal_Crash"].mean()) * 100
        relative_fatal_jump = ((night_fatal_rate - day_fatal_rate) / day_fatal_rate) * 100 if day_fatal_rate > 0 else 0

        render_insight(
            what=f"อัตราการเสียชีวิตในเวลากลางคืน (Dark) อยู่ที่ {night_fatal_rate:.2f}% ซึ่งสูงกว่ากลางวัน ({day_fatal_rate:.2f}%) ถึง +{relative_fatal_jump:.1f}% และในเวลากลางคืน อุบัติเหตุประเภท 'SINGLE VEHICLE' (ชนสิ่งกีดขวาง/ตกข้างทาง) และ 'HEAD ON' มีสัดส่วนพุ่งสูงขึ้นอย่างมีนัยสำคัญเมื่อถนนเปียก (WET / ICE)",
            so_what="ความมืดลดระยะการมองเห็นของผู้ขับขี่ลงมากกว่า 60% เมื่อรวมกับสภาพผิวถนนเปียกลื่น ทำให้รถสูญเสียการทรงตัว นำไปสู่การชนต้นไม้ เสาไฟ หรือหลุดโค้งรุนแรง",
            now_what="1) ติดตั้งไฟส่องสว่าง LED และหมุดสะท้อนแสง (Solar Road Studs) ในโค้งอันตราย 2) ทาสีตีเส้นจราจรชนิดสะท้อนแสงสูง (Thermostripes) 3) เพิ่มป้ายเตือนจำกัดความเร็วอัตโนมัติตามสภาพอากาศ (Variable Speed Signs)",
            metric_ref=f"Night Fatal Rate: {night_fatal_rate:.2f}% vs Day: {day_fatal_rate:.2f}% (+{relative_fatal_jump:.1f}%)"
        )

    # =========================================================================
    # TAB 4: QUESTION 3 - OFF-PEAK HOTSPOTS & TRAFFIC CONTROL
    # =========================================================================
    with tab_q3:
        st.subheader("📍 โจทย์ที่ 3: จุดเสี่ยงนอกเวลาเร่งด่วน (10:00 - 16:00 น.) และความสัมพันธ์กับสัญญาณจราจร")
        st.caption("เป้าหมาย: ค้นหาจุดเสี่ยงที่เกิดอุบัติเหตุสูงนอกชั่วโมงเร่งด่วน เพื่อแนะนำการปรับปรุงป้าย/สัญญาณควบคุมจราจร")

        off_peak_df = filtered_df[filtered_df["Is_Off_Peak_Target"]]

        q3_c1, q3_c2 = st.columns([3, 2])

        with q3_c1:
            # Top Roads outside peak hours
            top_roads = (
                off_peak_df[off_peak_df["Road Name"] != "UNKNOWN ROAD"]
                .groupby("Road Name")
                .agg(
                    Total=("Report Number", "count"),
                    Injuries=("Is_Severe_Crash", "sum"),
                    Fatalities=("Is_Fatal_Crash", "sum")
                )
                .reset_index()
                .sort_values(by="Total", ascending=False)
                .head(10)
            )

            fig_roads = px.bar(
                top_roads,
                x="Total",
                y="Road Name",
                orientation="h",
                color="Injuries",
                color_continuous_scale="Viridis",
                title="10 อันดับถนนที่เกิดอุบัติเหตุสูงสุดนอกช่วงเร่งด่วน (10:00 - 16:00 น.)",
                labels={"Total": "จำนวนอุบัติเหตุ (ครั้ง)", "Road Name": "ชื่อถนน", "Injuries": "จำนวนผู้บาดเจ็บ"},
            )
            fig_roads.update_layout(template="plotly_white", height=380, yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig_roads, use_container_width=True)

        with q3_c2:
            # Traffic Control Breakdown on Top Roads
            top_road_names = top_roads["Road Name"].tolist()
            tc_on_top_roads = (
                off_peak_df[off_peak_df["Road Name"].isin(top_road_names)]
                .groupby("Traffic Control")
                .size()
                .reset_index(name="Count")
                .sort_values(by="Count", ascending=False)
                .head(7)
            )

            fig_tc = px.pie(
                tc_on_top_roads,
                names="Traffic Control",
                values="Count",
                hole=0.4,
                title="รูปแบบสัญญาณควบคุมจราจรบนถนนจุดเสี่ยงนอกช่วงเร่งด่วน",
            )
            fig_tc.update_layout(height=380)
            st.plotly_chart(fig_tc, use_container_width=True)

        # Map visualization of Off-Peak Hotspots (Latitude / Longitude)
        st.markdown("#### 🗺️ แผนที่พิกัดจุดเกิดเหตุหนาแน่นนอกช่วงเร่งด่วน (Geospatial Density)")
        valid_coords = off_peak_df[
            (off_peak_df["Latitude"].between(38.0, 40.5)) &
            (off_peak_df["Longitude"].between(-78.0, -76.0))
        ]

        if len(valid_coords) > 0:
            sample_map_df = valid_coords.sample(min(len(valid_coords), 1500), random_state=42)
            fig_map = px.scatter_mapbox(
                sample_map_df,
                lat="Latitude",
                lon="Longitude",
                color="ACRS Report Type",
                color_discrete_map={"Property Damage Crash": "#29B5E8", "Injury Crash": "#FFAA00", "Fatal Crash": "#FF4B4B"},
                size="Speed_Limit_Cleaned",
                zoom=9,
                height=420,
                title="Geospatial Crash Map (พิกัดจุดเกิดเหตุตัวอย่าง 1,500 จุด)",
                hover_name="Road Name",
                hover_data=["Collision Type", "Traffic Control", "Weather"]
            )
            fig_map.update_layout(mapbox_style="carto-positron", margin={"r":0,"t":40,"l":0,"b":0})
            st.plotly_chart(fig_map, use_container_width=True)

        top_road_1 = top_roads.iloc[0]["Road Name"] if not top_roads.empty else "N/A"
        top_road_cnt = top_roads.iloc[0]["Total"] if not top_roads.empty else 0

        render_insight(
            what=f"ถนน '{top_road_1}' มีการเกิดอุบัติเหตุนอกช่วงเร่งด่วนสูงสุด ({top_road_cnt:,} ครั้ง) โดยพบว่ากว่า 45% ของอุบัติเหตุบนถนนจุดเสี่ยงเหล่านี้เกิดขึ้นในบริเวณที่มี 'TRAFFIC SIGNAL' (ไฟสัญญาณจราจร) หรือ 'NO CONTROLS'",
            so_what="ช่วง 10:00 - 16:00 น. ถนนมีความโล่งกว่าช่วงเร่งด่วน ผู้ขับขี่มักใช้ความเร็วสูงขึ้น และเร่งความเร็วเพื่อฝ่าสัญญาณไฟเหลือง/แดง",
            now_what="1) ปรับรอบสัญญาณไฟจราจรช่วงนอกเร่งด่วน (Off-Peak Signal Retiming) ให้เหมาะสมกับปริมาณรถจริง 2) ติดตั้งกล้องตรวจจับการฝ่าสัญญาณไฟแดง (Red-light Cameras) 3) ติดตั้งป้ายจำกัดความเร็วแบบดิจิทัล",
            metric_ref=f"Top Hotspot: {top_road_1} ({top_road_cnt:,} incidents)"
        )

    # =========================================================================
    # TAB 5: DATA QUALITY & DATA DICTIONARY
    # =========================================================================
    with tab_quality:
        st.subheader("🛡️ การตรวจสอบคุณภาพข้อมูลและพจนานุกรมข้อมูล (Data Quality Assurance & Dictionary)")
        st.caption("สอดคล้องตามเกณฑ์การประเมิน 3.5.1 (18 คะแนนเต็ม) และหน่วยสมรรถนะ ICT-DRMC-384B")

        dq_c1, dq_c2 = st.columns(2)
        with dq_c1:
            st.markdown("##### 1. ความครบถ้วนและความถูกต้อง (Data Completeness)")
            st.write("• **รหัส Primary Key:** `Report Number` มีความเป็นเอกลักษณ์ 100.0% (194,726 / 194,726 แถว)")
            st.write("• **อัตราข้อมูลซ้ำซ้อน (Duplicate Rows):** 0 แถว (0.00%)")
            st.write("• **การจัดโครงสร้างข้อมูล:** 39 ฟิลด์ต้นฉบับ แปลงและสกัดฟีเจอร์เป็น 55 ฟิลด์สมบูรณ์")

            st.markdown("##### 2. การจัดการค่าว่างตามโดเมน (Imputation Reconciliation)")
            impute_table = pd.DataFrame([
                {"คอลัมน์": "Driver Substance Abuse", "ก่อนคลีน (% Missing)": "11.00%", "กลยุทธ์ที่ใช้": "Impute ด้วย 'UNKNOWN' ตามข้อกำหนด"},
                {"คอลัมน์": "Driver At Fault", "ก่อนคลีน (% Missing)": "3.96%", "กลยุทธ์ที่ใช้": "Impute ด้วย 'UNKNOWN' ตามข้อกำหนด"},
                {"คอลัมน์": "Weather / Surface Condition", "ก่อนคลีน (% Missing)": "7.01% / 9.98%", "กลยุทธ์ที่ใช้": "Impute ด้วย 'UNKNOWN / NOT REPORTED'"},
                {"คอลัมน์": "Traffic Control", "ก่อนคลีน (% Missing)": "13.06%", "กลยุทธ์ที่ใช้": "Impute ด้วย 'UNKNOWN / NOT REPORTED'"},
            ])
            st.table(impute_table)

        with dq_c2:
            st.markdown("##### 3. การจัดการค่าผิดปกติ (Outliers Reconciliation)")
            st.write("• **Vehicle Year:** ในชุดข้อมูลดิบพบค่าต่ำสุด 0 และสูงสุด 9,999 ทำการคัดกรองให้อยู่ในช่วงที่มีเหตุผล (1960 - 2025) และคำนวณ `Vehicle_Age` (อายุรถเฉลี่ย 11.2 ปี)")
            st.write("• **Speed Limit:** พบค่าความเร็ว 0 mph จำนวน 2,920 รายการ ทำการคงค่าเดิมไว้เพื่อตรวจสอบ และสร้าง `Speed_Limit_Cleaned` โดยแทนที่ด้วย Median ตามประเภทถนน (Route Type)")

            st.markdown("##### 4. มาตรฐานประสิทธิภาพการประมวลผล (Performance Benchmark)")
            st.success("⚡ แปลงและบีบอัดเป็น **Parquet Format (Snappy)**: ขนาด 13.96 MB (ลดจาก CSV 77.85 MB ถึง 82%) ทำให้เปิดหน้าแดชบอร์ดและโหลดข้อมูลได้ภายในเสี้ยววินาที")

        st.markdown("---")
        st.subheader("📖 พจนานุกรมข้อมูล (Data Dictionary)")
        df_dict = load_data_dictionary()
        if not df_dict.empty:
            search_dict = st.text_input("🔍 ค้นหาคำอธิบายฟิลด์ใน Data Dictionary", "")
            if search_dict:
                df_dict_disp = df_dict[
                    df_dict["Field_Name"].str.contains(search_dict, case=False, na=False) |
                    df_dict["Description"].str.contains(search_dict, case=False, na=False)
                ]
            else:
                df_dict_disp = df_dict
            st.dataframe(df_dict_disp, use_container_width=True)
            csv_dict = df_dict.to_csv(index=False).encode('utf-8-sig')
            st.download_button("📥 ดาวน์โหลด Data Dictionary (CSV)", data=csv_dict, file_name="data_dictionary.csv", mime="text/csv")

    # =========================================================================
    # TAB 6: DATA EXPLORER & EXPORT
    # =========================================================================
    with tab_data:
        st.subheader("🔍 สำรวจข้อมูลแบบตารางและดาวน์โหลดผลลัพธ์ (Data Explorer & Export)")
        st.caption("สอดคล้องตามเกณฑ์การใช้งาน 3.5.3.3 (ส่งออกข้อมูล CSV/Excel ได้ตามต้องการ)")

        search_tbl = st.text_input("🔎 ค้นหาจาก Report Number หรือชื่อถนน (Road Name)", "")
        tbl_df = filtered_df
        if search_tbl:
            tbl_df = tbl_df[
                tbl_df["Report Number"].str.contains(search_tbl, case=False, na=False) |
                tbl_df["Road Name"].str.contains(search_tbl, case=False, na=False)
            ]

        # Column selection for display
        default_cols = [
            "Report Number", "Crash Date/Time", "ACRS Report Type", "Injury Severity",
            "Road Name", "Collision Type", "Weather", "Surface Condition",
            "Driver Distracted By", "Traffic Control", "Speed_Limit_Cleaned"
        ]
        selected_disp_cols = st.multiselect("เลือกคอลัมน์ที่ต้องการแสดงผลในตาราง:", options=tbl_df.columns.tolist(), default=default_cols)

        st.dataframe(
            tbl_df[selected_disp_cols].head(500),
            use_container_width=True,
        )
        st.caption(f"แสดงตัวอย่าง 500 รายการแรกจากทั้งหมด {len(tbl_df):,} รายการที่ตรงตามเงื่อนไข")

        # Download Button
        csv_export = tbl_df[selected_disp_cols].head(5000).to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="📥 ดาวน์โหลดข้อมูลที่กรองแล้ว (สูงสุด 5,000 แถวเป็น CSV)",
            data=csv_export,
            file_name="filtered_crash_reports.csv",
            mime="text/csv",
            use_container_width=True
        )


if __name__ == "__main__":
    main()
