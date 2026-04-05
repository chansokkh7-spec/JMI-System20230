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
        menu = st.sidebar.radio("STRATEGIC MODULES", 
            ["📊 Dashboard", "🎓 Enrollment", "📔 Skill Passport", "📜 Certification", "💰 Financial Hub"])
    else:
        st.warning("🔒 SECURE ACCESS ONLY: DIRECTOR LEVEL")
        st.stop()

# --- MODULE 1: DASHBOARD ---
if menu == "📊 Dashboard":
    st.markdown("<h1 class='header-style'>JMI Strategic Analytics</h1>", unsafe_allow_html=True)
    
    c1, c2, c3, c4 = st.columns(4)
    total_s = len(st.session_state.db)
    total_rev = st.session_state.db[st.session_state.db['Paid'] == "PAID"]['Fee'].sum()
    pending_rev = st.session_state.db[st.session_state.db['Paid'] == "UNPAID"]['Fee'].sum()
    
    with c1: st.markdown(f"<div class='stat-card'>📚<br><small>Total Scholars</small><h2>{total_s}</h2></div>", unsafe_allow_html=True)
    with c2: st.markdown(f"<div class='stat-card'>💰<br><small>Total Revenue</small><h2>${total_rev:,.0f}</h2></div>", unsafe_allow_html=True)
    with c3: st.markdown(f"<div class='stat-card'>⏳<br><small>Pending</small><h2>${pending_rev:,.0f}</h2></div>", unsafe_allow_html=True)
    with c4: st.markdown(f"<div class='stat-card'>🏛️<br><small>Academic Year</small><h2>2026</h2></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if HAS_PLOTLY and not st.session_state.db.empty:
        col_left, col_right = st.columns(2)
        with col_left:
            st.markdown("### 🎓 Student Levels")
            fig_pie = px.pie(st.session_state.db, names='Level', hole=0.4, 
                             color_discrete_sequence=['#D4AF37', '#B8860B', '#8A6D3B'])
            fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color='#D4AF37', showlegend=True)
            st.plotly_chart(fig_pie, use_container_width=True)
        with col_right:
            st.markdown("### 💵 Revenue Status")
            fig_bar = px.bar(st.session_state.db, x='Paid', y='Fee', color='Paid',
                             color_discrete_map={'PAID': '#D4AF37', 'UNPAID': '#3B5998'})
            fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color='#D4AF37')
            st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("### 📋 Student Master List")
    st.dataframe(st.session_state.db, use_container_width=True)

