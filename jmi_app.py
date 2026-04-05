import streamlit as st
import pandas as pd

# --- ១. ការកំណត់ទំព័រ (Page Configuration) ---
st.set_page_config(page_title="JMI Management System", page_icon="🏥", layout="wide")

# បង្កើត Database បណ្តោះអាសន្ននៅក្នុង Session (ទិន្នន័យនឹង Reset បើ Refresh)
if 'jmi_db' not in st.session_state:
    st.session_state.jmi_db = pd.DataFrame(columns=[
        "ID", "ឈ្មោះសិស្ស", "កម្រិត", "ជំនាញវេជ្ជសាស្ត្រ", "ពិន្ទុវាយតម្លៃ", "ស្ថានភាពបង់ប្រាក់"
    ])

# --- ២. របារចំហៀង (Sidebar Menu) ---
st.sidebar.title("🏥 JMI Control Panel")
st.sidebar.subheader("ដោយ៖ Dr. CHAN Sokhoeurn")
menu = st.sidebar.selectbox("សូមជ្រើសរើសផ្នែក", 
    ["🏠 ទំព័រដើម", "📝 ចុះឈ្មោះសិស្ស", "📚 កម្មវិធីសិក្សា K-12", "🏆 Skill Passport", "💰 រដ្ឋបាល & ហិរញ្ញវត្ថុ"])

# --- ៣. មុខងារតាមផ្នែកនីមួយៗ ---

# 🏠 ផ្នែកទី ១៖ ទំព័រដើម (Dashboard)
if menu == "🏠 ទំព័រដើម":
    st.header("📊 ទំព័រដើម - JMI Overview")
    col1, col2, col3 = st.columns(3)
    total_students = len(st.session_state.jmi_db)
    paid_students = len(st.session_state.jmi_db[st.session_state.jmi_db["ស្ថានភាពបង់ប្រាក់"] == "បង់រួច"])
    
    col1.metric("សិស្សសរុប", total_students)
    col2.metric("សិស្សបង់ប្រាក់រួច", paid_students)
    col3.metric("កម្មវិធីសិក្សាសកម្ម", "K-12 Medical")

    st.write("---")
    st.subheader("📋 បញ្ជីឈ្មោះសិស្សសរុប")
    st.dataframe(st.session_state.jmi_db, use_container_width=True)

