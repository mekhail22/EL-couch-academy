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

# ===== CSS الرئيسي =====
st.markdown("""
<style>
    /* إخفاء شريط Streamlit العلوي فقط */
    header[data-testid="stHeader"] {
        display: none !important;
    }
    
    .stApp > header {
        display: none !important;
    }
    
    .st-emotion-cache-18ni7ap {
        display: none !important;
    }
    
    .st-emotion-cache-1v0mbdj {
        display: none !important;
    }
    
    #MainMenu {
        display: none !important;
    }
    
    footer {
        display: none !important;
    }
    
    /* إزالة المسافات */
    .main .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        padding-left: 0rem !important;
        padding-right: 0rem !important;
        max-width: 100% !important;
    }
    
    /* خلفية التطبيق */
    .stApp {
        background-color: #f0f2f6 !important;
    }
    
    /* ===== تنسيق عام ===== */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
        font-family: 'Cairo', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* ===== الهيدر العلوي ===== */
    .top-header {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        z-index: 10000;
        padding: 12px 0;
        border-bottom: 1px solid #e2e8f0;
    }
    
    .header-container {
        width: 95%;
        max-width: 1200px;
        margin: 0 auto;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    /* ===== اللوجو ===== */
    .logo-wrapper {
        display: flex;
        align-items: center;
        gap: 12px;
        cursor: pointer;
    }
    
    .logo-image {
        width: 55px;
        height: 55px;
        background: linear-gradient(135deg, #1e3a8a, #3b82f6);
        border-radius: 15px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        transition: transform 0.3s ease;
    }
    
    .logo-image:hover {
        transform: scale(1.05);
    }
    
    .logo-image span {
        font-size: 2rem;
    }
    
    .logo-text h1 {
        font-size: 1.6rem;
        margin: 0;
        color: #1e3a8a;
        font-weight: 800;
        letter-spacing: -0.5px;
    }
    
    .logo-text span {
        color: #f59e0b;
    }
    
    .logo-text p {
        font-size: 0.7rem;
        color: #64748b;
        margin: 0;
        font-weight: 500;
    }
    
    /* ===== برجر منيو ===== */
    .burger-menu-btn {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        width: 38px;
        height: 26px;
        background: transparent;
        border: none;
        cursor: pointer;
        padding: 0;
        z-index: 10002;
        transition: all 0.3s ease;
    }
    
    .burger-menu-btn span {
        display: block;
        width: 100%;
        height: 3px;
        background-color: #1e3a8a;
        border-radius: 4px;
        transition: all 0.3s ease;
    }
    
    .burger-menu-btn.active span:nth-child(1) {
        transform: rotate(45deg) translate(9px, 9px);
    }
    
    .burger-menu-btn.active span:nth-child(2) {
        opacity: 0;
        transform: translateX(-20px);
    }
    
    .burger-menu-btn.active span:nth-child(3) {
        transform: rotate(-45deg) translate(9px, -9px);
    }
    
    /* ===== القائمة الجانبية ===== */
    .side-navigation {
        position: fixed;
        top: 0;
        right: -350px;
        width: 320px;
        height: 100vh;
        background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
        box-shadow: -8px 0 30px rgba(0, 0, 0, 0.15);
        z-index: 10001;
        transition: right 0.35s cubic-bezier(0.4, 0, 0.2, 1);
        padding-top: 90px;
        overflow-y: auto;
    }
    
    .side-navigation.open {
        right: 0;
    }
    
    .side-navigation ul {
        list-style: none;
        padding: 0 20px;
    }
    
    .side-navigation li {
        margin-bottom: 8px;
        opacity: 0;
        transform: translateX(30px);
        transition: all 0.3s ease;
    }
    
    .side-navigation.open li {
        opacity: 1;
        transform: translateX(0);
    }
    
    .side-navigation.open li:nth-child(1) { transition-delay: 0.05s; }
    .side-navigation.open li:nth-child(2) { transition-delay: 0.1s; }
    .side-navigation.open li:nth-child(3) { transition-delay: 0.15s; }
    .side-navigation.open li:nth-child(4) { transition-delay: 0.2s; }
    .side-navigation.open li:nth-child(5) { transition-delay: 0.25s; }
    .side-navigation.open li:nth-child(6) { transition-delay: 0.3s; }
    .side-navigation.open li:nth-child(7) { transition-delay: 0.35s; }
    
    .side-navigation a {
        display: flex;
        align-items: center;
        gap: 15px;
        padding: 14px 20px;
        color: #1e293b;
        text-decoration: none;
        font-weight: 600;
        border-radius: 14px;
        transition: all 0.3s ease;
        cursor: pointer;
        font-size: 16px;
    }
    
    .side-navigation a:hover {
        background: linear-gradient(135deg, #eff6ff, #dbeafe);
        color: #3b82f6;
        transform: translateX(-5px);
    }
    
    /* طبقة التعتيم */
    .nav-overlay-layer {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-color: rgba(0, 0, 0, 0.5);
        z-index: 10000;
        display: none;
        backdrop-filter: blur(3px);
    }
    
    .nav-overlay-layer.show {
        display: block;
    }
    
    /* مساحة تعويضية */
    .header-spacer {
        height: 85px;
    }
    
    /* ===== حاوية المحتوى ===== */
    .content-container {
        width: 95%;
        max-width: 1200px;
        margin: 0 auto;
        padding: 20px 15px;
    }
    
    /* ===== باقي التنسيقات ===== */
    .hero-section {
        background: linear-gradient(135deg, rgba(0,0,0,0.75), rgba(0,0,0,0.65)), url('https://images.unsplash.com/photo-1575361204480-aadea25e6e68?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80');
        background-size: cover;
        background-position: center;
        border-radius: 24px;
        padding: 80px 20px;
        text-align: center;
        margin-bottom: 50px;
        position: relative;
        overflow: hidden;
    }
    
    .hero-section::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: rotate 20s linear infinite;
    }
    
    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    .hero-section h1 {
        color: white;
        font-size: 3rem;
        margin-bottom: 20px;
        font-weight: 800;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        position: relative;
        z-index: 1;
    }
    
    .hero-section p {
        color: #e2e8f0;
        max-width: 700px;
        margin: 0 auto;
        font-size: 1.1rem;
        position: relative;
        z-index: 1;
    }
    
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
        background: linear-gradient(90deg, #f59e0b, #fbbf24);
        border-radius: 2px;
    }
    
    /* بطاقات الإحصائيات */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 25px;
        margin-bottom: 60px;
    }
    
    .stat-card {
        background: white;
        padding: 35px 20px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
        border: 1px solid #e2e8f0;
    }
    
    .stat-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.12);
    }
    
    .stat-number {
        font-size: 3rem;
        font-weight: 800;
        color: #1e3a8a;
        display: block;
    }
    
    .stat-label {
        color: #64748b;
        margin-top: 10px;
        font-weight: 600;
        font-size: 1rem;
    }
    
    /* بطاقات المميزات */
    .features-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 25px;
        margin-bottom: 60px;
    }
    
    .feature-card {
        background: white;
        padding: 35px 25px;
        border-radius: 20px;
        text-align: center;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
    }
    
    .feature-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.12);
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 20px;
    }
    
    .feature-card h3 {
        color: #1e3a8a;
        margin-bottom: 15px;
        font-size: 1.3rem;
        font-weight: 700;
    }
    
    .feature-card p {
        color: #64748b;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    /* زر مخصص */
    .register-btn {
        background: linear-gradient(135deg, #f59e0b, #d97706);
        color: white;
        padding: 16px 50px;
        border-radius: 50px;
        font-weight: 800;
        font-size: 1.2rem;
        border: none;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
    }
    
    .register-btn:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
    }
    
    /* بطاقات البرامج */
    .programs-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 25px;
        margin-bottom: 60px;
    }
    
    .program-card {
        background: white;
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
        border: 1px solid #e2e8f0;
    }
    
    .program-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.12);
    }
    
    .program-header {
        height: 160px;
        background: linear-gradient(135deg, #3b82f6, #1e3a8a);
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
        font-size: 1.4rem;
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
        color: #334155;
        font-size: 1rem;
    }
    
    /* بطاقات المدربين */
    .coaches-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 25px;
        margin-bottom: 60px;
    }
    
    .coach-card {
        background: white;
        border-radius: 20px;
        overflow: hidden;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
        border: 1px solid #e2e8f0;
    }
    
    .coach-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.12);
    }
    
    .coach-avatar {
        height: 200px;
        background: linear-gradient(135deg, #3b82f6, #1e3a8a);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 4rem;
        color: white;
    }
    
    .coach-info {
        padding: 25px;
    }
    
    .coach-info h3 {
        color: #1e3a8a;
        margin-bottom: 8px;
        font-size: 1.3rem;
        font-weight: 700;
    }
    
    .coach-title {
        color: #3b82f6;
        font-weight: 600;
        margin-bottom: 12px;
    }
    
    /* صفحة من نحن */
    .about-wrapper {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 40px;
        margin-bottom: 50px;
        align-items: center;
    }
    
    .about-image {
        background: linear-gradient(135deg, #3b82f6, #1e3a8a);
        border-radius: 24px;
        height: 350px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 6rem;
        color: white;
    }
    
    .mission-vision-grid {
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
        border-right: 5px solid #3b82f6;
    }
    
    .vision-card {
        background: #fef3c7;
        border-right: 5px solid #f59e0b;
    }
    
    /* نموذج التسجيل */
    .registration-form {
        max-width: 700px;
        margin: 0 auto;
        background: white;
        padding: 35px;
        border-radius: 24px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    }
    
    .success-message {
        background: linear-gradient(135deg, #10b981, #059669);
        color: white;
        padding: 15px;
        border-radius: 12px;
        margin-bottom: 20px;
        text-align: center;
        font-weight: 500;
    }
    
    /* الاتصال */
    .contact-wrapper {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 30px;
    }
    
    .contact-card {
        background: white;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
    }
    
    .contact-item {
        display: flex;
        align-items: center;
        gap: 15px;
        padding: 15px 0;
        border-bottom: 1px solid #e2e8f0;
    }
    
    /* خريطة */
    .map-container {
        margin-top: 20px;
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    .map-container iframe {
        width: 100%;
        height: 250px;
        border: none;
    }
    
    /* الفوتر */
    .main-footer {
        background: linear-gradient(135deg, #1e293b, #0f172a);
        color: white;
        padding: 45px 0 25px;
        border-radius: 24px 24px 0 0;
        margin-top: 60px;
    }
    
    .footer-grid {
        width: 95%;
        max-width: 1200px;
        margin: 0 auto;
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 35px;
        margin-bottom: 35px;
    }
    
    .footer-link {
        color: #cbd5e1;
        text-decoration: none;
        transition: all 0.3s ease;
        cursor: pointer;
        display: inline-block;
    }
    
    .footer-link:hover {
        color: #f59e0b;
        transform: translateX(-5px);
    }
    
    /* تنسيقات للشاشات الصغيرة */
    @media (max-width: 768px) {
        .stats-grid, .features-grid, .programs-grid, .coaches-grid, .contact-wrapper, .about-wrapper, .mission-vision-grid {
            grid-template-columns: 1fr;
        }
        .hero-section h1 {
            font-size: 2rem;
        }
        .section-title {
            font-size: 1.6rem;
        }
        .stat-number {
            font-size: 2rem;
        }
        .logo-text h1 {
            font-size: 1.2rem;
        }
        .logo-image {
            width: 45px;
            height: 45px;
        }
        .logo-image span {
            font-size: 1.5rem;
        }
        .header-spacer {
            height: 75px;
        }
        .side-navigation {
            width: 280px;
            right: -280px;
        }
        .register-btn {
            padding: 12px 30px;
            font-size: 1rem;
        }
    }
</style>

<!-- HTML هيكل الهيدر والبرجر منيو -->
<div id="headerStructure" style="display: none;">
    <div class="top-header" id="mainHeader">
        <div class="header-container">
            <div class="logo-wrapper" id="logoArea">
                <div class="logo-image" id="logoBox">
                    <span>⚽</span>
                </div>
                <div class="logo-text">
                    <h1>الكوتش <span>أكاديمي</span></h1>
                    <p>أكاديمية كرة القدم المتخصصة</p>
                </div>
            </div>
            <button class="burger-menu-btn" id="burgerButton">
                <span></span>
                <span></span>
                <span></span>
            </button>
        </div>
    </div>
    <div class="side-navigation" id="sideNavMenu">
        <ul>
            <li><a href="#" data-nav-page="home" class="nav-menu-link">🏠 الرئيسية</a></li>
            <li><a href="#" data-nav-page="about" class="nav-menu-link">ℹ️ من نحن</a></li>
            <li><a href="#" data-nav-page="programs" class="nav-menu-link">⚽ البرامج التدريبية</a></li>
            <li><a href="#" data-nav-page="coaches" class="nav-menu-link">👨‍🏫 المدربون</a></li>
            <li><a href="#" data-nav-page="registration" class="nav-menu-link">📝 تسجيل لاعب جديد</a></li>
            <li><a href="#" data-nav-page="faq" class="nav-menu-link">❓ الأسئلة الشائعة</a></li>
            <li><a href="#" data-nav-page="contact" class="nav-menu-link">📞 اتصل بنا</a></li>
        </ul>
    </div>
    <div class="nav-overlay-layer" id="navOverlayLayer"></div>
</div>

<script>
// وظيفة التنقل بين الصفحات
function navigateToPage(pageName) {
    const url = new URL(window.location);
    url.searchParams.set('page', pageName);
    window.location.href = url.toString();
}

// تهيئة جميع العناصر بعد تحميل الصفحة
document.addEventListener('DOMContentLoaded', function() {
    // إضافة الهيكل إلى الصفحة
    const headerHtml = document.getElementById('headerStructure').innerHTML;
    document.body.insertAdjacentHTML('afterbegin', headerHtml);
    
    // إضافة المسافة العلوية
    const spacer = document.createElement('div');
    spacer.className = 'header-spacer';
    document.body.insertBefore(spacer, document.body.firstChild);
    
    // عناصر البرجر منيو
    const burgerBtn = document.getElementById('burgerButton');
    const sideMenu = document.getElementById('sideNavMenu');
    const overlayLayer = document.getElementById('navOverlayLayer');
    
    if (burgerBtn) {
        burgerBtn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            this.classList.toggle('active');
            if (sideMenu) sideMenu.classList.toggle('open');
            if (overlayLayer) overlayLayer.classList.toggle('show');
            // منع التمرير في الخلف
            if (sideMenu.classList.contains('open')) {
                document.body.style.overflow = 'hidden';
            } else {
                document.body.style.overflow = '';
            }
        });
    }
    
    if (overlayLayer) {
        overlayLayer.addEventListener('click', function() {
            this.classList.remove('show');
            if (sideMenu) sideMenu.classList.remove('open');
            if (burgerBtn) burgerBtn.classList.remove('active');
            document.body.style.overflow = '';
        });
    }
    
    // روابط القائمة الجانبية
    document.querySelectorAll('.nav-menu-link').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const pageId = this.getAttribute('data-nav-page');
            navigateToPage(pageId);
        });
    });
    
    // إغلاق القائمة عند الضغط على ESC
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            if (overlayLayer) overlayLayer.classList.remove('show');
            if (sideMenu) sideMenu.classList.remove('open');
            if (burgerBtn) burgerBtn.classList.remove('active');
            document.body.style.overflow = '';
        }
    });
});

// جعل وظيفة التنقل عامة
window.navigateToPage = navigateToPage;
</script>
""", unsafe_allow_html=True)

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
st.markdown('<div class="content-container">', unsafe_allow_html=True)

