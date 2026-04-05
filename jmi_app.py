import streamlit as st
import os
import base64

# --- មុខងារសម្រាប់ទាញរូបភាព Logo ---
def get_base64_logo(file_path):
    # បញ្ជាក់៖ លោកគ្រូត្រូវដាក់ File រូបភាពឈ្មោះ logo.png ក្នុង Folder ជាមួយកូដ Python នេះ
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return None

# --- ការបង្ហាញក្នុង Sidebar ---
with st.sidebar:
    logo_data = get_base64_logo("logo.png") # ត្រួតពិនិត្យរក File ឈ្មោះ logo.png
    
    if logo_data:
        # បង្ហាញ Logo បើរកឃើញ File
        st.markdown(f"""
            <div style="text-align: center;">
                <img src="data:image/png;base64,{logo_data}" width="150" style="margin-bottom: 10px;">
            </div>
        """, unsafe_allow_html=True)
    else:
        # បង្ហាញរូបសញ្ញាការពារ 🛡️ បើបាត់ File រូបភាព
        st.markdown("<center><h1 style='font-size:80px; color:#D4AF37; margin:0;'>🛡️</h1></center>", unsafe_allow_html=True)
    
    st.markdown("<h2 style='text-align: center; color:#D4AF37;'>JMI EXECUTIVE</h2>", unsafe_allow_html=True)
    st.markdown("---")
