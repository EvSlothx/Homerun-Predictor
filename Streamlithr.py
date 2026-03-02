import streamlit as st
import math

st.set_page_config(page_title="2026 HR Predictor", page_icon="⚾", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Barlow+Condensed:wght@400;700;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Share Tech Mono', monospace;
    background-color: #0a0e17;
    color: #c9d1d9;
}
.stApp { background: radial-gradient(ellipse at 20% 0%, #0d1f3c 0%, #0a0e17 60%); }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem; max-width: 680px; }

.hero-title {
    font-family: 'Barlow Condensed', sans-serif;
    font-weight: 900;
    font-size: clamp(2rem, 8vw, 3.2rem);
    color: #58a6ff;
    letter-spacing: 0.04em;
    line-height: 1;
    margin-bottom: 0.2rem;
}
.hero-sub {
    font-size: 0.78rem;
    color: #484f58;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 1.2rem;
}
.section-label {
    font-size: 0.65rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #484f58;
    margin-bottom: 0.4rem;
}
.stNumberInput input {
    background: #161b22 !important;
    border: 1px solid #30363d !important;
    border-radius: 6px !important;
    color: #f0f6fc !important;
    font-family: 'Share Tech Mono', monospace !important;
}
label[data-testid="stWidgetLabel"] {
    font-size: 0.8rem !important;
    color: #8b949e !important;
    font-family: 'Share Tech Mono', monospace !important;
}
.stButton button {
    width: 100%;
    background: linear-gradient(135deg, #1f6feb, #388bfd);
    color: white;
    font-family: 'Barlow Condensed', sans-serif;
    font-weight: 700;
    font-size: 1.1rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    border: none;
    border-radius: 8px;
    padding: 0.7rem 2rem;
    box-shadow: 0 4px 20px rgba(31,111,235,0.3);
}
.stButton button:hover {
    background: linear-gradient(135deg, #388bfd, #58a6ff);
    transform: translateY(-1px);
}
.hr-display {
    font-family: 'Barlow Condensed', sans-serif;
    font-weight: 900;
    font-size: 4rem;
    color: #f0f6fc;
    line-height: 1;
    text-align: center;
}
.hr-sublabel {
    font-size: 0.65rem;
    color: #484f58;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    text-align: center;
    margin-bottom: 0.5rem;
}
.metric-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.5rem 0.8rem;
    border-radius: 6px;
    margin-bottom: 0.4rem;
    background: #0d1117;
}
.metric-label { font-size: 0.85rem; color: #8b949e; }
.metric-vals { display: flex; gap: 1.2rem; align-items: center; }
.val-logit { font-size: 1rem; font-weight: bold; }
.val-ols { font-size: 0.85rem; color: #6e7681; }
.conf-badge {
    font-size: 0.72rem;
    font-weight: bold;
    padding: 2px 7px;
    border-radius: 4px;
}
.col-headers {
    display: flex;
    justify-content: flex-end;
    gap: 1rem;
    padding: 0 0.8rem 0.3rem;
    font-size: 0.62rem;
    color: #484f58;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}
.result-card {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 10px;
    padding: 1.2rem;
    margin-top: 1rem;
}
.warn {
    background: rgba(248,81,73,0.08);
    border: 1px solid rgba(248,81,73,0.3);
    border-radius: 6px;
    padding: 0.7rem 1rem;
    color: #f85149;
    font-size: 0.82rem;
    margin-top: 0.8rem;
}
</style>
""", unsafe_allow_html=True)

# ── Model Coefficients ────────────────────────────────────────────────────────
OLS = {"barrel_lag":1.214902,"la_lag":0.396909,"parkfactor":0.0802275,"exitvelo_lag":0.8137156,"ab":0.0564566,"pullpct_lag":0.2238586,"whiff_lag":-0.1904445,"_cons":-110.3828}
LOGIT_25 = {"barrel_lag":0.394023,"la_lag":0.164662,"ab":0.0163556,"whiff_lag":-0.0760035,"_cons":-13.72815}
LOGIT_30 = {"barrel_lag":0.2106175,"la_lag":0.1454653,"exitvelo_lag":0.2452231,"ab":0.0114286,"pullpct_lag":0.0618841,"_cons":-36.43202}
LOGIT_35 = {"barrel_lag":0.2148692,"la_lag":0.1638978,"parkfactor":0.0367873,"exitvelo_lag":0.3238177,"ab":0.0096571,"_cons":-45.51782}
LOGIT_40 = {"barrel_lag":0.4922924,"parkfactor":0.0349446,"ab":0.0099082,"whiff_lag":-0.0947542,"_cons":-15.80834}

CORRECTION_25, CORRECTION_30, CORRECTION_35, CORRECTION_40 = 0.854, 0.833, 0.733, 0.625
RMSE, OLS_BIAS = 7.0507, 2.0

def logistic(x): return 1 / (1 + math.exp(-x))
def norm_cdf(z): return 0.5 * (1 + math.erf(z / math.sqrt(2)))

def predict(barrel, la, pf, exitvelo, ab, pull, whiff):
    inputs = {"barrel_lag":barrel,"la_lag":la,"parkfactor":pf,"exitvelo_lag":exitvelo,"ab":ab,"pullpct_lag":pull,"whiff_lag":whiff}
    def score(c): return c["_cons"] + sum(c[k]*v for k,v in inputs.items() if k in c)
    hr  = score(OLS) - OLS_BIAS
    p25 = logistic(score(LOGIT_25))*100*CORRECTION_25
    p30 = logistic(score(LOGIT_30))*100*CORRECTION_30
    p35 = logistic(score(LOGIT_35))*100*CORRECTION_35
    p40 = logistic(score(LOGIT_40))*100*CORRECTION_40
    o25 = (1-norm_cdf((25-hr)/RMSE))*100
    o30 = (1-norm_cdf((30-hr)/RMSE))*100
    o35 = (1-norm_cdf((35-hr)/RMSE))*100
    o40 = (1-norm_cdf((40-hr)/RMSE))*100
    return hr, p25, p30, p35, p40, o25, o30, o35, o40

def fmt(p): return f"{p:.2f}%" if p < 0.1 else f"{p:.1f}%"

def conf(lp, op):
    gap = abs(lp - op)
    if gap <= 5:    return "● HIGH", "#3fb950"
    elif gap <= 10: return "● MOD",  "#d29922"
    else:           return "● LOW",  "#f85149"

# ── UI ────────────────────────────────────────────────────────────────────────
st.markdown('<div class="hero-title">⚾ 2026 HR PREDICTOR</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Statcast-powered home run projections</div>', unsafe_allow_html=True)
st.divider()

st.markdown('<div class="section-label">2025 Statcast Metrics</div>', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    barrel   = st.number_input("Barrel Rate %", min_value=0.0, max_value=30.0, value=None, placeholder="e.g. 12.5", format="%.1f")
    la       = st.number_input("Launch Angle Avg", min_value=-20.0, max_value=40.0, value=None, placeholder="e.g. 14.0", format="%.1f")
    exitvelo = st.number_input("Exit Velo Avg (mph)", min_value=70.0, max_value=120.0, value=None, placeholder="e.g. 91.2", format="%.1f")
with col2:
    pull  = st.number_input("Pull Rate %", min_value=0.0, max_value=80.0, value=None, placeholder="e.g. 42.0", format="%.1f")
    whiff = st.number_input("Whiff Rate %", min_value=0.0, max_value=60.0, value=None, placeholder="e.g. 28.0", format="%.1f")

st.markdown('<div class="section-label" style="margin-top:0.8rem">2026 Projections</div>', unsafe_allow_html=True)
col3, col4 = st.columns(2)
with col3:
    pf = st.number_input("Park Factor", min_value=70, max_value=130, value=None, placeholder="e.g. 105", format="%d")
with col4:
    ab = st.number_input("Projected At Bats", min_value=50, max_value=700, value=None, placeholder="e.g. 550", format="%d")

st.divider()
go = st.button("⚾  PREDICT 2026 HOME RUNS")

if go:
    if any(v is None for v in [barrel, la, exitvelo, pull, whiff, pf, ab]):
        st.markdown('<div class="warn">⚠ Please fill in all fields before predicting.</div>', unsafe_allow_html=True)
    elif barrel < 7 or exitvelo < 87:
        st.markdown('<div class="warn">⚠ Model requires Barrel Rate ≥ 7% and Exit Velo ≥ 87 mph.</div>', unsafe_allow_html=True)
    else:
        hr, p25, p30, p35, p40, o25, o30, o35, o40 = predict(barrel, la, pf, exitvelo, ab, pull, whiff)

        st.markdown(f"""
        <div class="result-card">
            <div class="hr-sublabel">Projected HRs (2026)</div>
            <div class="hr-display">{hr:.1f}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        rows = [
            ("P(25+ HRs)", "#3fb950", p25, o25),
            ("P(30+ HRs)", "#58a6ff", p30, o30),
            ("P(35+ HRs)", "#d2a8ff", p35, o35),
            ("P(40+ HRs)", "#ffa657", p40, o40),
        ]

        # Column headers
        c0, c1, c2, c3 = st.columns([3, 1.5, 1.5, 1.5])
        c0.markdown("<span style='font-size:0.65rem;color:#484f58;text-transform:uppercase;letter-spacing:0.08em'></span>", unsafe_allow_html=True)
        c1.markdown("<span style='font-size:0.65rem;color:#58a6ff;text-transform:uppercase;letter-spacing:0.08em'>LOGIT</span>", unsafe_allow_html=True)
        c2.markdown("<span style='font-size:0.65rem;color:#484f58;text-transform:uppercase;letter-spacing:0.08em'>OLS</span>", unsafe_allow_html=True)
        c3.markdown("<span style='font-size:0.65rem;color:#484f58;text-transform:uppercase;letter-spacing:0.08em'>CONF</span>", unsafe_allow_html=True)

        for label, color, lp, op in rows:
            symbol, conf_color = conf(lp, op)
            c0, c1, c2, c3 = st.columns([3, 1.5, 1.5, 1.5])
            c0.markdown(f"<span style='font-size:0.85rem;color:#8b949e'>{label}</span>", unsafe_allow_html=True)
            c1.markdown(f"<span style='font-size:1rem;font-weight:bold;color:{color}'>{fmt(lp)}</span>", unsafe_allow_html=True)
            c2.markdown(f"<span style='font-size:0.9rem;color:#6e7681'>{fmt(op)}</span>", unsafe_allow_html=True)
            c3.markdown(f"<span style='font-size:0.78rem;font-weight:bold;color:{conf_color}'>{symbol}</span>", unsafe_allow_html=True)

        st.markdown("<br><span style='font-size:0.65rem;color:#484f58'>● HIGH &lt;5pt gap &nbsp;|&nbsp; ● MOD &lt;10pt gap &nbsp;|&nbsp; ● LOW &gt;10pt gap</span>", unsafe_allow_html=True)
