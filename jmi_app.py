import streamlit as st
import pandas as pd
from datetime import datetime

# --- ១. ការកំណត់ទម្រង់កម្មវិធី ---
st.set_page_config(
    page_title="JMI | Strategic Management Portal",
    page_icon="🏥",
    layout="wide"
)

# --- ២. ការរចនា Style (Navy Blue & Gold) ---
style_block = """
<link href="https://fonts.googleapis.com/css2?family=Great+Vibes&family=Cinzel:wght@700&family=DM+Serif+Display&family=Kantumruy+Pro:wght@400;700&display=swap" rel="stylesheet">
<style>
    html, body, [class*="css"], .stMarkdown {
        font-family: 'Kantumruy Pro', sans-serif;
        color: #ffffff;
    }
    .stApp { background-color: #001f3f; }
    
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
        width: 100%;
    }
    
    /* កែសម្រួលពណ៌អក្សរក្នុងតារាងឱ្យខ្មៅងាយមើល */
    [data-testid="stTable"] td, [data-testid="stDataFrame"] td { color: black !important; }
    
    .cert-paper { 
        background-color: white; 
        border: 12px solid #D4AF37; 
        padding: 10px; 
        max-width: 800px; 
        margin: 30px auto; 
        color: #000;
    }
    .cert-border { border: 4px double #001f3f; padding: 40px; text-align: center; }
    .student-name { font-family: 'Great Vibes', cursive; font-size: 55px; color: #D4AF37; margin: 15px 0; }
</style>
"""
st.markdown(style_block, unsafe_allow_html=True)

# --- ៣. ការគ្រប់គ្រងទិន្នន័យ ---
if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame([
        {"ID": "JMI-26-001", "Name": "CHAN SOKHOEURN", "Level": "វិទ្យាល័យ", "Enroll_Date": "2026-01-10", "Status": "Active", "Skills": []}
    ])

# --- ៤. Sidebar ---
st.sidebar.markdown("<h2 style='text-align: center;'>JMI EXECUTIVE</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<center><h1 style='font-size:60px; color: #D4AF37;'>🛡️</h1></center>", unsafe_allow_html=True)
pwd = st.sidebar.text_input("Director's Key", type="password")

if pwd == "JMI2026":
    menu = st.sidebar.radio("MENU", ["📊 Dashboard", "🎓 Enrollment", "🏅 Skill Passport", "📜 Certification"])

    def get_lessons(level):
        return [f"មេរៀនទី {i}" for i in range(1, 10)] if level in ["មត្តេយ្យ", "បឋម"] else [f"មេរៀនទី {i}" for i in range(1, 13)]

    # --- ៥.១ Dashboard ---
    if menu == "📊 Dashboard":
        st.title("🏥 Strategic Command Center")
        
        c1, c2, c3 = st.columns(3)
        c1.markdown(f'<div class="metric-card"><div class="metric-title">Total</div><div class="metric-value">{len(st.session_state.db)}</div></div>', unsafe_allow_html=True)
        c2.markdown(f'<div class="metric-card"><div class="metric-title">Year</div><div class="metric-value">2026</div></div>', unsafe_allow_html=True)
        c3.markdown(f'<div class="metric-card"><div class="metric-title">Status</div><div class="metric-value">Live</div></div>', unsafe_allow_html=True)
        
        st.markdown("### ⚙️ Data Editor")
        cols = ["ID", "Name", "Level", "Enroll_Date", "Status"]
        edited = st.data_editor(st.session_state.db[cols], num_rows="dynamic", use_container_width=True)
        
        if st.button("💾 SAVE CHANGES"):
            skills_map = dict(zip(st.session_state.db["ID"], st.session_state.db["Skills"]))
            new_skills = [skills_map.get(s_id, []) for s_id in edited["ID"]]
            edited["Skills"] = new_skills
            st.session_state.db = edited
            st.success("Saved!")
            st.rerun()

    # --- ៥.២ Enrollment ---
    elif menu == "🎓 Enrollment":
        st.header("New Registration")
        with st.form("reg"):
            n = st.text_input("Name")
            i = st.text_input("ID")
            l = st.selectbox("Level", ["មត្តេយ្យ", "បឋម", "អនុវិទ្យាល័យ", "វិទ្យាល័យ"])
            if st.form_submit_button("REGISTER"):
                new_row = pd.DataFrame([{"ID": i, "Name": n.upper(), "Level": l, "Enroll_Date": "2026-04-05", "Status": "Active", "Skills": []}])
                st.session_state.db = pd.concat([st.session_state.db, new_row], ignore_index=True)
                st.success("Added!")

    # --- ៥.៣ Skill Passport ---
    elif menu == "🏅 Skill Passport":
        st.header("🏅 Skill Progress")
        s_list = st.session_state.db["Name"].tolist()
        if s_list:
            sel = st.selectbox("Select Student", s_list)
            idx = st.session_state.db[st.session_state.db["Name"] == sel].index[0]
            level = st.session_state.db.at[idx, "Level"]
            lessons = get_lessons(level)
            current = st.session_state.db.at[idx, "Skills"]
            
            new_s = []
            for m in lessons:
                if st.checkbox(m, value=(m in current)): new_s.append(m)
            
            if st.button("Update Skills"):
                st.session_state.db.at[idx, "Skills"] = new_s
                st.success("Updated!")

    # --- ៥.៤ Certification ---
    elif menu == "📜 Certification":
        st.header("Generate Certificate")
        s_list = st.session_state.db["Name"].tolist()
        if s_list:
            sel = st.selectbox("Select Recipient", s_list)
            info = st.session_state.db[st.session_state.db["Name"] == sel].iloc[0]
            if st.button("PRINT"):
                st.balloons()
                cert_html = f"""
                <div class="cert-paper">
                    <div class="cert-border">
                        <h1 style="color:#001f3f;">JUNIOR MEDICAL INSTITUTE</h1>
                        <p style="color:#333;">Certificate of Achievement</p>
                        <h2 class="student-name">{info['Name']}</h2>
                        <p style="color:#333;">Level: {info['Level']}</p>
                        <div style="margin-top:30px; border-top:1px solid #333; width:200px; margin-left:auto; margin-right:auto;">
                            <p style="color:#001f3f; font-weight:bold;">Dr. Chan Sokhoeurn</p>
                        </div>
                    </div>
                </div>
                """
                st.markdown(cert_html, unsafe_allow_html=True)
else:
    st.info("🔒 Please enter key to unlock.")
