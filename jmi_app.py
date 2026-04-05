import streamlit as st
import pandas as pd
from datetime import datetime

# --- ១. ការកំណត់ទម្រង់កម្មវិធី ---
st.set_page_config(
    page_title="JMI | Strategic Management Portal",
    page_icon="🏥",
    layout="wide"
)

# --- ២. ការរចនា Style (Navy Blue & Gold Premium) ---
style_block = """
<link href="https://fonts.googleapis.com/css2?family=Great+Vibes&family=Cinzel:wght@700&family=DM+Serif+Display&family=Kantumruy+Pro:wght@400;700&display=swap" rel="stylesheet">
<style>
    html, body, [class*="css"], .stMarkdown {
        font-family: 'Kantumruy Pro', sans-serif;
        color: #ffffff;
    }
    .stApp { background-color: #001f3f; }
    
    /* ការកំណត់អក្សរមេរៀនក្នុង Skill Passport */
    .stCheckbox label p {
        color: #D4AF37 !important;
        font-weight: bold !important;
    }
    
    h1, h2, h3 { color: #D4AF37 !important; }
    
    .stButton>button {
        background-color: #D4AF37 !important;
        color: #001f3f !important;
        font-weight: bold !important;
        border-radius: 8px !important;
    }

    /* --- ការរចនាវិញ្ញាបនបត្រ (Premium Certificate) --- */
    .cert-container {
        background-color: white;
        padding: 30px;
        border: 15px solid #D4AF37;
        box-shadow: 0 0 30px rgba(212, 175, 55, 0.5);
        max-width: 900px;
        margin: auto;
        color: #001f3f;
        position: relative;
    }
    .cert-inner-border {
        border: 3px double #001f3f;
        padding: 50px;
        text-align: center;
    }
    .cert-header { font-family: 'Cinzel', serif; font-size: 45px; margin: 0; color: #001f3f; }
    .cert-sub { font-size: 18px; letter-spacing: 3px; color: #555; text-transform: uppercase; }
    .cert-name { font-family: 'Great Vibes', cursive; font-size: 65px; color: #D4AF37; margin: 20px 0; }
    .cert-body { font-family: 'DM Serif Display', serif; font-size: 20px; color: #333; line-height: 1.6; }
    .cert-footer { margin-top: 50px; display: flex; justify-content: space-around; align-items: flex-end; }
    .signature-area { border-top: 2px solid #001f3f; width: 220px; padding-top: 10px; font-weight: bold; }
</style>
"""
st.markdown(style_block, unsafe_allow_html=True)

# --- ៣. ការគ្រប់គ្រងទិន្នន័យ ---
if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame([
        {"ID": "JMI-001", "Name": "CHAN SOKHOEURN", "Level": "វិទ្យាល័យ", "Enroll_Date": "2026-04-05", "Status": "Active", "Skills": ["មេរៀនទី 1", "មេរៀនទី 2"]}
    ])

# --- ៤. Sidebar ---
st.sidebar.markdown("<h2 style='text-align: center;'>JMI EXECUTIVE</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<center><h1 style='font-size:60px; color: #D4AF37;'>🛡️</h1></center>", unsafe_allow_html=True)
pwd = st.sidebar.text_input("Director's Key", type="password")