# ===== الصفحة الرئيسية (الصفحة 1) =====
if page == 'home':
    st.markdown("""
    <div class="hero-section">
        <h1>⚽ الكوتش أكاديمي</h1>
        <p>أول أكاديمية متخصصة في مصر تركز على بناء اللاعب الشامل من الناحية الفنية والبدنية والنفسية، تحت إشراف مدربين معتمدين دوليًا.</p>
        <p style="font-weight: 700; margin-top: 20px; color: #fbbf24;">نحن لا نصنع لاعبين فقط.. نحن نصنع قادة!</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 50px;">
            <button class="register-btn" onclick="navigateToPage('registration')">📝 سجل ابنك الآن</button>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="section-title">إنجازات الأكاديمية</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="stats-grid">
        <div class="stat-card">
            <div style="font-size: 3rem; margin-bottom: 15px;">👥</div>
            <span class="stat-number">500+</span>
            <div class="stat-label">لاعب مدرب</div>
        </div>
        <div class="stat-card">
            <div style="font-size: 3rem; margin-bottom: 15px;">👨‍🏫</div>
            <span class="stat-number">12</span>
            <div class="stat-label">مدرب محترف</div>
        </div>
        <div class="stat-card">
            <div style="font-size: 3rem; margin-bottom: 15px;">🏆</div>
            <span class="stat-number">150+</span>
            <div class="stat-label">لاعب محترف</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
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
    <div style="background: linear-gradient(135deg, #1e3a8a, #3b82f6); border-radius: 24px; padding: 55px 20px; text-align: center; margin-bottom: 45px;">
        <h1 style="color: white; font-size: 2.5rem; margin-bottom: 12px;">من نحن</h1>
        <p style="color: #e2e8f0;">الكوتش أكاديمي.. رؤية جديدة في عالم تدريب كرة القدم</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="about-wrapper">
        <div class="about-image">⚽</div>
        <div>
            <h2 style="color: #1e3a8a; font-size: 1.8rem; margin-bottom: 20px;">تأسيس الأكاديمية</h2>
            <p style="color: #334155; font-size: 1rem;">تأسست الأكاديمية عام 2020 على يد:</p>
            <ul style="margin-right: 25px; margin-top: 15px; color: #334155;">
                <li>كابتن ميخائيل كميل رؤف (ميخا)</li>
                <li>كابتن اندرو</li>
                <li>كابتن مينا</li>
            </ul>
            <p style="margin-top: 20px; color: #334155;">على ملاعب مدرسة السلام المتطورة</p>
            <p style="margin-top: 15px; font-weight: 700; color: #1e3a8a;">بدعم من الأب الروحي للأكاديمية: مستر / مؤنس منير</p>
        </div>
    </div>
    
    <div class="mission-vision-grid">
        <div class="mission-card">
            <h3 style="color: #1e3a8a; font-size: 1.5rem;">🎯 رسالتنا</h3>
            <p style="color: #334155;">تطوير جيل جديد من اللاعبين المبدعين القادرين على التألق محليًا ودوليًا، من خلال تقديم تدريب عصري يعتمد على أحدث الأساليب العلمية والتكنولوجية في عالم كرة القدم.</p>
        </div>
        <div class="vision-card">
            <h3 style="color: #1e3a8a; font-size: 1.5rem;">👁️ رؤيتنا</h3>
            <p style="color: #334155;">أن نكون الوجهة الأولى لأي موهبة كروية في مصر والوطن العربي، والجسر الذي يعبر من خلاله اللاعبون الموهوبون إلى العالمية.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ===== صفحة البرامج التدريبية (الصفحة 3) =====
elif page == 'programs':
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1e3a8a, #3b82f6); border-radius: 24px; padding: 55px 20px; text-align: center; margin-bottom: 45px;">
        <h1 style="color: white; font-size: 2.5rem; margin-bottom: 12px;">البرامج التدريبية</h1>
        <p style="color: #e2e8f0;">مواعيد تدريبية مصممة لكل فئة عمرية وجنسية</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="programs-grid">
        <div class="program-card">
            <div class="program-header">📅 السبت</div>
            <div class="program-body">
                <h3>مواعيد تدريب السبت</h3>
                <div class="schedule-box">
                    <div class="schedule-item"><strong>٥:٠٠ - ٦:٠٠ م</strong> → بنات (جميع الأعمار)</div>
                    <div class="schedule-item"><strong>٦:٠٠ - ٧:٣٠ م</strong> → بنين (الصف الأول - الخامس الابتدائي)</div>
                    <div class="schedule-item"><strong>٧:٣٠ - ٩:٠٠ م</strong> → بنين (الصف السادس الابتدائي - الثاني الإعدادي)</div>
                    <div style="margin-top: 15px; color: #64748b;">📍 ملاعب مدرسة السلام المتطورة - أسيوط</div>
                </div>
            </div>
        </div>
        <div class="program-card">
            <div class="program-header">✅ الخميس</div>
            <div class="program-body">
                <h3>مواعيد تدريب الخميس</h3>
                <div class="schedule-box">
                    <div class="schedule-item"><strong>٤:٣٠ - ٦:٠٠ م</strong> → بنات (جميع الأعمار)</div>
                    <div class="schedule-item"><strong>٦:٠٠ - ٨:٠٠ م</strong> → بنين (الصف الأول - الخامس الابتدائي)</div>
                    <div class="schedule-item"><strong>٨:٠٠ - ١٠:٠٠ م</strong> → بنين (الصف السادس الابتدائي - الثاني الإعدادي)</div>
                    <div style="margin-top: 15px; color: #64748b;">📍 ملاعب مدرسة السلام المتطورة - أسيوط</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ===== صفحة المدربون (الصفحة 4) =====
elif page == 'coaches':
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1e3a8a, #3b82f6); border-radius: 24px; padding: 55px 20px; text-align: center; margin-bottom: 45px;">
        <h1 style="color: white; font-size: 2.5rem; margin-bottom: 12px;">المدربون</h1>
        <p style="color: #e2e8f0;">فريقنا من المدربين المحترفين ذوي الخبرة والكفاءة</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="coaches-grid">
        <div class="coach-card">
            <div class="coach-avatar">👨‍🏫</div>
            <div class="coach-info">
                <h3>كابتن/ميخائيل كميل رؤف</h3>
                <div class="coach-title">المدير الفني - مدرب معتمد</div>
                <div class="coach-desc">بكالريوس تربية رياضية - رخصة تدريب CAF - دبلومة الإعداد البدني - دبلومة إصابات الملاعب - مدرس تربية رياضية بمدارس السلام الخاصة</div>
            </div>
        </div>
        <div class="coach-card">
            <div class="coach-avatar">🧤</div>
            <div class="coach-info">
                <h3>كابتن أحمد علي</h3>
                <div class="coach-title">مدرب حراس مرمى</div>
                <div class="coach-desc">مدرب معتمد من الاتحاد الأفريقي CAF - خبرة 15 عامًا في تدريب حراس المرمى</div>
            </div>
        </div>
        <div class="coach-card">
            <div class="coach-avatar">🏃</div>
            <div class="coach-info">
                <h3>د. خالد السيد</h3>
                <div class="coach-title">مدرب لياقة بدنية</div>
                <div class="coach-desc">دكتوراه في علوم الرياضة - مختص في تطوير قدرات الناشئين واللياقة البدنية</div>
            </div>
        </div>
        <div class="coach-card">
            <div class="coach-avatar">⚽</div>
            <div class="coach-info">
                <h3>كابتن محمد جابر</h3>
                <div class="coach-title">مدرب مهارات فنية</div>
                <div class="coach-desc">مدرب معتمد من الاتحاد الأفريقي CAF - خبرة 12 عامًا في تدريب المهارات الفنية</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ===== صفحة التسجيل (الصفحة 5) =====
elif page == 'registration':
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1e3a8a, #3b82f6); border-radius: 24px; padding: 55px 20px; text-align: center; margin-bottom: 45px;">
        <h1 style="color: white; font-size: 2.5rem; margin-bottom: 12px;">تسجيل لاعب جديد</h1>
        <p style="color: #e2e8f0;">انضم إلى الكوتش أكاديمي وابدأ رحلتك نحو الاحتراف</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.show_success:
        st.markdown('<div class="success-message">✅ تم إرسال طلب التسجيل بنجاح! سنتواصل معكم خلال 24 ساعة.</div>', unsafe_allow_html=True)
        st.session_state.show_success = False
    
    with st.form("registration_form"):
        st.markdown("### 📋 معلومات اللاعب")
        player_name = st.text_input("اسم اللاعب الثلاثي *", placeholder="محمد أحمد محمود")
        age_group = st.selectbox("الفئة العمرية المطلوبة *", 
                                 ["", "بنات (جميع الأعمار)", "بنين (الصف الأول - الخامس الابتدائي)", "بنين (الصف السادس الابتدائي - الثاني الإعدادي)"])
        birth_date = st.date_input("تاريخ الميلاد", None)
        
        st.markdown("### 👨‍👩‍👦 معلومات ولي الأمر")
        parent_name = st.text_input("اسم ولي الأمر *", placeholder="أحمد محمود")
        parent_phone = st.text_input("رقم الهاتف *", placeholder="01XXXXXXXXX")
        parent_whatsapp = st.text_input("رقم الواتساب (للتواصل السريع)", placeholder="01XXXXXXXXX")
        
        st.markdown("### 📍 معلومات إضافية")
        address = st.text_area("العنوان", height=60, placeholder="المدينة - المنطقة - العنوان بالكامل")
        notes = st.text_area("ملاحظات إضافية (اختياري)", height=80, placeholder="أي معلومات إضافية تود إضافتها مثل خبرات سابقة أو إصابات...")
        
        submitted = st.form_submit_button("📝 تقديم طلب التسجيل", use_container_width=True)
        
        if submitted:
            if player_name and age_group and parent_name and parent_phone:
                data = {
                    'playerName': player_name,
                    'ageGroup': age_group,
                    'birthDate': str(birth_date) if birth_date else "",
                    'parentName': parent_name,
                    'parentPhone': parent_phone,
                    'parentWhatsapp': parent_whatsapp,
                    'address': address,
                    'notes': notes
                }
                if save_registration(data):
                    st.session_state.show_success = True
                    st.rerun()
                else:
                    st.error("❌ حدث خطأ في حفظ البيانات، يرجى المحاولة مرة أخرى")
            else:
                st.error("⚠️ يرجى ملء جميع الحقول المطلوبة")

# ===== صفحة الأسئلة الشائعة (الصفحة 6) =====
elif page == 'faq':
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1e3a8a, #3b82f6); border-radius: 24px; padding: 55px 20px; text-align: center; margin-bottom: 45px;">
        <h1 style="color: white; font-size: 2.5rem; margin-bottom: 12px;">الأسئلة الشائعة</h1>
        <p style="color: #e2e8f0;">إجابات على أكثر الأسئلة شيوعًا من أولياء الأمور</p>
    </div>
    """, unsafe_allow_html=True)
    
    faqs = [
        ("ما الذي يميز الكوتش أكاديمي عن غيرها؟", 
         "الكوتش أكاديمي تتبنى منهجية تدريب متكاملة تركز على: التدريب الذهني وتطوير الذكاء الكروي، متابعة فردية لكل لاعب مع خطة تطوير شخصية، استخدام التكنولوجيا في تحليل الأداء، شراكات مع أندية محلية لدعم الموهوبين."),
        
        ("ما هي مدة التدريب وأوقاته؟", 
         "الموسم التدريبي يمتد لمدة 10 أشهر، من سبتمبر إلى يونيو. التدريبات في الفترة المسائية أيام السبت والخميس حسب الجدول المحدد لكل فئة عمرية، بما يتناسب مع أوقات المدارس."),
        
        ("ما هي تكلفة الاشتراك وآلية الدفع؟", 
         "تختلف التكلفة حسب الفئة العمرية وعدد أيام التدريب. نقدم خصومات للأشقاء، نظام تقسيط شهري مرن، ومنح جزئية للمتميزين ماليًا. يرجى التواصل معنا لمعرفة التفاصيل الدقيقة."),
        
        ("ما هي متطلبات الانضمام للأكاديمية؟", 
         "للانضمام للأكاديمية نحتاج إلى: إكمال نموذج التسجيل عبر الموقع، أن يكون اللاعب في الفئة العمرية المحددة، الرغبة الحقيقية في التعلم والتطوير، الالتزام بمواعيد التدريب، ودفع رسوم الاشتراك."),
        
        ("هل هناك تدريبات خاصة للمبتدئين؟", 
         "نعم، لدينا برامج خاصة للمبتدئين تركز على: تعلم أساسيات كرة القدم، تطوير المهارات الحركية الأساسية، بناء الثقة بالنفس، تعزيز حب الرياضة واللعب الجماعي."),
        
        ("كيف يمكن متابعة تطور اللاعب؟", 
         "نوفر نظام متابعة شامل يشمل: تقييم دوري للمهارات الفنية، متابعة التطور البدني، تقرير عن المشاركة والالتزام، لقاءات دورية مع أولياء الأمور، وفيديوهات تحليل أداء."),
        
        ("ماذا عن السلامة والإصابات خلال التدريب؟", 
         "السلامة أولوية لدينا، ونوفر: إشراف مستمر من مدربين مؤهلين، بيئة تدريب آمنة ومجهزة، برنامج إحماء وتبريد مناسب، مدربين حاصلين على شهادات في الإسعافات الأولية، وتأمين صحي للاعبين."),
        
        ("هل يمكن للاعب الانتقال بين الفئات العمرية؟", 
         "نعم، يمكن للاعب الانتقال بين الفئات بناءً على: تطور مهاراته وقدراته، توصية المدرب المسؤول، موافقة ولي الأمر، التقييم الدوري للأداء."),
        
        ("ما هي اللغات المستخدمة في التدريب؟", 
         "التدريب يتم باللغة العربية مع استخدام مصطلحات إنجليزية في بعض التمارين المتخصصة، مما يساعد اللاعبين على فهم المصطلحات العالمية."),
        
        ("هل هناك فريق نسائي؟", 
         "نعم، لدينا تدريبات مخصصة للبنات في أيام السبت والخميس، مع مدربات متخصصات وبيئة مناسبة ومحترمة تلبي احتياجات الفتيات.")
    ]
    
    for q, a in faqs:
        with st.expander(f"❓ {q}"):
            st.markdown(f'<p style="color: #334155; line-height: 1.6;">{a}</p>', unsafe_allow_html=True)

