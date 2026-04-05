import streamlit as st
import pandas as pd
from datetime import datetime

# --- ១. ការកំណត់ទម្រង់កម្មវិធី ---
st.set_page_config(
    page_title="JMI | Strategic Management Portal",
    page_icon="🏥",
    layout="wide"
)

# --- ២. ការរចនា Style (Navy Blue & Gold - Fixed Visibility) ---
style_block = """
<link href="https://fonts.googleapis.com/css2?family=Great+Vibes&family=Cinzel:wght@700&family=DM+Serif+Display&family=Kantumruy+Pro:wght@400;700&display=swap" rel="stylesheet">
<style>
    /* កំណត់ពណ៌ផ្ទៃខាងក្រោយ និងហ្វុន */
    html, body, [class*="css"], .stMarkdown {
        font-family: 'Kantumruy Pro', sans-serif;
        color: #ffffff;
    }
    .stApp { background-color: #001f3f; }
    
    /* កែសម្រួលអក្សរមេរៀន និង Checkbox ឱ្យមើលឃើញច្បាស់ (ពណ៌មាស) */
    .stCheckbox label p {
        color: #D4AF37 !important;
        font-weight: bold !important;
        font-size: 18px !important;
    }
    
    /* បន្ថែមស៊ុមជុំវិញ Checkbox នីមួយៗ */
    div[data-testid="stCheckbox"] {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid #D4AF37;
        padding: 5px 10px;
        border-radius: 5px;
        margin-bottom: 5px;
    }

    h1, h2, h3 { color: #D4AF37 !important; }
    
    .metric-card {
        background-color: #fcf3cf;
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #D4AF37;
        text-align: center;
    }
    .metric-title { font-size: 14px; color: #001f3f; text-transform: uppercase; font-weight: bold;}
    .metric-value { font-size: 32px; font-weight: bold; color: #001f3f; margin: 10px 0; }
    
    .stButton>button {
        background-color: #D4AF37 !important;
        color: #001f3f !important;
        font-weight: bold !important;
        border-radius: 8px !important;
    }

    /* តារាងទិន្នន័យ (Data Editor) */
    [data-testid="stDataFrame"] {
        background-color: white;
        border-radius: 10px;
    }
</style>
"""
st.markdown(style_block, unsafe_allow_html=True)

# --- ៣. ការគ្រប់គ្រងទិន្នន័យ ---
if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame([
        {"ID": "JMI-001", "Name": "CHAN SOKHOEURN", "Level": "វិទ្យាល័យ", "Enroll_Date": "2026-04-05", "Status": "Active", "Skills": []}
    ])

# --- ៤. Sidebar ---
st.sidebar.markdown("<h2 style='text-align: center;'>JMI EXECUTIVE</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<center><h1 style='font-size:60px; color: #D4AF37;'>🛡️</h1></center>", unsafe_allow_html=True)
pwd = st.sidebar.text_input("Director's Key", type="password")

