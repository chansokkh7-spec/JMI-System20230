import streamlit as st
import pandas as pd
from datetime import datetime
import os
import base64

# --- 1. Page Configuration ---
st.set_page_config(page_title="JMI | Strategic Management Portal", page_icon="🛡️", layout="wide")

# --- 2. UI Styling ---
st.markdown("""
<style>
    .stApp { background: radial-gradient(circle, #002d5a 0%, #001529 100%); }
    [data-testid="stSidebar"] { background-color: #001529 !important; border-right: 1px solid #D4AF37; }
    h1, h2, h3, p, span, label { color: #D4AF37 !important; font-family: 'Inter', sans-serif; }
    .stButton>button { background: linear-gradient(135deg, #D4AF37 0%, #B8860B 100%) !important; color: #001529 !important; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# --- 3. Database ---
if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame([
        {"ID": "JMI-001", "Name": "CHAN SOKHOEURN", "Level": "HIGH SCHOOL", "Fee": 500.0, "Paid": "PAID", "Date": "2026-03-25"}
    ])

# --- 4. Helper Function for Logo ---
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

# --- 5. Sidebar ---
with st.sidebar:
    logo_base = get_base64_image("logo.png")
    if logo_base: st.image(f"data:image/png;base64,{logo_base}")
    else: st.title("🛡️ JMI")
    
    st.markdown("---")
    pwd = st.text_input("Director's Key", type="password")
    if pwd == "JMI2026":
        choice = st.radio("STRATEGIC MODULES", ["Dashboard", "Enrollment", "Skill Passport", "Certification", "Financial Hub"])
    else:
        st.stop()

# --- MODULE 4: CERTIFICATION (FIXED ERROR) ---
if choice == "Certification":
    st.title("📜 Official Certification Hub")
    
    if not st.session_state.db.empty:
        # ប្រអប់បញ្ចូលឈ្មោះអ្នកចុះហត្ថលេខា (ដើម្បីងាយស្រួលប្តូរទៅថ្ងៃមុខ)
        st.subheader("🖋️ Signature Configuration")
        c_sig1, c_sig2 = st.columns(2)
        with c_sig1:
            dir_name = st.text_input("Director Name:", value="DR. CHAN SOKHOEURN")
            dir_title = st.text_input("Director Title:", value="Director, JMI International")
        with c_sig2:
            ins_name = st.text_input("Instructor Name:", value="DR. MEA LINA")
            ins_title = st.text_input("Instructor Title:", value="Senior Instructor")

        st.markdown("---")
        rec = st.selectbox("Select Student:", st.session_state.db['Name'].tolist())
        
        if st.button("GENERATE LUXURY CERTIFICATE"):
            s = st.session_state.db[st.session_state.db['Name'] == rec].iloc[0]
            
            # កំណត់ពណ៌តាមកម្រិត
            colors = {"KINDERGARTEN": "#2E7D32", "PRIMARY SCHOOL": "#1565C0", "JUNIOR HIGH SCHOOL": "#C62828", "HIGH SCHOOL": "#6A1B9A"}
            lvl_color = colors.get(s['Level'], "#D4AF37")
            
            logo_html = f'<img src="data:image/png;base64,{logo_base}" width="100">' if logo_base else '🛡️'

            # ប្រើ unsafe_allow_html=True ដើម្បីបង្ហាញ HTML ឱ្យត្រឹមត្រូវ
            st.markdown(f"""
            <div style="background: white; padding: 40px; border: 15px double {lvl_color}; text-align: center; color: #333;">
                <div style="border: 2px solid #D4AF37; padding: 20px;">
                    <div>{logo_html}</div>
                    <h2 style="color: #002d5a; margin: 10px 0;">JUNIOR MEDICAL INSTITUTE</h2>
                    <h1 style="color: {lvl_color}; font-size: 35px;">CERTIFICATE OF COMPLETION</h1>
                    <p>This is to certify that</p>
                    <h2 style="font-size: 40px; color: #002d5a; border-bottom: 2px solid #D4AF37; display: inline-block; padding: 0 20px;">{s['Name']}</h2>
                    <p>successfully completed the <b>{s['Level']}</b> program</p>
                    <h3 style="color: #B8860B;">LITTLE MEDIC</h3>
                    <p style="font-size: 12px;">Phnom Penh, Cambodia | {s['Date']}</p>
                    
                    <div style="display: flex; justify-content: space-around; margin-top: 50px;">
                        <div style="text-align: center; border-top: 1px solid #333; width: 200px;">
                            <br><b>{dir_name}</b><br><small>{dir_title}</small>
                        </div>
                        <div style="text-align: center;">
                            <img src="https://api.qrserver.com/v1/create-qr-code/?size=60x60&data={s['ID']}" width="60">
                        </div>
                        <div style="text-align: center; border-top: 1px solid #333; width: 200px;">
                            <br><b>{ins_name}</b><br><small>{ins_title}</small>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# --- MODULE ផ្សេងៗទៀត ---
elif choice == "Dashboard":
    st.title("📊 Dashboard")
    st.dataframe(st.session_state.db)
elif choice == "Enrollment":
    st.title("📝 Enrollment")
    with st.form("reg"):
        n = st.text_input("Name")
        l = st.selectbox("Level", ["KINDERGARTEN", "PRIMARY SCHOOL", "JUNIOR HIGH SCHOOL", "HIGH SCHOOL"])
        if st.form_submit_button("Submit"):
            new = {"ID": f"JMI-{len(st.session_state.db)+1:03d}", "Name": n.upper(), "Level": l, "Fee": 250.0, "Paid": "PAID", "Date": "2026-03-25"}
            st.session_state.db = pd.concat([st.session_state.db, pd.DataFrame([new])], ignore_index=True)
elif choice == "Skill Passport":
    st.title("📓 Skill Passport")
elif choice == "Financial Hub":
    st.title("💰 Financial Hub")
    st.data_editor(st.session_state.db)