# ===== صفحة اتصل بنا (الصفحة 7) =====
elif page == 'contact':
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1e3a8a, #3b82f6); border-radius: 24px; padding: 55px 20px; text-align: center; margin-bottom: 45px;">
        <h1 style="color: white; font-size: 2.5rem; margin-bottom: 12px;">اتصل بنا</h1>
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
                <div><a href="tel:01069238878" style="text-decoration: none; color: #334155; font-size: 1.1rem;">01069238878</a></div>
            </div>
            <div class="contact-item">
                <div style="font-size: 1.5rem;">💬</div>
                <div><a href="https://wa.me/201285197778" target="_blank" style="text-decoration: none; color: #25D366; font-size: 1.1rem;">01285197778 (واتساب)</a></div>
            </div>
            <div class="contact-item">
                <div style="font-size: 1.5rem;">📍</div>
                <div style="color: #334155;">
                    <strong>العنوان:</strong><br>
                    محافظة أسيوط - مصر<br>
                    على ملاعب مدرسة السلام المتطورة
                </div>
            </div>
            <div class="contact-item">
                <div style="font-size: 1.5rem;">⏰</div>
                <div style="color: #334155;">
                    <strong>أوقات العمل:</strong><br>
                    السبت والخميس: 4:00 مساءً - 9:00 مساءً<br>
                    باقي الأيام: إجازة (للرد على الاستفسارات)
                </div>
            </div>
            <div class="contact-item">
                <div style="font-size: 1.5rem;">📧</div>
                <div style="color: #334155;">
                    <strong>البريد الإلكتروني:</strong><br>
                    info@elcoach-academy.com
                </div>
            </div>
        </div>
        
        <div class="map-container">
            <iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d113686.258448786!2d31.156289!3d27.186696!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x1438a5f5c5b5b5b5%3A0x5b5b5b5b5b5b5b5b!2z2YXZg9mF2YrYp9mG2Ykg2KfZhNiq2YbYqSDYp9mE2YXYqtmG2Kkg2KfZhNir2YTYp9mG2Ykg2KfZhNi52YjYp9mG!5e0!3m2!1sar!2seg!4v1700000000000!5m2!1sar!2seg" 
                    allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="contact-card">
            <h3 style="color: #1e3a8a; margin-bottom: 25px;">✉️ أرسل رسالة</h3>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("contact_form"):
            c_name = st.text_input("الاسم *")
            c_phone = st.text_input("رقم الهاتف *", placeholder="010XXXXXXXX")
            c_email = st.text_input("البريد الإلكتروني", placeholder="example@email.com")
            c_subject = st.selectbox("الموضوع *", ["", "استفسار عام", "معلومات عن البرامج", "التسجيل", "شكوى أو اقتراح", "طلب شراكة", "أخرى"])
            c_msg = st.text_area("الرسالة *", height=120, placeholder="اكتب رسالتك هنا...")
            
            submitted = st.form_submit_button("📨 إرسال الرسالة", use_container_width=True)
            
            if submitted:
                if c_name and c_phone and c_subject and c_msg:
                    data = {
                        'name': c_name,
                        'phone': c_phone,
                        'email': c_email,
                        'subject': c_subject,
                        'message': c_msg
                    }
                    if save_contact(data):
                        st.success("✅ شكراً لتواصلك! تم إرسال رسالتك بنجاح وسنرد عليك خلال 24 ساعة.")
                    else:
                        st.error("❌ حدث خطأ في حفظ البيانات، يرجى المحاولة مرة أخرى")
                else:
                    st.error("⚠️ يرجى ملء جميع الحقول المطلوبة")

