import streamlit as st
import random

# ===== CẤU HÌNH =====
st.set_page_config(
    page_title="Soi kèo bóng đá",
    layout="centered"
)

# ===== CSS =====
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
.box-green {
    background:#1e7f3f;
    padding:12px;
    border-radius:10px;
    text-align:center;
    color:white;
}
.box-red {
    background:#7f1e1e;
    padding:12px;
    border-radius:10px;
    text-align:center;
    color:white;
}
.box-blue {
    background:#1e3f7f;
    padding:12px;
    border-radius:10px;
    text-align:center;
    color:white;
}
.ketluan {
    background:#1b1b1b;
    padding:15px;
    border-radius:10px;
    margin-top:15px;
}
</style>
""", unsafe_allow_html=True)

# ===== TIÊU ĐỀ =====
st.markdown("## ⚽ Soi kèo bóng đá PRO")
st.caption("Kèo Tài Xỉu – Châu Á – Gợi ý vào tiền 🚀")

# ===== NHẬP THÔNG TIN =====
doi_nha = st.text_input("🏠 Đội nhà", "Man City")
doi_khach = st.text_input("✈️ Đội khách", "Arsenal")

# ===== KÈO TÀI XỈU =====
st.subheader("📊 Kèo Tài / Xỉu")
keo_tx = st.selectbox("Mốc Tài Xỉu", ["2.0","2.25","2.5","2.75","3.0"])
col1, col2 = st.columns(2)
with col1:
    odd_tai = st.number_input("Odds TÀI", value=1.95)
with col2:
    odd_xiu = st.number_input("Odds XỈU", value=1.85)

# ===== KÈO CHÂU Á =====
st.subheader("📉 Kèo Châu Á")
keo_ca = st.selectbox(
    "Mốc chấp",
    ["0", "-0.25", "-0.5", "-0.75", "+0.25", "+0.5"]
)

col3, col4 = st.columns(2)
with col3:
    odd_nha = st.number_input("Odds đội nhà", value=1.90)
with col4:
    odd_khach = st.number_input("Odds đội khách", value=1.95)

# ===== VÀO TIỀN =====
st.subheader("💰 Quản lý vốn")
von = st.number_input("Vốn (VNĐ)", value=1000000, step=100000)
phan_tram = st.slider("Phần trăm vào kèo (%)", 1, 20, 5)

# ===== PHÂN TÍCH =====
if st.button("📈 Phân tích & gợi ý"):
    tx_rate = random.randint(45, 65)
    ca_rate = random.randint(45, 65)

    # Gợi ý Tài Xỉu
    if tx_rate >= 55:
        tx_goi_y = "TÀI"
        tx_mau = "#1e7f3f"
    else:
        tx_goi_y = "XỈU"
        tx_mau = "#7f1e1e"

    # Gợi ý Châu Á
    if ca_rate >= 55:
        ca_goi_y = "ĐỘI NHÀ"
        ca_mau = "#1e7f3f"
    else:
        ca_goi_y = "ĐỘI KHÁCH"
        ca_mau = "#1e3f7f"

    tien_vao = int(von * phan_tram / 100)

    st.markdown(f"""
    <div class="card">
        <h3 style="text-align:center;color:white;">
            ⚽ {doi_nha} vs {doi_khach}
        </h3>

        <hr style="border:1px solid #333">

        <h4 style="color:#aaa;">📊 Kèo Tài Xỉu {keo_tx}</h4>
        <div style="display:flex;gap:10px;">
            <div class="box-green">TÀI<br>{odd_tai}</div>
            <div class="box-red">XỈU<br>{odd_xiu}</div>
        </div>

        <p style="color:{tx_mau};margin-top:10px;">
            👉 Gợi ý: <b>{tx_goi_y}</b> ({tx_rate}%)
        </p>

        <hr style="border:1px solid #333">

        <h4 style="color:#aaa;">📉 Kèo Châu Á {keo_ca}</h4>
        <div style="display:flex;gap:10px;">
            <div class="box-green">{doi_nha}<br>{odd_nha}</div>
            <div class="box-blue">{doi_khach}<br>{odd_khach}</div>
        </div>

        <p style="color:{ca_mau};margin-top:10px;">
            👉 Gợi ý: <b>{ca_goi_y}</b> ({ca_rate}%)
        </p>

        <hr style="border:1px solid #333">

        <div class="ketluan">
            <h4 style="color:#ffd700;">💰 GỢI Ý VÀO TIỀN</h4>
            <p style="color:#ccc;">
                • Vốn: {von:,} VNĐ<br>
                • Đánh: {phan_tram}% vốn<br>
                • Tiền vào kèo: <b>{tien_vao:,} VNĐ</b>
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.warning("⚠️ Tool mô phỏng – chỉ tham khảo, không all-in")

# ===== FOOTER =====
st.markdown("---")
st.caption("© Soi kèo bóng đá PRO | Streamlit Cloud")
