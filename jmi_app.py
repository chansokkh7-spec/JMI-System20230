import streamlit as st
import pandas as pd
from datetime import datetime

# --- ១. ការកំណត់ទម្រង់កម្មវិធី ---
st.set_page_config(
    page_title="JMI | Strategic Management Portal",
    page_icon="🏥",
    layout="wide"
)

# --- ២. ការរចនា Style (Premium Blue & Gold Theme) ---
# ខ្ញុំបានកែប្រែពណ៌ Background ពណ៌អក្សរ និងប៊ូតុងឱ្យទៅជា ខៀវចាស់ និង មាស
style_block = """
<link href="https://fonts.googleapis.com/css2?family=Great+Vibes&family=Cinzel:wght@700&family=DM+Serif+Display&family=Kantumruy+Pro:wght@400;700&display=swap" rel="stylesheet">
<style>
    /* កំណត់ហ្វុនអក្សរទូទៅ */
    html, body, [class*="css"], .stMarkdown {
        font-family: 'Kantumruy Pro', sans-serif;
        color: #ffffff; /* អក្សរពណ៌សលើ Background ខ្មៅ/ខៀវ */
    }
    
    /* ១. ផ្ទៃ Background ដើម (Main App Background) -> ពណ៌ខៀវចាស់ */
    .stApp { 
        background-color: #001f3f; /* Navy Blue */
    }
    
    /* ២. ពណ៌អក្សរចំណងជើងធំៗ -> ពណ៌មាស */
    h1, h2, h3, .stMetric label {
        color: #D4AF37 !important; /* Gold */
    }
    
    /* ពណ៌ផ្កាយមាស */
    .star-gold { color: #D4AF37; font-size: 25px; margin-right: 3px; }
    
    /* ៣. ការរចនា Sidebar (របារចំហៀង) -> ខៀវរឹតតែចាស់ និងអក្សរមាស/ស */
    [data-testid="stSidebar"] {
        background-color: #001529; /* Darker Navy */
    }
    [data-testid="stSidebar"] * {
        color: #ffffff !important;
    }
    /* ពណ៌មាសសម្រាប់ចំណងជើង Sidebar */
    [data-testid="stSidebar"] h2 {
        color: #D4AF37 !important;
    }
    /* កែពណ៌ Radio Button ក្នុង Sidebar */
    div[data-testid="stMarkdownContainer"] p {
        color: #ffffff;
    }

    /* ៤. Dashboard KPI Cards -> ផ្ទៃពណ៌មាសខ្ចី អក្សរខៀវចាស់ */
    .metric-card {
        background-color: #fcf3cf; /* Light Gold/Yellow */
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(212, 175, 55, 0.3); /* Gold Shadow */
        border-left: 5px solid #D4AF37; /* Gold Border */
        text-align: center;
        transition: transform 0.2s;
    }
    .metric-card:hover {
        transform: translateY(-5px);
    }
    .metric-title { font-size: 14px; color: #001f3f; text-transform: uppercase; letter-spacing: 1px; font-weight: bold;}
    .metric-value { font-size: 32px; font-weight: bold; color: #001f3f; margin: 10px 0; }
    
    /* ៥. កែពណ៌ប៊ូតុង (Buttons) -> ផ្ទៃមាស អក្សរខៀវ */
    .stButton>button {
        background-color: #D4AF37 !important; /* Gold Background */
        color: #001f3f !important; /* Navy Text */
        border: none !important;
        font-weight: bold !important;
        border-radius: 8px !important;
    }
    .stButton>button:hover {
        background-color: #bfa030 !important; /* Darker Gold on hover */
        color: #ffffff !important;
    }
    
    /* ៦. កែពណ៌តារាង (Data Editor/Table) ឱ្យមើលឃើញច្បាស់ */
    .stDataFrame, div[data-testid="stTable"] {
        background-color: #ffffff; /* ផ្ទៃតារាងពណ៌ស ដើម្បីឱ្យងាយស្រួលអាន */
        border-radius: 8px;
        padding: 5px;
    }
    /* ពណ៌អក្សរក្នុងតារាង -> ពណ៌ខ្មៅ/ខៀវចាស់ */
    .stDataFrame * {
        color: #000000 !important;
    }
    
    /* ៧. Premium Certificate Style (រក្សាទុកសខ្មៅដើម្បីភាពថ្លៃថ្នូរ ប៉ុន្តែថែមស៊ុមមាស) */
    .cert-paper { 
        background-color: white; 
        border: 12px solid #D4AF37; /* Gold Outer Border */
        padding: 10px; 
        box-shadow: 0 25px 50px rgba(212, 175, 55, 0.5); 
        max-width: 800px; 
        margin: 30px auto; 
    }
    .cert-border { border: 4px double #001f3f; /* Navy Inner Border */ padding: 40px; text-align: center; }
    .cert-header { font-family: 'Cinzel', serif; color: #001f3f; font-size: 40px; margin: 0; letter-spacing: 5px; }
    .student-name { font-family: 'Great Vibes', cursive; font-size: 55px; color: #D4AF37; margin: 15px 0; font-weight: normal; }
    .cert-text { font-family: 'DM Serif Display', serif; font-size: 18px; color: #333; line-height: 1.6; }
    .signature { font-family: 'Great Vibes', cursive; font-size: 30px; color: #001f3f; margin-bottom: -10px; }
    .sig-box { border-top: 1px solid #333; width: 180px; margin: auto; padding-top: 5px; font-family: serif; font-size: 13px; color: #333; }
    
    /* កែពណ៌ Progress Bar -> ពណ៌មាស */
    .stProgress > div > div > div > div {
        background-color: #D4AF37 !important;
    }
    
    /* កែពណ៌ Input Fields (Text input, Selectbox) */
    .stTextInput>div>div>input, .stSelectbox>div>div>div {
        background-color: #ffffff !important;
        color: #000000 !important;
    }
</style>
"""
st.markdown(style_block, unsafe_allow_html=True)

