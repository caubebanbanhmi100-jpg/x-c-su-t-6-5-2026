import streamlit as st

# Cấu hình giao diện
st.set_page_config(page_title="Siêu Máy Tính Xác Suất 12H", layout="wide")

# Ký hiệu toán học
G, H, D, K = "∩", "∪", "̅", "|"

st.title("🚀 Siêu Máy Tính Xác Suất Toàn Diện")
st.info("Nhập các giá trị đã biết. Nút Xóa sẽ giúp ông reset nhanh để làm bài mới.")

# Danh sách các key để quản lý dữ liệu
keys = ["A", "B", "AgB", "AhB", "dA", "dB", "A_B", "B_A", "A_dB", "B_dA", "dA_B", "dB_dA", "AgdB", "dAgB", "dAgdB", "dAhB", "dBhA", "dAhdB"]

# Khởi tạo session_state nếu chưa có
for key in keys:
    if key not in st.session_state:
        st.session_state[key] = ""

# --- PHẦN 1: GIAO DIỆN NHẬP LIỆU (3 CỘT) ---
col1, col2, col3 = st.columns(3)

with col1:
    st.session_state["A"] = st.text_input("P(A)", value=st.session_state["A"])
    st.session_state["B"] = st.text_input("P(B)", value=st.session_state["B"])
    st.session_state["AgB"] = st.text_input(f"P(A {G} B)", value=st.session_state["AgB"])
    st.session_state["AhB"] = st.text_input(f"P(A {H} B)", value=st.session_state["AhB"])

with col2:
    st.session_state["A_B"] = st.text_input(f"P(A{K}B)", value=st.session_state["A_B"])
    st.session_state["B_A"] = st.text_input(f"P(B{K}A)", value=st.session_state["B_A"])
    st.session_state["A_dB"] = st.text_input(f"P(A{K}B{D})", value=st.session_state["A_dB"])
    st.session_state["B_dA"] = st.text_input(f"P(B{K}A{D})", value=st.session_state["B_dA"])

with col3:
    st.session_state["AgdB"] = st.text_input(f"P(A {G} B{D})", value=st.session_state["AgdB"])
    st.session_state["dAgB"] = st.text_input(f"P(A{D} {G} B)", value=st.session_state["dAgB"])
    st.session_state["dAgdB"] = st.text_input(f"P(A{D} {G} B{D})", value=st.session_state["dAgdB"])
    st.session_state["dAhdB"] = st.text_input(f"P(A{D} {H} B{D})", value=st.session_state["dAhdB"])

is_ind = st.checkbox("Giả định A, B độc lập")

# Nút Xóa và Nút Giải
btn_col1, btn_col2 = st.columns(2)
with btn_col1:
    if st.button("🗑️ XÓA TẤT CẢ", use_container_width=True, type="secondary"):
        for key in keys:
            st.session_state[key] = ""
        st.rerun()

with btn_col2:
    calculate_clicked = st.button("🚀 GIẢI TOÁN", use_container_width=True, type="primary")

# --- PHẦN 2: LOGIC TÍNH TOÁN ---
if calculate_clicked:
    try:
        # Chuyển dữ liệu sang dạng số
        p = {k: float(st.session_state[k]) if st.session_state[k] != "" else None for k in keys}
        steps = []

        # Vòng lặp suy luận (Cơ chế Domino)
        for _ in range(10):
            # Biến cố đối
            if p['A'] is not None and p['dA'] is None: p['dA'] = round(1-p['A'], 4); steps.append(f"P(A{D}) = 1 - P(A) = {p['dA']}")
            if p['B'] is not None and p['dB'] is None: p['dB'] = round(1-p['B'], 4); steps.append(f"P(B{D}) = 1 - P(B) = {p['dB']}")
            # Độc lập
            if is_ind and p['A'] is not None and p['B'] is not None and p['AgB'] is None:
                p['AgB'] = round(p['A']*p['B'], 4); steps.append(f"Vì A,B độc lập: P(A{G}B) = P(A).P(B) = {p['AgB']}")
            # Công thức cộng
            if all(p[k] is not None for k in ['A','B','AgB']) and p['AhB'] is None:
                p['AhB'] = round(p['A']+p['B']-p['AgB'], 4); steps.append(f"P(A{H}B) = P(A)+P(B)-P(A{G}B) = {p['AhB']}")
            # Điều kiện
            if p['AgB'] is not None and p['B'] and p['A_B'] is None: p['A_B'] = round(p['AgB']/p['B'], 4); steps.append(f"P(A|B) = P(A{G}B)/P(B) = {p['A_B']}")

        # Hiển thị kết quả
        st.divider()
        res_cols = st.columns(4)
        display_list = [("P(A)", 'A'), ("P(B)", 'B'), ("P(A∩B)", 'AgB'), ("P(A∪B)", 'AhB')]
        for i, (label, k) in enumerate(display_list):
            res_cols[i % 4].metric(label, p[k] if p[k] is not None else "---")

        st.subheader("📚 Các bước giải:")
        for s in list(dict.fromkeys(steps)): st.write(f"✅ {s}")

    except Exception as e:
        st.error(f"Lỗi nhập liệu: {e}")
        # --- PHẦN 2: LOGIC TÍNH TOÁN (60 VÒNG LẶP + TỐI ƯU) ---
