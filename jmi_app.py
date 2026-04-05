import streamlit as st
import pandas as pd
from datetime import datetime

# --- ១. ការពារ Error Library ---
try:
    import plotly.express as px
    HAS_PLOTLY = True
except ImportError:
    HAS_PLOTLY = False

# --- ២. ការកំណត់ទម្រង់កម្មវិធី ---
st.set_page_config(page_title="JMI | Strategic Management Portal", page_icon="🛡️", layout="wide")

# --- ៣. ការរចនា Style (Golden Luxury Theme) ---
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600&family=Kantumruy+Pro:wght@400;700&display=swap" rel="stylesheet">
<style>
    .stApp { background: radial-gradient(circle, #002d5a 0%, #001529 100%); }
    html, body, [data-testid="stWidgetLabel"], .stMarkdown, p, span, label, li, div, h1, h2, h3, .stMetric, [data-testid="stHeader"] {
        color: #D4AF37 !important;
        font-family: 'Kantumruy Pro', 'Cinzel', sans-serif;
    }
    [data-testid="stSidebar"] { background-color: #001529 !important; border-right: 1px solid rgba(212,175,55,0.4); }
    .stButton>button { 
        background: linear-gradient(135deg, #D4AF37 0%, #B8860B 100%) !important;
        color: #001529 !important; border-radius: 8px !important; font-weight: 700 !important; border: none !important;
    }
    .header-style { border-left: 5px solid #D4AF37; padding-left: 15px; margin-bottom: 20px; }
    .finance-card { background: rgba(212, 175, 55, 0.1); border: 1px solid #D4AF37; padding: 20px; border-radius: 15px; text-align: center; }
</style>
""", unsafe_allow_html=True)

# --- ៤. ការគ្រប់គ្រងទិន្នន័យ (Database) ---
if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame([
        {"ID": "JMI-001", "Name": "CHAN SOKHOEURN", "Level": "វិទ្យាល័យ", "Fee": 500, "Paid": "បង់រួច", "Date": "2026-03-25"}
    ])

# --- ៥. Sidebar ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>JMI EXECUTIVE</h2>", unsafe_allow_html=True)
    st.markdown("<center><h1 style='font-size:70px; margin:0;'>🛡️</h1></center>", unsafe_allow_html=True)
    st.markdown("---")
    pwd = st.text_input("Director's Key", type="password")
    
    if pwd == "JMI2026":
        menu = st.sidebar.radio("STRATEGIC MODULES", 
            ["📊 Dashboard", "🎓 Enrollment", "📔 Skill Passport", "📜 Certification", "💰 Financial Hub"])
    else:
        st.stop()

# --- MODULE 1: DASHBOARD ---
if menu == "📊 Dashboard":
    st.markdown("<h1 class='header-style'>JMI Strategic Command Center</h1>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Scholars", len(st.session_state.db))
    # គណនាចំណូលសរុប
    total_revenue = st.session_state.db[st.session_state.db['Paid'] == "បង់រួច"]['Fee'].sum()
    c2.metric("Total Revenue", f"${total_revenue:,.2f}")
    c3.metric("Year", "2026")
    st.dataframe(st.session_state.db, use_container_width=True)

# --- MODULE 2: ENROLLMENT ---
elif menu == "🎓 Enrollment":
    st.markdown("<h1 class='header-style'>Scholar Registration</h1>", unsafe_allow_html=True)
    with st.form("enroll"):
        name = st.text_input("ឈ្មោះសិស្ស (Full Name)")
        level = st.selectbox("កម្រិតសិក្សា", ["មត្តេយ្យ", "បឋម", "អនុវិទ្យាល័យ", "វិទ្យាល័យ"])
        fee = st.number_input("តម្លៃសិក្សា ($)", min_value=0, value=250)
        if st.form_submit_button("REGISTER NOW"):
            new_data = {"ID": f"JMI-{len(st.session_state.db)+1:03d}", "Name": name.upper(), "Level": level, "Fee": fee, "Paid": "មិនទាន់បង់", "Date": datetime.now().strftime("%Y-%m-%d")}
            st.session_state.db = pd.concat([st.session_state.db, pd.DataFrame([new_data])], ignore_index=True)
            st.success(f"ចុះឈ្មោះ {name} ជោគជ័យ!")

# --- MODULE 3: SKILL PASSPORT ---
elif menu == "📔 Skill Passport":
    st.markdown("<h1 class='header-style'>📔 Skill Mastery Passport</h1>", unsafe_allow_html=True)
    sel_student = st.selectbox("Select Student:", st.session_state.db['Name'].tolist())
    cols = st.columns(2)
    for i in range(1, 13):
        with cols[0 if i <= 6 else 1]:
            st.checkbox(f"មេរៀនទី {i}", key=f"L{i}_{sel_student}")

# --- MODULE 4: CERTIFICATION ---
elif menu == "📜 Certification":
    st.markdown("<h1 class='header-style'>Certification Generator</h1>", unsafe_allow_html=True)
    rec_name = st.selectbox("Select Recipient:", st.session_state.db['Name'].tolist())
    if st.button("GENERATE"):
        s = st.session_state.db[st.session_state.db['Name'] == rec_name].iloc[0]
        st.markdown(f"""<div style="background:white; padding:40px; border:15px solid #D4AF37; text-align:center; color:#001529 !important;">
            <h1 style="color:#D4AF37 !important;">JUNIOR MEDICAL INSTITUTE</h1>
            <h2 style="color:#B8860B !important;">{s['Name']}</h2>
            <p style="color:#001529 !important;">Completed: {s['Level']}</p>
            <hr><p style="color:#001529 !important;">Dr. CHAN Sokhoeurn</p></div>""", unsafe_allow_html=True)

# --- MODULE 5: FINANCIAL HUB (បន្ថែមថ្មី) ---
elif menu == "💰 Financial Hub":
    st.markdown("<h1 class='header-style'>💰 Financial Management</h1>", unsafe_allow_html=True)
    
    # បង្ហាញស្ថិតិហិរញ្ញវត្ថុ
    f1, f2 = st.columns(2)
    paid_sum = st.session_state.db[st.session_state.db['Paid'] == "បង់រួច"]['Fee'].sum()
    unpaid_sum = st.session_state.db[st.session_state.db['Paid'] == "មិនទាន់បង់"]['Fee'].sum()
    
    with f1: st.markdown(f"<div class='finance-card'><h3>Received Income</h3><h1>${paid_sum:,.2f}</h1></div>", unsafe_allow_html=True)
    with f2: st.markdown(f"<div class='finance-card'><h3>Pending Balance</h3><h1>${unpaid_sum:,.2f}</h1></div>", unsafe_allow_html=True)
    
    st.markdown("### 📝 Update Payment Status")
    edited_finance = st.data_editor(st.session_state.db[["ID", "Name", "Fee", "Paid"]], use_container_width=True)
    
    if st.button("💾 Save Financial Updates"):
        st.session_state.db.update(edited_df)
        st.success("ស្ថានភាពហិរញ្ញវត្ថុត្រូវបានធ្វើបច្ចុប្បន្នភាព!")

    # បោះពុម្ពវិក្កយបត្រ
    st.markdown("---")
    st.markdown("### 🧾 Print Receipt")
    target_student = st.selectbox("Select Student for Receipt:", st.session_state.db['Name'].tolist())
    if st.button("PRINT RECEIPT"):
        ts = st.session_state.db[st.session_state.db['Name'] == target_student].iloc[0]
        st.markdown(f"""
        <div style="background:#001529; padding:30px; border:2px dashed #D4AF37; border-radius:10px;">
            <h2 style="text-align:center;">OFFICIAL RECEIPT</h2>
            <p><b>Student:</b> {ts['Name']}</p>
            <p><b>Level:</b> {ts['Level']}</p>
            <p><b>Amount:</b> ${ts['Fee']}</p>
            <p><b>Status:</b> {ts['Paid']}</p>
            <p style="text-align:right;">Date: {ts['Date']}</p>
            <p style="text-align:center; font-size:12px;">Authorized by Dr. CHAN Sokhoeurn</p>
        </div>
        """, unsafe_allow_html=True)
