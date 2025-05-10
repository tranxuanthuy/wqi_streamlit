import streamlit as st
import base64
import pandas as pd
from features.dss1.dss1_main import calculate_wqi_for_df
from utils.map import render_wqi_map
import joblib
st.set_page_config(page_title="Calculator - watertech.vn", layout="wide")

# external CSS
def load_css(css_file):
    with open(css_file) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
load_css("style.css")

# encode image to base64
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        b64_data = base64.b64encode(img_file.read()).decode()
        return f"data:image/png;base64,{b64_data}"
# logo image
img_base64 = get_base64_image("assets/logo.png")

# Header and banner
st.markdown(f"""
    <div class="header">
        <a href="https://geoportal.watertech.vn/" target="_blank">
            <img src="{img_base64}" alt="Logo">
        </a>
    </div>

    <div class="content-wrapper">
        <div class="main-banner">
            <p class="main-banner__welcome">Welcome</p>
            <p>WaterTech GeoPortal – Calculator</p>
            <a href="https://geoportal.watertech.vn/">Geoportal</a>
        </div>
    </div>
""", unsafe_allow_html=True)

# Main content
tabs = st.tabs(["WQI", "WQ Predictor"])

process_clicked = False  # Biến cờ xác định có nhấn nút hay không

with tabs[0]:
    st.markdown("""
        <div style="text-align: center;">
            <h2>Water Quality Index (WQI)</h2>
            <p>Chức năng tính toán và hiển thị chỉ số chất lượng nước.</p>
        </div>
    """, unsafe_allow_html=True)

    # STEP 1 - DOWNLOAD TEMPLATE
    st.markdown("""
        <div style="border: 1px solid #ccc; border-left: 6px solid #2b6490;
             padding: 15px; margin-bottom: 15px; background-color: #f9f9f9;
             border-radius: 6px;">
            <h5>Step 1: Download Template</h5>
            <p>Tải về file mẫu CSV.</p>
    """, unsafe_allow_html=True)

    with open("assets/csv_templates/dss1_template.csv", "rb") as f:
        st.download_button("📥 Tải template CSV", f, "wqi_template.csv", "text/csv")
    st.markdown("</div>", unsafe_allow_html=True)

    # STEP 2 - UPLOAD FILE
    st.markdown("""
        <div style="border: 1px solid #ccc; border-left: 6px solid #2b6490;
             padding: 15px; margin-bottom: 15px; background-color: #f9f9f9;
             border-radius: 6px;">
            <h5>Step 2: Upload Your Data File</h5>
            <p>Tải lên file CSV đã điền dữ liệu đúng định dạng template.</p>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 4])
    with col1:
        uploaded_file = st.file_uploader("📤 Tải lên file CSV", type="csv", label_visibility="collapsed")

    st.markdown("</div>", unsafe_allow_html=True)

    # LUÔN HIỂN THỊ NÚT XỬ LÝ
    if st.button("🧮 Process"):
        if uploaded_file is None:
            st.error("⚠️ Vui lòng tải lên file CSV trước khi nhấn Xử lý.")
        else:
            df = pd.read_csv(uploaded_file)
            wqi_df = calculate_wqi_for_df(df)

            st.success("✅ Xử lý hoàn tất!")
            st.download_button(
                "📥 Download DSS1 Results CSV",
                data=wqi_df.to_csv(index=False).encode("utf-8"),
                file_name="wqi_results.csv",
                mime="text/csv"
            )

            st.markdown("### 🗺️ Bản đồ kết quả DSS1")
            with st.spinner("Đang tải bản đồ..."):
                render_wqi_map(wqi_df)

with tabs[1]:
    st.markdown("""
        <div style="text-align: center;">
            <h2>Water Quality Predictor</h2>
            <p>Dự đoán giá trị chất lượng nước từ các thành phần</p>
        </div>
    """, unsafe_allow_html=True)
    model = joblib.load("features/wqi_predictor/model/model_wqi.pkl")
    bhc = st.number_input("BHC", min_value=0.0, max_value=100.0, value=0.0, step=0.1)
    cod = st.number_input("COD", min_value=0.0, max_value=100.0, value=0.0, step=0.1)
    bod5 = st.number_input("BOD5", min_value=0.0, max_value=100.0, value=0.0, step=0.1)
    toc = st.number_input("TOC", min_value=0.0, max_value=100.0, value=0.0, step=0.1)
    cr6 = st.number_input("Cr6", min_value=0.0, max_value=100.0, value=0.0, step=0.1)
    cd = st.number_input("Cd", min_value=0.0, max_value=100.0, value=0.0, step=0.1)
    from features.wqi_predictor.utils import predict_wqi
    
    if st.button("🧮 Dự đoán WQI"):
        wqi_pred = predict_wqi(model, {
            "BOD5": bod5,
            "COD": cod,
            "TOC": toc,
            "BHC": bhc,
            "Cd": cd,
            "Cr6": cr6
        })
        st.success(f"✅ Giá trị WQI dự đoán: {wqi_pred:.2f}")

# Footer
st.markdown("""
    <div class="footer">
        <p>Powered by: <a href="https://geoportal.watertech.vn/" target="_blank">Geoportal</a></p>
    </div>
""", unsafe_allow_html=True)