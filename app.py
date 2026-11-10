import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# 1. إعدادات الصفحة
st.set_page_config(
    page_title="CUA Academic Assessment & CLO Platform",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. القاموس الثنائي للترجمة
TRANSLATIONS = {
    'English': {
        'title': "🎓 CUA Academic Assessment & CLO Analysis Platform",
        'subtitle': "Aligned with UAE Higher Education Standards (CAA) & QFEmirates Framework",
        'login_header': "🔐 Secure Login / تسجيل الدخول",
        'id_label': "Staff ID / الرقم الوظيفي:",
        'pass_label': "Password / الرقم السري:",
        'login_btn': "Login / دخول",
        'login_error': "Invalid Staff ID or Password. Please check your credentials.",
        'college_select': "🏛️ Select Faculty / College:",
        'colleges': [
            "Faculty of Media & Mass Communication",
            "Faculty of Business Administration",
            "Faculty of Law",
            "Faculty of Education",
            "Faculty of Allied Health Sciences"
        ],
        'welcome': "Welcome, logged in as:",
        'tabs': {
            'input': "📊 Course & Data Setup",
            'upload': "📁 Import Grades & Data",
            'clo': "🎯 CLO & Bloom's Analysis",
            'reports': "💡 Smart Accreditation Reports"
        },
        'course_info': "Course Information & Manual Setup",
        'course_name': "Course Name:",
        'course_code': "Course Code:",
        'students_cnt': "Number of Enrolled Students:",
        'bloom_dist': "Bloom's Taxonomy Distribution in Assessments (%)",
        'bloom_levels': ['Remember', 'Understand', 'Apply', 'Analyze', 'Evaluate', 'Create'],
        'upload_section': "📁 Upload Student Assessment & Grades File",
        'upload_help': "Upload an Excel (.xlsx) or CSV file containing student grades and CLO mappings.",
        'data_preview': "Preview Uploaded Student Data & Detailed Analysis:",
        'clo_perf': "Course Learning Outcomes (CLO) Performance Analysis",
        'recommendations': "💡 Smart Audit & Accreditation Recommendations",
        'instructor_plan': "Course Improvement Plan (For Instructor):",
        'strengths': "Strengths:",
        'gaps': "Performance Gaps:",
        'actions': "Continuous Improvement Plan:",
        'qa_audit': "Quality Assurance & CAA Alignment Note:",
        'export_pdf': "📄 Export CAA Audit Report (PDF)"
    },
    'العربية': {
        'title': "🎓 منصة جامعة المدينة عجمان لتحليل الاختبارات ومخرجات التعلم",
        'subtitle': "معتمدة ومطابقة لـ معايير هيئة الاعتماد الأكاديمي (CAA) وإطار المؤهلات الوطنية (QFEmirates)",
        'login_header': "🔐 تسجيل الدخول الآمن للأطراف الأكاديمية",
        'id_label': "الرقم الوظيفي / Staff ID:",
        'pass_label': "الرقم السري / Password:",
        'login_btn': "تسجيل الدخول",
        'login_error': "الرقم الوظيفي أو الرمز السري غير صحيح. يرجى المحاولة مرة أخرى.",
        'college_select': "🏛️ اختر الكلية الأكاديمية:",
        'colleges': [
            "كلية الإعلام والاتصال",
            "كلية إدارة الأعمال",
            "كلية القانون",
            "كلية التربية",
            "كلية العلوم الصحية المساندة"
        ],
        'welcome': "مرحباً بك، أنت مسجل بصلاحية:",
        'tabs': {
            'input': "📊 بيانات المساق والإعداد اليدوي",
            'upload': "📁 استيراد ملفات الدرجات والبيانات",
            'clo': "🎯 تحليلات CLO ومستويات بلوم",
            'reports': "💡 التوصيات والتقارير الذكية"
        },
        'course_info': "بيانات المساق الأساسية",
        'course_name': "اسم المساق:",
        'course_code': "رمز المساق:",
        'students_cnt': "عدد الطلاب المسجلين:",
        'bloom_dist': "توزيع أسئلة الاختبارات على مستويات بلوم (%)",
        'bloom_levels': ['التذكر', 'الفهم', 'التطبيق', 'التحليل', 'التقييم', 'الابتكار'],
        'upload_section': "📁 رفع ملف درجات الطلاب وتقييمات الاختبارات",
        'upload_help': "قم برفع ملف Excel (.xlsx) أو CSV يحتوي على درجات الطلاب وتوزيع مخرجات التعلم.",
        'data_preview': "معاينة بيانات الطلاب المستوردة والتحليل التفصيلي:",
        'clo_perf': "تحليل أداء مخرجات التعلم (CLOs)",
        'recommendations': "💡 التوصيات والتقارير الذكية الموجهة للجان الاعتماد والتقييم",
        'instructor_plan': "توصيات خاصة بأستاذ المساق (Course Improvement Plan):",
        'strengths': "مواطن القوة:",
        'gaps': "فجوة الأداء (Gaps):",
        'actions': "الخطط التصحيحية (Continuous Improvement):",
        'qa_audit': "ملاحظات جودة ومطابقة CAA لرئيس القسم:",
        'export_pdf': "📄 تصدير تقرير التقييم الاعتمادي (PDF)"
    }
}

# قاعدة بيانات الأمان والأدوار (اعتمدنا Deputy Dean حصرياً)
VALID_USERS = {
    "1001": {"pass": "dean123", "role": {"English": "Dean / Executive Management", "العربية": "العميد / الإدارة العليا"}},
    "1002": {"pass": "deputy123", "role": {"English": "Deputy Dean", "العربية": "نائب العميد (Deputy Dean)"}},
    "1003": {"pass": "chair123", "role": {"English": "Department Chair", "العربية": "رئيس القسم الأكاديمي"}},
    "1004": {"pass": "inst123", "role": {"English": "Course Instructor", "العربية": "أستاذ المساق"}}
}

# 3. الشريط الجانبي ونظام المصادقة
with st.sidebar:
    try:
        st.image("cua_logo.png", use_container_width=True)
    except:
        st.write("🏛️ **City University Ajman - CUA**")
        
    st.markdown("---")
    
    lang = st.selectbox("🌐 Language / اختر اللغة", options=['English', 'العربية'], index=1)
    t = TRANSLATIONS[lang]
    
    st.markdown("---")
    st.subheader(t['login_header'])
    
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False
        st.session_state['user_role'] = ""
        st.session_state['user_id'] = ""

    if not st.session_state['authenticated']:
        staff_id = st.text_input(t['id_label'], value="")
        staff_pass = st.text_input(t['pass_label'], type="password", value="")
        
        if st.button(t['login_btn']):
            if staff_id in VALID_USERS and VALID_USERS[staff_id]["pass"] == staff_pass:
                st.session_state['authenticated'] = True
                st.session_state['user_id'] = staff_id
                st.session_state['user_role'] = VALID_USERS[staff_id]["role"][lang]
                st.rerun()
            else:
                st.error(t['login_error'])
        st.stop()
    else:
        st.success(f"{t['welcome']} **{st.session_state['user_role']}** (ID: {st.session_state['user_id']})")
        if st.button("Logout / تسجيل خروج"):
            st.session_state['authenticated'] = False
            st.rerun()

    st.markdown("---")
    college = st.selectbox(t['college_select'], options=t['colleges'])
    
    st.markdown("---")
    qf_level = st.selectbox(
        "Course Level (QFEmirates):",
        options=["Level 7 (Bachelor)", "Level 9 (Master)", "Level 10 (Doctorate)"],
        index=1
    )

# 4. العنوان الرئيسي للمنصة
st.title(t['title'])
st.caption(f"{t['subtitle']} | 🏛️ **{college}** | 👤 **{st.session_state['user_role']}**")
st.markdown("---")

# 5. التبويبات الرئيسية
tab1, tab2, tab3, tab4 = st.tabs([
    t['tabs']['input'], 
    t['tabs']['upload'], 
    t['tabs']['clo'], 
    t['tabs']['reports']
])

with tab1:
    st.subheader(t['course_info'])
    col1, col2, col3 = st.columns(3)
    with col1:
        c_name = st.text_input(t['course_name'], value="Advanced Media Research Methods")
    with col2:
        c_code = st.text_input(t['course_code'], value="MDR-701")
    with col3:
        std_num = st.number_input(t['students_cnt'], min_value=1, value=35)
        
    st.markdown("---")
    st.subheader(t['bloom_dist'])
    b_cols = st.columns(6)
    bloom_vals = []
    default_vals = [10, 15, 25, 25, 15, 10]
    for i, level in enumerate(t['bloom_levels']):
        with b_cols[i]:
            val = st.number_input(level, min_value=0, max_value=100, value=default_vals[i])
            bloom_vals.append(val)

with tab2:
    st.subheader(t['upload_section'])
    st.info(t['upload_help'])
    
    uploaded_file = st.file_uploader("Upload Excel / CSV", type=["xlsx", "csv"])
    
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            st.success("✅ File uploaded successfully!" if lang == 'English' else "✅ تم رفع الملف ومعالجته بنجاح!")
            st.write(t['data_preview'])
            st.dataframe(df.head(10))
            
            if 'Score' in df.columns or 'Grade' in df.columns:
                score_col = 'Score' if 'Score' in df.columns else 'Grade'
                avg_score = df[score_col].mean()
                st.metric(label="Average Student Score / متوسط الدرجات", value=f"{avg_score:.2f}%")
        except Exception as e:
            st.error(f"Error reading file: {e}")
    else:
        sample_data = pd.DataFrame({
            'Student_ID': ['CUA-101', 'CUA-102', 'CUA-103', 'CUA-104', 'CUA-105'],
            'Student_Name': ['Student A', 'Student B', 'Student C', 'Student D', 'Student E'],
            'Midterm_Exam': [85, 78, 92, 65, 88],
            'Final_Exam': [88, 74, 90, 70, 85],
            'CLO_1_Score': [90, 80, 95, 70, 88],
            'CLO_2_Score': [82, 75, 88, 60, 80]
        })
        st.write("📋 **Sample Template Structure / نموذج بيانات مقترح للملف:**")
        st.dataframe(sample_data)

with tab3:
    st.subheader(t['clo_perf'])
    
    fig_bloom = px.bar(
        x=t['bloom_levels'],
        y=bloom_vals,
        labels={'x': 'Bloom Level', 'y': '%'},
        title="Bloom's Taxonomy Distribution" if lang == 'English' else "توزيع مستويات تصنيف بلوم",
        color=bloom_vals,
        color_continuous_scale="Blues"
    )
    st.plotly_chart(fig_bloom, use_container_width=True)
    
    clos = ['CLO 1 (Knowledge)', 'CLO 2 (Skills)', 'CLO 3 (Autonomy/Aspects)']
    scores = [82, 74, 68]
    fig_clo = px.bar(
        x=clos,
        y=scores,
        title="CLO Achievement Rates (%)" if lang == 'English' else "نسب تحقيق مخرجات التعلم (%)",
        labels={'x': 'CLO', 'y': 'Achievement (%)'},
        color=scores,
        color_continuous_scale="RdYlGn"
    )
    fig_clo.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="Target Threshold (70%)")
    st.plotly_chart(fig_clo, use_container_width=True)