# --- MODULE 2: ENROLLMENT ---
elif menu == "🎓 Enrollment":
    st.markdown("<h1 class='header-style'>Scholar Registration</h1>", unsafe_allow_html=True)
    
    # ចែកអេក្រង់ជា ២ (ម្ខាងបំពេញ ម្ខាងបង្ហាញវិក្កយបត្រ)
    col_reg, col_inv = st.columns([1, 1.2])
    
    with col_reg:
        with st.form("enroll", clear_on_submit=False):
            name = st.text_input("Scholar Full Name")
            level = st.selectbox("Academic Level", ["KINDERGARTEN", "PRIMARY", "SECONDARY", "HIGH SCHOOL"])
            fee = st.number_input("Tuition Fee ($)", min_value=0.0, value=250.0)
            payment_now = st.radio("Initial Payment Status", ["UNPAID", "PAID"], horizontal=True)
            
            submitted = st.form_submit_button("REGISTER NOW & GENERATE INVOICE")
            
            if submitted:
                if name:
                    new_id = f"JMI-{len(st.session_state.db)+1:03d}"
                    new_entry = {
                        "ID": new_id, 
                        "Name": name.upper(), 
                        "Level": level, 
                        "Fee": fee, 
                        "Paid": payment_now, 
                        "Date": datetime.now().strftime("%Y-%m-%d %I:%M %p")
                    }
                    st.session_state.db = pd.concat([st.session_state.db, pd.DataFrame([new_entry])], ignore_index=True)
                    st.session_state.last_invoice = new_entry
                    st.success(f"SUCCESS: {name.upper()} REGISTERED")
                else:
                    st.error("REQUIRED: PLEASE ENTER FULL NAME")

    with col_inv:
        if 'last_invoice' in st.session_state:
            inv = st.session_state.last_invoice
            st.markdown(f"""
            <div style="background-color: white; padding: 30px; border-radius: 10px; border: 2px solid #D4AF37; color: #002d5a !important;">
                <div style="text-align: center; border-bottom: 2px solid #D4AF37; padding-bottom: 10px;">
                    <h2 style="color: #002d5a !important; font-family: 'Cinzel'; margin: 0;">JUNIOR MEDICAL INSTITUTE</h2>
                    <p style="color: #B8860B !important; font-weight: bold; margin: 5px 0;">OFFICIAL TUITION RECEIPT</p>
                </div>
                <div style="padding: 15px 0;">
                    <table style="width: 100%; font-family: 'Inter'; font-size: 14px; color: #333;">
                        <tr><td><b>Invoice No:</b></td><td style="text-align: right;">{inv['ID']}</td></tr>
                        <tr><td><b>Date:</b></td><td style="text-align: right;">{inv['Date']}</td></tr>
                        <tr><td><b>Scholar:</b></td><td style="text-align: right;">{inv['Name']}</td></tr>
                        <tr><td><b>Level:</b></td><td style="text-align: right;">{inv['Level']}</td></tr>
                    </table>
                </div>
                <div style="background-color: #f9f9f9; padding: 15px; border-radius: 5px; border-left: 5px solid #D4AF37;">
                    <table style="width: 100%; font-size: 18px; color: #333;">
                        <tr style="font-weight: bold;">
                            <td>TOTAL PAID:</td>
                            <td style="text-align: right; color: #D4AF37;">${inv['Fee']:,.2f}</td>
                        </tr>
                        <tr>
                            <td style="font-size: 12px;">Status:</td>
                            <td style="text-align: right; font-size: 12px; color: {'green' if inv['Paid'] == 'PAID' else 'red'};">
                                <b>{inv['Paid']}</b>
                            </td>
                        </tr>
                    </table>
                </div>
                <div style="margin-top: 30px; display: flex; justify-content: space-between; font-size: 11px; color: #666;">
                    <div style="text-align: center;">_________________<br>Customer</div>
                    <div style="text-align: center;"><b>Dr. CHAN Sokhoeurn</b><br>Director</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Close Invoice"):
                del st.session_state.last_invoice
                st.rerun()

# --- MODULE 3: SKILL PASSPORT ---
elif menu == "📔 Skill Passport":
    st.markdown("<h1 class='header-style'>📔 Skill Mastery Passport</h1>", unsafe_allow_html=True)
    if not st.session_state.db.empty:
        sel_student = st.selectbox("Select Student:", st.session_state.db['Name'].tolist())
        st.info(f"Scholar: {sel_student} | Level: {st.session_state.db[st.session_state.db['Name']==sel_student]['Level'].values[0]}")
        
        # មុខងារ Sync Toggle (Check/Uncheck All)
        def sync_lessons():
            state_val = st.session_state[f"master_{sel_student}"]
            for i in range(1, 13):
                st.session_state[f"L{i}_{sel_student}"] = state_val

        st.checkbox("✅ Check all Lesson", key=f"master_{sel_student}", on_change=sync_lessons)
        st.markdown("---")
        cols = st.columns(2)
        for i in range(1, 13):
            check_key = f"L{i}_{sel_student}"
            if check_key not in st.session_state: st.session_state[check_key] = False
            with cols[0 if i <= 6 else 1]:
                st.checkbox(f"Medical Competency Module {i}", key=check_key)
    else:
        st.warning("NO DATA FOUND: ENROLL STUDENTS FIRST")

# --- MODULE 4: CERTIFICATION ---
elif menu == "📜 Certification":
    st.markdown("<h1 class='header-style'>Official Certification Hub</h1>", unsafe_allow_html=True)
    if not st.session_state.db.empty:
        rec_name = st.selectbox("Select Recipient:", st.session_state.db['Name'].tolist())
        if st.button("GENERATE OFFICIAL CERTIFICATE"):
            s = st.session_state.db[st.session_state.db['Name'] == rec_name].iloc[0]
            st.markdown(f"""
                <div style="background:white; padding:50px; border:15px double #D4AF37; text-align:center; color:#001529 !important;">
                    <h1 style="color:#D4AF37 !important; font-family:'Cinzel'; margin:0;">JUNIOR MEDICAL INSTITUTE</h1>
                    <p style="letter-spacing:3px; font-weight:bold;">CERTIFICATE OF EXCELLENCE</p>
                    <br>
                    <p>This is to certify that</p>
                    <h2 style="color:#B8860B !important; font-size:45px; font-family:'Cinzel'; border-bottom: 2px solid #D4AF37; display:inline-block;">{s['Name']}</h2>
                    <br><br>
                    <p>Has successfully completed the medical curriculum for</p>
                    <h3 style="color:#002d5a !important;">LEVEL: {s['Level']}</h3>
                    <br><br>
                    <div style="display: flex; justify-content: space-around;">
                        <div>_________________________<br><b>Academic Board</b></div>
                        <div>_________________________<br><b>Dr. CHAN Sokhoeurn</b><br><small>Founder & Director</small></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

# --- MODULE 5: FINANCIAL HUB ---
elif menu == "💰 Financial Hub":
    st.markdown("<h1 class='header-style'>💰 Financial Management</h1>", unsafe_allow_html=True)
    edited_finance = st.data_editor(st.session_state.db, use_container_width=True)
    if st.button("💾 SAVE FINANCIAL UPDATES"):
        st.session_state.db = edited_finance
        st.success("FINANCIAL DATA SYNCHRONIZED")
