import streamlit as st

# Cấu hình giao diện
st.set_page_config(page_title="Giải Xác Suất Pro", layout="centered")

st.title("🧮 Hệ Thống Giải Toán Xác Suất 2026")
st.markdown("---")

# Ký hiệu toán học chuẩn
GIAO = "∩"
DOI = "̅" 

# Nhập liệu chia làm 2 cột cho đẹp
col1, col2 = st.columns(2)
with col1:
    pa = st.text_input("P(A)", placeholder="Ví dụ: 0.5")
    pb = st.text_input("P(B)", placeholder="Ví dụ: 0.4")
with col2:
    pagb = st.text_input(f"P(A {GIAO} B)", placeholder="Ví dụ: 0.2")
    is_ind = st.checkbox("Giả định A, B độc lập")

if st.button("TÍNH TOÁN CHI TIẾT", type="primary", use_container_width=True):
    try:
        # Chuyển đổi dữ liệu
        p_a = float(pa) if pa else None
        p_b = float(pb) if pb else None
        p_agb = float(pagb) if pagb else None
        
        process = []
        
        # Một vài logic tính toán mẫu
        if p_a is not None:
            p_da = round(1 - p_a, 4)
            process.append(f"P(A{DOI}) = 1 - P(A) = 1 - {p_a} = {p_da}")
            
        if is_ind and p_a is not None and p_b is not None:
            p_agb = round(p_a * p_b, 4)
            process.append(f"Do A,B độc lập: P(A{GIAO}B) = P(A).P(B) = {p_a}.{p_b} = {p_agb}")

        # Hiển thị
        st.subheader("📍 Quy trình giải chi tiết")
        if process:
            for step in process:
                st.success(step)
        else:
            st.warning("Vui lòng nhập thêm dữ liệu!")
    except:
        st.error("Lỗi: Chỉ được nhập số thập phân!")
