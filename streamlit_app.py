import streamlit as st
import requests
import datetime

# ================== CẤU HÌNH ==================
API_KEY = "d6d20b7df16e6b44d434073dadf38b3e"
HEADERS = {"x-apisports-key": API_KEY}

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
st.caption("Trận hôm nay – Tài/Xỉu – Châu Á – Gợi ý vào tiền 🚀")

# ================== LẤY TRẬN HÔM NAY ==================
@st.cache_data(ttl=300)
def get_today_matches():
    today = datetime.date.today().strftime("%Y-%m-%d")
    url = f"https://v3.football.api-sports.io/fixtures?date={today}"
    r = requests.get(url, headers=HEADERS)
    if r.status_code != 200:
        return []
    return r.json().get("response", [])

matches = get_today_matches()

if not matches:
    st.warning("❌ Hôm nay không có trận đấu")
    st.stop()

# ================== CHỌN TRẬN ==================
match_names = []
for m in matches:
    home = m["teams"]["home"]["name"]
    away = m["teams"]["away"]["name"]
    time = m["fixture"]["date"][11:16]
    match_names.append(f"{home} vs {away} ({time})")

selected = st.selectbox("📅 Chọn trận hôm nay", match_names)
idx = match_names.index(selected)
match = matches[idx]

home = match["teams"]["home"]["name"]
away = match["teams"]["away"]["name"]
time = match["fixture"]["date"][11:16]

st.markdown(f"""
<div class="card">
<b>{home}</b> 🆚 <b>{away}</b><br>
🕒 Giờ đá: {time}
</div>
""", unsafe_allow_html=True)

# ================== KÈO TÀI / XỈU ==================
st.markdown("## 📊 Kèo Tài / Xỉu")

line = st.selectbox("Mốc Tài/Xỉu", [1.5, 2.0, 2.5, 3.0, 3.5])

if st.button("📈 Gợi ý Tài/Xỉu"):
    if line <= 2.0:
        st.markdown("👉 <span class='good'>GỢI Ý 1: Ưu tiên TÀI sớm</span>", unsafe_allow_html=True)
        st.markdown("👉 <span class='neutral'>GỢI Ý 2: Chờ bàn sớm rồi theo TÀI</span>", unsafe_allow_html=True)
        st.markdown("👉 <span class='bad'>GỢI Ý 3: Không vào nếu odds thấp</span>", unsafe_allow_html=True)
    else:
        st.markdown("👉 <span class='good'>GỢI Ý 1: Ưu tiên XỈU đầu trận</span>", unsafe_allow_html=True)
        st.markdown("👉 <span class='neutral'>GỢI Ý 2: Canh TÀI live nếu có bàn sớm</span>", unsafe_allow_html=True)
        st.markdown("👉 <span class='bad'>GỢI Ý 3: Tránh vào sớm mốc cao</span>", unsafe_allow_html=True)

# ================== KÈO CHÂU Á ==================
st.markdown("## 📉 Kèo Châu Á")

handicap = st.selectbox("Mốc chấp", [-1, -0.75, -0.5, -0.25, 0, 0.25, 0.5])

if st.button("📉 Gợi ý Châu Á"):
    if handicap < 0:
        st.markdown("👉 <span class='good'>GỢI Ý 1: Cửa trên mạnh – có thể theo</span>", unsafe_allow_html=True)
        st.markdown("👉 <span class='neutral'>GỢI Ý 2: Chờ odds tăng rồi vào</span>", unsafe_allow_html=True)
        st.markdown("👉 <span class='bad'>GỢI Ý 3: Tránh all-in</span>", unsafe_allow_html=True)
    else:
        st.markdown("👉 <span class='good'>GỢI Ý 1: Cửa dưới an toàn</span>", unsafe_allow_html=True)
        st.markdown("👉 <span class='neutral'>GỢI Ý 2: Theo hiệp 1</span>", unsafe_allow_html=True)
        st.markdown("👉 <span class='bad'>GỢI Ý 3: Không theo nếu odds thấp</span>", unsafe_allow_html=True)
