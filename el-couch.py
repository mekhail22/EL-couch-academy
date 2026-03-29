import streamlit as st
import json
import os
from datetime import datetime

# إعدادات الصفحة - يجب أن تكون أول أمر في التطبيق
st.set_page_config(
    page_title="الكوتش أكاديمي",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ===== إخفاء الشريط العلوي لـ Streamlit بالكامل =====
st.markdown("""
<style>
    /* إخفاء كل شيء متعلق بـ Streamlit */
    header {
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
    
    /* إزالة كل المسافات العلوية */
    .main .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        padding-left: 0rem !important;
        padding-right: 0rem !important;
        max-width: 100% !important;
    }
    
    /* جعل الخلفية بيضاء */
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
    
    body {
        background-color: white;
    }
    
    /* ===== الهيدر المخصص ===== */
    .main-header {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        background-color: white;
        box-shadow: 0 2px 15px rgba(0, 0, 0, 0.08);
        z-index: 1000;
        padding: 12px 0;
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
        gap: 12px;
    }
    
    .logo-icon {
        width: 50px;
        height: 50px;
        background: linear-gradient(135deg, #2563eb, #1e3a8a);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 28px;
        box-shadow: 0 4px 10px rgba(37, 99, 235, 0.3);
    }
    
    .logo-text h1 {
        font-size: 1.4rem;
        margin: 0;
        color: #1e3a8a;
    }
    
    .logo-text span {
        color: #f59e0b;
    }
    
    .logo-text p {
        font-size: 0.75rem;
        color: #666;
        margin: 0;
    }
    
    /* ===== برجر منيو ===== */
    .burger-btn {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        width: 32px;
        height: 24px;
        background: transparent;
        border: none;
        cursor: pointer;
        padding: 0;
        z-index: 1002;
        position: relative;
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
        transform: rotate(45deg) translate(7px, 7px);
    }
    
    .burger-btn.active span:nth-child(2) {
        opacity: 0;
    }
    
    .burger-btn.active span:nth-child(3) {
        transform: rotate(-45deg) translate(7px, -7px);
    }
    
    /* ===== القائمة الجانبية ===== */
    .side-menu {
        position: fixed;
        top: 0;
        right: -300px;
        width: 280px;
        height: 100vh;
        background-color: white;
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
        margin-bottom: 5px;
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
        z-index: 1000;
        display: none;
    }
    
    .menu-overlay.show {
        display: block;
    }
    
    /* مساحة تعويضية */
    .header-spacer {
        height: 74px;
    }
    
    /* ===== حاوية المحتوى ===== */
    .content-wrapper {
        width: 95%;
        max-width: 1200px;
        margin: 0 auto;
        padding: 20px 15px;
    }
    
    /* ===== تنسيقات للشاشات الصغيرة ===== */
    @media (max-width: 768px) {
        .logo-icon {
            width: 42px;
            height: 42px;
            font-size: 22px;
        }
        .logo-text h1 {
            font-size: 1.1rem;
        }
        .logo-text p {
            font-size: 0.65rem;
        }
        .header-spacer {
            height: 68px;
        }
        .side-menu {
            width: 260px;
        }
        .side-menu a {
            padding: 12px 16px;
            font-size: 14px;
        }
    }
    
    /* ===== باقي التنسيقات ===== */
    /* الأزرار */
    .custom-btn {
        background-color: #f59e0b;
        color: #1e293b;
        padding: 14px 40px;
        border-radius: 12px;
        font-weight: 700;
        border: none;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        font-size: 18px;
    }
    
    .custom-btn:hover {
        background-color: #d97706;
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
    }
    
    /* بطاقات */
    .stat-card {
        background: white;
        padding: 25px 20px;
        border-radius: 16px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
        border: 1px solid #e2e8f0;
    }
    
    .stat-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.12);
    }
    
    .stat-number {
        font-size: 2.2rem;
        font-weight: bold;
        color: #1e3a8a;
        display: block;
    }
    
    .feature-card {
        background: #f8fafc;
        padding: 30px 20px;
        border-radius: 16px;
        text-align: center;
        transition: all 0.3s ease;
        height: 100%;
    }
    
    .feature-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.1);
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 15px;
    }
    
    .hero-section {
        background: linear-gradient(rgba(0, 0, 0, 0.65), rgba(0, 0, 0, 0.6)), url('https://images.unsplash.com/photo-1575361204480-aadea25e6e68?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80');
        background-size: cover;
        background-position: center;
        border-radius: 20px;
        padding: 70px 20px;
        text-align: center;
        margin-bottom: 40px;
    }
    
    .hero-section h1 {
        color: white;
        font-size: 2.2rem;
        margin-bottom: 15px;
    }
    
    .hero-section p {
        color: #e2e8f0;
        max-width: 600px;
        margin: 0 auto;
        font-size: 1rem;
    }
    
    .page-title {
        background: linear-gradient(135deg, #1e3a8a, #2563eb);
        border-radius: 20px;
        padding: 50px 20px;
        text-align: center;
        margin-bottom: 40px;
    }
    
    .page-title h1 {
        color: white;
        font-size: 2rem;
        margin-bottom: 10px;
    }
    
    .page-title p {
        color: #e2e8f0;
    }
    
    h2 {
        font-size: 1.8rem;
        color: #1e3a8a;
        text-align: center;
        margin-bottom: 30px;
        position: relative;
        padding-bottom: 12px;
    }
    
    h2:after {
        content: '';
        position: absolute;
        bottom: 0;
        right: 50%;
        transform: translateX(50%);
        width: 60px;
        height: 3px;
        background-color: #f59e0b;
        border-radius: 2px;
    }
    
    .program-card {
        background: white;
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
        height: 100%;
        border: 1px solid #e2e8f0;
    }
    
    .program-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.12);
    }
    
    .program-img {
        height: 150px;
        background: linear-gradient(135deg, #2563eb, #1e3a8a);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 3rem;
        color: white;
    }
    
    .program-body {
        padding: 20px;
    }
    
    .coach-card {
        background: white;
        border-radius: 16px;
        overflow: hidden;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
        height: 100%;
        border: 1px solid #e2e8f0;
    }
    
    .coach-card:hover {
        transform: translateY(-8px);
    }
    
    .coach-img {
        height: 180px;
        background: linear-gradient(135deg, #2563eb, #1e3a8a);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 3.5rem;
        color: white;
    }
    
    .coach-body {
        padding: 20px;
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
    
    .contact-info-card {
        background: #f8fafc;
        padding: 25px;
        border-radius: 16px;
        height: 100%;
    }
    
    hr {
        margin: 40px 0;
        border: none;
        height: 1px;
        background: linear-gradient(to right, transparent, #cbd5e1, transparent);
    }
    
    @media (max-width: 768px) {
        .hero-section h1 {
            font-size: 1.6rem;
        }
        h2 {
            font-size: 1.4rem;
        }
        .page-title h1 {
            font-size: 1.5rem;
        }
        .stat-number {
            font-size: 1.6rem;
        }
    }
</style>

<script>
// وظيفة التنقل بين الصفحات
function goToPage(page) {
    const url = new URL(window.location);
    url.searchParams.set('page', page);
    window.history.pushState({}, '', url);
    window.location.reload();
}

// برجر منيو
document.addEventListener('DOMContentLoaded', function() {
    const burgerBtn = document.getElementById('burgerBtn');
    const sideMenu = document.getElementById('sideMenu');
    const menuOverlay = document.getElementById('menuOverlay');
    
    if (burgerBtn) {
        burgerBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            this.classList.toggle('active');
            sideMenu.classList.toggle('open');
            menuOverlay.classList.toggle('show');
        });
    }
    
    if (menuOverlay) {
        menuOverlay.addEventListener('click', function() {
            this.classList.remove('show');
            sideMenu.classList.remove('open');
            burgerBtn.classList.remove('active');
        });
    }
    
    // إغلاق القائمة عند الضغط على ESC
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            menuOverlay.classList.remove('show');
            sideMenu.classList.remove('open');
            if (burgerBtn) burgerBtn.classList.remove('active');
        }
    });
});
</script>
""", unsafe_allow_html=True)

# ===== التحقق من وجود صورة الشعار =====
logo_exists = os.path.exists('logo.jpg')

# ===== الهيدر المخصص =====
if logo_exists:
    logo_icon_html = f'<div class="logo-icon" style="background-image: url(\'logo.jpg\'); background-size: cover; background-position: center;"></div>'
else:
    logo_icon_html = '<div class="logo-icon">⚽</div>'

header_html = f'''
<div class="main-header">
    <div class="header-inner">
        <div class="logo-area">
            {logo_icon_html}
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

# ===== ملفات حفظ البيانات =====
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

# ===== الحصول على الصفحة الحالية =====
query_params = st.query_params
if 'page' in query_params:
    st.session_state.page = query_params['page']

page = st.session_state.page

# حاوية المحتوى
st.markdown('<div class="content-wrapper">', unsafe_allow_html=True)

# ===== الصفحة الرئيسية =====
if page == 'home':
    st.markdown("""
    <div class="hero-section">
        <h1>⚽ الكوتش أكاديمي</h1>
        <p>أول أكاديمية متخصصة في مصر تركز على بناء اللاعب الشامل من الناحية الفنية والبدنية والنفسية، تحت إشراف مدربين معتمدين دوليًا.</p>
        <p style="font-weight: 600; margin-top: 15px;">نحن لا نصنع لاعبين فقط.. نحن نصنع قادة!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # زر التسجيل
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 40px;">
            <button class="custom-btn" onclick="goToPage('registration')">📝 سجل ابنك الآن</button>
        </div>
        """, unsafe_allow_html=True)
    
    # الإحصائيات
    st.markdown("<h2>إنجازات الأكاديمية</h2>", unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #64748b; margin-bottom: 30px;">أرقام تتحدث عن نجاح مسيرتنا</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="stat-card">
            <div style="font-size: 2.5rem; margin-bottom: 10px;">👥</div>
            <span class="stat-number">300+</span>
            <div style="margin-top: 8px;">لاعب مدرب</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="stat-card">
            <div style="font-size: 2.5rem; margin-bottom: 10px;">👨‍🏫</div>
            <span class="stat-number">8</span>
            <div style="margin-top: 8px;">مدرب محترف</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="stat-card">
            <div style="font-size: 2.5rem; margin-bottom: 10px;">🏆</div>
            <span class="stat-number">100+</span>
            <div style="margin-top: 8px;">لاعب محترف</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # المميزات
    st.markdown("<h2>لماذا تختار الكوتش أكاديمي؟</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🧠</div>
            <h3 style="color: #1e3a8a;">منهجية التدريب الذهني</h3>
            <p>نركز على تطوير الذكاء الكروي والقدرة على اتخاذ القرارات السريعة.</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🛡️</div>
            <h3 style="color: #1e3a8a;">بيئة آمنة محفزة</h3>
            <p>نوفر بيئة تدريب آمنة تحترم الفروق الفردية وتشجع على الإبداع.</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🤝</div>
            <h3 style="color: #1e3a8a;">شراكات مع الأندية</h3>
            <p>لدينا شراكات مع أندية محلية لتمكين الموهوبين من الانضمام للأندية الكبرى.</p>
        </div>
        """, unsafe_allow_html=True)

# ===== صفحة من نحن =====
elif page == 'about':
    st.markdown("""
    <div class="page-title">
        <h1>من نحن</h1>
        <p>الكوتش أكاديمي.. رؤية جديدة في عالم تدريب كرة القدم</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #2563eb, #1e3a8a); border-radius: 20px; height: 300px; display: flex; align-items: center; justify-content: center; font-size: 5rem; color: white;">
            ⚽
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <h2 style="text-align: right;">تأسيس الأكاديمية</h2>
        <p>تأسست الأكاديمية عام 2020 على يد:</p>
        <ul style="margin-right: 20px;">
            <li>كابتن ميخا</li>
            <li>كابتن اندرو</li>
            <li>كابتن مينا</li>
        </ul>
        <p style="margin-top: 15px;">على ملاعب مدرسة السلام المتطورة</p>
        <p style="font-weight: 600; color: #1e3a8a;">بدعم من الأب الروحي: مستر / مؤنس منير</p>
        """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div style="background: #f0f9ff; padding: 25px; border-radius: 16px; border-right: 4px solid #2563eb;">
            <h3>🎯 رسالتنا</h3>
            <p>تطوير جيل جديد من اللاعبين المبدعين القادرين على التألق محليًا ودوليًا.</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style="background: #fef3c7; padding: 25px; border-radius: 16px; border-right: 4px solid #f59e0b;">
            <h3>👁️ أهدافنا</h3>
            <p>أن نكون الوجهة الأولى لأي موهبة كروية في مصر والوطن العربي.</p>
        </div>
        """, unsafe_allow_html=True)

# ===== صفحة البرامج =====
elif page == 'programs':
    st.markdown("""
    <div class="page-title">
        <h1>البرامج التدريبية</h1>
        <p>مواعيد تدريبية مصممة لكل فئة عمرية</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="program-card">
            <div class="program-img">📅 السبت</div>
            <div class="program-body">
                <div style="background: #f8fafc; padding: 15px; border-radius: 12px;">
                    <p><strong>٥:٠٠ - ٦:٠٠ م</strong> → بنات</p>
                    <p><strong>٦:٠٠ - ٧:٣٠ م</strong> → بنين (١-٥ ابتدائي)</p>
                    <p><strong>٧:٣٠ - ٩:٠٠ م</strong> → بنين (٦ ابتدائي - ٢ إعدادي)</p>
                    <p style="margin-top: 12px; color: #666;">📍 ملاعب مدرسة السلام المتطورة</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="program-card">
            <div class="program-img">✅ الخميس</div>
            <div class="program-body">
                <div style="background: #f8fafc; padding: 15px; border-radius: 12px;">
                    <p><strong>٤:٣٠ - ٦:٠٠ م</strong> → بنات</p>
                    <p><strong>٦:٠٠ - ٨:٠٠ م</strong> → بنين (١-٥ ابتدائي)</p>
                    <p><strong>٨:٠٠ - ١٠:٠٠ م</strong> → بنين (٦ ابتدائي - ٢ إعدادي)</p>
                    <p style="margin-top: 12px; color: #666;">📍 ملاعب مدرسة السلام المتطورة</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ===== صفحة المدربون =====
elif page == 'coaches':
    st.markdown("""
    <div class="page-title">
        <h1>المدربون</h1>
        <p>فريقنا من المدربين المحترفين ذوي الخبرة</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="coach-card">
            <div class="coach-img">👨‍🏫</div>
            <div class="coach-body">
                <h3>كابتن/ميخائيل كميل</h3>
                <p style="color: #2563eb; font-weight: 600;">مدرب معتمد</p>
                <p style="font-size: 0.85rem;">بكالريوس تربية رياضية - رخصة CAF</p>
            </div>
        </div>
        <div class="coach-card">
            <div class="coach-img">🏃</div>
            <div class="coach-body">
                <h3>د. خالد السيد</h3>
                <p style="color: #2563eb; font-weight: 600;">مدرب لياقة بدنية</p>
                <p style="font-size: 0.85rem;">دكتوراه في علوم الرياضة</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="coach-card">
            <div class="coach-img">🧤</div>
            <div class="coach-body">
                <h3>كابتن أحمد علي</h3>
                <p style="color: #2563eb; font-weight: 600;">مدرب حراس مرمى</p>
                <p style="font-size: 0.85rem;">خبرة 15 عامًا</p>
            </div>
        </div>
        <div class="coach-card">
            <div class="coach-img">⚽</div>
            <div class="coach-body">
                <h3>كابتن محمد جابر</h3>
                <p style="color: #2563eb; font-weight: 600;">مدرب مهارات فنية</p>
                <p style="font-size: 0.85rem;">خبرة 12 عامًا</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ===== صفحة التسجيل =====
elif page == 'registration':
    st.markdown("""
    <div class="page-title">
        <h1>تسجيل لاعب جديد</h1>
        <p>انضم إلى الكوتش أكاديمي وابدأ رحلتك نحو الاحتراف</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.show_success:
        st.markdown('<div class="success-msg">✅ تم إرسال طلب التسجيل بنجاح! سنتواصل معكم خلال 24 ساعة.</div>', unsafe_allow_html=True)
        st.session_state.show_success = False
    
    with st.form("reg_form"):
        st.markdown("### 📋 معلومات اللاعب")
        player_name = st.text_input("اسم اللاعب الثلاثي *")
        age_group = st.selectbox("الفئة العمرية *", ["", "بنات", "١ ابتدائي - ٥ ابتدائي", "٦ ابتدائي - ٢ إعدادي"])
        
        st.markdown("### 👨‍👩‍👦 معلومات ولي الأمر")
        parent_name = st.text_input("اسم ولي الأمر *")
        parent_phone = st.text_input("رقم الهاتف *", placeholder="01XXXXXXXXX")
        notes = st.text_area("ملاحظات إضافية", height=80)
        
        submitted = st.form_submit_button("📝 تقديم طلب التسجيل", use_container_width=True)
        
        if submitted:
            if player_name and age_group and parent_name and parent_phone:
                if save_registration({'playerName': player_name, 'ageGroup': age_group, 'parentName': parent_name, 'parentPhone': parent_phone, 'notes': notes}):
                    st.session_state.show_success = True
                    st.rerun()
                else:
                    st.error("حدث خطأ، يرجى المحاولة مرة أخرى")
            else:
                st.error("يرجى ملء جميع الحقول المطلوبة")

# ===== صفحة الأسئلة =====
elif page == 'faq':
    st.markdown("""
    <div class="page-title">
        <h1>الأسئلة الشائعة</h1>
        <p>إجابات على أكثر الأسئلة شيوعًا</p>
    </div>
    """, unsafe_allow_html=True)
    
    faqs = [
        ("ما الذي يميز الكوتش أكاديمي عن غيرها؟", "الكوتش أكاديمي تتبنى منهجية تدريب متكاملة تركز على التدريب الذهني وتطوير الذكاء الكروي، ومتابعة فردية لكل لاعب."),
        ("ما هي مدة التدريب وأوقاته؟", "الموسم التدريبي يمتد لمدة 10 أشهر، من سبتمبر إلى يونيو. التدريبات في الفترة المسائية."),
        ("ما هي تكلفة الاشتراك؟", "تختلف التكلفة حسب الفئة العمرية. يرجى التواصل معنا لمعرفة التفاصيل."),
        ("ما هي متطلبات الانضمام؟", "إكمال نموذج التسجيل، أن يكون اللاعب في الفئة العمرية المحددة، الالتزام بمواعيد التدريب.")
    ]
    
    for q, a in faqs:
        with st.expander(f"❓ {q}"):
            st.markdown(a)

# ===== صفحة الاتصال =====
elif page == 'contact':
    st.markdown("""
    <div class="page-title">
        <h1>اتصل بنا</h1>
        <p>تواصل معنا لأي استفسارات</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="contact-info-card">
            <h3 style="color: #1e3a8a;">📞 معلومات الاتصال</h3>
            <div style="margin: 20px 0;"><span style="font-size: 1.3rem;">📱</span> <a href="tel:01069238878" style="text-decoration: none; color: #1e293b;">01069238878</a></div>
            <div style="margin: 20px 0;"><span style="font-size: 1.3rem;">💬</span> <a href="https://wa.me/201285197778" target="_blank" style="text-decoration: none; color: #25D366;">01285197778</a></div>
            <div style="margin: 20px 0;"><span style="font-size: 1.3rem;">📍</span> أسيوط - ملاعب مدرسة السلام المتطورة</div>
            <div style="margin: 20px 0;"><span style="font-size: 1.3rem;">⏰</span> السبت - الخميس: 4م - 9م</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        with st.form("contact_form"):
            st.markdown("<h3 style='color: #1e3a8a;'>✉️ أرسل رسالة</h3>", unsafe_allow_html=True)
            c_name = st.text_input("الاسم")
            c_phone = st.text_input("رقم الهاتف")
            c_subject = st.selectbox("الموضوع", ["", "استفسار عام", "معلومات عن البرامج", "التسجيل"])
            c_msg = st.text_area("الرسالة", height=100)
            if st.form_submit_button("📨 إرسال", use_container_width=True):
                if c_name and c_phone and c_subject and c_msg:
                    if save_contact({'name': c_name, 'phone': c_phone, 'subject': c_subject, 'message': c_msg}):
                        st.success("تم إرسال رسالتك بنجاح!")
                    else:
                        st.error("حدث خطأ")
                else:
                    st.error("يرجى ملء جميع الحقول")

# إغلاق حاوية المحتوى
st.markdown('</div>', unsafe_allow_html=True)

# ===== الفوتر =====
st.markdown("""
<div style="background-color: #1e293b; color: white; padding: 35px 0 20px; border-radius: 20px; margin-top: 50px;">
    <div style="width: 90%; max-width: 1200px; margin: 0 auto; text-align: center;">
        <p>© 2024 الكوتش أكاديمي - جميع الحقوق محفوظة</p>
        <p style="margin-top: 10px; font-size: 0.8rem; color: #94a3b8;">أكاديمية كرة القدم المتخصصة | صناعة أبطال المستقبل</p>
    </div>
</div>
""", unsafe_allow_html=True)
