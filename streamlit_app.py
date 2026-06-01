import streamlit as st
import pandas as pd
import joblib
import os

st.set_page_config(
    page_title="NPL Auction System",
    page_icon="🏏",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700;800&family=Inter:wght@300;400;500;600&display=swap');

:root {
    --bg:         #0C0E14;
    --surface:    #13161F;
    --card:       #181C28;
    --card-hover: #1E2335;
    --border:     rgba(180,155,90,0.15);
    --border-mid: rgba(180,155,90,0.30);
    --gold:       #C9A84C;
    --gold-light: #E8C97A;
    --gold-dim:   rgba(201,168,76,0.12);
    --crimson:    #C0392B;
    --crimson-dim:rgba(192,57,43,0.12);
    --sapphire:   #1A6EA8;
    --sapphire-dim:rgba(26,110,168,0.12);
    --emerald:    #1A8C5B;
    --emerald-dim:rgba(26,140,91,0.12);
    --text:       #EEE8D8;
    --text-mid:   #A89E86;
    --text-dim:   #665E50;
    --radius:     12px;
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Inter', sans-serif !important;
}
[data-testid="stHeader"]  { background: transparent !important; }
[data-testid="stSidebar"] { background: var(--surface) !important; }
#MainMenu, footer { visibility: hidden; }

/* ── Hero ── */
.hero {
    background: linear-gradient(160deg, #14192B 0%, #0E1220 60%, #13101A 100%);
    border: 1px solid var(--border-mid);
    border-radius: 18px;
    padding: 52px 48px 44px;
    margin-bottom: 36px;
    position: relative;
    overflow: hidden;
}
.hero::after {
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(ellipse 60% 60% at 80% 50%, rgba(201,168,76,0.06) 0%, transparent 70%);
    pointer-events: none;
}
.hero .eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--gold);
    border: 1px solid var(--border-mid);
    background: var(--gold-dim);
    padding: 5px 14px;
    border-radius: 20px;
    margin-bottom: 18px;
}
.hero h1 {
    font-family: 'Playfair Display', serif !important;
    font-size: 3rem !important;
    font-weight: 800 !important;
    color: var(--text) !important;
    margin: 0 0 10px !important;
    letter-spacing: -0.5px;
    line-height: 1.15 !important;
}
.hero h1 span { color: var(--gold); }
.hero p {
    color: var(--text-mid) !important;
    font-size: 1rem !important;
    font-weight: 300 !important;
    margin: 0 !important;
    max-width: 520px;
    line-height: 1.65;
}
.hero-crest {
    position: absolute;
    right: 48px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 110px;
    opacity: 0.07;
    pointer-events: none;
    filter: sepia(1);
}

/* ── Section divider ── */
.sec {
    display: flex;
    align-items: center;
    gap: 14px;
    margin: 36px 0 22px;
}
.sec-line {
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, var(--border-mid), transparent);
}
.sec-label {
    font-family: 'Playfair Display', serif;
    font-size: 1.05rem;
    font-weight: 600;
    color: var(--gold);
    white-space: nowrap;
    letter-spacing: 0.3px;
}

/* ── Result card ── */
.result-wrap {
    background: var(--card);
    border: 1px solid var(--border-mid);
    border-radius: var(--radius);
    padding: 32px 36px;
    margin-top: 18px;
    position: relative;
    overflow: hidden;
}
.result-wrap::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--gold), var(--gold-light), transparent);
}
.result-wrap .label {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--text-dim);
    margin-bottom: 8px;
}
.result-wrap .value {
    font-family: 'Playfair Display', serif;
    font-size: 3rem;
    font-weight: 700;
    color: var(--gold-light);
    line-height: 1;
    margin-bottom: 16px;
}
.cat-pill {
    display: inline-block;
    font-family: 'Playfair Display', serif;
    font-size: 0.9rem;
    font-weight: 700;
    padding: 5px 20px;
    border-radius: 20px;
    letter-spacing: 0.5px;
}
.cat-A { background: rgba(201,168,76,0.15); color: var(--gold-light); border: 1px solid rgba(201,168,76,0.35); }
.cat-B { background: var(--sapphire-dim);   color: #60A8D8;          border: 1px solid rgba(26,110,168,0.4); }
.cat-C { background: var(--emerald-dim);    color: #4EC99A;          border: 1px solid rgba(26,140,91,0.4); }

/* ── Summary card ── */
.sum-card {
    background: var(--card);
    border: 1px solid var(--border-mid);
    border-radius: var(--radius);
    padding: 28px 32px;
    margin-top: 4px;
    position: relative;
    overflow: hidden;
}
.sum-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--gold), transparent);
}
.sum-card .title {
    font-family: 'Playfair Display', serif;
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--text);
    margin-bottom: 20px;
}
.stat-row {
    display: flex;
    align-items: center;
    padding: 11px 0;
    border-bottom: 1px solid var(--border);
    font-size: 0.9rem;
}
.stat-row:last-child { border-bottom: none; }
.stat-icon { color: var(--gold); margin-right: 12px; font-size: 1rem; width: 20px; text-align: center; }
.stat-key  { color: var(--text-mid); flex: 1; }
.stat-val  { color: var(--text); font-weight: 500; }
.live-dot  { color: var(--emerald); font-size: 0.65rem; margin-right: 4px; }

