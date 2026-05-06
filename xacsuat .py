import streamlit as st

# Cấu hình giao diện rộng để chứa đủ các cột
st.set_page_config(page_title="Siêu Máy Tính Xác Suất 12H", layout="wide")

# Định nghĩa ký hiệu toán học
G, H, D, K = "∩", "∪", "̅", "|"

st.title("Bố của xác suất thống kê ")
st.info("Nhập ít nhất 2-3 giá trị bất kỳ để hệ thống tự động suy luận toàn bộ ma trận biến cố.")

# --- PHẦN 1: GIAO DIỆN NHẬP LIỆU (3 CỘT) ---
col1, col2, col3 = st.columns(3)

with col1:
    pa = st.text_input("P(A)", key="A")
    pb = st.text_input("P(B)", key="B")
    pagb = st.text_input(f"P(A {G} B)", key="AgB")
    pahb = st.text_input(f"P(A {H} B)", key="AhB")
    pda = st.text_input(f"P(A{D})", key="dA")
    pdb = st.text_input(f"P(B{D})", key="dB")

with col2:
    pab = st.text_input(f"P(A{K}B)", key="A_B")
    pba = st.text_input(f"P(B{K}A)", key="B_A")
    padb = st.text_input(f"P(A{K}B{D})", key="A_dB")
    pbda = st.text_input(f"P(B{K}A{D})", key="B_dA")
    pdab = st.text_input(f"P(A{D}{K}B)", key="dA_B")
    pdbda = st.text_input(f"P(B{D}{K}A{D})", key="dB_dA")

with col3:
    pagdb = st.text_input(f"P(A {G} B{D})", key="AgdB")
    pdagb = st.text_input(f"P(A{D} {G} B)", key="dAgB")
    pdagdb = st.text_input(f"P(A{D} {G} B{D})", key="dAgdB")
    pdahb = st.text_input(f"P(A{D} {H} B)", key="dAhB")
    pdbha = st.text_input(f"P(B{D} {H} A)", key="dBhA")
    pdahdb = st.text_input(f"P(A{D} {H} B{D})", key="dAhdB")

is_ind = st.checkbox("Giả định A, B độc lập")

