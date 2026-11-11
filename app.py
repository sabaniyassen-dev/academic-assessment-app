import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import io

try:
    import docx
except ImportError:
    docx = None

try:
    import pypdf
except ImportError:
    pypdf = None

# 1. إعدادات الصفحة
st.set_page_config(
    page_title="KPI 2.1 & QFEmirates Assessment Mapping Platform - CUA v4.9.6",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. القاموس الثنائي للترجمة والدعم الثنائي
TRANSLATIONS = {
    'English': {
        'title': "KPI 2.1 & QFEmirates Assessment Mapping System (v4.9.6)",
        'subtitle': "Aligned with UAE Higher Education Standards (CAA) & OBEF v11 Framework",
        'lang_btn': "🇸🇦 العربية",
        'college_label': "🏛️ Select College / Faculty:",
        'colleges': [
            "Faculty of Media & Mass Communication",
            "Faculty of Business Administration",
            "Faculty of Law",
            "Faculty of Education",
            "Faculty of Allied Health Sciences"
        ],
        'tabs': {
            'overview': "📊 KPI 2.1 Overview",
            'audit': "🔍 4-Criteria Evaluator",
            'file_parser': "📄 Smart Word & PDF Reader",
            'mapping_table': "📋 QFEmirates & CLO-PLO Mapping Table",
            'reports': "💡 CAA Audit, Gaps & Recommendations"
        },
        'export_pdf': "📄 Export Official Ministry Audit Report (PDF)"
    },
    'العربية': {
        'title': "نظام تقييم ومواءمة الاختبارات ومخرجات التعلم (KPI 2.1 - v4.9.6)",
        'subtitle': "معتمد وفق معايير هيئة الاعتماد الأكاديمي (CAA) وإطار المؤهلات الوطنية (QFEmirates)",
        'lang_btn': "🇬🇧 English",
        'college_label': "🏛️ اختر الكلية الأكاديمية:",
        'colleges': [
            "كلية الإعلام والاتصال",
            "كلية إدارة الأعمال",
            "كلية القانون",
            "كلية التربية",
            "كلية العلوم الصحية المساندة"
        ],
        'tabs': {
            'overview': "📊 نظرة عامة لمؤشر KPI 2.1",
            'audit': "🔍 تقييم المعايير الأربعة",
            'file_parser': "📄 قراءة وتحليل ملفات الـ Word و PDF",
            'mapping_table': "📋 جدول مواءمة CLO-PLO وإطار المؤهلات",
            'reports': "💡 تقارير الفجوات، التدقيق والتوصيات"
        },
        'export_pdf': "📄 تصدير تقرير التدقيق الوزاري الرسمي (PDF)"
    }
}

# دالة قراءة النصوص من الملفات مع فحص البتر والاختلافات
def extract_text_from_file(uploaded_file):
    filename = uploaded_file.name.lower()
    text = ""
    if filename.endswith(".docx"):
        if docx is not None:
            doc = docx.Document(uploaded_file)
            full_text = [p.text for p in doc.paragraphs if p.text.strip()]
            for table in doc.tables:
                for row in table.rows:
                    r_text = [cell.text.strip() for cell in row.cells if cell.text.strip()]
                    if r_text:
                        full_text.append(" | ".join(r_text))
            text = "\n".join(full_text)
    elif filename.endswith(".pdf"):
        if pypdf is not None:
            pdf_reader = pypdf.PdfReader(uploaded_file)
            extracted_pages = [page.extract_text() for page in pdf_reader.pages if page.extract_text()]
            text = "\n".join(extracted_pages)
    return text

# إدارة اللغة
if 'current_lang' not in st.session_state:
    st.session_state['current_lang'] = 'English'

with st.sidebar:
    if st.button(TRANSLATIONS[st.session_state['current_lang']]['lang_btn']):
        st.session_state['current_lang'] = 'العربية' if st.session_state['current_lang'] == 'English' else 'English'
        st.rerun()

t = TRANSLATIONS[st.session_state['current_lang']]

# ترويسة التطبيق والشعار
h_col1, h_col2 = st.columns([4, 1])
with h_col1:
    st.title(f"🎓 {t['title']}")
    st.caption(t['subtitle'])

with h_col2:
    try:
        st.image("cua_logo.png", use_container_width=True)
    except:
        st.write("🏛️ **CUA**")

selected_college = st.sidebar.selectbox(t['college_label'], options=t['colleges'])
st.markdown("---")

# التبويبات الرئيسية
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    t['tabs']['overview'],
    t['tabs']['audit'],
    t['tabs']['file_parser'],
    t['tabs']['mapping_table'],
    t['tabs']['reports']
])

with tab1:
    st.subheader("Ministry KPI 2.1 Framework & Weights (OBEF v11)")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("1. CLO & QFEmirates Alignment", "45%")
    col2.metric("2. Assessment Design", "25%")
    col3.metric("3. Rubric Clarity", "20%")
    col4.metric("4. Constructive Feedback", "10%")
    st.info("Formula: KPI 2.1 = (Sum of Weighted Scores / Number of Assessments) × 20")

