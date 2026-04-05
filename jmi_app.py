import streamlit as st
import pandas as pd
from datetime import datetime
import os
import base64

# --- 1. Page Configuration ---
st.set_page_config(page_title="JMI | Strategic Management Portal", page_icon="🛡️", layout="wide")

# --- 2. UI Styling (Golden Luxury Theme) ---
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600&family=Inter:wght@400;700&display=swap" rel="stylesheet">
<style>
    .stApp { background: radial-gradient(circle, #002d5a 0%, #001529 100%); }
    html, body, [data-testid="stWidgetLabel"], .stMarkdown, p, span, label, li, div, h1, h2, h3, .stMetric, [data-testid="stHeader"] {
        color: #D4AF37 !important; font-family: 'Inter', 'Cinzel', sans-serif;
    }
    [data-testid="stSidebar"] { background-color: #001529 !important; border-right: 1px solid rgba(212,175,55,0.4); }
    .stButton>button { 
        background: linear-gradient(135deg, #D4AF37 0%, #B8860B 100%) !important;
        color: #001529 !important; border-radius: 8px !important; font-weight: 700 !important; border: none !important;
    }
    .header-style { border-left: 5px solid #D4AF37; padding-left: 15px; margin-bottom: 20px; }
</style>
""", unsafe_allow_html=True)

# --- 3. Database Management ---
if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame([
        {"ID": "JMI-001", "Name": "CHAN SOKHOEURN", "Level": "HIGH SCHOOL", "Fee": 500.0, "Paid": "PAID", "Date": "2026-03-25"}
    ])

# --- 4. Helper Function for Image ---
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

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
        choice = st.sidebar.radio("STRATEGIC MODULES", 
            ["Dashboard", "Enrollment", "Skill Passport", "Certification", "Financial Hub"])
    else:
        st.warning("🔒 SECURE ACCESS ONLY")
        st.stop()

# --- MODULE 4: CERTIFICATION (មានប្រអប់សរសេរឈ្មោះអ្នកចុះហត្ថលេខា) ---
if choice == "Certification":
    st.markdown("<h1 class='header-style'>Official Certification Hub</h1>", unsafe_allow_html=True)
    
    if not st.session_state.db.empty:
        # បន្ថែមផ្នែកកំណត់ឈ្មោះអ្នកចុះហត្ថលេខា
        st.markdown("### 🖋️ Signature Settings")
        col_sig1, col_sig2 = st.columns(2)
        with col_sig1:
            director_name = st.text_input("Director's Name", value="DR. CHAMNAN VICHET")
            director_title = st.text_input("Director's Title", value="Director, JMI International")
        with col_sig2:
            instructor_name = st.text_input("Senior Instructor's Name", value="DR. MEA LINA")
            instructor_title = st.text_input("Instructor's Title", value="Senior Instructor")
            
        st.markdown("---")
        
        # ជ្រើសរើសសិស្ស
        rec = st.selectbox("Select Student Name", st.session_state.db['Name'].tolist())
        
        if st.button("GENERATE LUXURY CERTIFICATE"):
            s = st.session_state.db[st.session_state.db['Name'] == rec].iloc[0]
            
            # កំណត់ស្ទីលទៅតាមកម្រិត
            cert_styles = {
                "KINDERGARTEN": {"title": "CERTIFICATE OF PREPARATION", "color": "#2E7D32", "grades": "Ages 4-6"},
                "PRIMARY SCHOOL": {"title": "CERTIFICATE OF ACHIEVEMENT", "color": "#1565C0", "grades": "Grades 1-5"},
                "JUNIOR HIGH SCHOOL": {"title": "DIPLOMA OF COMPLETION", "color": "#C62828", "grades": "Grades 6-8"},
                "HIGH SCHOOL": {"title": "DIPLOMA OF ACADEMIC EXCELLENCE", "color": "#6A1B9A", "grades": "Grades 9-12"}
            }
            style = cert_styles.get(s['Level'], cert_styles["HIGH SCHOOL"])
            logo_img = f'<img src="data:image/png;base64,{logo_base64}" width="100">' if logo_base64 else '🛡️'

            st.markdown(f"""
            <div style="background:white; padding:40px; border:15px double {style['color']}; color:#333; text-align:center; font-family:'Inter';">
                <div style="border:2px solid #D4AF37; padding:20px;">
                    <div style="margin-bottom:15px;">{logo_img}</div>
                    <h3 style="margin:0; font-family:'Cinzel';">JUNIOR MEDICAL INSTITUTE</h3>
                    <p style="margin:0; color:{style['color']};">({style['grades']})</p>
                    <h1 style="font-family:'Cinzel'; color:{style['color']}; font-size:35px; margin:20px 0;">{style['title']}</h1>
                    <p>This is to certify that</p>
                    <h2 style="font-size:40px; border-bottom:2px solid #D4AF37; display:inline-block; padding:0 30px;">{s['Name']}</h2>
                    <p style="margin-top:15px;">successfully completed the esteemed <b>{s['Level']}</b> program</p>
                    <h2 style="color:#B8860B; font-family:'Cinzel';">LITTLE MEDIC</h2>
                    <p style="font-size:12px;">Phnom Penh, Cambodia | {s['Date']}</p>
                    
                    <div style="display:flex; justify-content:space-around; margin-top:40px;">
                        <div style="text-align: center; border-top:1px solid #333; width:200px;">
                            <br><b>{director_name}</b><br><small>{director_title}</small>
                        </div>
                        <div style="text-align: center;">
                            <img src="https://api.qrserver.com/v1/create-qr-code/?size=60x60&data={s['ID']}" width="60">
                            <br><small style="font-size:8px;">Scan to Verify</small>
                        </div>
                        <div style="text-align: center; border-top:1px solid #333; width:200px;">
                            <br><b>{instructor_name}</b><br><small>{instructor_title}</small>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# --- MODULE 1, 2, 3, 5 ( Dashboard, Enrollment, Passport, Finance ) នៅរក្សាទុកដដែល ---
elif choice == "Dashboard":
    st.markdown("<h1 class='header-style'>JMI Strategic Analytics</h1>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Scholars", len(st.session_state.db))
    c2.metric("Total Revenue", f"${st.session_state.db['Fee'].sum():,.2f}")
    c3.metric("Academic Year", "2026")
    st.dataframe(st.session_state.db, use_container_width=True)

elif choice == "Enrollment":
    st.markdown("<h1 class='header-style'>Scholar Registration</h1>", unsafe_allow_html=True)
    with st.form("reg_form"):
        n = st.text_input("Scholar Name")
        l = st.selectbox("Level", ["KINDERGARTEN", "PRIMARY SCHOOL", "JUNIOR HIGH SCHOOL", "HIGH SCHOOL"])
        f = st.number_input("Fee ($)", value=250.0)
        p = st.radio("Status", ["PAID", "UNPAID"], horizontal=True)
        if st.form_submit_button("REGISTER"):
            new_id = f"JMI-{len(st.session_state.db)+1:03d}"
            new_data = {"ID": new_id, "Name": n.upper(), "Level": l, "Fee": f, "Paid": p, "Date": datetime.now().strftime("%Y-%m-%d")}
            st.session_state.db = pd.concat([st.session_state.db, pd.DataFrame([new_data])], ignore_index=True)
            st.success("Success!")

elif choice == "Skill Passport":
    st.markdown("<h1 class='header-style'>Skill Mastery Passport</h1>", unsafe_allow_html=True)
    if not st.session_state.db.empty:
        sel = st.selectbox("Select Student", st.session_state.db['Name'].tolist())
        def sync():
            for i in range(1, 13): st.session_state[f"L{i}_{sel}"] = st.session_state[f"m_{sel}"]
        st.checkbox("Check all Lesson", key=f"m_{sel}", on_change=sync)
        c1, c2 = st.columns(2)
        for i in range(1, 13):
            with c1 if i<=6 else c2: st.checkbox(f"Medical Module {i}", key=f"L{i}_{sel}")

elif choice == "Financial Hub":
    st.markdown("<h1 class='header-style'>Financial Management</h1>", unsafe_allow_html=True)
    st.data_editor(st.session_state.db, use_container_width=True)
