import streamlit as st
import pandas as pd
import math

st.set_page_config(page_title="2027 HR Predictor", page_icon="⚾", layout="centered")

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
.stNumberInput input, .stTextInput input {
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
.lock-box {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 12px;
    padding: 2.5rem 2rem;
    text-align: center;
    margin-top: 2rem;
}
.lock-title {
    font-family: 'Barlow Condensed', sans-serif;
    font-weight: 900;
    font-size: 1.6rem;
    color: #58a6ff;
    letter-spacing: 0.06em;
    margin-bottom: 0.4rem;
}
.lock-sub {
    font-size: 0.75rem;
    color: #484f58;
    letter-spacing: 0.08em;
    margin-bottom: 1.5rem;
}
</style>
""", unsafe_allow_html=True)

# ── Customer Passwords ────────────────────────────────────────────────────────
# Add a new unique password for each customer who buys.
# To revoke access, just delete their password from this list.
# Format: "name-code" makes it easy to track who is who.

VALID_PASSWORDS = {
    "devan-owner",       # your own access
    "homer-3847",        # Customer 1
    "homer-9261",        # Customer 2
    "homer-5734",        # Customer 3
    "homer-1829",        # Customer 4
    "homer-6453",        # Customer 5
    "homer-2917",        # Customer 6
    "homer-8365",        # Customer 7
    "homer-4782",        # Customer 8
    "homer-5193",        # Customer 9
    "homer-7624",        # Customer 10
    "homer-3158",        # Customer 11
    "homer-9047",        # Customer 12
    "homer-6831",        # Customer 13
    "homer-2574",        # Customer 14
    "homer-8916",        # Customer 15
    "homer-4239",        # Customer 16
    "homer-7583",        # Customer 17
    "homer-1467",        # Customer 18
    "homer-9728",        # Customer 19
    "homer-3692",        # Customer 20
    "homer-5841",        # Customer 21
    "homer-2306",        # Customer 22
    "homer-7159",        # Customer 23
    "homer-4873",        # Customer 24
    "homer-8524",        # Customer 25
    "homer-1395",        # Customer 26
    "homer-6047",        # Customer 27
    "homer-9382",        # Customer 28
    "homer-3761",        # Customer 29
    "homer-5218",        # Customer 30
    "homer-8934",        # Customer 31
    "homer-2685",        # Customer 32
    "homer-7413",        # Customer 33
    "homer-4956",        # Customer 34
    "homer-1274",        # Customer 35
    "homer-6839",        # Customer 36
    "homer-3527",        # Customer 37
    "homer-9164",        # Customer 38
    "homer-8742",        # Customer 39
    "homer-2493",        # Customer 40
    "homer-5368",        # Customer 41
    "homer-7831",        # Customer 42
    "homer-4015",        # Customer 43
    "homer-9573",        # Customer 44
    "homer-1846",        # Customer 45
    "homer-6392",        # Customer 46
    "homer-3284",        # Customer 47
    "homer-8617",        # Customer 48
    "homer-5749",        # Customer 49
    "homer-2138",        # Customer 50
    
    # Add more below as you get new customers:
    # "homer-XXXX",
}

# ── Session state ─────────────────────────────────────────────────────────────
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# ── Login Screen ──────────────────────────────────────────────────────────────
if not st.session_state.authenticated:
    st.markdown('<div class="hero-title">⚾ 2027 HR PREDICTOR</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Statcast-powered home run projections</div>', unsafe_allow_html=True)
    st.divider()
    st.markdown("""
    <div class="lock-box">
        <div class="lock-title">🔒 ACCESS REQUIRED</div>
        <div class="lock-sub">Enter your access key to unlock the predictor</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    pw = st.text_input("Access Key", type="password", placeholder="Enter your access key...")
    if st.button("🔓  UNLOCK"):
        if pw in VALID_PASSWORDS:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.markdown('<div class="warn">⚠ Invalid access key. Please check your key and try again.</div>', unsafe_allow_html=True)
    st.stop()

# ── Model Coefficients ────────────────────────────────────────────────────────
OLS = {"barrel_lag": 0.7326097, "la_lag": 0.4061775, "parkfactor": 0.0917247, "exitvelo_lag": 1.242968, "ab": 0.05774608, "pullpct_lag": 0.2259274, "_cons": -151.5358}
LOGIT_25 = {"barrel_lag": 0.2331153, "la_lag": 0.103897, "ab": 0.01461827, "_cons": -12.25556}
LOGIT_30 = {"barrel_lag": 0.1222681, "la_lag": 0.1026502, "exitvelo_lag": 0.2966573, "ab": 0.01279434, "pullpct_lag": 0.06011243, "_cons": -40.40814}
LOGIT_35 = {"barrel_lag": 0.1551013, "la_lag": 0.1607183, "parkfactor": 0.03143246, "exitvelo_lag": 0.3986306, "ab": 0.0119372, "_cons": -52.38233}
LOGIT_40 = {"barrel_lag": 0.3815333, "parkfactor": 0.03494231, "ab": 0.01456047, "_cons": -19.45617}

# Refit on 2022-2026 data. Leave-one-year-out calibration ratios were ~0.96-0.98,
# so the old era corrections (0.63-0.85, -2 HR) are no longer needed.
CORRECTION_25, CORRECTION_30, CORRECTION_35, CORRECTION_40 = 0.984, 0.957, 0.981, 0.977
RMSE, OLS_BIAS = 7.37, 0.0

def logistic(x): return 1 / (1 + math.exp(-x))
def norm_cdf(z): return 0.5 * (1 + math.erf(z / math.sqrt(2)))

def predict(barrel, la, pf, exitvelo, ab, pull):
    inputs = {"barrel_lag":barrel,"la_lag":la,"parkfactor":pf,"exitvelo_lag":exitvelo,"ab":ab,"pullpct_lag":pull}
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
    # Separate models can cross at the tails; a higher threshold can never be more
    # likely than a lower one, so cap each probability at the one below it.
    p30 = min(p30, p25); p35 = min(p35, p30); p40 = min(p40, p35)
    return hr, p25, p30, p35, p40, o25, o30, o35, o40

def fmt(p): return f"{p:.2f}%" if p < 0.1 else f"{p:.1f}%"

def conf(lp, op):
    gap = abs(lp - op)
    if gap <= 5:    return "● HIGH", "#3fb950"
    elif gap <= 10: return "● MOD",  "#d29922"
    else:           return "● LOW",  "#f85149"

# ── 2026 player metrics for the Leaderboard tab ──────────────────────────────
# (name, 2026 PA, 2026 HR, barrel %, launch angle, exit velo, pull %)
# Only hitters meeting the model's requirements (barrel >= 7%, exit velo >= 87).
PLAYERS_2026 = [
    ('A.J. Ewing', 492, 11, 7.5, 10.8, 89.6, 31.0),
    ('Aaron Judge', 285, 18, 20.9, 15.0, 94.0, 43.1),
    ('Abimelec Ortiz', 136, 5, 7.5, 15.1, 89.7, 44.1),
    ('Adley Rutschman', 410, 13, 7.0, 14.7, 88.9, 37.9),
    ('Adolis García', 259, 7, 9.3, 14.6, 92.1, 36.0),
    ('Alec Burleson', 670, 26, 11.3, 13.0, 92.0, 48.6),
    ('Alek Thomas', 120, 2, 7.1, 13.0, 89.5, 28.7),
    ('Amed Rosario', 244, 10, 10.4, 11.5, 90.2, 36.4),
    ('Andrew Benintendi', 468, 15, 8.6, 17.3, 89.3, 50.6),
    ('Andrés Chaparro', 228, 13, 13.1, 16.8, 89.9, 50.3),
    ('Andy Pages', 574, 23, 7.9, 15.7, 88.9, 37.6),
    ('Angel Martínez', 416, 18, 7.2, 14.8, 87.5, 43.9),
    ('Austin Riley', 630, 19, 12.4, 18.5, 91.3, 39.5),
    ('Austin Wells', 388, 14, 7.7, 20.5, 89.3, 47.4),
    ('Ben Malgeri', 140, 5, 7.1, 11.4, 90.1, 35.3),
    ('Ben Rice', 667, 41, 14.3, 14.5, 91.9, 44.9),
    ('Blaze Jordan', 199, 3, 10.1, 9.1, 88.4, 38.8),
    ('Bo Naylor', 98, 3, 11.9, 19.0, 89.1, 38.8),
    ('Bobby Witt Jr.', 632, 18, 11.4, 16.4, 92.2, 31.3),
    ('Brady House', 355, 10, 9.5, 10.2, 90.1, 30.6),
    ('Brandon Lowe', 655, 35, 12.4, 15.8, 91.0, 46.3),
    ('Brandon Marsh', 568, 18, 8.0, 13.1, 89.2, 38.5),
    ('Brandon Nimmo', 655, 14, 8.9, 10.4, 92.1, 32.8),
    ('Brandon Valenzuela', 271, 9, 7.0, 14.5, 88.4, 43.0),
    ('Braxton Fulford', 85, 1, 7.1, 23.3, 87.6, 28.6),
    ('Brent Rooker', 202, 10, 15.5, 19.7, 89.9, 39.3),
    ('Brett Baty', 473, 11, 10.3, 12.9, 90.4, 35.0),
    ('Brett Callahan', 80, 1, 11.1, 18.6, 89.9, 35.6),
    ('Brian Serven', 85, 5, 8.5, 10.3, 87.5, 39.0),
    ('Brice Turang', 680, 21, 7.7, 8.8, 90.3, 29.2),
    ('Bryan Reynolds', 699, 17, 11.2, 8.3, 90.8, 38.8),
    ('Bryce Eldridge', 448, 17, 11.5, 13.7, 92.7, 37.8),
    ('Bryce Harper', 693, 29, 10.3, 12.8, 90.0, 39.4),
    ('Byron Buxton', 408, 25, 15.9, 20.3, 90.2, 48.2),
    ('CJ Abrams', 654, 33, 10.6, 18.0, 89.6, 45.0),
    ('Cal Raleigh', 530, 23, 14.1, 25.4, 90.1, 51.5),
    ('Cam Smith', 568, 21, 11.2, 12.3, 88.7, 38.9),
    ('Carlos Correa', 141, 3, 10.3, 7.2, 89.2, 40.2),
    ('Carson Benge', 654, 20, 7.3, 12.1, 88.8, 32.6),
    ('Carter Jensen', 603, 27, 12.7, 20.6, 91.5, 41.8),
    ('Casey Schmitt', 409, 21, 12.3, 21.6, 89.9, 39.0),
    ('Christian Encarnacion-Strand', 213, 11, 14.0, 19.1, 89.5, 45.5),
    ('Christian Moore', 147, 2, 9.3, 11.2, 88.4, 25.3),
    ('Christian Walker', 635, 29, 9.6, 14.6, 89.0, 41.2),
    ('Christian Yelich', 500, 12, 9.6, 4.0, 88.9, 34.6),
    ('Coby Mayo', 454, 24, 13.5, 19.0, 91.3, 50.9),
    ('Colby Thomas', 121, 4, 8.9, 20.9, 89.1, 35.4),
    ('Colson Montgomery', 638, 31, 12.0, 23.7, 88.6, 49.6),
    ('Colt Keith', 423, 10, 7.6, 13.3, 88.7, 37.4),
    ('Colton Cowser', 392, 13, 9.4, 13.0, 87.9, 38.4),
    ('Connor Norby', 383, 7, 7.6, 18.8, 87.4, 41.1),
    ('Corbin Carroll', 671, 22, 12.2, 15.6, 91.7, 42.4),
    ('Corey Seager', 436, 20, 14.8, 12.4, 91.7, 44.0),
    ('Curtis Mead', 329, 17, 10.9, 15.8, 88.0, 46.8),
    ('Dalton Rushing', 253, 12, 11.9, 18.6, 89.5, 45.7),
    ('Daniel Schneemann', 286, 7, 8.4, 12.2, 88.0, 47.2),
    ('Dansby Swanson', 486, 19, 7.3, 15.5, 89.2, 50.0),
    ('Davis Schneider', 156, 5, 10.8, 26.3, 87.5, 44.0),
    ('Daylen Lile', 655, 22, 9.6, 19.2, 88.6, 40.7),
    ('Derek Hill', 216, 11, 10.6, 14.1, 88.9, 36.8),
    ('Dillon Dingler', 607, 27, 10.1, 17.6, 88.8, 42.2),
    ('Dominic Canzone', 533, 23, 12.2, 10.6, 91.1, 38.9),
    ('Drake Baldwin', 615, 25, 12.9, 11.0, 91.5, 30.8),
    ('Dylan Beavers', 363, 9, 8.4, 19.0, 87.8, 40.1),
    ('Dylan Crews', 443, 13, 9.4, 13.7, 90.3, 33.6),
    ('Edmundo Sosa', 250, 9, 7.2, 11.1, 87.8, 41.4),
    ('Edouard Julien', 276, 3, 7.3, 7.7, 90.8, 37.0),
    ('Eduardo Valencia', 138, 8, 15.5, 14.1, 90.3, 43.3),
    ('Elias Díaz', 237, 8, 9.6, 15.9, 88.5, 38.1),
    ('Elly De La Cruz', 636, 30, 16.3, 9.9, 94.7, 34.6),
    ('Endy Rodríguez', 159, 7, 10.6, 19.1, 92.4, 45.7),
    ('Enrique Hernández', 96, 4, 8.1, 10.9, 89.0, 27.4),
    ('Esmerlyn Valdez', 287, 17, 19.9, 18.0, 91.9, 37.5),
    ('Eugenio Suárez', 498, 26, 12.5, 21.2, 88.5, 47.0),
    ('Everson Pereira', 111, 5, 12.7, 9.7, 88.5, 36.5),
    ('Ezequiel Tovar', 506, 13, 7.0, 17.8, 87.3, 36.4),
    ('Fernando Tatis Jr.', 704, 25, 12.7, 5.3, 92.9, 33.4),
    ('Francisco Alvarez', 420, 16, 15.4, 10.2, 90.8, 39.0),
    ('Francisco Lindor', 469, 21, 9.0, 18.8, 91.6, 45.5),
    ('Freddie Freeman', 657, 16, 8.1, 12.2, 89.5, 33.4),
    ('Gabriel Arias', 149, 5, 9.9, 4.4, 89.3, 33.3),
    ('Gabriel Moreno', 549, 16, 7.7, 12.9, 89.3, 35.2),
    ('Gabriel Rincones Jr.', 89, 2, 9.4, 13.3, 90.1, 28.6),
    ('Garrett Mitchell', 531, 11, 11.7, 2.2, 93.2, 32.6),
    ('Gary Sánchez', 275, 12, 8.4, 14.3, 87.9, 42.5),
    ('Gavin Sheets', 419, 17, 7.1, 13.8, 87.4, 37.9),
    ('George Lombard Jr.', 166, 7, 8.2, 8.5, 87.1, 36.9),
    ('Giancarlo Stanton', 96, 3, 18.0, 21.5, 94.1, 39.3),
    ('Grant McCray', 91, 2, 11.5, 10.6, 87.4, 34.6),
    ('Griffin Conine', 323, 19, 16.4, 12.6, 91.1, 41.8),
    ('Gunnar Henderson', 702, 24, 7.7, 12.2, 89.2, 42.6),
    ('Hao-Yu Lee', 364, 10, 8.5, 13.3, 89.5, 27.1),
    ('Harrison Bader', 111, 5, 8.2, 12.3, 89.2, 46.6),
    ('Heliot Ramos', 442, 13, 13.8, 6.8, 92.2, 34.0),
    ('Henry Bolte', 473, 11, 8.1, 1.3, 91.0, 31.9),
    ('Henry Davis', 298, 10, 8.6, 20.9, 90.3, 52.5),
    ('Heriberto Hernández', 505, 25, 12.7, 13.3, 91.5, 46.0),
    ('Hunter Feduccia', 251, 3, 7.4, 14.9, 89.4, 32.1),
    ('Hunter Goodman', 574, 41, 14.5, 18.6, 89.8, 48.0),
    ('Ian Happ', 636, 24, 11.1, 14.2, 89.3, 45.7),
    ('JJ Bleday', 545, 24, 9.5, 23.2, 88.4, 46.6),
    ('JJ Wetherholt', 619, 17, 7.4, 11.5, 89.7, 36.3),
    ('Jac Caglianone', 553, 23, 13.0, 7.7, 93.3, 46.1),
    ('Jackson Chourio', 573, 25, 12.3, 11.8, 91.6, 30.0),
    ('Jackson Merrill', 664, 26, 12.4, 14.3, 91.5, 38.0),
    ('Jahmai Jones', 181, 6, 10.8, 18.8, 90.6, 52.9),
    ('Jake Bauers', 578, 26, 14.0, 12.1, 92.1, 41.0),
    ('Jake Burger', 620, 28, 12.3, 13.9, 90.1, 44.3),
    ('Jake Rogers', 171, 4, 9.4, 21.7, 88.0, 44.8),
    ('James McCann', 166, 7, 11.1, 11.2, 89.9, 31.6),
    ('James Wood', 623, 30, 18.6, 8.5, 95.4, 34.0),
    ('Jared Young', 342, 9, 7.7, 11.7, 90.4, 42.7),
    ('Jarred Kelenic', 83, 1, 19.0, 11.6, 92.6, 26.2),
    ('Jarren Duran', 608, 20, 9.1, 12.5, 89.6, 38.9),
    ('Jase Bowen', 103, 2, 8.9, 13.2, 87.7, 45.6),
    ('Jazz Chisholm Jr.', 532, 19, 8.2, 16.3, 90.4, 50.9),
    ('Jeremiah Jackson', 293, 10, 8.0, 8.3, 89.2, 40.6),
    ('Jeremy Peña', 483, 22, 7.2, 13.0, 88.6, 48.2),
    ('Jesús Sánchez', 315, 8, 10.8, 10.9, 90.7, 31.8),
    ('Jimmy Crooks', 149, 5, 11.6, 19.4, 91.7, 36.8),
    ('Jo Adell', 660, 23, 8.9, 16.2, 90.4, 41.0),
    ('Joc Pederson', 432, 26, 11.3, 16.0, 92.1, 42.9),
    ('Joe Mack', 330, 14, 8.4, 9.9, 88.8, 47.6),
    ('Joey Wiemer', 83, 3, 10.0, 2.2, 88.8, 36.6),
    ('John Peck', 80, 0, 7.7, 10.3, 88.6, 24.5),
    ('John Rave', 161, 6, 10.5, 14.2, 87.9, 44.3),
    ('Jonathan Aranda', 668, 22, 9.9, 14.4, 91.1, 30.1),
    ('Jordan Lawlar', 136, 6, 7.0, 18.1, 88.4, 44.2),
    ('Jordan Walker', 667, 29, 13.2, 11.8, 92.6, 38.7),
    ('Jorge Mateo', 221, 5, 7.9, 14.5, 87.3, 35.7),
    ('Jorge Soler', 361, 12, 10.9, 14.5, 88.5, 52.0),
    ('Jose Siri', 251, 10, 13.2, 15.4, 89.1, 43.1),
    ('Josh Bell', 631, 21, 9.6, 13.3, 89.9, 40.7),
    ('Josh Jung', 444, 12, 7.2, 12.0, 90.7, 39.3),
    ('Josh Lowe', 343, 12, 9.0, 18.8, 88.8, 34.3),
    ('Joshua Báez', 108, 7, 11.8, 23.1, 92.1, 47.1),
    ('José Tena', 288, 7, 8.3, 8.1, 90.6, 32.1),
    ('Juan Soto', 482, 27, 14.0, 16.0, 92.6, 39.8),
    ('Julio Rodríguez', 654, 22, 8.8, 12.8, 90.1, 39.1),
    ('Junior Caminero', 702, 42, 13.1, 10.4, 92.7, 45.1),
    ('Justin Foscue', 247, 11, 10.4, 18.9, 89.3, 44.5),
    ('Kahlil Watson', 91, 1, 7.1, 10.6, 89.3, 35.7),
    ('Kazuma Okamoto', 636, 33, 13.1, 19.4, 90.6, 50.8),
    ('Kerry Carpenter', 259, 13, 9.6, 21.4, 89.8, 43.4),
    ('Ketel Marte', 624, 22, 9.4, 13.8, 90.2, 48.9),
    ('Kevin McGonigle', 707, 18, 7.3, 19.5, 87.8, 37.1),
    ('Kody Clemens', 583, 27, 11.3, 15.4, 91.9, 47.1),
    ('Konnor Griffin', 339, 6, 7.0, 7.9, 88.1, 38.8),
    ('Kyle Higashioka', 186, 7, 8.5, 17.3, 88.2, 38.1),
    ('Kyle Karros', 475, 13, 8.3, 12.6, 89.7, 40.8),
    ('Kyle Manzardo', 356, 13, 12.0, 19.3, 89.5, 43.5),
    ('Kyle Schwarber', 701, 45, 15.6, 20.1, 92.3, 54.2),
    ('Kyle Stowers', 512, 21, 12.8, 18.1, 92.5, 46.0),
    ('Lars Nootbaar', 334, 8, 10.1, 9.2, 92.0, 39.9),
    ('Lawrence Butler', 540, 17, 8.6, 7.7, 89.7, 36.7),
    ('Lazaro Montes', 59, 4, 17.9, 21.0, 90.0, 39.3),
    ('Leo Bernal', 102, 5, 10.0, 16.1, 92.6, 40.0),
    ('LuJames Groover', 54, 1, 11.1, 16.7, 90.0, 40.5),
    ('Lucas Spence', 63, 4, 12.1, 10.6, 91.9, 54.5),
    ('Luis Campusano', 248, 8, 8.1, 16.3, 87.3, 41.4),
    ('Luis García Jr.', 543, 30, 12.2, 11.5, 91.4, 41.8),
    ('Luis Robert Jr.', 230, 11, 9.9, 15.1, 89.8, 44.4),
    ('Luke Raley', 287, 15, 15.7, 15.1, 90.8, 45.9),
    ('MJ Melendez', 144, 4, 11.1, 23.6, 94.2, 50.0),
    ('Manny Machado', 677, 30, 9.7, 14.5, 90.1, 40.1),
    ('Marcell Ozuna', 280, 8, 7.7, 20.3, 89.1, 38.0),
    ('Mark Vientos', 295, 13, 9.7, 14.6, 89.8, 37.4),
    ('Matt McLain', 496, 15, 9.0, 20.7, 87.8, 38.0),
    ('Matt Olson', 698, 41, 14.2, 18.1, 92.5, 37.8),
    ('Matt Wallner', 135, 4, 10.4, 8.1, 88.4, 44.8),
    ('Max Kepler', 145, 2, 7.8, 19.2, 88.7, 43.1),
    ('Max Muncy', 561, 29, 12.9, 17.5, 89.9, 51.3),
    ('Max Muncy', 284, 9, 10.7, 15.9, 89.1, 44.0),
    ('Max Schuemann', 87, 2, 9.8, 24.6, 89.4, 39.2),
    ('Michael Busch', 710, 20, 9.1, 15.6, 88.4, 39.5),
    ('Michael Conforto', 314, 15, 11.9, 16.7, 90.0, 47.2),
    ('Michael Harris II', 621, 26, 10.3, 10.0, 90.5, 35.6),
    ('Mickey Gasper', 225, 10, 10.4, 15.9, 88.9, 44.2),
    ('Mickey Moniak', 436, 23, 9.6, 21.4, 89.7, 48.1),
    ('Miguel Amaya', 254, 6, 7.9, 22.2, 87.8, 38.2),
    ('Miguel Vargas', 704, 33, 13.0, 20.5, 90.1, 46.7),
    ('Mike Trout', 634, 22, 16.0, 17.4, 90.1, 36.0),
    ('Mitch Garver', 149, 4, 9.1, 18.3, 90.6, 53.2),
    ('Moisés Ballesteros', 352, 9, 8.4, 10.7, 90.1, 36.4),
    ('Mookie Betts', 528, 23, 7.8, 17.9, 90.2, 40.1),
    ('Munetaka Murakami', 553, 35, 20.5, 16.1, 93.9, 46.3),
    ('Nathaniel Lowe', 429, 17, 8.4, 14.6, 89.6, 36.2),
    ('Nelson Velázquez', 113, 6, 13.8, 21.5, 94.8, 43.1),
    ('Nick Castellanos', 122, 4, 8.4, 13.0, 87.7, 55.4),
    ('Nick Kurtz', 434, 21, 18.0, 11.9, 93.4, 34.6),
    ('Nolan Gorman', 302, 9, 9.9, 21.8, 89.3, 45.6),
    ('Oneil Cruz', 419, 20, 15.4, 5.4, 94.1, 40.6),
    ('Owen Caissie', 330, 14, 14.2, 16.9, 91.1, 33.5),
    ('Patrick Bailey', 345, 10, 7.7, 13.4, 90.5, 36.2),
    ('Patrick Wisdom', 50, 1, 19.2, 28.4, 92.7, 34.6),
    ('Pete Alonso', 700, 43, 15.3, 14.9, 93.9, 36.8),
    ('Pete Crow-Armstrong', 726, 45, 13.3, 22.0, 90.6, 51.1),
    ('Rafael Devers', 633, 37, 12.5, 15.0, 93.0, 34.2),
    ('Rafael Flores Jr.', 163, 11, 14.6, 12.4, 90.7, 46.6),
    ('Ramón Laureano', 206, 7, 14.3, 12.1, 88.0, 35.3),
    ('Ramón Urías', 100, 4, 10.1, 17.9, 88.5, 31.9),
    ('Randal Grichuk', 280, 15, 11.2, 17.1, 91.3, 44.4),
    ('Randy Arozarena', 670, 26, 8.1, 10.0, 90.8, 36.2),
    ('Rhys Hoskins', 317, 13, 12.6, 26.6, 89.4, 54.5),
    ('Riley Greene', 592, 21, 14.8, 17.7, 89.9, 38.7),
    ('Rodolfo Durán', 91, 3, 8.5, 15.8, 87.5, 40.7),
    ('Roman Anthony', 242, 5, 11.7, 6.1, 92.0, 41.8),
    ('Ronald Acuña Jr.', 469, 20, 13.0, 15.7, 89.6, 37.0),
    ('Ronny Mauricio', 62, 4, 15.4, 10.2, 90.4, 41.0),
    ('Royce Lewis', 509, 15, 10.7, 20.9, 89.8, 46.7),
    ('Ryan Jeffers', 369, 14, 10.2, 16.6, 88.6, 39.4),
    ('Ryan Kreidler', 267, 8, 8.2, 12.9, 88.3, 41.5),
    ('Ryan McMahon', 360, 11, 9.0, 14.3, 90.5, 41.5),
    ('Ryan Vilade', 278, 11, 7.1, 17.0, 89.2, 35.3),
    ('Ryan Ward', 60, 3, 10.8, 19.3, 88.5, 55.3),
    ('Sal Stewart', 700, 32, 12.2, 12.9, 90.5, 32.2),
    ('Salvador Perez', 627, 21, 10.7, 15.2, 89.2, 40.2),
    ('Samuel Basallo', 399, 18, 12.1, 11.4, 90.4, 43.6),
    ('Sean Keys', 67, 2, 10.0, 17.0, 88.6, 42.5),
    ('Sean Murphy', 121, 3, 8.2, 5.6, 87.8, 49.3),
    ('Seiya Suzuki', 634, 26, 10.7, 17.5, 88.6, 41.0),
    ('Shea Langeliers', 467, 23, 13.3, 18.4, 91.3, 40.5),
    ('Shohei Ohtani', 618, 30, 16.4, 12.3, 93.3, 47.9),
    ('Spencer Jones', 289, 11, 15.9, 20.6, 94.1, 35.0),
    ('Spencer Steer', 384, 16, 12.4, 16.9, 89.7, 47.3),
    ('Spencer Torkelson', 612, 26, 12.2, 20.0, 89.5, 47.9),
    ('Starling Marte', 168, 2, 9.6, 6.4, 87.4, 31.6),
    ('Taylor Trammell', 289, 8, 12.3, 15.6, 88.5, 49.7),
    ('Teoscar Hernández', 491, 16, 10.7, 13.9, 90.3, 34.5),
    ('Thomas Saggese', 180, 4, 9.6, 12.6, 90.7, 29.3),
    ('Tim Tawa', 351, 11, 10.5, 12.8, 90.5, 36.7),
    ('Trent Grisham', 484, 18, 9.6, 17.5, 90.6, 44.4),
    ('Trevor Larnach', 433, 13, 7.5, 13.8, 87.7, 44.6),
    ('Ty France', 500, 21, 9.1, 14.6, 91.5, 38.8),
    ("Tyler O'Neill", 260, 10, 8.8, 22.5, 89.4, 44.0),
    ('Tyler Soderstrom', 453, 19, 9.5, 11.1, 90.7, 38.9),
    ('Tyler Stephenson', 468, 15, 12.4, 18.0, 90.8, 36.1),
    ('Victor Bericoto', 116, 5, 13.8, 10.0, 91.1, 32.5),
    ('Victor Mesa Jr.', 262, 14, 10.8, 21.0, 89.4, 37.8),
    ('Vinnie Pasquantino', 481, 17, 9.5, 20.6, 90.0, 43.7),
    ('Wenceel Pérez', 175, 7, 7.6, 17.0, 87.2, 44.7),
    ('Will Benson', 114, 3, 12.7, 24.9, 91.1, 41.4),
    ('Will Smith', 276, 10, 12.4, 20.1, 89.1, 29.9),
    ('Willi Castro', 477, 15, 8.0, 17.7, 87.6, 44.5),
    ('William Contreras', 640, 18, 8.5, 13.2, 90.3, 36.4),
    ('Willson Contreras', 535, 27, 13.3, 17.9, 89.8, 49.8),
    ('Willy Adames', 505, 21, 8.9, 22.8, 87.4, 49.5),
    ('Wilyer Abreu', 681, 24, 12.5, 18.9, 89.8, 35.8),
    ('Wyatt Langford', 471, 17, 7.9, 20.3, 88.6, 43.0),
    ('Yandy Díaz', 686, 22, 7.1, 6.0, 90.9, 22.8),
    ('Yohendrick Piñango', 180, 5, 8.0, 9.6, 90.9, 28.8),
    ('Yordan Alvarez', 691, 42, 16.0, 19.1, 94.4, 41.4),
    ('Yoán Moncada', 130, 3, 7.7, 15.8, 90.3, 39.4),
    ('Zac Veen', 79, 3, 7.5, 18.6, 87.4, 40.0),
    ('Zach Cole', 53, 3, 16.7, 15.3, 92.5, 50.0),
    ('Zach Neto', 704, 27, 11.9, 22.8, 89.9, 48.9),
    ('Zack Gelof', 435, 22, 10.8, 16.2, 89.7, 39.3),
]

LB_PARK_FACTOR = 100   # neutral park for every player
LB_AT_BATS     = 500   # same playing time for every player

# ── Main App ──────────────────────────────────────────────────────────────────
st.markdown('<div class="hero-title">⚾ 2027 HR PREDICTOR</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Statcast-powered home run projections</div>', unsafe_allow_html=True)
st.divider()

tab1, tab2 = st.tabs(["⚾ Player Projector", "📊 Leaderboard"])

with tab1:
    st.markdown('<div class="section-label">2026 Statcast Metrics</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        barrel   = st.number_input("Barrel Rate %", min_value=0.0, max_value=30.0, value=None, placeholder="e.g. 12.5", format="%.1f")
        la       = st.number_input("Launch Angle Avg", min_value=-20.0, max_value=40.0, value=None, placeholder="e.g. 14.0", format="%.1f")
        exitvelo = st.number_input("Exit Velo Avg (mph)", min_value=70.0, max_value=120.0, value=None, placeholder="e.g. 91.2", format="%.1f")
    with col2:
        pull  = st.number_input("Pull Rate %", min_value=0.0, max_value=80.0, value=None, placeholder="e.g. 42.0", format="%.1f")

    st.markdown('<div class="section-label" style="margin-top:0.8rem">2027 Projections</div>', unsafe_allow_html=True)
    col3, col4 = st.columns(2)
    with col3:
        pf = st.number_input("Park Factor", min_value=70, max_value=130, value=None, placeholder="e.g. 105", format="%d")
    with col4:
        ab = st.number_input("Projected At Bats", min_value=50, max_value=700, value=None, placeholder="e.g. 550", format="%d")

    st.divider()
    go = st.button("⚾  PREDICT 2027 HOME RUNS")

    if go:
        if any(v is None for v in [barrel, la, exitvelo, pull, pf, ab]):
            st.markdown('<div class="warn">⚠ Please fill in all fields before predicting.</div>', unsafe_allow_html=True)
        elif barrel < 7 or exitvelo < 87:
            st.markdown('<div class="warn">⚠ Model requires Barrel Rate ≥ 7% and Exit Velo ≥ 87 mph.</div>', unsafe_allow_html=True)
        else:
            hr, p25, p30, p35, p40, o25, o30, o35, o40 = predict(barrel, la, pf, exitvelo, ab, pull)

            st.markdown(f"""
            <div class="result-card">
                <div class="hr-sublabel">Projected HRs (2027)</div>
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

            c0, c1, c2, c3 = st.columns([3, 1.5, 1.5, 1.5])
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


with tab2:
    st.markdown('<div class="section-label">All hitters ranked by projected 2027 home runs</div>', unsafe_allow_html=True)
    st.markdown(
        f"<span style='font-size:0.72rem;color:#8b949e'>Built from 2026 Statcast metrics with a neutral park factor "
        f"({LB_PARK_FACTOR}) and {LB_AT_BATS} at bats for everyone, so this ranks underlying power only. "
        f"Use the Player Projector tab to enter a real park and playing time. "
        f"Only hitters with barrel rate &ge; 7% and exit velo &ge; 87 mph are shown.</span>",
        unsafe_allow_html=True)
    f1, f2 = st.columns([2, 1])
    with f1:
        search = st.text_input("Search player", placeholder="e.g. Judge")
    with f2:
        min_pa = st.number_input("Min 2026 PA", min_value=0, max_value=700, value=200, step=25)

    pop = []
    for name, pa_, hr26, brl, la_, ev_, pl in PLAYERS_2026:
        if pa_ < min_pa:
            continue
        hr_, p25_, p30_, p35_, p40_, *_ = predict(brl, la_, LB_PARK_FACTOR, ev_, LB_AT_BATS, pl)
        pop.append({"Player": name, "Proj HR": round(hr_, 1), "P(25+)": p25_, "P(30+)": p30_,
                    "P(35+)": p35_, "P(40+)": p40_, "2026 HR": hr26, "2026 PA": pa_,
                    "Barrel %": brl, "LA": la_, "Exit Velo": ev_, "Pull %": pl})
    pop.sort(key=lambda r: r["Proj HR"], reverse=True)
    for i, r in enumerate(pop, 1):
        r["Rank"] = i

    if not pop:
        st.markdown('<div class="warn">No players match those filters.</div>', unsafe_allow_html=True)
    else:
        cols = ["Rank", "Player", "Proj HR", "P(25+)", "P(30+)", "P(35+)", "P(40+)",
                "2026 HR", "2026 PA", "Barrel %", "LA", "Exit Velo", "Pull %"]
        heat_cols = cols[2:]
        lb_all = pd.DataFrame(pop)[cols]
        # Heat map cutoffs come from the full list (at the min-PA setting), not the search result
        hi = lb_all[heat_cols].quantile(0.90)
        lo = lb_all[heat_cols].quantile(0.10)
        lb = lb_all
        if search:
            lb = lb_all[lb_all["Player"].str.lower().str.contains(search.lower(), regex=False)]

        if len(lb) == 0:
            st.markdown('<div class="warn">No players match those filters.</div>', unsafe_allow_html=True)
        else:
            GREEN = "background-color: rgba(63,185,80,0.45)"
            RED   = "background-color: rgba(248,81,73,0.45)"

            def heat(col):
                return [GREEN if v >= hi[col.name] else (RED if v <= lo[col.name] else "") for v in col]

            styled = lb.style.apply(heat, subset=heat_cols).format({
                "Proj HR": "{:.1f}",
                "P(25+)": "{:.1f}%", "P(30+)": "{:.1f}%", "P(35+)": "{:.1f}%", "P(40+)": "{:.1f}%",
                "2026 HR": "{:d}", "2026 PA": "{:d}",
                "Barrel %": "{:.1f}", "LA": "{:.1f}", "Exit Velo": "{:.1f}", "Pull %": "{:.1f}",
            })
            st.dataframe(styled, hide_index=True, height=620)
            st.markdown(
                f"<span style='font-size:0.65rem;color:#484f58'>{len(lb)} of {len(lb_all)} players &nbsp;|&nbsp; "
                f"<span style='color:#3fb950'>&#9632;</span> top 10% of each column &nbsp;"
                f"<span style='color:#f85149'>&#9632;</span> bottom 10% &nbsp;|&nbsp; "
                f"probabilities are the logit models &nbsp;|&nbsp; click a column header to sort</span>",
                unsafe_allow_html=True)