# إغلاق حاوية المحتوى
st.markdown('</div>', unsafe_allow_html=True)

# ===== الفوتر =====
st.markdown("""
<div class="main-footer">
    <div class="footer-grid">
        <div>
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 18px;">
                <div style="width: 50px; height: 50px; background: linear-gradient(135deg, #3b82f6, #1e3a8a); border-radius: 14px; display: flex; align-items: center; justify-content: center; font-size: 1.6rem;">⚽</div>
                <h3 style="color: white; margin: 0;">الكوتش أكاديمي</h3>
            </div>
            <p style="color: #cbd5e1; font-size: 0.85rem; line-height: 1.7;">تأسست عام 2020 على ملاعب مدرسة السلام المتطورة. أول أكاديمية متخصصة في مصر تركز على بناء اللاعب الشامل من الناحية الفنية والبدنية والنفسية، تحت إشراف مدربين معتمدين دوليًا.</p>
        </div>
        <div>
            <h4 style="color: white; margin-bottom: 18px;">روابط سريعة</h4>
            <ul style="list-style: none; padding: 0;">
                <li style="margin-bottom: 12px;"><a href="#" onclick="navigateToPage('home'); return false;" class="footer-link">← الرئيسية</a></li>
                <li style="margin-bottom: 12px;"><a href="#" onclick="navigateToPage('about'); return false;" class="footer-link">← من نحن</a></li>
                <li style="margin-bottom: 12px;"><a href="#" onclick="navigateToPage('programs'); return false;" class="footer-link">← البرامج التدريبية</a></li>
                <li style="margin-bottom: 12px;"><a href="#" onclick="navigateToPage('coaches'); return false;" class="footer-link">← المدربون</a></li>
                <li style="margin-bottom: 12px;"><a href="#" onclick="navigateToPage('registration'); return false;" class="footer-link">← تسجيل لاعب جديد</a></li>
                <li style="margin-bottom: 12px;"><a href="#" onclick="navigateToPage('faq'); return false;" class="footer-link">← الأسئلة الشائعة</a></li>
                <li style="margin-bottom: 12px;"><a href="#" onclick="navigateToPage('contact'); return false;" class="footer-link">← اتصل بنا</a></li>
            </ul>
        </div>
        <div>
            <h4 style="color: white; margin-bottom: 18px;">معلومات الاتصال</h4>
            <ul style="list-style: none; padding: 0;">
                <li style="margin-bottom: 14px; display: flex; gap: 12px;">
                    <span>📍</span>
                    <span style="color: #cbd5e1;">أسيوط - مصر<br>ملاعب مدرسة السلام المتطورة</span>
                </li>
                <li style="margin-bottom: 14px; display: flex; gap: 12px;">
                    <span>📞</span>
                    <a href="tel:01069238878" style="color: #cbd5e1; text-decoration: none;">01069238878</a>
                </li>
                <li style="margin-bottom: 14px; display: flex; gap: 12px;">
                    <span>💬</span>
                    <a href="https://wa.me/201285197778" target="_blank" style="color: #25D366; text-decoration: none;">01285197778 (واتساب)</a>
                </li>
                <li style="margin-bottom: 14px; display: flex; gap: 12px;">
                    <span>⏰</span>
                    <span style="color: #cbd5e1;">السبت والخميس: 4م - 9م</span>
                </li>
            </ul>
        </div>
    </div>
    <div style="text-align: center; padding-top: 25px; border-top: 1px solid rgba(255, 255, 255, 0.1);">
        <p style="color: #94a3b8;">© 2025 الكوتش أكاديمي - جميع الحقوق محفوظة</p>
        <p style="color: #94a3b8; margin-top: 8px; font-size: 0.8rem;">أكاديمية كرة القدم المتخصصة | صناعة أبطال المستقبل</p>
        <p style="color: #94a3b8; margin-top: 6px; font-size: 0.75rem;">تأسست عام 2020 على يد: كابتن ميخائيل كميل (ميخا)، كابتن اندرو، كابتن مينا</p>
        <p style="color: #94a3b8; margin-top: 5px; font-size: 0.7rem;">بدعم من الأب الروحي للأكاديمية: مستر / مؤنس منير</p>
    </div>
</div>

<script>
// تأكيد وجود وظيفة navigateToPage في النطاق العام
window.navigateToPage = function(page) {
    const url = new URL(window.location);
    url.searchParams.set('page', page);
    window.location.href = url.toString();
};
</script>
""", unsafe_allow_html=True)
