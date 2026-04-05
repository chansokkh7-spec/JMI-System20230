import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# --- ១. ការកំណត់ទម្រង់កម្មវិធី (Standard Config) ---
st.set_page_config(
    page_title="JMI | Strategic Management Portal",
    page_icon="🛡️",
    layout="wide"
)

# --- ២. ការរចនា Style (Modern Navy & Luxury Gold) ---
style_block = """
<link href="https://fonts.googleapis.com/css2?family=Great+Vibes&family=Cinzel:wght@600&family=Montserrat:wght@300;600&family=Kantumruy+Pro:wght@400;700&display=swap" rel="stylesheet">
<style>
    /* Global Reset */
    html, body, [class*="css"], .stMarkdown {
        font-family: 'Kantumruy Pro', sans-serif;
        color: #E0E0E0;
    }
    .stApp { background: radial-gradient(circle, #002d5a 0%, #001529 100%); }
    
    /* Metrics/KPI Cards */
    .kpi-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(212, 175, 55, 0.3);
        border-radius: 15px;
        padding: 25px;
        text-align: center;
        transition: 0.4s;
    }
    .kpi-card:hover { border-color: #D4AF37; transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0,0,0,0.4); }
    .kpi-value { font-size: 38px; font-weight: bold; color: #D4AF37; font-family: 'Cinzel'; }
    .kpi-label { font-size: 13px; text-transform: uppercase; letter-spacing: 2px; color: #888; }

    /* Buttons Style */
    .stButton>button {
        background: linear-gradient(135deg, #D4AF37 0%, #B8860B 100%) !important;
        color: #001529 !important;
        font-weight: bold !important;
        border-radius: 30px !important;
        padding: 10px 25px !important;
        border: none !important;
        width: 100%;
    }

    /* Checkbox for Skill Passport */
    .stCheckbox label p {
        color: #D4AF37 !important;
        font-weight: bold !important;
    }

    /* --- International Certificate Frame --- */
    .cert-frame {
        background: #fff;
        padding: 20px;
        border: 15px solid #D4AF37;
        position: relative;
        max-width: 900px;
        margin: auto;
        box-shadow: 0 20px 40px rgba(0,0,0,0.5);
    }
    .cert-inner {
        border: 2px solid #001529;
        padding: 60px;
        text-align: center;
        background-image: url('https://www.transparenttextures.com/patterns/cream-paper.png');
    }
    .cert-badge { width: 100px; margin-bottom: 20px; }
    .cert-title { font-family: 'Cinzel', serif; font-size: 45px; color: #001529; margin: 0; }
    .cert-name { font-family: 'Great Vibes', cursive; font-size: 75px; color: #D4AF37; margin: 25px 0; }
    .cert-body { font-family: 'DM Serif Display', serif; font-size: 22px; color: #333; line-height: 1.6; }
    .cert-footer { display: flex; justify-content: space-between; margin-top: 60px; }
    .sig-line { border-top: 2px solid #001529; width: 220px; color: #001529; font-weight: bold; padding-top: 5px; text-align: center;}
</style>
"""
st.markdown(style_block, unsafe_allow_html=True)

# --- ៣. ការគ្រប់គ្រងទិន្នន័យ (Database Session) ---
if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame([
        {"ID": "JMI-2026-001", "Name": "DR. CHAN SOKHOEURN", "Level": "វិទ្យាល័យ", "Enroll_Date": "2026-04-05", "Status": "Active", "Skills": ["មេរៀនទី 1", "មេរៀនទី 2"]}
    ])

# --- ៤. Sidebar Navigation ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color:#D4AF37;'>JMI EXECUTIVE</h2>", unsafe_allow_html=True)
    st.markdown("<center><h1 style='font-size:70px;'>🛡️</h1></center>", unsafe_allow_html=True)
    st.markdown("---")
    pwd = st.text_input("Access Key", type="password")

