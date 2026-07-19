import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="AI Rainfall Prediction System",
    page_icon="🌧",
    layout="wide"
)

# ==========================================
# LOAD DATA
# ==========================================

@st.cache_data
def load_data():
    return pd.read_excel("data/india_weather_rainfall_data.xlsx")


df = load_data()

# ==========================================
# TITLE
# ==========================================

st.title("🌧 AI-Based Rainfall Prediction System")

st.markdown("""
Welcome to the **AI-Based Rainfall Prediction System**.

This project predicts rainfall using Machine Learning techniques based on historical weather observations collected from different weather stations across India.

### Weather Parameters Used

- 🌡 Average Temperature
- ❄ Minimum Temperature
- ☀ Maximum Temperature
- 💨 Wind Speed
- 🌍 Air Pressure
- 📍 Latitude
- 📍 Longitude
- ⛰ Elevation
- 🍂 Season
- 📅 Month
- 🌧 Previous Rainfall
""")

st.divider()

# ==========================================
# DATASET OVERVIEW
# ==========================================

st.header("📊 Dataset Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Records", f"{len(df):,}")
col2.metric("States", df["state"].nunique())
col3.metric("Districts", df["district"].nunique())
col4.metric("Weather Stations", df["station_name"].nunique())

st.divider()

# ==========================================
# DATASET STATISTICS
# ==========================================

st.header("📈 Dataset Statistics")

c1, c2, c3 = st.columns(3)

c1.metric(
    "Average Temperature",
    f"{df['avg_temp'].mean():.2f} °C"
)

c2.metric(
    "Average Rainfall",
    f"{df['rainfall'].mean():.2f} mm"
)

c3.metric(
    "Maximum Rainfall",
    f"{df['rainfall'].max():.2f} mm"
)

st.divider()

# ==========================================
# MONTHLY RAINFALL
# ==========================================

st.header("🌧 Average Monthly Rainfall")

month_order = [
    "January", "February", "March", "April",
    "May", "June", "July", "August",
    "September", "October", "November", "December"
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

st.plotly_chart(fig, use_container_width=True)

st.divider()

# ==========================================
# MODEL PERFORMANCE
# ==========================================

st.header("🤖 Model Performance Comparison")

performance = pd.DataFrame({
    "Model": [
        "Linear Regression",
        "Random Forest",
        "XGBoost",
        "CNN + BiLSTM"
    ],
    "R² Score": [
        1.000,
        0.995,
        0.973,
        0.077
    ]
})

fig2 = px.bar(
    performance,
    x="Model",
    y="R² Score",
    color="R² Score",
    text="R² Score",
    title="Model Comparison"
)

st.plotly_chart(fig2, use_container_width=True)

st.success("✅ XGBoost was selected as the final model because it achieved the best overall performance.")

st.divider()

# ==========================================
# PROJECT WORKFLOW
# ==========================================

st.header("⚙ Project Workflow")

st.markdown("""
1. Collect Weather Dataset

2. Data Cleaning

3. Exploratory Data Analysis (EDA)

4. Feature Engineering

5. Feature Selection

6. Train Multiple Models

7. Compare Model Performance

8. Select Best Model (XGBoost)

9. Save Trained Model

10. Deploy using Streamlit
""")

st.divider()

# ==========================================
# TECHNOLOGIES
# ==========================================

st.header("🛠 Technologies Used")

t1, t2, t3, t4 = st.columns(4)

with t1:
    st.success("""
Python

Pandas

NumPy
""")

with t2:
    st.success("""
Scikit-Learn

XGBoost

TensorFlow
""")

with t3:
    st.success("""
Plotly

Joblib

Google Colab
""")

with t4:
    st.success("""
Streamlit

GitHub

VS Code
""")

st.divider()

# ==========================================
# FOOTER
# ==========================================

st.markdown("""
---
### 👩‍💻 Developed By

**Amisha Choudhary**

B.Tech CSE (Bioinformatics)

AI-Based Rainfall Prediction System
""")
