import streamlit as st
import pandas as pd
from datetime import datetime
import os
import base64
import plotly.express as px

# --- 1. Page Configuration ---
st.set_page_config(page_title="JMI | Strategic Management Portal", page_icon="🛡️", layout="wide")

# --- 2. Luxury UI Styling (Deep Blue & Gold) ---
st.markdown("""
<style>
    /* ផ្ទៃខាងក្រោយកម្មវិធី */
    .stApp { 
        background: radial-gradient(circle, #002d5a 0%, #001529 100%); 
    }
    /* Sidebar Styling */
    [data-testid="stSidebar"] { 
        background-color: #001529 !important; 
        border-right: 2px solid #D4AF37; 
    }
    /* អក្សរពណ៌មាស */
    html, body, [data-testid="stWidgetLabel"], .stMarkdown, p, span, label, h1, h2, h3, .stMetric {
        color: #D4AF37 !important;
        font-family: 'Inter', sans-serif;
    }
    /* ប៊ូតុង Luxury Gold */
    .stButton>button { 
        background: linear-gradient(135deg, #D4AF37 0%, #B8860B 100%) !important;
        color: #001529 !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        border: none !important;
        box-shadow: 0px 4px 15px rgba(212, 175, 55, 0.3);
    }
    /* Metric Value ពណ៌សឱ្យងាយមើល */
    [data-testid="stMetricValue"] { color: #FFFFFF !important; }
</style>
""", unsafe_allow_html=True)

# --- 3. Database Management ---
if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame([
        {"ID": "JMI-001", "Name": "CHAN SOKHOEURN", "Level": "HIGH SCHOOL", "Fee": 500.0, "Paid": "PAID", "Date": "2026-03-25"},
        {"ID": "JMI-002", "Name": "SOK SAMBATH", "Level": "PRIMARY SCHOOL", "Fee": 250.0, "Paid": "PAID", "Date": "2026-03-26"},
        {"ID": "JMI-003", "Name": "MEA LINA", "Level": "KINDERGARTEN", "Fee": 200.0, "Paid": "UNPAID", "Date": "2026-03-27"}
    ])

# --- 4. Helper Function for Image ---
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return ""

# --- 5. Sidebar Navigation ---
with st.sidebar:
    logo_base64 = get_base64_image("logo.png")
    if logo_base64:
        st.markdown(f'<center><img src="data:image/png;base64,{logo_base64}" width="150"></center>', unsafe_allow_html=True)
    else:
        st.markdown("<center><h1 style='font-size:70px; margin:0;'>🛡️</h1></center>", unsafe_allow_html=True)
    
    st.markdown("<h2 style='text-align: center;'>JMI EXECUTIVE</h2>", unsafe_allow_html=True)
    st.markdown("---")
    pwd = st.text_input("Director's Key", type="password")
    
    if pwd == "JMI2026":
        choice = st.radio("STRATEGIC MODULES", ["Dashboard", "Enrollment", "Certification", "Financial Hub"])
    else:
        st.warning("🔒 SECURE ACCESS ONLY")
        st.stop()

# --- MODULE 1: DASHBOARD ---
if choice == "Dashboard":
    st.markdown("<h1>📊 JMI Strategic Analytics</h1>", unsafe_allow_html=True)
    
    # Metrics
    total_students = len(st.session_state.db)
    total_revenue = st.session_state.db[st.session_state.db['Paid'] == 'PAID']['Fee'].sum()
    pending_fees = st.session_state.db[st.session_state.db['Paid'] == 'UNPAID']['Fee'].sum()
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Scholars", f"{total_students}")
    m2.metric("Total Revenue", f"${total_revenue:,.2f}")
    m3.metric("Pending Fees", f"${pending_fees:,.2f}")
    
    st.markdown("---")
    
    # Charts
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("🎓 Enrollment by Level")
        fig_pie = px.pie(st.session_state.db, names='Level', 
                         color_discrete_sequence=px.colors.sequential.Gold_r, hole=0.4)
        fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="#D4AF37")
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with c2:
        st.subheader("💵 Payment Analysis")
        fig_bar = px.bar(st.session_state.db, x='Paid', y='Fee', color='Paid',
                         color_discrete_map={'PAID': '#D4AF37', 'UNPAID': '#C62828'})
        fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#D4AF37")
        st.plotly_chart(fig_bar, use_container_width=True)

