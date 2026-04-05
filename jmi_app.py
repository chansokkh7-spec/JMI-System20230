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
    
    /* កែសម្រួលពណ៌អក្សរមេរៀនឱ្យច្បាស់ */
    .stCheckbox label p {
        color: #D4AF37 !important;
        font-weight: bold !important;
        font-size: 16px !important;
    }
    
    h1, h2, h3 { color: #D4AF37 !important; }
    
    /* ប៊ូតុងពណ៌មាស */
    .stButton>button {
        background-color: #D4AF37 !important;
        color: #001f3f !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        border: none !important;
    }

    /* --- ការរចនាវិញ្ញាបនបត្រតាមស្ទីលចាស់ដែលលោកគ្រូពេញចិត្ត --- */
    .cert-main-box {
        background-color: white;
        padding: 20px;
        border: 15px solid #D4AF37; /* ស៊ុមមាសក្រាស់ */
        max-width: 900px;
        margin: auto;
        color: #001f3f;
    }
    .cert-content {
        border: 2px solid #001f3f;
        padding: 40px;
        text-align: center;
    }
    .cert-title { font-family: 'Cinzel', serif; font-size: 40px; color: #D4AF37; margin: 0; }
    .cert-name { font-family: 'Great Vibes', cursive; font-size: 60px; color: #D4AF37; margin: 20px 0; }
    .cert-text { font-size: 20px; color: #333; }
</style>
"""
st.markdown(style_block, unsafe_allow_html=True)

# --- ៣. ការគ្រប់គ្រងទិន្នន័យ (Session State) ---
if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame([
        {"ID": "JMI-001", "Name": "CHAN SOKHOEURN", "Level": "វិទ្យាល័យ", "Enroll_Date": "2026-03-25", "Status": "Active", "Skills": []}
    ])

# --- ៤. Sidebar ---
st.sidebar.markdown("<h2 style='text-align: center;'>JMI EXECUTIVE</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<center><h1 style='font-size:60px; color: #D4AF37;'>🛡️</h1></center>", unsafe_allow_html=True)
pwd = st.sidebar.text_input("Director's Key", type="password")

if pwd == "JMI2026":
    menu = st.sidebar.radio("STRATEGIC MODULES", ["📊 Dashboard", "🎓 Enrollment", "🏅 Skill Passport", "📜 Certification"])

    def get_lessons(level):
        return [f"មេរៀនទី {i}" for i in range(1, 10)] if level in ["មត្តេយ្យ", "បឋម"] else [f"មេរៀនទី {i}" for i in range(1, 13)]

    # --- ៥.១ Dashboard (ជួសជុល Error) ---
    if menu == "📊 Dashboard":
        st.title("🏥 JMI Strategic Command Center")
        
        # បង្ហាញតារាងធម្មតា (ជៀសវាង Error ពី Data Editor)
        st.markdown("### 📋 បញ្ជីឈ្មោះសិស្សទាំងស្រុង")
        st.dataframe(st.session_state.db, use_container_width=True)
        
        if st.button("🗑️ លុបទិន្នន័យទាំងអស់ (Clear All)"):
            st.session_state.db = pd.DataFrame(columns=["ID", "Name", "Level", "Enroll_Date", "Status", "Skills"])
            st.rerun()

    # --- ៥.២ Enrollment ---
    elif menu == "🎓 Enrollment":
        st.header("Enroll New Scholar")
        with st.form("reg_form"):
            n = st.text_input("Scholar Name")
            l = st.selectbox("Level", ["មត្តេយ្យ", "បឋម", "អនុវិទ្យាល័យ", "វិទ្យាល័យ"])
            if st.form_submit_button("REGISTER"):
                new_id = f"JMI-{len(st.session_state.db)+1:03d}"
                new_data = pd.DataFrame([{"ID": new_id, "Name": n.upper(), "Level": l, "Enroll_Date": "2026-04-05", "Status": "Active", "Skills": []}])
                st.session_state.db = pd.concat([st.session_state.db, new_data], ignore_index=True)
                st.success(f"Registered {n}!")

    # --- ៥.៣ Skill Passport ---
    elif menu == "🏅 Skill Passport":
        st.header("🏅 Skill Mastery Passport")
        levels = ["មត្តេយ្យ", "បឋម", "អនុវិទ្យាល័យ", "វិទ្យាល័យ"]
        sel_l = st.selectbox("Select Level:", levels)
        filtered = st.session_state.db[st.session_state.db['Level'] == sel_l]
        
        if not filtered.empty:
            sel_n = st.selectbox("Select Student:", filtered['Name'].tolist())
            idx = st.session_state.db[st.session_state.db['Name'] == sel_n].index[0]
            lessons = get_lessons(sel_l)
            current = st.session_state.db.at[idx, 'Skills']
            
            new_selection = []
            col1, col2 = st.columns(2)
            for i, m in enumerate(lessons):
                with (col1 if i % 2 == 0 else col2):
                    if st.checkbox(m, value=(m in current), key=f"chk_{idx}_{m}"):
                        new_selection.append(m)
            
            if st.button("💾 Save Progress"):
                st.session_state.db.at[idx, 'Skills'] = new_selection
                st.success("Updated!")
        else:
            st.warning("មិនទាន់មានសិស្សក្នុងកម្រិតនេះទេ។")

    # --- ៥.៤ Certification (កែឱ្យដូច Skill Passport និងស្អាតដូចមុន) ---
    elif menu == "📜 Certification":
        st.header("📜 Certification Generator")
        
        # រៀបចំ Layout ដូច Skill Passport
        c_level = st.selectbox("១. ជ្រើសរើសកម្រិតសិក្សា:", ["មត្តេយ្យ", "បឋម", "អនុវិទ្យាល័យ", "វិទ្យាល័យ"])
        c_filtered = st.session_state.db[st.session_state.db['Level'] == c_level]
        
        if not c_filtered.empty:
            c_student = st.selectbox("២. ជ្រើសរើសឈ្មោះសិស្ស:", c_filtered['Name'].tolist())
            s_info = st.session_state.db[st.session_state.db['Name'] == c_student].iloc[0]
            
            if st.button("🌟 GENERATE CERTIFICATE"):
                st.balloons()
                cert_html = f"""
                <div class="cert-main-box">
                    <div class="cert-content">
                        <h1 class="cert-title">JUNIOR MEDICAL INSTITUTE</h1>
                        <p style="letter-spacing: 2px;">Certificate of Completion</p>
                        <br>
                        <h2 class="cert-name">{s_info['Name']}</h2>
                        <p class="cert-text">Successfully mastered the curriculum for <b>{s_info['Level']}</b></p>
                        <br><br>
                        <div style="border-top: 2px solid #333; width: 250px; margin: auto;">
                            <p style="margin: 5px 0 0 0; font-weight: bold;">Dr. Chan Sokhoeurn</p>
                            <small>Academic Director</small>
                        </div>
                    </div>
                </div>
                """
                st.markdown(cert_html, unsafe_allow_html=True)
        else:
            st.warning("មិនទាន់មានសិស្សសម្រាប់ចេញវិញ្ញាបនបត្រទេ។")

else:
    st.info("🔒 Please enter key to unlock.")
