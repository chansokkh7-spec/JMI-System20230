import streamlit as st
import pandas as pd
from datetime import datetime

# --- ១. ដោះស្រាយបញ្ហា ModuleNotFoundError (Plotly) ---
try:
    import plotly.express as px
    HAS_PLOTLY = True
except ImportError:
    HAS_PLOTLY = False

# --- ២. ការកំណត់ទម្រង់កម្មវិធី ---
st.set_page_config(page_title="JMI | Strategic Management Portal", page_icon="🛡️", layout="wide")

# --- ៣. ការរចនា Style បន្ថែម (Custom CSS) ---
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600&family=Kantumruy+Pro:wght@400;700&display=swap" rel="stylesheet">
<style>
    .stApp { background: radial-gradient(circle, #002d5a 0%, #001529 100%); color: #E6E9ED !important; }
    [data-testid="stSidebar"] { background-color: #001529 !important; border-right: 1px solid rgba(212,175,55,0.2); }
    .header-style { color: #D4AF37 !important; border-left: 5px solid #D4AF37; padding-left: 15px; font-family: 'Cinzel'; }
    .skill-card { background: rgba(255,255,255,0.05); border: 1px solid rgba(212,175,55,0.2); border-radius: 10px; padding: 15px; margin-bottom: 10px; }
    .stButton>button { border-radius: 8px !important; font-weight: 600 !important; }
</style>
""", unsafe_allow_html=True)

# --- ៤. ការគ្រប់គ្រងទិន្នន័យ (Session State) ---
if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame([
        {"ID": "JMI-001", "Name": "CHAN SOKHOEURN", "Level": "វិទ្យាល័យ", "Enroll_Date": "2026-03-25", "Status": "Active"}
    ])

# --- ៥. Sidebar Navigation ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color:#D4AF37;'>JMI EXECUTIVE</h2>", unsafe_allow_html=True)
    st.markdown("<center><h1 style='font-size:70px; margin:0;'>🛡️</h1></center>", unsafe_allow_html=True)
    st.markdown("---")
    pwd = st.text_input("Director's Key", type="password")
    
    if pwd == "JMI2026":
        st.success("Welcome, Dr. CHAN Sokhoeurn")
        menu = st.sidebar.radio("STRATEGIC MODULES", ["📊 Dashboard", "🎓 Enrollment", "📔 Skill Passport", "📜 Certification"])
    else:
        st.warning("Please enter access key")
        st.stop()

# --- MODULE 1: DASHBOARD (ជាមួយ Quick Filter) ---
if menu == "📊 Dashboard":
    st.markdown("<h1 class='header-style'>JMI Strategic Command Center</h1>", unsafe_allow_html=True)
    
    # KPI Top Row
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Scholars", len(st.session_state.db))
    c2.metric("Status", "Operational")
    c3.metric("Year", "2026")

    # Quick Filter System (ចំណុចបន្ថែមទី៣)
    st.markdown("### 🔍 ចម្រោះទិន្នន័យតាមកម្រិតសិក្សា (Quick Filter)")
    lv_filter = st.segmented_control("ជ្រើសរើសកម្រិត:", ["ទាំងអស់", "មត្តេយ្យ", "បឋម", "អនុវិទ្យាល័យ", "វិទ្យាល័យ"], default="ទាំងអស់")
    
    df_display = st.session_state.db
    if lv_filter != "ទាំងអស់":
        df_display = st.session_state.db[st.session_state.db['Level'] == lv_filter]

    st.dataframe(df_display, use_container_width=True)

    # Data Management Hub (ចំណុចបន្ថែមទី២ - កែសម្រួលទិន្នន័យ)
    st.markdown("### ⚙️ Data Management Hub (រក្សាទុក កែ និងលុប)")
    edited_df = st.data_editor(st.session_state.db, num_rows="dynamic", use_container_width=True)
    if st.button("រក្សាទុកការកែប្រែ (Save Changes)"):
        st.session_state.db = edited_df
        st.success("ទិន្នន័យត្រូវបានធ្វើបច្ចុប្បន្នភាព!")

# --- MODULE 2: ENROLLMENT ---
elif menu == "🎓 Enrollment":
    st.markdown("<h1 class='header-style'>Scholar Registration</h1>", unsafe_allow_html=True)
    with st.form("enroll"):
        name = st.text_input("ឈ្មោះសិស្ស (Full Name)")
        level = st.selectbox("កម្រិតសិក្សា", ["មត្តេយ្យ", "បឋម", "អនុវិទ្យាល័យ", "វិទ្យាល័យ"])
        if st.form_submit_button("REGISTER NOW"):
            new_id = f"JMI-{len(st.session_state.db)+1:03d}"
            new_row = {"ID": new_id, "Name": name.upper(), "Level": level, "Enroll_Date": datetime.now().strftime("%Y-%m-%d"), "Status": "Active"}
            st.session_state.db = pd.concat([st.session_state.db, pd.DataFrame([new_row])], ignore_index=True)
            st.balloons()
            st.success(f"សិស្ស {name} ចុះឈ្មោះជោគជ័យ!")

# --- MODULE 3: SKILL PASSPORT (ចំណុចបន្ថែមទី១ - មេរៀន) ---
elif menu == "📔 Skill Passport":
    st.markdown("<h1 class='header-style'>📔 Skill Mastery Passport</h1>", unsafe_allow_html=True)
    sel_student = st.selectbox("Select Student:", st.session_state.db['Name'].tolist())
    student_level = st.session_state.db[st.session_state.db['Name'] == sel_student]['Level'].values[0]
    
    st.info(f"កម្រិត: {student_level} (មានចំនួន ១២ មេរៀន)")
    
    cols = st.columns(2)
    for i in range(1, 13):
        col_idx = 0 if i <= 6 else 1
        with cols[col_idx]:
            st.checkbox(f"មេរៀនទី {i}", key=f"lesson_{sel_student}_{i}")
    
    if st.button("💾 Save Progress"):
        st.success(f"វឌ្ឍនភាពរបស់ {sel_student} ត្រូវបានរក្សាទុក!")

# --- MODULE 4: CERTIFICATION ---
elif menu == "📜 Certification":
    st.markdown("<h1 class='header-style'>Certification Generator</h1>", unsafe_allow_html=True)
    rec_name = st.selectbox("Select Recipient:", st.session_state.db['Name'].tolist())
    s_info = st.session_state.db[st.session_state.db['Name'] == rec_name].iloc[0]
    
    if st.button("GENERATE"):
        st.markdown(f"""
        <div style="background:white; padding:40px; border:15px solid #D4AF37; text-align:center; color:#001529;">
            <h1 style="color:#D4AF37; margin:0;">JUNIOR MEDICAL INSTITUTE</h1>
            <p>Certificate of Completion</p>
            <h2 style="font-family:'Cinzel'; font-size:50px; color:#B8860B;">{s_info['Name']}</h2>
            <p>Successfully mastered the curriculum for <b>{s_info['Level']}</b></p>
            <br><br>
            <hr style="width:30%; border:1px solid #001529;">
            <b>Dr. Chan Sokhoeurn</b>
        </div>
        """, unsafe_allow_html=True)
