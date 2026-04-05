import streamlit as st
import pandas as pd

# --- ១. ការកំណត់ទំព័រ ---
st.set_page_config(page_title="JMI Management System", page_icon="🏥", layout="wide")

# បង្កើត Database បណ្តោះអាសន្ន
if 'jmi_db' not in st.session_state:
    st.session_state.jmi_db = pd.DataFrame(columns=["ID", "ឈ្មោះសិស្ស", "កម្រិត", "ជំនាញវេជ្ជសាស្ត្រ", "ពិន្ទុវាយតម្លៃ", "ស្ថានភាពបង់ប្រាក់"])

# បង្កើតកន្លែងផ្ទុកពិន្ទុមេរៀនទាំង ៩ (Grades Storage)
if 'jmi_grades' not in st.session_state:
    st.session_state.jmi_grades = {}

# --- ២. Sidebar Menu ---
st.sidebar.title("🏥 JMI Control Panel")
menu = st.sidebar.selectbox("សូមជ្រើសរើសផ្នែក", ["🏠 ទំព័រដើម", "📝 ចុះឈ្មោះសិស្ស", "📚 កម្មវិធីសិក្សា K-12", "🏆 Skill Passport", "💰 រដ្ឋបាល & ហិរញ្ញវត្ថុ"])

# --- ៣. មុខងារ Skill Passport (វាយតម្លៃមេរៀនទាំង ៩) ---
if menu == "🏆 Skill Passport":
    st.header("🏆 វាយតម្លៃសមត្ថភាពសិស្ស (៩ មេរៀន)")
    
    if not st.session_state.jmi_db.empty:
        # ១. ជ្រើសរើសសិស្ស
        student_list = st.session_state.jmi_db["ឈ្មោះសិស្ស"].tolist()
        selected_student = st.selectbox("សូមជ្រើសរើសឈ្មោះសិស្សដើម្បីដាក់ពិន្ទុ:", student_list)
        
        # រកមើលកម្រិតរបស់សិស្សនោះ
        student_info = st.session_state.jmi_db[st.session_state.jmi_db["ឈ្មោះសិស្ស"] == selected_student].iloc[0]
        st.info(f"សិស្ស៖ {selected_student} | កម្រិត៖ {student_info['កម្រិត']}")

        # ២. បង្កើតតារាងបញ្ចូលពិន្ទុសម្រាប់មេរៀនទាំង ៩
        st.write("### បញ្ចូលពិន្ទុតាមមេរៀន (០-១០០)")
        
        # បញ្ជីមេរៀន (ប្រើឈ្មោះរួម ឬតាមកម្រិត)
        lessons = [f"មេរៀនទី {i}" for i in range(1, 10)]
        
        # បង្កើត Form សម្រាប់បញ្ចូលពិន្ទុ
        with st.form("grading_form"):
            cols = st.columns(3)
            new_scores = {}
            
            for i, lesson in enumerate(lessons):
                # ទាញយកពិន្ទុចាស់ (បើមាន)
                current_val = 0
                if selected_student in st.session_state.jmi_grades:
                    current_val = st.session_state.jmi_grades[selected_student].get(lesson, 0)
                
                # បង្កើតកន្លែងបញ្ចូលពិន្ទុ
                new_scores[lesson] = cols[i % 3].number_input(lesson, min_value=0, max_value=100, value=int(current_val))
            
            save_btn = st.form_submit_button("រក្សាទុកពិន្ទុទាំងអស់")
            
            if save_btn:
                # រក្សាទុកចូលក្នុង Session State
                st.session_state.jmi_grades[selected_student] = new_scores
                
                # គណនាមធ្យមភាគដើម្បីដាក់ក្នុង Database រួម
                avg_score = sum(new_scores.values()) / 9
                st.session_state.jmi_db.loc[st.session_state.jmi_db["ឈ្មោះសិស្ស"] == selected_student, "ពិន្ទុវាយតម្លៃ"] = round(avg_score, 2)
                
                st.success(f"បានរក្សាទុកពិន្ទុសម្រាប់ {selected_student} រួចរាល់! មធ្យមភាគ៖ {round(avg_score, 2)}%")

        # ៣. បង្ហាញតារាងសង្ខេប Skill Passport (Progress Bar)
        st.write("---")
        st.subheader("📊 លទ្ធផល Skill Passport")
        if selected_student in st.session_state.jmi_grades:
            display_data = st.session_state.jmi_grades[selected_student]
            for lesson, score in display_data.items():
                col_l, col_r = st.columns([1, 4])
                col_l.write(lesson)
                col_r.progress(score / 100)
    else:
        st.warning("មិនទាន់មានទិន្នន័យសិស្សទេ។ សូមទៅកាន់ផ្នែក 'ចុះឈ្មោះសិស្ស' ជាមុនសិន!")

# --- ៤. រក្សាមុខងារផ្សេងៗ (Home, Registration, etc.) ---
elif menu == "🏠 ទំព័រដើម":
    st.header("📊 JMI Dashboard")
    st.dataframe(st.session_state.jmi_db)

elif menu == "📝 ចុះឈ្មោះសិស្ស":
    st.header("📝 ចុះឈ្មោះសិស្ស")
    with st.form("reg"):
        id_in = st.text_input("ID")
        name_in = st.text_input("ឈ្មោះ")
        lvl_in = st.selectbox("កម្រិត", ["Kindergarten", "Primary", "Secondary", "High School"])
        if st.form_submit_button("ចុះឈ្មោះ"):
            new_data = pd.DataFrame([[id_in, name_in, lvl_in, "", 0, "មិនទាន់បង់"]], columns=st.session_state.jmi_db.columns)
            st.session_state.jmi_db = pd.concat([st.session_state.jmi_db, new_data], ignore_index=True)
            st.success("ជោគជ័យ!")

elif menu == "📚 កម្មវិធីសិក្សា K-12":
    st.header("📚 កម្មវិធីសិក្សា JMI")
    st.write("មេរៀនទាំង ៩ សម្រាប់កម្រិតនីមួយៗ...")
    # (ដាក់កូដមេរៀនទាំង ៩ ដែលខ្ញុំឱ្យមុននេះបញ្ចូលទីនេះ)

elif menu == "💰 រដ្ឋបាល & ហិរញ្ញវត្ថុ":
    st.header("💰 ហិរញ្ញវត្ថុ")
    st.dataframe(st.session_state.jmi_db[["ឈ្មោះសិស្ស", "កម្រិត", "ស្ថានភាពបង់ប្រាក់"]])
