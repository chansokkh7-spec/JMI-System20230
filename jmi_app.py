import streamlit as st
import pandas as pd
from datetime import datetime
import os
import base64

# --- 1. Page Configuration ---
st.set_page_config(page_title="JMI | Strategic Management Portal", page_icon="🛡️", layout="wide")

# --- 2. Database Management ---
if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame([
        {"ID": "JMI-001", "Name": "CHAN SOKHOEURN", "Level": "HIGH SCHOOL", "Fee": 500.0, "Paid": "PAID", "Date": "2026-03-25"}
    ])

# --- 3. Helper Function for Image ---
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return ""

# --- 4. Sidebar Navigation ---
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
        choice = st.radio("STRATEGIC MODULES", ["Dashboard", "Enrollment", "Skill Passport", "Certification", "Financial Hub"])
    else:
        st.warning("🔒 SECURE ACCESS ONLY")
        st.stop()

# --- MODULE 4: CERTIFICATION ---
if choice == "Certification":
    st.title("📜 Official Certification Hub")
    
    if not st.session_state.db.empty:
        st.subheader("🖋️ Signature Settings")
        
        # ផ្នែកនេះទុកសម្រាប់ប្តូរតែឈ្មោះគ្រូបង្គោលប៉ុណ្ណោះ ព្រោះឈ្មោះ Director ថេរ
        col_sig = st.columns(2)
        with col_sig[0]:
            st.info("Director: **DR. CHAN SOKHOEURN**") # បង្ហាញឱ្យដឹងថាឈ្មោះ Director ត្រូវបានកំណត់រួចរាល់
        with col_sig[1]:
            ins_name = st.text_input("Instructor Name", value="DR. MEA LINA")
            ins_title = st.text_input("Instructor Title", value="Senior Instructor")
            
        st.markdown("---")
        rec = st.selectbox("Select Student Name", st.session_state.db['Name'].tolist())
        
        if st.button("GENERATE LUXURY CERTIFICATE"):
            s = st.session_state.db[st.session_state.db['Name'] == rec].iloc[0]
            
            # កំណត់ស្ទីលតាមកម្រិត
            cert_styles = {
                "KINDERGARTEN": {"title": "CERTIFICATE OF PREPARATION", "color": "#2E7D32", "grades": "Ages 4-6"},
                "PRIMARY SCHOOL": {"title": "CERTIFICATE OF ACHIEVEMENT", "color": "#1565C0", "grades": "Grades 1-5"},
                "JUNIOR HIGH SCHOOL": {"title": "DIPLOMA OF COMPLETION", "color": "#C62828", "grades": "Grades 6-8"},
                "HIGH SCHOOL": {"title": "DIPLOMA OF ACADEMIC EXCELLENCE", "color": "#6A1B9A", "grades": "Grades 9-12"}
            }
            style = cert_styles.get(s['Level'], cert_styles["HIGH SCHOOL"])
            logo_img = f'<img src="data:image/png;base64,{logo_base64}" width="100">' if logo_base64 else '🛡️'

            # ឈ្មោះ Director កំណត់ផ្ទាល់ក្នុងកូដ HTML តែម្តង
            html_code = f"""
            <div style="background:white; padding:30px; border:15px double {style['color']}; color:#333; text-align:center; font-family:Arial, sans-serif;">
                <div style="border:2px solid #D4AF37; padding:20px;">
                    <div style="margin-bottom:15px;">{logo_img}</div>
                    <h3 style="margin:0; color:#002d5a;">JUNIOR MEDICAL INSTITUTE</h3>
                    <p style="margin:0; color:{style['color']};">({style['grades']})</p>
                    <h1 style="color:{style['color']}; font-size:32px; margin:15px 0;">{style['title']}</h1>
                    <p>This is to certify that</p>
                    <h2 style="font-size:38px; border-bottom:2px solid #D4AF37; display:inline-block; padding:0 30px; color:#002d5a;">{s['Name']}</h2>
                    <p style="margin-top:10px;">successfully completed the <b>{s['Level']}</b> program</p>
                    <h2 style="color:#B8860B;">LITTLE MEDIC</h2>
                    <p style="font-size:12px;">Phnom Penh, Cambodia | {s['Date']}</p>
                    
                    <div style="display:flex; justify-content:space-around; margin-top:30px; align-items: flex-end;">
                        <div style="text-align:center; border-top:1px solid #333; width:180px;">
                            <br><b>DR. CHAN SOKHOEURN</b><br><small style="font-size:10px;">Director, JMI International</small>
                        </div>
                        
                        <div style="text-align:center;">
                            <img src="https://api.qrserver.com/v1/create-qr-code/?size=60x60&data={s['ID']}" width="60">
                        </div>
                        
                        <div style="text-align:center; border-top:1px solid #333; width:180px;">
                            <br><b>{ins_name}</b><br><small style="font-size:10px;">{ins_title}</small>
                        </div>
                    </div>
                </div>
            </div>
            """
            st.components.v1.html(html_code, height=650, scrolling=True)

# --- ផ្នែកផ្សេងៗ Dashboard, Enrollment, Financial Hub នៅរក្សាទុកដដែល ---
elif choice == "Dashboard":
    st.title("📊 JMI Strategic Analytics")
    st.dataframe(st.session_state.db, use_container_width=True)

elif choice == "Enrollment":
    st.title("📝 Scholar Registration")
    with st.form("reg"):
        n = st.text_input("Scholar Name")
        l = st.selectbox("Level", ["KINDERGARTEN", "PRIMARY SCHOOL", "JUNIOR HIGH SCHOOL", "HIGH SCHOOL"])
        if st.form_submit_button("REGISTER"):
            new = {"ID": f"JMI-{len(st.session_state.db)+1:03d}", "Name": n.upper(), "Level": l, "Fee": 250.0, "Paid": "PAID", "Date": datetime.now().strftime("%Y-%m-%d")}
            st.session_state.db = pd.concat([st.session_state.db, pd.DataFrame([new])], ignore_index=True)
            st.success("Registration Successful!")

elif choice == "Financial Hub":
    st.title("💰 Financial Hub")
    st.data_editor(st.session_state.db, use_container_width=True)
