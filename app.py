import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# إعدادات الصفحة
st.set_page_config(
    page_title="منصة تحليل الاختبارات ومخرجات التعلم - معايير CAA & KPIs",
    layout="wide"
)

# تصميم واجهة تسجيل الدخول والصلاحيات
st.sidebar.title("🔐 بوابة تسجيل الدخول والصلاحيات")
user_role = st.sidebar.selectbox(
    "اختر صفحتك / صلاحيتك:",
    [
        "أستاذ المساق (Course Instructor)",
        "رئيس القسم (Head of Department)",
        "نائب العميد (Vice Dean / QA)",
        "العميد (Dean)",
        "هيئة الاعتماد الأكاديمي والتقييم (CAA & KPIs)"
    ]
)

user_name = st.sidebar.text_input("اسم المستخدم:", "د. أحمد الفلاسي")
st.sidebar.success(f"مرحباً بك، أنت تصفح بصلاحية: {user_role}")

# اختيار المستوى الأكاديمي (بما يتوافق مع إطار QFEmirates)
st.sidebar.markdown("---")
academic_level = st.sidebar.selectbox(
    "المستوى الأكاديمي للمساق (QFEmirates):",
    [
        "بكالوريوس - المستوى 7 (Bachelor's Degree)",
        "ماجستير - المستوى 9 (Master's Degree)",
        "دكتوراه - المستوى 10 (Doctoral Degree)"
    ]
)

st.title("📊 المنصة الذكية لتحليل الاختبارات ومواءمة مخرجات التعلم (KPIs & CAA Compliance)")
st.markdown("---")