# --- MODULE 2: ENROLLMENT ---
elif choice == "Enrollment":
    st.markdown("<h1>📝 Scholar Registration</h1>", unsafe_allow_html=True)
    with st.form("reg"):
        n = st.text_input("Scholar Name")
        l = st.selectbox("Level", ["KINDERGARTEN", "PRIMARY SCHOOL", "JUNIOR HIGH SCHOOL", "HIGH SCHOOL"])
        f = st.number_input("Fee Amount ($)", value=250.0)
        p = st.selectbox("Payment Status", ["PAID", "UNPAID"])
        if st.form_submit_button("REGISTER"):
            new = {"ID": f"JMI-{len(st.session_state.db)+1:03d}", "Name": n.upper(), "Level": l, "Fee": f, "Paid": p, "Date": datetime.now().strftime("%Y-%m-%d")}
            st.session_state.db = pd.concat([st.session_state.db, pd.DataFrame([new])], ignore_index=True)
            st.success("Registration Successful!")

# --- MODULE 3: CERTIFICATION ---
elif choice == "Certification":
    st.markdown("<h1>📜 Official Certification Hub</h1>", unsafe_allow_html=True)
    if not st.session_state.db.empty:
        st.subheader("🖋️ Signature Settings")
        col_sig = st.columns(2)
        with col_sig[0]:
            st.success("Director: **DR. CHAN SOKHOEURN**")
        with col_sig[1]:
            ins_name = st.text_input("Instructor Name", value="DR. MEA LINA")
            ins_title = st.text_input("Instructor Title", value="Senior Instructor")
            
        st.markdown("---")
        rec = st.selectbox("Select Student Name", st.session_state.db['Name'].tolist())
        
        if st.button("GENERATE LUXURY CERTIFICATE"):
            s = st.session_state.db[st.session_state.db['Name'] == rec].iloc[0]
            cert_styles = {
                "KINDERGARTEN": {"title": "CERTIFICATE OF PREPARATION", "color": "#2E7D32", "grades": "Ages 4-6"},
                "PRIMARY SCHOOL": {"title": "CERTIFICATE OF ACHIEVEMENT", "color": "#1565C0", "grades": "Grades 1-5"},
                "JUNIOR HIGH SCHOOL": {"title": "DIPLOMA OF COMPLETION", "color": "#C62828", "grades": "Grades 6-8"},
                "HIGH SCHOOL": {"title": "DIPLOMA OF ACADEMIC EXCELLENCE", "color": "#6A1B9A", "grades": "Grades 9-12"}
            }
            style = cert_styles.get(s['Level'], cert_styles["HIGH SCHOOL"])
            
            html_code = f"""
            <div style="background:white; padding:40px; border:15px double {style['color']}; color:#333; text-align:center;">
                <div style="border:2px solid #D4AF37; padding:20px;">
                    <h3 style="margin:0; color:#002d5a;">JUNIOR MEDICAL INSTITUTE</h3>
                    <h1 style="color:{style['color']}; font-size:35px; margin:20px 0;">{style['title']}</h1>
                    <p style="color:#333 !important;">This is to certify that</p>
                    <h2 style="font-size:40px; border-bottom:2px solid #D4AF37; display:inline-block; color:#002d5a !important;">{s['Name']}</h2>
                    <p style="margin-top:15px; color:#333 !important;">successfully completed the <b>{s['Level']}</b> program</p>
                    <h2 style="color:#B8860B;">LITTLE MEDIC</h2>
                    <div style="display:flex; justify-content:space-around; margin-top:50px; align-items: flex-end;">
                        <div style="text-align:center; border-top:1px solid #333; width:200px; color:#333 !important;">
                            <br><b>DR. CHAN SOKHOEURN</b><br><small>Director, JMI International</small>
                        </div>
                        <div style="text-align:center;">
                            <img src="https://api.qrserver.com/v1/create-qr-code/?size=60x60&data={s['ID']}" width="60">
                        </div>
                        <div style="text-align:center; border-top:1px solid #333; width:200px; color:#333 !important;">
                            <br><b>{ins_name}</b><br><small>{ins_title}</small>
                        </div>
                    </div>
                </div>
            </div>
            """
            st.markdown(html_code, unsafe_allow_html=True)

# --- MODULE 4: FINANCIAL HUB ---
elif choice == "Financial Hub":
    st.markdown("<h1>💰 Financial Hub</h1>", unsafe_allow_html=True)
    st.data_editor(st.session_state.db, use_container_width=True)
