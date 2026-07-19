import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------------------
# PAGE CONFIG
# -----------------------------------------

st.set_page_config(
    page_title="Analytics",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Rainfall Analytics Dashboard")

# -----------------------------------------
# LOAD DATA
# -----------------------------------------

@st.cache_data
def load_data():
    return pd.read_excel("data/india_weather_rainfall_data.xlsx")

df = load_data()

# -----------------------------------------
# DATASET SUMMARY
# -----------------------------------------

st.header("Dataset Summary")

c1,c2,c3,c4 = st.columns(4)

c1.metric("Records",len(df))
c2.metric("States",df["state"].nunique())
c3.metric("Districts",df["district"].nunique())
c4.metric("Stations",df["station_name"].nunique())

st.divider()

# -----------------------------------------
# MONTHLY RAINFALL
# -----------------------------------------

st.header("Average Monthly Rainfall")

month_order = [
    "January","February","March","April","May","June",
    "July","August","September","October","November","December"
]

monthly = (
    df.groupby("month")["rainfall"]
    .mean()
    .reset_index()
)

monthly["month"] = pd.Categorical(
    monthly["month"],
    categories=month_order,
    ordered=True
)

monthly = monthly.sort_values("month")

fig = px.bar(
    monthly,
    x="month",
    y="rainfall",
    color="rainfall",
    title="Average Rainfall by Month"
)

st.plotly_chart(fig,use_container_width=True)

st.divider()

# -----------------------------------------
# RAINFALL DISTRIBUTION
# -----------------------------------------

st.header("Rainfall Distribution")

fig = px.histogram(
    df,
    x="rainfall",
    nbins=50,
    title="Distribution of Rainfall"
)

st.plotly_chart(fig,use_container_width=True)

st.divider()

# -----------------------------------------
# TEMPERATURE VS RAINFALL
# -----------------------------------------

st.header("Temperature vs Rainfall")

fig = px.scatter(
    df.sample(5000),
    x="avg_temp",
    y="rainfall",
    color="season",
    title="Temperature vs Rainfall"
)

st.plotly_chart(fig,use_container_width=True)

st.divider()

# -----------------------------------------
# TOP RAINY DISTRICTS
# -----------------------------------------

st.header("Top 10 Rainiest Districts")

district = (
    df.groupby("district")["rainfall"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig = px.bar(
    district,
    x="district",
    y="rainfall",
    color="rainfall",
    title="Top 10 Rainiest Districts"
)

st.plotly_chart(fig,use_container_width=True)

st.divider()

# -----------------------------------------
# STATE WISE RAINFALL
# -----------------------------------------

st.header("Average Rainfall by State")

state = (
    df.groupby("state")["rainfall"]
    .mean()
    .sort_values(ascending=False)
    .reset_index()
)

fig = px.bar(
    state,
    x="state",
    y="rainfall",
    color="rainfall"
)

st.plotly_chart(fig,use_container_width=True)

st.divider()

# -----------------------------------------
# SEASONAL RAINFALL
# -----------------------------------------

st.header("Season Wise Rainfall")

season = (
    df.groupby("season")["rainfall"]
    .mean()
    .reset_index()
)

fig = px.pie(
    season,
    names="season",
    values="rainfall",
    hole=0.4
)

st.plotly_chart(fig,use_container_width=True)

st.divider()

# -----------------------------------------
# CORRELATION HEATMAP
# -----------------------------------------

st.header("Correlation Heatmap")

corr = df.select_dtypes(include="number").corr()

fig,ax = plt.subplots(figsize=(10,8))

sns.heatmap(
    corr,
    cmap="coolwarm",
    annot=False,
    ax=ax
)

st.pyplot(fig)

st.divider()

# -----------------------------------------
# RAW DATA
# -----------------------------------------

st.header("Dataset Preview")

st.dataframe(df.head(100),use_container_width=True)