if pwd == "JMI2026":
    menu = st.sidebar.radio("STRATEGIC MODULES", ["📊 Dashboard", "🎓 Enrollment", "🏅 Skill Passport", "📜 Certification"])

    def get_lessons(level):
        return [f"មេរៀនទី {i}" for i in range(1, 10)] if level in ["មត្តេយ្យ", "បឋម"] else [f"មេរៀនទី {i}" for i in range(1, 13)]

    # --- ៥.១ Dashboard ---
    if menu == "📊 Dashboard":
        st.title("🏥 Command Center")
        st.dataframe(st.session_state.db, use_container_width=True)

    # --- ៥.២ Enrollment ---
    elif menu == "🎓 Enrollment":
        st.header("Register Scholar")
        with st.form("reg"):
            n = st.text_input("Full Name")
            l = st.selectbox("Level", ["មត្តេយ្យ", "បឋម", "អនុវិទ្យាល័យ", "វិទ្យាល័យ"])
            if st.form_submit_button("ADD SCHOLAR"):
                new_row = pd.DataFrame([{"ID": f"JMI-{len(st.session_state.db)+1:03d}", "Name": n.upper(), "Level": l, "Enroll_Date": "2026-04-05", "Status": "Active", "Skills": []}])
                st.session_state.db = pd.concat([st.session_state.db, new_row], ignore_index=True)
                st.success("Added!")

    # --- ៥.៣ Skill Passport ---
    elif menu == "🏅 Skill Passport":
        st.header("🏅 Skill Mastery Passport")
        sel_level = st.selectbox("Select Level:", ["មត្តេយ្យ", "បឋម", "អនុវិទ្យាល័យ", "វិទ្យាល័យ"], key="skill_level")
        filtered = st.session_state.db[st.session_state.db['Level'] == sel_level]
        
        if not filtered.empty:
            sel_student = st.selectbox("Select Student:", filtered['Name'].tolist())
            idx = st.session_state.db[st.session_state.db['Name'] == sel_student].index[0]
            lessons = get_lessons(sel_level)
            current = st.session_state.db.at[idx, 'Skills']
            
            new_s = []
            c1, c2 = st.columns(2)
            for i, m in enumerate(lessons):
                with (c1 if i % 2 == 0 else c2):
                    if st.checkbox(m, value=(m in current), key=f"sk_{m}"): new_s.append(m)
            
            if st.button("💾 SAVE PROGRESS"):
                st.session_state.db.at[idx, 'Skills'] = new_s
                st.success("Updated!")
        else: st.warning("គ្មានទិន្នន័យសិស្សក្នុងកម្រិតនេះទេ។")

    # --- ៥.៤ Certification (កែសម្រួលថ្មីតាមទម្រង់ Skill Passport) ---
    elif menu == "📜 Certification":
        st.header("📜 Official Certification Hub")
        
        # រៀបចំការ Filter ដូច Skill Passport
        c_level = st.selectbox("Step 1: Select Academic Level", ["មត្តេយ្យ", "បឋម", "អនុវិទ្យាល័យ", "វិទ្យាល័យ"], key="cert_level")
        c_filtered = st.session_state.db[st.session_state.db['Level'] == c_level]
        
        if not c_filtered.empty:
            c_student = st.selectbox("Step 2: Select Recipient Name", c_filtered['Name'].tolist())
            s_info = st.session_state.db[st.session_state.db['Name'] == c_student].iloc[0]
            
            st.markdown("---")
            if st.button("🌟 GENERATE PREMIUM CERTIFICATE"):
                st.balloons()
                
                # បង្កើតផ្កាយតាមចំនួនមេរៀនដែលបានរៀន
                stars = " ".join(["★" for _ in range(min(len(s_info['Skills']), 10))])
                
                cert_html = f"""
                <div class="cert-container">
                    <div class="cert-inner-border">
                        <p class="cert-sub">Junior Medical Institute</p>
                        <h1 class="cert-header">CERTIFICATE</h1>
                        <p style="color: #D4AF37; font-size: 24px;">{stars}</p>
                        <p class="cert-body">This is to certify that</p>
                        <h2 class="cert-name">{s_info['Name']}</h2>
                        <p class="cert-body">
                            has successfully demonstrated exceptional proficiency and <br>
                            completed the required curriculum for the level of<br>
                            <b style="font-size: 24px; color: #001f3f;">{s_info['Level']}</b>
                        </p>
                        <div class="cert-footer">
                            <div style="text-align: center;">
                                <p style="margin:0;">{datetime.now().strftime("%d %B %Y")}</p>
                                <div class="signature-area">DATE</div>
                            </div>
                            <div style="text-align: center;">
                                <p style="font-family: 'Great Vibes'; font-size: 30px; margin:0;">Dr. Chan Sokhoeurn</p>
                                <div class="signature-area">ACADEMIC DIRECTOR</div>
                            </div>
                        </div>
                    </div>
                </div>
                """
                st.markdown(cert_html, unsafe_allow_html=True)
        else:
            st.warning("មិនទាន់មានសិស្សក្នុងកម្រិតនេះសម្រាប់ចេញវិញ្ញាបនបត្រទេ។")

else:
    st.title("🏥 JMI Strategic Portal")
    st.info("🔒 Please enter Director's Key to unlock the system.")
