import streamlit as st
import pandas as pd
from datetime import datetime
import os
import plotly.express as px

# --- 1. Page Config ---
st.set_page_config(page_title="JMI | Strategic Management Portal", page_icon="🛡️", layout="wide")

# --- 2. Excel Sync Engine (បេះដូងនៃកម្មវិធី - ការពារការបាត់ទិន្នន័យ) ---
DB_FILE = "jmi_database.xlsx"

def load_data():
    if os.path.exists(DB_FILE):
        # ទាញយកទិន្នន័យពី Excel មកវិញ
        db = pd.read_excel(DB_FILE, sheet_name="Students")
        skills = pd.read_excel(DB_FILE, sheet_name="Skills")
        return db, skills
    else:
        # បង្កើតទិន្នន័យគំរូដំបូងបំផុត (Default)
        db = pd.DataFrame([{"ID": "JMI-001", "Name": "CHAN SOKHOEURN", "Level": "HIGH SCHOOL", "Fee": 500.0, "Paid": "PAID", "Date": "2026-03-25"}])
        skills = pd.DataFrame(columns=["ID", "Skill_Name", "Status", "Verified_By"])
        return db, skills

def save_to_excel(db, skills):
    # រក្សាទុកទិន្នន័យទាំងអស់ចូល Excel រាល់ពេលមានការផ្លាស់ប្តូរ
    with pd.ExcelWriter(DB_FILE, engine='openpyxl') as writer:
        db.to_excel(writer, sheet_name="Students", index=False)
        skills.to_excel(writer, sheet_name="Skills", index=False)

# ចាប់ផ្តើមទាញយកទិន្នន័យពេលបើក App ភ្លាម
if 'db' not in st.session_state or 'skills_db' not in st.session_state:
    st.session_state.db, st.session_state.skills_db = load_data()

# --- 3. Sidebar ---
with st.sidebar:
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
    # បង្ហាញតារាងទិន្នន័យសិស្សទាំងអស់ដែលមានក្នុង Excel
    st.subheader("📋 Current Enrollment Status")
    st.dataframe(st.session_state.db, use_container_width=True)

# --- MODULE 2: ENROLLMENT (ចុះឈ្មោះថ្មី) ---
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
            # រក្សាទុកចូល Excel ភ្លាមៗដើម្បីកុំឱ្យបាត់
            save_to_excel(st.session_state.db, st.session_state.skills_db)
            st.success("Registration Successful and Saved to Database!")

# --- MODULE 3: SKILL PASSPORT (បោះត្រាជំនាញ) ---
elif choice == "Skill Passport":
    st.markdown("<h1>🛂 Medical Skill Passport</h1>", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("🛡️ Stamp New Skill")
        target_id = st.selectbox("Select ID", st.session_state.db['ID'].tolist())
        skill = st.selectbox("Medical Skill Area", ["First Aid", "Anatomy", "Vital Signs", "Surgical Basics"])
        if st.button("STAMP PASSPORT"):
            new_skill = {"ID": target_id, "Skill_Name": skill, "Status": "Certified", "Verified_By": "DR. CHAN SOKHOEURN"}
            st.session_state.skills_db = pd.concat([st.session_state.skills_db, pd.DataFrame([new_skill])], ignore_index=True)
            # រក្សាទុកចូល Excel ភ្លាមៗ
            save_to_excel(st.session_state.db, st.session_state.skills_db)
            st.success("Skill Passport Updated!")
    with col2:
        st.subheader("📜 Skill Records")
        st.dataframe(st.session_state.skills_db, use_container_width=True)

# --- MODULE 5: FINANCIAL HUB (កែប្រែទិន្នន័យហិរញ្ញវត្ថុ) ---
elif choice == "Financial Hub":
    st.markdown("<h1>💰 Financial Hub (Live Database Editor)</h1>", unsafe_allow_html=True)
    st.info("💡 លោកគ្រូអាចកែប្រែទិន្នន័យក្នុងតារាងខាងក្រោម រួចចុច Save Changes ដើម្បី Update ចូល Excel ។")
    
    # មុខងារកែទិន្នន័យផ្ទាល់
    edited_df = st.data_editor(st.session_state.db, use_container_width=True)
    
    if st.button("💾 SAVE CHANGES TO EXCEL"):
        st.session_state.db = edited_df
        save_to_excel(st.session_state.db, st.session_state.skills_db)
        st.success("Excel Database has been successfully updated!")
