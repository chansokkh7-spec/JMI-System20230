import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- 1. Library Error Prevention ---
try:
    import plotly.express as px
    HAS_PLOTLY = True
except ImportError:
    HAS_PLOTLY = False

# --- 2. Page Configuration ---
st.set_page_config(page_title="JMI | Strategic Management Portal", page_icon="🛡️", layout="wide")

# --- 3. UI Styling (Golden Luxury Theme) ---
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600&family=Inter:wght@400;700&display=swap" rel="stylesheet">
<style>
    .stApp { background: radial-gradient(circle, #002d5a 0%, #001529 100%); }
    html, body, [data-testid="stWidgetLabel"], .stMarkdown, p, span, label, li, div, h1, h2, h3, .stMetric, [data-testid="stHeader"] {
        color: #D4AF37 !important;
        font-family: 'Inter', 'Cinzel', sans-serif;
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

# --- 4. Database Management ---
if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame([
        {"ID": "JMI-001", "Name": "CHAN SOKHOEURN", "Level": "HIGH SCHOOL", "Fee": 500.0, "Paid": "PAID", "Date": "2026-03-25"}
    ])

# --- 5. Sidebar Navigation ---
with st.sidebar:
    if os.path.exists("logo.png"):
        st.image("logo.png", use_container_width=True)
    else:
        st.markdown("<center><h1 style='font-size:70px; margin:0;'>🛡️</h1></center>", unsafe_allow_html=True)
    
    st.markdown("<h2 style='text-align: center;'>JMI EXECUTIVE</h2>", unsafe_allow_html=True)
    st.markdown("---")
    pwd = st.text_input("Director's Key", type="password")
    
    if pwd == "JMI2026":
        # ប្រើឈ្មោះ Menu ដោយមិនប្រើ Emoji ក្នុង String ដើម្បីការពារ Syntax Error លើ Server ខ្លះ
        choice = st.sidebar.radio("STRATEGIC MODULES", 
            ["Dashboard", "Enrollment", "Skill Passport", "Certification", "Financial Hub"])
    else:
        st.warning("🔒 SECURE ACCESS ONLY")
        st.stop()

# --- MODULE 1: DASHBOARD ---
if choice == "Dashboard":
    st.markdown("<h1 class='header-style'>JMI Strategic Analytics</h1>", unsafe_allow_html=True)
    
    c1, c2, c3, c4 = st.columns(4)
    total_s = len(st.session_state.db)
    total_rev = st.session_state.db[st.session_state.db['Paid'] == "PAID"]['Fee'].sum()
    pending_rev = st.session_state.db[st.session_state.db['Paid'] == "UNPAID"]['Fee'].sum()
    
    with c1: st.markdown(f"<div class='stat-card'>📚<br><small>Total Scholars</small><h2>{total_s}</h2></div>", unsafe_allow_html=True)
    with c2: st.markdown(f"<div class='stat-card'>💰<br><small>Total Revenue</small><h2>${total_rev:,.0f}</h2></div>", unsafe_allow_html=True)
    with c3: st.markdown(f"<div class='stat-card'>⏳<br><small>Pending</small><h2>${pending_rev:,.0f}</h2></div>", unsafe_allow_html=True)
    with c4: st.markdown(f"<div class='stat-card'>🏛️<br><small>Academic Year</small><h2>2026</h2></div>", unsafe_allow_html=True)

    if HAS_PLOTLY and not st.session_state.db.empty:
        col_left, col_right = st.columns(2)
        with col_left:
            fig_pie = px.pie(st.session_state.db, names='Level', hole=0.4, color_discrete_sequence=['#D4AF37', '#B8860B'])
            fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color='#D4AF37')
            st.plotly_chart(fig_pie, use_container_width=True)
        with col_right:
            fig_bar = px.bar(st.session_state.db, x='Paid', y='Fee', color='Paid', color_discrete_map={'PAID': '#D4AF37', 'UNPAID': '#3B5998'})
            fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color='#D4AF37')
            st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("### 📋 Student Master List")
    st.dataframe(st.session_state.db, use_container_width=True)

# --- MODULE 2: ENROLLMENT & INVOICE ---
elif choice == "Enrollment":
    st.markdown("<h1 class='header-style'>Scholar Registration</h1>", unsafe_allow_html=True)
    col_reg, col_inv = st.columns([1, 1.2])
    
    with col_reg:
        with st.form("enroll_form"):
            name = st.text_input("Scholar Full Name")
            level = st.selectbox("Academic Level", ["KINDERGARTEN", "PRIMARY", "SECONDARY", "HIGH SCHOOL"])
            fee = st.number_input("Tuition Fee ($)", min_value=0.0, value=250.0)
            payment = st.radio("Payment Status", ["UNPAID", "PAID"], horizontal=True)
            if st.form_submit_button("REGISTER & GENERATE INVOICE"):
                if name:
                    new_id = f"JMI-{len(st.session_state.db)+1:03d}"
                    new_entry = {"ID": new_id, "Name": name.upper(), "Level": level, "Fee": fee, "Paid": payment, "Date": datetime.now().strftime("%Y-%m-%d %I:%M %p")}
                    st.session_state.db = pd.concat([st.session_state.db, pd.DataFrame([new_entry])], ignore_index=True)
                    st.session_state.last_inv = new_entry
                    st.success("Registration Successful!")
                else: st.error("Please enter name")

    with col_inv:
        if 'last_inv' in st.session_state:
            inv = st.session_state.last_inv
            st.markdown(f"""
            <div style="background:white; padding:25px; border-radius:10px; border-top:8px solid #D4AF37; color:#333 !important;">
                <h3 style="text-align:center; color:#002d5a !important; margin:0;">JUNIOR MEDICAL INSTITUTE</h3>
                <p style="text-align:center; font-size:10px; color:#666;">OFFICIAL RECEIPT</p>
                <hr>
                <small><b>Invoice:</b> {inv['ID']} | <b>Date:</b> {inv['Date']}</small><br>
                <small><b>Scholar:</b> {inv['Name']}</small><br>
                <small><b>Program:</b> {inv['Level']}</small>
                <div style="background:#f9f9f9; padding:10px; margin-top:10px; border-radius:5px;">
                    <h4 style="margin:0; color:#002d5a;">Total Paid: <span style="float:right; color:#D4AF37;">${inv['Fee']:,.2f}</span></h4>
                    <p style="font-size:12px; margin:0; color:{'green' if inv['Paid']=='PAID' else 'red'};">Status: {inv['Paid']}</p>
                </div>
                <p style="font-size:10px; margin-top:15px; text-align:center;"><i>Authorized by Dr. CHAN Sokhoeurn</i></p>
            </div>
            """, unsafe_allow_html=True)

# --- MODULE 3: SKILL PASSPORT ---
elif choice == "Skill Passport":
    st.markdown("<h1 class='header-style'>Skill Mastery Passport</h1>", unsafe_allow_html=True)
    if not st.session_state.db.empty:
        sel_student = st.selectbox("Select Student:", st.session_state.db['Name'].tolist())
        def sync():
            for i in range(1, 13): st.session_state[f"L{i}_{sel_student}"] = st.session_state[f"m_{sel_student}"]
        
        st.checkbox("Check all Lessons", key=f"m_{sel_student}", on_change=sync)
        cols = st.columns(2)
        for i in range(1, 13):
            k = f"L{i}_{sel_student}"
            if k not in st.session_state: st.session_state[k] = False
            with cols[0 if i <= 6 else 1]: st.checkbox(f"Medical Module {i}", key=k)

# --- MODULE 4: CERTIFICATION (Luxury Design) ---
elif choice == "Certification":
    st.markdown("<h1 class='header-style'>Official Certification Hub</h1>", unsafe_allow_html=True)
    if not st.session_state.db.empty:
        rec_name = st.selectbox("Select Recipient:", st.session_state.db['Name'].tolist())
        if st.button("GENERATE LUXURY CERTIFICATE"):
            s = st.session_state.db[st.session_state.db['Name'] == rec_name].iloc[0]
            st.markdown(f"""
            <div style="background:#fdfdfd; padding:30px; border:12px double #002d5a; color:#002d5a; font-family:'Inter'; text-align:center;">
                <div style="border:2px solid #D4AF37; padding:20px;">
                    <h5 style="margin:0; letter-spacing:3px; color:#D4AF37;">JUNIOR MEDICAL INSTITUTE</h5>
                    <h1 style="font-family:'Cinzel'; font-size:28px; margin:15px 0;">CERTIFICATE OF COMPLETION</h1>
                    <p style="margin:0;">This is to certify that</p>
                    <h2 style="font-size:35px; border-bottom:2px solid #D4AF37; display:inline-block; padding:0 20px;">{s['Name']}</h2>
                    <p style="margin-top:10px;">has successfully completed the esteemed <b>{s['Level']}</b> program</p>
                    <h3 style="color:#D4AF37; font-family:'Cinzel';">LITTLE MEDIC</h3>
                    <div style="display:flex; justify-content:space-around; margin-top:30px; font-size:10px;">
                        <div style="border-top:1px solid #002d5a; width:150px;"><br><b>Academic Board</b></div>
                        <div><img src="https://api.qrserver.com/v1/create-qr-code/?size=50x50&data={s['ID']}" width="50"></div>
                        <div style="border-top:1px solid #002d5a; width:150px;"><br><b>Dr. CHAN Sokhoeurn</b><br>Director</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# --- MODULE 5: FINANCIAL HUB ---
elif choice == "Financial Hub":
    st.markdown("<h1 class='header-style'>Financial Management</h1>", unsafe_allow_html=True)
    edited = st.data_editor(st.session_state.db, use_container_width=True)
    if st.button("Save Updates"):
        st.session_state.db = edited
        st.success("Data Saved")