# --- ៣. ការគ្រប់គ្រងទិន្នន័យ (Session State) ---
if 'db' not in st.session_state:
    # បង្កើតទិន្នន័យគំរូសិស្សពិតប្រាកដសម្រាប់ JMI
    st.session_state.db = pd.DataFrame([
        {"ID": "JMI-26-001", "Name": "CHAN SOKHOEURN", "Level": "វិទ្យាល័យ", "Enroll_Date": "2026-01-10", "Status": "Active", "Skills": ["មេរៀនទី 1", "មេរៀនទី 2"]},
        {"ID": "JMI-26-002", "Name": "DARA VICHET", "Level": "អនុវិទ្យាល័យ", "Enroll_Date": "2026-02-15", "Status": "Active", "Skills": ["មេរៀនទី 1"]},
        {"ID": "JMI-26-003", "Name": "VITHA VICHIRA", "Level": "បឋម", "Enroll_Date": "2026-03-01", "Status": "Inactive", "Skills": []},
        {"ID": "JMI-26-004", "Name": "SIDA RATA", "Level": "មត្តេយ្យ", "Enroll_Date": "2026-03-20", "Status": "Active", "Skills": []},
    ])

# --- ៤. របារចំហៀង (Sidebar) ---
st.sidebar.markdown("<h2 style='text-align: center;'>JMI EXECUTIVE</h2>", unsafe_allow_html=True)
# ប្តូរពណ៌ Logo Shield ឱ្យទៅជាពណ៌មាស
st.sidebar.markdown("<center><h1 style='font-size:60px; color: #D4AF37;'>🛡️</h1></center>", unsafe_allow_html=True)
st.sidebar.markdown("---")

pwd = st.sidebar.text_input("Director's Key", type="password", placeholder="Enter Password")

