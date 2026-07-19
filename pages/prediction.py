# ==========================================
# PAGE TITLE
# ==========================================

st.title("🌧 Rainfall Prediction")

st.markdown(
    "Select a **State** and **District**, then enter the current weather conditions to predict rainfall."
)

st.divider()

# ==========================================
# STATE SELECTION
# ==========================================

states = sorted(df["state"].unique())

selected_state = st.selectbox(
    "Select State",
    states
)

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