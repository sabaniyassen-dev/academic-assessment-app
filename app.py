import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# 1. التهوئة وإعدادات الصفحة
st.set_page_config(
    page_title="Academic Assessment & CLO Platform",
    page_layout="wide",
    initial_sidebar_state="expanded"
)

# 2. قاموس اللغات (Translations Dictionary)
TRANSLATIONS = {
    'English': {
        'title': "🎓 Academic Assessment & CLO Analysis Platform",
        'subtitle': "Aligned with UAE Higher Education Standards (CAA) & QFEmirates Framework",
        'lang_select': "🌐 Select Language / اختر اللغة",
        'role_select': "🔐 Access Control / Role Selection:",
        'roles': {
            'instructor': "Course Instructor",
            'chair': "Department Chair / Quality Assurance",
            'dean': "Dean / Executive Management"
        },
        'user_name': "User Name:",
        'welcome': "Welcome! Logged in as:",
        'qf_level': "Course Academic Level (QFEmirates):",
        'tabs': {
            'input': "📊 Course & Data Setup",
            'clo': "🎯 CLO & Bloom's Analysis",
            'reports': "💡 Smart Accreditation Reports"
        },
        'course_info': "Course Information",
        'course_name': "Course Name:",
        'course_code': "Course Code:",
        'students_cnt': "Number of Enrolled Students:",
        'bloom_dist': "Bloom's Taxonomy Distribution in Assessments (%)",
        'bloom_levels': ['Remember', 'Understand', 'Apply', 'Analyze', 'Evaluate', 'Create'],
        'clo_perf': "Course Learning Outcomes (CLO) Performance Analysis",
        'clo_target': "Target Target Achievement Threshold (%)",
        'recommendations': "💡 Smart Audit & Accreditation Recommendations",
        'instructor_plan': "Course Improvement Plan (For Instructor):",
        'strengths': "Strengths:",
        'gaps': "Performance Gaps:",
        'actions': "Continuous Improvement Plan:",
        'qa_audit': "Quality Assurance & CAA Alignment Note:",
        'export_pdf': "📄 Export CAA Audit Report (PDF)"
    },
    'العربية': {
        'title': "🎓 منصة تحليل الاختبارات ومخرجات التعلم الأكاديمية",
        'subtitle': "معتمدة ومطابقة لـ معايير هيئة الاعتماد الأكاديمي (CAA) وإطار المؤهلات الوطنية (QFEmirates)",
        'lang_select': "🌐 Select Language / اختر اللغة",
        'role_select': "🔐 بوابة تسجيل الدخول والصلاحيات:",
        'roles': {
            'instructor': "أستاذ المساق (Course Instructor)",
            'chair': "رئيس القسم / الجودة (Department Chair / QA)",
            'dean': "العميد / الإدارة العليا (Dean)"
        },
        'user_name': "اسم المستخدم:",
        'welcome': "مرحباً بك، أنت تتصفح بصلاحية:",
        'qf_level': "المستوى الأكاديمي للمساق (QFEmirates):",
        'tabs': {
            'input': "📊 بيانات المساق والنتائج",
            'clo': "🎯 تحليلات CLO ومستويات بلوم",
            'reports': "💡 التوصيات والتقارير الذكية"
        },
        'course_info': "بيانات المساق الأساسية",
        'course_name': "اسم المساق:",
        'course_code': "رمز المساق:",
        'students_cnt': "عدد الطلاب المسجلين:",
        'bloom_dist': "توزيع أسئلة الاختبارات على مستويات بلوم (%)",
        'bloom_levels': ['التذكر', 'الفهم', 'التطبيق', 'التحليل', 'التقييم', 'الابتكار'],
        'clo_perf': "تحليل أداء مخرجات التعلم (CLOs)",
        'clo_target': "حد تحقيق الهدف المستهدف (%)",
        'recommendations': "💡 التوصيات والتقارير الذكية الموجهة للجان الاعتماد والتقييم",
        'instructor_plan': "توصيات خاصة بأستاذ المساق (Course Improvement Plan):",
        'strengths': "مواطن القوة:",
        'gaps': "فجوة الأداء (Gaps):",
        'actions': "الخطط التصحيحية (Continuous Improvement):",
        'qa_audit': "ملاحظات جودة ومطابقة CAA لرئيس القسم:",
        'export_pdf': "📄 تصدير تقرير التقييم الاعتمادي (PDF)"
    }
}

# 3. الشريط الجانبي (Sidebar)
with st.sidebar:
    lang = st.selectbox("🌐 Language / اللغة", options=['English', 'العربية'], index=0)
    t = TRANSLATIONS[lang]
    
    st.markdown("---")
    st.subheader(t['role_select'])
    role = st.selectbox(
        "",
        options=list(t['roles'].values())
    )
    
    user_name = st.text_input(t['user_name'], value="Dr. Ahmad / د. أحمد")
    st.success(f"{t['welcome']} **{role}**")
    
    st.markdown("---")
    qf_level = st.selectbox(
        t['qf_level'],
        options=["Level 7 (Bachelor)", "Level 9 (Master)", "Level 10 (Doctorate)"],
        index=1
    )

# 4. العنوان الرئيسي
st.title(t['title'])
st.caption(t['subtitle'])
st.markdown("---")

# 5. التبويبات الرئيسية
tab1, tab2, tab3 = st.tabs([t['tabs']['input'], t['tabs']['clo'], t['tabs']['reports']])

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
    st.subheader(t['clo_perf'])
    
    # الرسم البياني لمستويات بلوم
    fig_bloom = px.bar(
        x=t['bloom_levels'],
        y=bloom_vals,
        labels={'x': 'Bloom Level', 'y': '%'},
        title="Bloom's Taxonomy Distribution",
        color=bloom_vals,
        color_continuous_scale="Blues"
    )
    st.plotly_chart(fig_bloom, use_container_width=True)
    
    # رسم بياني محاكاة لأداء CLO
    clos = ['CLO 1 (Knowledge)', 'CLO 2 (Skills)', 'CLO 3 (Autonomy/Aspects)']
    scores = [82, 74, 68]
    fig_clo = px.bar(
        x=clos,
        y=scores,
        title="CLO Achievement Rates (%)",
        labels={'x': 'CLO', 'y': 'Achievement (%)'},
        color=scores,
        color_continuous_scale="RdYlGn"
    )
    fig_clo.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="Target (70%)")
    st.plotly_chart(fig_clo, use_container_width=True)

with tab3:
    st.subheader(t['recommendations'])
    
    st.info(f"📌 {t['instructor_plan']}")
    st.write(f"• **{t['strengths']}** High achievement in core knowledge and application levels (CLO 1).")
    st.write(f"• **{t['gaps']}** Performance drop observed in evaluation & higher-order analysis tasks (CLO 3).")
    st.write(f"• **{t['actions']}** Revise formative assessment rubrics and introduce case study scenarios.")
    
    st.markdown("---")
    st.warning(f"🛡️ {t['qa_audit']}")
    st.write("• Align course assessment weights with QFEmirates Level 9 descriptor standards.")
    st.write("• Ensure direct assessment artifacts are ready for CAA peer review committee audit.")
    
    st.markdown("---")
    st.button(t['export_pdf'])
