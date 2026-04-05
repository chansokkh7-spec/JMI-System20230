import streamlit as st
import pandas as pd
from datetime import datetime

# --- ១. ការកំណត់ទម្រង់កម្មវិធី (App Configuration) ---
st.set_page_config(
    page_title="JMI | Strategic Management Portal",
    page_icon="🏥",
    layout="wide"
)

# --- ២. ការរចនា Style (Safe CSS - គ្មានថ្ងៃ Error អក្សររាយប៉ាយ) ---
style_block = """
<link href="https://fonts.googleapis.com/css2?family=Great+Vibes&family=Cinzel:wght@700&family=DM+Serif+Display&family=Kantumruy+Pro:wght@400;700&display=swap" rel="stylesheet">
<style>
    html, body, [class*="css"], .stMarkdown {
        font-family: 'Kantumruy Pro', sans-serif;
    }
    .stApp { background-color: #f8f9fa; }
    
    /* Star Styling */
    .star-gold { color: #D4AF37; font-size: 25px; margin-right: 3px; }
    
    /* Premium Certificate Style */
    .cert-paper { 
        background-color: white; 
        border: 12px solid #001f3f; 
        padding: 10px; 
        box-shadow: 0 25px 50px rgba(0,0,0,0.3); 
        max-width: 800px; 
        margin: 30px auto; 
    }
    .cert-border { border: 4px double #D4AF37; padding: 40px; text-align: center; }
    .cert-header { font-family: 'Cinzel', serif; color: #001f3f; font-size: 40px; margin: 0; letter-spacing: 5px; }
    .student-name { font-family: 'Great Vibes', cursive; font-size: 55px; color: #D4AF37; margin: 15px 0; font-weight: normal; }
    .cert-text { font-family: 'DM Serif Display', serif; font-size: 18px; color: #333; line-height: 1.6; }
    .signature { font-family: 'Great Vibes', cursive; font-size: 30px; color: #001f3f; margin-bottom: -10px; }
    .sig-box { border-top: 1px solid #333; width: 180px; margin: auto; padding-top: 5px; font-family: serif; font-size: 13px; color: #333; }
</style>
"""
st.markdown(style_block, unsafe_allow_html=True)

# --- ៣. ការគ្រប់គ្រងទិន្នន័យ (Session State) ---
if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame([
        {
            "ID": "JMI-2026-001", 
            "Name": "Sokhoeurn Sovannachak", 
            "Level": "K-G3", 
            "Enroll_Date": "2026-03-25", 
            "Status": "Active", 
            "Skills": ["Clinical Hygiene", "Human Anatomy"]
        }
    ])

# --- ៤. របារចំហៀង (Sidebar Security) ---
st.sidebar.markdown("<h2 style='text-align: center; color: #001f3f;'>JMI EXECUTIVE</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<center><h1 style='font-size:60px;'>🏥</h1></center>", unsafe_allow_html=True)
st.sidebar.markdown("---")

pwd = st.sidebar.text_input("Director's Key", type="password", placeholder="Enter Password")

