import streamlit as st

# Cấu hình giao diện
st.set_page_config(page_title="Siêu Máy Tính Xác Suất 12H", layout="wide")

# Ký hiệu toán học
G, H, D, K = "∩", "∪", "̅", "|"

st.title("🚀 Siêu Máy Tính Xác Suất Toàn Diện")
st.info("Nhập các giá trị đã biết. Nút Xóa sẽ giúp ông reset nhanh để làm bài mới.")

# Danh sách các key để quản lý dữ liệu
keys = ["A", "B", "AgB", "AhB", "dA", "dB", "A_B", "B_A", "A_dB", "B_dA", "dA_B", "dB_dA", "AgdB", "dAgB", "dAgdB", "dAhdB"]

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

        # Vòng lặp suy luận (10 vòng lặp)
        for _ in range(10):
            # Biến cố đối
            if p['A'] is not None and p['dA'] is None: p['dA'] = round(1-p['A'], 4); steps.append(f"P(A{D}) = 1 - P(A) = {p['dA']}")
            if p['B'] is not None and p['dB'] is None: p['dB'] = round(1-p['B'], 4); steps.append(f"P(B{D}) = 1 - P(B) = {p['dB']}")
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
