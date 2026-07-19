import streamlit as st

# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(
    page_title="About",
    page_icon="ℹ️",
    layout="wide"
)

st.title("ℹ️ About the Project")

st.markdown("---")

# -----------------------------------
# PROJECT DESCRIPTION
# -----------------------------------

st.header("🌧 Project Overview")

st.write("""
The **AI-Based Rainfall Prediction System** is a Machine Learning application
developed to predict rainfall using historical weather data.

The model analyzes multiple meteorological parameters such as:

- Temperature
- Wind Speed
- Air Pressure
- Season
- Elevation
- Latitude & Longitude

and predicts the expected rainfall for a selected location.

The main objective of this project is to assist farmers, researchers,
government agencies, and disaster management authorities in making
better decisions based on weather conditions.
""")

st.markdown("---")

# -----------------------------------
# PROBLEM STATEMENT
# -----------------------------------

st.header("🎯 Problem Statement")

st.write("""
Accurate rainfall prediction is important for agriculture,
water resource management, transportation, and disaster preparedness.

Traditional forecasting methods require expensive equipment and
large-scale meteorological analysis.

This project demonstrates how Artificial Intelligence can be used
to predict rainfall using historical weather observations.
""")

st.markdown("---")

# -----------------------------------
# DATASET
# -----------------------------------

st.header("📂 Dataset")

st.write("""
The dataset contains historical weather observations collected
from multiple weather stations across India.

Dataset Features:

- Date
- State
- District
- Station Name
- Average Temperature
- Minimum Temperature
- Maximum Temperature
- Wind Speed
- Air Pressure
- Elevation
- Latitude
- Longitude
- Rainfall
""")

st.markdown("---")

# -----------------------------------
# PROJECT WORKFLOW
# -----------------------------------

st.header("⚙️ Project Workflow")

st.markdown("""
1. Data Collection

2. Data Cleaning

3. Exploratory Data Analysis (EDA)

4. Feature Engineering

5. Feature Selection

6. Model Training

7. Model Evaluation

8. Model Comparison

9. Save Best Model

10. Streamlit Deployment
""")

st.markdown("---")

# -----------------------------------
# MACHINE LEARNING MODELS
# -----------------------------------

st.header("🤖 Models Used")

st.table({

    "Model":[

        "Linear Regression",

        "Random Forest",

        "XGBoost",

        "CNN + BiLSTM"

    ],

    "Purpose":[

        "Baseline Model",

        "Ensemble Learning",

        "Gradient Boosting",

        "Deep Learning"

    ]

})

st.markdown("---")

# -----------------------------------
# TECHNOLOGIES
# -----------------------------------

st.header("🛠 Technologies Used")

c1,c2,c3 = st.columns(3)

with c1:

    st.success("""
Python

Pandas

NumPy

Matplotlib

Seaborn
""")

with c2:

    st.success("""
Scikit-Learn

XGBoost

TensorFlow

Joblib
""")

with c3:

    st.success("""
Streamlit

Google Colab

GitHub

Plotly
""")

st.markdown("---")

# -----------------------------------
# APPLICATIONS
# -----------------------------------

st.header("🌍 Applications")

st.write("""
The proposed system can be useful in:

• Agriculture

• Flood Prediction

• Disaster Management

• Weather Monitoring

• Water Resource Planning

• Climate Research
""")

st.markdown("---")

# -----------------------------------
# FUTURE SCOPE
# -----------------------------------

st.header("🚀 Future Scope")

st.write("""
Future improvements can include:

• Integration with Live Weather APIs

• Satellite Image Analysis

• District-wise Real-time Prediction

• Mobile Application

• Cloud Deployment

• Explainable AI (SHAP)

• 7-Day Rainfall Forecasting
""")

st.markdown("---")

# -----------------------------------
# DEVELOPER
# -----------------------------------

st.header("👨‍💻 Developer")

st.info("""
Project Developed By

Amisha Choudhary

B.Tech Computer Science & Engineering
(Bioinformatics)

Artificial Intelligence Based Rainfall Prediction System
""")

st.markdown("---")

st.caption("© 2026 AI Based Rainfall Prediction System")