# --- ៥. កម្មវិធីចម្បង (Main Logic) ---
if pwd == "JMI2026":
    st.sidebar.success("Welcome, Dr. CHAN Sokhoeurn")
    
    # ម៉ឺនុយបញ្ជា (Menu)
    menu = st.sidebar.radio("STRATEGIC MODULES", ["📊 Dashboard", "🎓 Enrollment", "🏅 Skill Passport", "📜 Certification"])

    # --- ៥.១ ម៉ូឌុល Dashboard ---
    if menu == "📊 Dashboard":
        st.title("🏥 JMI Strategic Command Center")
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Scholars", len(st.session_state.db))
        c2.metric("Med-Modules", "12 Units")
        c3.metric("Capacity", "250 Seats")
        
        st.markdown("### 📋 Student Roster")
        # បង្ហាញតារាងដោយលាក់ Skill កុំឱ្យរញ៉េរញ៉ៃ
        st.dataframe(st.session_state.db.drop(columns=['Skills']), use_container_width=True)

    # --- ៥.២ ម៉ូឌុល Enrollment ---
    elif menu == "🎓 Enrollment":
        st.header("Register New Scholar")
        with st.form("enroll_form", clear_on_submit=True):
            name = st.text_input("Full Name (ឈ្មោះពេញ)")
            sid = st.text_input("Scholar ID (លេខសម្គាល់)")
            level = st.selectbox("Academic Level", ["K-G3", "G4-G6", "G7-G9", "G10-G12"])
            
            if st.form_submit_button("✅ CONFIRM ENROLLMENT"):
                if name and sid:
                    new_entry = pd.DataFrame([{
                        "ID": sid, 
                        "Name": name, 
                        "Level": level, 
                        "Enroll_Date": datetime.now().strftime("%Y-%m-%d"), 
                        "Status": "Active", 
                        "Skills": []
                    }])
                    st.session_state.db = pd.concat([st.session_state.db, new_entry], ignore_index=True)
                    st.success(f"Scholar '{name}' has been added successfully.")
                else:
                    st.error("សូមបំពេញព័ត៌មានទាំងឈ្មោះ និងលេខសម្គាល់!")

    # --- ៥.៣ ម៉ូឌុល Skill Passport ---
    elif menu == "🏅 Skill Passport":
        st.header("🏅 Skill Mastery Passport")
        sel_student = st.selectbox("Select Student:", st.session_state.db['Name'].tolist())
        
        # ទាញយក Index របស់សិស្សដែលបានរើស
        idx = st.session_state.db.index[st.session_state.db['Name'] == sel_student][0]
        
        available_skills = ["Clinical Hygiene", "Human Anatomy", "Vital Signs", "First Aid (CPR)", "Medical Ethics", "Nutrition"]
        current_skills = st.session_state.db.at[idx, 'Skills']
        
        st.write("Tick the medical foundations completed by the scholar:")
        new_selection = []
        
        # បង្កើត Checkbox ជា ២ ជួរដេក
        col1, col2 = st.columns(2)
        for i, skill in enumerate(available_skills):
            with (col1 if i % 2 == 0 else col2):
                if st.checkbox(skill, value=(skill in current_skills)):
                    new_selection.append(skill)
        
        if st.button("💾 Save Progress"):
            st.session_state.db.at[idx, 'Skills'] = new_selection
            st.success(f"Updated skills for {sel_student}!")
            st.rerun()

    # --- ៥.៤ ម៉ូឌុល Certification ---
    elif menu == "📜 Certification":
        st.header("Certification Generator")
        target = st.selectbox("Select Recipient:", st.session_state.db['Name'].tolist())
        
        # ទាញយកព័ត៌មានសិស្ស
        s_info = st.session_state.db[st.session_state.db['Name'] == target].iloc[0]
        
        if st.button("🌟 GENERATE CERTIFICATE"):
            if len(s_info['Skills']) == 0:
                st.warning("Scholar នេះមិនទាន់ទទួលបាន Skill ណាមួយនៅឡើយទេ ដូច្នេះមិនទាន់អាចបង្កើតវិញ្ញាបនបត្របានទេ។")
            else:
                st.balloons()
                
                # បង្កើតផ្កាយមាសតាមចំនួន Skill ដែលទទួលបាន
                stars_html = "".join(['<span class="star-gold">★</span>' for _ in range(len(s_info['Skills']))])
                
                # បង្កើត HTML វិញ្ញាបនបត្រ
                certificate_html = f"""
                <div class="cert-paper">
                    <div class="cert-border">
                        <p style="letter-spacing: 5px; color: #555; font-size: 12px; margin-bottom:10px;">JUNIOR MEDICAL INSTITUTE</p>
                        <h1 class="cert-header">CERTIFICATE</h1>
                        <div style="margin: 10px 0;">{stars_html}</div>
                        <p class="cert-text" style="font-style: italic;">This award is proudly presented to</p>
                        <h2 class="student-name">{s_info['Name']}</h2>
                        <p class="cert-text">for successfully completing the<br><b>Medical Foundation Pathway</b> ({s_info['Level']})</p>
                        <div style="margin-top: 50px; display: flex; justify-content: space-around;">
                            <div style="text-align:center;">
                                <p style="font-size:14px; margin-bottom:5px;">{datetime.now().strftime("%d %B %Y")}</p>
                                <div class="sig-box">DATE</div>
                            </div>
                            <div style="text-align:center;">
                                <p class="signature">Dr. Chan Sokhoeurn</p>
                                <div class="sig-box">ACADEMIC DIRECTOR</div>
                            </div>
                        </div>
                    </div>
                </div>
                """
                st.markdown(certificate_html, unsafe_allow_html=True)

# --- ៦. ផ្ទាំង Lock បិទជិត ---
else:
    st.title("🏥 JMI Strategic Command Portal")
    st.info("🔒 សូមបញ្ចូល Password 'JMI2026' នៅរបារចំហៀងខាងឆ្វេង ដើម្បីបើកដំណើរការប្រព័ន្ធ។")
