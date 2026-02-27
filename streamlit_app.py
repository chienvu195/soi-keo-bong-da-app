import streamlit as st
import requests
from datetime import date

# ============ CONFIG ============
API_KEY = st.secrets["API_KEY"]
HEADERS = {"x-apisports-key": API_KEY}
BASE_URL = "https://v3.football.api-sports.io"

st.set_page_config(page_title="Soi kèo bóng đá PRO", layout="centered")

# ============ STYLE (GIỮ NGUYÊN) ============
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
.wait { color:#999; font-weight:bold; }
.star { color:#ffd700; }
</style>
""", unsafe_allow_html=True)

st.title("⚽ Soi kèo bóng đá PRO")
st.caption("Live + Trận hôm nay + Gợi ý vào tiền 🚀")

tab1, tab2 = st.tabs(["📡 LIVE", "📅 TRẬN HÔM NAY"])

# ================= LIVE AUTO FALLBACK =================
@st.cache_data(ttl=60)
def live_matches():
    # 1️⃣ live=all
    try:
        r = requests.get(
            f"{BASE_URL}/fixtures?live=all",
            headers=HEADERS, timeout=8
        )
        data = r.json().get("response", [])
        if data:
            return data, "LIVE=ALL"
    except:
        pass

    # 2️⃣ status=1H-2H (FREE KEY hay chạy)
    try:
        r = requests.get(
            f"{BASE_URL}/fixtures?status=1H-2H",
            headers=HEADERS, timeout=8
        )
        data = r.json().get("response", [])
        if data:
            return data, "STATUS 1H-2H"
    except:
        pass

    # 3️⃣ FAKE LIVE từ trận hôm nay
    try:
        today = date.today().isoformat()
        r = requests.get(
            f"{BASE_URL}/fixtures?date={today}",
            headers=HEADERS, timeout=8
        )
        data = r.json().get("response", [])
        live_like = []
        for m in data:
            minute = m["fixture"]["status"]["elapsed"]
            if minute and minute >= 1:
                live_like.append(m)
        if live_like:
            return live_like, "FAKE LIVE"
    except:
        pass

    return [], "NO DATA"

# ================= TAB LIVE =================
with tab1:
    matches, source = live_matches()

    if not matches:
        st.error("❌ Không có trận live hoặc API bị giới hạn (FREE key)")
    else:
        st.caption(f"📡 Nguồn dữ liệu: {source}")

        for m in matches:
            minute = m["fixture"]["status"]["elapsed"]
            if not minute or minute < 55:
                continue

            home = m["teams"]["home"]["name"]
            away = m["teams"]["away"]["name"]
            sh = m["goals"]["home"]
            sa = m["goals"]["away"]
            total = sh + sa

            # ===== TÍNH SHOTS (SAFE) =====
            shots = 0
            for team in m.get("statistics", []):
                for s in team.get("statistics", []):
                    if s["type"] == "Shots on Goal" and s["value"]:
                        shots += s["value"]

            # ===== CHẤM SAO ÉP SÂN =====
            stars = 1
            if shots >= 10: stars = 2
            if shots >= 15: stars = 3
            if shots >= 20: stars = 4
            if shots >= 25: stars = 5

            star_view = "⭐" * stars

            # ===== LOGIC KÈO (GIỮ NGUYÊN + NÂNG) =====
            if minute >= 70 and total <= 1 and shots < 15:
                tip = "XỈU LIVE CUỐI"
                money = "Vào 10–15% vốn"
                cls = "good"
            elif minute >= 60 and total >= 2 and shots >= 15:
                tip = "TÀI LIVE"
                money = "Vào 15–25% vốn"
                cls = "good"
            else:
                tip = "CHỜ KÈO"
                money = "Không vào"
                cls = "wait"

            st.markdown(f"""
            <div class="card">
            <b>{home}</b> {sh}-{sa} <b>{away}</b><br>
            ⏱️ {minute}' | 🎯 Shots: {shots}<br>
            🔥 Độ ép sân: <span class="star">{star_view}</span><br>
            👉 <span class="{cls}">{tip}</span><br>
            💰 {money}
            </div>
            """, unsafe_allow_html=True)

# ================= PREMATCH (GIỮ NGUYÊN) =================
@st.cache_data(ttl=3600)
def today_matches():
    try:
        today = date.today().isoformat()
        r = requests.get(
            f"{BASE_URL}/fixtures?date={today}",
            headers=HEADERS, timeout=10
        )
        return r.json().get("response", [])
    except:
        return []

with tab2:
    games = today_matches()
    if not games:
        st.warning("❌ Hôm nay không có trận")
    else:
        for g in games:
            home = g["teams"]["home"]["name"]
            away = g["teams"]["away"]["name"]
            league = g["league"]["name"]

            # GIỮ LOGIC ĐƠN GIẢN
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
