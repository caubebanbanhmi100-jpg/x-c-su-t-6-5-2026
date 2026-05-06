import streamlit as st

# 1. Cấu hình & Ký hiệu
st.set_page_config(page_title="Siêu Máy Tính Xác Suất 12H", layout="wide")
G, H, D, K = "∩", "∪", "̅", "|"
keys = ["A", "B", "AgB", "AhB", "dA", "dB", "A_B", "B_A", "A_dB", "B_dA", "dA_B", "dB_dA", "AgdB", "dAgB", "dAgdB", "dAhB", "dBhA", "dAhdB"]

# 2. Khởi tạo bộ nhớ
for key in keys:
    if key not in st.session_state:
        st.session_state[key] = ""

st.title("🚀 Siêu Máy Tính Xác Suất Toàn Diện (V.2.0)")
st.info("Bản nâng cấp 60 vòng lặp suy luận - Chấp mọi bài toán IELTS & ĐGNL.")

# 3. Giao diện nhập liệu
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

# 4. Nút bấm
b_col1, b_col2 = st.columns(2)
with b_col1:
    if st.button("🗑️ XÓA TẤT CẢ DỮ LIỆU", use_container_width=True):
        for k in keys: st.session_state[k] = ""
        st.rerun()
with b_col2:
    calculate = st.button("🚀 GIẢI TOÁN", type="primary", use_container_width=True)

# 5. Logic tính toán 60 vòng lặp
if calculate:
    try:
        p = {k: float(st.session_state[k]) if st.session_state[k] != "" else None for k in keys}
        steps = []
        for i in range(60):
            old_p = p.copy()
            # Đối
            if p['A'] is not None and p['dA'] is None: p['dA'] = round(1-p['A'], 4); steps.append(f"P(A{D}) = 1-P(A) = {p['dA']}")
            if p['dA'] is not None and p['A'] is None: p['A'] = round(1-p['dA'], 4); steps.append(f"P(A) = 1-P(A{D}) = {p['A']}")
            if p['B'] is not None and p['dB'] is None: p['dB'] = round(1-p['B'], 4); steps.append(f"P(B{D}) = 1-P(B) = {p['dB']}")
            if p['dB'] is not None and p['B'] is None: p['B'] = round(1-p['dB'], 4); steps.append(f"P(B) = 1-P(B{D}) = {p['B']}")
            # Cộng/Giao
            if all(p[k] is not None for k in ['A','B','AgB']) and p['AhB'] is None: p['AhB'] = round(p['A']+p['B']-p['AgB'], 4); steps.append(f"P(A{H}B) = P(A)+P(B)-P(A{G}B) = {p['AhB']}")
            if all(p[k] is not None for k in ['A','B','AhB']) and p['AgB'] is None: p['AgB'] = round(p['A']+p['B']-p['AhB'], 4); steps.append(f"P(A{G}B) = P(A)+P(B)-P(A{H}B) = {p['AgB']}")
            # Điều kiện & Giao thành phần
            if p['AgB'] is not None and p['B'] and p['A_B'] is None: p['A_B'] = round(p['AgB']/p['B'], 4); steps.append(f"P(A{K}B) = P(A{G}B)/P(B) = {p['A_B']}")
            if p['A'] is not None and p['AgB'] is not None and p['AgdB'] is None: p['AgdB'] = round(p['A']-p['AgB'], 4); steps.append(f"P(A{G}B{D}) = P(A)-P(A{G}B) = {p['AgdB']}")
            if p['AgdB'] is not None and p['dB'] and p['A_dB'] is None: p['A_dB'] = round(p['AgdB']/p['dB'], 4); steps.append(f"P(A{K}B{D}) = P(A{G}B{D})/P(B{D}) = {p['A_dB']}")
            if p['AhB'] is not None and p['dAgdB'] is None: p['dAgdB'] = round(1-p['AhB'], 4); steps.append(f"P(A{D}{G}B{D}) = 1-P(A{H}B) = {p['dAgdB']}")
            
            if p == old_p: break

        # 6. Hiển thị kết quả
        st.divider()
        res_cols = st.columns(4)
        show = [("P(A)",'A'), ("P(B)",'B'), ("P(A∩B)",'AgB'), ("P(A∪B)",'AhB'), ("P(A|B)",'A_B'), ("P(A|B̅)",'A_dB'), ("P(B|A)",'B_A'), ("P(A̅∩B̅)",'dAgdB')]
        for i, (label, k) in enumerate(show): res_cols[i%4].metric(label, p[k] if p[k] is not None else "---")
        
        st.subheader("📚 Giải chi tiết:")
        for s in list(dict.fromkeys(steps)): st.success(f"✅ {s}")
    except Exception as e: st.error(f"Lỗi: {e}")