# --- PHẦN 2: LOGIC TÍNH TOÁN ---
if st.button("🚀 BẮT ĐẦU GIẢI TOÁN", type="primary", use_container_width=True):
    try:
        # Lấy dữ liệu từ các ô nhập
        keys = ["A", "B", "AgB", "AhB", "dA", "dB", "A_B", "B_A", "A_dB", "B_dA", "dA_B", "dB_dA", "AgdB", "dAgB", "dAgdB", "dAhB", "dBhA", "dAhdB"]
        p = {k: float(st.session_state[k]) if st.session_state[k] else None for k in keys}
        steps = []

        # Chạy vòng lặp suy luận 15 lần để vét cạn công thức (Cơ chế Domino)
        for _ in range(15):
            # 1. Biến cố đối
            if p['A'] is not None and p['dA'] is None: p['dA'] = round(1-p['A'], 4); steps.append(f"P(A{D}) = 1 - P(A) = {p['dA']}")
            if p['dA'] is not None and p['A'] is None: p['A'] = round(1-p['dA'], 4); steps.append(f"P(A) = 1 - P(A{D}) = {p['A']}")
            if p['B'] is not None and p['dB'] is None: p['dB'] = round(1-p['B'], 4); steps.append(f"P(B{D}) = 1 - P(B) = {p['dB']}")
            if p['dB'] is not None and p['B'] is None: p['B'] = round(1-p['dB'], 4); steps.append(f"P(B) = 1 - P(B{D}) = {p['B']}")

            # 2. Độc lập
            if is_ind and p['A'] is not None and p['B'] is not None and p['AgB'] is None:
                p['AgB'] = round(p['A']*p['B'], 4); steps.append(f"Vì A,B độc lập: P(A{G}B) = P(A).P(B) = {p['AgB']}")

            # 3. Luật cộng & Giao
            if all(p[k] is not None for k in ['A','B','AgB']) and p['AhB'] is None:
                p['AhB'] = round(p['A']+p['B']-p['AgB'], 4); steps.append(f"P(A{H}B) = P(A)+P(B)-P(A{G}B) = {p['AhB']}")
            if all(p[k] is not None for k in ['A','B','AhB']) and p['AgB'] is None:
                p['AgB'] = round(p['A']+p['B']-p['AhB'], 4); steps.append(f"P(A{G}B) = P(A)+P(B)-P(A{H}B) = {p['AgB']}")

            # 4. Xác suất có điều kiện thuận
            if p['AgB'] is not None and p['B'] and p['A_B'] is None: p['A_B'] = round(p['AgB']/p['B'], 4); steps.append(f"P(A|B) = P(A{G}B)/P(B) = {p['A_B']}")
            if p['AgB'] is not None and p['A'] and p['B_A'] is None: p['B_A'] = round(p['AgB']/p['A'], 4); steps.append(f"P(B|A) = P(A{G}B)/P(A) = {p['B_A']}")

            # 5. Luật hiệu (Venn)
            if p['A'] is not None and p['AgB'] is not None and p['AgdB'] is None:
                p['AgdB'] = round(p['A'] - p['AgB'], 4); steps.append(f"P(A{G}B{D}) = P(A) - P(A{G}B) = {p['AgdB']}")
            if p['B'] is not None and p['AgB'] is not None and p['dAgB'] is None:
                p['dAgB'] = round(p['B'] - p['AgB'], 4); steps.append(f"P(A{D}{G}B) = P(B) - P(A{G}B) = {p['dAgB']}")

            # 6. De Morgan
            if p['AhB'] is not None and p['dAgdB'] is None:
                p['dAgdB'] = round(1 - p['AhB'], 4); steps.append(f"P(A{D}{G}B{D}) = 1 - P(A{H}B) = {p['dAgdB']}")
            if p['AgB'] is not None and p['dAhdB'] is None:
                p['dAhdB'] = round(1 - p['AgB'], 4); steps.append(f"P(A{D}{H}B{D}) = 1 - P(A{G}B) = {p['dAhdB']}")

        # --- PHẦN 3: HIỂN THỊ MA TRẬN KẾT QUẢ ---
        st.markdown("---")
        st.subheader("📊 Ma trận kết quả đầy đủ")
        res_col1, res_col2, res_col3 = st.columns(3)
        
        # Danh sách nhãn hiển thị cho đẹp
        display_labels = {
            "A": "P(A)", "B": "P(B)", "dA": f"P(A{D})", "dB": f"P(B{D})",
            "AgB": f"P(A{G}B)", "AhB": f"P(A{H}B)", "A_B": "P(A|B)", "B_A": "P(B|A)",
            "AgdB": f"P(A{G}B{D})", "dAgB": f"P(A{D}{G}B)", "dAgdB": f"P(A{D}{G}B{D})", "dAhdB": f"P(A{D}{H}B{D})"
        }

        for i, (key, label) in enumerate(display_labels.items()):
            val_out = p.get(key)
            target = [res_col1, res_col2, res_col3][i % 3]
            if val_out is not None:
                target.metric(label, val_out)
            else:
                target.write(f"**{label}**: ❌")

        # --- PHẦN 4: HIỂN THỊ CÁC BƯỚC GIẢI ---
        st.markdown("---")
        st.subheader("📚 Quy trình giải chi tiết (Dành cho tự luận)")
        if steps:
            for s in list(dict.fromkeys(steps)):
                st.success(s)
        else:
            st.warning("Nhập thêm ít nhất 2 biến số để thấy quy trình giải!")

    except Exception as e:
        st.error(f"Lỗi: Hãy nhập đúng định dạng số thập phân (Ví dụ: 0.5). Chi tiết: {e}")
