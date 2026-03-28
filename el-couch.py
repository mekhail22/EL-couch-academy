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
    /* إخفاء الشريط العلوي بالكامل */
    header {
        visibility: hidden;
        height: 0px !important;
        display: none !important;
    }
    
    /* إخفاء القائمة الرئيسية (النقاط الثلاث) */
    #MainMenu {
        visibility: hidden;
        display: none;
    }
    
    /* إخفاء الفوتر */
    footer {
        visibility: hidden;
        display: none;
    }
    
    /* إخفاء الشريط الأبيض العلوي */
    .stApp > header {
        display: none !important;
    }
    
    .st-emotion-cache-18ni7ap {
        display: none !important;
    }
    
    .st-emotion-cache-1v0mbdj {
        display: none !important;
    }
    
    /* إزالة المسافة العلوية */
    .main .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        max-width: 100% !important;
    }
    
    /* ضبط الهيدر المخصص */
    .custom-header {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 999999;
        background-color: rgba(255, 255, 255, 0.98);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        padding: 15px 0;
        backdrop-filter: blur(5px);
    }
    
    /* مساحة تعويضية للهيدر */
    .custom-header-spacer {
        height: 90px;
    }
    
    /* تنسيق الروابط في الهيدر للشاشات الكبيرة */
    .nav-links {
        display: flex;
        gap: 5px;
        flex-wrap: wrap;
        justify-content: center;
    }
    
    .nav-link {
        padding: 10px 15px;
        background: none;
        border: none;
        cursor: pointer;
        font-weight: 600;
        color: #1e293b;
        text-decoration: none;
        display: inline-block;
        transition: all 0.3s ease;
        border-radius: 6px;
        font-size: 14px;
    }
    
    .nav-link:hover {
        background-color: rgba(59, 130, 246, 0.1);
        color: #3b82f6;
    }
    
    .nav-link.active {
        background-color: #3b82f6;
        color: white;
    }
    
    /* برجر منيو - يظهر فقط في الهواتف */
    .burger-menu {
        display: none;
        flex-direction: column;
        justify-content: space-between;
        width: 30px;
        height: 21px;
        background: transparent;
        border: none;
        cursor: pointer;
        padding: 0;
        z-index: 1001;
    }
    
    .burger-menu span {
        width: 100%;
        height: 3px;
        background-color: #1e3a8a;
        border-radius: 2px;
        transition: all 0.3s ease;
    }
    
    .burger-menu.active span:nth-child(1) {
        transform: rotate(45deg) translate(6px, 6px);
    }
    
    .burger-menu.active span:nth-child(2) {
        opacity: 0;
    }
    
    .burger-menu.active span:nth-child(3) {
        transform: rotate(-45deg) translate(6px, -6px);
    }
    
    /* القائمة الجانبية للهواتف */
    .side-nav {
        position: fixed;
        top: 0;
        right: -300px;
        width: 280px;
        height: 100vh;
        background-color: white;
        box-shadow: -5px 0 15px rgba(0, 0, 0, 0.1);
        z-index: 1000;
        transition: all 0.3s ease;
        overflow-y: auto;
        padding-top: 80px;
    }
    
    .side-nav.active {
        right: 0;
    }
    
    .side-nav ul {
        list-style: none;
        padding: 20px;
    }
    
    .side-nav li {
        margin-bottom: 15px;
    }
    
    .side-nav a {
        display: flex;
        align-items: center;
        gap: 15px;
        color: #1e293b;
        text-decoration: none;
        font-weight: 600;
        padding: 12px 15px;
        border-radius: 8px;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .side-nav a:hover, .side-nav a.active {
        background-color: rgba(59, 130, 246, 0.1);
        color: #3b82f6;
    }
    
    .nav-overlay {
        position: fixed;
        top: 0;
        right: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.5);
        z-index: 999;
        display: none;
    }
    
    .nav-overlay.active {
        display: block;
    }
    
    /* تنسيق للهواتف */
    @media (max-width: 992px) {
        .nav-links {
            display: none;
        }
        .burger-menu {
            display: flex;
        }
        .custom-header-spacer {
            height: 70px;
        }
    }
    
    @media (max-width: 768px) {
        .custom-header {
            padding: 10px 0;
        }
        .nav-link {
            padding: 5px 8px;
            font-size: 12px;
        }
        .logo-title {
            font-size: 1.2rem !important;
        }
        .logo-subtitle {
            font-size: 0.7rem !important;
        }
    }
    
    /* تنسيق الشعار */
    .logo-img {
        width: 60px;
        height: 60px;
        border-radius: 10px;
        object-fit: cover;
        border: 2px solid #3b82f6;
    }
    
    @media (max-width: 768px) {
        .logo-img {
            width: 45px;
            height: 45px;
        }
    }
</style>