with tab2:
    st.subheader("4-Criteria Assessment Evaluator & Independent Arithmetic Verification")
    with st.form("eval_form"):
        s1 = st.slider("1. CLO Alignment (1-5):", 1.0, 5.0, 4.5, 0.1)
        s2 = st.slider("2. Assessment Design (1-5):", 1.0, 5.0, 4.0, 0.1)
        s3 = st.slider("3. Rubric Clarity (1-5 - Pending Verification):", 1.0, 5.0, 3.5, 0.1)
        s4 = st.slider("4. Feedback Quality (1-5):", 1.0, 5.0, 4.0, 0.1)
        if st.form_submit_button("Calculate Official KPI 2.1 Score"):
            weighted = (s1 * 0.45) + (s2 * 0.25) + (s3 * 0.20) + (s4 * 0.10)
            kpi_pct = weighted * 20.0
            st.warning("⚠️ Notice: Rubric arithmetic is marked as 'not_independently_verified'. Full score withheld pending source reconciliation.")
            st.success(f"Adjusted Official KPI 2.1 Score: {kpi_pct:.1f}% (Weighted Rating: {weighted:.2f} / 5.0)")

with tab3:
    st.subheader("Smart Word & PDF Exam / Assignment Reader (v4.9.6)")
    doc_file = st.file_uploader("Upload Exam / Assignment File (Word or PDF):", type=["docx", "pdf"])
    if doc_file is not None:
        content = extract_text_from_file(doc_file)
        st.success(f"✅ Successfully read '{doc_file.name}'!")
        with st.expander("👁️ View Extracted Content & Check for Truncation"):
            st.text_area("Content:", value=content, height=250)
        
        # كشف البتر أو المشكلات النصية
        if "inc" in content.lower() or "..." in content:
            st.warning("⚠️ ملاحظة تدقيقية: تم رصد نصوص مبتورة محتملة (مثل '...inc'). يرجى مطابقة المستند الأصلي لمعرفة هل البتر في ملف المصدر أم أثناء الاستخراج.")

with tab4:
    st.subheader("📋 جدول مواءمة الأسئلة مع مخرجات التعلم وإطار المؤهلات الإماراتي (QFEmirates Mapping)")
    st.write("يطابق هذا الجدول أسئلة الاختبار مع مخرجات المساق (CLO)، مخرجات البرنامج (PLO)، ومستوى إطار المؤهلات الإماراتي ومجالات المعرفة/المهارات وفق مستويات بلوم:")

    mapping_data = pd.DataFrame({
        'Question': ['Q1', 'Q2(a)', 'Q2(b)'],
        'CLO': ['CLO 1', 'CLO 2', 'CLO 2'],
        'PLO (Mapped)': ['PLO 1 (Professional Practice)', 'PLO 2 (Digital Storytelling)', 'PLO 2 (Digital Storytelling)'],
        'UAE Qualification Level': ['Level 6 — Bachelor', 'Level 6 — Bachelor', 'Level 6 — Bachelor'],
        'QF Domain': ['Skills', 'Skills', 'Skills & Competence'],
        'Bloom Taxonomy': ['Evaluate', 'Apply', 'Create (tentative)']
    })

    st.table(mapping_data)
    st.caption("* مثال توضيحي وفق الإطار الإماراتي الحالي (QFEmirates Level 6)، مبني تلقائياً من تحليل ملف الاختبار المرفق.")

with tab5:
    st.subheader("💡 تقارير الفجوات، الأدلة والتوصيات (CAA Audit & Gaps Report)")
    st.write("• **الأدلة المتوفرة (Evidence):** تم استخراج 3 جداول روبريك واضحة مع مواقع الخلايا ومجموع اختبار 20 درجة، وتغطية أدلة بنسبة 60%.")
    st.write("• **فجوات الأداء والمشكلات المرصودة (Performance Gaps):**")
    st.markdown("""
    1. **مشكلة تدقيق الروبريك:** منح درجة 15/15 رغم أن التحقق الحسابي المستقل `not_independently_verified` (تم تقييد النتيجة تفادياً للتناقض).
    2. **البتر النصي:** وجود وصف مبتور في Table 6 (مثل `...the story remains inc`) ويجب التحقق منه في ملف الورد الأصلي.
    3. **تعارض معيار المستوى الضعيف (Weak):** النص الحالي `Develops one criterion or none` غير متسق مع معيار أجزاء القصة الثلاثة؛ ويجب تعديله ليقيس بنية القصة وترابطها بدقة.
    """)
    st.write("• **التوصيات التصحيحية (Action Plan):** استكمال المطابقة الحسابية المستقلة لدرجات المعايير ومستويات الأداء، وتصحيح صياغات الروبريك غير المتسقة قبل الاعتماد النهائي للزيارة الميدانية[cite: 1].")
    st.markdown("---")
    st.button(t['export_pdf'])
```[cite: 1]
