import streamlit as st
import pandas as pd
from datetime import datetime

# --- ១. ការកំណត់ទំព័រ ---
st.set_page_config(page_title="JMI Management System", page_icon="🏥", layout="wide")

# បង្កើត Database បណ្តោះអាសន្ន
if 'jmi_db' not in st.session_state:
    st.session_state.jmi_db = pd.DataFrame(columns=[
        "ID", "ឈ្មោះសិស្ស", "កម្រិត", "ជំនាញវេជ្ជសាស្ត្រ", "ពិន្ទុវាយតម្លៃ", "ស្ថានភាពបង់ប្រាក់", "ថ្ងៃបង់ប្រាក់"
    ])

if 'jmi_grades' not in st.session_state:
    st.session_state.jmi_grades = {}

# --- ២. Sidebar Menu ---
st.sidebar.title("🏥 JMI Control Panel")
st.sidebar.write(f"អ្នកគ្រប់គ្រង៖ **Dr. CHAN Sokhoeurn**")
menu = st.sidebar.selectbox("សូមជ្រើសរើសផ្នែក", ["🏠 ទំព័រដើម", "📝 ចុះឈ្មោះសិស្ស", "📚 កម្មវិធីសិក្សា K-12", "🏆 Skill Passport", "💰 រដ្ឋបាល & ហិរញ្ញវត្ថុ"])

# --- ៣. មុខងារតាមផ្នែកនីមួយៗ ---

# 🏠 ផ្នែកទី ១៖ ទំព័រដើម
if menu == "🏠 ទំព័រដើម":
    st.header("📊 JMI Dashboard Overview")
    c1, c2, c3 = st.columns(3)
    c1.metric("សិស្សសរុប", len(st.session_state.jmi_db))
    paid_count = len(st.session_state.jmi_db[st.session_state.jmi_db["ស្ថានភាពបង់ប្រាក់"] == "បង់រួច"])
    c2.metric("បង់ប្រាក់រួច", paid_count)
    c3.metric("ជំពាក់ប្រាក់", len(st.session_state.jmi_db) - paid_count)
    st.write("---")
    st.subheader("📋 បញ្ជីឈ្មោះសិស្សក្នុងប្រព័ន្ធ")
    st.dataframe(st.session_state.jmi_db, use_container_width=True)