<script>
// جافا سكريبت للبرجر منيو والتنقل
document.addEventListener('DOMContentLoaded', function() {
    // عناصر البرجر منيو
    const burgerMenu = document.getElementById('burgerMenu');
    const sideNav = document.getElementById('sideNav');
    const navOverlay = document.getElementById('navOverlay');
    
    if (burgerMenu) {
        burgerMenu.addEventListener('click', function() {
            this.classList.toggle('active');
            sideNav.classList.toggle('active');
            navOverlay.classList.toggle('active');
        });
    }
    
    if (navOverlay) {
        navOverlay.addEventListener('click', function() {
            this.classList.remove('active');
            sideNav.classList.remove('active');
            burgerMenu.classList.remove('active');
        });
    }
    
    // إغلاق القائمة عند تغيير حجم النافذة
    window.addEventListener('resize', function() {
        if (window.innerWidth > 992) {
            if (sideNav) sideNav.classList.remove('active');
            if (navOverlay) navOverlay.classList.remove('active');
            if (burgerMenu) burgerMenu.classList.remove('active');
        }
    });
});
</script>
""", unsafe_allow_html=True)

# ===== التحقق من وجود صورة الشعار =====
logo_exists = os.path.exists('logo.jpg')

# ===== الهيدر المخصص مع برجر منيو =====
if logo_exists:
    logo_html = f'''
    <div class="logo-img" style="background-image: url('logo.jpg'); background-size: cover; background-position: center;"></div>
    '''
else:
    logo_html = '''
    <div class="logo-img" style="background: linear-gradient(45deg, #3b82f6, #1e3a8a); display: flex; align-items: center; justify-content: center;">
        <span style="font-size: 1.8rem;">⚽</span>
    </div>
    '''

st.markdown(f'''
<div class="custom-header">
    <div style="width: 90%; max-width: 1200px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center;">
        <div style="display: flex; align-items: center; gap: 10px;">
            {logo_html}
            <div>
                <h1 class="logo-title" style="font-size: 1.6rem; margin: 0; color: #1e3a8a;">الكوتش <span style="color: #f59e0b;">أكاديمي</span></h1>
                <p class="logo-subtitle" style="font-size: 0.9rem; color: #666; margin: 0;">أكاديمية كرة القدم المتخصصة</p>
            </div>
        </div>
        
        <!-- روابط للشاشات الكبيرة -->
        <div class="nav-links">
            <a class="nav-link" data-page="home">🏠 الرئيسية</a>
            <a class="nav-link" data-page="about">ℹ️ من نحن</a>
            <a class="nav-link" data-page="programs">⚽ البرامج</a>
            <a class="nav-link" data-page="coaches">👨‍🏫 المدربون</a>
            <a class="nav-link" data-page="registration">📝 التسجيل</a>
            <a class="nav-link" data-page="faq">❓ الأسئلة</a>
            <a class="nav-link" data-page="contact">📞 اتصل بنا</a>
        </div>
        
        <!-- زر برجر منيو للهواتف -->
        <button class="burger-menu" id="burgerMenu">
            <span></span>
            <span></span>
            <span></span>
        </button>
    </div>
</div>

<!-- القائمة الجانبية للهواتف -->
<div class="side-nav" id="sideNav">
    <ul>
        <li><a class="side-nav-link" data-page="home">🏠 الرئيسية</a></li>
        <li><a class="side-nav-link" data-page="about">ℹ️ من نحن</a></li>
        <li><a class="side-nav-link" data-page="programs">⚽ البرامج التدريبية</a></li>
        <li><a class="side-nav-link" data-page="coaches">👨‍🏫 المدربون</a></li>
        <li><a class="side-nav-link" data-page="registration">📝 تسجيل لاعب جديد</a></li>
        <li><a class="side-nav-link" data-page="faq">❓ الأسئلة الشائعة</a></li>
        <li><a class="side-nav-link" data-page="contact">📞 اتصل بنا</a></li>
    </ul>
</div>

<!-- طبقة التعتيم -->
<div class="nav-overlay" id="navOverlay"></div>

<div class="custom-header-spacer"></div>
''', unsafe_allow_html=True)

# ===== إدارة حالة الجلسة =====
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'show_success' not in st.session_state:
    st.session_state.show_success = False

# ===== جافا سكريبت للتنقل في نفس التاب =====
st.markdown("""
<script>
// وظيفة التنقل بين الصفحات بدون إعادة تحميل
function navigateTo(page) {
    // تحديث حالة الجلسة عبر Streamlit
    const url = new URL(window.location);
    url.searchParams.set('page', page);
    window.history.pushState({}, '', url);
    
    // تحديث الواجهة عبر Streamlit
    const event = new Event('streamlit:setQueryParams');
    window.dispatchEvent(event);
    
    // تحديث القائمة النشطة
    document.querySelectorAll('.nav-link, .side-nav-link').forEach(link => {
        link.classList.remove('active');
        if(link.getAttribute('data-page') === page) {
            link.classList.add('active');
        }
    });
    
    // إغلاق القائمة الجانبية
    const sideNav = document.getElementById('sideNav');
    const burgerMenu = document.getElementById('burgerMenu');
    const navOverlay = document.getElementById('navOverlay');
    if(sideNav) sideNav.classList.remove('active');
    if(burgerMenu) burgerMenu.classList.remove('active');
    if(navOverlay) navOverlay.classList.remove('active');
    
    // التمرير لأعلى
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// إضافة مستمعي الأحداث لروابط التنقل
document.addEventListener('DOMContentLoaded', function() {
    // روابط القائمة العلوية
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const page = this.getAttribute('data-page');
            navigateTo(page);
        });
    });
    
    // روابط القائمة الجانبية
    document.querySelectorAll('.side-nav-link').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const page = this.getAttribute('data-page');
            navigateTo(page);
        });
    });
    
    // تحديث القائمة النشطة بناءً على الصفحة الحالية
    function updateActiveLink() {
        const urlParams = new URLSearchParams(window.location.search);
        const currentPage = urlParams.get('page') || 'home';
        
        document.querySelectorAll('.nav-link, .side-nav-link').forEach(link => {
            link.classList.remove('active');
            if(link.getAttribute('data-page') === currentPage) {
                link.classList.add('active');
            }
        });
    }
    
    updateActiveLink();
    
    // مراقبة تغييرات URL
    window.addEventListener('popstate', function() {
        updateActiveLink();
        window.location.reload();
    });
});
</script>
""", unsafe_allow_html=True)

# ===== ملفات حفظ البيانات =====
DATA_FILE = 'registrations.json'
CONTACT_FILE = 'contacts.json'

def save_registration(data):
    """حفظ بيانات التسجيل"""
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
    except Exception as e:
        st.error(f"حدث خطأ: {e}")
        return False

def save_contact(data):
    """حفظ بيانات الاتصال"""
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
    except Exception as e:
        st.error(f"حدث خطأ: {e}")
        return False

# ===== CSS العام للتطبيق =====
st.markdown("""
<style>
    /* تنسيقات عامة */
    .main {
        direction: rtl;
        text-align: right;
    }
    
    .stApp {
        direction: rtl;
    }
    
    /* تنسيق الأزرار */
    .stButton > button {
        background-color: #3b82f6;
        color: white;
        padding: 12px 30px;
        border-radius: 5px;
        font-weight: 600;
        border: none;
        transition: all 0.3s ease;
        width: auto;
        cursor: pointer;
    }
    
    .stButton > button:hover {
        background-color: #1e3a8a;
        transform: translateY(-3px);
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.15);
    }
    
    /* تنسيق الحقول */
    .stTextInput > div > div > input,
    .stSelectbox > div > div,
    .stTextArea > div > div > textarea {
        text-align: right;
        padding: 12px 15px;
        border: 1px solid #cbd5e1;
        border-radius: 5px;
    }
    
    /* العناوين */
    h1 {
        font-size: 2.8rem;
        color: #1e293b;
        margin-bottom: 1rem;
    }
    
    h2 {
        font-size: 2.2rem;
        color: #1e3a8a;
        position: relative;
        padding-bottom: 15px;
        margin-bottom: 2rem;
    }
    
    h2:after {
        content: '';
        position: absolute;
        bottom: 0;
        right: 0;
        width: 80px;
        height: 4px;
        background-color: #f59e0b;
        border-radius: 2px;
    }
    
    /* بطاقات */
    .card {
        background-color: #f8fafc;
        padding: 30px;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        text-align: center;
        margin-bottom: 20px;
        height: 100%;
    }
    
    .card:hover {
        transform: translateY(-10px);
        box-shadow: 0 15px 30px rgba(0, 0, 0, 0.1);
    }
    
    .card-icon {
        font-size: 2.5rem;
        color: #3b82f6;
        margin-bottom: 20px;
    }
    
    .card h3 {
        color: #1e3a8a;
        margin-bottom: 15px;
    }
    
    /* بطاقات البرامج */
    .program-card {
        background-color: white;
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        margin-bottom: 20px;
        height: 100%;
    }
    
    .program-card:hover {
        transform: translateY(-10px);
    }
    
    .program-image {
        height: 200px;
        background: linear-gradient(45deg, #3b82f6, #1e3a8a);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 4rem;
    }
    
    .program-content {
        padding: 25px;
    }
    
    /* بطاقات المدربين */
    .coach-card {
        background-color: white;
        border-radius: 10px;
        overflow: hidden;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        margin-bottom: 20px;
        height: 100%;
    }
    
    .coach-card:hover {
        transform: translateY(-10px);
    }
    
    .coach-image {
        height: 250px;
        background: linear-gradient(45deg, #3b82f6, #1e3a8a);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 5rem;
    }
    
    .coach-info {
        padding: 20px;
    }
    
    .coach-info h3 {
        color: #1e3a8a;
        margin-bottom: 5px;
    }
    
    /* تنسيقات الإحصائيات */
    .stat-box {
        padding: 30px 20px;
        background-color: white;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        text-align: center;
        transition: all 0.3s ease;
        margin-bottom: 20px;
    }
    
    .stat-box:hover {
        transform: translateY(-10px);
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1e3a8a;
        display: block;
    }
    
    /* البطل (Hero) */
    .hero {
        background: linear-gradient(rgba(0, 0, 0, 0.75), rgba(0, 0, 0, 0.7)), url('https://images.unsplash.com/photo-1575361204480-aadea25e6e68?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80');
        background-size: cover;
        background-position: center;
        color: white;
        padding: 100px 0;
        text-align: center;
        border-radius: 10px;
        margin-bottom: 30px;
    }
    
    .hero h1 {
        color: white;
        font-size: 3.2rem;
        margin-bottom: 20px;
    }
    
    .hero p {
        font-size: 1.2rem;
        max-width: 800px;
        margin: 0 auto 30px;
        color: #e2e8f0;
    }
    
    /* تنسيقات الصفحات */
    .page-header {
        background: linear-gradient(rgba(30, 58, 138, 0.9), rgba(30, 58, 138, 0.85));
        color: white;
        text-align: center;
        padding: 80px 0 50px;
        border-radius: 10px;
        margin-bottom: 40px;
    }
    
    .page-header h1 {
        color: white;
        font-size: 2.5rem;
    }
    
    .page-header p {
        color: #e2e8f0;
        max-width: 700px;
        margin: 0 auto;
    }
    
    /* رسالة النجاح */
    .success-message {
        background-color: #10b981;
        color: white;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 20px;
        text-align: center;
        animation: fadeOut 3s ease forwards;
    }
    
    @keyframes fadeOut {
        0% { opacity: 1; }
        70% { opacity: 1; }
        100% { opacity: 0; display: none; }
    }
    
    /* تنسيقات الروابط */
    .phone-link, .whatsapp-link, .map-link {
        color: inherit;
        text-decoration: none;
        transition: color 0.3s;
    }
    
    .phone-link:hover, .map-link:hover {
        color: #3b82f6;
        text-decoration: underline;
    }
    
    .whatsapp-link {
        color: #25D366;
    }
    
    .whatsapp-link:hover {
        color: #128C7E;
    }
    
    /* تنسيقات للشاشات الصغيرة */
    @media (max-width: 768px) {
        .hero h1 {
            font-size: 2rem;
        }
        
        h2 {
            font-size: 1.5rem;
        }
        
        .hero {
            padding: 60px 0;
        }
        
        .page-header {
            padding: 60px 0 40px;
        }
        
        .page-header h1 {
            font-size: 1.8rem;
        }
        
        .card, .program-card, .coach-card, .stat-box {
            margin-bottom: 15px;
        }
    }
</style>
""", unsafe_allow_html=True)

# ===== الحصول على الصفحة الحالية =====
query_params = st.query_params
if 'page' in query_params:
    st.session_state.page = query_params['page']

page = st.session_state.page

# ===== الصفحة الرئيسية =====
if page == 'home':
    # القسم الرئيسي
    st.markdown("""
    <div class="hero">
        <div style="width: 90%; max-width: 1200px; margin: 0 auto;">
            <h1>⚽ الكوتش أكاديمي</h1>
            <p>أول أكاديمية متخصصة في مصر تركز على بناء اللاعب الشامل من الناحية الفنية والبدنية والنفسية، تحت إشراف مدربين معتمدين دوليًا.</p>
            <p style="font-weight: 600; margin-bottom: 20px;">نحن لا نصنع لاعبين فقط.. نحن نصنع قادة!</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # أزرار الإجراء
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        # زر التسجيل مع التنقل في نفس الصفحة
        st.markdown("""
        <div style="text-align: center;">
            <button onclick="navigateTo('registration')" style="background-color: #f59e0b; color: #1e293b; padding: 12px 30px; border-radius: 5px; font-weight: 600; border: none; cursor: pointer; transition: all 0.3s ease; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1); font-size: 16px;">
                📝 سجل ابنك الآن
            </button>
        </div>
        """, unsafe_allow_html=True)
    
    # قسم الإحصائيات
    st.markdown("---")
    st.markdown('<h2 style="text-align: center;">إنجازات الأكاديمية</h2>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #64748b; margin-bottom: 40px;">أرقام تتحدث عن نجاح مسيرتنا في صناعة أبطال المستقبل</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="stat-box">
            <div class="card-icon">👥</div>
            <span class="stat-number">300+</span>
            <div>لاعب مدرب</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="stat-box">
            <div class="card-icon">👨‍🏫</div>
            <span class="stat-number">8</span>
            <div>مدرب محترف</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="stat-box">
            <div class="card-icon">🏆</div>
            <span class="stat-number">100+</span>
            <div>لاعب محترف</div>
        </div>
        """, unsafe_allow_html=True)
    
    # قسم المميزات
    st.markdown("---")
    st.markdown('<h2 style="text-align: center;">لماذا تختار الكوتش أكاديمي؟</h2>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #64748b; margin-bottom: 40px;">نحن نؤمن أن الموهبة تحتاج إلى منهجية علمية وتدريب منظم</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="card">
            <div class="card-icon">🧠</div>
            <h3>منهجية التدريب الذهني</h3>
            <p>نركز على تطوير الذكاء الكروي والقدرة على اتخاذ القرارات السريعة والصحيحة داخل الملعب.</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="card">
            <div class="card-icon">🛡️</div>
            <h3>بيئة آمنة محفزة</h3>
            <p>نوفر بيئة تدريب آمنة تحترم الفروق الفردية وتشجع على الإبداع والتميز.</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="card">
            <div class="card-icon">🤝</div>
            <h3>شراكات مع الأندية</h3>
            <p>لدينا شراكات مع أندية محلية لتمكين الموهوبين من الانضمام للمنتخبات والأندية الكبرى.</p>
        </div>
        """, unsafe_allow_html=True)

# ===== صفحة من نحن =====
elif page == 'about':
    st.markdown("""
    <div class="page-header">
        <div style="width: 90%; max-width: 1200px; margin: 0 auto;">
            <h1>من نحن</h1>
            <p>الكوتش أكاديمي.. رؤية جديدة في عالم تدريب كرة القدم</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div style="height: 400px; background: linear-gradient(45deg, #3b82f6, #1e3a8a); border-radius: 10px; display: flex; align-items: center; justify-content: center; color: white; font-size: 8rem;">
            ⚽
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <h2>تأسيس الأكاديمية</h2>
        <p>تأسست الأكاديمية عام 2020 على يد:</p>
        <ul>
            <li>كابتن ميخا</li>
            <li>كابتن اندرو</li>
            <li>كابتن مينا</li>
        </ul>
        <p>على ملاعب مدرسة السلام المتطورة</p>
        <p style="font-weight: 600; color: #1e3a8a;">بدعم من الأب الروحي للأكاديمية: مستر / مؤنس منير</p>
        """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div style="padding: 30px; border-radius: 10px; background-color: #f0f9ff; border-right: 4px solid #3b82f6; margin-top: 20px;">
            <h3>🎯 رسالتنا</h3>
            <p>تطوير جيل جديد من اللاعبين المبدعين القادرين على التألق محليًا ودوليًا، من خلال تقديم تدريب عصري يعتمد على أحدث الأساليب العلمية والتكنولوجية في عالم كرة القدم.</p>
            <ul>
                <li>تطوير المهارات الفنية الأساسية والمتقدمة</li>
                <li>بناء اللياقة البدنية المخصصة لكل لاعب</li>
                <li>تعزيز الذكاء الكروي والقدرات الذهنية</li>
                <li>غرس القيم الرياضية والسلوك القيادي</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style="padding: 30px; border-radius: 10px; background-color: #fef3c7; border-right: 4px solid #f59e0b; margin-top: 20px;">
            <h3>👁️ أهدافنا</h3>
            <p>أن نكون الوجهة الأولى لأي موهبة كروية في مصر والوطن العربي، والجسر الذي يعبر من خلاله اللاعبون الموهوبون إلى العالمية.</p>
            <ul>
                <li>صناعة لاعبين مؤهلين للدوريات العالمية</li>
                <li>تطوير منهج تدريبي يُدرس في المعاهد الرياضية</li>
                <li>المساهمة في تطوير كرة القدم العربية</li>
                <li>بناء قاعدة بيانات للمواهب الكروية</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# ===== صفحة البرامج التدريبية =====
elif page == 'programs':
    st.markdown("""
    <div class="page-header">
        <div style="width: 90%; max-width: 1200px; margin: 0 auto;">
            <h1>البرامج التدريبية</h1>
            <p>مواعيد تدريبية مصممة لكل فئة عمرية وجنسية</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<h2 style="text-align: center;">المواعيد التدريبية</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="program-card">
            <div class="program-image">📅</div>
            <div class="program-content">
                <h3>السبت</h3>
                <p>مواعيد تدريب السبت المخصصة للبنين والبنات</p>
                <div style="background-color: #f8fafc; padding: 15px; border-radius: 8px; border-right: 4px solid #f59e0b;">
                    <h4>المواعيد:</h4>
                    <div style="margin: 10px 0;"><strong>[٥:٠٠ - ٦:٠٠ م]</strong> - بنات</div>
                    <div style="margin: 10px 0;"><strong>[٦:٠٠ - ٧:٣٠ م]</strong> - بنين (١ ابتدائي - ٥ ابتدائي)</div>
                    <div style="margin: 10px 0;"><strong>[٧:٣٠ - ٩:٠٠ م]</strong> - بنين (٦ ابتدائي - ٢ إعدادي)</div>
                    <p style="margin-top: 15px; color: #666;">📍 جميع التدريبات في ملاعب مدرسة السلام المتطورة</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="program-card">
            <div class="program-image">✅</div>
            <div class="program-content">
                <h3>الخميس</h3>
                <p>مواعيد تدريب الخميس المخصصة للبنين والبنات</p>
                <div style="background-color: #f8fafc; padding: 15px; border-radius: 8px; border-right: 4px solid #f59e0b;">
                    <h4>المواعيد:</h4>
                    <div style="margin: 10px 0;"><strong>[٤:٣٠ - ٦:٠٠ م]</strong> - بنات</div>
                    <div style="margin: 10px 0;"><strong>[٦:٠٠ - ٨:٠٠ م]</strong> - بنين (١ ابتدائي - ٥ ابتدائي)</div>
                    <div style="margin: 10px 0;"><strong>[٨:٠٠ - ١٠:٠٠ م]</strong> - بنين (٦ ابتدائي - ٢ إعدادي)</div>
                    <p style="margin-top: 15px; color: #666;">📍 جميع التدريبات في ملاعب مدرسة السلام المتطورة</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="program-card">
            <div class="program-image">⚽</div>
            <div class="program-content">
                <h3>معلومات عامة</h3>
                <p>معلومات هامة حول البرامج التدريبية</p>
                <div style="background-color: #f8fafc; padding: 15px; border-radius: 8px;">
                    <h4>🎯 أهداف التدريب:</h4>
                    <ul>
                        <li>تنمية المهارات الفنية الأساسية</li>
                        <li>تطوير القدرات البدنية</li>
                        <li>تعزيز العمل الجماعي</li>
                        <li>بناء الشخصية الرياضية</li>
                    </ul>
                    <h4>💼 ما يقدمه النادي:</h4>
                    <ul>
                        <li>ملابس التدريب</li>
                        <li>مسابقات دورية</li>
                    </ul>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ===== صفحة المدربون =====
elif page == 'coaches':
    st.markdown("""
    <div class="page-header">
        <div style="width: 90%; max-width: 1200px; margin: 0 auto;">
            <h1>المدربون</h1>
            <p>فريقنا من المدربين المحترفين ذوي الخبرة والكفاءة</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<h2 style="text-align: center;">فريق التدريب المتكامل</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="coach-card">
            <div class="coach-image">👨‍🏫</div>
            <div class="coach-info">
                <h3>كابتن/ميخائيل كميل رؤف</h3>
                <p style="color: #3b82f6;">مدرب معتمد</p>
                <ul style="list-style: none; padding-right: 10px; text-align: right;">
                    <li>• بكالريوس/تربية رياضية</li>
                    <li>• حاصل على الرخصة التدريبية لمراحل البراعم والمعتمدة من الاتحاد الأفريقي لكرة القدم</li>
                    <li>• حاصل على دبلومة الإعداد البدني</li>
                    <li>• حاصل على دبلومة في إصابات الملاعب والعلاج الطبيعي</li>
                    <li>• مدرس تربية رياضية بمدارس السلام الخاصة</li>
                </ul>
            </div>
        </div>
        
        <div class="coach-card">
            <div class="coach-image">🏃</div>
            <div class="coach-info">
                <h3>د. خالد السيد</h3>
                <p style="color: #3b82f6;">مدرب لياقة بدنية</p>
                <p>دكتوراه في علوم الرياضة</p>
                <p style="margin-top: 10px; color: #666;">مختص في تطوير قدرات الناشئين</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="coach-card">
            <div class="coach-image">🧤</div>
            <div class="coach-info">
                <h3>كابتن أحمد علي</h3>
                <p style="color: #3b82f6;">مدرب حراس مرمى</p>
                <p>مدرب معتمد من الاتحاد الأفريقي CAF</p>
                <p style="margin-top: 10px; color: #666;">خبرة 15 عامًا في تدريب الحراس</p>
            </div>
        </div>
        
        <div class="coach-card">
            <div class="coach-image">⚽</div>
            <div class="coach-info">
                <h3>كابتن محمد جابر</h3>
                <p style="color: #3b82f6;">مدرب مهارات فنية</p>
                <p>مدرب مهارات معتمد من الاتحاد الأفريقي CAF</p>
                <p style="margin-top: 10px; color: #666;">خبرة 12 عامًا في المهارات الفنية</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ===== صفحة التسجيل =====
elif page == 'registration':
    st.markdown("""
    <div class="page-header">
        <div style="width: 90%; max-width: 1200px; margin: 0 auto;">
            <h1>تسجيل لاعب جديد</h1>
            <p>انضم إلى الكوتش أكاديمي وابدأ رحلتك نحو الاحتراف</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<h2 style="text-align: center;">نموذج التسجيل</h2>', unsafe_allow_html=True)
    
    if st.session_state.show_success:
        st.markdown('<div class="success-message">✅ تم إرسال طلب التسجيل بنجاح! سنتواصل معكم خلال 24 ساعة.</div>', unsafe_allow_html=True)
        st.session_state.show_success = False
    
    with st.form("registration_form"):
        st.markdown("### معلومات اللاعب")
        
        player_name = st.text_input("اسم اللاعب الثلاثي *")
        age_group = st.selectbox("الفئة العمرية المطلوبة *", 
                                 ["", "بنات", "١ ابتدائي - ٥ ابتدائي", "٦ ابتدائي - ٢ إعدادي"])
        
        st.markdown("### معلومات ولي الأمر")
        
        parent_name = st.text_input("اسم ولي الأمر *")
        parent_phone = st.text_input("رقم الهاتف *", placeholder="01XXXXXXXXX")
        
        notes = st.text_area("ملاحظات إضافية (اختياري)")
        
        submitted = st.form_submit_button("تقديم طلب التسجيل", use_container_width=True)
        
        if submitted:
            if player_name and age_group and parent_name and parent_phone:
                data = {
                    'playerName': player_name,
                    'ageGroup': age_group,
                    'parentName': parent_name,
                    'parentPhone': parent_phone,
                    'notes': notes
                }
                if save_registration(data):
                    st.session_state.show_success = True
                    st.rerun()
                else:
                    st.error("حدث خطأ في حفظ البيانات. يرجى المحاولة مرة أخرى.")
            else:
                st.error("يرجى ملء جميع الحقول المطلوبة")

# ===== صفحة الأسئلة الشائعة =====
elif page == 'faq':
    st.markdown("""
    <div class="page-header">
        <div style="width: 90%; max-width: 1200px; margin: 0 auto;">
            <h1>الأسئلة الشائعة</h1>
            <p>إجابات على أكثر الأسئلة شيوعًا من أولياء الأمور</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<h2 style="text-align: center;">أسئلة متكررة</h2>', unsafe_allow_html=True)
    
    faqs = [
        ("ما الذي يميز الكوتش أكاديمي عن غيرها؟", 
         "الكوتش أكاديمي تتبنى منهجية تدريب متكاملة تركز على: التدريب الذهني وتطوير الذكاء الكروي، متابعة فردية لكل لاعب مع خطة تطوير شخصية، استخدام التكنولوجيا في تحليل الأداء، شراكات مع أندية محلية لدعم الموهوبين."),
        
        ("ما هي مدة التدريب وأوقاته؟", 
         "الموسم التدريبي يمتد لمدة 10 أشهر، من سبتمبر إلى يونيو. التدريبات في الفترة المسائية حسب الجدول المحدد لكل فئة عمرية، بما يتناسب مع أوقات المدارس."),
        
        ("ما هي تكلفة الاشتراك وآلية الدفع؟", 
         "تختلف التكلفة حسب الفئة العمرية وعدد أيام التدريب. نقدم خصومات للأشقاء، نظام تقسيط شهري، ومنح جزئية للمتميزين. يرجى التواصل معنا لمعرفة التفاصيل الدقيقة."),
        
        ("ما هي متطلبات الانضمام للأكاديمية؟", 
         "للانضمام للأكاديمية نحتاج إلى: إكمال نموذج التسجيل عبر الموقع، أن يكون اللاعب في الفئة العمرية المحددة، الرغبة الحقيقية في التعلم والتطوير، الالتزام بمواعيد التدريب."),
        
        ("هل هناك تدريبات خاصة للمبتدئين؟", 
         "نعم، لدينا برامج خاصة للمبتدئين تركز على: تعلم أساسيات كرة القدم، تطوير المهارات الحركية الأساسية، بناء الثقة بالنفس، تعزيز حب الرياضة واللعب الجماعي."),
        
        ("كيف يمكن متابعة تطور اللاعب؟", 
         "نوفر نظام متابعة شامل يشمل: تقييم دوري للمهارات الفنية، متابعة التطور البدني، تقرير عن المشاركة والالتزام، لقاءات دورية مع أولياء الأمور."),
        
        ("ماذا عن السلامة والإصابات خلال التدريب؟", 
         "السلامة أولوية لدينا، ونوفر: إشراف مستمر من مدربين مؤهلين، بيئة تدريب آمنة ومجهزة، برنامج إحماء وتبريد مناسب، مدربين حاصلين على شهادات في الإسعافات الأولية.")
    ]
    
    for i, (question, answer) in enumerate(faqs):
        with st.expander(question):
            st.markdown(answer)

# ===== صفحة اتصل بنا =====
elif page == 'contact':
    st.markdown("""
    <div class="page-header">
        <div style="width: 90%; max-width: 1200px; margin: 0 auto;">
            <h1>اتصل بنا</h1>
            <p>تواصل معنا لأي استفسارات أو معلومات إضافية</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background-color: #f8fafc; padding: 30px; border-radius: 10px;">
            <h3 style="color: #1e3a8a;">معلومات الاتصال</h3>
            <div style="margin: 20px 0; display: flex; align-items: flex-start; gap: 15px;">
                <div style="font-size: 1.2rem; color: #3b82f6;">📞</div>
                <div>
                    <h4>الهاتف</h4>
                    <p><a href="tel:01069238878" class="phone-link">01069238878</a></p>
                </div>
            </div>
            <div style="margin: 20px 0; display: flex; align-items: flex-start; gap: 15px;">
                <div style="font-size: 1.2rem; color: #3b82f6;">💬</div>
                <div>
                    <h4>الواتساب</h4>
                    <p><a href="https://wa.me/201285197778" target="_blank" class="whatsapp-link">01285197778</a></p>
                </div>
            </div>
            <div style="margin: 20px 0; display: flex; align-items: flex-start; gap: 15px;">
                <div style="font-size: 1.2rem; color: #3b82f6;">📍</div>
                <div>
                    <h4>العنوان الرئيسي</h4>
                    <p><a href="https://maps.google.com/?q=مدرسة السلام المتطورة، أسيوط، مصر" target="_blank" class="map-link">أسيوط - مصر</a></p>
                    <p style="color: #666;">على ملاعب مدرسة السلام المتطورة</p>
                </div>
            </div>
            <div style="margin: 20px 0; display: flex; align-items: flex-start; gap: 15px;">
                <div style="font-size: 1.2rem; color: #3b82f6;">⏰</div>
                <div>
                    <h4>أوقات العمل</h4>
                    <p>السبت - الخميس: 4:00 مساءً - 9:00 مساءً</p>
                    <p>الجمعة: إجازة</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background-color: #f8fafc; padding: 30px; border-radius: 10px;">
            <h3 style="color: #1e3a8a;">أرسل رسالة</h3>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("contact_form"):
            contact_name = st.text_input("الاسم")
            contact_phone = st.text_input("رقم الهاتف", placeholder="010XXXXXXXX")
            contact_subject = st.selectbox("الموضوع", ["", "استفسار عام", "معلومات عن البرامج", "التسجيل", "أخرى"])
            contact_message = st.text_area("الرسالة", height=150)
            
            submitted = st.form_submit_button("إرسال الرسالة", use_container_width=True)
            
            if submitted:
                if contact_name and contact_phone and contact_subject and contact_message:
                    data = {
                        'name': contact_name,
                        'phone': contact_phone,
                        'subject': contact_subject,
                        'message': contact_message
                    }
                    if save_contact(data):
                        st.success("شكراً لتواصلك معنا! تم إرسال رسالتك بنجاح وسنرد عليك خلال 24 ساعة.")
                    else:
                        st.error("حدث خطأ في حفظ البيانات. يرجى المحاولة مرة أخرى.")
                else:
                    st.error("يرجى ملء جميع الحقول")

# ===== الفوتر =====
st.markdown("---")
st.markdown("""
<div style="background-color: #1e293b; color: white; padding: 50px 0 20px; border-radius: 10px; margin-top: 50px;">
    <div style="width: 90%; max-width: 1200px; margin: 0 auto;">
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 40px; margin-bottom: 40px;">
            <div>
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 20px;">
                    <div style="width: 50px; height: 50px; background-color: #3b82f6; border-radius: 8px; display: flex; align-items: center; justify-content: center;">
                        ⚽
                    </div>
                    <h3 style="color: white; margin: 0;">الكوتش أكاديمي</h3>
                </div>
                <p style="color: #cbd5e1;">تأسست عام 2020 على ملاعب مدرسة السلام المتطورة. أول أكاديمية في مصر تركز على تطوير اللاعب الشامل من الناحية الفنية والبدنية والنفسية، تحت إشراف مدربين معتمدين من الاتحاد الأفريقي CAF.</p>
            </div>
            <div>
                <h4 style="color: white;">روابط سريعة</h4>
                <ul style="list-style: none; padding: 0;">
                    <li style="margin-bottom: 10px;"><a onclick="navigateTo('home')" style="color: #cbd5e1; text-decoration: none; cursor: pointer;">← الرئيسية</a></li>
                    <li style="margin-bottom: 10px;"><a onclick="navigateTo('about')" style="color: #cbd5e1; text-decoration: none; cursor: pointer;">← من نحن</a></li>
                    <li style="margin-bottom: 10px;"><a onclick="navigateTo('programs')" style="color: #cbd5e1; text-decoration: none; cursor: pointer;">← البرامج التدريبية</a></li>
                    <li style="margin-bottom: 10px;"><a onclick="navigateTo('coaches')" style="color: #cbd5e1; text-decoration: none; cursor: pointer;">← المدربون</a></li>
                    <li style="margin-bottom: 10px;"><a onclick="navigateTo('faq')" style="color: #cbd5e1; text-decoration: none; cursor: pointer;">← الأسئلة الشائعة</a></li>
                </ul>
            </div>
            <div>
                <h4 style="color: white;">معلومات الاتصال</h4>
                <ul style="list-style: none; padding: 0;">
                    <li style="margin-bottom: 15px; display: flex; gap: 10px;">📍 <a href="https://maps.google.com/?q=مدرسة السلام المتطورة، أسيوط، مصر" target="_blank" class="map-link" style="color: #cbd5e1;">مصر، أسيوط - على ملاعب مدرسة السلام المتطورة</a></li>
                    <li style="margin-bottom: 15px; display: flex; gap: 10px;">📞 <a href="tel:01069238878" class="phone-link" style="color: #cbd5e1;">01069238878</a></li>
                    <li style="margin-bottom: 15px; display: flex; gap: 10px;">💬 <a href="https://wa.me/201285197778" target="_blank" class="whatsapp-link">01285197778</a></li>
                    <li style="margin-bottom: 15px; display: flex; gap: 10px;">⏰ السبت - الخميس: 4:00م - 9:00م</li>
                </ul>
            </div>
        </div>
        <div style="text-align: center; padding-top: 20px; border-top: 1px solid rgba(255, 255, 255, 0.1); color: #94a3b8;">
            <p>© 2024 الكوتش أكاديمي. جميع الحقوق محفوظة.</p>
            <p>أكاديمية كرة القدم المتخصصة | صناعة أبطال المستقبل</p>
            <p style="font-size: 0.8rem;">تأسست عام 2020 على يد: كابتن ميخا، كابتن اندرو، كابتن مينا</p>
        </div>
    </div>
</div>

<script>
// إضافة وظيفة navigateTo للنطاق العام
window.navigateTo = function(page) {
    const url = new URL(window.location);
    url.searchParams.set('page', page);
    window.history.pushState({}, '', url);
    window.location.reload();
};
</script>
""", unsafe_allow_html=True)
