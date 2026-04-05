import streamlit as st
import pandas as pd
from datetime import datetime

# --- ១. ការកំណត់ទំព័រ និង Branding ---
st.set_page_config(page_title="JMI Management System", page_icon="🏥", layout="wide")

# បង្កើត Database បណ្តោះអាសន្ន (Session State)
if 'jmi_db' not in st.session_state:
    st.session_state.jmi_db = pd.DataFrame(columns=[
        "ID", "ឈ្មោះសិស្ស", "កម្រិត", "ជំនាញវេជ្ជសាស្ត្រ", "ពិន្ទុវាយតម្លៃ", "ស្ថានភាពបង់ប្រាក់"
    ])

# --- Side Bar សម្រាប់រដ្ឋបាល (Admin & Finance) ---
st.sidebar.image("https://via.placeholder.com/150?text=JMI+LOGO", width=100) # អ្នកអាចប្តូរ Link Logo ពិតប្រាកដ
st.sidebar.title("ផ្ទាំងគ្រប់គ្រង JMI")
menu = st.sidebar.selection_box("សូមជ្រើសរើសផ្នែក", 
    ["🏠 ទំព័រដើម", "📝 ចុះឈ្មោះសិស្ស", "📚 កម្មវិធីសិក្សា K-12", "🏆 Skill Passport", "💰 រដ្ឋបាល & ហិរញ្ញវត្ថុ"])

# --- ២. ផ្នែកចុះឈ្មោះសិស្ស (Student Management) ---
if menu == "📝 ចុះឈ្មោះសិស្ស":
    st.header("📝 ចុះឈ្មោះសិស្សថ្មីចូល JMI")
    with st.form("registration_form"):
        col1, col2 = st.columns(2)
        with col1:
            s_id = st.text_input("លេខសម្គាល់ (ID)")
            s_name = st.text_input("ឈ្មោះពេញសិស្ស")
        with col2:
            s_level = st.selectbox("កម្រិតសិក្សា (K-12)", ["Kindergarten", "Primary", "Secondary", "High School"])
            s_skill = st.text_input("ជំនាញគោល (ឧ. Anatomy Basics)")
        
        submit = st.form_submit_button("ចុះឈ្មោះ")
        if submit:
            new_entry = pd.DataFrame([[s_id, s_name, s_level, s_skill, 0, "មិនទាន់បង់"]], columns=st.session_state.jmi_db.columns)
            st.session_state.jmi_db = pd.concat([st.session_state.jmi_db, new_entry], ignore_index=True)
            st.success(f"បានចុះឈ្មោះ {s_name} រួចរាល់!")

# --- ៣. ផ្នែកកម្មវិធីសិក្សា (Academic & Curriculum) ---
elif menu == "📚 កម្មវិធីសិក្សា K-12":
    st.header("📚 កម្មវិធីសិក្សាវេជ្ជសាស្ត្រ (Bilingual)")
    tab1, tab2 = st.tabs(["មេរៀនមត្តេយ្យ/បឋម", "មេរៀនអនុ/វិទ្យាល័យ"])
    
    with tab1:
        st.write("### 🍼 Junior Doctor Foundation")
        st.info("មេរៀន៖ អាហារូបត្ថម្ភ និងកាយវិភាគសាស្ត្របឋម (Nutrition & Basic Anatomy)")
        st.video("https://www.youtube.com/watch?v=your_video_link") # អ្នកអាចដាក់ Link វីដេអូបង្រៀន
        
    with tab2:
        st.write("### 🔬 Clinical Pre-Med Basics")
        st.write("មេរៀន៖ ការវាស់សម្ពាធឈាម និងការសង្គ្រោះបឋម (Blood Pressure & First Aid)")

# --- ៤. ផ្នែកវាយតម្លៃ (Assessment & Skill Passport) ---
elif menu == "🏆 Skill Passport":
    st.header("🏆 វាយតម្លៃសមត្ថភាព និង Skill Passport")
    if not st.session_state.jmi_db.empty:
        selected_s = st.selectbox("ជ្រើសរើសឈ្មោះសិស្ស", st.session_state.jmi_db["ឈ្មោះសិស្ស"])
        score = st.slider("ផ្តល់ពិន្ទុការអនុវត្ត (0-100)", 0, 100, 50)
        
        if st.button("រក្សាទុកពិន្ទុ"):
            st.session_state.jmi_db.loc[st.session_state.jmi_db["ឈ្មោះសិស្ស"] == selected_s, "ពិន្ទុវាយតម្លៃ"] = score
            st.success(f"បានបញ្ចូលពិន្ទុ {score}% ជូន {selected_s}")
            
        st.table(st.session_state.jmi_db[st.session_state.jmi_db["ឈ្មោះសិស្ស"] == selected_s])
    else:
        st.warning("មិនទាន់មានទិន្នន័យសិស្សឡើយ!")

# --- ៥. ផ្នែករដ្ឋបាល និងហិរញ្ញវត្ថុ (Admin & Finance) ---
elif menu == "💰 រដ្ឋបាល & ហិរញ្ញវត្ថុ":
    st.header("💰 ការគ្រប់គ្រងការបង់ប្រថ្លៃសិក្សា")
    st.dataframe(st.session_state.jmi_db[["ID", "ឈ្មោះសិស្ស", "កម្រិត", "ស្ថានភាពបង់ប្រាក់"]])
    
    st.write("---")
    st.subheader("📢 ទំនាក់ទំនងមាតាបិតា (Communication)")
    st.text_area("សរសេរសារផ្ញើទៅកាន់អាណាព្យាបាល:", "សូមជម្រាបសួរ លោក/លោកស្រី... កូនរបស់លោកអ្នកបានសម្រេចជំនាញថ្មី...")
    if st.button("ផ្ញើសារ (Mockup)"):
        st.info("សារត្រូវបានរៀបចំរួចរាល់សម្រាប់ផ្ញើតាម Telegram/Email")

# --- ទំព័រដើម (Dashboard) ---
else:
    st.header("📊 ទំព័រដើម - JMI Overview")
    col1, col2, col3 = st.columns(3)
    col1.metric("សិស្សសរុប", len(st.session_state.jmi_db))
    col2.metric("សិស្សបានបង់ប្រាក់", "0")
    col3.metric("កម្មវិធីសិក្សាសកម្ម", "K-12")
    
    st.write("### 📋 បញ្ជីឈ្មោះសិស្សសរុប")
    st.dataframe(st.session_state.jmi_db, use_container_width=True)
