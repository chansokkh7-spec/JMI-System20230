import streamlit as st
import pandas as pd
from datetime import datetime

# --- ១. ការកំណត់ទម្រង់កម្មវិធី ---
st.set_page_config(
    page_title="JMI | Strategic Management Portal",
    page_icon="🏥",
    layout="wide"
)

# --- ២. ការរចនា Style (Safe CSS) ---
style_block = """
<link href="https://fonts.googleapis.com/css2?family=Great+Vibes&family=Cinzel:wght@700&family=DM+Serif+Display&family=Kantumruy+Pro:wght@400;700&display=swap" rel="stylesheet">
<style>
    html, body, [class*="css"], .stMarkdown {
        font-family: 'Kantumruy Pro', sans-serif;
    }
    .stApp { background-color: #f8f9fa; }
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
        {"ID": "JMI-001", "Name": "សិស្សគំរូ មត្តេយ្យ", "Level": "មត្តេយ្យ", "Enroll_Date": "2026-03-25", "Status": "Active", "Skills": []},
        {"ID": "JMI-002", "Name": "សិស្សគំរូ បឋម", "Level": "បឋម", "Enroll_Date": "2026-03-25", "Status": "Active", "Skills": []},
        {"ID": "JMI-003", "Name": "សិស្សគំរូ អនុវិទ្យាល័យ", "Level": "អនុវិទ្យាល័យ", "Enroll_Date": "2026-03-25", "Status": "Active", "Skills": []},
        {"ID": "JMI-004", "Name": "សិស្សគំរូ វិទ្យាល័យ", "Level": "វិទ្យាល័យ", "Enroll_Date": "2026-03-25", "Status": "Active", "Skills": []},
    ])

if 'filter_level' not in st.session_state:
    st.session_state.filter_level = "ទាំងអស់"

# --- ៤. របារចំហៀង (Sidebar) ---
st.sidebar.markdown("<h2 style='text-align: center; color: #001f3f;'>JMI EXECUTIVE</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<center><h1 style='font-size:60px;'>🏥</h1></center>", unsafe_allow_html=True)
st.sidebar.markdown("---")

pwd = st.sidebar.text_input("Director's Key", type="password", placeholder="Enter Password")

# --- ៥. កម្មវិធីចម្បង (Main Logic) ---
if pwd == "JMI2026":
    st.sidebar.success("Welcome, Dr. CHAN Sokhoeurn")
    
    menu = st.sidebar.radio("STRATEGIC MODULES", ["📊 Dashboard", "🎓 Enrollment", "🏅 Skill Passport", "📜 Certification"])

    # មុខងារកំណត់មេរៀនស្វ័យប្រវត្តិតាមកម្រិត
    def get_lessons(level):
        if level in ["មត្តេយ្យ", "បឋម"]:
            return [f"មេរៀនទី {i}" for i in range(1, 10)] # ៩ មេរៀន
        else:
            return [f"មេរៀនទី {i}" for i in range(1, 13)] # ១២ មេរៀន

    # --- ៥.១ Dashboard ---
    if menu == "📊 Dashboard":
        st.title("🏥 JMI Strategic Command Center")
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Scholars", len(st.session_state.db))
        c2.metric("Status", "Operational")
        c3.metric("Year", "2026")
        
        st.markdown("### 🔍 ច្រោះទិន្នន័យតាមកម្រិតសិក្សា (Quick Filter)")
        
        b0, b1, b2, b3, b4 = st.columns(5)
        if b0.button("🌐 ទាំងអស់", use_container_width=True): st.session_state.filter_level = "ទាំងអស់"
        if b1.button("🧸 មត្តេយ្យ", use_container_width=True): st.session_state.filter_level = "មត្តេយ្យ"
        if b2.button("🎒 បឋម", use_container_width=True): st.session_state.filter_level = "បឋម"
        if b3.button("📚 អនុវិទ្យាល័យ", use_container_width=True): st.session_state.filter_level = "អនុវិទ្យាល័យ"
        if b4.button("🎓 វិទ្យាល័យ", use_container_width=True): st.session_state.filter_level = "វិទ្យាល័យ"

        if st.session_state.filter_level == "ទាំងអស់":
            display_db = st.session_state.db
        else:
            display_db = st.session_state.db[st.session_state.db['Level'] == st.session_state.filter_level]

        st.markdown(f"**កំពុងបង្ហាញ៖ សិស្សកម្រិត [{st.session_state.filter_level}]**")
        st.dataframe(display_db.drop(columns=['Skills']), use_container_width=True)

    # --- ៥.២ Enrollment (ចុះឈ្មោះ) ---
    elif menu == "🎓 Enrollment":
        st.header("Register New Scholar")
        with st.form("enroll_form", clear_on_submit=True):
            name = st.text_input("Full Name (ឈ្មោះពេញ)")
            sid = st.text_input("Scholar ID (លេខសម្គាល់)")
            level = st.selectbox("Academic Level (កម្រិតសិក្សា)", ["មត្តេយ្យ", "បឋម", "អនុវិទ្យាល័យ", "វិទ្យាល័យ"])
            
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

    # --- ៥.៣ Skill Passport ---
    elif menu == "🏅 Skill Passport":
        st.header("🏅 Skill Mastery Passport")
        
        sel_level = st.selectbox("Select Level (ជ្រើសរើសកម្រិតសិក្សា):", ["ទាំងអស់", "មត្តេយ្យ", "បឋម", "អនុវិទ្យាល័យ", "វិទ្យាល័យ"], key="passport_level_sel")
        
        if sel_level == "ទាំងអស់":
            filtered_students = st.session_state.db
        else:
            filtered_students = st.session_state.db[st.session_state.db['Level'] == sel_level]
            
        if filtered_students.empty:
            st.warning(f"មិនទាន់មានសិស្សនៅក្នុងកម្រិត '{sel_level}' ទេ។")
        else:
            student_list = filtered_students.apply(lambda x: f"{x['Name']} ({x['Level']})", axis=1).tolist()
            sel_student_str = st.selectbox("Select Student (ជ្រើសរើសសិស្ស):", student_list, key="passport_student_sel")
            
            selected_idx = filtered_students.index[student_list.index(sel_student_str)]
            
            student_name = st.session_state.db.at[selected_idx, 'Name']
            student_level = st.session_state.db.at[selected_idx, 'Level']
            available_skills = get_lessons(student_level)
            current_skills = st.session_state.db.at[selected_idx, 'Skills']
            
            st.markdown(f"### ស្ថានភាពសិក្សារបស់៖ {student_name}")
            st.write(f"កម្រិតសិក្សា៖ **{student_level}** (ត្រូវការរៀនចំនួន {len(available_skills)} មេរៀន)")
            
            completed_count = len([s for s in current_skills if s in available_skills])
            total_count = len(available_skills)
            progress = completed_count / total_count if total_count > 0 else 0
            
            st.progress(progress)
            st.write(f"បានបញ្ចប់៖ {completed_count} / {total_count} មេរៀន")
            st.markdown("---")
            
            new_selection = []
            col1, col2 = st.columns(2)
            for i, skill in enumerate(available_skills):
                with (col1 if i % 2 == 0 else col2):
                    if st.checkbox(skill, value=(skill in current_skills), key=f"{selected_idx}_{skill}"):
                        new_selection.append(skill)
            
            if st.button("💾 Save Progress"):
                st.session_state.db.at[selected_idx, 'Skills'] = new_selection
                st.success(f"Updated skills for {student_name}!")
                st.rerun()

    # --- ៥.៤ Certification (កែសម្រួលឱ្យដូច Skill Passport) ---
    elif menu == "📜 Certification":
        st.header("Certification Generator")
        
        # បន្ថែមការជ្រើសរើសកម្រិត ដើម្បីចម្រោះឈ្មោះសិស្ស
        sel_level_cert = st.selectbox("Select Level (ជ្រើសរើសកម្រិតសិក្សា):", ["ទាំងអស់", "មត្តេយ្យ", "បឋម", "អនុវិទ្យាល័យ", "វិទ្យាល័យ"], key="cert_level_sel")
        
        if sel_level_cert == "ទាំងអស់":
            filtered_students_cert = st.session_state.db
        else:
            filtered_students_cert = st.session_state.db[st.session_state.db['Level'] == sel_level_cert]
            
        if filtered_students_cert.empty:
            st.warning(f"មិនទាន់មានសិស្សនៅក្នុងកម្រិត '{sel_level_cert}' ទេ។")
        else:
            # បង្ហាញឈ្មោះសិស្ស ភ្ជាប់ជាមួយកម្រិត
            student_list_cert = filtered_students_cert.apply(lambda x: f"{x['Name']} ({x['Level']})", axis=1).tolist()
            sel_student_str_cert = st.selectbox("Select Recipient (ជ្រើសរើសសិស្ស):", student_list_cert, key="cert_student_sel")
            
            # ទាញយក index ពិតប្រាកដក្នុង Database
            selected_idx_cert = filtered_students_cert.index[student_list_cert.index(sel_student_str_cert)]
            s_info = st.session_state.db.loc[selected_idx_cert]
            
            if st.button("🌟 GENERATE CERTIFICATE"):
                if len(s_info['Skills']) == 0:
                    st.warning("Scholar នេះមិនទាន់ទទួលបាន Skill ណាមួយនៅឡើយទេ។")
                else:
                    st.balloons()
                    stars_html = "".join(['<span class="star-gold">★</span>' for _ in range(len(s_info['Skills']))])
                    
                    certificate_html = f"""
                    <div class="cert-paper">
                        <div class="cert-border">
                            <p style="letter-spacing: 5px; color: #555; font-size: 12px; margin-bottom:10px;">JUNIOR MEDICAL INSTITUTE</p>
                            <h1 class="cert-header">CERTIFICATE</h1>
                            <div style="margin: 10px 0;">{stars_html}</div>
                            <p class="cert-text" style="font-style: italic;">This award is proudly presented to</p>
                            <h2 class="student-name">{s_info['Name']}</h2>
                            <p class="cert-text">for successfully completing <b>{len(s_info['Skills'])} lessons</b><br>in <b>Medical Foundation Pathway</b> ({s_info['Level']})</p>
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
else:
    st.title("🏥 JMI Strategic Command Portal")
    st.info("🔒 សូមបញ្ចូល Password 'JMI2026' ដើម្បីចាប់ផ្ដើម។")