if pwd == "JMI2026":
    menu = st.sidebar.radio("MODULES", ["📊 Dashboard", "🎓 Enrollment", "🏅 Skill Passport", "📜 Certification"])

    def get_lessons(level):
        return [f"មេរៀនទី {i}" for i in range(1, 10)] if level in ["មត្តេយ្យ", "បឋម"] else [f"មេរៀនទី {i}" for i in range(1, 13)]

    # --- ៥.១ Dashboard ---
    if menu == "📊 Dashboard":
        st.title("🏥 JMI Command Center")
        c1, c2, c3 = st.columns(3)
        c1.markdown(f'<div class="metric-card"><div class="metric-title">Scholars</div><div class="metric-value">{len(st.session_state.db)}</div></div>', unsafe_allow_html=True)
        c2.markdown(f'<div class="metric-card"><div class="metric-title">System</div><div class="metric-value">Online</div></div>', unsafe_allow_html=True)
        c3.markdown(f'<div class="metric-card"><div class="metric-title">Year</div><div class="metric-value">2026</div></div>', unsafe_allow_html=True)
        
        st.markdown("### ⚙️ Scholar Database")
        cols = ["ID", "Name", "Level", "Enroll_Date", "Status"]
        edited = st.data_editor(st.session_state.db[cols], num_rows="dynamic", use_container_width=True)
        
        if st.button("💾 Save All Changes"):
            skills_map = dict(zip(st.session_state.db["ID"], st.session_state.db["Skills"]))
            new_skills = [skills_map.get(s_id, []) for s_id in edited["ID"]]
            edited["Skills"] = new_skills
            st.session_state.db = edited
            st.success("Database Updated!")

    # --- ៥.២ Enrollment ---
    elif menu == "🎓 Enrollment":
        st.header("Register New Scholar")
        with st.form("reg_form"):
            n = st.text_input("Scholar Name")
            i = st.text_input("Scholar ID")
            l = st.selectbox("Academic Level", ["មត្តេយ្យ", "បឋម", "អនុវិទ្យាល័យ", "វិទ្យាល័យ"])
            if st.form_submit_button("REGISTER NOW"):
                new_data = pd.DataFrame([{"ID": i, "Name": n.upper(), "Level": l, "Enroll_Date": datetime.now().strftime("%Y-%m-%d"), "Status": "Active", "Skills": []}])
                st.session_state.db = pd.concat([st.session_state.db, new_data], ignore_index=True)
                st.success(f"Registered {n}!")

    # --- ៥.៣ Skill Passport (កែសម្រួលឱ្យមើលឃើញច្បាស់) ---
    elif menu == "🏅 Skill Passport":
        st.header("🏅 Skill Mastery Passport")
        names = st.session_state.db["Name"].tolist()
        if names:
            sel_name = st.selectbox("Select Student", names)
            idx = st.session_state.db[st.session_state.db["Name"] == sel_name].index[0]
            s_level = st.session_state.db.at[idx, "Level"]
            lessons = get_lessons(s_level)
            current_skills = st.session_state.db.at[idx, "Skills"]
            
            st.markdown(f"### Lessons for Level: <span style='color:#D4AF37'>{s_level}</span>", unsafe_allow_html=True)
            
            # បង្ហាញមេរៀនជា ២ កូឡោន
            new_selection = []
            col1, col2 = st.columns(2)
            for count, m in enumerate(lessons):
                target_col = col1 if count % 2 == 0 else col2
                with target_col:
                    if st.checkbox(m, value=(m in current_skills), key=f"chk_{idx}_{m}"):
                        new_selection.append(m)
            
            if st.button("💾 Update Scholar Skills"):
                st.session_state.db.at[idx, "Skills"] = new_selection
                st.success("Progress Saved Successfully!")

    # --- ៥.៤ Certification ---
    elif menu == "📜 Certification":
        st.header("Certification Hub")
        names = st.session_state.db["Name"].tolist()
        if names:
            sel_name = st.selectbox("Recipient Name", names)
            info = st.session_state.db[st.session_state.db["Name"] == sel_name].iloc[0]
            if st.button("GENERATE"):
                st.balloons()
                st.markdown(f"""
                <div style="background:white; padding:40px; border:10px solid #D4AF37; text-align:center; color:#001f3f;">
                    <h1>JUNIOR MEDICAL INSTITUTE</h1>
                    <p>Certificate of Completion</p>
                    <h2 style="font-family:'Great Vibes'; font-size:50px; color:#D4AF37;">{info['Name']}</h2>
                    <p>Successfully mastered the curriculum for <b>{info['Level']}</b></p>
                    <br><br>
                    <p>__________________________<br>Dr. Chan Sokhoeurn</p>
                </div>
                """, unsafe_allow_html=True)
else:
    st.title("🏥 JMI Strategic Portal")
    st.warning("🔒 Enter Director's Key to Access.")
