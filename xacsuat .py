import streamlit as st

st.set_page_config(page_title="Hệ Thống Xác Suất Toàn Diện", layout="centered")

# Định nghĩa ký hiệu toán học
GIAO = "∩"
HOP = "∪"
DOI = "̅"

st.title("📊 Hệ Thống Xác Suất Toàn Diện")
st.markdown("---")

st.subheader("Dữ liệu đầu vào")
# Chia thành 2 cột để giống giao diện cũ nhưng gọn hơn
col1, col2 = st.columns(2)

with col1:
    pa = st.text_input("P(A)", placeholder="Ví dụ: 0.6")
    pb = st.text_input("P(B)", placeholder="Ví dụ: 0.4")
    pab = st.text_input("P(A|B)", placeholder="Xác suất A khi biết B")
    pba = st.text_input("P(B|A)", placeholder="Xác suất B khi biết A")
    padb = st.text_input(f"P(A|{B}{DOI})", placeholder="Xác suất A khi biết B đối")

with col2:
    pbda = st.text_input(f"P(B|{A}{DOI})", placeholder="Xác suất B khi biết A đối")
    pagb = st.text_input(f"P(A {GIAO} B)", placeholder="Xác suất giao")
    pahb = st.text_input(f"P(A {HOP} B)", placeholder="Xác suất hợp")
    pda = st.text_input(f"P(A{DOI})", placeholder="Biến cố đối của A")
    pdb = st.text_input(f"P(B{DOI})", placeholder="Biến cố đối của B")

is_ind = st.checkbox("Giả định A, B độc lập")

if st.button("TÍNH TOÁN", type="primary", use_container_width=True):
    try:
        # Chuyển đổi dữ liệu sang dạng số
        inputs = {
            'A': pa, 'B': pb, 'A_B': pab, 'B_A': pba, 
            'AgB': pagb, 'AhB': pahb, 'dA': pda, 'dB': pdb
        }
        p = {k: float(v) if v else None for k, v in inputs.items()}
        
        process = []
        # Chạy vòng lặp tính toán để suy luận các biến còn thiếu
        for _ in range(10):
            # 1. Tính biến cố đối
            if p['A'] is not None and p['dA'] is None:
                p['dA'] = round(1 - p['A'], 4); process.append(f"P(A{DOI}) = 1 - P(A) = {p['dA']}")
            if p['dA'] is not None and p['A'] is None:
                p['A'] = round(1 - p['dA'], 4); process.append(f"P(A) = 1 - P(A{DOI}) = {p['A']}")
            if p['B'] is not None and p['dB'] is None:
                p['dB'] = round(1 - p['B'], 4); process.append(f"P(B{DOI}) = 1 - P(B) = {p['dB']}")
            if p['dB'] is not None and p['B'] is None:
                p['B'] = round(1 - p['dB'], 4); process.append(f"P(B) = 1 - P(B{DOI}) = {p['B']}")

            # 2. Độc lập
            if is_ind and p['A'] is not None and p['B'] is not None and p['AgB'] is None:
                p['AgB'] = round(p['A'] * p['B'], 4)
                process.append(f"Vì A,B độc lập: P(A{GIAO}B) = P(A).P(B) = {p['AgB']}")

            # 3. Công thức cộng (Xác suất hợp)
            if p['A'] is not None and p['B'] is not None and p['AgB'] is not None and p['AhB'] is None:
                p['AhB'] = round(p['A'] + p['B'] - p['AgB'], 4)
                process.append(f"P(A{HOP}B) = P(A)+P(B)-P(A{GIAO}B) = {p['AhB']}")

            # 4. Xác suất có điều kiện
            if p['AgB'] is not None and p['B'] is not None and p['B']>0 and p['A_B'] is None:
                p['A_B'] = round(p['AgB'] / p['B'], 4); process.append(f"P(A|B) = P(A{GIAO}B)/P(B) = {p['A_B']}")
            if p['AgB'] is not None and p['A'] is not None and p['A']>0 and p['B_A'] is None:
                p['B_A'] = round(p['AgB'] / p['A'], 4); process.append(f"P(B|A) = P(A{GIAO}B)/P(A) = {p['B_A']}")

        st.subheader(" quy trình giải chi tiết")
        if process:
            # Loại bỏ các bước lặp lại
            for step in list(dict.fromkeys(process)):
                st.success(step)
        else:
            st.warning("Hãy nhập ít nhất 2 hoặc 3 giá trị để hệ thống có thể tính toán!")

    except Exception:
        st.error("Lỗi: Bạn chỉ được nhập số thập phân!")
