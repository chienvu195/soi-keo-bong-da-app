 import streamlit as st
import requests
import datetime

# ================== CẤU HÌNH ==================
API_KEY = "b4b4c0f97e599b6531fc0683ba683638"
HEADERS = {
    "x-apisports-key": API_KEY
}

st.set_page_config(
    page_title="Soi kèo bóng đá PRO",
    layout="centered"
)

# ================== CSS ==================
st.markdown("""
<style>
body { background:#0e1117; }
.card {
    background:#111;
    padding:20px;
    border-radius:14px;
    border:1px solid #2a2a2a;
    margin-top:20px;
}
.good { color:#00ff9c; font-weight:bold; }
.bad { color:#ff4b4b; font-weight:bold; }
.neutral { color:#ffaa00; font-weight:bold; }
</style>
""", unsafe_allow_html=True)

st.title("⚽ Soi kèo bóng đá PRO")
st.caption("Kèo Tài/Xỉu – Châu Á – LIVE ⚡")

# ================== LẤY TRẬN ĐANG ĐÁ ==================
@st.cache_data(ttl=60)
def get_live_matches():
    url = "https://v3.football.api-sports.io/fixtures?live=all"
    r = requests.get(url, headers=HEADERS)
    if r.status_code != 200:
        return []
    return r.json().get("response", [])

live_matches = get_live_matches()

if not live_matches:
    st.warning("❌ Hiện không có trận LIVE")
    st.stop()

# ================== CHỌN TRẬN ==================
match_names = []
for m in live_matches:
    home = m["teams"]["home"]["name"]
    away = m["teams"]["away"]["name"]
    minute = m["fixture"]["status"]["elapsed"]
    match_names.append(f"{home} vs {away} ({minute}')")

selected = st.selectbox("📡 Chọn trận LIVE", match_names)
idx = match_names.index(selected)
match = live_matches[idx]

home = match["teams"]["home"]["name"]
away = match["teams"]["away"]["name"]
score_home = match["goals"]["home"]
score_away = match["goals"]["away"]
minute = match["fixture"]["status"]["elapsed"]

st.markdown(f"""
<div class="card">
<b>{home}</b> {score_home} - {score_away} <b>{away}</b><br>
⏱️ Phút: {minute}'
</div>
""", unsafe_allow_html=True)

# ================== KÈO TÀI / XỈU ==================
st.markdown("## 📊 Kèo Tài / Xỉu")

line = st.selectbox("Mốc Tài/Xỉu", [1.5, 2.0, 2.5, 3.0, 3.5])
odds_over = st.number_input("Odds TÀI", value=1.95, step=0.01)
odds_under = st.number_input("Odds XỈU", value=1.85, step=0.01)

total_goals = score_home + score_away

if st.button("📈 Phân tích Tài/Xỉu"):
    if minute < 30 and total_goals == 0:
        st.markdown("<span class='good'>👉 ƯU TIÊN XỈU (trận chậm)</span>", unsafe_allow_html=True)
    elif minute > 70 and total_goals < line:
        st.markdown("<span class='good'>👉 ƯU TIÊN TÀI CUỐI TRẬN</span>", unsafe_allow_html=True)
    elif total_goals >= line:
        st.markdown("<span class='neutral'>⚠️ Đã chạm mốc – CÂN NHẮC</span>", unsafe_allow_html=True)
    else:
        st.markdown("<span class='bad'>🚫 NO BET – không rõ xu hướng</span>", unsafe_allow_html=True)

# ================== KÈO CHÂU Á ==================
st.markdown("## 📉 Kèo Châu Á")

handicap = st.selectbox("Mốc chấp", [-1, -0.75, -0.5, -0.25, 0, 0.25, 0.5])
odds_home = st.number_input("Odds đội nhà", value=1.90, step=0.01)
odds_away = st.number_input("Odds đội khách", value=1.90, step=0.01)

if st.button("📉 Phân tích Châu Á"):
    diff = score_home - score_away
    if diff + handicap > 0:
        st.markdown("<span class='good'>👉 CỬA TRÊN ĐANG AN TOÀN</span>", unsafe_allow_html=True)
    elif diff + handicap < 0:
        st.markdown("<span class='good'>👉 CỬA DƯỚI CÓ LỢI</span>", unsafe_allow_html=True)
    else:
        st.markdown("<span class='neutral'>⚠️ KÈO CÂN – CÂN NHẮC</span>", unsafe_allow_html=True)
