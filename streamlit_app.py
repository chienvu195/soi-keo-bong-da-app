import streamlit as st

st.set_page_config(page_title="Soi kèo bóng đá", layout="centered")

st.title("⚽ Soi kèo bóng đá")
st.write("App đang chạy OK 🚀")

doi_nha = st.text_input("Đội nhà")
doi_khach = st.text_input("Đội khách")

if st.button("Phân tích kèo"):
    if doi_nha and doi_khach:
        st.success(f"Kèo tham khảo: {doi_nha} chấp 0.5")
    else:
        st.warning("Nhập đủ tên 2 đội")