# 📝 ផ្នែកទី ២៖ ចុះឈ្មោះសិស្ស
elif menu == "📝 ចុះឈ្មោះសិស្ស":
    st.header("📝 ចុះឈ្មោះសិស្សថ្មី")
    with st.form("reg_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            sid = st.text_input("លេខសម្គាល់ (ID)")
            sname = st.text_input("ឈ្មោះពេញសិស្ស")
        with col2:
            slevel = st.selectbox("កម្រិតសិក្សា", ["Kindergarten", "Primary", "Secondary", "High School"])
            sskill = st.text_input("ជំនាញគោល")
        
        if st.form_submit_button("រក្សាទុក"):
            if sid and sname:
                new_row = pd.DataFrame([[sid, sname, slevel, sskill, 0, "មិនទាន់បង់", "-"]], columns=st.session_state.jmi_db.columns)
                st.session_state.jmi_db = pd.concat([st.session_state.jmi_db, new_row], ignore_index=True)
                st.success("ចុះឈ្មោះជោគជ័យ!")
            else: st.error("សូមបំពេញព័ត៌មានឱ្យគ្រប់!")

# 📚 ផ្នែកទី ៣៖ កម្មវិធីសិក្សា K-12 (៩ មេរៀន)
elif menu == "📚 កម្មវិធីសិក្សា K-12":
    st.header("📚 កម្មវិធីសិក្សាឯកទេស JMI")
    tabs = st.tabs(["🍼 Kindergarten", "🏫 Primary", "🔬 Secondary", "🎓 High School"])
    lessons_list = ["១. មេរៀនមូលដ្ឋាន", "២. សរីរាង្គ", "៣. អនាម័យ", "៤. អាហារូបត្ថម្ភ", "៥. ការពារជំងឺ", "៦. សង្គ្រោះបឋម", "៧. ប្រព័ន្ធប្រសាទ", "៨. បច្ចេកវិទ្យា", "៩. ការអនុវត្តផ្ទាល់"]
    for i, tab in enumerate(tabs):
        with tab:
            cols = st.columns(3)
            for j, lesson in enumerate(lessons_list):
                cols[j%3].info(lesson)

# 🏆 ផ្នែកទី ៤៖ Skill Passport
elif menu == "🏆 Skill Passport":
    st.header("🏆 វាយតម្លៃសមត្ថភាព (Skill Passport)")
    if not st.session_state.jmi_db.empty:
        s_target = st.selectbox("ជ្រើសរើសសិស្ស:", st.session_state.jmi_db["ឈ្មោះសិស្ស"])
        with st.form("grade_form"):
            new_scores = {}
            cols = st.columns(3)
            for i in range(1, 10):
                new_scores[f"មេរៀនទី {i}"] = cols[(i-1)%3].number_input(f"មេរៀនទី {i}", 0, 100, 0)
            if st.form_submit_button("រក្សាទុកពិន្ទុ"):
                st.session_state.jmi_grades[s_target] = new_scores
                avg = sum(new_scores.values())/9
                st.session_state.jmi_db.loc[st.session_state.jmi_db["ឈ្មោះសិស្ស"] == s_target, "ពិន្ទុវាយតម្លៃ"] = round(avg, 2)
                st.success("រក្សាទុកពិន្ទុរួចរាល់!")
    else: st.warning("មិនទាន់មានសិស្ស!")

# 💰 ផ្នែកទី ៥៖ រដ្ឋបាល & ហិរញ្ញវត្ថុ (បង់ប្រាក់ និង ចេញវិក្កយបត្រ)
elif menu == "💰 រដ្ឋបាល & ហិរញ្ញវត្ថុ":
    st.header("💰 គ្រប់គ្រងហិរញ្ញវត្ថុ និងវិក្កយបត្រ")
    
    if not st.session_state.jmi_db.empty:
        col_list, col_pay = st.columns([2, 1])
        
        with col_list:
            st.subheader("📋 ស្ថានភាពហិរញ្ញវត្ថុសរុប")
            st.dataframe(st.session_state.jmi_db[["ID", "ឈ្មោះសិស្ស", "កម្រិត", "ស្ថានភាពបង់ប្រាក់", "ថ្ងៃបង់ប្រាក់"]], use_container_width=True)
            
        with col_pay:
            st.subheader("💵 បញ្ជាក់ការបង់ប្រាក់")
            s_pay = st.selectbox("ជ្រើសរើសសិស្សបង់ប្រាក់:", st.session_state.jmi_db["ឈ្មោះសិស្ស"])
            amount = st.number_input("ចំនួនទឹកប្រាក់ ($)", min_value=0.0, value=50.0)
            date_now = datetime.now().strftime("%d-%m-%Y")
            
            if st.button("បញ្ជាក់ការបង់ប្រាក់"):
                st.session_state.jmi_db.loc[st.session_state.jmi_db["ឈ្មោះសិស្ស"] == s_pay, "ស្ថានភាពបង់ប្រាក់"] = "បង់រួច"
                st.session_state.jmi_db.loc[st.session_state.jmi_db["ឈ្មោះសិស្ស"] == s_pay, "ថ្ងៃបង់ប្រាក់"] = date_now
                st.success(f"បានបង់ប្រាក់ជូន {s_pay} រួចរាល់!")
                st.rerun()

        st.write("---")
        st.subheader("📄 ចេញវិក្កយបត្រ (Invoice Generator)")
        s_inv = st.selectbox("ជ្រើសរើសសិស្សដើម្បីទាញយកវិក្កយបត្រ:", st.session_state.jmi_db["ឈ្មោះសិស្ស"])
        inv_data = st.session_state.jmi_db[st.session_state.jmi_db["ឈ្មោះសិស្ស"] == s_inv].iloc[0]
        
        if inv_data["ស្ថានភាពបង់ប្រាក់"] == "បង់រួច":
            # បង្កើតទម្រង់វិក្កយបត្រលើអេក្រង់
            st.code(f"""
            =========================================
                   JUNIOR MEDICAL INSTITUTE (JMI)
                   OFFICIAL PAYMENT RECEIPT
            =========================================
            លេខវិក្កយបត្រ: INV-{inv_data['ID']}-{datetime.now().strftime('%y%m%d')}
            កាលបរិច្ឆេទ:   {inv_data['ថ្ងៃបង់ប្រាក់']}
            -----------------------------------------
            ឈ្មោះសិស្ស:    {inv_data['ឈ្មោះសិស្ស']}
            អត្តសញ្ញាណ:    {inv_data['ID']}
            កម្រិតសិក្សា:    {inv_data['កម្រិត']}
            -----------------------------------------
            បរិយាយ:       ថ្លៃសិក្សាវគ្គ K-12 Medical Basics
            ស្ថានភាព:      បង់ប្រាក់រួចរាល់ (PAID)
            -----------------------------------------
            អរគុណសម្រាប់ការគាំទ្រ JMI!
            =========================================
            """, language="text")
            st.button("🖨️ បោះពុម្ពវិក្កយបត្រ (Print)")
        else:
            st.error("សិស្សនេះមិនទាន់បានបង់ប្រាក់នៅឡើយទេ។ មិនអាចចេញវិក្កយបត្របានទេ!")
    else: st.warning("មិនទាន់មានទិន្នន័យសិស្ស!")
