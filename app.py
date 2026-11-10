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
        'auth_title': "🔐 Authentication / المصادقة",
        'tab_login': "Login",
        'tab_register': "Register New Account",
        'user_label': "Username / اسم المستخدم:",
        'pass_label': "Password / الرقم السري:",
        'pass_confirm_label': "Confirm Password / تأكيد الرقم السري:",
        'role_select_reg': "Select Role / اختر الصلاحية:",
        'login_btn': "Login / دخول",
        'register_btn': "Register / إنشاء الحساب",
        'login_error': "Invalid Username or Password. Please register first.",
        'reg_success': "Account created successfully! Please switch to Login.",
        'reg_error_match': "Passwords do not match! Please re-enter.",
        'reg_error_exist': "Username already exists. Choose another one.",
        'college_select': "🏛️ Select Faculty / College:",
        'colleges': [
            "Faculty of Media & Mass Communication",
            "Faculty of Business Administration",
            "Faculty of Law",
            "Faculty of Education",
            "Faculty of Allied Health Sciences"
        ],
        'roles_list': [
            "Dean / Executive Management",
            "Deputy Dean",
            "Department Chair",
            "Course Instructor"
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
        'auth_title': "🔐 بوابة الدخول وإنشاء الحسابات",
        'tab_login': "تسجيل الدخول",
        'tab_register': "إنشاء حساب جديد",
        'user_label': "اسم المستخدم / Username:",
        'pass_label': "الرقم السري / Password:",
        'pass_confirm_label': "تأكيد الرقم السري / Confirm Password:",
        'role_select_reg': "اختر الصلاحية الأكاديمية:",
        'login_btn': "تسجيل الدخول",
        'register_btn': "إتمام التسجيل",
        'login_error': "اسم المستخدم أو الرقم السري غير صحيح، أو يجب إنشاء حساب جديد أولاً.",
        'reg_success': "تم إنشاء الحساب بنجاح! انتقل لتبويب تسجيل الدخول والدخول الآن.",
        'reg_error_match': "كلمتا المرور غير متطابقتين! يرجى إعادة المحاولة.",
        'reg_error_exist': "اسم المستخدم موجود مسبقاً، اختر اسم来的 آخر.",
        'college_select': "🏛️ اختر الكلية الأكاديمية:",
        'colleges': [
            "كلية الإعلام والاتصال",
            "كلية إدارة الأعمال",
            "كلية القانون",
            "كلية التربية",
            "كلية العلوم الصحية المساندة"
        ],
        'roles_list': [
            "العميد / الإدارة العليا",
            "نائب العميد (Deputy Dean)",
            "رئيس القسم الأكاديمي",
            "أستاذ المساق"
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

# 3. إدارة حالة الحسابات المسجلة في الذاكرة المؤقتة
if 'users_db' not in st.session_state:
    # حسابات تجريبية جاهزة مسبقاً
    st.session_state['users_db'] = {
        "dean": {"pass": "123456", "role": "Dean"},
        "deputy": {"pass": "123456", "role": "Deputy Dean"},
        "chair": {"pass": "123456", "role": "Department Chair"},
        "instructor": {"pass": "123456", "role": "Course Instructor"}
    }

if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
    st.session_state['username'] = ""
    st.session_state['user_role'] = ""

with st.sidebar:
    try:
        st.image("cua_logo.png", use_container_width=True)
    except:
        st.write("🏛️ **City University Ajman - CUA**")
        
    st.markdown("---")
    
    lang = st.selectbox("🌐 Language / اختر اللغة", options=['English', 'العربية'], index=1)
    t = TRANSLATIONS[lang]
    
    st.markdown("---")
    
    if not st.session_state['authenticated']:
        st.subheader(t['auth_title'])
        auth_tab1, auth_tab2 = st.tabs([t['tab_login'], t['tab_register']])
        
        with auth_tab1:
            login_user = st.text_input(t['user_label'], key="l_user")
            login_pass = st.text_input(t['pass_label'], type="password", key="l_pass")
            
            if st.button(t['login_btn']):
                if login_user in st.session_state['users_db'] and st.session_state['users_db'][login_user]["pass"] == login_pass:
                    st.session_state['authenticated'] = True
                    st.session_state['username'] = login_user
                    st.session_state['user_role'] = st.session_state['users_db'][login_user]["role"]
                    st.rerun()
                else:
                    st.error(t['login_error'])
        
        with auth_tab2:
            reg_user = st.text_input(t['user_label'], key="r_user")
            reg_pass = st.text_input(t['pass_label'], type="password", key="r_pass")
            reg_pass_confirm = st.text_input(t['pass_confirm_label'], type="password", key="r_pass_conf")
            reg_role = st.selectbox(t['role_select_reg'], options=t['roles_list'])
            
            if st.button(t['register_btn']):
                if not reg_user or not reg_pass:
                    st.error("Please fill all fields.")
                elif reg_pass != reg_pass_confirm:
                    st.error(t['reg_error_match'])
                elif reg_user in st.session_state['users_db']:
                    st.error(t['reg_error_exist'])
                else:
                    st.session_state['users_db'][reg_user] = {"pass": reg_pass, "role": reg_role}
                    st.success(t['reg_success'])
        st.stop()
    else:
        st.success(f"{t['welcome']} **{st.session_state['username']}** ({st.session_state['user_role']})")
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
st.caption(f"{t['subtitle']} | 🏛️ **{college}** | 👤 **{st.session_state['username']}**")
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
