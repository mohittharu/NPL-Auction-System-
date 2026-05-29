import streamlit as st
import pandas as pd
import joblib
import os

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="NPL Auction System",
    page_icon="🏏",
    layout="wide"
)

# =====================================================
# PROFESSIONAL UI
# =====================================================

st.markdown("""
<style>

/* Background */

.stApp{
    background: #f4f7fc;
}

/* Hero Header */

.hero {

    background:
    linear-gradient(
        135deg,
        #0f172a,
        #1e3a8a
    );

    padding: 35px;

    border-radius: 20px;

    text-align: center;

    color: white;

    margin-bottom: 25px;

    box-shadow:
    0 10px 30px rgba(0,0,0,0.2);
}

.hero h1{
    font-size: 45px;
    margin-bottom: 10px;
}

.hero p{
    font-size: 18px;
    opacity: 0.9;
}

/* Cards */

.card {

    background: white;

    border-radius: 18px;

    padding: 20px;

    margin-bottom: 20px;

    box-shadow:
    0px 8px 24px rgba(0,0,0,0.08);

    transition: 0.3s;
}

.card:hover {

    transform: translateY(-4px);

    box-shadow:
    0px 12px 28px rgba(0,0,0,0.15);
}

/* Metrics */

[data-testid="metric-container"] {

    background: white;

    border-radius: 15px;

    padding: 18px;

    border-left: 5px solid #2563eb;

    box-shadow:
    0px 5px 15px rgba(0,0,0,0.08);
}

/* Buttons */

.stButton > button {

    width: 100%;

    height: 50px;

    border-radius: 12px;

    border: none;

    color: white;

    font-weight: bold;

    font-size: 16px;

    background:
    linear-gradient(
        135deg,
        #2563eb,
        #1d4ed8
    );
}

.stButton > button:hover {

    background:
    linear-gradient(
        135deg,
        #1d4ed8,
        #1e40af
    );
}

/* Section Headings */

.section {

    background: white;

    padding: 15px;

    border-radius: 15px;

    font-size: 24px;

    font-weight: bold;

    color: #1e3a8a;

    margin-top: 15px;

    margin-bottom: 15px;

    box-shadow:
    0px 5px 15px rgba(0,0,0,0.08);
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# LOAD DATA
# =====================================================

try:
    df = pd.read_csv("data/npl_data.csv")

    rf = joblib.load(r"C:\Users\acer\OneDrive\Desktop\NPL-Auction-System-\notebooks\models\random_forest_model.pkl")
    feature_columns = joblib.load(r"C:\Users\acer\OneDrive\Desktop\NPL-Auction-System-\notebooks\models\feature_columns.pkl")

except Exception as e:
    st.error(f"Error Loading Files: {e}")
    st.stop()

# =====================================================
# FEATURE ENGINEERING
# =====================================================

df["batting_score"] = (
    df["runs"] * 0.5 +
    df["batting_average"] * 0.3 +
    df["strike_rate"] * 0.2
)

df["bowling_score"] = (
    df["wickets"] * 0.6 -
    df["economy_rate"] * 0.4
)

df["fielding_score"] = (
    df["catches"] +
    df["stumpings"]
)

df["player_score"] = (
    df["batting_score"] +
    df["bowling_score"] +
    df["fielding_score"]
)

# =====================================================
# HEADER
# =====================================================

st.markdown("""
<div class="hero">

<h1>🏏 NPL Auction System</h1>

<p>
AI Powered Player Market Value Prediction
Using Machine Learning
</p>

</div>
""", unsafe_allow_html=True)

# =====================================================
# EXISTING PLAYER
# =====================================================

st.markdown("""
<div class="section">
📊 Existing Player Prediction
</div>
""", unsafe_allow_html=True)

selected_player = st.selectbox(
    "Select Player",
    sorted(df["player"].unique())
)

if st.button("Predict Existing Player"):

    player_data = df[df["player"] == selected_player]

    features = player_data[feature_columns]

    predicted_value = rf.predict(features)[0]

    if predicted_value >= 150:
        category = "A"
    elif predicted_value >= 100:
        category = "B"
    else:
        category = "C"

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Predicted Market Value",
            f"₹ {predicted_value:,.0f}"
        )

    with col2:
        st.metric(
            "Player Category",
            category
        )

# =====================================================
# NEW PLAYER SIMULATION
# =====================================================

st.markdown("""
<div class="section">
🆕 New Player Simulation
</div>
""", unsafe_allow_html=True)

player_name = st.text_input("Player Name")

col1, col2 = st.columns(2)

with col1:
    runs = st.number_input("Runs", min_value=0.0)
    batting_average = st.number_input("Batting Average", min_value=0.0)
    strike_rate = st.number_input("Strike Rate", min_value=0.0)
    catches = st.number_input("Catches", min_value=0.0)

with col2:
    wickets = st.number_input("Wickets", min_value=0.0)
    bowling_average = st.number_input("Bowling Average", min_value=0.0)
    economy_rate = st.number_input("Economy Rate", min_value=0.0)
    stumpings = st.number_input("Stumpings", min_value=0.0)

if st.button("Simulate Auction"):

    new_player = pd.DataFrame(
        [[0] * len(feature_columns)],
        columns=feature_columns
    )

    if "runs" in feature_columns:
        new_player["runs"] = runs

    if "batting_average" in feature_columns:
        new_player["batting_average"] = batting_average

    if "strike_rate" in feature_columns:
        new_player["strike_rate"] = strike_rate

    if "wickets" in feature_columns:
        new_player["wickets"] = wickets

    if "bowling_average" in feature_columns:
        new_player["bowling_average"] = bowling_average

    if "economy_rate" in feature_columns:
        new_player["economy_rate"] = economy_rate

    if "catches" in feature_columns:
        new_player["catches"] = catches

    if "stumpings" in feature_columns:
        new_player["stumpings"] = stumpings

    # Engineered Features

    new_player["batting_score"] = (
        runs * 0.5 +
        batting_average * 0.3 +
        strike_rate * 0.2
    )

    new_player["bowling_score"] = (
        wickets * 0.6 -
        economy_rate * 0.4
    )

    new_player["fielding_score"] = (
        catches +
        stumpings
    )

    new_player["player_score"] = (
        new_player["batting_score"] +
        new_player["bowling_score"] +
        new_player["fielding_score"]
    )

    predicted_value = rf.predict(
        new_player[feature_columns]
    )[0]

    if predicted_value >= 150:
        category = "A"
    elif predicted_value >= 100:
        category = "B"
    else:
        category = "C"

    st.markdown(f"""
<div class="card">

<h2>💰 Predicted Market Value</h2>

<h1>
₹ {predicted_value:,.0f}
</h1>

<h3>
Player Category : {category}
</h3>

</div>
""", unsafe_allow_html=True)

# =====================================================
# FEEDBACK
# =====================================================

st.markdown("""
<div class="section">
⭐ Rating & Feedback
</div>
""", unsafe_allow_html=True)

rating = st.slider(
    "Rate Prediction",
    1,
    5
)

comment = st.text_area(
    "Feedback Comment"
)

if st.button("Submit Feedback"):

    feedback = pd.DataFrame({
        "rating": [rating],
        "stars": ["⭐" * rating],
        "comment": [comment]
    })

    if os.path.exists("feedback.csv"):
        feedback.to_csv(
            "feedback.csv",
            mode="a",
            header=False,
            index=False
        )
    else:
        feedback.to_csv(
            "feedback.csv",
            index=False
        )

    st.success("✅ Feedback Saved")

# =====================================================
# PROJECT STATS
# =====================================================

# =====================================================
# PROJECT STATISTICS
# =====================================================

st.markdown("""
<style>

/* Metric Container */

[data-testid="metric-container"]{
    background:white;
    padding:15px;
    border-radius:15px;
    box-shadow:0px 4px 15px rgba(0,0,0,0.08);
}

/* Label */

[data-testid="stMetricLabel"]{
    color:black !important;
}

/* Value */

[data-testid="stMetricValue"]{
    color:black !important;
}

/* All text inside metrics */

[data-testid="metric-container"] *{
    color:black !important;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# SYSTEM SUMMARY CARD
# =====================================================

st.markdown(f"""
<div style="
background:white;
padding:25px;
border-radius:15px;
box-shadow:0px 8px 24px rgba(0,0,0,0.08);
margin-top:20px;
color:black;
">

<h2 style="color:#1e3a8a;">
📌 System Summary
</h2>

<hr>

<p style="font-size:18px;color:black;">
🏏 <b>Total Players:</b> {len(df)}
</p>

<p style="font-size:18px;color:black;">
📊 <b>Total Features:</b> {len(feature_columns)}
</p>

<p style="font-size:18px;color:black;">
🤖 <b>Prediction Model:</b> Random Forest Regressor
</p>

<p style="font-size:18px;color:black;">
🎯 <b>Target Variable:</b> Market Value
</p>

<p style="font-size:18px;color:black;">
🚀 <b>System Status:</b> Active
</p>

<p style="font-size:18px;color:black;">
⭐ <b>Auction Categories:</b> A, B, C
</p>

</div>
""", unsafe_allow_html=True)