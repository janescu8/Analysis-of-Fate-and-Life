import streamlit as st
import pandas as pd
import matplotlib
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px

# 🖼️ 接下來才是畫面內容
st.title("🔮 名人命運與人生資料分析")


# 設定中文字型（macOS 適用）
matplotlib.rcParams['font.family'] = 'Heiti TC'
matplotlib.rcParams['axes.unicode_minus'] = False

# 讀取資料
df = pd.read_csv("list.csv")

# 補充欄位：年齡、簡化婚姻分類、姓名、工作類型
def calculate_age(birth_str):
    try:
        birth = datetime.strptime(birth_str, "%Y-%m-%d")
        today = datetime.today()
        return today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
    except:
        return None

def simplify_marriage(status):
    if pd.isna(status):
        return "未知"
    elif "已婚" in status:
        return "已婚"
    elif "未婚" in status:
        return "未婚"
    elif "離婚" in status:
        return "離婚"
    else:
        return "其他"

def classify_job(job):
    if pd.isna(job): return "其他"
    if "總統" in job or "國務卿" in job or "議員" in job or "領袖" in job:
        return "政治"
    elif "公司" in job or "創辦人" in job or "執行長" in job or "企業" in job:
        return "企業"
    elif "演員" in job or "歌手" in job or "電視" in job or "媒體" in job or "影" in job:
        return "演藝"
    elif "宗教" in job or "教宗" in job or "達賴" in job:
        return "宗教"
    elif "籃球" in job or "足球" in job or "運動" in job or "高爾夫" in job or "網球" in job:
        return "運動"
    else:
        return "其他"

df["年齡"] = df["完整生日"].apply(calculate_age)
df["婚姻分類"] = df["婚姻狀態"].apply(simplify_marriage)
df["姓名"] = df["中文姓名"].fillna(df["英文姓名"])
df["工作類型"] = df["工作經歷"].apply(classify_job)

# Sidebar 篩選
with st.sidebar:
    st.header("🔍 篩選條件")
    selected_signs = st.multiselect("星座", df["星座"].dropna().unique())
    selected_mbti = st.multiselect("MBTI", df["MBTI"].dropna().unique())

filtered_df = df.copy()
if selected_signs:
    filtered_df = filtered_df[filtered_df["星座"].isin(selected_signs)]
if selected_mbti:
    filtered_df = filtered_df[filtered_df["MBTI"].isin(selected_mbti)]

# 顯示篩選後的資料表格
st.subheader("📋 名人清單")
st.dataframe(filtered_df, use_container_width=True)

# 長條圖：婚姻分類 vs 工作類型（滑鼠顯示人名）
st.markdown("---")
st.header("📊 資料視覺化分析")

grouped = filtered_df.groupby(["婚姻分類", "工作類型"])["姓名"].apply(lambda x: "<br>".join(x)).reset_index()
grouped["人數"] = grouped["姓名"].apply(lambda x: x.count("<br>") + 1)

fig1 = go.Figure()
for job_type in grouped["工作類型"].unique():
    subset = grouped[grouped["工作類型"] == job_type]
    fig1.add_trace(go.Bar(
        x=subset["婚姻分類"],
        y=subset["人數"],
        name=job_type,
        text=subset["姓名"],
        textposition="none",
        hovertemplate="<b>%{x} - " + job_type + "</b><br>人數: %{y}<br>名人:<br>%{text}<extra></extra>"
    ))

fig1.update_layout(
    barmode='stack',
    title="💍 婚姻分類 vs 工作類型",
    xaxis_title="婚姻分類",
    yaxis_title="人數",
    legend_title="工作類型"
)
st.plotly_chart(fig1, use_container_width=True)

# 熱力圖：MBTI vs 星座（顯示名人名單）
heat_data = filtered_df.groupby(["MBTI", "星座"])["姓名"].apply(lambda x: "<br>".join(x)).reset_index()
heat_data["人數"] = heat_data["姓名"].apply(lambda x: x.count("<br>") + 1)

fig2 = go.Figure(
    data=go.Heatmap(
        z=heat_data["人數"],
        x=heat_data["星座"],
        y=heat_data["MBTI"],
        text=heat_data["姓名"],
        hoverinfo="text",
        colorscale="YlGnBu"
    )
)
fig2.update_layout(
    title="MBTI vs 星座熱力圖",
    xaxis_title="星座",
    yaxis_title="MBTI"
)
st.plotly_chart(fig2, use_container_width=True)






