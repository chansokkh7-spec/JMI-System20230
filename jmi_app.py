import streamlit as st
import pandas as pd
from datetime import datetime
import os
import base64
import plotly.express as px

# --- 1. Page Configuration ---
st.set_page_config(page_title="JMI | Strategic Management Portal", page_icon="🛡️", layout="wide")

# --- 2. Luxury UI Styling (Deep Blue & Gold) ---
st.markdown("""
<style>
    .stApp { background: radial-gradient(circle, #002d5a 0%, #001529 100%); }
    [data-testid="stSidebar"] { background-color: #001529 !important; border-right: 2px solid #D4AF37; }
    html, body, [data-testid="stWidgetLabel"], .stMarkdown, p, span, label, h1, h2, h3, .stMetric {
        color: #D4AF37 !important; font-family: 'Inter', sans-serif;
    }
    .stButton>button { 
        background: linear-gradient(135deg, #D4AF37 0%, #B8860B 100%) !important;
        color: #001529 !important; border-radius: 8px !important; font-weight: bold !important; border: none !important;
    }
    [data-testid="stMetricValue"] { color: #FFFFFF !important; }
    .skill-card { border: 1px solid #D4AF37; padding: 15px; border-radius: 10px; background: rgba(255,255,255,0.05); }
</style>
""", unsafe_allow_html=True)

# --- 3. Database Management ---
if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame([
        {"ID": "JMI-001", "Name": "CHAN SOKHOEURN", "Level": "HIGH SCHOOL", "Fee": 500.0, "Paid": "PAID", "Date": "2026-03-25"}
    ])

# Database សម្រាប់ Skill Passport
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

# --- MODULE 1: DASHBOARD ---
if choice == "Dashboard":
    st.markdown("<h1>📊 JMI Strategic Analytics</h1>", unsafe_allow_html=True)
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Scholars", len(st.session_state.db))
    m2.metric("Total Revenue", f"${st.session_state.db[st.session_state.db['Paid'] == 'PAID']['Fee'].sum():,.2f}")
    m3.metric("Skills Certified", len(st.session_state.skills_db))
    
    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("🎓 Enrollment by Level")
        gold_colors = ['#D4AF37', '#B8860B', '#FFD700', '#DAA520']
        fig_pie = px.pie(st.session_state.db, names='Level', color_discrete_sequence=gold_colors, hole=0.4)
        fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="#D4AF37")
        st.plotly_chart(fig_pie, use_container_width=True)
    with c2:
        st.subheader("💵 Payment Analysis")
        fig_bar = px.bar(st.session_state.db, x='Paid', y='Fee', color='Paid', color_discrete_map={'PAID': '#D4AF37', 'UNPAID': '#C62828'})
        fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#D4AF37")
        st.plotly_chart(fig_bar, use_container_width=True)

# --- MODULE 2: ENROLLMENT ---
elif choice == "Enrollment":
    st.markdown("<h1>📝 Scholar Registration</h1>", unsafe_allow_html=True)
    with st.form("reg"):
        n = st.text_input("Scholar Name")
        l = st.selectbox("Level", ["KINDERGARTEN", "PRIMARY SCHOOL", "JUNIOR HIGH SCHOOL", "HIGH SCHOOL"])
        f = st.number_input("Fee Amount ($)", value=250.0)
        p = st.selectbox("Payment Status", ["PAID", "UNPAID"])
        if st.form_submit_button("REGISTER"):
            new_id = f"JMI-{len(st.session_state.db)+1:03d}"
            new = {"ID": new_id, "Name": n.upper(), "Level": l, "Fee": f, "Paid": p, "Date": datetime.now().strftime("%Y-%m-%d")}
            st.session_state.db = pd.concat([st.session_state.db, pd.DataFrame([new])], ignore_index=True)
            st.success(f"Registration Successful! ID: {new_id}")

# --- MODULE 3: SKILL PASSPORT (NEW) ---
elif choice == "Skill Passport":
    st.markdown("<h1>🛂 Medical Skill Passport</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("🛡️ Verify New Skill")
        target_id = st.selectbox("Select Scholar ID", st.session_state.db['ID'].tolist())
        skill = st.selectbox("Medical Skill Area", ["First Aid Basics", "Anatomy Knowledge", "Medical Terminology", "Vital Signs Monitoring", "Surgical Basics"])
        verifier = st.text_input("Verified By", value="DR. CHAN SOKHOEURN")
        
        if st.button("STAMP PASSPORT"):
            new_skill = {"ID": target_id, "Skill_Name": skill, "Status": "Certified", "Verified_By": verifier}
            st.session_state.skills_db = pd.concat([st.session_state.skills_db, pd.DataFrame([new_skill])], ignore_index=True)
            st.success(f"Skill '{skill}' added to Passport!")

    with col2:
        st.subheader("📜 Skill History")
        view_id = st.selectbox("Filter by Student ID", ["ALL"] + st.session_state.db['ID'].tolist())
        
        if view_id == "ALL":
            display_skills = st.session_state.skills_db
        else:
            display_skills = st.session_state.skills_db[st.session_state.skills_db['ID'] == view_id]
            student_name = st.session_state.db[st.session_state.db['ID'] == view_id]['Name'].values[0]
            st.info(f"Scholar: **{student_name}**")

        st.dataframe(display_skills, use_container_width=True)

# --- MODULE 4: CERTIFICATION ---
elif choice == "Certification":
    st.markdown("<h1>📜 Official Certification Hub</h1>", unsafe_allow_html=True)
    if not st.session_state.db.empty:
        st.subheader("🖋️ Signature Settings")
        c_sig = st.columns(2)
        with c_sig[0]: st.success("Director: **DR. CHAN SOKHOEURN**")
        with c_sig[1]: ins_name = st.text_input("Instructor Name", value="DR. MEA LINA")
        
        rec_name = st.selectbox("Select Student Name", st.session_state.db['Name'].tolist())
        if st.button("GENERATE LUXURY CERTIFICATE"):
            s = st.session_state.db[st.session_state.db['Name'] == rec_name].iloc[0]
            # ទាញយក Skills របស់សិស្សម្នាក់នេះមកបង្ហាញក្នុង Certificate (Optional)
            st.markdown(f"""
            <div style="background:white; padding:30px; border:10px double #002d5a; text-align:center; color:#333;">
                <div style="border:2px solid #D4AF37; padding:20px;">
                    <h3>JUNIOR MEDICAL INSTITUTE</h3>
                    <h1 style="color:#002d5a;">CERTIFICATE OF EXCELLENCE</h1>
                    <p>This is to certify that</p>
                    <h2 style="border-bottom:2px solid #D4AF37; display:inline-block; padding:0 20px;">{s['Name']}</h2>
                    <p>Level: <b>{s['Level']}</b></p>
                    <p><i>Distinguished in Medical Foundations</i></p>
                    <div style="display:flex; justify-content:space-around; margin-top:40px;">
                        <div style="border-top:1px solid #333; width:150px;"><br><b>DR. CHAN SOKHOEURN</b><br><small>Director</small></div>
                        <img src="https://api.qrserver.com/v1/create-qr-code/?size=60x60&data={s['ID']}" width="60">
                        <div style="border-top:1px solid #333; width:150px;"><br><b>{ins_name}</b><br><small>Instructor</small></div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# --- MODULE 5: FINANCIAL HUB ---
elif choice == "Financial Hub":
    st.markdown("<h1>💰 Financial Hub</h1>", unsafe_allow_html=True)
    st.data_editor(st.session_state.db, use_container_width=True)
