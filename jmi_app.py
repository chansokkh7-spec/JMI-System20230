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
    .stat-card { 
        background: rgba(212, 175, 55, 0.05); 
        border: 1px solid rgba(212, 175, 55, 0.3); 
        padding: 20px; 
        border-radius: 15px; 
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
</style>
""", unsafe_allow_html=True)

# --- ៤. ការគ្រប់គ្រងទិន្នន័យ (Database) ---
if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame([
        {"ID": "JMI-001", "Name": "CHAN SOKHOEURN", "Level": "វិទ្យាល័យ", "Fee": 500.0, "Paid": "បង់រួច", "Date": "2026-03-25"},
        {"ID": "JMI-002", "Name": "SOPHEAP RA", "Level": "បឋម", "Fee": 300.0, "Paid": "មិនទាន់បង់", "Date": "2026-04-01"}
    ])

# --- ៥. Sidebar ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>JMI EXECUTIVE</h2>", unsafe_allow_html=True)
    st.markdown("<center><h1 style='font-size:70px; margin:0;'>🛡️</h1></center>", unsafe_allow_html=True)
    st.markdown("---")
    pwd = st.text_input("Director's Key", type="password")
    if pwd == "JMI2026":
        menu = st.sidebar.radio("STRATEGIC MODULES", ["📊 Dashboard", "🎓 Enrollment", "📔 Skill Passport", "📜 Certification", "💰 Financial Hub"])
    else:
        st.stop()

# --- MODULE 1: DASHBOARD (កែលម្អថ្មី) ---
if menu == "📊 Dashboard":
    st.markdown("<h1 class='header-style'>JMI Strategic Analytics</h1>", unsafe_allow_html=True)
    
    # --- លេខសង្ខេប (Summary Cards) ---
    c1, c2, c3, c4 = st.columns(4)
    total_s = len(st.session_state.db)
    total_rev = st.session_state.db[st.session_state.db['Paid'] == "បង់រួច"]['Fee'].sum()
    pending_rev = st.session_state.db[st.session_state.db['Paid'] == "មិនទាន់បង់"]['Fee'].sum()
    
    with c1: st.markdown(f"<div class='stat-card'>📚<br><small>Total Scholars</small><h2>{total_s}</h2></div>", unsafe_allow_html=True)
    with c2: st.markdown(f"<div class='stat-card'>💰<br><small>Total Revenue</small><h2>${total_rev:,.0f}</h2></div>", unsafe_allow_html=True)
    with c3: st.markdown(f"<div class='stat-card'>⏳<br><small>Pending</small><h2>${pending_rev:,.0f}</h2></div>", unsafe_allow_html=True)
    with c4: st.markdown(f"<div class='stat-card'>🏛️<br><small>Academic Year</small><h2>2026</h2></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- ក្រាហ្វិក (Charts) ---
    if HAS_PLOTLY and not st.session_state.db.empty:
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.markdown("### 🎓 Student Levels (Pie Chart)")
            fig_pie = px.pie(st.session_state.db, names='Level', 
                             color_discrete_sequence=['#D4AF37', '#B8860B', '#8A6D3B', '#FFD700'],
                             hole=0.4)
            fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#D4AF37')
            st.plotly_chart(fig_pie, use_container_width=True)
            
        with col_right:
            st.markdown("### 💵 Payment Status (Bar Chart)")
            fig_bar = px.bar(st.session_state.db, x='Paid', y='Fee', color='Paid',
                             color_discrete_map={'បង់រួច': '#D4AF37', 'មិនទាន់បង់': '#3B5998'})
            fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#D4AF37')
            st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info("Install plotly to see advanced analytics.")

    st.markdown("### 📋 Student Master List")
    st.dataframe(st.session_state.db, use_container_width=True)

# --- MODULE ផ្សេងៗទៀត (រក្សាកូដដដែល) ---
elif menu == "🎓 Enrollment":
    st.markdown("<h1 class='header-style'>Scholar Registration</h1>", unsafe_allow_html=True)
    with st.form("enroll"):
        name = st.text_input("ឈ្មោះសិស្ស (Full Name)")
        level = st.selectbox("កម្រិតសិក្សា", ["មត្តេយ្យ", "បឋម", "អនុវិទ្យាល័យ", "វិទ្យាល័យ"])
        fee = st.number_input("តម្លៃសិក្សា ($)", min_value=0.0, value=250.0)
        if st.form_submit_button("REGISTER NOW"):
            new_id = f"JMI-{len(st.session_state.db)+1:03d}"
            new_data = pd.DataFrame([{"ID": new_id, "Name": name.upper(), "Level": level, "Fee": fee, "Paid": "មិនទាន់បង់", "Date": datetime.now().strftime("%Y-%m-%d")}])
            st.session_state.db = pd.concat([st.session_state.db, new_data], ignore_index=True)
            st.success(f"ចុះឈ្មោះ {name} ជោគជ័យ!")

elif menu == "📔 Skill Passport":
    st.markdown("<h1 class='header-style'>📔 Skill Mastery Passport</h1>", unsafe_allow_html=True)
    if not st.session_state.db.empty:
        sel_student = st.selectbox("Select Student:", st.session_state.db['Name'].tolist())
        cols = st.columns(2)
        for i in range(1, 13):
            with cols[0 if i <= 6 else 1]:
                st.checkbox(f"មេរៀនទី {i}", key=f"L{i}_{sel_student}")

elif menu == "📜 Certification":
    st.markdown("<h1 class='header-style'>Certification Generator</h1>", unsafe_allow_html=True)
    if not st.session_state.db.empty:
        rec_name = st.selectbox("Select Recipient:", st.session_state.db['Name'].tolist())
        if st.button("GENERATE"):
            s = st.session_state.db[st.session_state.db['Name'] == rec_name].iloc[0]
            st.markdown(f"""<div style="background:white; padding:40px; border:15px solid #D4AF37; text-align:center;">
                <h1 style="color:#D4AF37 !important;">JUNIOR MEDICAL INSTITUTE</h1>
                <h2 style="color:#B8860B !important;">{s['Name']}</h2>
                <p style="color:#001529 !important;">Completed: {s['Level']}</p>
                <hr><p style="color:#001529 !important;">Dr. CHAN Sokhoeurn</p></div>""", unsafe_allow_html=True)

elif menu == "💰 Financial Hub":
    st.markdown("<h1 class='header-style'>💰 Financial Management</h1>", unsafe_allow_html=True)
    edited_finance = st.data_editor(st.session_state.db, use_container_width=True)
    if st.button("💾 Save Financial Updates"):
        st.session_state.db = edited_finance
        st.success("ស្ថានភាពហិរញ្ញវត្ថុត្រូវបានធ្វើបច្ចុប្បន្នភាព!")
