import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="AI Rainfall Prediction",
    page_icon="🌧",
    layout="wide"
)

# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_data
def load_data():
    return pd.read_csv("data/rainfall.csv")

df = load_data()

# -----------------------------
# TITLE
# -----------------------------
st.title("🌧 AI Based Rainfall Prediction System")

st.markdown("""
### Welcome!

This project predicts rainfall using **Machine Learning and Deep Learning** techniques.

The system analyzes multiple weather parameters like:

- 🌡 Temperature
- 💨 Wind Speed
- 🌍 Air Pressure
- 📍 Latitude & Longitude
- ⛰ Elevation
- 🍂 Season

to estimate rainfall accurately.
""")

st.divider()

# -----------------------------
# DATASET OVERVIEW
# -----------------------------
st.header("📊 Dataset Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Records", f"{len(df):,}")
col2.metric("States", df["state"].nunique())
col3.metric("Districts", df["district"].nunique())
col4.metric("Weather Stations", df["station_name"].nunique())

st.divider()

# -----------------------------
# QUICK STATISTICS
# -----------------------------
st.header("📈 Dataset Statistics")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Average Temperature",
    f"{df['avg_temp'].mean():.2f} °C"
)

col2.metric(
    "Average Rainfall",
    f"{df['rainfall'].mean():.2f} mm"
)

col3.metric(
    "Maximum Rainfall",
    f"{df['rainfall'].max():.2f} mm"
)

st.divider()

# -----------------------------
# MONTHLY RAINFALL
# -----------------------------
st.header("🌧 Monthly Average Rainfall")

monthly = (
    df.groupby("month")["rainfall"]
    .mean()
    .reset_index()
)

month_order = [
    "January","February","March","April","May","June",
    "July","August","September","October","November","December"
]

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
    title="Average Monthly Rainfall"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# -----------------------------
# MODEL PERFORMANCE
# -----------------------------
st.header("🤖 Model Comparison")

performance = pd.DataFrame({

    "Model":[
        "Linear Regression",
        "Random Forest",
        "XGBoost",
        "CNN + BiLSTM"
    ],

    "R²":[
        1.000,
        0.995,
        0.973,
        0.077
    ]

})

fig2 = px.bar(
    performance,
    x="Model",
    y="R²",
    text="R²",
    color="R²"
)

st.plotly_chart(fig2, use_container_width=True)

st.info(
    "XGBoost is selected as the final model because it performed best on structured weather data."
)

st.divider()

# -----------------------------
# PROJECT WORKFLOW
# -----------------------------
st.header("⚙ Project Workflow")

st.markdown("""

1. Dataset Collection

2. Data Cleaning

3. Exploratory Data Analysis

4. Feature Engineering

5. Feature Selection

6. Model Training

7. Model Evaluation

8. Save Best Model

9. Streamlit Deployment

""")

st.divider()

# -----------------------------
# TECHNOLOGIES
# -----------------------------
st.header("🛠 Technologies Used")

tech1, tech2, tech3, tech4 = st.columns(4)

tech1.success("""
Python

Pandas

NumPy
""")

tech2.success("""
Scikit-Learn

XGBoost

TensorFlow
""")

tech3.success("""
Plotly

Matplotlib

Joblib
""")

tech4.success("""
Streamlit

GitHub

Google Colab
""")

st.divider()

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("""
---
### Developed By

**Amisha Choudhary**

B.Tech CSE (Bioinformatics)

AI Based Rainfall Prediction System
""")
# ==========================================
# PREDICTION
# ==========================================

if predict:

    # Get encoders
    state_encoder = encoders["state"]
    district_encoder = encoders["district"]
    station_encoder = encoders["station_name"]
    month_encoder = encoders["month"]
    season_encoder = encoders["season"]

    # Encode categorical features
    encoded_state = state_encoder.transform([latest["state"]])[0]
    encoded_district = district_encoder.transform([latest["district"]])[0]
    encoded_station = station_encoder.transform([latest["station_name"]])[0]
    encoded_month = month_encoder.transform([latest["month"]])[0]
    encoded_season = season_encoder.transform([latest["season"]])[0]

    # Create input dataframe in EXACT SAME ORDER
    input_df = pd.DataFrame({

        "month":[encoded_month],
        "season":[encoded_season],
        "station_name":[encoded_station],
        "state":[encoded_state],
        "district":[encoded_district],

        "avg_temp":[avg_temp],
        "min_temp":[min_temp],
        "max_temp":[max_temp],

        "wind_speed":[wind_speed],
        "air_pressure":[air_pressure],

        "elevation":[latest["elevation"]],
        "latitude":[latest["latitude"]],
        "longitude":[latest["longitude"]],

        "year":[latest["year"]],
        "month_num":[latest["month_num"]],
        "day":[latest["day"]],
        "day_of_week":[latest["day_of_week"]],
        "week":[latest["week"]],

        "rainfall_lag1":[latest["rainfall_lag1"]],
        "rainfall_lag2":[latest["rainfall_lag2"]],
        "rainfall_lag3":[latest["rainfall_lag3"]],

        "rainfall_roll3":[latest["rainfall_roll3"]],
        "rainfall_roll7":[latest["rainfall_roll7"]]

    })

    # Make prediction
    prediction = model.predict(input_df)[0]
       st.divider()

    st.subheader("🌧 Prediction Result")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Predicted Rainfall",
            f"{prediction:.2f} mm"
        )

    # Rainfall Category
    if prediction < 0.5:
        category = "No Rain 🌞"
        color = "green"
        recommendation = "No rainfall expected."

    elif prediction < 10:
        category = "Light Rain 🌦"
        color = "blue"
        recommendation = "Carry an umbrella."

    elif prediction < 30:
        category = "Moderate Rain 🌧"
        color = "orange"
        recommendation = "Moderate rainfall expected."

    elif prediction < 70:
        category = "Heavy Rain ⛈"
        color = "red"
        recommendation = "Avoid unnecessary travel."

    else:
        category = "Very Heavy Rain 🌊"
        color = "darkred"
        recommendation = "Stay indoors if possible."

    with col2:

        st.metric(
            "Category",
            category
        )

    st.success(recommendation) 
        st.divider()

    st.subheader("📋 Weather Data Used")

    summary = pd.DataFrame({

        "Parameter":[
            "State",
            "District",
            "Station",
            "Average Temp",
            "Minimum Temp",
            "Maximum Temp",
            "Wind Speed",
            "Air Pressure"
        ],

        "Value":[
            latest["state"],
            latest["district"],
            latest["station_name"],
            avg_temp,
            min_temp,
            max_temp,
            wind_speed,
            air_pressure
        ]

    })

    st.dataframe(
        summary,
        use_container_width=True
    )
        st.divider()

    output = pd.DataFrame({

        "State":[latest["state"]],
        "District":[latest["district"]],
        "Predicted Rainfall (mm)":[round(prediction,2)],
        "Category":[category]

    })

    csv = output.to_csv(index=False)

    st.download_button(

        label="⬇ Download Prediction",

        data=csv,

        file_name="rainfall_prediction.csv",

        mime="text/csv"

    )