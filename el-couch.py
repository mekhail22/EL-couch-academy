import streamlit as st
import json
import os
from datetime import datetime
import base64

# إعدادات الصفحة
st.set_page_config(
    page_title="الكوتش أكاديمي",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ===== CSS كامل مع JavaScript =====
st.markdown("""
<style>
    /* إخفاء كل عناصر Streamlit */
    header, .stApp > header, .st-emotion-cache-18ni7ap, .st-emotion-cache-1v0mbdj, #MainMenu, footer {
        display: none !important;
    }
    
    .main .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }
    
    .stApp {
        background-color: white !important;
    }
    
    /* تنسيق عام */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* ===== الهيدر ===== */
    .main-header {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        background: white;
        box-shadow: 0 2px 15px rgba(0, 0, 0, 0.08);
        z-index: 1000;
        padding: 10px 0;
    }
    
    .header-inner {
        width: 95%;
        max-width: 1200px;
        margin: 0 auto;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    /* الشعار */
    .logo-area {
        display: flex;
        align-items: center;
        gap: 15px;
    }
    
    .logo-img {
        width: 60px;
        height: 60px;
        border-radius: 15px;
        object-fit: cover;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
    }
    
    .logo-text h1 {
        font-size: 2rem;
        margin: 0;
        color: #1e3a8a;
        font-weight: 800;
    }
    
    .logo-text span {
        color: #f59e0b;
    }
    
    .logo-text p {
        font-size: 0.85rem;
        color: #666;
        margin: 0;
    }
    
    /* ===== برجر منيو ===== */
    .burger-btn {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        width: 35px;
        height: 25px;
        background: transparent;
        border: none;
        cursor: pointer;
        padding: 0;
        z-index: 1002;
    }
    
    .burger-btn span {
        display: block;
        width: 100%;
        height: 3px;
        background-color: #1e3a8a;
        border-radius: 3px;
        transition: all 0.3s ease;
    }
    
    .burger-btn.active span:nth-child(1) {
        transform: rotate(45deg) translate(8px, 8px);
    }
    
    .burger-btn.active span:nth-child(2) {
        opacity: 0;
    }
    
    .burger-btn.active span:nth-child(3) {
        transform: rotate(-45deg) translate(8px, -8px);
    }
    
    /* ===== القائمة الجانبية ===== */
    .side-menu {
        position: fixed;
        top: 0;
        right: -300px;
        width: 280px;
        height: 100vh;
        background: white;
        box-shadow: -5px 0 25px rgba(0, 0, 0, 0.15);
        z-index: 1001;
        transition: right 0.3s ease;
        padding-top: 80px;
        overflow-y: auto;
    }
    
    .side-menu.open {
        right: 0;
    }
    
    .side-menu ul {
        list-style: none;
        padding: 0 20px;
    }
    
    .side-menu li {
        margin-bottom: 8px;
    }
    
    .side-menu a {
        display: flex;
        align-items: center;
        gap: 15px;
        padding: 14px 18px;
        color: #1e293b;
        text-decoration: none;
        font-weight: 600;
        border-radius: 12px;
        transition: all 0.3s ease;
        cursor: pointer;
        font-size: 16px;
    }
    
    .side-menu a:hover {
        background-color: #eff6ff;
        color: #2563eb;
    }
    
    /* طبقة التعتيم */
    .menu-overlay {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-color: rgba(0, 0, 0, 0.5);
        z-index: 999;
        display: none;
    }
    
    .menu-overlay.show {
        display: block;
    }
    
    /* مساحة تعويضية */
    .header-spacer {
        height: 85px;
    }
    
    /* ===== حاوية المحتوى ===== */
    .content-wrapper {
        width: 95%;
        max-width: 1200px;
        margin: 0 auto;
        padding: 20px 15px;
    }
    
    /* ===== القسم الرئيسي ===== */
    .hero-section {
        background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.6)), url('https://images.unsplash.com/photo-1575361204480-aadea25e6e68?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80');
        background-size: cover;
        background-position: center;
        border-radius: 20px;
        padding: 80px 20px;
        text-align: center;
        margin-bottom: 50px;
    }
    
    .hero-section h1 {
        color: white;
        font-size: 2.8rem;
        margin-bottom: 20px;
        font-weight: 800;
    }
    
    .hero-section p {
        color: #e2e8f0;
        max-width: 700px;
        margin: 0 auto;
        font-size: 1.1rem;
    }
    
    /* العناوين الرئيسية */
    .section-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #1e293b;
        text-align: center;
        margin-bottom: 40px;
        position: relative;
        padding-bottom: 15px;
    }
    
    .section-title:after {
        content: '';
        position: absolute;
        bottom: 0;
        right: 50%;
        transform: translateX(50%);
        width: 80px;
        height: 4px;
        background-color: #f59e0b;
        border-radius: 2px;
    }
    
    /* بطاقات الإحصائيات */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 30px;
        margin-bottom: 60px;
    }
    
    .stat-card {
        background: white;
        padding: 35px 20px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
        border: 1px solid #e2e8f0;
    }
    
    .stat-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.12);
    }
    
    .stat-number {
        font-size: 3rem;
        font-weight: 800;
        color: #1e3a8a;
        display: block;
    }
    
    .stat-label {
        color: #4b5563;
        margin-top: 10px;
        font-weight: 600;
        font-size: 1.1rem;
    }
    
    /* بطاقات المميزات */
    .features-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 30px;
        margin-bottom: 60px;
    }
    
    .feature-card {
        background: #f8fafc;
        padding: 35px 25px;
        border-radius: 20px;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 20px;
    }
    
    .feature-card h3 {
        color: #1e3a8a;
        margin-bottom: 15px;
        font-size: 1.4rem;
        font-weight: 700;
    }
    
    .feature-card p {
        color: #4b5563;
        font-size: 1rem;
        line-height: 1.6;
    }
    
    /* زر مخصص */
    .custom-btn {
        background-color: #f59e0b;
        color: #1e293b;
        padding: 16px 50px;
        border-radius: 50px;
        font-weight: 800;
        font-size: 1.2rem;
        border: none;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    .custom-btn:hover {
        background-color: #d97706;
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
    }
    
    /* بطاقات البرامج */
    .programs-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 30px;
        margin-bottom: 60px;
    }
    
    .program-card {
        background: white;
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
        border: 1px solid #e2e8f0;
    }
    
    .program-card:hover {
        transform: translateY(-10px);
    }
    
    .program-img {
        height: 160px;
        background: linear-gradient(135deg, #2563eb, #1e3a8a);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 3.5rem;
        color: white;
    }
    
    .program-body {
        padding: 25px;
    }
    
    .program-body h3 {
        color: #1e3a8a;
        margin-bottom: 15px;
        font-size: 1.5rem;
        font-weight: 700;
    }
    
    .schedule-box {
        background: #f8fafc;
        padding: 18px;
        border-radius: 15px;
    }
    
    .schedule-item {
        padding: 10px 0;
        border-bottom: 1px solid #e2e8f0;
        color: #1e293b;
        font-size: 1rem;
    }
    
    /* بطاقات المدربين */
    .coaches-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 30px;
        margin-bottom: 60px;
    }
    
    .coach-card {
        background: white;
        border-radius: 20px;
        overflow: hidden;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
        border: 1px solid #e2e8f0;
    }
    
    .coach-card:hover {
        transform: translateY(-10px);
    }
    
    .coach-img {
        height: 200px;
        background: linear-gradient(135deg, #2563eb, #1e3a8a);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 4rem;
        color: white;
    }
    
    .coach-body {
        padding: 25px;
    }
    
    .coach-body h3 {
        color: #1e3a8a;
        margin-bottom: 8px;
        font-size: 1.3rem;
        font-weight: 700;
    }
    
    .coach-title {
        color: #2563eb;
        font-weight: 600;
        margin-bottom: 12px;
    }
    
    /* صفحة من نحن */
    .about-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 40px;
        margin-bottom: 50px;
        align-items: center;
    }
    
    .about-image {
        background: linear-gradient(135deg, #2563eb, #1e3a8a);
        border-radius: 20px;
        height: 350px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 6rem;
        color: white;
    }
    
    .mission-vision {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 30px;
        margin-top: 30px;
    }
    
    .mission-card, .vision-card {
        padding: 30px;
        border-radius: 20px;
    }
    
    .mission-card {
        background: #f0f9ff;
        border-right: 5px solid #2563eb;
    }
    
    .vision-card {
        background: #fef3c7;
        border-right: 5px solid #f59e0b;
    }
    
    /* نموذج التسجيل */
    .form-container {
        max-width: 700px;
        margin: 0 auto;
        background: #f8fafc;
        padding: 35px;
        border-radius: 20px;
    }
    
    .success-msg {
        background-color: #10b981;
        color: white;
        padding: 15px;
        border-radius: 12px;
        margin-bottom: 20px;
        text-align: center;
        font-weight: 500;
    }
    
    /* الأسئلة */
    .faq-item {
        margin-bottom: 15px;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        overflow: hidden;
    }
    
    /* الاتصال */
    .contact-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 30px;
    }
    
    .contact-card {
        background: #f8fafc;
        padding: 30px;
        border-radius: 20px;
    }
    
    .contact-item {
        display: flex;
        align-items: center;
        gap: 15px;
        padding: 15px 0;
        border-bottom: 1px solid #e2e8f0;
    }
    
    /* الفوتر */
    .footer {
        background-color: #1e293b;
        color: white;
        padding: 40px 0 25px;
        border-radius: 20px;
        margin-top: 50px;
    }
    
    .footer-inner {
        width: 90%;
        max-width: 1200px;
        margin: 0 auto;
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 30px;
        margin-bottom: 30px;
    }
    
    .footer a {
        color: #cbd5e1;
        text-decoration: none;
        transition: color 0.3s;
        cursor: pointer;
    }
    
    .footer a:hover {
        color: #f59e0b;
    }
    
    /* تنسيقات للشاشات الصغيرة */
    @media (max-width: 768px) {
        .stats-grid, .features-grid, .programs-grid, .coaches-grid, .contact-grid, .about-grid, .mission-vision {
            grid-template-columns: 1fr;
        }
        .hero-section h1 {
            font-size: 1.8rem;
        }
        .section-title {
            font-size: 1.6rem;
        }
        .stat-number {
            font-size: 2rem;
        }
        .logo-text h1 {
            font-size: 1.3rem;
        }
        .logo-img {
            width: 45px;
            height: 45px;
        }
        .header-spacer {
            height: 75px;
        }
        .custom-btn {
            padding: 12px 30px;
            font-size: 1rem;
        }
    }
</style>

<script>
// وظيفة التنقل بين الصفحات
function goToPage(page) {
    const url = new URL(window.location);
    url.searchParams.set('page', page);
    window.location.href = url.toString();
}

// برجر منيو
document.addEventListener('DOMContentLoaded', function() {
    const burgerBtn = document.getElementById('burgerBtn');
    const sideMenu = document.getElementById('sideMenu');
    const menuOverlay = document.getElementById('menuOverlay');
    
    if (burgerBtn) {
        burgerBtn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            this.classList.toggle('active');
            if (sideMenu) sideMenu.classList.toggle('open');
            if (menuOverlay) menuOverlay.classList.toggle('show');
        });
    }
    
    if (menuOverlay) {
        menuOverlay.addEventListener('click', function() {
            this.classList.remove('show');
            if (sideMenu) sideMenu.classList.remove('open');
            if (burgerBtn) burgerBtn.classList.remove('active');
        });
    }
    
    // إغلاق القائمة عند الضغط على ESC
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            if (menuOverlay) menuOverlay.classList.remove('show');
            if (sideMenu) sideMenu.classList.remove('open');
            if (burgerBtn) burgerBtn.classList.remove('active');
        }
    });
});
</script>
""", unsafe_allow_html=True)

# ===== التحقق من وجود صورة الشعار =====
logo_exists = os.path.exists('logo.jpg')

# ===== الهيدر =====
if logo_exists:
    with open('logo.jpg', 'rb') as f:
        img_data = base64.b64encode(f.read()).decode()
    logo_html = f'<img src="data:image/jpeg;base64,{img_data}" class="logo-img">'
else:
    logo_html = '<div class="logo-img" style="background: linear-gradient(135deg, #2563eb, #1e3a8a); display: flex; align-items: center; justify-content: center; font-size: 1.8rem;">⚽</div>'

header_html = f'''
<div class="main-header">
    <div class="header-inner">
        <div class="logo-area">
            {logo_html}
            <div class="logo-text">
                <h1>الكوتش <span>أكاديمي</span></h1>
                <p>أكاديمية كرة القدم المتخصصة</p>
            </div>
        </div>
        <button class="burger-btn" id="burgerBtn">
            <span></span>
            <span></span>
            <span></span>
        </button>
    </div>
</div>

<div class="side-menu" id="sideMenu">
    <ul>
        <li><a onclick="goToPage('home')">🏠 الرئيسية</a></li>
        <li><a onclick="goToPage('about')">ℹ️ من نحن</a></li>
        <li><a onclick="goToPage('programs')">⚽ البرامج التدريبية</a></li>
        <li><a onclick="goToPage('coaches')">👨‍🏫 المدربون</a></li>
        <li><a onclick="goToPage('registration')">📝 تسجيل لاعب جديد</a></li>
        <li><a onclick="goToPage('faq')">❓ الأسئلة الشائعة</a></li>
        <li><a onclick="goToPage('contact')">📞 اتصل بنا</a></li>
    </ul>
</div>

<div class="menu-overlay" id="menuOverlay"></div>

<div class="header-spacer"></div>
'''

st.markdown(header_html, unsafe_allow_html=True)

# ===== إدارة حالة الجلسة =====
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'show_success' not in st.session_state:
    st.session_state.show_success = False

# ===== حفظ البيانات =====
DATA_FILE = 'registrations.json'
CONTACT_FILE = 'contacts.json'

def save_registration(data):
    try:
        registrations = []
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                registrations = json.load(f)
        data['timestamp'] = datetime.now().isoformat()
        registrations.append(data)
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(registrations, f, ensure_ascii=False, indent=2)
        return True
    except Exception:
        return False

def save_contact(data):
    try:
        contacts = []
        if os.path.exists(CONTACT_FILE):
            with open(CONTACT_FILE, 'r', encoding='utf-8') as f:
                contacts = json.load(f)
        data['timestamp'] = datetime.now().isoformat()
        contacts.append(data)
        with open(CONTACT_FILE, 'w', encoding='utf-8') as f:
            json.dump(contacts, f, ensure_ascii=False, indent=2)
        return True
    except Exception:
        return False

# ===== الصفحة الحالية =====
query_params = st.query_params
if 'page' in query_params:
    st.session_state.page = query_params['page']

page = st.session_state.page

# حاوية المحتوى
st.markdown('<div class="content-wrapper">', unsafe_allow_html=True)

# ===== الصفحة الرئيسية (الصفحة 1) =====
if page == 'home':
    st.markdown("""
    <div class="hero-section">
        <h1>⚽ الكوتش أكاديمي</h1>
        <p>أول أكاديمية متخصصة في مصر تركز على بناء اللاعب الشامل من الناحية الفنية والبدنية والنفسية، تحت إشراف مدربين معتمدين دوليًا.</p>
        <p style="font-weight: 700; margin-top: 20px; color: #f59e0b;">نحن لا نصنع لاعبين فقط.. نحن نصنع قادة!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # زر التسجيل
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 50px;">
            <button class="custom-btn" onclick="goToPage('registration')">📝 سجل ابنك الآن</button>
        </div>
        """, unsafe_allow_html=True)
    
    # إنجازات الأكاديمية
    st.markdown('<div class="section-title">إنجازات الأكاديمية</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="stats-grid">
        <div class="stat-card">
            <div style="font-size: 3rem; margin-bottom: 15px;">👥</div>
            <span class="stat-number">300+</span>
            <div class="stat-label">لاعب مدرب</div>
        </div>
        <div class="stat-card">
            <div style="font-size: 3rem; margin-bottom: 15px;">👨‍🏫</div>
            <span class="stat-number">8</span>
            <div class="stat-label">مدرب محترف</div>
        </div>
        <div class="stat-card">
            <div style="font-size: 3rem; margin-bottom: 15px;">🏆</div>
            <span class="stat-number">100+</span>
            <div class="stat-label">لاعب محترف</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # لماذا تختار الكوتش أكاديمي
    st.markdown('<div class="section-title">لماذا تختار الكوتش أكاديمي؟</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="features-grid">
        <div class="feature-card">
            <div class="feature-icon">🧠</div>
            <h3>منهجية التدريب الذهني</h3>
            <p>نركز على تطوير الذكاء الكروي والقدرة على اتخاذ القرارات السريعة والصحيحة داخل الملعب.</p>
        </div>
        <div class="feature-card">
            <div class="feature-icon">🛡️</div>
            <h3>بيئة آمنة محفزة</h3>
            <p>نوفر بيئة تدريب آمنة تحترم الفروق الفردية وتشجع على الإبداع والتميز.</p>
        </div>
        <div class="feature-card">
            <div class="feature-icon">🤝</div>
            <h3>شراكات مع الأندية</h3>
            <p>لدينا شراكات مع أندية محلية لتمكين الموهوبين من الانضمام للمنتخبات والأندية الكبرى.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ===== صفحة من نحن (الصفحة 2) =====
elif page == 'about':
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1e3a8a, #2563eb); border-radius: 20px; padding: 50px 20px; text-align: center; margin-bottom: 40px;">
        <h1 style="color: white; font-size: 2.5rem; margin-bottom: 10px;">من نحن</h1>
        <p style="color: #e2e8f0;">الكوتش أكاديمي.. رؤية جديدة في عالم تدريب كرة القدم</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="about-grid">
        <div class="about-image">⚽</div>
        <div>
            <h2 style="color: #1e3a8a; font-size: 1.8rem; margin-bottom: 20px;">تأسيس الأكاديمية</h2>
            <p style="color: #1e293b; font-size: 1rem;">تأسست الأكاديمية عام 2020 على يد:</p>
            <ul style="margin-right: 25px; margin-top: 15px; color: #1e293b;">
                <li>كابتن ميخا</li>
                <li>كابتن اندرو</li>
                <li>كابتن مينا</li>
            </ul>
            <p style="margin-top: 20px; color: #1e293b;">على ملاعب مدرسة السلام المتطورة</p>
            <p style="margin-top: 15px; font-weight: 700; color: #1e3a8a;">بدعم من الأب الروحي للأكاديمية: مستر / مؤنس منير</p>
        </div>
    </div>
    
    <div class="mission-vision">
        <div class="mission-card">
            <h3 style="color: #1e3a8a; font-size: 1.5rem;">🎯 رسالتنا</h3>
            <p style="color: #1e293b;">تطوير جيل جديد من اللاعبين المبدعين القادرين على التألق محليًا ودوليًا، من خلال تقديم تدريب عصري يعتمد على أحدث الأساليب العلمية.</p>
        </div>
        <div class="vision-card">
            <h3 style="color: #1e3a8a; font-size: 1.5rem;">👁️ أهدافنا</h3>
            <p style="color: #1e293b;">أن نكون الوجهة الأولى لأي موهبة كروية في مصر والوطن العربي، والجسر الذي يعبر من خلاله اللاعبون الموهوبون إلى العالمية.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ===== صفحة البرامج التدريبية (الصفحة 3) =====
elif page == 'programs':
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1e3a8a, #2563eb); border-radius: 20px; padding: 50px 20px; text-align: center; margin-bottom: 40px;">
        <h1 style="color: white; font-size: 2.5rem; margin-bottom: 10px;">البرامج التدريبية</h1>
        <p style="color: #e2e8f0;">مواعيد تدريبية مصممة لكل فئة عمرية وجنسية</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="programs-grid">
        <div class="program-card">
            <div class="program-img">📅 السبت</div>
            <div class="program-body">
                <h3>مواعيد تدريب السبت</h3>
                <div class="schedule-box">
                    <div class="schedule-item"><strong>٥:٠٠ - ٦:٠٠ م</strong> → بنات</div>
                    <div class="schedule-item"><strong>٦:٠٠ - ٧:٣٠ م</strong> → بنين (١ ابتدائي - ٥ ابتدائي)</div>
                    <div class="schedule-item"><strong>٧:٣٠ - ٩:٠٠ م</strong> → بنين (٦ ابتدائي - ٢ إعدادي)</div>
                    <div style="margin-top: 15px; color: #666;">📍 ملاعب مدرسة السلام المتطورة</div>
                </div>
            </div>
        </div>
        <div class="program-card">
            <div class="program-img">✅ الخميس</div>
            <div class="program-body">
                <h3>مواعيد تدريب الخميس</h3>
                <div class="schedule-box">
                    <div class="schedule-item"><strong>٤:٣٠ - ٦:٠٠ م</strong> → بنات</div>
                    <div class="schedule-item"><strong>٦:٠٠ - ٨:٠٠ م</strong> → بنين (١ ابتدائي - ٥ ابتدائي)</div>
                    <div class="schedule-item"><strong>٨:٠٠ - ١٠:٠٠ م</strong> → بنين (٦ ابتدائي - ٢ إعدادي)</div>
                    <div style="margin-top: 15px; color: #666;">📍 ملاعب مدرسة السلام المتطورة</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ===== صفحة المدربون (الصفحة 4) =====
elif page == 'coaches':
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1e3a8a, #2563eb); border-radius: 20px; padding: 50px 20px; text-align: center; margin-bottom: 40px;">
        <h1 style="color: white; font-size: 2.5rem; margin-bottom: 10px;">المدربون</h1>
        <p style="color: #e2e8f0;">فريقنا من المدربين المحترفين ذوي الخبرة والكفاءة</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="coaches-grid">
        <div class="coach-card">
            <div class="coach-img">👨‍🏫</div>
            <div class="coach-body">
                <h3>كابتن/ميخائيل كميل رؤف</h3>
                <div class="coach-title">مدرب معتمد</div>
                <div class="coach-desc">بكالريوس تربية رياضية - رخصة CAF - دبلومة إعداد بدني</div>
            </div>
        </div>
        <div class="coach-card">
            <div class="coach-img">🧤</div>
            <div class="coach-body">
                <h3>كابتن أحمد علي</h3>
                <div class="coach-title">مدرب حراس مرمى</div>
                <div class="coach-desc">مدرب معتمد من CAF - خبرة 15 عامًا</div>
            </div>
        </div>
        <div class="coach-card">
            <div class="coach-img">🏃</div>
            <div class="coach-body">
                <h3>د. خالد السيد</h3>
                <div class="coach-title">مدرب لياقة بدنية</div>
                <div class="coach-desc">دكتوراه في علوم الرياضة - مختص في تطوير الناشئين</div>
            </div>
        </div>
        <div class="coach-card">
            <div class="coach-img">⚽</div>
            <div class="coach-body">
                <h3>كابتن محمد جابر</h3>
                <div class="coach-title">مدرب مهارات فنية</div>
                <div class="coach-desc">مدرب معتمد من CAF - خبرة 12 عامًا</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ===== صفحة التسجيل (الصفحة 5) =====
elif page == 'registration':
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1e3a8a, #2563eb); border-radius: 20px; padding: 50px 20px; text-align: center; margin-bottom: 40px;">
        <h1 style="color: white; font-size: 2.5rem; margin-bottom: 10px;">تسجيل لاعب جديد</h1>
        <p style="color: #e2e8f0;">انضم إلى الكوتش أكاديمي وابدأ رحلتك نحو الاحتراف</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.show_success:
        st.markdown('<div class="success-msg">✅ تم إرسال طلب التسجيل بنجاح! سنتواصل معكم خلال 24 ساعة.</div>', unsafe_allow_html=True)
        st.session_state.show_success = False
    
    with st.form("reg_form"):
        st.markdown("### 📋 معلومات اللاعب")
        player_name = st.text_input("اسم اللاعب الثلاثي *")
        age_group = st.selectbox("الفئة العمرية المطلوبة *", ["", "بنات", "١ ابتدائي - ٥ ابتدائي", "٦ ابتدائي - ٢ إعدادي"])
        
        st.markdown("### 👨‍👩‍👦 معلومات ولي الأمر")
        parent_name = st.text_input("اسم ولي الأمر *")
        parent_phone = st.text_input("رقم الهاتف *", placeholder="01XXXXXXXXX")
        notes = st.text_area("ملاحظات إضافية (اختياري)", height=80)
        
        submitted = st.form_submit_button("📝 تقديم طلب التسجيل", use_container_width=True)
        
        if submitted:
            if player_name and age_group and parent_name and parent_phone:
                data = {'playerName': player_name, 'ageGroup': age_group, 'parentName': parent_name, 'parentPhone': parent_phone, 'notes': notes}
                if save_registration(data):
                    st.session_state.show_success = True
                    st.rerun()
                else:
                    st.error("❌ حدث خطأ، يرجى المحاولة مرة أخرى")
            else:
                st.error("⚠️ يرجى ملء جميع الحقول المطلوبة")

# ===== صفحة الأسئلة الشائعة (الصفحة 6) =====
elif page == 'faq':
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1e3a8a, #2563eb); border-radius: 20px; padding: 50px 20px; text-align: center; margin-bottom: 40px;">
        <h1 style="color: white; font-size: 2.5rem; margin-bottom: 10px;">الأسئلة الشائعة</h1>
        <p style="color: #e2e8f0;">إجابات على أكثر الأسئلة شيوعًا من أولياء الأمور</p>
    </div>
    """, unsafe_allow_html=True)
    
    faqs = [
        ("ما الذي يميز الكوتش أكاديمي عن غيرها؟", "الكوتش أكاديمي تتبنى منهجية تدريب متكاملة تركز على: التدريب الذهني وتطوير الذكاء الكروي، متابعة فردية لكل لاعب مع خطة تطوير شخصية، استخدام التكنولوجيا في تحليل الأداء، شراكات مع أندية محلية لدعم الموهوبين."),
        ("ما هي مدة التدريب وأوقاته؟", "الموسم التدريبي يمتد لمدة 10 أشهر، من سبتمبر إلى يونيو. التدريبات في الفترة المسائية حسب الجدول المحدد لكل فئة عمرية، بما يتناسب مع أوقات المدارس."),
        ("ما هي تكلفة الاشتراك وآلية الدفع؟", "تختلف التكلفة حسب الفئة العمرية وعدد أيام التدريب. نقدم خصومات للأشقاء، نظام تقسيط شهري، ومنح جزئية للمتميزين. يرجى التواصل معنا لمعرفة التفاصيل الدقيقة."),
        ("ما هي متطلبات الانضمام للأكاديمية؟", "للانضمام للأكاديمية نحتاج إلى: إكمال نموذج التسجيل عبر الموقع، أن يكون اللاعب في الفئة العمرية المحددة، الرغبة الحقيقية في التعلم والتطوير، الالتزام بمواعيد التدريب."),
        ("هل هناك تدريبات خاصة للمبتدئين؟", "نعم، لدينا برامج خاصة للمبتدئين تركز على: تعلم أساسيات كرة القدم، تطوير المهارات الحركية الأساسية، بناء الثقة بالنفس، تعزيز حب الرياضة واللعب الجماعي."),
        ("كيف يمكن متابعة تطور اللاعب؟", "نوفر نظام متابعة شامل يشمل: تقييم دوري للمهارات الفنية، متابعة التطور البدني، تقرير عن المشاركة والالتزام، لقاءات دورية مع أولياء الأمور."),
        ("ماذا عن السلامة والإصابات خلال التدريب؟", "السلامة أولوية لدينا، ونوفر: إشراف مستمر من مدربين مؤهلين، بيئة تدريب آمنة ومجهزة، برنامج إحماء وتبريد مناسب، مدربين حاصلين على شهادات في الإسعافات الأولية.")
    ]
    
    for q, a in faqs:
        with st.expander(f"❓ {q}"):
            st.markdown(f'<p style="color: #1e293b;">{a}</p>', unsafe_allow_html=True)

# ===== صفحة اتصل بنا (الصفحة 7) =====
elif page == 'contact':
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1e3a8a, #2563eb); border-radius: 20px; padding: 50px 20px; text-align: center; margin-bottom: 40px;">
        <h1 style="color: white; font-size: 2.5rem; margin-bottom: 10px;">اتصل بنا</h1>
        <p style="color: #e2e8f0;">تواصل معنا لأي استفسارات أو معلومات إضافية</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="contact-card">
            <h3 style="color: #1e3a8a; margin-bottom: 25px;">📞 معلومات الاتصال</h3>
            <div class="contact-item">
                <div style="font-size: 1.5rem;">📱</div>
                <div><a href="tel:01069238878" style="text-decoration: none; color: #1e293b;">01069238878</a></div>
            </div>
            <div class="contact-item">
                <div style="font-size: 1.5rem;">💬</div>
                <div><a href="https://wa.me/201285197778" target="_blank" style="text-decoration: none; color: #25D366;">01285197778 (واتساب)</a></div>
            </div>
            <div class="contact-item">
                <div style="font-size: 1.5rem;">📍</div>
                <div style="color: #1e293b;">أسيوط - مصر - على ملاعب مدرسة السلام المتطورة</div>
            </div>
            <div class="contact-item">
                <div style="font-size: 1.5rem;">⏰</div>
                <div style="color: #1e293b;">السبت - الخميس: 4:00م - 9:00م<br>الجمعة: إجازة</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="contact-card"><h3 style="color: #1e3a8a; margin-bottom: 25px;">✉️ أرسل رسالة</h3></div>', unsafe_allow_html=True)
        
        with st.form("contact_form"):
            c_name = st.text_input("الاسم")
            c_phone = st.text_input("رقم الهاتف", placeholder="010XXXXXXXX")
            c_subject = st.selectbox("الموضوع", ["", "استفسار عام", "معلومات عن البرامج", "التسجيل", "أخرى"])
            c_msg = st.text_area("الرسالة", height=100)
            if st.form_submit_button("📨 إرسال الرسالة", use_container_width=True):
                if c_name and c_phone and c_subject and c_msg:
                    if save_contact({'name': c_name, 'phone': c_phone, 'subject': c_subject, 'message': c_msg}):
                        st.success("✅ شكراً لتواصلك! تم إرسال رسالتك بنجاح.")
                    else:
                        st.error("❌ حدث خطأ")
                else:
                    st.error("⚠️ يرجى ملء جميع الحقول")

# إغلاق حاوية المحتوى
st.markdown('</div>', unsafe_allow_html=True)

# ===== الفوتر =====
st.markdown("""
<div class="footer">
    <div class="footer-inner">
        <div>
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 15px;">
                <div style="width: 45px; height: 45px; background: linear-gradient(135deg, #2563eb, #1e3a8a); border-radius: 12px; display: flex; align-items: center; justify-content: center;">⚽</div>
                <h3 style="color: white;">الكوتش أكاديمي</h3>
            </div>
            <p style="color: #cbd5e1; font-size: 0.85rem;">تأسست عام 2020 على ملاعب مدرسة السلام المتطورة. أول أكاديمية في مصر تركز على تطوير اللاعب الشامل.</p>
        </div>
        <div>
            <h4 style="color: white; margin-bottom: 15px;">روابط سريعة</h4>
            <ul style="list-style: none; padding: 0;">
                <li style="margin-bottom: 8px;"><a onclick="goToPage('home')">← الرئيسية</a></li>
                <li style="margin-bottom: 8px;"><a onclick="goToPage('about')">← من نحن</a></li>
                <li style="margin-bottom: 8px;"><a onclick="goToPage('programs')">← البرامج التدريبية</a></li>
                <li style="margin-bottom: 8px;"><a onclick="goToPage('coaches')">← المدربون</a></li>
                <li style="margin-bottom: 8px;"><a onclick="goToPage('faq')">← الأسئلة الشائعة</a></li>
            </ul>
        </div>
        <div>
            <h4 style="color: white; margin-bottom: 15px;">معلومات الاتصال</h4>
            <ul style="list-style: none; padding: 0;">
                <li style="margin-bottom: 10px;">📍 أسيوط - ملاعب مدرسة السلام</li>
                <li style="margin-bottom: 10px;"><a href="tel:01069238878">📞 01069238878</a></li>
                <li style="margin-bottom: 10px;"><a href="https://wa.me/201285197778" target="_blank">💬 01285197778</a></li>
            </ul>
        </div>
    </div>
    <div style="text-align: center; padding-top: 20px; border-top: 1px solid rgba(255, 255, 255, 0.1);">
        <p style="color: #94a3b8;">© 2024 الكوتش أكاديمي - جميع الحقوق محفوظة</p>
        <p style="color: #94a3b8; margin-top: 5px; font-size: 0.75rem;">تأسست عام 2020 على يد: كابتن ميخا، كابتن اندرو، كابتن مينا</p>
    </div>
</div>
""", unsafe_allow_html=True)