# --- ៥. កម្មវិធីចម្បង (Main Logic) ---
if pwd == "JMI2026":
    st.sidebar.success("Welcome, Dr. CHAN Sokhoeurn")
    
    menu = st.sidebar.radio("STRATEGIC MODULES", ["📊 Dashboard", "🎓 Enrollment", "🏅 Skill Passport", "📜 Certification"])

    # មុខងារកំណត់មេរៀនស្វ័យប្រវត្តិតាមកម្រិត
    def get_lessons(level):
        if level in ["មត្តេយ្យ", "បឋម"]:
            return [f"មេរៀនទី {i}" for i in range(1, 10)]
        else:
            return [f"មេរៀនទី {i}" for i in range(1, 13)]

    # --- ៥.១ Dashboard (Blue & Gold CRUD) ---
    if menu == "📊 Dashboard":
        st.title("🏥 JMI Strategic Command Center")
        st.markdown("គ្រប់គ្រងស្ថិតិ និងទិន្នន័យសិស្សជាសកល")
        
        # Dashboard KPI Cards (ពណ៌មាសខ្ចី អក្សរខៀវ)
        total_scholars = len(st.session_state.db)
        active_scholars = len(st.session_state.db[st.session_state.db['Status'] == 'Active'])
        
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            st.markdown(f'<div class="metric-card"><div class="metric-title">👥 Total Scholars</div><div class="metric-value">{total_scholars}</div></div>', unsafe_allow_html=True)
        with col_m2:
            st.markdown(f'<div class="metric-card"><div class="metric-title">✅ Active Students</div><div class="metric-value">{active_scholars}</div></div>', unsafe_allow_html=True)
        with col_m3:
            st.markdown(f'<div class="metric-card"><div class="metric-title">📅 Current Year</div><div class="metric-value">2026</div></div>', unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Analytics Chart (ពណ៌មាស)
        st.markdown("### 📊 ក្រាហ្វិកស្ថិតិសិស្សតាមកម្រិត (Analytics)")
        if not st.session_state.db.empty:
            level_counts = st.session_state.db['Level'].value_counts()
            st.bar_chart(level_counts, color="#D4AF37") # Gold Chart
        else:
            st.info("មិនទាន់មានទិន្នន័យសម្រាប់បង្ហាញក្រាហ្វិកទេ។")

        st.markdown("---")
        
        # CRUD Section (ពណ៌សំបូរមាស)
        st.markdown("### ⚙️ Data Management Hub (រក្សាទុក កែ និងលុប)")
        st.info("💡 លោកអ្នកអាចចុចលើប្រអប់ដើម្បីកែប្រែ ឬចុចលើជួរដេក រួចចុចគ្រាប់ចុច `Delete` លើ Keyboard ដើម្បីលុប។")
        
        cols_to_edit = ["ID", "Name", "Level", "Enroll_Date", "Status"]
        df_to_edit = st.session_state.db[cols_to_edit]
        
        # Data Editor (ផ្ទៃតារាងពណ៌ស ដើម្បីឱ្យងាយស្រួលមើលលើ Background ខៀវ)
        edited_data = st.data_editor(
            df_to_edit, 
            num_rows="dynamic",
            use_container_width=True,
            column_config={
                "Status": st.column_config.SelectboxColumn(
                    "Status",
                    options=["Active", "Inactive", "Graduated"],
                    required=True
                ),
                "Level": st.column_config.SelectboxColumn(
                    "Level",
                    options=["មត្តេយ្យ", "បឋម", "អនុវិទ្យាល័យ", "វិទ្យាល័យ"],
                    required=True
                )
            }
        )
        
        # ប៊ូតុងរក្សាទុក (ពណ៌មាស)
        if st.button("💾 រក្សាទុកការផ្លាស់ប្តូរ (Save Changes)", type="primary"):
            skills_map = dict(zip(st.session_state.db["ID"], st.session_state.db["Skills"]))
            new_skills = []
            for s_id in edited_data["ID"]:
                new_skills.append(skills_map.get(s_id, []))
            edited_data["Skills"] = new_skills
            st.session_state.db = edited_data
            st.success("🎉 ទិន្នន័យត្រូវបានរក្សាទុកដោយជោគជ័យ!")
            st.rerun()

    # --- ៥.២ Enrollment ---
    elif menu == "🎓 Enrollment":
        st.header("Register New Scholar")
        with st.form("enroll_form", clear_on_submit=True):
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                name = st.text_input("Full Name (ឈ្មោះពេញ)")
                sid = st.text_input("Scholar ID (លេខសម្គាល់)")
            with col_f2:
                level = st.selectbox("Academic Level (កម្រិតសិក្សា)", ["មត្តេយ្យ", "បឋម", "អនុវិទ្យាល័យ", "វិទ្យាល័យ"])
            
            # ប៊ូតុងចុះឈ្មោះ (ពណ៌មាស)
            if st.form_submit_button("✅ CONFIRM ENROLLMENT"):
                if name and sid:
                    new_entry = pd.DataFrame([{
                        "ID": sid, 
                        "Name": name.upper(), # ប្តូរជាអក្សរធំសកល
                        "Level": level, 
                        "Enroll_Date": datetime.now().strftime("%Y-%m-%d"), 
                        "Status": "Active", 
                        "Skills": []
                    }])
                    st.session_state.db = pd.concat([st.session_state.db, new_entry], ignore_index=True)
                    st.success(f"Scholar '{name}' has been added successfully.")
                    st.rerun()
                else:
                    st.error("សូមបំពេញព័ត៌មានទាំងឈ្មោះ និងលេខសម្គាល់!")

    # --- ៥.៣ Skill Passport ---
    elif menu == "🏅 Skill Passport":
        st.header("🏅 Skill Mastery Passport")
        
        # Input fields នឹងមានផ្ទៃពណ៌ស អក្សរខ្មៅ
        sel_level = st.selectbox("Select Level:", ["ទាំងអស់", "មត្តេយ្យ", "បឋម", "អនុវិទ្យាល័យ", "វិទ្យាល័យ"], key="passport_level_sel")
        
        if sel_level == "ទាំងអស់":
            filtered_students = st.session_state.db
        else:
            filtered_students = st.session_state.db[st.session_state.db['Level'] == sel_level]
            
        if filtered_students.empty:
            st.warning(f"មិនទាន់មានសិស្សនៅក្នុងកម្រិត '{sel_level}' ទេ។")
        else:
            student_list = filtered_students.apply(lambda x: f"{x['Name']} ({x['Level']})", axis=1).tolist()
            sel_student_str = st.selectbox("Select Student:", student_list, key="passport_student_sel")
            
            selected_idx = filtered_students.index[student_list.index(sel_student_str)]
            
            student_name = st.session_state.db.at[selected_idx, 'Name']
            student_level = st.session_state.db.at[selected_idx, 'Level']
            available_skills = get_lessons(student_level)
            current_skills = st.session_state.db.at[selected_idx, 'Skills']
            
            st.markdown(f"### ស្ថានភាពសិក្សារបស់៖ <span style='color: #D4AF37;'>{student_name}</span>", unsafe_allow_html=True)
            
            completed_count = len([s for s in current_skills if s in available_skills])
            total_count = len(available_skills)
            progress = completed_count / total_count if total_count > 0 else 0
            
            # Progress Bar ពណ៌មាស
            st.progress(progress)
            st.write(f"បានបញ្ចប់៖ {completed_count} / {total_count} មេរៀន")
            st.markdown("---")
            
            new_selection = []
            col1, col2 = st.columns(2)
            for i, skill in enumerate(available_skills):
                with (col1 if i % 2 == 0 else col2):
                    # Checkbox អក្សរពណ៌ស
                    if st.checkbox(skill, value=(skill in current_skills), key=f"{selected_idx}_{skill}"):
                        new_selection.append(skill)
            
            # ប៊ូតុងរក្សាទុក (ពណ៌មាស)
            if st.button("💾 Save Progress"):
                st.session_state.db.at[selected_idx, 'Skills'] = new_selection
                st.success(f"Updated skills for {student_name}!")
                st.rerun()

    # --- ៥.៤ Certification (Blue & Gold Certificate) ---
    elif menu == "📜 Certification":
        st.header("Certification Generator")
        
        sel_level_cert = st.selectbox("Select Level:", ["ទាំងអស់", "មត្តេយ្យ", "បឋម", "អនុវិទ្យាល័យ", "វិទ្យាល័យ"], key="cert_level_sel")
        
        if sel_level_cert == "ទាំងអស់":
            filtered_students_cert = st.session_state.db
        else:
            filtered_students_cert = st.session_state.db[st.session_state.db['Level'] == sel_level_cert]
            
        if filtered_students_cert.empty:
            st.warning(f"មិនទាន់មានសិស្សនៅក្នុងកម្រិត '{sel_level_cert}' ទេ។")
        else:
            student_list_cert = filtered_students_cert.apply(lambda x: f"{x['Name']} ({x['Level']})", axis=1).tolist()
            sel_student_str_cert = st.selectbox("Select Recipient:", student_list_cert, key="cert_student_sel")
            
            selected_idx_cert = filtered_students_cert.index[student_list_cert.index(sel_student_str_cert)]
            s_info = st.session_state.db.loc[selected_idx_cert]
            
            # ប៊ូតុងបង្កើត (ពណ៌មាស)
            if st.button("🌟 GENERATE CERTIFICATE"):
                if len(s_info['Skills']) == 0:
                    st.warning("Scholar នេះមិនទាន់ទទួលបាន Skill ណាមួយនៅឡើយទេ។")
                else:
                    st.balloons()
                    stars_html = "".join(['<span class="star-gold">★</span>' for _ in range(len(s_info['Skills']))])
                    
                    # វិញ្ញាបនបត្រដែលមានស៊ុមពណ៌មាស និង Navy Blue
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
                                    <p style="font-size:14px; margin-bottom:5px; color:#333;">{datetime.now().strftime("%d %B %Y")}</p>
                                    <div class="sig-box">DATE</div>
                                }
                                <div style="text-align:center;">
                                    <p class="signature">Dr. Chan Sokhoeurn</p>
                                    <div class="sig-box">ACADEMIC DIRECTOR</div>
                                }
                            }
                        }
                    }
                    """
                    st.markdown(certificate_html, unsafe_allow_html=True)
# --- ៦. ផ្ទាំង Lock ---
else:
    st.title("🏥 JMI Strategic Command Portal")
    # កែពណ៌អក្សរក្នុង Info box
    st.markdown("""
        <div style="background-color: #fcf3cf; color: #001f3f; padding: 15px; border-radius: 8px; border-left: 5px solid #D4AF37;">
            🔒 សូមបញ្ចូល Password 'JMI2026' នៅរបារចំហៀងខាងឆ្វេង ដើម្បីបើកដំណើរការប្រព័ន្ធ។
        </div>
    """, unsafe_allow_html=True)
