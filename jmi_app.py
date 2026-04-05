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

# --- ៣. ការរចនា Style បន្ថែម (អក្សរពណ៌មាសទាំងអស់) ---
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600&family=Kantumruy+Pro:wght@400;700&display=swap" rel="stylesheet">
<style>
    /* កំណត់ផ្ទៃខាងក្រោយ */
    .stApp { 
        background: radial-gradient(circle, #002d5a 0%, #001529 100%); 
    }

    /* បង្ខំឱ្យអក្សរទាំងអស់ទៅជាពណ៌មាស #D4AF37 */
    html, body, [data-testid="stWidgetLabel"], .stMarkdown, p, span, label, li, div, h1, h2, h3, .stMetric, [data-testid="stHeader"] {
        color: #D4AF37 !important;
        font-family: 'Kantumruy Pro', 'Cinzel', sans-serif;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] { 
        background-color: #001529 !important; 
        border-right: 1px solid rgba(212,175,55,0.4); 
    }
    
    /* ការកំណត់ពណ៌មាសសម្រាប់ Input Boxes និង Widgets */
    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stDataEditor {
        color: #D4AF37 !important;
        border-color: rgba(212,175,55,0.5) !important;
    }

    .header-style { 
        color: #D4AF37 !important; 
        border-left: 5px solid #D4AF37; 
        padding-left: 15px; 
        font-family: 'Cinzel'; 
    }

    /* រចនាប៊ូតុងឱ្យមានពន្លឺមាស */
    .stButton>button { 
        background: linear-gradient(135deg, #D4AF37 0%, #B8860B 100%) !important;
        color: #001529 !important; /* អក្សរក្នុងប៊ូតុងពណ៌ខៀវចាស់ដើម្បីឱ្យច្បាស់ */
        border-radius: 8px !important; 
        font-weight: 700 !important;
        border: none !important;
    }
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

# --- MODULE 1: DASHBOARD ---
if menu == "📊 Dashboard":
    st.markdown("<h1 class='header-style'>JMI Strategic Command Center</h1>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Scholars", len(st.session_state.db))
    c2.metric("Status", "Operational")
    c3.metric("Year", "2026")

    st.markdown("### 🔍 ចម្រោះទិន្នន័យតាមកម្រិតសិក្សា (Quick Filter)")
    lv_filter = st.segmented_control("ជ្រើសរើសកម្រិត:", ["ទាំងអស់", "មត្តេយ្យ", "បឋម", "អនុវិទ្យាល័យ", "វិទ្យាល័យ"], default="ទាំងអស់")
    
    df_display = st.session_state.db
    if lv_filter != "ទាំងអស់":
        df_display = st.session_state.db[st.session_state.db['Level'] == lv_filter]

    st.dataframe(df_display, use_container_width=True)

    st.markdown("### ⚙️ Data Management Hub")
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

# --- MODULE 3: SKILL PASSPORT ---
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
        # សម្រាប់សញ្ញាបត្រ ខ្ញុំរក្សាពណ៌ចម្រុះ (ស/មាស) ដើម្បីឱ្យដូចសញ្ញាបត្រពិត
        st.markdown(f"""
        <div style="background:white; padding:40px; border:15px solid #D4AF37; text-align:center;">
            <h1 style="color:#D4AF37 !important; margin:0; font-family:'Cinzel';">JUNIOR MEDICAL INSTITUTE</h1>
            <p style="color:#001529 !important;">Certificate of Completion</p>
            <h2 style="font-family:'Cinzel'; font-size:50px; color:#B8860B !important;">{s_info['Name']}</h2>
            <p style="color:#001529 !important;">Successfully mastered the curriculum for <b>{s_info['Level']}</b></p>
            <br><br>
            <hr style="width:30%; border:1px solid #001529;">
            <b style="color:#001529 !important;">Dr. Chan Sokhoeurn</b>
        </div>
        """, unsafe_allow_html=True)
