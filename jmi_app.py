import streamlit as st
import pandas as pd
from datetime import datetime
import os
import base64
import plotly.express as px

# --- 1. Page Configuration ---
st.set_page_config(page_title="JMI | Strategic Management Portal", page_icon="🛡️", layout="wide")

# --- 2. UI Styling (Golden Luxury Theme) ---
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600&family=Inter:wght@400;700&display=swap" rel="stylesheet">
<style>
    .stApp { background: radial-gradient(circle, #002d5a 0%, #001529 100%); }
    [data-testid="stSidebar"] { background-color: #001529 !important; border-right: 2px solid #D4AF37; }
    html, body, [data-testid="stWidgetLabel"], .stMarkdown, p, span, label, li, div, h1, h2, h3, .stMetric {
        color: #D4AF37 !important; font-family: 'Inter', sans-serif;
    }
    .stButton>button { 
        background: linear-gradient(135deg, #D4AF37 0%, #B8860B 100%) !important;
        color: #001529 !important; border-radius: 8px !important; font-weight: 700 !important; border: none !important;
    }
    [data-testid="stMetricValue"] { color: #FFFFFF !important; }
</style>
""", unsafe_allow_html=True)

# --- 3. Database Management ---
if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame([
        {"ID": "JMI-001", "Name": "CHAN SOKHOEURN", "Level": "HIGH SCHOOL", "Fee": 500.0, "Paid": "PAID", "Date": "2026-03-25"}
    ])

# Database for Skill Passport
if 'skills_db' not in st.session_state:
    st.session_state.skills_db = pd.DataFrame(columns=["ID", "Skill_Name", "Status", "Verified_By"])

# --- 4. Helper Function for Image ---
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return ""

# --- 5. Sidebar Navigation ---
with st.sidebar:
    logo_base64 = get_base64_image("logo.png")
    if logo_base64:
        st.markdown(f'<center><img src="data:image/png;base64,{logo_base64}" width="150"></center>', unsafe_allow_html=True)
    else:
        st.markdown("<center><h1 style='font-size:70px; margin:0;'>🛡️</h1></center>", unsafe_allow_html=True)
    
    st.markdown("<h2 style='text-align: center;'>JMI EXECUTIVE</h2>", unsafe_allow_html=True)
    st.markdown("---")
    pwd = st.text_input("Director's Key", type="password")
    
    if pwd == "JMI2026":
        choice = st.radio("STRATEGIC MODULES", ["Dashboard", "Enrollment", "Skill Passport", "Certification", "Financial Hub"])
    else:
        st.stop()

# --- MODULE 4: CERTIFICATION (REDESIGNED LUXURY) ---
if choice == "Certification":
    st.markdown("<h1>📜 Official Certification Hub</h1>", unsafe_allow_html=True)
    if not st.session_state.db.empty:
        # តំបន់កំណត់ហត្ថលេខា
        st.subheader("🖋️ Signature Settings")
        c_sig = st.columns(2)
        with c_sig[0]: st.success("Director: **DR. CHAN SOKHOEURN**")
        with c_sig[1]: ins_name = st.text_input("Instructor Name", value="DR. MEA LINA")
        
        st.markdown("---")
        rec_name = st.selectbox("Select Recipient:", st.session_state.db['Name'].tolist())
        
        if st.button("GENERATE LUXURY CERTIFICATE"):
            s = st.session_state.db[st.session_state.db['Name'] == rec_name].iloc[0]
            current_date = datetime.now().strftime("%B %d, %Y")
            
            # កូដ HTML/CSS សម្រាប់ទម្រង់វិញ្ញាបនបត្រប្រណីត
            st.markdown(f"""
            <div style="background-color: white; padding: 50px; border: 20px double #D4AF37; border-radius: 5px; color: #002d5a; text-align: center; position: relative; box-shadow: 0 0 30px rgba(0,0,0,0.5); font-family: 'Inter', sans-serif;">
                <div style="border: 2px solid #D4AF37; padding: 25px; border-radius: 3px; position: relative;">
                    
                    <h1 style="margin: 0; font-family: 'Cinzel', serif; font-size: 35px; color: #B8860B; text-shadow: 2px 2px 3px rgba(184, 134, 11, 0.3);">JUNIOR MEDICAL INSTITUTE</h1>
                    <hr style="border: 1px solid #D4AF37; width: 40%; margin: 15px auto;">
                    
                    <h1 style="font-family: 'Cinzel', serif; font-size: 40px; margin: 25px 0 10px 0; color: #002d5a;">CERTIFICATE OF EXCELLENCE</h1>
                    <p style="margin: 0; color: #555;"><i>This is to certify that</i></p>
                    
                    <h2 style="font-size: 45px; margin: 15px 0 20px 0; border-bottom: 3px solid #D4AF37; display: inline-block; padding: 0 40px; color: #001529;">{s['Name']}</h2>
                    
                    <p style="margin-top: 20px; color: #333; line-height: 1.6;">
                        has successfully completed the esteemed <b>{s['Level']}</b> program<br>
                        and has demonstrated proficiency in essential medical foundations.
                    </p>
                    
                    <h2 style="color: #B8860B; font-family: 'Cinzel', serif; letter-spacing: 5px; font-size: 30px; margin: 20px 0;">LITTLE MEDIC</h2>
                    <p style="font-size: 14px; color: #666;">Awarded this day, {current_date} | Phnom Penh, Cambodia</p>
                    
                    <div style="display: flex; justify-content: space-around; margin-top: 60px; align-items: flex-end;">
                        <div style="text-align: center; border-top: 1px solid #333; width: 220px; color: #333;">
                            <br><b>DR. CHAN SOKHOEURN</b><br><small>Director, JMI International</small>
                        </div>
                        <div style="text-align: center;">
                            <img src="https://api.qrserver.com/v1/create-qr-code/?size=70x70&data={s['ID']}" style="border: 1px solid #ccc; padding: 5px;">
                            <br><small style="color: #888; font-size: 9px;">Scan to Verify</small>
                        </div>
                        <div style="text-align: center; border-top: 1px solid #333; width: 220px; color: #333;">
                            <br><b>{ins_name}</b><br><small>Senior Instructor</small>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# --- ផ្នែកផ្សេងៗ (Dashboard, Enrollment, Skill Passport, Finance) នៅរក្សាដដែល ---
elif choice == "Dashboard":
    st.markdown("<h1>📊 JMI Strategic Analytics</h1>", unsafe_allow_html=True)
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Scholars", len(st.session_state.db))
    m2.metric("Total Revenue", f"${st.session_state.db[st.session_state.db['Paid'] == 'PAID']['Fee'].sum():,.2f}")
    m3.metric("Skills Certified", len(st.session_state.skills_db))
    st.dataframe(st.session_state.db, use_container_width=True)

elif choice == "Enrollment":
    st.markdown("<h1>📝 Scholar Registration</h1>", unsafe_allow_html=True)
    with st.form("reg"):
        n = st.text_input("Scholar Name")
        l = st.selectbox("Level", ["KINDERGARTEN", "PRIMARY SCHOOL", "JUNIOR HIGH SCHOOL", "HIGH SCHOOL"])
        if st.form_submit_button("REGISTER"):
            new = {"ID": f"JMI-{len(st.session_state.db)+1:03d}", "Name": n.upper(), "Level": l, "Fee": 250.0, "Paid": "PAID", "Date": "2026-03-25"}
            st.session_state.db = pd.concat([st.session_state.db, pd.DataFrame([new])], ignore_index=True)
            st.success("Success!")

elif choice == "Skill Passport":
    st.markdown("<h1>🛂 Medical Skill Passport</h1>", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 2])
    with col1:
        target_id = st.selectbox("Select Scholar ID", st.session_state.db['ID'].tolist())
        skill = st.selectbox("Medical Skill Area", ["First Aid Basics", "Anatomy Knowledge", "Vital Signs Monitoring"])
        if st.button("STAMP PASSPORT"):
            new_skill = {"ID": target_id, "Skill_Name": skill, "Status": "Certified", "Verified_By": "DR. CHAN SOKHOEURN"}
            st.session_state.skills_db = pd.concat([st.session_state.skills_db, pd.DataFrame([new_skill])], ignore_index=True)
            st.success("Skill Added!")
    with col2:
        st.dataframe(st.session_state.skills_db, use_container_width=True)

elif choice == "Financial Hub":
    st.markdown("<h1>💰 Financial Hub</h1>", unsafe_allow_html=True)
    st.data_editor(st.session_state.db, use_container_width=True)
