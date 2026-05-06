import streamlit as st

st.set_page_config(page_title="Xác Suất Pro 2026", layout="centered")

# Định nghĩa ký hiệu
GIAO = "∩"
DOI = "̅"

st.title("🧮 Hệ Thống Giải Toán Xác Suất 2026")
st.markdown("---")

# Nhập liệu chia 2 cột
col1, col2 = st.columns(2)

with col1:
    pa = st.text_input("P(A)", placeholder="Ví dụ: 0.6")
    pb = st.text_input("P(B)", placeholder="Ví dụ: 0.4")
    pab = st.text_input("P(A|B)", placeholder="Xác suất A khi biết B")

with col2:
    pba = st.text_input("P(B|A)", placeholder="Xác suất B khi biết A")
    pagb = st.text_input(f"P(A {GIAO} B)", placeholder="Ví dụ: 0.2")
    pda = st.text_input(f"P(A{DOI})", placeholder="Biến cố đối của A")

is_ind = st.checkbox("Giả định A, B độc lập")

if st.button("TÍNH TOÁN CHI TIẾT", type="primary", use_container_width=True):
    try:
        # Chuyển đổi dữ liệu (silently filter data based on logic)
        p = {
            'A': float(pa) if pa else None,
            'B': float(pb) if pb else None,
            'A_B': float(pab) if pab else None,
            'B_A': float(pba) if pba else None,
            'AgB': float(pagb) if pagb else None,
            'dA': float(pda) if pda else None
        }
        
        process = []
        # Thực hiện vòng lặp suy luận (logic tương tự bản cũ)
        for _ in range(5):
            # Tính biến cố đối
            if p['A'] is not None and p['dA'] is None:
                p['dA'] = round(1 - p['A'], 4)
                process.append(f"P(A{DOI}) = 1 - P(A) = 1 - {p['A']} = {p['dA']}")
            elif p['dA'] is not None and p['A'] is None:
                p['A'] = round(1 - p['dA'], 4)
                process.append(f"P(A) = 1 - P(A{DOI}) = 1 - {p['dA']} = {p['A']}")

            # Tính giao dựa trên độc lập
            if is_ind and p['A'] is not None and p['B'] is not None and p['AgB'] is None:
                p['AgB'] = round(p['A'] * p['B'], 4)
                process.append(f"Do A, B độc lập: P(A{GIAO}B) = P(A).P(B) = {p['A']}.{p['B']} = {p['AgB']}")

            # Công thức xác suất có điều kiện
            if p['AgB'] is not None and p['B'] is not None and p['B'] > 0 and p['A_B'] is None:
                p['A_B'] = round(p['AgB'] / p['B'], 4)
                process.append(f"P(A|B) = P(A{GIAO}B) / P(B) = {p['AgB']} / {p['B']} = {p['A_B']}")

        st.subheader("📍 Kết quả & Quy trình")
        if process:
            for step in list(dict.fromkeys(process)):
                st.success(step)
        else:
            st.warning("Nhập thêm dữ liệu để hệ thống tính toán!")
            
    except Exception:
        st.error("Lỗi: Vui lòng chỉ nhập số thập phân (ví dụ: 0.5)")
