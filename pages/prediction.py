import streamlit as st
import pandas as pd
import joblib

# ============================
# LOAD DATA
# ============================

@st.cache_data
def load_data():

    df = pd.read_excel("data/india_weather_rainfall_data.xlsx")

    df["date_of_record"] = pd.to_datetime(df["date_of_record"])

    # Date features
    df["year"] = df["date_of_record"].dt.year
    df["month_num"] = df["date_of_record"].dt.month
    df["day"] = df["date_of_record"].dt.day
    df["day_of_week"] = df["date_of_record"].dt.dayofweek
    df["week"] = df["date_of_record"].dt.isocalendar().week.astype(int)

    # Sort exactly like training
    df = df.sort_values("date_of_record")

    # Lag features
    df["rainfall_lag1"] = df["rainfall"].shift(1)
    df["rainfall_lag2"] = df["rainfall"].shift(2)
    df["rainfall_lag3"] = df["rainfall"].shift(3)

    # Rolling features
    df["rainfall_roll3"] = df["rainfall"].rolling(3).mean()
    df["rainfall_roll7"] = df["rainfall"].rolling(7).mean()

    # Remove rows with NaN
    df.dropna(inplace=True)

    return df

# ============================
# LOAD MODEL
# ============================

from sklearn.preprocessing import LabelEncoder

@st.cache_resource
def load_model():
    return joblib.load("model/xgboost_model.pkl")

model = load_model()

encoders = {}

for col in ["month", "season", "station_name", "state", "district"]:
    le = LabelEncoder()
    le.fit(df[col].astype(str))
    encoders[col] = le

# Build fresh encoders from the dataset
encoders = {}

for col in ["month", "season", "station_name", "state", "district"]:
    le = LabelEncoder()
    le.fit(df[col].astype(str))
    encoders[col] = le
st.title("🌧 Rainfall Prediction")

st.markdown(
    "Select a **State** and **District**, then enter the current weather conditions to predict rainfall."
)

st.divider()

# ==========================================
# STATE SELECTION
# ==========================================

# Dictionary for state abbreviations
state_mapping = {
    "AP": "Andhra Pradesh",
    "AR": "Arunachal Pradesh",
    "AS": "Assam",
    "BR": "Bihar",
    "CT": "Chhattisgarh",
    "DL": "Delhi",
    "GA": "Goa",
    "GJ": "Gujarat",
    "HR": "Haryana",
    "HP": "Himachal Pradesh",
    "JH": "Jharkhand",
    "KA": "Karnataka",
    "KL": "Kerala",
    "MP": "Madhya Pradesh",
    "MH": "Maharashtra",
    "MN": "Manipur",
    "ML": "Meghalaya",
    "MZ": "Mizoram",
    "NL": "Nagaland",
    "OR": "Odisha",
    "PB": "Punjab",
    "RJ": "Rajasthan",
    "SK": "Sikkim",
    "TN": "Tamil Nadu",
    "TG": "Telangana",
    "TR": "Tripura",
    "UP": "Uttar Pradesh",
    "UK": "Uttarakhand",
    "WB": "West Bengal",
    "AN": "Andaman and Nicobar Islands",
    "CH": "Chandigarh",
    "DD": "Dadra and Nagar Haveli and Daman and Diu",
    "JK": "Jammu and Kashmir",
    "LA": "Ladakh",
    "LD": "Lakshadweep",
    "PY": "Puducherry"
}

# Available abbreviations in your dataset
state_codes = sorted(df["state"].unique())

# Show full names in the dropdown
selected_state_name = st.selectbox(
    "Select State",
    [state_mapping.get(code, code) for code in state_codes]
)

# Convert back to abbreviation for filtering
reverse_mapping = {v: k for k, v in state_mapping.items()}
selected_state = reverse_mapping[selected_state_name]

# ==========================================
# DISTRICT SELECTION
# ==========================================

districts = sorted(
    df[df["state"] == selected_state]["district"].unique()
)

selected_district = st.selectbox(
    "Select District",
    districts
)

# ==========================================
# GET LATEST RECORD
# ==========================================

district_df = df[
    (df["state"] == selected_state) &
    (df["district"] == selected_district)
].sort_values("date_of_record")

latest = district_df.iloc[-1]

# ==========================================
# SHOW LOCATION DETAILS
# ==========================================

st.subheader("📍 Location Information")

col1, col2 = st.columns(2)

with col1:

    st.write("**Station:**", latest["station_name"])

    st.write("**Season:**", latest["season"])

    st.write("**Elevation:**", latest["elevation"], "m")

with col2:

    st.write("**Latitude:**", latest["latitude"])

    st.write("**Longitude:**", latest["longitude"])

    st.write("**Last Recorded Rainfall:**", latest["rainfall"], "mm")

st.divider()

# ==========================================
# WEATHER INPUTS
# ==========================================

st.subheader("🌤 Current Weather")

col1, col2 = st.columns(2)

with col1:

    avg_temp = st.number_input(
        "Average Temperature (°C)",
        value=float(latest["avg_temp"])
    )

    min_temp = st.number_input(
        "Minimum Temperature (°C)",
        value=float(latest["min_temp"])
    )

    max_temp = st.number_input(
        "Maximum Temperature (°C)",
        value=float(latest["max_temp"])
    )

with col2:

    wind_speed = st.number_input(
        "Wind Speed",
        value=float(latest["wind_speed"])
    )

    air_pressure = st.number_input(
        "Air Pressure",
        value=float(latest["air_pressure"])
    )

st.divider()

predict = st.button(
    "🌧 Predict Rainfall",
    use_container_width=True
)
# ==========================================
# PREDICT
# ==========================================

if predict:
    encoded_month = encoders["month"].transform([str(latest["month"])])[0]
    encoded_season = encoders["season"].transform([str(latest["season"])])[0]
    encoded_station = encoders["station_name"].transform([str(latest["station_name"])])[0]
    encoded_state = encoders["state"].transform([str(latest["state"])])[0]
    encoded_district = encoders["district"].transform([str(latest["district"])])[0]

    # Create input dataframe
    input_df = pd.DataFrame([{
        "month": encoded_month,
        "season": encoded_season,
        "station_name": encoded_station,
        "state": encoded_state,
        "district": encoded_district,
    
        "avg_temp": avg_temp,
        "min_temp": min_temp,
        "max_temp": max_temp,
    
        "wind_speed": wind_speed,
        "air_pressure": air_pressure,
    
        "elevation": latest["elevation"],
        "latitude": latest["latitude"],
        "longitude": latest["longitude"],
    
        "year": latest["year"],
        "month_num": latest["month_num"],
        "day": latest["day"],
        "day_of_week": latest["day_of_week"],
        "week": latest["week"],
    
        "rainfall_lag1": latest["rainfall_lag1"],
        "rainfall_lag2": latest["rainfall_lag2"],
        "rainfall_lag3": latest["rainfall_lag3"],
    
        "rainfall_roll3": latest["rainfall_roll3"],
        "rainfall_roll7": latest["rainfall_roll7"]
    }])

    prediction = model.predict(input_df)[0]

    st.divider()

    st.subheader("🌧 Prediction Result")

    st.metric(
        "Predicted Rainfall",
        f"{prediction:.2f} mm"
    )

    if prediction < 0.5:
        st.success("☀ No Rain Expected")

    elif prediction < 10:
        st.info("🌦 Light Rain Expected")

    elif prediction < 30:
        st.warning("🌧 Moderate Rain Expected")

    else:
        st.error("⛈ Heavy Rain Expected")
