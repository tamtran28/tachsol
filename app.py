import streamlit as st
import pandas as pd
import io

# Page configuration
st.set_page_config(page_title="Bộ lọc Dữ liệu Chi nhánh", layout="wide")

st.title("📂 Công cụ Lọc Dữ liệu MỤC 51")
st.markdown("Tải lên tệp Excel và lọc dữ liệu theo **Mã SOL** hoặc **Tên chi nhánh**.")

# 1. File Uploader
uploaded_file = st.file_uploader("Chọn tệp Excel (KTNB_MUC51.xlsx)", type=["xlsx"])

if uploaded_file:
    # Load data
    @st.cache_data
    def load_data(file):
        return pd.read_excel(file, dtype=str)
    
    df_tt = load_data(uploaded_file)
    st.success(f"Đã tải thành công {len(df_tt)} dòng dữ liệu.")

    # 2. Filter Input
    chi_nhanh = st.text_input("Nhập tên chi nhánh hoặc mã SOL cần lọc:", placeholder="Ví dụ: HANOI hoặc 001").strip().upper()

    if chi_nhanh:
        # Filtering logic
        df_ftp_filtered = df_tt[df_tt['BRANCH_LAP_DAT_MAY'].astype(str).str.upper().str.contains(chi_nhanh, na=False)]
        
        # 3. Results Display
        st.subheader(f"📌 Kết quả lọc cho: '{chi_nhanh}'")
        st.write(f"Tìm thấy **{len(df_ftp_filtered)}** dòng.")
        
        if not df_ftp_filtered.empty:
            st.dataframe(df_ftp_filtered, use_container_width=True)

            # 4. Download Button
            # We use an in-memory buffer to allow downloading without saving to the local disk
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                df_ftp_filtered.to_excel(writer, index=False, sheet_name='Filtered_Data')
            
            st.download_button(
                label="📥 Tải về tệp Excel đã lọc",
                data=buffer.getvalue(),
                file_name=f"MUC51_Filtered_{chi_nhanh}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.warning("Không tìm thấy dữ liệu phù hợp với từ khóa trên.")
else:
    st.info("Vui lòng tải tệp Excel lên để bắt đầu.")