# 📝 ផ្នែកទី ២៖ ចុះឈ្មោះសិស្ស
elif menu == "📝 ចុះឈ្មោះសិស្ស":
    st.header("📝 ចុះឈ្មោះសិស្សថ្មីចូល JMI")
    with st.form("reg_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            sid = st.text_input("លេខសម្គាល់ (ID)")
            sname = st.text_input("ឈ្មោះពេញសិស្ស")
        with c2:
            slevel = st.selectbox("កម្រិតសិក្សា", ["Kindergarten", "Primary", "Secondary", "High School"])
            sskill = st.text_input("ជំនាញគោល (Focus Skill)")
        
        btn = st.form_submit_button("រក្សាទុកទិន្នន័យ")
        if btn:
            if sid and sname:
                new_row = pd.DataFrame([[sid, sname, slevel, sskill, 0, "មិនទាន់បង់"]], 
                                       columns=st.session_state.jmi_db.columns)
                st.session_state.jmi_db = pd.concat([st.session_state.jmi_db, new_row], ignore_index=True)
                st.success(f"បានចុះឈ្មោះសិស្ស {sname} ជោគជ័យ!")
            else:
                st.error("សូមបំពេញ ID និង ឈ្មោះសិស្ស!")

# 📚 ផ្នែកទី ៣៖ កម្មវិធីសិក្សា (Curriculum) បែងចែកជា ៤ កម្រិត
elif menu == "📚 កម្មវិធីសិក្សា K-12":
    st.header("📚 កម្មវិធីសិក្សាឯកទេស Junior Medical Institute")
    
    t1, t2, t3, t4 = st.tabs(["🍼 Kindergarten", "🏫 Primary", "🔬 Secondary", "🎓 High School"])
    
    with t1:
        st.subheader("🍼 កម្រិតមត្តេយ្យ (Foundation)")
        c1, c2 = st.columns(2)
        with c1:
            st.info("**មេរៀនទី១:** ស្គាល់ពីសរីរាង្គខាងក្រៅ (Human Organs)")
            st.write("- ភ្នែក ច្រមុះ មាត់ ត្រចៀក និងមុខងាររបស់វា")
        with c2:
            st.info("**មេរៀនទី២:** អាហារូបត្ថម្ភកុមារ (Pediatric Nutrition)")
            st.write("- ស្គាល់ពីបន្លែ ផ្លែឈើ និងអត្ថប្រយោជន៍ទឹកដោះគោ")
        st.success("💡 **គន្លឹះបង្រៀន:** ប្រើប្រាស់រូបភាពពណ៌ ហ្គេមបិទរូបសរីរាង្គ និងចម្រៀងកាយវិការ។")

    with t2:
        st.subheader("🏫 កម្រិតបឋមសិក្សា (Elementary)")
        c1, c2 = st.columns(2)
        with c1:
            st.info("**មេរៀនទី១:** ប្រព័ន្ធរំលាយអាហារ (Digestive System)")
            st.write("- ដំណើរការនៃអាហារពីមាត់ទៅកាន់ក្រពះ និងពោះវៀន")
        with c2:
            st.info("**មេរៀនទី២:** អនាម័យ និងមេរោគ (Germs & Hygiene)")
            st.write("- របៀបលាងដៃ ៧ ជំហាន និងការការពារខ្លួនពីបាក់តេរី")
        st.success("💡 **គន្លឹះបង្រៀន:** ពិសោធន៍វិទ្យាសាស្ត្រងាយៗ (ឧ. ការប្រើម្សៅតំណាងឱ្យមេរោគលើដៃ)។")

    with t3:
        st.subheader("🔬 កម្រិតអនុវិទ្យាល័យ (Secondary)")
        c1, c2 = st.columns(2)
        with c1:
            st.info("**មេរៀនទី១:** ប្រព័ន្ធរបត់ឈាម (Circulatory System)")
            st.write("- មុខងារបេះដូង សរសៃឈាម និងការវាស់ចង្វាក់បេះដូង (Pulse)")
        with c2:
            st.info("**មេរៀនទី២:** មូលដ្ឋានគ្រឹះសង្គ្រោះបឋម (Basic First Aid)")
            st.write("- របៀបលាងរបួស ការរុំរបួសបឋម និងការប្រើប្រាស់បង់បិទ")
        st.success("💡 **គន្លឹះបង្រៀន:** ការអនុវត្តផ្ទាល់ជាមួយឧបករណ៍វាស់ស្ទង់ (Stethoscope)។")

    with t4:
        st.subheader("🎓 កម្រិតវិទ្យាល័យ (High School - Pre-Med)")
        c1, c2 = st.columns(2)
        with c1:
            st.info("**មេរៀនទី១:** សញ្ញាជីវិត (Vital Signs)")
            st.write("- របៀបវាស់សម្ពាធឈាម (BP) កម្តៅ និងអុកស៊ីសែនក្នុងឈាម")
        with c2:
            st.info("**មេរៀនទី២:** វេជ្ជសាស្ត្របច្ចេកវិទ្យា (Digital Health/AI)")
            st.write("- ការប្រើប្រាស់ AI និង Telemedicine ក្នុងវិស័យសុខាភិបាលទំនើប")
        st.success("💡 **គន្លឹះបង្រៀន:** ចុះអនុវត្តនៅមន្ទីរពេទ្យ ឬស្តាប់ការចែករំលែកពីគ្រូពេទ្យជំនាញ។")

# 🏆 ផ្នែកទី ៤៖ Skill Passport (វាយតម្លៃ)
elif menu == "🏆 Skill Passport":
    st.header("🏆 ការវាយតម្លៃជំនាញ (Skill Passport)")
    if not st.session_state.jmi_db.empty:
        target_s = st.selectbox("ជ្រើសរើសសិស្សដើម្បីផ្តល់ពិន្ទុ:", st.session_state.jmi_db["ឈ្មោះសិស្ស"])
        score = st.slider("ផ្តល់ពិន្ទុសមត្ថភាព (%)", 0, 100, 50)
        
        if st.button("បញ្ជាក់ការវាយតម្លៃ"):
            st.session_state.jmi_db.loc[st.session_state.jmi_db["ឈ្មោះសិស្ស"] == target_s, "ពិន្ទុវាយតម្លៃ"] = score
            st.success(f"បាន Update ជំនាញជូន {target_s} ចំនួន {score}%")
            st.table(st.session_state.jmi_db[st.session_state.jmi_db["ឈ្មោះសិស្ស"] == target_s])
    else:
        st.info("មិនទាន់មានសិស្សក្នុងបញ្ជីសម្រាប់វាយតម្លៃឡើយ។")

# 💰 ផ្នែកទី ៥៖ រដ្ឋបាល & ហិរញ្ញវត្ថុ
elif menu == "💰 រដ្ឋបាល & ហិរញ្ញវត្ថុ":
    st.header("💰 គ្រប់គ្រងការបង់ប្រាក់ និងរដ្ឋបាល")
    if not st.session_state.jmi_db.empty:
        col_a, col_b = st.columns(2)
        with col_a:
            s_edit = st.selectbox("ជ្រើសរើសសិស្សបង់ប្រាក់:", st.session_state.jmi_db["ឈ្មោះសិស្ស"])
        with col_b:
            status_edit = st.radio("ស្ថានភាព:", ["មិនទាន់បង់", "បង់រួច"], horizontal=True)
        
        if st.button("Update ស្ថានភាពហិរញ្ញវត្ថុ"):
            st.session_state.jmi_db.loc[st.session_state.jmi_db["ឈ្មោះសិស្ស"] == s_edit, "ស្ថានភាពបង់ប្រាក់"] = status_edit
            st.success("បានកែប្រែទិន្នន័យរួចរាល់!")
            
        st.write("---")
        st.dataframe(st.session_state.jmi_db[["ID", "ឈ្មោះសិស្ស", "កម្រិត", "ស្ថានភាពបង់ប្រាក់"]])
    else:
        st.info("មិនទាន់មានទិន្នន័យហិរញ្ញវត្ថុ។")
