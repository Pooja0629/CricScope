import streamlit as st

import pandas as pd

# -----------------------------------
# PAGE CONFIG
# -----------------------------------
st.set_page_config(
    page_title="IPL Intelligence Engine",
    page_icon="🏏",
    layout="wide"
)

# -----------------------------------
# LOAD MODEL
# -----------------------------------
import joblib

model = joblib.load("model.pkl")
columns = joblib.load("columns.pkl")

# -----------------------------------
# PREMIUM CSS
# -----------------------------------
st.markdown("""
<style>

[data-testid="stAppViewContainer"] {
    background: linear-gradient(180deg,#020617,#020617,#0f172a);
    color: white;
}

/* Hero */
.hero {
    text-align: center;
    padding: 70px 20px;
    border-radius: 25px;
    background: linear-gradient(135deg,#020617,#0f172a,#1e293b);
    box-shadow: 0px 20px 60px rgba(0,0,0,0.8);
}

.hero h1 {
    font-size: 55px;
}

.hero p {
    font-size: 20px;
    opacity: 0.85;
}

/* Buttons */
.stButton>button {
    background: linear-gradient(135deg,#ff512f,#dd2476);
    color:white;
    border:none;
    border-radius:12px;
    height:50px;
    font-size:17px;
    font-weight:600;
    width:100%;
    transition:0.3s;
}

.stButton>button:hover {
    transform:scale(1.04);
    box-shadow:0px 6px 25px rgba(255,80,100,0.6);
}

/* Cards */
.section-card {
    padding:16px;
    border-radius:16px;
    background: rgba(15,23,42,0.6);
    backdrop-filter: blur(12px);
    border:1px solid rgba(255,255,255,0.08);
    margin-top:30px;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#020617,#0f172a);
}

/* Metrics */
[data-testid="metric-container"] {
    background: rgba(15,23,42,0.7);
    border-radius:12px;
    padding:10px;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------------
# HERO
# -----------------------------------
st.markdown("""
<div class="hero">
    <h1>🏏 IPL Match Intelligence Engine</h1>
    <p>Real-Time AI Predictions • Advanced Cricket Analytics</p>
</div>
""", unsafe_allow_html=True)

# -----------------------------------
# SIDEBAR
# -----------------------------------
st.sidebar.title("🏏 IPL AI Engine")

st.sidebar.info("""
Predict match outcomes using real-time match stats,
run rates, and ML-powered insights.
""")

st.sidebar.markdown("---")
st.sidebar.markdown("### 👤 Developer")
st.sidebar.write("**Arnav Singh**")
st.sidebar.markdown("📧 itsarnav.singh80@gmail.com")
st.sidebar.markdown("[🔗 LinkedIn](https://www.linkedin.com/in/arnav-singh-a87847351)")
st.sidebar.markdown("[💻 GitHub](https://github.com/Arnav-Singh-5080)")

# -----------------------------------
# INPUT SECTION
# -----------------------------------
st.markdown('<div class="section-card">🏏 Match Setup</div>', unsafe_allow_html=True)

teams = [
    'Chennai Super Kings','Delhi Capitals','Kings XI Punjab',
    'Kolkata Knight Riders','Mumbai Indians',
    'Rajasthan Royals','Royal Challengers Bangalore',
    'Sunrisers Hyderabad'
]

cities = ['Mumbai','Chennai','Kolkata','Delhi','Bangalore','Hyderabad','Jaipur']

col1, col2 = st.columns(2)

with col1:
    batting_team = st.selectbox("Batting Team", teams)
    bowling_team = st.selectbox("Bowling Team", teams)
    city = st.selectbox("City", cities)

with col2:
    target = st.number_input("Target", min_value=1)
    score = st.number_input("Current Score", min_value=0)
    overs = st.number_input("Overs Completed", min_value=0.1, max_value=20.0)
    wickets = st.number_input("Wickets Fallen", min_value=0, max_value=10)

# -----------------------------------
# CALCULATIONS
# -----------------------------------
runs_left = target - score
balls_left = 120 - (overs * 6)
wickets_remaining = 10 - wickets
crr = score / overs if overs > 0 else 0
rrr = (runs_left * 6) / balls_left if balls_left > 0 else 0

# -----------------------------------
# PREDICTION
# -----------------------------------
if st.button("🚀 Analyze Match"):

    input_df = pd.DataFrame({
        'batting_team':[batting_team],
        'bowling_team':[bowling_team],
        'city':[city],
        'runs_left':[runs_left],
        'balls_left':[balls_left],
        'wickets':[wickets_remaining],
        'total_runs_x':[target],
        'crr':[crr],
        'rrr':[rrr]
    })

    result = pipe.predict_proba(input_df)

    win = result[0][1]
    loss = result[0][0]

    st.markdown("---")

    # ✅ CLEAN WIN PROBABILITY (NO HTML BUG)
    st.subheader("🏏 Win Probability")

    colA, colB = st.columns(2)

    with colA:
        st.write(f"**{batting_team}**")
        st.progress(win)

    with colB:
        st.write(f"**{bowling_team}**")
        st.progress(loss)

    st.markdown(f"""
    <div style="text-align:center; font-size:18px; margin-top:10px;">
    <b>{batting_team}</b>: {round(win*100)}% &nbsp;&nbsp; | &nbsp;&nbsp;
    <b>{bowling_team}</b>: {round(loss*100)}%
    </div>
    """, unsafe_allow_html=True)

    # -----------------------------------
    # METRICS
    # -----------------------------------
    st.markdown("---")
    st.subheader("📈 Match Intelligence Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Runs Left", runs_left)
    col2.metric("Balls Left", int(balls_left))
    col3.metric("Current RR", round(crr,2))
    col4.metric("Required RR", round(rrr,2))

    # -----------------------------------
    # AI INSIGHT
    # -----------------------------------
    st.markdown("---")
    st.subheader("🧠 AI Match Insight")

    if rrr > crr + 2:
        st.error("High pressure situation — batting team struggling.")
    elif wickets_remaining <= 3:
        st.warning("Few wickets left — risk increasing.")
    elif win > 0.7:
        st.success("Batting team is in strong control.")
    else:
        st.info("Match is balanced — could go either way.")

# -----------------------------------
# FOOTER
# -----------------------------------
st.markdown("""
<div style="
margin-top:80px;
padding:30px;
border-radius:20px;
background: rgba(15, 23, 42, 0.6);
backdrop-filter: blur(12px);
border: 1px solid rgba(255,255,255,0.08);
box-shadow: 0 8px 32px rgba(0,0,0,0.6);
text-align:center;
color:#e2e8f0;
">

<h3>⚡ IPL Match Intelligence Engine</h3>

<p style="opacity:0.8;">
AI-powered predictive analytics system delivering real-time match insights
</p>

<hr style="margin:20px 0;">

<p style="opacity:0.5;">
© 2026 • AI-Powered Sports Analytics • Arnav Singh
</p>

</div>
""", unsafe_allow_html=True)
