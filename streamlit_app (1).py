import streamlit as st
import pandas as pd
import joblib
from pathlib import Path
from database.connection import conn, cursor

st.set_page_config(
    page_title="NPL Auction System",
    page_icon="🏏",
    layout="wide",
)
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    :root {
        --bg: #F3F5F8;
        --surface: #FFFFFF;
        --sidebar: #F7F8FA;
        --border: #E5E7EB;
        --border-soft: #ECEEF2;
        --crimson: #C8102E;
        --crimson-hover: #A80D26;
        --crimson-soft: #FBE9EC;
        --crimson-mid: #F1CBD4;
        --text: #111827;
        --text-mid: #6B7280;
        --text-dim: #9CA3AF;
        --blue: #2563EB;
        --blue-soft: #EEF4FF;
        --radius: 10px;
        --radius-lg: 14px;
    }

    html, body, [data-testid="stAppViewContainer"] {
        background: linear-gradient(180deg, #f7f8fb 0%, #f2f4f7 100%) !important;
        color: var(--text) !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }
    [data-testid="stHeader"] { background: transparent !important; }
    [data-testid="stMain"] { padding-top: 0.35rem; }
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 2.2rem !important;
        max-width: 1200px !important;
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8f9fb 0%, #f4f5f7 100%) !important;
        border-right: 1px solid var(--border) !important;
        padding-top: 12px !important;
        box-shadow: 1px 0 0 rgba(17, 24, 39, 0.02) !important;
    }
    [data-testid="stSidebar"] * { color: var(--text) !important; }
    [data-testid="stSidebar"] .stRadio > label {
        display: none !important;
    }
    #MainMenu, footer { visibility: hidden; }

    /* Brand */
    .brand-row {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 8px 6px 16px;
        margin-bottom: 6px;
    }
    .brand-mark {
        width: 38px;
        height: 38px;
        border-radius: 10px;
        background: linear-gradient(135deg, #D61A35, #A50F24);
        display: flex;
        align-items: center;
        justify-content: center;
        color: #fff;
        font-size: 1.05rem;
        box-shadow: 0 4px 12px rgba(200, 16, 46, 0.28);
        flex-shrink: 0;
    }
    .brand-name {
        font-size: 1.15rem;
        font-weight: 800;
        color: var(--crimson) !important;
        letter-spacing: -0.02em;
        line-height: 1.2;
    }
    .brand-tag {
        font-size: 0.72rem;
        color: var(--text-mid) !important;
        font-weight: 500;
    }

    /* Sidebar navigation */
    [data-testid="stSidebar"] .stRadio > div[role="radiogroup"] {
        display: flex;
        flex-direction: column;
        gap: 2px;
        padding: 2px 2px 0;
    }
    [data-testid="stSidebar"] .stRadio > div[role="radiogroup"] label {
        background: transparent !important;
        border: none !important;
        border-radius: 0 !important;
        padding: 8px 10px 8px 12px !important;
        margin: 0;
        transition: all 0.16s ease;
        cursor: pointer;
        font-weight: 700 !important;
        font-size: 0.93rem !important;
        color: var(--text-mid) !important;
        display: flex;
        align-items: center;
        box-shadow: none !important;
    }
    [data-testid="stSidebar"] .stRadio > div[role="radiogroup"] label:hover {
        background: transparent !important;
        color: var(--text) !important;
    }
    [data-testid="stSidebar"] .stRadio > div[role="radiogroup"] label[data-checked="true"],
    [data-testid="stSidebar"] .stRadio > div[role="radiogroup"] label:has(input:checked) {
        background: transparent !important;
        color: var(--crimson) !important;
        box-shadow: none !important;
        font-weight: 800 !important;
    }
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label > div:first-child {
        display: none !important;
    }
    [data-testid="stSidebar"] input[type="radio"] {
        display: none !important;
    }
    .sidebar-footer {
        margin-top: 24px;
        padding: 12px 8px 0;
        border-top: 1px solid var(--border);
        font-size: 0.78rem;
        color: var(--text-mid) !important;
        line-height: 1.45;
        font-weight: 600;
    }
    .sidebar-note {
        background: transparent;
        border: none;
        border-left: 2px solid var(--border);
        border-radius: 0;
        padding: 0 0 0 12px;
        color: var(--text-mid) !important;
        font-size: 0.84rem;
        line-height: 1.45;
        margin-top: 8px;
    }

    /* Top bar */
    .top-bar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 16px;
        margin-bottom: 14px;
        padding: 14px 16px;
        background: linear-gradient(135deg, #ffffff 0%, #fdfdfe 100%);
        border: 1px solid var(--border);
        border-radius: 14px;
        box-shadow: 0 2px 10px rgba(15, 23, 42, 0.03);
    }
    .top-bar-copy {
        display: flex;
        flex-direction: column;
        gap: 2px;
    }
    .top-bar-kicker {
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: var(--crimson);
    }
    .top-bar-title {
        font-size: 1.35rem;
        font-weight: 800;
        color: var(--text);
        letter-spacing: -0.02em;
        margin: 0;
    }
    .top-bar-subtitle {
        font-size: 0.9rem;
        color: var(--text-mid);
        font-weight: 500;
    }
    .format-chip {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: linear-gradient(135deg, #fff 0%, #fff7f8 100%);
        border: 1px solid #F0D6DB;
        border-radius: 999px;
        padding: 6px 12px;
        font-size: 0.8rem;
        font-weight: 700;
        color: var(--crimson);
        white-space: nowrap;
        box-shadow: 0 1px 2px rgba(15, 23, 42, 0.03);
    }

    /* Main panel */
    .main-panel {
        background: transparent !important;
        border: none !important;
        border-radius: 0 !important;
        padding: 0 !important;
        box-shadow: none !important;
        margin-bottom: 0 !important;
    }
    .section-head {
        display: flex;
        align-items: flex-start;
        justify-content: space-between;
        gap: 12px;
        flex-wrap: wrap;
        margin-bottom: 12px;
        padding-bottom: 8px;
        border-bottom: 1px solid var(--border-soft);
    }
    .section-title {
        font-size: 1rem;
        font-weight: 800;
        color: var(--text);
        margin: 0 0 3px;
        letter-spacing: -0.01em;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .section-title .star {
        color: var(--crimson);
        font-size: 0.95rem;
    }
    .section-subtitle {
        color: var(--text-mid);
        font-size: 0.84rem;
        margin: 0;
        font-weight: 500;
    }

    /* Hero / page intro */
    .hero {
        background: transparent;
        border: none;
        border-radius: 0;
        padding: 0 0 16px;
        margin-bottom: 16px;
        box-shadow: none;
    }
    .eyebrow {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        color: var(--crimson);
        background: var(--crimson-soft);
        padding: 5px 11px;
        border-radius: 999px;
        margin-bottom: 10px;
    }
    .hero h1 {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 1.65rem !important;
        font-weight: 800 !important;
        color: var(--text) !important;
        margin: 0 0 6px !important;
        letter-spacing: -0.03em !important;
        line-height: 1.25 !important;
    }
    .hero h1 span { color: var(--crimson); }
    .hero p {
        color: var(--text-mid) !important;
        margin: 0 !important;
        max-width: 640px;
        font-size: 0.92rem;
        font-weight: 500;
    }

    .page-header {
        margin: 0 0 12px;
        padding-bottom: 8px;
    }
    .page-badge {
        display: inline-block;
        font-size: 0.68rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: var(--crimson);
        background: var(--crimson-soft);
        padding: 4px 9px;
        border-radius: 999px;
        margin-bottom: 7px;
    }
    .page-title {
        font-size: 1.28rem;
        font-weight: 800;
        color: var(--text);
        margin-bottom: 3px;
        letter-spacing: -0.02em;
    }
    .page-subtitle {
        color: var(--text-mid);
        font-size: 0.9rem;
        font-weight: 500;
    }

    .panel-card {
        background: transparent;
        border: none;
        border-radius: 0;
        padding: 0;
        margin-top: 14px;
        box-shadow: none;
    }

    /* KPI / player-style cards */
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: 12px;
        margin: 8px 0 16px;
    }
    .kpi-card {
        background: #FFF;
        border: 1px solid var(--border-soft);
        border-radius: 10px;
        padding: 14px 15px;
        min-height: 100px;
        border-left: 3px solid transparent;
        transition: border-color 0.15s ease, box-shadow 0.15s ease, transform 0.15s ease;
    }
    .kpi-card:hover {
        border-color: #F0C8D1;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.05);
        transform: translateY(-1px);
    }
    .kpi-card.gold { border-left: 3px solid var(--crimson); }
    .kpi-card.blue { border-left: 3px solid var(--blue); }
    .kpi-card.green { border-left: 3px solid #059669; }
    .kpi-label {
        color: var(--text-dim);
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        margin-bottom: 8px;
    }
    .kpi-value {
        font-size: 1.45rem;
        font-weight: 800;
        color: var(--text);
        margin-bottom: 4px;
        letter-spacing: -0.03em;
    }
    .kpi-subtitle {
        color: var(--text-mid);
        font-size: 0.84rem;
        line-height: 1.35;
        font-weight: 500;
    }

    /* Rating banner */
    .rating-banner {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 12px;
        background: #FFF7F8;
        border: 1px solid #F7D7DD;
        border-radius: 12px;
        padding: 14px 18px;
        margin: 12px 0 18px;
    }
    .rating-banner-left {
        display: flex;
        align-items: center;
        gap: 10px;
        font-weight: 700;
        color: var(--text);
        font-size: 0.95rem;
    }
    .rating-banner-left .icon {
        width: 32px;
        height: 32px;
        border-radius: 8px;
        background: #fff;
        border: 1px solid var(--crimson-mid);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.95rem;
    }
    .rating-banner-score {
        font-size: 1.45rem;
        font-weight: 800;
        color: var(--crimson);
        letter-spacing: -0.03em;
    }

    .result-wrap {
        background: linear-gradient(135deg, #fff7f8 0%, #ffffff 100%);
        border: 1px solid #F7D7DD;
        border-radius: 12px;
        padding: 22px 24px;
        margin-top: 12px;
        box-shadow: 0 3px 10px rgba(200, 16, 46, 0.04);
    }
    .result-wrap .label {
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: var(--text-mid);
    }
    .result-wrap .value {
        font-size: 2rem;
        font-weight: 800;
        color: var(--crimson);
        margin: 6px 0;
        letter-spacing: -0.03em;
    }
    .cat-pill {
        display: inline-block;
        font-size: 0.85rem;
        font-weight: 700;
        padding: 4px 12px;
        border-radius: 999px;
        letter-spacing: 0.02em;
    }
    .cat-A { background: var(--crimson-soft); color: var(--crimson); border: 1px solid var(--crimson-mid); }
    .cat-B { background: var(--blue-soft); color: var(--blue); border: 1px solid #BFDBFE; }
    .cat-C { background: #ECFDF5; color: #059669; border: 1px solid #A7F3D0; }

    /* Player mini-cards for tables context */
    .player-card {
        background: #FFF;
        border: 1px solid var(--border-soft);
        border-radius: 10px;
        padding: 12px 13px;
        margin-bottom: 0;
        box-shadow: 0 2px 6px rgba(15, 23, 42, 0.03);
    }
    .player-card-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 8px;
        margin-bottom: 8px;
    }
    .player-name {
        font-weight: 700;
        font-size: 0.98rem;
        color: var(--text);
    }
    .player-rating {
        font-weight: 700;
        font-size: 0.9rem;
        color: #D97706;
        white-space: nowrap;
    }
    .role-pill {
        display: inline-block;
        font-size: 0.72rem;
        font-weight: 700;
        padding: 3px 9px;
        border-radius: 999px;
        margin-bottom: 10px;
    }
    .role-bat { background: var(--crimson-soft); color: var(--crimson); }
    .role-bowl { background: var(--blue-soft); color: var(--blue); }
    .role-all { background: #ECFDF5; color: #059669; }
    .player-stats {
        display: flex;
        gap: 18px;
        font-size: 0.84rem;
        color: var(--text-mid);
    }
    .player-stats strong {
        color: var(--text);
        font-weight: 700;
    }

    /* Form controls */
    .stTextInput label, .stNumberInput label, .stSelectbox label, .stTextArea label, .stSlider label {
        color: var(--text-mid) !important;
        font-size: 0.78rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.02em;
    }
    .stTextInput input, .stNumberInput input, .stTextArea textarea,
    .stSelectbox div[data-baseweb="select"] > div {
        background: var(--surface) !important;
        color: var(--text) !important;
        border: 1px solid var(--border) !important;
        border-radius: 10px !important;
        padding: 8px 10px !important;
        box-shadow: none !important;
    }
    .stNumberInput div[data-testid="stNumberInputStepContainer"] {
        gap: 4px !important;
    }
    .stNumberInput button {
        background: #FFF7F8 !important;
        border: 1px solid #F7D7DD !important;
        color: var(--crimson) !important;
        border-radius: 8px !important;
        min-width: 30px !important;
        min-height: 30px !important;
        padding: 0 !important;
    }
    .stNumberInput button:hover {
        background: #FDE8EC !important;
        border-color: var(--crimson-mid) !important;
    }
    .stNumberInput button:focus {
        box-shadow: none !important;
    }
    .stButton > button {
        background: var(--crimson) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        padding: 9px 16px !important;
        box-shadow: 0 1px 3px rgba(200, 16, 46, 0.14) !important;
        transition: background 0.15s ease, transform 0.1s ease !important;
    }
    .stButton > button:hover {
        background: var(--crimson-hover) !important;
        color: #FFFFFF !important;
        border: none !important;
    }
    .stButton > button:focus {
        box-shadow: 0 0 0 3px rgba(200, 16, 46, 0.2) !important;
    }
    /* Form submit (Run Auction Simulation) */
    [data-testid="stForm"] button,
    .stFormSubmitButton > button,
    button[kind="secondaryFormSubmit"],
    button[kind="primaryFormSubmit"],
    [data-testid="stBaseButton-secondaryFormSubmit"],
    [data-testid="stBaseButton-primaryFormSubmit"] {
        background: var(--crimson) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        padding: 10px 20px !important;
        box-shadow: 0 4px 14px rgba(200, 16, 46, 0.25) !important;
    }
    [data-testid="stForm"] button *,
    .stFormSubmitButton > button *,
    button[kind="secondaryFormSubmit"] *,
    button[kind="primaryFormSubmit"] *,
    [data-testid="stBaseButton-secondaryFormSubmit"] *,
    [data-testid="stBaseButton-primaryFormSubmit"] * {
        color: #FFFFFF !important;
    }
    [data-testid="stForm"] button:hover,
    .stFormSubmitButton > button:hover {
        background: var(--crimson-hover) !important;
        color: #FFFFFF !important;
    }
    [data-testid="metric-container"] {
        background: var(--surface) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius) !important;
        box-shadow: none !important;
        padding: 12px 14px !important;
    }
    [data-testid="stMetricValue"] { color: var(--crimson) !important; font-weight: 800 !important; }
    [data-testid="stMetricLabel"] { color: var(--text-mid) !important; }
    div[data-testid="stDataFrame"] {
        border: 1px solid var(--border) !important;
        border-radius: 10px !important;
        overflow: hidden !important;
    }
    div[data-testid="stDataFrame"] thead th {
        background: #F8FAFC !important;
        color: #4B5563 !important;
        font-weight: 700 !important;
        border-bottom: 1px solid #E5E7EB !important;
    }
    div[data-testid="stDataFrame"] td {
        padding-top: 8px !important;
        padding-bottom: 8px !important;
    }
    [data-testid="stSidebar"] hr {
        border-color: var(--border) !important;
        margin: 14px 0 !important;
    }
    /* Alerts / warnings — readable text on light banners */
    .stAlert,
    div[data-testid="stAlert"],
    [data-testid="stNotification"] {
        border-radius: 10px !important;
    }
    .stAlert *,
    div[data-testid="stAlert"] *,
    [data-testid="stNotification"] *,
    div[data-testid="stAlert"] p,
    div[data-testid="stAlert"] span,
    div[data-testid="stAlert"] [data-testid="stMarkdownContainer"] * {
        color: #5C3D0A !important;
    }
    div[data-testid="stAlert"][kind="error"] *,
    div[data-testid="stAlert"] [data-testid="stAlertContentError"] * {
        color: #7F1D1D !important;
    }
    div[data-testid="stAlert"][kind="success"] *,
    div[data-testid="stAlert"] [data-testid="stAlertContentSuccess"] * {
        color: #14532D !important;
    }
    div[data-testid="stAlert"][kind="info"] *,
    div[data-testid="stAlert"] [data-testid="stAlertContentInfo"] * {
        color: #1E3A5F !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "npl_data.csv"
MODEL_PATH = BASE_DIR / "notebooks" / "models" / "random_forest_model.pkl"
FEATURE_COLUMNS_PATH = BASE_DIR / "notebooks" / "models" / "feature_columns.pkl"
FEEDBACK_PATH = BASE_DIR / "feedback.csv"

try:
    df = pd.read_csv(DATA_PATH)
    rf = joblib.load(MODEL_PATH)
    # Prefer the model's own feature names — feature_columns.pkl can be outdated
    if hasattr(rf, "feature_names_in_"):
        feature_columns = list(rf.feature_names_in_)
    else:
        feature_columns = joblib.load(FEATURE_COLUMNS_PATH)
except Exception as e:
    st.error(f"Error Loading Files: {e}")
    st.stop()

player_df = df.copy()
if "player" in player_df.columns:
    player_df["player"] = player_df["player"].astype(str).str.strip()
player_df["batting_score"] = player_df["runs"] * 0.5 + player_df["batting_average"] * 0.3 + player_df["strike_rate"] * 0.2
player_df["bowling_score"] = player_df["wickets"] * 0.6 - player_df["economy_rate"] * 0.4
player_df["fielding_score"] = player_df["catches"] + player_df["stumpings"]
player_df["player_score"] = player_df["batting_score"] + player_df["bowling_score"] + player_df["fielding_score"]


def get_category(value: float) -> str:
    """Category for composite player_score (used in Insights)."""
    if value >= 150:
        return "A"
    if value >= 100:
        return "B"
    return "C"


def get_market_category(value: float) -> str:
    """Category for predicted market value (rupees)."""
    if value >= 1_500_000:
        return "A"
    if value >= 750_000:
        return "B"
    return "C"


def format_currency(value: float) -> str:
    return f"₹ {value:,.0f}"


def score_to_rating(score: float, max_score: float) -> float:
    if max_score <= 0:
        return 0.0
    return round(min(10.0, max(0.0, (score / max_score) * 10)), 1)


def render_kpi_card(title: str, value: str, subtitle: str, accent: str = "gold") -> None:
    st.markdown(
        f"""
        <div class="kpi-card {accent}">
            <div class="kpi-label">{title}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-subtitle">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def predict_value(row_df: pd.DataFrame) -> float:
    """Build a model-ready row with all trained features, then predict."""
    if isinstance(row_df, pd.Series):
        row_df = row_df.to_frame().T
    if row_df.empty:
        raise ValueError("No player row available for prediction.")

    features = pd.DataFrame(0.0, index=[0], columns=feature_columns)
    source = row_df.iloc[0]
    for col in feature_columns:
        if col in row_df.columns:
            val = source[col]
            features.at[0, col] = 0.0 if pd.isna(val) else float(val)
    return float(rf.predict(features)[0])


def build_simulation_features(
    runs: float,
    batting_average: float,
    strike_rate: float,
    wickets: float,
    bowling_average: float,
    economy_rate: float,
    catches: float,
    stumpings: float,
) -> pd.DataFrame:
    """
    Build a full model feature row from the simulation form.
    Fills related cricket stats so the model is not stuck on an all-zero profile.
    """
    row = {col: 0.0 for col in feature_columns}

    row["runs"] = float(runs)
    row["batting_average"] = float(batting_average)
    row["strike_rate"] = float(strike_rate)
    row["wickets"] = float(wickets)
    row["bowling_average"] = float(bowling_average)
    row["economy_rate"] = float(economy_rate)
    row["catches"] = float(catches)
    row["stumpings"] = float(stumpings)

    # Derive correlated features the model was trained on
    if strike_rate > 0 and runs > 0:
        row["balls_faced"] = (runs / strike_rate) * 100.0
    if batting_average > 0 and runs > 0:
        outs = max(runs / batting_average, 1.0)
        row["innings_batted"] = max(outs, 1.0)
        row["not_out"] = max(row["innings_batted"] * 0.15, 0.0)
        row["matches_played"] = max(row["innings_batted"] * 1.1, 1.0)
    elif wickets > 0:
        row["matches_played"] = max(wickets * 1.5, 1.0)
    else:
        row["matches_played"] = 1.0 if (runs > 0 or catches > 0 or stumpings > 0) else 0.0

    row["highest_inns_score"] = min(runs, max(batting_average * 2.5, runs * 0.25, 0.0)) if runs > 0 else 0.0
    row["hundreds_scored"] = float(runs // 100)
    row["fifties_scored"] = float(max((runs // 50) - row["hundreds_scored"], 0))
    row["boundary_fours"] = float(runs * 0.08) if runs > 0 else 0.0
    row["boundary_sixes"] = float(runs * 0.03) if runs > 0 else 0.0

    if wickets > 0:
        row["innings_bowled"] = max(wickets * 1.2, 1.0)
        row["bowl_matches"] = max(row["innings_bowled"], row["matches_played"])
        if bowling_average > 0:
            row["conceded"] = wickets * bowling_average
        elif economy_rate > 0:
            row["conceded"] = economy_rate * max(wickets * 4.0, 4.0)
        if economy_rate > 0 and row["conceded"] > 0:
            row["overs"] = row["conceded"] / economy_rate
            row["balls"] = row["overs"] * 6.0
        if bowling_average > 0 and economy_rate > 0:
            row["bowling_strike_rate"] = (bowling_average / economy_rate) * 6.0
        row["four_wickets"] = float(wickets // 4)
        row["five_wickets"] = float(wickets // 5)
        row["best_wickets"] = min(wickets, 5.0)
        row["best_runs"] = row["best_wickets"] * max(bowling_average, economy_rate * 4.0, 10.0)

    row["field_matches"] = row["matches_played"]
    row["field_innings"] = row["matches_played"]
    row["maximum_innings_catches"] = min(catches, 4.0) if catches > 0 else 0.0
    row["catches_per_innings"] = (catches / row["field_innings"]) if row["field_innings"] > 0 else 0.0

    if stumpings > 0 or catches > 0:
        row["wk_matches"] = row["matches_played"]
        row["innings_as_keeper"] = row["matches_played"]
        row["dismissed"] = catches + stumpings
        row["caught_as_a_keeper"] = catches
        row["maximum_dismissals_per_innings"] = min(catches + stumpings, 5.0)
        row["dismissials_per_innings"] = (
            (catches + stumpings) / row["innings_as_keeper"] if row["innings_as_keeper"] > 0 else 0.0
        )

    row["batting_score"] = runs * 0.5 + batting_average * 0.3 + strike_rate * 0.2
    row["bowling_score"] = wickets * 0.6 - economy_rate * 0.4
    row["fielding_score"] = catches + stumpings
    row["player_score"] = row["batting_score"] + row["bowling_score"] + row["fielding_score"]

    return pd.DataFrame([{col: row.get(col, 0.0) for col in feature_columns}])


def render_page_header(title: str, subtitle: str) -> None:
    st.markdown(
        f"""
        <div class="page-header">
            <div class="page-badge">Auction Dashboard</div>
            <div class="page-title">{title}</div>
            <div class="page-subtitle">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_top_bar(title: str, subtitle: str) -> None:
    st.markdown(
        f"""
        <div class="top-bar">
            <div class="top-bar-copy">
                <div class="top-bar-kicker">NPL Auction System</div>
                <h1 class="top-bar-title">{title}</h1>
                <div class="top-bar-subtitle">{subtitle}</div>
            </div>
            <div class="format-chip">📊 NPL Auction</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_player_card(name: str, rating: float, role: str, role_class: str, stat_a: str, val_a: str, stat_b: str, val_b: str) -> None:
    st.markdown(
        f"""
        <div class="player-card">
            <div class="player-card-top">
                <div class="player-name">{name}</div>
                <div class="player-rating">★ {rating}</div>
            </div>
            <div class="role-pill {role_class}">{role}</div>
            <div class="player-stats">
                <span>{stat_a}: <strong>{val_a}</strong></span>
                <span>{stat_b}: <strong>{val_b}</strong></span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


if "page" not in st.session_state:
    st.session_state.page = "Data Overview"

st.sidebar.markdown(
    """
    <div class="brand-row">
        <div class="brand-mark">🏏</div>
        <div>
            <div class="brand-name">NPL Auction</div>
            <div class="brand-tag">Intelligence Hub</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

page = st.sidebar.radio(
    "Navigation",
    ["Data Overview", "ML Predictions", "Player Comparison", "Market Insights"],
    index=0,
    key="page",
)

st.sidebar.divider()
st.sidebar.markdown(
    '<div class="sidebar-note">Switch views to inspect rankings, predict values, compare stars, and review auction insights.</div>',
    unsafe_allow_html=True,
)
st.sidebar.markdown(
    '<div class="sidebar-footer">Designed for smart NPL bidding decisions</div>',
    unsafe_allow_html=True,
)

max_player_score = float(player_df["player_score"].max()) if len(player_df) else 1.0

if page == "Data Overview":
    render_top_bar("Data Overview", "Player pool overview and market signals")
    st.markdown('<div class="main-panel">', unsafe_allow_html=True)
    render_page_header("Auction Overview", "A practical view of the talent pool and the current market signals.")

    avg_rating = score_to_rating(float(player_df["player_score"].mean()), max_player_score)
    st.markdown(
        f"""
        <div class="rating-banner">
            <div class="rating-banner-left">
                <div class="icon">🛡</div>
                <span>League Strength Index</span>
            </div>
            <div class="rating-banner-score">{avg_rating}/10</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    kpi_cols = st.columns(3)
    with kpi_cols[0]:
        render_kpi_card("Players", f"{len(player_df):,}", "Registered talent profiles", "gold")
    with kpi_cols[1]:
        top_value = player_df["player_score"].max()
        render_kpi_card("Top Score", f"{top_value:,.1f}", "Highest composite valuation signal", "blue")
    with kpi_cols[2]:
        avg_value = player_df["player_score"].mean()
        render_kpi_card("Average", f"{avg_value:,.1f}", "Overall league benchmark", "green")

    st.markdown(
        """
        <div class="section-head">
            <div>
                <div class="section-title"><span class="star">★</span> Top Market Value Candidates</div>
                <p class="section-subtitle">Highest composite scores across the auction pool</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    top_candidates = player_df.nlargest(8, "player_score").copy()
    card_rows = [top_candidates.iloc[i:i + 2] for i in range(0, min(8, len(top_candidates)), 2)]
    for chunk in card_rows:
        cols = st.columns(2)
        for col, (_, row) in zip(cols, chunk.iterrows()):
            with col:
                is_bowler = row["wickets"] >= row["runs"] * 0.05 and row["wickets"] > 0 and row["runs"] < 500
                if is_bowler:
                    role, role_class = "Bowler", "role-bowl"
                    stat_a, val_a = "Wickets", f"{int(row['wickets'])}"
                    stat_b, val_b = "Econ", f"{row['economy_rate']:.2f}"
                elif row["stumpings"] > 0:
                    role, role_class = "WK", "role-bat"
                    stat_a, val_a = "Runs", f"{int(row['runs'])}"
                    stat_b, val_b = "Avg", f"{row['batting_average']:.1f}"
                elif row["wickets"] > 0 and row["runs"] > 200:
                    role, role_class = "All-rounder", "role-all"
                    stat_a, val_a = "Runs", f"{int(row['runs'])}"
                    stat_b, val_b = "Wkts", f"{int(row['wickets'])}"
                else:
                    role, role_class = "Batter", "role-bat"
                    stat_a, val_a = "Runs", f"{int(row['runs'])}"
                    stat_b, val_b = "Avg", f"{row['batting_average']:.1f}"
                rating = score_to_rating(float(row["player_score"]), max_player_score)
                render_player_card(row["player"], rating, role, role_class, stat_a, val_a, stat_b, val_b)

    st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Auction Snapshot</div>', unsafe_allow_html=True)
    st.markdown('<p class="section-subtitle">Sorted by composite valuation signal</p>', unsafe_allow_html=True)
    snapshot = player_df[["player", "runs", "wickets", "batting_average", "economy_rate", "player_score"]].copy()
    snapshot = snapshot.sort_values("player_score", ascending=False).head(6)
    snapshot.columns = ["Player", "Runs", "Wickets", "Batting Avg", "Economy", "Composite Score"]
    st.dataframe(snapshot, width="stretch", hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)

elif page == "ML Predictions":
    render_top_bar("ML Predictions", "Live valuation estimates and simulation workspace")
    st.markdown('<div class="main-panel">', unsafe_allow_html=True)
    render_page_header("Prediction Studio", "Estimate value for existing players and simulate new auction profiles.")

    st.markdown(
        """
        <div class="section-head">
            <div>
                <div class="section-title"><span class="star">★</span> Existing Player Prediction</div>
                <p class="section-subtitle">Select a player and generate an AI market valuation</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    selected_player = st.selectbox("Select a player", sorted(player_df["player"].unique()))

    if st.button("Predict Market Value", key="btn_existing"):
        player_row = player_df[player_df["player"] == selected_player]
        predicted_value = predict_value(player_row)
        category = get_market_category(predicted_value)
        st.markdown(
            f"""
            <div class="result-wrap">
                <div class="label">Predicted Market Value</div>
                <div class="value">{format_currency(predicted_value)}</div>
                <div style="color:var(--text-mid); font-size:0.95rem; font-weight:500;">
                    Auction Category <span class="cat-pill cat-{category}">{category}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown('<div style="height:18px"></div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="section-head">
            <div>
                <div class="section-title"><span class="star">★</span> New Player Simulation</div>
                <p class="section-subtitle">Enter stats, then submit the form — empty stats will not produce a valuation</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if "simulation_result" not in st.session_state:
        st.session_state.simulation_result = None

    with st.form("new_player_simulation_form", clear_on_submit=False):
        player_name = st.text_input("Player Name", placeholder="e.g. Rohit Sharma", key="sim_player_name")

        col1, col2 = st.columns(2)
        with col1:
            runs = st.number_input("Runs", min_value=0.0, value=0.0, step=1.0, key="sim_runs")
            batting_average = st.number_input("Batting Average", min_value=0.0, value=0.0, step=0.1, key="sim_bat_avg")
            strike_rate = st.number_input("Strike Rate", min_value=0.0, value=0.0, step=0.1, key="sim_strike")
            catches = st.number_input("Catches", min_value=0.0, value=0.0, step=1.0, key="sim_catches")
        with col2:
            wickets = st.number_input("Wickets", min_value=0.0, value=0.0, step=1.0, key="sim_wickets")
            bowling_average = st.number_input("Bowling Average", min_value=0.0, value=0.0, step=0.1, key="sim_bowl_avg")
            economy_rate = st.number_input("Economy Rate", min_value=0.0, value=0.0, step=0.1, key="sim_economy")
            stumpings = st.number_input("Stumpings", min_value=0.0, value=0.0, step=1.0, key="sim_stumpings")

        simulate_clicked = st.form_submit_button(
            "Run Auction Simulation",
            type="primary",
            use_container_width=False,
        )

    if simulate_clicked:
        has_signal = any(v > 0 for v in [runs, batting_average, strike_rate, wickets, bowling_average, economy_rate, catches, stumpings])
        if not has_signal:
            st.session_state.simulation_result = None
            st.warning("Enter at least one stat greater than 0 before running the simulation.")
        else:
            new_player = build_simulation_features(
                runs=runs,
                batting_average=batting_average,
                strike_rate=strike_rate,
                wickets=wickets,
                bowling_average=bowling_average,
                economy_rate=economy_rate,
                catches=catches,
                stumpings=stumpings,
            )
            predicted_value = predict_value(new_player)
            category = get_market_category(predicted_value)
            try:
                cursor.execute(
                    """
                    INSERT INTO prediction_history
                    (
                        player_name,
                        runs,
                        batting_average,
                        strike_rate,
                        wickets,
                        bowling_average,
                        economy_rate,
                        catches,
                        stumpings,
                        predicted_market_value,
                        predicted_category
                    )
                    VALUES (?,?,?,?,?,?,?,?,?,?,?)
                    """,
                    (
                        player_name,
                        runs,
                        batting_average,
                        strike_rate,
                        wickets,
                        bowling_average,
                        economy_rate,
                        catches,
                        stumpings,
                        predicted_value,
                        category
                    )
                )

                conn.commit()

            except Exception as e:
                st.error(f"Database Error: {e}")
            st.session_state.simulation_result = {
                "value": predicted_value,
                "category": category,
                "name": player_name.strip() if player_name else "Custom profile",
                "runs": runs,
                "wickets": wickets,
                "player_score": float(new_player.iloc[0]["player_score"]),
            }

    if st.session_state.simulation_result:
        result = st.session_state.simulation_result
        st.markdown(
            f"""
            <div class="result-wrap">
                <div class="label">Predicted Market Value</div>
                <div class="value">{format_currency(result["value"])}</div>
                <div style="color:var(--text-mid); font-size:0.95rem; font-weight:500;">
                    Auction Category <span class="cat-pill cat-{result["category"]}">{result["category"]}</span>
                    · {result["name"]}
                    · Runs {result["runs"]:.0f} · Wickets {result["wickets"]:.0f}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown('<div style="height:18px"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Feedback</div>', unsafe_allow_html=True)
    st.markdown('<p class="section-subtitle">Help improve prediction quality</p>', unsafe_allow_html=True)
    rating = st.slider("Rate this prediction", 1, 5, value=4)
    comment = st.text_area(
        "Your feedback",
        placeholder="Share your thoughts on prediction accuracy…"
    )

    if st.button("Submit Feedback", key="btn_feedback"):

        try:
            # Save to MySQL
            cursor.execute(
                """
                INSERT INTO feedback (rating, comment)
                VALUES (?, ?)
                """,
                (rating, comment)
            )
            conn.commit()

            # Save to CSV
            feedback = pd.DataFrame({
                "rating": [rating],
                "stars": ["⭐" * rating],
                "comment": [comment]
            })

            if FEEDBACK_PATH.exists():
                feedback.to_csv(
                    FEEDBACK_PATH,
                    mode="a",
                    header=False,
                    index=False
                )
            else:
                feedback.to_csv(FEEDBACK_PATH, index=False)

            st.success("✅ Feedback saved successfully!")

        except Exception as e:
            st.error(f"Database Error: {e}")
    st.markdown("</div>", unsafe_allow_html=True)

elif page == "Player Comparison":
    render_top_bar("Player Comparison", "Side-by-side player profile review")
    st.markdown('<div class="main-panel">', unsafe_allow_html=True)
    render_page_header("Player Comparison", "Compare two profiles side by side to spot valuation gaps and strengths.")

    st.markdown(
        """
        <div class="section-head">
            <div>
                <div class="section-title"><span class="star">★</span> Compare Two Players</div>
                <p class="section-subtitle">Side-by-side auction profile breakdown</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    left, right = st.columns(2)
    with left:
        player_one = st.selectbox("Player 1", sorted(player_df["player"].unique()), key="player_one")
    with right:
        player_two = st.selectbox("Player 2", sorted(player_df["player"].unique()), key="player_two")

    if player_one and player_two and player_one != player_two:
        p1 = player_df[player_df["player"] == player_one].iloc[0]
        p2 = player_df[player_df["player"] == player_two].iloc[0]

        c1, c2 = st.columns(2)
        with c1:
            render_player_card(
                player_one,
                score_to_rating(float(p1["player_score"]), max_player_score),
                "Profile",
                "role-bat",
                "Runs",
                f"{int(p1['runs'])}",
                "Wkts",
                f"{int(p1['wickets'])}",
            )
        with c2:
            render_player_card(
                player_two,
                score_to_rating(float(p2["player_score"]), max_player_score),
                "Profile",
                "role-bowl",
                "Runs",
                f"{int(p2['runs'])}",
                "Wkts",
                f"{int(p2['wickets'])}",
            )

        comparison = pd.DataFrame(
            {
                "Metric": ["Runs", "Wickets", "Batting Avg", "Economy", "Catches", "Stumpings", "Composite Score"],
                player_one: [p1["runs"], p1["wickets"], p1["batting_average"], p1["economy_rate"], p1["catches"], p1["stumpings"], p1["player_score"]],
                player_two: [p2["runs"], p2["wickets"], p2["batting_average"], p2["economy_rate"], p2["catches"], p2["stumpings"], p2["player_score"]],
            }
        )
        st.dataframe(comparison, width="stretch", hide_index=True)

        m1, m2 = st.columns(2)
        with m1:
            st.metric(player_one, format_currency(predict_value(pd.DataFrame([p1]))))
        with m2:
            st.metric(player_two, format_currency(predict_value(pd.DataFrame([p2]))))
    else:
        st.info("Choose two different players to compare their auction profile.")
    st.markdown("</div>", unsafe_allow_html=True)

else:
    render_top_bar("Market Insights", "Auction trends and recommended picks")
    st.markdown('<div class="main-panel">', unsafe_allow_html=True)
    render_page_header("Market Insights", "Review the strongest performers and the most promising auction picks.")

    category_counts = player_df["player_score"].apply(get_category).value_counts().reindex(["A", "B", "C"], fill_value=0)
    a_share = (category_counts.get("A", 0) / max(len(player_df), 1)) * 10
    st.markdown(
        f"""
        <div class="rating-banner">
            <div class="rating-banner-left">
                <div class="icon">🛡</div>
                <span>Category A Density</span>
            </div>
            <div class="rating-banner-score">{a_share:.1f}/10</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="section-head">
            <div>
                <div class="section-title"><span class="star">★</span> Leading Performers</div>
                <p class="section-subtitle">Top batting and bowling signals in the pool</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    insight_col1, insight_col2 = st.columns(2)
    with insight_col1:
        batting_top = player_df.nlargest(5, "runs")[["player", "runs", "batting_average", "strike_rate"]]
        batting_top.columns = ["Player", "Runs", "Batting Avg", "Strike Rate"]
        st.dataframe(batting_top, width="stretch", hide_index=True)
    with insight_col2:
        bowling_top = player_df.nlargest(5, "wickets")[["player", "wickets", "economy_rate", "bowling_average"]]
        bowling_top.columns = ["Player", "Wickets", "Economy", "Bowling Avg"]
        st.dataframe(bowling_top, width="stretch", hide_index=True)

    st.bar_chart(category_counts)

    st.markdown('<div class="section-title">Recommended Auction Picks</div>', unsafe_allow_html=True)
    st.markdown('<p class="section-subtitle">Highest composite valuation candidates</p>', unsafe_allow_html=True)
    picks = player_df.nlargest(6, "player_score").copy()
    pick_cols = st.columns(2)
    for i, (_, row) in enumerate(picks.iterrows()):
        with pick_cols[i % 2]:
            rating = score_to_rating(float(row["player_score"]), max_player_score)
            role = "Batter" if row["runs"] >= row["wickets"] * 20 else "Bowler"
            role_class = "role-bat" if role == "Batter" else "role-bowl"
            if role == "Batter":
                render_player_card(
                    row["player"], rating, role, role_class,
                    "Runs", f"{int(row['runs'])}", "Avg", f"{row['batting_average']:.1f}",
                )
            else:
                render_player_card(
                    row["player"], rating, role, role_class,
                    "Wickets", f"{int(row['wickets'])}", "Econ", f"{row['economy_rate']:.2f}",
                )
    st.markdown("</div>", unsafe_allow_html=True)
