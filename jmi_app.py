import streamlit as st
import pandas as pd
from datetime import datetime
import os
import base64
import plotly.express as px

# --- 1. Page Configuration ---
st.set_page_config(page_title="JMI | Strategic Management Portal", page_icon="🛡️", layout="wide")

# --- 2. Luxury UI Styling ---
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
</style>
""", unsafe_allow_html=True)

# --- 3. Excel Database Engine (Save & Load) ---
DB_FILE = "jmi_database.xlsx"

def load_data():
    if os.path.exists(DB_FILE):
        with pd.ExcelWriter(DB_FILE, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
            pass # ចង់ឱ្យប្រាកដថា File ដំណើរការ
        db = pd.read_excel(DB_FILE, sheet_name="Students")
        skills = pd.read_excel(DB_FILE, sheet_name="Skills")
        return db, skills
    else:
        db = pd.DataFrame([{"ID": "JMI-001", "Name": "CHAN SOKHOEURN", "Level": "HIGH SCHOOL", "Fee": 500.0, "Paid": "PAID", "Date": "2026-03-25"}])
        skills = pd.DataFrame(columns=["ID", "Skill_Name", "Status", "Verified_By"])
        save_to_excel(db, skills)
        return db, skills

def save_to_excel(db, skills):
    with pd.ExcelWriter(DB_FILE, engine='openpyxl') as writer:
        db.to_excel(writer, sheet_name="Students", index=False)
        skills.to_excel(writer, sheet_name="Skills", index=False)

if 'db' not in st.session_state or 'skills_db' not in st.session_state:
    st.session_state.db, st.session_state.skills_db = load_data()

# --- 4. Sidebar & Security ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>JMI EXECUTIVE</h2>", unsafe_allow_html=True)
    st.markdown("---")
    pwd = st.text_input("Director's Key", type="password")
    if pwd == "JMI2026":
        choice = st.radio("STRATEGIC MODULES", ["Dashboard", "Enrollment", "Skill Passport", "Certification", "Financial Hub"])
        if st.button("💾 MANUAL SAVE TO EXCEL"):
            save_to_excel(st.session_state.db, st.session_state.skills_db)
            st.toast("Data securely saved to Excel!")
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
        fig_pie = px.pie(st.session_state.db, names='Level', color_discrete_sequence=['#D4AF37', '#B8860B'], hole=0.4)
        fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="#D4AF37", title="Enrollment by Level")
        st.plotly_chart(fig_pie, use_container_width=True)
    with c2:
        fig_bar = px.bar(st.session_state.db, x='Paid', y='Fee', color='Paid', color_discrete_map={'PAID': '#D4AF37', 'UNPAID': '#C62828'})
        fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#D4AF37", title="Payment Status")
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
            save_to_excel(st.session_state.db, st.session_state.skills_db) # Auto-Save
            st.success(f"Registration Successful! Data saved to Excel.")

# --- MODULE 3: SKILL PASSPORT ---
elif choice == "Skill Passport":
    st.markdown("<h1>🛂 Medical Skill Passport</h1>", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 2])
    with col1:
        target_id = st.selectbox("Select Scholar ID", st.session_state.db['ID'].tolist())
        skill = st.selectbox("Medical Skill Area", ["First Aid Basics", "Anatomy Knowledge", "Vital Signs Monitoring", "Surgical Basics"])
        if st.button("STAMP PASSPORT"):
            new_skill = {"ID": target_id, "Skill_Name": skill, "Status": "Certified", "Verified_By": "DR. CHAN SOKHOEURN"}
            st.session_state.skills_db = pd.concat([st.session_state.skills_db, pd.DataFrame([new_skill])], ignore_index=True)
            save_to_excel(st.session_state.db, st.session_state.skills_db) # Auto-Save
            st.success("Skill Stamped & Saved!")
    with col2:
        st.dataframe(st.session_state.skills_db, use_container_width=True)

# --- MODULE 4: CERTIFICATION ---
elif choice == "Certification":
    st.markdown("<h1>📜 Certification Hub</h1>", unsafe_allow_html=True)
    rec_name = st.selectbox("Select Student", st.session_state.db['Name'].tolist())
    if st.button("GENERATE LUXURY CERTIFICATE"):
        s = st.session_state.db[st.session_state.db['Name'] == rec_name].iloc[0]
        st.markdown(f"""
        <div style="background:white; padding:30px; border:10px double #002d5a; text-align:center; color:#333;">
            <h2 style="color:#002d5a;">JUNIOR MEDICAL INSTITUTE</h2>
            <h1 style="color:#D4AF37;">CERTIFICATE OF EXCELLENCE</h1>
            <p>This is to certify that <b>{s['Name']}</b></p>
            <p>Has successfully mastered the <b>{s['Level']}</b> Medical Roadmap.</p>
            <div style="margin-top:30px; border-top:1px solid #333; display:inline-block; width:200px;"><br>DR. CHAN SOKHOEURN</div>
        </div>
        """, unsafe_allow_html=True)

# --- MODULE 5: FINANCIAL HUB ---
elif choice == "Financial Hub":
    st.markdown("<h1>💰 Financial Hub (Excel Sync)</h1>", unsafe_allow_html=True)
    # អនុញ្ញាតឱ្យកែទិន្នន័យក្នុងតារាង រួច Save ចូល Excel វិញ
    edited_df = st.data_editor(st.session_state.db, use_container_width=True)
    if st.button("CONFIRM CHANGES & UPDATE EXCEL"):
        st.session_state.db = edited_df
        save_to_excel(st.session_state.db, st.session_state.skills_db)
        st.success("Excel Database Updated!")