with tab4:
    st.subheader(t['recommendations'])
    
    st.info(f"📌 {t['instructor_plan']}")
    st.write(f"• **{t['strengths']}** " + ("High achievement in core knowledge and application levels (CLO 1)." if lang == 'English' else "تحقيق عالٍ في مستويات المعرفة الأساسية والتطبيق (CLO 1)."))
    st.write(f"• **{t['gaps']}** " + ("Performance drop observed in evaluation & higher-order analysis tasks (CLO 3)." if lang == 'English' else "ملاحظة انخفاض طفيف في مهام التحليل والتقييم ذات المستويات العليا (CLO 3)."))
    st.write(f"• **{t['actions']}** " + ("Revise formative assessment rubrics and introduce case study scenarios." if lang == 'English' else "مراجعة معايير التقييم التكويني وإدخال سيناريوهات دراسة الحالة."))
    
    st.markdown("---")
    st.warning(f"🛡️ {t['qa_audit']}")
    st.write("• " + ("Align course assessment weights with QFEmirates Level 9 descriptor standards." if lang == 'English' else "مواءمة أوزان تقييم المساق مع معايير ومواصفات المستوى 9 لإطار المؤهلات الوطنية."))
    st.write("• " + ("Ensure direct assessment artifacts are ready for CAA peer review committee audit." if lang == 'English' else "التأكد من جاهزية أدلة التقييم المباشر لمراجعة لجان الاعتماد الأكاديمي CAA."))
    
    st.markdown("---")
    st.button(t['export_pdf'])
