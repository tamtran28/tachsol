import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Bộ lọc Dữ liệu Chi nhánh", layout="wide")

st.title("📂 Công cụ Lọc Dữ liệu Đa Cột")

uploaded_file = st.file_uploader("Chọn tệp Excel", type=["xlsx"])

if uploaded_file:
    df_tt = pd.read_excel(uploaded_file, dtype=str)
    
    # --- LOGIC TÌM CỘT CHI NHÁNH ---
    # Danh sách các tên cột tiềm năng (viết thường để so sánh)
    potential_columns = ['branch_lap_dat_may', 'branch_code', 'brcd', 'ma_cn', 'chinhanh', 'SOL_ID_FROM', 'sol_id_from', 'SOL_ID',]
    
    # Tìm cột thực tế có trong file khớp với danh sách trên
    found_col = None
    for col in df_tt.columns:
        if col.lower() in potential_columns:
            found_col = col
            break
    
    if found_col:
        st.success(f"🔍 Đã nhận diện được cột dữ liệu: **{found_col}**")
        
        chi_nhanh = st.text_input("Nhập tên chi nhánh hoặc mã SOL:").strip().upper()

        if chi_nhanh:
            # Lọc dữ liệu trên cột vừa tìm thấy
            df_ftp_filtered = df_tt[df_tt[found_col].astype(str).str.upper().str.contains(chi_nhanh, na=False)]
            
            st.subheader(f"📌 Kết quả lọc cho: '{chi_nhanh}'")
            st.dataframe(df_ftp_filtered)

            # Xuất file
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                df_ftp_filtered.to_excel(writer, index=False)
            
            st.download_button(
                label="📥 Tải về kết quả",
                data=buffer.getvalue(),
                file_name=f"Filtered_{chi_nhanh}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    else:
        st.error("❌ Không tìm thấy cột nào liên quan đến Chi nhánh (BRCD, BRANCH_CODE...). Vui lòng kiểm tra lại file.")
