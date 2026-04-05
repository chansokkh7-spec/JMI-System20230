import streamlit as st
import pandas as pd

# --- ១. ការកំណត់ទំព័រ ---
st.set_page_config(page_title="JMI Management System", page_icon="🏥", layout="wide")

if 'jmi_db' not in st.session_state:
    st.session_state.jmi_db = pd.DataFrame(columns=["ID", "ឈ្មោះសិស្ស", "កម្រិត", "ជំនាញវេជ្ជសាស្ត្រ", "ពិន្ទុវាយតម្លៃ", "ស្ថានភាពបង់ប្រាក់"])

# --- ២. Sidebar Menu ---
st.sidebar.title("🏥 JMI Control Panel")
menu = st.sidebar.selectbox("សូមជ្រើសរើសផ្នែក", ["🏠 ទំព័រដើម", "📝 ចុះឈ្មោះសិស្ស", "📚 កម្មវិធីសិក្សា K-12", "🏆 Skill Passport", "💰 រដ្ឋបាល & ហិរញ្ញវត្ថុ"])

# --- ៣. មុខងារកម្មវិធីសិក្សា (៩ មេរៀនក្នុងមួយកម្រិត) ---
if menu == "📚 កម្មវិធីសិក្សា K-12":
    st.header("📚 កម្មវិធីសិក្សាឯកទេស JMI (៩ មេរៀនក្នុងមួយកម្រិត)")
    
    t1, t2, t3, t4 = st.tabs(["🍼 Kindergarten", "🏫 Primary", "🔬 Secondary", "🎓 High School"])
    
    levels = {
        "🍼 Kindergarten": [
            "១. ស្គាល់សរីរាង្គខាងក្រៅ", "២. អាហារូបត្ថម្ភកុមារ", "៣. អនាម័យមាត់ធ្មេញ", 
            "៤. ការលាងដៃឱ្យស្អាត", "៥. វីតាមីនផ្ដល់ថាមពល", "៦. ស្គាល់ឧបករណ៍ពេទ្យ", 
            "៧. សុវត្ថិភាពចំណីអាហារ", "៨. ការគេងនិងសុខភាព", "៩. លំហាត់ប្រាណកុមារ"
        ],
        "🏫 Primary": [
            "១. ប្រព័ន្ធរំលាយអាហារ", "២. មេរោគនិងបាក់តេរី", "៣. សួតនិងការដកដង្ហើម", 
            "៤. គ្រោងឆ្អឹងមនុស្ស", "៥. ការពារជំងឺឆ្លង", "៦. របៀបហៅលេខសង្គ្រោះ", 
            "៧. សុខភាពភ្នែកនិងត្រចៀក", "៨. ការផឹកទឹកនិងតម្រងនោម", "៩. ជំនាញបង់រុំរបួស"
        ],
        "🔬 Secondary": [
            "១. ប្រព័ន្ធរបត់ឈាម", "២. បេះដូងនិងសរសៃឈាម", "៣. ការវាស់ចង្វាក់បេះដូង", 
            "៤. មូលដ្ឋានគ្រឹះសង្គ្រោះបឋម", "៥. ប្រព័ន្ធប្រសាទនិងខួរក្បាល", "៦. ស្គាល់ប្រភេទថ្នាំទូទៅ", 
            "៧. សុខភាពផ្លូវចិត្តបឋម", "៨. ប្រព័ន្ធស៊ាំរាងកាយ", "៩. ការវិភាគឈាមបឋម"
        ],
        "🎓 High School": [
            "១. ការវាស់សញ្ញាជីវិត (Vital Signs)", "២. របៀបវាស់សម្ពាធឈាម", "៣. ជីវវិទ្យាកោសិកានិងហ្សែន", 
            "៤. ក្រមសីលធម៌គ្រូពេទ្យ", "៥. ជំងឺមិនឆ្លង (NCDs)", "៦. ការប្រើប្រាស់ AI ក្នុងពេទ្យ", 
            "៧. ការសរសេររបាយការណ៍ពេទ្យ", "៨. បច្ចេកទេសវះកាត់តូចៗ", "៩. ការរៀបចំខ្លួនចូលរៀនពេទ្យ"
        ]
    }

    current_tabs = [t1, t2, t3, t4]
    for i, (level_name, lessons) in enumerate(levels.items()):
        with current_tabs[i]:
            st.subheader(f"មេរៀនសម្រាប់កម្រិត {level_name}")
            cols = st.columns(3) # បែងចែកជា ៣ ជួរឱ្យស្អាត
            for index, lesson in enumerate(lessons):
                cols[index % 3].info(lesson)
            st.success("💡 រាល់បញ្ចប់មេរៀនទាំង ៩ សិស្សនឹងទទួលបានត្រាបញ្ជាក់ក្នុង Skill Passport។")

# --- ៤. ផ្នែកផ្សេងៗ (រក្សាមុខងារចាស់) ---
elif menu == "🏠 ទំព័រដើម":
    st.header("📊 JMI Dashboard")
    st.metric("សិស្សសរុប", len(st.session_state.jmi_db))
    st.dataframe(st.session_state.jmi_db)

elif menu == "📝 ចុះឈ្មោះសិស្ស":
    st.header("📝 ចុះឈ្មោះសិស្ស")
    with st.form("reg"):
        id, name = st.text_input("ID"), st.text_input("Name")
        lvl = st.selectbox("Level", ["Kindergarten", "Primary", "Secondary", "High School"])
        if st.form_submit_button("Save"):
            new = pd.DataFrame([[id, name, lvl, "", 0, "មិនទាន់បង់"]], columns=st.session_state.jmi_db.columns)
            st.session_state.jmi_db = pd.concat([st.session_state.jmi_db, new], ignore_index=True)
            st.success("Done!")

elif menu == "🏆 Skill Passport":
    st.header("🏆 វាយតម្លៃសមត្ថភាព")
    st.write("សូមជ្រើសរើសសិស្សដើម្បីបញ្ចូលពិន្ទុសម្រាប់មេរៀនទាំង ៩។")

elif menu == "💰 រដ្ឋបាល & ហិរញ្ញវត្ថុ":
    st.header("💰 ហិរញ្ញវត្ថុ")
    st.write("គ្រប់គ្រងការបង់ថ្លៃសិក្សារបស់សិស្ស JMI។")