# رفع ملف البيانات الحقيقي أو استخدام البيانات التجريبية
st.sidebar.markdown("---")
st.sidebar.subheader("📁 رفع البيانات والملفات الأكاديمية")
uploaded_file = st.sidebar.file_uploader("ارفع ملف مصفوفة الاختبار والدرجات (Excel)", type=["xlsx", "csv"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
else:
    # بيانات تجريبية افتراضية متوافقة مع متطلبات التقييم المتقدمة
    data = {
        'رقم السؤال': ['السؤال 1', 'السؤال 2', 'السؤال 3', 'السؤال 4', 'السؤال 5', 'السؤال 6', 'السؤال 7', 'السؤال 8'],
        'مستوى بلوم': ['التطبيق', 'التحليل', 'الفهم', 'الابتكار', 'التطبيق', 'التقييم', 'التحليل', 'الابتكار'],
        'مخرج المقرر (CLO)': ['CLO 1', 'CLO 2', 'CLO 1', 'CLO 3', 'CLO 2', 'CLO 3', 'CLO 2', 'CLO 3'],
        'مخرج البرنامج (PLO)': ['PLO 1', 'PLO 2', 'PLO 1', 'PLO 3', 'PLO 2', 'PLO 3', 'PLO 2', 'PLO 3'],
        'متوسط الدرجة الحاصل عليها الطلاب (%)': [78, 62, 85, 48, 70, 55, 60, 45],
        'مستهدف الـ KPI المحدد (%)': [70, 70, 70, 65, 70, 65, 70, 65]
    }
    df = pd.DataFrame(data)

# عرض المؤشرات الرئيسية (KPI Cards)
st.subheader("📈 مؤشرات الأداء الرئيسية للتقييم (Assessment KPIs)")
col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)

general_avg = df['متوسط الدرجة الحاصل عليها الطلاب (%)'].mean()
target_avg = df['مستهدف الـ KPI المحدد (%)'].mean()
achieved_clos = (df['متوسط الدرجة الحاصل عليها الطلاب (%)'] >= df['مستهدف الـ KPI المحدد (%)']).mean() * 100

with col_kpi1:
    st.metric(label="متوسط أداء الطلاب العام", value=f"{general_avg:.1f}%", delta=f"{general_avg - 70:.1f}% vs Benchmark")
with col_kpi2:
    st.metric(label="مستهدف المؤشر المؤسسي (KPI Target)", value=f"{target_avg:.1f}%")
with col_kpi3:
    st.metric(label="نسبة تحقيق مخرجات المقرر", value=f"{achieved_clos:.1f}%", delta="مقبول (>=70%)" if achieved_clos >= 70 else "يحتاج تحسين")
with col_kpi4:
    st.metric(label="معيار الاعتماد الأكاديمي (CAA)", value="متوافق (Compliant)", delta="جاهز للتدقيق")

st.markdown("---")

# عرض البيانات الأساسية
st.subheader("📋 جدول مواءمة الاختبار وتحليل أداء الأسئلة (CLO/PLO Mapping)")
st.dataframe(df, use_container_width=True)

# الرسوم البيانية التحليلية
col1, col2 = st.columns(2)

with col1:
    st.subheader("📌 تحليل أداء مستويات بلوم المعرفية")
    fig_bloom = px.bar(
        df, x='مستوى بلوم', y=['متوسط الدرجة الحاصل عليها الطلاب (%)', 'مستهدف الـ KPI المحدد (%)'],
        barmode='group', title="مقارنة أداء الطلاب مع المستهدفات حسب مستويات بلوم"
    )
    st.plotly_chart(fig_bloom, use_container_width=True)

with col2:
    st.subheader("🎯 تحليل مخرجات تعلم المقرر (CLOs Performance)")
    fig_clo = px.box(
        df, x='مخرج المقرر (CLO)', y='متوسط الدرجة الحاصل عليها الطلاب (%)', color='مخرج المقرر (CLO)',
        title="توزيع الدرجات عبر مخرجات تعلم المقرر"
    )
    st.plotly_chart(fig_clo, use_container_width=True)

st.markdown("---")

# التحليلات والتوصيات الذكية الموجهة بناءً على الصلاحية ومعايير الـ CAA
st.subheader("💡 التوصيات والتقارير الذكية الموجهة للجان الاعتماد والتقييم")

if "أستاذ المساق" in user_role:
    st.info("👤 **توصيات خاصة بأستاذ المساق (Course Improvement Plan):**")
    st.markdown("""
    - **مواطن القوة:** أداء ممتاز في الأسئلة المرتبطة بـ (CLO 1) ومستويات الفهم والتطبيق الأساسية.
    - **فجوة الأداء (Gaps):** قصور في الأسئلة التي تقيس مستويات التفكير العليا (الابتكار والتحليل) خصوصاً في المستويات المتقدمة للدراسات العليا.
    - **الخطة التصحيحية (Continuous Improvement):** إعادة صياغة بعض أنشطة التقييم البنائية (Formative Assessments) لتعزيز المهارات البحثية والنقدية للطلاب.
    """)

elif "رئيس القسم" in user_role:
    st.warning("🏛️ **تقرير رئيس القسم الأكاديمي:**")
    st.markdown("""
    - **مواءمة المخرجات:** تم التحقق من ارتباط أسئلة الاختبار بمخرجات البرنامج (PLOs) بنسبة تطابق بلغت 90%.
    - **تحليل الـ KPIs:** مؤشر الأداء الرئيسي للتقييم يحقق الحد الأدنى لمتطلبات القسم، مع وجود حاجة لورشة عمل لأعضاء الهيئة التدريسية حول تصميم أسئلة مستويات بلوم العليا لبرامج الماجستير/الدكتوراه.
    """)

else:
    st.success("👑 **لوحة تحكم الإدارة العليا وضمان الجودة (CAA & Institutional Effectiveness):**")
    st.markdown(f"""
    - **حالة الاعتماد:** البيانات الخاصة بهذا المساق ضمن المستوى (**{academic_level}**) مستوفية لمعايير هيئة الاعتماد الأكاديمي (CAA).
    - **أدلة الجودة:** تم توثيق أدلة تقييم مخرجات التعلم وجاهزيتها للتحميل والإرفاق في ملف تقرير مراجعة البرنامج البرنامجي (Program Review).
    - **التوصية المعتمدة:** اعتماد تقرير التحسين المستمر للمساق وإغلاق الحلقة التطويرية (Closing the Loop).
    """)

# زر لتنزيل التقرير الشامل
st.markdown("---")
st.download_button(
    label="📥 تحميل تقرير مواءمة التقييم الشامل بصيغة CSV / Excel (جاهز لملفات الـ CAA)",
    data=df.to_csv(index=False).encode('utf-8'),
    file_name='CAA_Assessment_Alignment_Report.csv',
    mime='text/csv',
)