if calculate_clicked:
    try:
        p = {k: float(st.session_state[k]) if st.session_state[k] != "" else None for k in keys}
        steps = []

        # Tăng lên 60 vòng lặp để đảm bảo không sót bất kỳ mối liên hệ nào
        for i in range(60):
            old_p = p.copy() # Lưu lại trạng thái cũ để kiểm tra
            
            # 1. Biến cố đối
            if p['A'] is not None and p['dA'] is None: p['dA'] = round(1-p['A'], 4); steps.append(f"P(A{D}) = 1-P(A) = {p['dA']}")
            if p['dA'] is not None and p['A'] is None: p['A'] = round(1-p['dA'], 4); steps.append(f"P(A) = 1-P(A{D}) = {p['A']}")
            if p['B'] is not None and p['dB'] is None: p['dB'] = round(1-p['B'], 4); steps.append(f"P(B{D}) = 1-P(B) = {p['dB']}")
            if p['dB'] is not None and p['B'] is None: p['B'] = round(1-p['dB'], 4); steps.append(f"P(B) = 1-P(B{D}) = {p['B']}")

            # 2. Công thức cộng (Hợp) và Giao
            if all(p[k] is not None for k in ['A','B','AgB']) and p['AhB'] is None:
                p['AhB'] = round(p['A']+p['B']-p['AgB'], 4); steps.append(f"P(A{H}B) = P(A)+P(B)-P(A{G}B) = {p['AhB']}")
            if all(p[k] is not None for k in ['A','B','AhB']) and p['AgB'] is None:
                p['AgB'] = round(p['A']+p['B']-p['AhB'], 4); steps.append(f"P(A{G}B) = P(A)+P(B)-P(A{H}B) = {p['AgB']}")

            # 3. De Morgan & Biến cố đối phức hợp
            if p['AhB'] is not None and p['dAgdB'] is None: p['dAgdB'] = round(1-p['AhB'], 4); steps.append(f"P(A{D}{G}B{D}) = 1-P(A{H}B) = {p['dAgdB']}")
            if p['AgB'] is not None and p['dAhdB'] is None: p['dAhdB'] = round(1-p['AgB'], 4); steps.append(f"P(A{D}{H}B{D}) = 1-P(A{G}B) = {p['dAhdB']}")

            # 4. Xác suất điều kiện (Tất cả các trường hợp)
            # A|B
            if p['AgB'] is not None and p['B'] and p['A_B'] is None: p['A_B'] = round(p['AgB']/p['B'], 4); steps.append(f"P(A{K}B) = P(A{G}B)/P(B) = {p['A_B']}")
            # A|B-đối (Cái ông cần cho bài test IELTS)
            if p['AgdB'] is not None and p['dB'] and p['A_dB'] is None: p['A_dB'] = round(p['AgdB']/p['dB'], 4); steps.append(f"P(A{K}B{D}) = P(A{G}B{D})/P(B{D}) = {p['A_dB']}")
            # B|A
            if p['AgB'] is not None and p['A'] and p['B_A'] is None: p['B_A'] = round(p['AgB']/p['A'], 4); steps.append(f"P(B{K}A) = P(A{G}B)/P(A) = {p['B_A']}")

            # 5. Xác suất tích (Giao thành phần)
            if p['A'] is not None and p['AgB'] is not None and p['AgdB'] is None:
                p['AgdB'] = round(p['A'] - p['AgB'], 4); steps.append(f"P(A{G}B{D}) = P(A) - P(A{G}B) = {p['AgdB']}")
            if p['B'] is not None and p['AgB'] is not None and p['dAgB'] is None:
                p['dAgB'] = round(p['B'] - p['AgB'], 4); steps.append(f"P(A{D}{G}B) = P(B) - P(A{G}B) = {p['dAgB']}")
            
            # Kiểm tra nếu không có gì mới được tính thêm thì ngắt vòng lặp sớm cho mượt
            if p == old_p:
                break

        # Hiển thị kết quả... (Giữ nguyên phần hiển thị bên dưới)

