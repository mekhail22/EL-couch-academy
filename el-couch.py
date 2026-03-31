
import streamlit as st
import json
import os
from datetime import datetime
import hashlib
import random
import base64

st.set_page_config(
    page_title="الكوتش أكاديمي - أكاديمية كرة القدم المتخصصة",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ----------------------------
# Session state
# ----------------------------
defaults = {
    "page": "home",
    "show_success": False,
    "show_contact_success": False,
    "visitor_count": random.randint(1000, 5000),
    "last_visit": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


def go_to(page_name: str) -> None:
    st.session_state.page = page_name
    st.rerun()


# ----------------------------
# Helpers
# ----------------------------
def get_image_base64(image_path: str) -> str | None:
    try:
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except Exception:
        return None


def load_json_list(path: str) -> list:
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except Exception:
        return []


def append_json_item(path: str, item: dict) -> bool:
    try:
        items = load_json_list(path)
        items.append(item)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(items, f, ensure_ascii=False, indent=2)
        return True
    except Exception:
        return False


def save_registration(data: dict) -> bool:
    data = dict(data)
    data["timestamp"] = datetime.now().isoformat()
    data["id"] = hashlib.md5(
        f"{data.get('playerName','')}{data['timestamp']}".encode()
    ).hexdigest()[:8]
    return append_json_item("registrations.json", data)


def save_contact(data: dict) -> bool:
    data = dict(data)
    data["timestamp"] = datetime.now().isoformat()
    data["id"] = hashlib.md5(
        f"{data.get('name','')}{data['timestamp']}".encode()
    ).hexdigest()[:8]
    return append_json_item("contacts.json", data)


logo_base64 = get_image_base64("logo.jpg")
logo_html = (
    f'<img src="data:image/jpeg;base64,{logo_base64}" alt="Logo">'
    if logo_base64
    else '<span>⚽</span>'
)

# ----------------------------
# Styles
# ----------------------------
st.markdown(
    """
<style>
header[data-testid="stHeader"], .stApp > header, #MainMenu, footer { display: none !important; }
.main .block-container {
    padding-top: 0rem !important;
    padding-bottom: 0rem !important;
    padding-left: 0rem !important;
    padding-right: 0rem !important;
    max-width: 100% !important;
}
.stApp {
    background: linear-gradient(135deg, #f0f2f6 0%, #ffffff 100%) !important;
}
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: 'Cairo', 'Tajawal', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
.custom-top-header {
    position: sticky;
    top: 0;
    background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
    box-shadow: 0 4px 25px rgba(0, 0, 0, 0.1);
    z-index: 10000;
    padding: 12px 0;
    border-bottom: 2px solid #e2e8f0;
}
.custom-header-container {
    width: 90%;
    max-width: 1200px;
    margin: 0 auto;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.custom-logo-wrapper {
    display: flex;
    align-items: center;
    gap: 15px;
}
.custom-logo-image {
    width: 60px;
    height: 60px;
    border-radius: 18px;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    background: linear-gradient(135deg, #1e3a8a, #3b82f6);
    box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2);
}
.custom-logo-image img { width: 100%; height: 100%; object-fit: cover; }
.custom-logo-image span { font-size: 2.2rem; color: white; }
.custom-logo-text h1 {
    font-size: 1.8rem;
    margin: 0;
    color: #1e3a8a;
    font-weight: 800;
}
.custom-logo-text span { color: #f59e0b; }
.custom-logo-text p { font-size: 0.75rem; color: #64748b; margin: 0; font-weight: 500; }

.custom-content-container {
    width: 90%;
    max-width: 1200px;
    margin: 0 auto;
    padding: 25px 15px;
}
.custom-hero-section {
    background: linear-gradient(135deg, rgba(0,0,0,0.8), rgba(0,0,0,0.65)),
                url('https://images.unsplash.com/photo-1575361204480-aadea25e6e68?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80');
    background-size: cover;
    background-position: center;
    border-radius: 28px;
    padding: 90px 25px;
    text-align: center;
    margin-bottom: 55px;
    overflow: hidden;
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
}
.custom-hero-section h1 {
    color: white;
    font-size: 3.2rem;
    margin-bottom: 20px;
    font-weight: 800;
}
.custom-hero-section p { color: #e2e8f0; max-width: 750px; margin: 0 auto; font-size: 1.15rem; }
.custom-section-title {
    font-size: 2.3rem;
    font-weight: 800;
    color: #1e293b;
    text-align: center;
    margin: 0 0 45px 0;
    position: relative;
    padding-bottom: 18px;
}
.custom-section-title:after {
    content: '';
    position: absolute;
    bottom: 0;
    right: 50%;
    transform: translateX(50%);
    width: 100px;
    height: 4px;
    background: linear-gradient(90deg, #f59e0b, #fbbf24, #f59e0b);
    border-radius: 2px;
}
.custom-stats-grid, .custom-features-grid, .custom-programs-grid, .custom-coaches-grid,
.custom-contact-wrapper, .custom-about-wrapper, .custom-mission-vision-grid, .custom-gallery-grid {
    display: grid;
    gap: 30px;
}
.custom-stats-grid { grid-template-columns: repeat(3, 1fr); margin-bottom: 65px; }
.custom-features-grid { grid-template-columns: repeat(3, 1fr); margin-bottom: 65px; }
.custom-programs-grid { grid-template-columns: repeat(2, 1fr); margin-bottom: 65px; }
.custom-coaches-grid { grid-template-columns: repeat(2, 1fr); margin-bottom: 65px; }
.custom-contact-wrapper { grid-template-columns: 1fr 1fr; }
.custom-about-wrapper { grid-template-columns: 1fr 1fr; align-items: center; margin-bottom: 55px; }
.custom-mission-vision-grid { grid-template-columns: 1fr 1fr; margin-top: 35px; }
.custom-gallery-grid { grid-template-columns: repeat(3, 1fr); margin-bottom: 40px; }

.custom-stat-card, .custom-feature-card, .custom-program-card, .custom-coach-card, .custom-contact-card,
.custom-news-card, .custom-gallery-item, .custom-registration-form-container {
    background: white;
    border-radius: 24px;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
    border: 1px solid #e2e8f0;
}
.custom-stat-card {
    padding: 40px 25px; text-align: center; transition: all 0.3s ease;
}
.custom-stat-number { font-size: 3.2rem; font-weight: 800; color: #1e3a8a; display: block; }
.custom-stat-label { color: #64748b; margin-top: 12px; font-weight: 600; font-size: 1.05rem; }

.custom-feature-card { padding: 40px 28px; text-align: center; transition: all 0.3s ease; }
.custom-feature-icon { font-size: 3.2rem; margin-bottom: 22px; }
.custom-feature-card h3 { color: #1e3a8a; margin-bottom: 18px; font-size: 1.4rem; font-weight: 700; }
.custom-feature-card p { color: #64748b; font-size: 0.95rem; line-height: 1.65; }

.custom-register-btn {
    background: linear-gradient(135deg, #f59e0b, #d97706, #f59e0b);
    color: white;
    padding: 18px 55px;
    border-radius: 60px;
    font-weight: 800;
    font-size: 1.25rem;
    border: none;
    cursor: pointer;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
}
.custom-program-header {
    height: 170px;
    background: linear-gradient(135deg, #3b82f6, #1e3a8a, #3b82f6);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 3.8rem;
    color: white;
    border-radius: 24px 24px 0 0;
}
.custom-program-body { padding: 28px; }
.custom-program-body h3 { color: #1e3a8a; margin-bottom: 18px; font-size: 1.5rem; font-weight: 700; }
.custom-schedule-box { background: #f8fafc; padding: 20px; border-radius: 18px; }
.custom-schedule-item {
    padding: 12px 0;
    border-bottom: 1px solid #e2e8f0;
    color: #334155;
    font-size: 1rem;
}

.custom-coach-card { overflow: hidden; text-align: center; transition: all 0.3s ease; }
.custom-coach-avatar {
    height: 220px;
    background: linear-gradient(135deg, #3b82f6, #1e3a8a, #3b82f6);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 4.5rem;
    color: white;
    border-radius: 24px 24px 0 0;
}
.custom-coach-info { padding: 28px; }
.custom-coach-info h3 { color: #1e3a8a; margin-bottom: 10px; font-size: 1.35rem; font-weight: 700; }
.custom-coach-title { color: #3b82f6; font-weight: 600; margin-bottom: 15px; }
.custom-coach-desc { color: #64748b; font-size: 0.9rem; line-height: 1.6; margin-top: 10px; }

.custom-page-header {
    background: linear-gradient(135deg, #1e3a8a, #3b82f6, #1e3a8a);
    border-radius: 28px;
    padding: 60px 25px;
    text-align: center;
    margin-bottom: 50px;
}
.custom-page-header h1 { color: white; font-size: 2.5rem; margin-bottom: 15px; }
.custom-page-header p { color: #e2e8f0; font-size: 1.05rem; }

.custom-about-image {
    background: linear-gradient(135deg, #3b82f6, #1e3a8a, #3b82f6);
    border-radius: 28px;
    height: 380px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 6.5rem;
    color: white;
}
.custom-mission-card, .custom-vision-card {
    padding: 35px;
    border-radius: 24px;
    transition: all 0.3s ease;
}
.custom-mission-card { background: linear-gradient(135deg, #f0f9ff, #e0f2fe); border-right: 6px solid #3b82f6; }
.custom-vision-card { background: linear-gradient(135deg, #fef3c7, #fde68a); border-right: 6px solid #f59e0b; }

.custom-registration-form-container {
    max-width: 750px;
    margin: 0 auto;
    padding: 40px;
}
.custom-success-message {
    background: linear-gradient(135deg, #10b981, #059669);
    color: white;
    padding: 18px;
    border-radius: 16px;
    margin-bottom: 25px;
    text-align: center;
    font-weight: 600;
}

.custom-contact-card { padding: 35px; }
.custom-contact-item {
    display: flex;
    align-items: center;
    gap: 18px;
    padding: 18px 0;
    border-bottom: 1px solid #e2e8f0;
}
.custom-contact-item:last-child { border-bottom: none; }
.custom-map-container {
    margin-top: 25px;
    border-radius: 18px;
    overflow: hidden;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.12);
}
.custom-map-container iframe {
    width: 100%;
    height: 260px;
    border: none;
}

.custom-news-card { padding: 25px; margin-bottom: 20px; border-right: 4px solid #f59e0b; }
.custom-gallery-item { overflow: hidden; transition: all 0.3s ease; }
.custom-gallery-image {
    height: 200px;
    background: linear-gradient(135deg, #3b82f6, #1e3a8a);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 3rem;
    color: white;
}
.custom-gallery-caption { padding: 15px; text-align: center; color: #334155; font-weight: 500; }

.custom-main-footer {
    background: linear-gradient(135deg, #1e293b, #0f172a, #1e293b);
    color: white;
    padding: 50px 0 30px;
    border-radius: 30px 30px 0 0;
    margin-top: 70px;
}
.custom-footer-grid {
    width: 90%;
    max-width: 1200px;
    margin: 0 auto;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 40px;
}
.custom-footer-link {
    color: #cbd5e1;
    text-decoration: none;
    display: inline-block;
}
.custom-footer-link:hover { color: #f59e0b; }

@media (max-width: 768px) {
    .custom-stats-grid, .custom-features-grid, .custom-programs-grid, .custom-coaches-grid,
    .custom-contact-wrapper, .custom-about-wrapper, .custom-mission-vision-grid, .custom-gallery-grid {
        grid-template-columns: 1fr;
    }
    .custom-hero-section { padding: 60px 20px; }
    .custom-hero-section h1 { font-size: 2rem; }
    .custom-section-title { font-size: 1.6rem; }
    .custom-stat-number { font-size: 2.2rem; }
    .custom-logo-text h1 { font-size: 1.2rem; }
    .custom-logo-image { width: 45px; height: 45px; }
    .custom-register-btn { padding: 14px 35px; font-size: 1rem; }
    .custom-page-header h1 { font-size: 1.8rem; }
}
</style>
""",
    unsafe_allow_html=True,
)

# ----------------------------
# Sidebar navigation
# ----------------------------
PAGE_LABELS = {
    "home": "🏠 الرئيسية",
    "about": "ℹ️ من نحن",
    "programs": "⚽ البرامج التدريبية",
    "coaches": "👨‍🏫 المدربون",
    "registration": "📝 تسجيل لاعب جديد",
    "faq": "❓ الأسئلة الشائعة",
    "contact": "📞 اتصل بنا",
    "gallery": "📸 معرض الصور",
    "news": "📰 الأخبار",
}
label_to_page = {v: k for k, v in PAGE_LABELS.items()}

with st.sidebar:
    st.markdown("### التنقل")
    selected_label = st.radio(
        "اختر صفحة",
        list(PAGE_LABELS.values()),
        index=list(PAGE_LABELS).index(st.session_state.page) if st.session_state.page in PAGE_LABELS else 0,
        label_visibility="collapsed",
    )
    st.caption("افتح القائمة الجانبية للتنقل بين الصفحات.")
    if st.button("العودة للرئيسية", use_container_width=True):
        go_to("home")

st.session_state.page = label_to_page.get(selected_label, "home")

# ----------------------------
# Page renderers
# ----------------------------
def render_header():
    st.markdown(
        f"""
<div class="custom-top-header">
    <div class="custom-header-container">
        <div class="custom-logo-wrapper">
            <div class="custom-logo-image">{logo_html}</div>
            <div class="custom-logo-text">
                <h1>الكوتش <span>أكاديمي</span></h1>
                <p>أكاديمية كرة القدم المتخصصة</p>
            </div>
        </div>
        <div style="text-align:left; color:#64748b; font-size:0.9rem;">
            عدد الزوار: {st.session_state.visitor_count} | آخر زيارة: {st.session_state.last_visit}
        </div>
    </div>
</div>
""",
        unsafe_allow_html=True,
    )
    st.markdown('<div style="height: 18px;"></div>', unsafe_allow_html=True)


def render_home():
    st.markdown(
        """
    <div class="custom-hero-section">
        <h1>⚽ الكوتش أكاديمي</h1>
        <p>أول أكاديمية متخصصة في مصر تركز على بناء اللاعب الشامل من الناحية الفنية والبدنية والنفسية، تحت إشراف مدربين معتمدين دوليًا.</p>
        <p style="font-weight: 700; margin-top: 22px; color: #fbbf24; font-size: 1.2rem;">نحن لا نصنع لاعبين فقط.. نحن نصنع قادة!</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        if st.button("📝 سجل ابنك الآن", use_container_width=True):
            go_to("registration")

    st.markdown('<div class="custom-section-title">إنجازات الأكاديمية</div>', unsafe_allow_html=True)
    st.markdown(
        """
    <div class="custom-stats-grid">
        <div class="custom-stat-card"><div style="font-size: 3.2rem;">👥</div><span class="custom-stat-number">500+</span><div class="custom-stat-label">لاعب مدرب</div></div>
        <div class="custom-stat-card"><div style="font-size: 3.2rem;">👨‍🏫</div><span class="custom-stat-number">12</span><div class="custom-stat-label">مدرب محترف</div></div>
        <div class="custom-stat-card"><div style="font-size: 3.2rem;">🏆</div><span class="custom-stat-number">150+</span><div class="custom-stat-label">لاعب محترف</div></div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="custom-section-title">لماذا تختار الكوتش أكاديمي؟</div>', unsafe_allow_html=True)
    st.markdown(
        """
    <div class="custom-features-grid">
        <div class="custom-feature-card"><div class="custom-feature-icon">🧠</div><h3>منهجية التدريب الذهني</h3><p>نركز على تطوير الذكاء الكروي والقدرة على اتخاذ القرارات السريعة والصحيحة داخل الملعب.</p></div>
        <div class="custom-feature-card"><div class="custom-feature-icon">🛡️</div><h3>بيئة آمنة محفزة</h3><p>نوفر بيئة تدريب آمنة تحترم الفروق الفردية وتشجع على الإبداع والتميز.</p></div>
        <div class="custom-feature-card"><div class="custom-feature-icon">🤝</div><h3>شراكات مع الأندية</h3><p>لدينا شراكات مع أندية محلية ودولية لتمكين الموهوبين من الانضمام للمنتخبات والأندية الكبرى.</p></div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="custom-section-title">أحدث الأخبار</div>', unsafe_allow_html=True)
    news_preview = [
        {"title": "بدء التسجيل للموسم الجديد 2025", "date": "2025-01-15"},
        {"title": "فوز فريق الأكاديمية ببطولة أسيوط", "date": "2025-01-10"},
        {"title": "محاضرة تدريبية للمدربين", "date": "2025-01-05"},
    ]
    cols = st.columns(3)
    for idx, news in enumerate(news_preview):
        with cols[idx]:
            st.markdown(
                f"""
                <div class="custom-news-card" style="text-align:center;">
                    <h4 style="color:#1e3a8a;">📌 {news['title']}</h4>
                    <p style="color:#64748b; font-size:0.8rem;">{news['date']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_about():
    st.markdown(
        """
    <div class="custom-page-header">
        <h1>من نحن</h1>
        <p>الكوتش أكاديمي.. رؤية جديدة في عالم تدريب كرة القدم</p>
    </div>
    """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
    <div class="custom-about-wrapper">
        <div class="custom-about-image">⚽</div>
        <div>
            <h2 style="color:#1e3a8a; font-size:1.9rem; margin-bottom:22px;">تأسيس الأكاديمية</h2>
            <p style="color:#334155; font-size:1rem; line-height:1.7;">تأسست الأكاديمية عام 2020 على يد نخبة من المدربين المتخصصين:</p>
            <ul style="margin-right:25px; margin-top:18px; color:#334155; font-size:1rem;">
                <li>كابتن ميخائيل كميل رؤف (ميخا) - المدير الفني</li>
                <li>كابتن اندرو - مدرب مهارات</li>
                <li>كابتن مينا - مدرب لياقة بدنية</li>
            </ul>
            <p style="margin-top:22px; color:#334155;">على ملاعب مدرسة السلام المتطورة - أسيوط</p>
            <p style="margin-top:18px; font-weight:700; color:#1e3a8a; font-size:1.05rem;">بدعم من الأب الروحي للأكاديمية: مستر / مؤنس منير</p>
        </div>
    </div>
    <div class="custom-mission-vision-grid">
        <div class="custom-mission-card">
            <h3 style="color:#1e3a8a; font-size:1.6rem; margin-bottom:18px;">🎯 رسالتنا</h3>
            <p style="color:#334155; line-height:1.7;">تطوير جيل جديد من اللاعبين المبدعين القادرين على التألق محليًا ودوليًا، من خلال تدريب عصري يعتمد على أحدث الأساليب العلمية والتكنولوجية، مع غرس القيم والأخلاق الرياضية.</p>
        </div>
        <div class="custom-vision-card">
            <h3 style="color:#1e3a8a; font-size:1.6rem; margin-bottom:18px;">👁️ رؤيتنا</h3>
            <p style="color:#334155; line-height:1.7;">أن نكون الوجهة الأولى لأي موهبة كروية في مصر والوطن العربي، والجسر الذي يعبر من خلاله اللاعبون الموهوبون إلى العالمية.</p>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
    <div style="margin-top:45px; padding:30px; background:linear-gradient(135deg, #1e3a8a, #3b82f6); border-radius:28px; text-align:center; color:white;">
        <h3 style="font-size:1.8rem;">📊 أرقام وإحصائيات</h3>
        <div style="display:grid; grid-template-columns:repeat(4, 1fr); gap:20px; margin-top:30px;">
            <div><div style="font-size:2rem;">🎓</div><div style="font-weight:bold;">4+</div><div>سنوات من التميز</div></div>
            <div><div style="font-size:2rem;">👥</div><div style="font-weight:bold;">500+</div><div>لاعب تم تدريبهم</div></div>
            <div><div style="font-size:2rem;">🏆</div><div style="font-weight:bold;">25+</div><div>بطولة محلية</div></div>
            <div><div style="font-size:2rem;">⭐</div><div style="font-weight:bold;">150+</div><div>لاعب محترف</div></div>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )


def render_programs():
    st.markdown(
        """
    <div class="custom-page-header">
        <h1>البرامج التدريبية</h1>
        <p>مواعيد تدريبية مصممة لكل فئة عمرية وجنسية</p>
    </div>
    """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
    <div class="custom-programs-grid">
        <div class="custom-program-card">
            <div class="custom-program-header">📅 السبت</div>
            <div class="custom-program-body">
                <h3>مواعيد تدريب السبت</h3>
                <div class="custom-schedule-box">
                    <div class="custom-schedule-item"><strong>🕔 ٥:٠٠ - ٦:٠٠ م</strong> → 🏃‍♀️ بنات (جميع الأعمار)</div>
                    <div class="custom-schedule-item"><strong>🕕 ٦:٠٠ - ٧:٣٠ م</strong> → 🏃 بنين (الصف الأول - الخامس الابتدائي)</div>
                    <div class="custom-schedule-item"><strong>🕢 ٧:٣٠ - ٩:٠٠ م</strong> → 🏃 بنين (الصف السادس الابتدائي - الثاني الإعدادي)</div>
                    <div style="margin-top:18px; color:#64748b; font-size:0.9rem;">📍 ملاعب مدرسة السلام المتطورة - أسيوط</div>
                </div>
            </div>
        </div>
        <div class="custom-program-card">
            <div class="custom-program-header">✅ الخميس</div>
            <div class="custom-program-body">
                <h3>مواعيد تدريب الخميس</h3>
                <div class="custom-schedule-box">
                    <div class="custom-schedule-item"><strong>🕟 ٤:٣٠ - ٦:٠٠ م</strong> → 🏃‍♀️ بنات (جميع الأعمار)</div>
                    <div class="custom-schedule-item"><strong>🕕 ٦:٠٠ - ٨:٠٠ م</strong> → 🏃 بنين (الصف الأول - الخامس الابتدائي)</div>
                    <div class="custom-schedule-item"><strong>🕗 ٨:٠٠ - ١٠:٠٠ م</strong> → 🏃 بنين (الصف السادس الابتدائي - الثاني الإعدادي)</div>
                    <div style="margin-top:18px; color:#64748b; font-size:0.9rem;">📍 ملاعب مدرسة السلام المتطورة - أسيوط</div>
                </div>
            </div>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
    <div class="custom-program-card" style="margin-top:25px;">
        <div class="custom-program-header">⚽ معلومات عامة عن البرامج</div>
        <div class="custom-program-body">
            <h3>تفاصيل البرامج التدريبية</h3>
            <div class="custom-schedule-box">
                <h4 style="color:#1e3a8a; margin-bottom:15px; font-size:1.2rem;">🎯 أهداف التدريب:</h4>
                <ul style="margin-right:20px; margin-bottom:20px;">
                    <li>تنمية المهارات الفنية الأساسية (التمرير - الاستلام - المراوغة - التسديد)</li>
                    <li>تطوير القدرات البدنية (السرعة - الرشاقة - القوة - التحمل)</li>
                    <li>تعزيز العمل الجماعي والانضباط التكتيكي</li>
                    <li>بناء الشخصية الرياضية والثقة بالنفس</li>
                    <li>تطوير الذكاء الكروي والقدرة على القراءة التحليلية للملعب</li>
                </ul>
                <h4 style="color:#1e3a8a; margin-bottom:15px; font-size:1.2rem;">💼 ما يقدمه النادي للاعبين:</h4>
                <ul style="margin-right:20px;">
                    <li>ملابس تدريب رسمية (قميص - شورت - جوارب)</li>
                    <li>مسابقات دورية داخلية وخارجية</li>
                    <li>تقييمات شهرية وتقارير تطور الأداء</li>
                    <li>فيديوهات تحليل أداء للاعبين المتميزين</li>
                    <li>فرص احتراف في الأندية الكبرى</li>
                    <li>تأمين صحي للاعبين أثناء التدريبات</li>
                </ul>
            </div>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )
    if st.button("سجل الآن", use_container_width=True):
        go_to("registration")


def render_coaches():
    st.markdown(
        """
    <div class="custom-page-header">
        <h1>المدربون</h1>
        <p>فريقنا من المدربين المحترفين ذوي الخبرة والكفاءة</p>
    </div>
    """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
    <div class="custom-coaches-grid">
        <div class="custom-coach-card">
            <div class="custom-coach-avatar">👨‍🏫</div>
            <div class="custom-coach-info">
                <h3>كابتن/ميخائيل كميل رؤف</h3>
                <div class="custom-coach-title">المدير الفني - مدرب معتمد (CAF)</div>
                <div class="custom-coach-desc">🎓 بكالريوس تربية رياضية<br>📜 رخصة تدريب CAF لمراحل البراعم<br>📜 دبلومة الإعداد البدني المتقدم<br>📜 دبلومة إصابات الملاعب والعلاج الطبيعي<br>🏫 مدرس تربية رياضية بمدارس السلام الخاصة</div>
            </div>
        </div>
        <div class="custom-coach-card">
            <div class="custom-coach-avatar">🧤</div>
            <div class="custom-coach-info">
                <h3>كابتن أحمد علي</h3>
                <div class="custom-coach-title">مدرب حراس مرمى - معتمد (CAF)</div>
                <div class="custom-coach-desc">🎓 بكالريوس تربية رياضية<br>📜 رخصة تدريب حراس مرمى CAF<br>📜 خبرة 15 عامًا في تدريب حراس المرمى<br>📜 عمل مع عدة أندية في الدوري المصري</div>
            </div>
        </div>
        <div class="custom-coach-card">
            <div class="custom-coach-avatar">🏃</div>
            <div class="custom-coach-info">
                <h3>د. خالد السيد</h3>
                <div class="custom-coach-title">مدرب لياقة بدنية - دكتوراه</div>
                <div class="custom-coach-desc">🎓 دكتوراه في علوم الرياضة<br>📜 أستاذ مساعد بكلية التربية الرياضية<br>📜 مختص في تطوير قدرات الناشئين<br>📜 مدرب لياقة معتمد من الاتحاد المصري</div>
            </div>
        </div>
        <div class="custom-coach-card">
            <div class="custom-coach-avatar">⚽</div>
            <div class="custom-coach-info">
                <h3>كابتن محمد جابر</h3>
                <div class="custom-coach-title">مدرب مهارات فنية - معتمد (CAF)</div>
                <div class="custom-coach-desc">🎓 بكالريوس تربية رياضية<br>📜 رخصة تدريب مهارات CAF<br>📜 خبرة 12 عامًا في تدريب المهارات الفنية<br>📜 حاصل على دورات متقدمة في تدريب الناشئين</div>
            </div>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
    <div style="background: linear-gradient(135deg, #1e3a8a, #3b82f6); border-radius: 28px; padding: 40px; text-align: center; color: white;">
        <h3 style="font-size: 1.8rem;">🌟 فريق تدريب متكامل</h3>
        <p style="margin-top: 15px;">يجمع فريقنا بين الخبرات الأكاديمية والعملية لضمان أفضل تدريب للاعبين</p>
        <div style="display: flex; justify-content: center; gap: 20px; margin-top: 25px;">
            <div><span style="font-size: 1.5rem;">12+</span><br>مدرب معتمد</div>
            <div><span style="font-size: 1.5rem;">100+</span><br>دورة تدريبية</div>
            <div><span style="font-size: 1.5rem;">20+</span><br>سنة خبرة</div>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )


def render_registration():
    st.markdown(
        """
    <div class="custom-page-header">
        <h1>تسجيل لاعب جديد</h1>
        <p>انضم إلى الكوتش أكاديمي وابدأ رحلتك نحو الاحتراف</p>
    </div>
    """,
        unsafe_allow_html=True,
    )
    if st.session_state.show_success:
        st.markdown(
            '<div class="custom-success-message">✅ تم إرسال طلب التسجيل بنجاح! سنتواصل معكم خلال 24 ساعة.</div>',
            unsafe_allow_html=True,
        )
        st.session_state.show_success = False

    with st.form("registration_form"):
        st.markdown("### 📋 معلومات اللاعب")
        col1, col2 = st.columns(2)
        with col1:
            player_name = st.text_input("اسم اللاعب الثلاثي *", placeholder="مثال: محمد أحمد محمود")
            birth_date = st.date_input("تاريخ الميلاد *", None)
            previous_club = st.text_input("النادي السابق (إن وجد)", placeholder="اسم النادي السابق")
        with col2:
            age_group = st.selectbox(
                "الفئة العمرية المطلوبة *",
                ["", "🏃‍♀️ بنات (جميع الأعمار)", "🏃 بنين (الصف الأول - الخامس الابتدائي)", "🏃 بنين (الصف السادس الابتدائي - الثاني الإعدادي)"],
            )
            position = st.selectbox("المركز المفضل", ["", "حارس مرمى", "مدافع", "لاعب وسط", "مهاجم", "أكثر من مركز"])
            shirt_size = st.selectbox("مقاس القميص", ["", "XS", "S", "M", "L", "XL", "XXL"])

        st.markdown("### 👨‍👩‍👦 معلومات ولي الأمر")
        col1, col2 = st.columns(2)
        with col1:
            parent_name = st.text_input("اسم ولي الأمر *", placeholder="مثال: أحمد محمود")
            parent_phone = st.text_input("رقم الهاتف *", placeholder="01XXXXXXXXX")
        with col2:
            parent_whatsapp = st.text_input("رقم الواتساب (للتواصل السريع)", placeholder="01XXXXXXXXX")
            parent_email = st.text_input("البريد الإلكتروني", placeholder="example@email.com")

        st.markdown("### 📍 معلومات إضافية")
        address = st.text_area("العنوان بالكامل", height=70, placeholder="المدينة - الحي - الشارع - رقم المنزل")
        col1, col2 = st.columns(2)
        with col1:
            medical_notes = st.text_area("ملاحظات طبية (إن وجدت)", height=60, placeholder="حساسية - أمراض مزمنة - إصابات سابقة")
        with col2:
            notes = st.text_area("ملاحظات إضافية (اختياري)", height=60, placeholder="أي معلومات إضافية تود إضافتها...")

        st.markdown("### 📅 مواعيد التدريب المناسبة")
        training_days = st.multiselect("اختر أيام التدريب المناسبة", ["السبت", "الخميس", "كلا اليومين"])

        st.markdown("### 📄 موافقة ولي الأمر")
        terms = st.checkbox("أقر بأن جميع البيانات المقدمة صحيحة، وأوافق على سياسات وشروط الأكاديمية *")

        submitted = st.form_submit_button("📝 تقديم طلب التسجيل", use_container_width=True)

        if submitted:
            if player_name and age_group and parent_name and parent_phone and terms:
                data = {
                    "playerName": player_name,
                    "ageGroup": age_group,
                    "birthDate": str(birth_date) if birth_date else "",
                    "previousClub": previous_club,
                    "position": position,
                    "shirtSize": shirt_size,
                    "parentName": parent_name,
                    "parentPhone": parent_phone,
                    "parentWhatsapp": parent_whatsapp,
                    "parentEmail": parent_email,
                    "address": address,
                    "medicalNotes": medical_notes,
                    "notes": notes,
                    "trainingDays": training_days,
                    "registrationDate": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }
                if save_registration(data):
                    st.session_state.show_success = True
                    st.rerun()
                else:
                    st.error("❌ حدث خطأ في حفظ البيانات، يرجى المحاولة مرة أخرى")
            elif not terms:
                st.error("⚠️ يرجى الموافقة على سياسات وشروط الأكاديمية")
            else:
                st.error("⚠️ يرجى ملء جميع الحقول المطلوبة")


def render_faq():
    st.markdown(
        """
    <div class="custom-page-header">
        <h1>الأسئلة الشائعة</h1>
        <p>إجابات على أكثر الأسئلة شيوعًا من أولياء الأمور</p>
    </div>
    """,
        unsafe_allow_html=True,
    )
    faqs = [
        ("ما الذي يميز الكوتش أكاديمي عن غيرها من الأكاديميات؟", "الكوتش أكاديمي تتبنى منهجية تدريب متكاملة وشاملة تركز على عدة محاور: التدريب الذهني، المتابعة الفردية، استخدام التكنولوجيا الحديثة، شراكات مع أندية محلية ودولية، ومدربين معتمدين دوليًا من CAF."),
        ("ما هي مدة التدريب وأوقاته؟", "الموسم التدريبي يمتد لمدة 10 أشهر، من بداية سبتمبر إلى نهاية يونيو. التدريبات تقام في الفترة المسائية أيام السبت والخميس حسب الجدول المحدد لكل فئة عمرية."),
        ("ما هي تكلفة الاشتراك وآلية الدفع؟", "تختلف التكلفة حسب الفئة العمرية وعدد أيام التدريب في الأسبوع. نقدم خصومات خاصة للأشقاء، ونظام تقسيط شهري مرن، ومنحًا جزئية للمتميزين، وخصمًا للتسجيل المبكر."),
        ("ما هي متطلبات الانضمام للأكاديمية؟", "نحتاج إلى إكمال نموذج التسجيل، وأن يكون اللاعب في الفئة العمرية المناسبة، والالتزام بمواعيد التدريب، وتقديم شهادة ميلاد وصورة شخصية حديثة، ودفع رسوم الاشتراك."),
        ("هل هناك تدريبات خاصة للمبتدئين؟", "نعم، لدينا برامج خاصة للمبتدئين تركز على تعلم الأساسيات، تطوير المهارات الحركية، بناء الثقة بالنفس، وتعزيز العمل الجماعي."),
        ("كيف يمكن متابعة تطور اللاعب داخل الأكاديمية؟", "نوفر تقييمًا فنيًا دوريًا، وتقارير شهرية، ولقاءات دورية مع أولياء الأمور، وفيديوهات تحليل أداء للاعبين المتميزين."),
        ("ماذا عن السلامة والإصابات خلال التدريب؟", "السلامة أولوية قصوى، ونوفر إشرافًا مستمرًا، وبيئة آمنة، وإحماءً وتبريدًا مناسبين، ومدربين حاصلين على الإسعافات الأولية، وتأمينًا صحيًا أثناء التدريب."),
        ("هل يوجد تدريبات مخصصة للبنات؟", "نعم، لدينا برامج تدريبية مخصصة للبنات في أيام السبت والخميس، مع مدربات مؤهلات وبيئة مناسبة ومراعاة خصوصية كاملة."),
        ("هل توجد وسائل نقل للاعبين؟", "حالياً لا نوفر خدمات نقل للاعبين، لكن يمكن لأولياء الأمور توصيل أبنائهم إلى ملاعب التدريب."),
        ("ما هي شروط الانسحاب واسترداد الرسوم؟", "استرداد كامل خلال أول أسبوعين من بداية الموسم، واسترداد 50% خلال الشهر الأول، ولا يوجد استرداد بعد انقضاء الشهر الأول."),
        ("هل يوجد عروض خاصة للأشقاء؟", "نعم، نقدم خصم 15% للشقيق الثاني، وخصم 25% للشقيق الثالث، وخصم 30% لأكثر من ثلاثة أشقاء."),
    ]
    for q, a in faqs:
        with st.expander(f"❓ {q}"):
            st.markdown(f'<p style="color:#334155; line-height:1.7; font-size:0.95rem;">{a}</p>', unsafe_allow_html=True)

    st.markdown(
        """
    <div style="margin-top:40px; background:linear-gradient(135deg, #f0f9ff, #e0f2fe); border-radius:24px; padding:30px; text-align:center;">
        <h3 style="color:#1e3a8a;">❗ لم تجد سؤالك؟</h3>
        <p style="color:#334155; margin:15px 0;">تواصل معنا وسنقوم بالرد عليك في أقرب وقت</p>
    </div>
    """,
        unsafe_allow_html=True,
    )
    if st.button("اتصل بنا", use_container_width=True):
        go_to("contact")


def render_contact():
    st.markdown(
        """
    <div class="custom-page-header">
        <h1>اتصل بنا</h1>
        <p>تواصل معنا لأي استفسارات أو معلومات إضافية</p>
    </div>
    """,
        unsafe_allow_html=True,
    )
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
        <div class="custom-contact-card">
            <h3 style="color:#1e3a8a; margin-bottom:28px; font-size:1.5rem;">📞 معلومات الاتصال</h3>
            <div class="custom-contact-item"><div style="font-size:1.6rem;">📱</div><div><strong>الهاتف:</strong><br><a href="tel:01069238878" style="text-decoration:none; color:#334155; font-size:1.1rem;">01069238878</a></div></div>
            <div class="custom-contact-item"><div style="font-size:1.6rem;">💬</div><div><strong>الواتساب:</strong><br><a href="https://wa.me/201285197778" target="_blank" style="text-decoration:none; color:#25D366; font-size:1.1rem;">01285197778</a></div></div>
            <div class="custom-contact-item"><div style="font-size:1.6rem;">📍</div><div><strong>العنوان الرئيسي:</strong><br>محافظة أسيوط - مصر<br>على ملاعب مدرسة السلام المتطورة</div></div>
            <div class="custom-contact-item"><div style="font-size:1.6rem;">⏰</div><div><strong>أوقات العمل والإجابة على الاستفسارات:</strong><br>السبت والخميس: 4:00 مساءً - 9:00 مساءً<br>باقي الأيام: متاح للرد من 10ص - 10م</div></div>
            <div class="custom-contact-item"><div style="font-size:1.6rem;">📧</div><div><strong>البريد الإلكتروني:</strong><br>info@elcoach-academy.com<br>support@elcoach-academy.com</div></div>
        </div>
        <div class="custom-map-container">
            <iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d113686.258448786!2d31.156289!3d27.186696!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x1438a5f5c5b5b5b5%3A0x5b5b5b5b5b5b5b5b!2z2YXZg9mF2YrYp9mG2Ykg2KfZhNiq2YbYqSDYp9mE2YXYqtmG2Kkg2KfZhNir2YTYp9mG2Ykg2KfZhNi52YjYp9mG!5e0!3m2!1sar!2seg!4v1700000000000!5m2!1sar!2seg" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
        <div class="custom-contact-card">
            <h3 style="color:#1e3a8a; margin-bottom:28px; font-size:1.5rem;">✉️ أرسل رسالة</h3>
            <p style="color:#64748b; margin-bottom:20px;">سنقوم بالرد عليك في أقرب وقت ممكن خلال 24 ساعة</p>
        </div>
        """,
            unsafe_allow_html=True,
        )
        with st.form("contact_form"):
            c_name = st.text_input("الاسم الكامل *")
            c_phone = st.text_input("رقم الهاتف *", placeholder="01XXXXXXXXX")
            c_email = st.text_input("البريد الإلكتروني", placeholder="example@email.com")
            c_subject = st.selectbox("نوع الاستفسار *", ["", "استفسار عام", "معلومات عن البرامج", "التسجيل والاشتراك", "شكوى أو اقتراح", "طلب شراكة أو رعاية", "أخرى"])
            c_msg = st.text_area("الرسالة *", height=130, placeholder="اكتب رسالتك هنا بتفصيل...")
            submitted = st.form_submit_button("📨 إرسال الرسالة", use_container_width=True)
            if submitted:
                if c_name and c_phone and c_subject and c_msg:
                    data = {
                        "name": c_name,
                        "phone": c_phone,
                        "email": c_email,
                        "subject": c_subject,
                        "message": c_msg,
                        "contactDate": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    }
                    if save_contact(data):
                        st.success("✅ شكراً لتواصلك! تم إرسال رسالتك بنجاح وسنرد عليك خلال 24 ساعة.")
                    else:
                        st.error("❌ حدث خطأ في حفظ البيانات، يرجى المحاولة مرة أخرى")
                else:
                    st.error("⚠️ يرجى ملء جميع الحقول المطلوبة")

        st.markdown(
            """
        <div class="custom-contact-card" style="margin-top:25px;">
            <h3 style="color:#1e3a8a; margin-bottom:20px;">🌐 تابعنا على وسائل التواصل</h3>
            <div style="display:flex; gap:15px; justify-content:center;">
                <div style="width:45px; height:45px; background:#1877f2; border-radius:50%; display:flex; align-items:center; justify-content:center;">📘</div>
                <div style="width:45px; height:45px; background:#1da1f2; border-radius:50%; display:flex; align-items:center; justify-content:center;">🐦</div>
                <div style="width:45px; height:45px; background:#e4405f; border-radius:50%; display:flex; align-items:center; justify-content:center;">📷</div>
                <div style="width:45px; height:45px; background:#25d366; border-radius:50%; display:flex; align-items:center; justify-content:center;">💬</div>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )


def render_gallery():
    st.markdown(
        """
    <div class="custom-page-header">
        <h1>📸 معرض الصور</h1>
        <p>لحظات من التدريبات والمباريات في الكوتش أكاديمي</p>
    </div>
    """,
        unsafe_allow_html=True,
    )
    gallery_items = [
        {"icon": "⚽", "title": "تدريبات يومية", "desc": "تمارين المهارات الفنية"},
        {"icon": "🏃", "title": "تدريبات لياقة", "desc": "تطوير القدرات البدنية"},
        {"icon": "🏆", "title": "المباريات", "desc": "مباريات دورية داخلية"},
        {"icon": "👨‍🏫", "title": "فريق المدربين", "desc": "مدربون معتمدون دوليًا"},
        {"icon": "🎓", "title": "تكريم اللاعبين", "desc": "تكريم المتميزين شهريًا"},
        {"icon": "🤝", "title": "فعاليات خاصة", "desc": "أنشطة ترفيهية وتعليمية"},
        {"icon": "🏅", "title": "البطولات", "desc": "مشاركات خارجية"},
        {"icon": "📊", "title": "محاضرات نظرية", "desc": "تطوير الجانب المعرفي"},
        {"icon": "🎉", "title": "احتفالات", "desc": "مناسبات واحتفالات"},
    ]
    cols = st.columns(3)
    for i, item in enumerate(gallery_items):
        with cols[i % 3]:
            st.markdown(
                f"""
            <div class="custom-gallery-item">
                <div class="custom-gallery-image">{item['icon']}</div>
                <div class="custom-gallery-caption">
                    <h4 style="color:#1e3a8a;">{item['title']}</h4>
                    <p style="font-size:0.85rem; color:#64748b;">{item['desc']}</p>
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )
    st.markdown(
        """
    <div style="text-align:center; margin-top:40px; padding:30px; background:linear-gradient(135deg, #f0f9ff, #e0f2fe); border-radius:24px;">
        <p style="color:#1e3a8a; font-size:1.1rem;">📸 يتم تحديث المعرض باستمرار بأحدث صور التدريبات والمباريات</p>
        <p style="color:#64748b; margin-top:10px;">تابعونا على وسائل التواصل الاجتماعي لمشاهدة المزيد من اللحظات المميزة</p>
    </div>
    """,
        unsafe_allow_html=True,
    )


def render_news():
    st.markdown(
        """
    <div class="custom-page-header">
        <h1>📰 آخر الأخبار</h1>
        <p>أحدث المستجدات والإعلانات من الكوتش أكاديمي</p>
    </div>
    """,
        unsafe_allow_html=True,
    )
    news_items = [
        {"title": "بدء التسجيل للموسم الجديد 2025", "date": "2025-01-15", "content": "يعلن الكوتش أكاديمي عن بدء التسجيل للموسم الجديد 2025. خصومات خاصة للمسجلين المبكرين حتى نهاية فبراير. للتسجيل يرجى زيارة صفحة التسجيل أو الاتصال بنا.", "author": "إدارة الأكاديمية"},
        {"title": "فوز فريق الأكاديمية ببطولة أسيوط", "date": "2025-01-10", "content": "حقق فريق تحت 12 سنة فوزًا مستحقًا في بطولة أسيوط الرمضانية بعد تفوقه على 8 فرق. تألق لاعبو الأكاديمية وأظهروا مستويات متميزة طوال البطولة.", "author": "كابتن ميخا"},
        {"title": "محاضرة تدريبية للمدربين", "date": "2025-01-05", "content": "أقيمت محاضرة تدريبية للمدربين حول أحدث أساليب التدريب الحديثة بحضور خبراء من الاتحاد المصري لكرة القدم.", "author": "كابتن أحمد علي"},
        {"title": "دورة تدريبية لحراس المرمى", "date": "2024-12-05", "content": "انطلقت دورة تدريبية متخصصة لحراس المرمى تحت إشراف كابتن أحمد علي، تشمل التدريبات النظرية والتطبيقية.", "author": "إدارة التدريب"},
        {"title": "اتفاقية تعاون مع نادي الزمالك", "date": "2024-11-28", "content": "وقع الكوتش أكاديمي اتفاقية تعاون مع نادي الزمالك لاكتشاف المواهب وتأهيلها للانضمام لقطاع الناشئين بالنادي.", "author": "الإدارة التنفيذية"},
    ]
    for news in news_items:
        st.markdown(
            f"""
        <div class="custom-news-card">
            <h3 style="color:#1e3a8a; margin-bottom:10px;">📌 {news['title']}</h3>
            <div style="display:flex; gap:15px; margin-bottom:12px;">
                <p style="color:#64748b; font-size:0.85rem;">📅 {news['date']}</p>
                <p style="color:#f59e0b; font-size:0.85rem;">✍️ {news['author']}</p>
            </div>
            <p style="color:#334155; line-height:1.6;">{news['content']}</p>
        </div>
        """,
            unsafe_allow_html=True,
        )
    if st.button("سجل الآن في الأكاديمية", use_container_width=True):
        go_to("registration")


def render_footer():
    st.markdown(
        """
    <div class="custom-main-footer">
        <div class="custom-footer-grid">
            <div>
                <h3>الكوتش أكاديمي</h3>
                <p style="color:#cbd5e1; margin-top:12px;">أكاديمية كرة القدم المتخصصة في بناء اللاعب الشامل.</p>
            </div>
            <div>
                <h4>روابط سريعة</h4>
                <div style="display:grid; gap:8px; margin-top:12px;">
                    <span class="custom-footer-link">الرئيسية</span>
                    <span class="custom-footer-link">البرامج التدريبية</span>
                    <span class="custom-footer-link">التسجيل</span>
                    <span class="custom-footer-link">اتصل بنا</span>
                </div>
            </div>
            <div>
                <h4>تواصل معنا</h4>
                <p style="color:#cbd5e1; margin-top:12px;">01069238878</p>
                <p style="color:#cbd5e1;">01285197778</p>
            </div>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )


render_header()

page = st.session_state.page
if page == "home":
    render_home()
elif page == "about":
    render_about()
elif page == "programs":
    render_programs()
elif page == "coaches":
    render_coaches()
elif page == "registration":
    render_registration()
elif page == "faq":
    render_faq()
elif page == "contact":
    render_contact()
elif page == "gallery":
    render_gallery()
elif page == "news":
    render_news()
else:
    st.session_state.page = "home"
    render_home()

render_footer()