if pwd == "JMI2026":
    menu = st.sidebar.radio("MANAGEMENT HUB", ["📊 Global Dashboard", "🎓 Enrollment", "🏅 Skill Passport", "📜 Certification"])

    def get_lessons(level):
        return [f"មេរៀនទី {i}" for i in range(1, 10)] if level in ["មត្តេយ្យ", "បឋម"] else [f"មេរៀនទី {i}" for i in range(1, 13)]

    # --- ៥.១ Dashboard (International Standard) ---
    if menu == "📊 Global Dashboard":
        st.title("🏥 JMI Strategic Dashboard")
        
        # Row 1: KPI Metrics
        c1, c2, c3, c4 = st.columns(4)
        c1.markdown(f'<div class="kpi-card"><div class="kpi-label">TOTAL SCHOLARS</div><div class="kpi-value">{len(st.session_state.db)}</div></div>', unsafe_allow_html=True)
        c2.markdown('<div class="kpi-card"><div class="kpi-label">SYSTEM UPTIME</div><div class="kpi-value">99.9%</div></div>', unsafe_allow_html=True)
        c3.markdown('<div class="kpi-card"><div class="kpi-label">ACADEMIC YEAR</div><div class="kpi-value">2026</div></div>', unsafe_allow_html=True)
        c4.markdown('<div class="kpi-card"><div class="kpi-label">STATUS</div><div class="kpi-value">LIVE</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        
        # Row 2: Analytics & Database
        col_left, col_right = st.columns([1, 1])
        
        with col_left:
            st.subheader("📈 Scholar Analytics")
            if not st.session_state.db.empty:
                level_data = st.session_state.db['Level'].value_counts().reset_index()
                fig = px.pie(level_data, values='count', names='Level', hole=.4, 
                             color_discrete_sequence=['#D4AF37', '#00509d', '#f1c40f', '#2c3e50'])
                fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="white", showlegend=True)
                st.plotly_chart(fig, use_container_width=True)
        
        with col_right:
            st.subheader("📂 Master Registry")
            st.dataframe(st.session_state.db[["ID", "Name", "Level", "Status"]], use_container_width=True)

    # --- ៥.២ Enrollment ---
    elif menu == "🎓 Enrollment":
        st.header("Register New Scholar")
        with st.form("enroll_form", clear_on_submit=True):
            col_a, col_b = st.columns(2)
            name = col_a.text_input("Scholar Full Name")
            level = col_b.selectbox("Academic Level", ["មត្តេយ្យ", "បឋម", "អនុវិទ្យាល័យ", "វិទ្យាល័យ"])
            if st.form_submit_button("CONFIRM REGISTRATION"):
                new_id = f"JMI-{datetime.now().year}-{len(st.session_state.db)+1:03d}"
                new_entry = pd.DataFrame([{"ID": new_id, "Name": name.upper(), "Level": level, "Enroll_Date": datetime.now().strftime("%Y-%m-%d"), "Status": "Active", "Skills": []}])
                st.session_state.db = pd.concat([st.session_state.db, new_entry], ignore_index=True)
                st.success(f"Success! {name} has been enrolled.")

    # --- ៥.៣ Skill Passport ---
    elif menu == "🏅 Skill Passport":
        st.header("🏅 Skill Mastery Tracker")
        levels = ["មត្តេយ្យ", "បឋម", "អនុវិទ្យាល័យ", "វិទ្យាល័យ"]
        sel_level = st.selectbox("Filter Level:", levels)
        filtered = st.session_state.db[st.session_state.db['Level'] == sel_level]
        
        if not filtered.empty:
            sel_student = st.selectbox("Select Scholar:", filtered['Name'].tolist())
            idx = st.session_state.db[st.session_state.db['Name'] == sel_student].index[0]
            all_lessons = get_lessons(sel_level)
            current_skills = st.session_state.db.at[idx, 'Skills']
            
            st.markdown(f"### Update Progress for: <span style='color:#D4AF37'>{sel_student}</span>", unsafe_allow_html=True)
            new_selection = []
            c1, c2 = st.columns(2)
            for i, m in enumerate(all_lessons):
                with (c1 if i % 2 == 0 else c2):
                    if st.checkbox(m, value=(m in current_skills), key=f"chk_{idx}_{m}"):
                        new_selection.append(m)
            
            if st.button("💾 SAVE PROGRESS"):
                st.session_state.db.at[idx, 'Skills'] = new_selection
                st.success("Synchronized successfully!")
        else:
            st.warning("No scholars found in this level.")

    # --- ៥.៤ Certification (International Luxury Standard) ---
    elif menu == "📜 Certification":
        st.header("📜 Professional Certification Hub")
        
        c_level = st.selectbox("Step 1: Academic Level", ["មត្តេយ្យ", "បឋម", "អនុវិទ្យាល័យ", "វិទ្យាល័យ"], key="cert_lvl")
        c_filtered = st.session_state.db[st.session_state.db['Level'] == c_level]
        
        if not c_filtered.empty:
            c_name = st.selectbox("Step 2: Recipient Name", c_filtered['Name'].tolist(), key="cert_name")
            s_data = st.session_state.db[st.session_state.db['Name'] == c_name].iloc[0]
            
            if st.button("🌟 ISSUE INTERNATIONAL CERTIFICATE"):
                st.balloons()
                cert_html = f"""
                <div class="cert-frame">
                    <div class="cert-inner">
                        <img src="https://cdn-icons-png.flaticon.com/512/610/610333.png" class="cert-badge">
                        <h1 class="cert-title">JUNIOR MEDICAL INSTITUTE</h1>
                        <p style="text-transform: uppercase; letter-spacing: 5px; color: #666; font-size: 12px; margin-top:10px;">Global Academic Excellence</p>
                        <hr style="border: 0.5px solid #D4AF37; width: 40%; margin: 20px auto;">
                        <p class="cert-body" style="color: #555;">This is to certify that</p>
                        <h2 class="cert-name">{s_data['Name']}</h2>
                        <p class="cert-body" style="color: #333;">
                            has demonstrated exceptional proficiency and successfully <br>
                            completed the required medical curriculum for the level of<br>
                            <b style="color: #001529; font-size: 26px;">{s_data['Level']}</b>
                        </p>
                        <div class="cert-footer">
                            <div class="sig-box">
                                <div style="color:#001529; font-size:14px; margin-bottom:5px;">{datetime.now().strftime("%d %B %Y")}</div>
                                <div class="sig-line">DATE OF ISSUE</div>
                            </div>
                            <div class="sig-box">
                                <p style="font-family: 'Great Vibes'; font-size: 32px; margin:0; color:#001529;">Dr. Chan Sokhoeurn</p>
                                <div class="sig-line">ACADEMIC DIRECTOR</div>
                                <span style="font-size: 10px; color: #D4AF37;">C2/DBA & PhD in Leadership</span>
                            </div>
                        </div>
                    </div>
                </div>
                """
                st.markdown(cert_html, unsafe_allow_html=True)
        else:
            st.warning("Please enroll scholars before issuing certificates.")

else:
    st.title("🏥 JMI Global Strategic Portal")
    st.warning("🔒 Enter Executive Security Key to Unlock.")
