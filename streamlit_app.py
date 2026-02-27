import streamlit as st
import requests
from datetime import date

# ============ CONFIG ============
API_KEY = st.secrets["API_KEY"]
HEADERS = {"x-apisports-key": API_KEY}

st.set_page_config(page_title="Soi kèo bóng đá PRO", layout="centered")

# ============ STYLE ============
st.markdown("""
<style>
body { background:#0e1117; }
.card {
    background:#111;
    padding:16px;
    border-radius:14px;
    border:1px solid #2a2a2a;
    margin-top:12px;
}
.good { color:#00ff9c; font-weight:bold; }
.warn { color:#ffaa00; font-weight:bold; }
</style>
""", unsafe_allow_html=True)

st.title("⚽ Soi kèo bóng đá PRO")
st.caption("Live + Trận hôm nay + Gợi ý vào tiền 🚀")

tab1, tab2 = st.tabs(["📡 LIVE", "📅 TRẬN HÔM NAY"])

# ============ LIVE ============
@st.cache_data(ttl=60)
def live_matches():
    r = requests.get(
        "https://v3.football.api-sports.io/fixtures?live=all",
        headers=HEADERS
    )
    return r.json().get("response", [])

with tab1:
    matches = live_matches()
    if not matches:
        st.warning("❌ Không có trận live")
    else:
        for m in matches:
            minute = m["fixture"]["status"]["elapsed"]
            if not minute or minute < 55:
                continue

            home = m["teams"]["home"]["name"]
            away = m["teams"]["away"]["name"]
            sh = m["goals"]["home"]
            sa = m["goals"]["away"]
            total = sh + sa

            if minute >= 70 and total <= 1:
                tip = "XỈU LIVE CUỐI TRẬN"
            elif minute >= 60 and total >= 2:
                tip = "TÀI LIVE"
            else:
                tip = "CHỜ"

            st.markdown(f"""
            <div class="card">
            <b>{home}</b> {sh}-{sa} <b>{away}</b><br>
            ⏱️ {minute}'<br>
            👉 <span class='good'>{tip}</span>
            </div>
            """, unsafe_allow_html=True)

# ============ PREMATCH ============
@st.cache_data(ttl=3600)
def today_matches():
    today = date.today().isoformat()
    url = f"https://v3.football.api-sports.io/fixtures?date={today}"
    r = requests.get(url, headers=HEADERS)
    return r.json().get("response", [])

with tab2:
    games = today_matches()
    if not games:
        st.warning("❌ Hôm nay không có trận")
    else:
        for g in games:
            home = g["teams"]["home"]["name"]
            away = g["teams"]["away"]["name"]
            league = g["league"]["name"]

            # DỰ ĐOÁN ĐƠN GIẢN
            tip_tx = "XỈU 2.5"
            tip_ah = f"{home} -0.25"

            st.markdown(f"""
            <div class="card">
            🏆 {league}<br>
            <b>{home}</b> vs <b>{away}</b><br>
            ⚽ <span class='good'>{tip_tx}</span><br>
            🟦 <span class='warn'>{tip_ah}</span>
            </div>
            """, unsafe_allow_html=True)