/* ── Widget overrides ── */
.stTextInput label, .stNumberInput label,
.stSelectbox label, .stTextArea label, .stSlider label {
    color: var(--text-mid) !important;
    font-size: 0.72rem !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    letter-spacing: 1.5px;
}
.stTextInput input, .stNumberInput input {
    background: var(--surface) !important;
    color: var(--text) !important;
    border: 1px solid var(--border-mid) !important;
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
}
.stTextInput input:focus, .stNumberInput input:focus {
    border-color: var(--gold) !important;
    box-shadow: 0 0 0 3px rgba(201,168,76,0.12) !important;
}
.stTextArea textarea {
    background: var(--surface) !important;
    color: var(--text) !important;
    border: 1px solid var(--border-mid) !important;
    border-radius: 8px !important;
}
.stTextArea textarea:focus { border-color: var(--gold) !important; }
.stSelectbox div[data-baseweb="select"] > div {
    background: var(--surface) !important;
    border: 1px solid var(--border-mid) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
}
.stButton > button {
    background: linear-gradient(135deg, #B8891E, #C9A84C) !important;
    color: #0C0E14 !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    padding: 10px 28px !important;
    transition: opacity 0.2s, transform 0.15s !important;
}
.stButton > button:hover { opacity: 0.88 !important; transform: translateY(-1px) !important; }
[data-testid="stSliderThumb"] { background: var(--gold) !important; }
[data-testid="metric-container"] {
    background: var(--card) !important;
    border: 1px solid var(--border-mid) !important;
    border-radius: var(--radius) !important;
    padding: 20px 24px !important;
}
[data-testid="stMetricLabel"] p {
    color: var(--text-mid) !important;
    font-size: 0.72rem !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    letter-spacing: 1.5px;
}
[data-testid="stMetricValue"] {
    color: var(--gold-light) !important;
    font-family: 'Playfair Display', serif !important;
    font-weight: 700 !important;
    font-size: 1.8rem !important;
}
[data-testid="stAlert"] {
    background: var(--emerald-dim) !important;
    border: 1px solid rgba(26,140,91,0.3) !important;
    border-radius: 8px !important;
    color: #4EC99A !important;
}
input::placeholder, textarea::placeholder { color: var(--text-dim) !important; }
</style>
""", unsafe_allow_html=True)

# ── Load data ──
try:
    df = pd.read_csv("data/npl_data.csv")
    rf = joblib.load(r"C:\Users\acer\OneDrive\Desktop\NPL-Auction-System-\notebooks\models\random_forest_model.pkl")
    feature_columns = joblib.load(r"C:\Users\acer\OneDrive\Desktop\NPL-Auction-System-\notebooks\models\feature_columns.pkl")
except Exception as e:
    st.error(f"Error Loading Files: {e}")
    st.stop()

# ── Feature engineering ──
df["batting_score"]  = df["runs"] * 0.5 + df["batting_average"] * 0.3 + df["strike_rate"] * 0.2
df["bowling_score"]  = df["wickets"] * 0.6 - df["economy_rate"] * 0.4
df["fielding_score"] = df["catches"] + df["stumpings"]
df["player_score"]   = df["batting_score"] + df["bowling_score"] + df["fielding_score"]

# ── Hero ──
st.markdown("""
<div class="hero">
    <div class="eyebrow">🏏 &nbsp;NPL Auction System &nbsp;·&nbsp; Season 2025</div>
    <h1>Player <span>Market Value</span><br>Intelligence</h1>
    <p>AI-driven valuation and auction category classification powered by Random Forest machine learning.</p>
    <div class="hero-crest">🏆</div>
</div>
""", unsafe_allow_html=True)

# ── Existing Player ──
st.markdown("""
<div class="sec">
    <div class="sec-label">📊 &nbsp;Existing Player Prediction</div>
    <div class="sec-line"></div>
</div>
""", unsafe_allow_html=True)

selected_player = st.selectbox("Select Player", sorted(df["player"].unique()))

if st.button("Predict Market Value", key="btn_existing"):
    player_data    = df[df["player"] == selected_player]
    predicted_value = rf.predict(player_data[feature_columns])[0]
    category = "A" if predicted_value >= 150 else ("B" if predicted_value >= 100 else "C")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Predicted Market Value", f"₹ {predicted_value:,.0f}")
    with col2:
        st.metric("Player Category", category)

# ── New Player Simulation ──
st.markdown("""
<div class="sec">
    <div class="sec-label">🆕 &nbsp;New Player Simulation</div>
    <div class="sec-line"></div>
</div>
""", unsafe_allow_html=True)

player_name = st.text_input("Player Name", placeholder="e.g. Rohit Sharma")

col1, col2 = st.columns(2)
with col1:
    runs            = st.number_input("Runs",            min_value=0.0)
    batting_average = st.number_input("Batting Average", min_value=0.0)
    strike_rate     = st.number_input("Strike Rate",     min_value=0.0)
    catches         = st.number_input("Catches",         min_value=0.0)
with col2:
    wickets         = st.number_input("Wickets",         min_value=0.0)
    bowling_average = st.number_input("Bowling Average", min_value=0.0)
    economy_rate    = st.number_input("Economy Rate",    min_value=0.0)
    stumpings       = st.number_input("Stumpings",       min_value=0.0)

if st.button("Run Auction Simulation", key="btn_simulate"):
    new_player = pd.DataFrame([[0] * len(feature_columns)], columns=feature_columns)
    for col_name, val in [
        ("runs", runs), ("batting_average", batting_average), ("strike_rate", strike_rate),
        ("wickets", wickets), ("bowling_average", bowling_average), ("economy_rate", economy_rate),
        ("catches", catches), ("stumpings", stumpings)
    ]:
        if col_name in feature_columns:
            new_player[col_name] = val

    new_player["batting_score"]  = runs * 0.5 + batting_average * 0.3 + strike_rate * 0.2
    new_player["bowling_score"]  = wickets * 0.6 - economy_rate * 0.4
    new_player["fielding_score"] = catches + stumpings
    new_player["player_score"]   = new_player["batting_score"] + new_player["bowling_score"] + new_player["fielding_score"]

    predicted_value = rf.predict(new_player[feature_columns])[0]
    category = "A" if predicted_value >= 150 else ("B" if predicted_value >= 100 else "C")

    st.markdown(f"""
    <div class="result-wrap">
        <div class="label">Predicted Market Value</div>
        <div class="value">₹ {predicted_value:,.0f}</div>
        <div style="color:var(--text-mid); font-size:0.9rem;">
            Auction Category &nbsp;
            <span class="cat-pill cat-{category}">{category}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Feedback ──
st.markdown("""
<div class="sec">
    <div class="sec-label">⭐ &nbsp;Prediction Feedback</div>
    <div class="sec-line"></div>
</div>
""", unsafe_allow_html=True)

rating  = st.slider("Rate this prediction", 1, 5, value=4)
comment = st.text_area("Your feedback", placeholder="Share your thoughts on prediction accuracy…")

if st.button("Submit Feedback", key="btn_feedback"):
    feedback = pd.DataFrame({"rating": [rating], "stars": ["⭐" * rating], "comment": [comment]})
    if os.path.exists("feedback.csv"):
        feedback.to_csv("feedback.csv", mode="a", header=False, index=False)
    else:
        feedback.to_csv("feedback.csv", index=False)
    st.success("✅ Feedback saved — thank you!")

# ── System Summary ──
st.markdown("""
<div class="sec">
    <div class="sec-label">📌 &nbsp;System Summary</div>
    <div class="sec-line"></div>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="sum-card">
    <div class="title">System Overview</div>
    <div class="stat-row"><span class="stat-icon">🏏</span><span class="stat-key">Total Players</span><span class="stat-val">{len(df)}</span></div>
    <div class="stat-row"><span class="stat-icon">📊</span><span class="stat-key">Total Features</span><span class="stat-val">{len(feature_columns)}</span></div>
    <div class="stat-row"><span class="stat-icon">🤖</span><span class="stat-key">Prediction Model</span><span class="stat-val">Random Forest Regressor</span></div>
    <div class="stat-row"><span class="stat-icon">🎯</span><span class="stat-key">Target Variable</span><span class="stat-val">Market Value</span></div>
    <div class="stat-row"><span class="stat-icon">🚀</span><span class="stat-key">System Status</span><span class="stat-val"><span class="live-dot">●</span> Active</span></div>
    <div class="stat-row"><span class="stat-icon">⭐</span><span class="stat-key">Auction Categories</span><span class="stat-val">A &nbsp;·&nbsp; B &nbsp;·&nbsp; C</span></div>
</div>
""", unsafe_allow_html=True)
