import streamlit as st
import json
import os
from datetime import datetime
import hashlib
import random
import base64

# ====================================================================================================
# 1. إعدادات الصفحة الأساسية
# ====================================================================================================
st.set_page_config(
    page_title="الكوتش أكاديمي - أكاديمية كرة القدم المتخصصة",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ====================================================================================================
# 2. إعدادات الجلسة (Session State)
# ====================================================================================================
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'show_success' not in st.session_state:
    st.session_state.show_success = False
if 'show_contact_success' not in st.session_state:
    st.session_state.show_contact_success = False
if 'visitor_count' not in st.session_state:
    st.session_state.visitor_count = random.randint(1000, 5000)
if 'menu_open' not in st.session_state:
    st.session_state.menu_open = False

# ====================================================================================================
# 3. تحويل الصورة إلى Base64 لعرضها
# ====================================================================================================
def get_image_base64(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    except:
        return None

logo_base64 = get_image_base64("logo.jpg")

# ====================================================================================================
# 4. CSS الرئيسي والأنماط الكاملة
# ====================================================================================================
st.markdown("""
<style>
    /* ---------------------------------------------------------------------------------------------- */
    /* إخفاء عناصر Streamlit الافتراضية */
    /* ---------------------------------------------------------------------------------------------- */
    header[data-testid="stHeader"] { display: none !important; }
    .stApp > header { display: none !important; }
    .st-emotion-cache-18ni7ap { display: none !important; }
    .st-emotion-cache-1v0mbdj { display: none !important; }
    #MainMenu { display: none !important; }
    footer { display: none !important; }
    
    /* ---------------------------------------------------------------------------------------------- */
    /* إزالة المسافات الداخلية */
    /* ---------------------------------------------------------------------------------------------- */
    .main .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        padding-left: 0rem !important;
        padding-right: 0rem !important;
        max-width: 100% !important;
    }
    
    /* ---------------------------------------------------------------------------------------------- */
    /* الخلفية العامة */
    /* ---------------------------------------------------------------------------------------------- */
    .stApp { background: linear-gradient(135deg, #f0f2f6 0%, #ffffff 100%) !important; }
    
    /* ---------------------------------------------------------------------------------------------- */
    /* تنسيق عام للخطوط */
    /* ---------------------------------------------------------------------------------------------- */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
        font-family: 'Cairo', 'Tajawal', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* ---------------------------------------------------------------------------------------------- */
    /* تنسيق الهيدر العلوي المخصص */
    /* ---------------------------------------------------------------------------------------------- */
    .custom-top-header {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
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
    
    /* ---------------------------------------------------------------------------------------------- */
    /* تنسيق اللوجو */
    /* ---------------------------------------------------------------------------------------------- */
    .custom-logo-wrapper {
        display: flex;
        align-items: center;
        gap: 15px;
        cursor: pointer;
    }
    
    .custom-logo-image {
        width: 60px;
        height: 60px;
        border-radius: 18px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
        overflow: hidden;
    }
    
    .custom-logo-image img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
    
    .custom-logo-image:hover {
        transform: scale(1.08) rotate(5deg);
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
    }
    
    .custom-logo-text h1 {
        font-size: 1.8rem;
        margin: 0;
        color: #1e3a8a;
        font-weight: 800;
        letter-spacing: -0.5px;
    }
    
    .custom-logo-text span { color: #f59e0b; }
    .custom-logo-text p {
        font-size: 0.75rem;
        color: #64748b;
        margin: 0;
        font-weight: 500;
    }
    
    /* ---------------------------------------------------------------------------------------------- */
    /* زر البرجر منيو (Burger Menu) */
    /* ---------------------------------------------------------------------------------------------- */
    .custom-burger-menu-btn {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        width: 40px;
        height: 28px;
        background: transparent;
        border: none;
        cursor: pointer;
        padding: 0;
        z-index: 10002;
        transition: all 0.3s ease;
    }
    
    .custom-burger-menu-btn span {
        display: block;
        width: 100%;
        height: 3px;
        background: linear-gradient(90deg, #1e3a8a, #3b82f6);
        border-radius: 4px;
        transition: all 0.3s ease;
    }
    
    .custom-burger-menu-btn.active span:nth-child(1) {
        transform: rotate(45deg) translate(10px, 10px);
        background: #f59e0b;
    }
    
    .custom-burger-menu-btn.active span:nth-child(2) {
        opacity: 0;
        transform: translateX(-20px);
    }
    
    .custom-burger-menu-btn.active span:nth-child(3) {
        transform: rotate(-45deg) translate(10px, -10px);
        background: #f59e0b;
    }
    
    /* ---------------------------------------------------------------------------------------------- */
    /* القائمة الجانبية (Side Navigation) */
    /* ---------------------------------------------------------------------------------------------- */
    .custom-side-navigation {
        position: fixed;
        top: 0;
        right: -380px;
        width: 340px;
        height: 100vh;
        background: linear-gradient(180deg, #ffffff 0%, #f1f5f9 100%);
        box-shadow: -10px 0 40px rgba(0, 0, 0, 0.2);
        z-index: 10001;
        transition: right 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        padding-top: 100px;
        overflow-y: auto;
    }
    
    .custom-side-navigation.open { right: 0; }
    
    .custom-side-navigation ul { list-style: none; padding: 0 20px; }
    
    .custom-side-navigation li {
        margin-bottom: 10px;
        opacity: 0;
        transform: translateX(40px);
        transition: all 0.4s ease;
    }
    
    .custom-side-navigation.open li {
        opacity: 1;
        transform: translateX(0);
    }
    
    .custom-side-navigation.open li:nth-child(1) { transition-delay: 0.05s; }
    .custom-side-navigation.open li:nth-child(2) { transition-delay: 0.1s; }
    .custom-side-navigation.open li:nth-child(3) { transition-delay: 0.15s; }
    .custom-side-navigation.open li:nth-child(4) { transition-delay: 0.2s; }
    .custom-side-navigation.open li:nth-child(5) { transition-delay: 0.25s; }
    .custom-side-navigation.open li:nth-child(6) { transition-delay: 0.3s; }
    .custom-side-navigation.open li:nth-child(7) { transition-delay: 0.35s; }
    .custom-side-navigation.open li:nth-child(8) { transition-delay: 0.4s; }
    .custom-side-navigation.open li:nth-child(9) { transition-delay: 0.45s; }
    
    .custom-side-navigation a {
        display: flex;
        align-items: center;
        gap: 18px;
        padding: 15px 22px;
        color: #1e293b;
        text-decoration: none;
        font-weight: 600;
        border-radius: 16px;
        transition: all 0.3s ease;
        cursor: pointer;
        font-size: 16px;
    }
    
    .custom-side-navigation a:hover {
        background: linear-gradient(135deg, #eff6ff, #dbeafe);
        color: #3b82f6;
        transform: translateX(-8px);
    }
    
    /* ---------------------------------------------------------------------------------------------- */
    /* طبقة التعتيم (Overlay) */
    /* ---------------------------------------------------------------------------------------------- */
    .custom-nav-overlay-layer {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-color: rgba(0, 0, 0, 0.6);
        z-index: 10000;
        display: none;
        backdrop-filter: blur(4px);
    }
    
    .custom-nav-overlay-layer.show { display: block; }
    
    /* ---------------------------------------------------------------------------------------------- */
    /* مساحة تعويضية للهيدر */
    /* ---------------------------------------------------------------------------------------------- */
    .custom-header-spacer { height: 90px; }
    
    /* ---------------------------------------------------------------------------------------------- */
    /* حاوية المحتوى الرئيسية */
    /* ---------------------------------------------------------------------------------------------- */
    .custom-content-container {
        width: 90%;
        max-width: 1200px;
        margin: 0 auto;
        padding: 25px 15px;
    }
    
    /* ---------------------------------------------------------------------------------------------- */
    /* القسم الرئيسي (Hero Section) */
    /* ---------------------------------------------------------------------------------------------- */
    .custom-hero-section {
        background: linear-gradient(135deg, rgba(0,0,0,0.8), rgba(0,0,0,0.65)), url('https://images.unsplash.com/photo-1575361204480-aadea25e6e68?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80');
        background-size: cover;
        background-position: center;
        border-radius: 28px;
        padding: 90px 25px;
        text-align: center;
        margin-bottom: 55px;
        position: relative;
        overflow: hidden;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
    }
    
    .custom-hero-section h1 {
        color: white;
        font-size: 3.2rem;
        margin-bottom: 20px;
        font-weight: 800;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.4);
        position: relative;
        z-index: 1;
    }
    
    .custom-hero-section p {
        color: #e2e8f0;
        max-width: 750px;
        margin: 0 auto;
        font-size: 1.15rem;
        position: relative;
        z-index: 1;
    }
    
    /* ---------------------------------------------------------------------------------------------- */
    /* عناوين الأقسام */
    /* ---------------------------------------------------------------------------------------------- */
    .custom-section-title {
        font-size: 2.3rem;
        font-weight: 800;
        color: #1e293b;
        text-align: center;
        margin-bottom: 45px;
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
    
    /* ---------------------------------------------------------------------------------------------- */
    /* بطاقات الإحصائيات */
    /* ---------------------------------------------------------------------------------------------- */
    .custom-stats-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 30px;
        margin-bottom: 65px;
    }
    
    .custom-stat-card {
        background: white;
        padding: 40px 25px;
        border-radius: 24px;
        text-align: center;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
        border: 1px solid #e2e8f0;
    }
    
    .custom-stat-card:hover {
        transform: translateY(-12px);
        box-shadow: 0 25px 45px rgba(0, 0, 0, 0.15);
        border-color: #3b82f6;
    }
    
    .custom-stat-number {
        font-size: 3.2rem;
        font-weight: 800;
        color: #1e3a8a;
        display: block;
    }
    
    .custom-stat-label {
        color: #64748b;
        margin-top: 12px;
        font-weight: 600;
        font-size: 1.05rem;
    }
    
    /* ---------------------------------------------------------------------------------------------- */
    /* بطاقات المميزات */
    /* ---------------------------------------------------------------------------------------------- */
    .custom-features-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 30px;
        margin-bottom: 65px;
    }
    
    .custom-feature-card {
        background: white;
        padding: 40px 28px;
        border-radius: 24px;
        text-align: center;
        transition: all 0.3s ease;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
    }
    
    .custom-feature-card:hover {
        transform: translateY(-12px);
        box-shadow: 0 25px 45px rgba(0, 0, 0, 0.15);
    }
    
    .custom-feature-icon { font-size: 3.2rem; margin-bottom: 22px; }
    .custom-feature-card h3 {
        color: #1e3a8a;
        margin-bottom: 18px;
        font-size: 1.4rem;
        font-weight: 700;
    }
    .custom-feature-card p {
        color: #64748b;
        font-size: 0.95rem;
        line-height: 1.65;
    }
    
    /* ---------------------------------------------------------------------------------------------- */
    /* زر التسجيل المخصص */
    /* ---------------------------------------------------------------------------------------------- */
    .custom-register-btn {
        background: linear-gradient(135deg, #f59e0b, #d97706, #f59e0b);
        background-size: 200% 200%;
        color: white;
        padding: 18px 55px;
        border-radius: 60px;
        font-weight: 800;
        font-size: 1.25rem;
        border: none;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
        animation: btnGradient 3s ease infinite;
    }
    
    @keyframes btnGradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .custom-register-btn:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.25);
    }
    
    /* ---------------------------------------------------------------------------------------------- */
    /* بطاقات البرامج التدريبية */
    /* ---------------------------------------------------------------------------------------------- */
    .custom-programs-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 30px;
        margin-bottom: 65px;
    }
    
    .custom-program-card {
        background: white;
        border-radius: 24px;
        overflow: hidden;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
        border: 1px solid #e2e8f0;
    }
    
    .custom-program-card:hover {
        transform: translateY(-12px);
        box-shadow: 0 25px 45px rgba(0, 0, 0, 0.15);
    }
    
    .custom-program-header {
        height: 170px;
        background: linear-gradient(135deg, #3b82f6, #1e3a8a, #3b82f6);
        background-size: 200% 200%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 3.8rem;
        color: white;
        animation: headerGradient 4s ease infinite;
    }
    
    @keyframes headerGradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .custom-program-body { padding: 28px; }
    .custom-program-body h3 {
        color: #1e3a8a;
        margin-bottom: 18px;
        font-size: 1.5rem;
        font-weight: 700;
    }
    
    .custom-schedule-box {
        background: #f8fafc;
        padding: 20px;
        border-radius: 18px;
    }
    
    .custom-schedule-item {
        padding: 12px 0;
        border-bottom: 1px solid #e2e8f0;
        color: #334155;
        font-size: 1rem;
    }
    
    /* ---------------------------------------------------------------------------------------------- */
    /* بطاقات المدربين */
    /* ---------------------------------------------------------------------------------------------- */
    .custom-coaches-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 30px;
        margin-bottom: 65px;
    }
    
    .custom-coach-card {
        background: white;
        border-radius: 24px;
        overflow: hidden;
        text-align: center;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
        border: 1px solid #e2e8f0;
    }
    
    .custom-coach-card:hover {
        transform: translateY(-12px);
        box-shadow: 0 25px 45px rgba(0, 0, 0, 0.15);
    }
    
    .custom-coach-avatar {
        height: 220px;
        background: linear-gradient(135deg, #3b82f6, #1e3a8a, #3b82f6);
        background-size: 200% 200%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 4.5rem;
        color: white;
        animation: avatarGradient 4s ease infinite;
    }
    
    @keyframes avatarGradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .custom-coach-info { padding: 28px; }
    .custom-coach-info h3 {
        color: #1e3a8a;
        margin-bottom: 10px;
        font-size: 1.35rem;
        font-weight: 700;
    }
    .custom-coach-title {
        color: #3b82f6;
        font-weight: 600;
        margin-bottom: 15px;
    }
    .custom-coach-desc {
        color: #64748b;
        font-size: 0.9rem;
        line-height: 1.6;
        margin-top: 10px;
    }
    
    /* ---------------------------------------------------------------------------------------------- */
    /* صفحة من نحن */
    /* ---------------------------------------------------------------------------------------------- */
    .custom-about-wrapper {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 45px;
        margin-bottom: 55px;
        align-items: center;
    }
    
    .custom-about-image {
        background: linear-gradient(135deg, #3b82f6, #1e3a8a, #3b82f6);
        background-size: 200% 200%;
        border-radius: 28px;
        height: 380px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 6.5rem;
        color: white;
        animation: aboutGradient 4s ease infinite;
    }
    
    @keyframes aboutGradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .custom-mission-vision-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 35px;
        margin-top: 35px;
    }
    
    .custom-mission-card, .custom-vision-card {
        padding: 35px;
        border-radius: 24px;
        transition: all 0.3s ease;
    }
    
    .custom-mission-card {
        background: linear-gradient(135deg, #f0f9ff, #e0f2fe);
        border-right: 6px solid #3b82f6;
    }
    
    .custom-vision-card {
        background: linear-gradient(135deg, #fef3c7, #fde68a);
        border-right: 6px solid #f59e0b;
    }
    
    .custom-mission-card:hover, .custom-vision-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
    }
    
    /* ---------------------------------------------------------------------------------------------- */
    /* نموذج التسجيل */
    /* ---------------------------------------------------------------------------------------------- */
    .custom-success-message {
        background: linear-gradient(135deg, #10b981, #059669);
        color: white;
        padding: 18px;
        border-radius: 16px;
        margin-bottom: 25px;
        text-align: center;
        font-weight: 600;
        animation: fadeIn 0.5s ease;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* ---------------------------------------------------------------------------------------------- */
    /* صفحة الاتصال */
    /* ---------------------------------------------------------------------------------------------- */
    .custom-contact-wrapper {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 35px;
    }
    
    .custom-contact-card {
        background: white;
        padding: 35px;
        border-radius: 24px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
    }
    
    .custom-contact-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.12);
    }
    
    .custom-contact-item {
        display: flex;
        align-items: center;
        gap: 18px;
        padding: 18px 0;
        border-bottom: 1px solid #e2e8f0;
    }
    
    .custom-contact-item:last-child { border-bottom: none; }
    
    /* ---------------------------------------------------------------------------------------------- */
    /* خريطة Google Maps */
    /* ---------------------------------------------------------------------------------------------- */
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
    
    /* ---------------------------------------------------------------------------------------------- */
    /* تنسيقات الصفحات العامة */
    /* ---------------------------------------------------------------------------------------------- */
    .custom-page-header {
        background: linear-gradient(135deg, #1e3a8a, #3b82f6, #1e3a8a);
        background-size: 200% 200%;
        border-radius: 28px;
        padding: 60px 25px;
        text-align: center;
        margin-bottom: 50px;
        animation: pageHeaderGradient 4s ease infinite;
    }
    
    @keyframes pageHeaderGradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .custom-page-header h1 {
        color: white;
        font-size: 2.5rem;
        margin-bottom: 15px;
    }
    
    .custom-page-header p {
        color: #e2e8f0;
        font-size: 1.05rem;
    }
    
    /* ---------------------------------------------------------------------------------------------- */
    /* الفوتر (Footer) */
    /* ---------------------------------------------------------------------------------------------- */
    .custom-main-footer {
        background: linear-gradient(135deg, #1e293b, #0f172a, #1e293b);
        background-size: 200% 200%;
        color: white;
        padding: 50px 0 30px;
        border-radius: 30px 30px 0 0;
        margin-top: 70px;
        animation: footerGradient 6s ease infinite;
    }
    
    @keyframes footerGradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .custom-footer-grid {
        width: 90%;
        max-width: 1200px;
        margin: 0 auto;
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 40px;
        margin-bottom: 40px;
    }
    
    .custom-footer-link {
        color: #cbd5e1;
        text-decoration: none;
        transition: all 0.3s ease;
        cursor: pointer;
        display: inline-block;
    }
    
    .custom-footer-link:hover {
        color: #f59e0b;
        transform: translateX(-6px);
    }
    
    /* ---------------------------------------------------------------------------------------------- */
    /* تنسيقات للشاشات الصغيرة */
    /* ---------------------------------------------------------------------------------------------- */
    @media (max-width: 768px) {
        .custom-stats-grid, .custom-features-grid, .custom-programs-grid, 
        .custom-coaches-grid, .custom-contact-wrapper, .custom-about-wrapper, 
        .custom-mission-vision-grid {
            grid-template-columns: 1fr;
        }
        .custom-hero-section h1 { font-size: 2rem; }
        .custom-section-title { font-size: 1.6rem; }
        .custom-stat-number { font-size: 2.2rem; }
        .custom-logo-text h1 { font-size: 1.2rem; }
        .custom-logo-image { width: 45px; height: 45px; }
        .custom-header-spacer { height: 80px; }
        .custom-side-navigation { width: 280px; right: -280px; }
        .custom-register-btn { padding: 14px 35px; font-size: 1rem; }
        .custom-hero-section { padding: 60px 20px; }
    }
</style>
""", unsafe_allow_html=True)

# ====================================================================================================
# 5. إضافة الهيدر والقائمة الجانبية (HTML + JavaScript)
# ====================================================================================================

# بناء HTML للوجو مع الصورة أو الإيموجي كبديل
logo_html = ""
if logo_base64:
    logo_html = f'<img src="data:image/jpeg;base64,{logo_base64}" alt="Logo">'
else:
    logo_html = '<span>⚽</span>'

st.markdown(f"""
<div id="custom-header-root">
    <div class="custom-top-header">
        <div class="custom-header-container">
            <div class="custom-logo-wrapper" id="logoClickArea">
                <div class="custom-logo-image">
                    {logo_html}
                </div>
                <div class="custom-logo-text">
                    <h1>الكوتش <span>أكاديمي</span></h1>
                    <p>أكاديمية كرة القدم المتخصصة</p>
                </div>
            </div>
            <button class="custom-burger-menu-btn" id="burgerBtn">
                <span></span>
                <span></span>
                <span></span>
            </button>
        </div>
    </div>
    <div class="custom-side-navigation" id="sideMenu">
        <ul>
            <li><a href="#" data-page="home" class="nav-link">🏠 الرئيسية</a></li>
            <li><a href="#" data-page="about" class="nav-link">ℹ️ من نحن</a></li>
            <li><a href="#" data-page="programs" class="nav-link">⚽ البرامج التدريبية</a></li>
            <li><a href="#" data-page="coaches" class="nav-link">👨‍🏫 المدربون</a></li>
            <li><a href="#" data-page="registration" class="nav-link">📝 تسجيل لاعب جديد</a></li>
            <li><a href="#" data-page="faq" class="nav-link">❓ الأسئلة الشائعة</a></li>
            <li><a href="#" data-page="contact" class="nav-link">📞 اتصل بنا</a></li>
            <li><a href="#" data-page="gallery" class="nav-link">📸 معرض الصور</a></li>
            <li><a href="#" data-page="news" class="nav-link">📰 الأخبار</a></li>
        </ul>
    </div>
    <div class="custom-nav-overlay-layer" id="overlayLayer"></div>
    <div class="custom-header-spacer"></div>
</div>

<script>
(function() {{
    // وظيفة التنقل بين الصفحات
    function navigateToPage(pageName) {{
        const url = new URL(window.location);
        url.searchParams.set('page', pageName);
        window.location.href = url.toString();
    }}
    
    // جعل الدالة عامة
    window.customNavigateToPage = navigateToPage;
    
    // تهيئة القائمة بعد تحميل الصفحة
    function initMenu() {{
        const burgerBtn = document.getElementById('burgerBtn');
        const sideMenu = document.getElementById('sideMenu');
        const overlayLayer = document.getElementById('overlayLayer');
        const logoArea = document.getElementById('logoClickArea');
        
        console.log("Menu initialized", burgerBtn, sideMenu);
        
        if (burgerBtn) {{
            burgerBtn.addEventListener('click', function(e) {{
                e.preventDefault();
                e.stopPropagation();
                console.log("Burger clicked");
                this.classList.toggle('active');
                if (sideMenu) sideMenu.classList.toggle('open');
                if (overlayLayer) overlayLayer.classList.toggle('show');
                if (sideMenu && sideMenu.classList.contains('open')) {{
                    document.body.style.overflow = 'hidden';
                }} else {{
                    document.body.style.overflow = '';
                }}
            }});
        }}
        
        if (overlayLayer) {{
            overlayLayer.addEventListener('click', function() {{
                this.classList.remove('show');
                if (sideMenu) sideMenu.classList.remove('open');
                if (burgerBtn) burgerBtn.classList.remove('active');
                document.body.style.overflow = '';
            }});
        }}
        
        if (logoArea) {{
            logoArea.addEventListener('click', function() {{
                navigateToPage('home');
            }});
        }}
        
        // ربط روابط القائمة
        document.querySelectorAll('.nav-link').forEach(link => {{
            link.addEventListener('click', function(e) {{
                e.preventDefault();
                const pageName = this.getAttribute('data-page');
                if (pageName) navigateToPage(pageName);
            }});
        }});
        
        // إغلاق القائمة عند الضغط على Escape
        document.addEventListener('keydown', function(e) {{
            if (e.key === 'Escape') {{
                if (overlayLayer) overlayLayer.classList.remove('show');
                if (sideMenu) sideMenu.classList.remove('open');
                if (burgerBtn) burgerBtn.classList.remove('active');
                document.body.style.overflow = '';
            }}
        }});
    }}
    
    if (document.readyState === 'loading') {{
        document.addEventListener('DOMContentLoaded', initMenu);
    }} else {{
        initMenu();
    }}
}})();
</script>
""", unsafe_allow_html=True)

# ====================================================================================================
# 6. دوال حفظ البيانات (Save to JSON files)
# ====================================================================================================
DATA_FILE = 'registrations.json'
CONTACT_FILE = 'contacts.json'

def save_registration(data):
    try:
        registrations = []
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                registrations = json.load(f)
        data['timestamp'] = datetime.now().isoformat()
        data['id'] = hashlib.md5(f"{data['playerName']}{data['timestamp']}".encode()).hexdigest()[:8]
        registrations.append(data)
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(registrations, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Error saving registration: {e}")
        return False

def save_contact(data):
    try:
        contacts = []
        if os.path.exists(CONTACT_FILE):
            with open(CONTACT_FILE, 'r', encoding='utf-8') as f:
                contacts = json.load(f)
        data['timestamp'] = datetime.now().isoformat()
        data['id'] = hashlib.md5(f"{data['name']}{data['timestamp']}".encode()).hexdigest()[:8]
        contacts.append(data)
        with open(CONTACT_FILE, 'w', encoding='utf-8') as f:
            json.dump(contacts, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Error saving contact: {e}")
        return False

# ====================================================================================================
# 7. تحديد الصفحة الحالية من Query Parameters
# ====================================================================================================
query_params = st.query_params
if 'page' in query_params:
    st.session_state.page = query_params['page']

page = st.session_state.page

# بداية حاوية المحتوى الرئيسية
st.markdown('<div class="custom-content-container">', unsafe_allow_html=True)

# ====================================================================================================
# 8. الصفحة الرئيسية (Home Page)
# ====================================================================================================
if page == 'home':
    st.markdown("""
    <div class="custom-hero-section">
        <h1>⚽ الكوتش أكاديمي</h1>
        <p>أول أكاديمية متخصصة في مصر تركز على بناء اللاعب الشامل من الناحية الفنية والبدنية والنفسية، تحت إشراف مدربين معتمدين دوليًا.</p>
        <p style="font-weight: 700; margin-top: 22px; color: #fbbf24; font-size: 1.2rem;">نحن لا نصنع لاعبين فقط.. نحن نصنع قادة!</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 55px;">
            <button class="custom-register-btn" onclick="customNavigateToPage('registration')">📝 سجل ابنك الآن</button>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="custom-section-title">إنجازات الأكاديمية</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="custom-stats-grid">
        <div class="custom-stat-card"><div style="font-size: 3.2rem;">👥</div><span class="custom-stat-number">500+</span><div class="custom-stat-label">لاعب مدرب</div></div>
        <div class="custom-stat-card"><div style="font-size: 3.2rem;">👨‍🏫</div><span class="custom-stat-number">12</span><div class="custom-stat-label">مدرب محترف</div></div>
        <div class="custom-stat-card"><div style="font-size: 3.2rem;">🏆</div><span class="custom-stat-number">150+</span><div class="custom-stat-label">لاعب محترف</div></div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="custom-section-title">لماذا تختار الكوتش أكاديمي؟</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="custom-features-grid">
        <div class="custom-feature-card"><div class="custom-feature-icon">🧠</div><h3>منهجية التدريب الذهني</h3><p>نركز على تطوير الذكاء الكروي والقدرة على اتخاذ القرارات السريعة والصحيحة داخل الملعب.</p></div>
        <div class="custom-feature-card"><div class="custom-feature-icon">🛡️</div><h3>بيئة آمنة محفزة</h3><p>نوفر بيئة تدريب آمنة تحترم الفروق الفردية وتشجع على الإبداع والتميز.</p></div>
        <div class="custom-feature-card"><div class="custom-feature-icon">🤝</div><h3>شراكات مع الأندية</h3><p>لدينا شراكات مع أندية محلية ودولية لتمكين الموهوبين من الانضمام للمنتخبات والأندية الكبرى.</p></div>
    </div>
    """, unsafe_allow_html=True)

# ====================================================================================================
# 9. صفحة من نحن (About Page)
# ====================================================================================================
elif page == 'about':
    st.markdown("""
    <div class="custom-page-header">
        <h1>من نحن</h1>
        <p>الكوتش أكاديمي.. رؤية جديدة في عالم تدريب كرة القدم</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="custom-about-wrapper">
        <div class="custom-about-image">⚽</div>
        <div>
            <h2 style="color: #1e3a8a; font-size: 1.9rem; margin-bottom: 22px;">تأسيس الأكاديمية</h2>
            <p style="color: #334155; font-size: 1rem; line-height: 1.7;">تأسست الأكاديمية عام 2020 على يد نخبة من المدربين المتخصصين:</p>
            <ul style="margin-right: 25px; margin-top: 18px; color: #334155;">
                <li>كابتن ميخائيل كميل رؤف (ميخا) - المدير الفني</li>
                <li>كابتن اندرو - مدرب مهارات</li>
                <li>كابتن مينا - مدرب لياقة بدنية</li>
            </ul>
            <p style="margin-top: 22px; color: #334155;">على ملاعب مدرسة السلام المتطورة - أسيوط</p>
            <p style="margin-top: 18px; font-weight: 700; color: #1e3a8a;">بدعم من الأب الروحي للأكاديمية: مستر / مؤنس منير</p>
        </div>
    </div>
    <div class="custom-mission-vision-grid">
        <div class="custom-mission-card"><h3 style="color: #1e3a8a;">🎯 رسالتنا</h3><p>تطوير جيل جديد من اللاعبين المبدعين القادرين على التألق محليًا ودوليًا، من خلال تقديم تدريب عصري يعتمد على أحدث الأساليب العلمية.</p></div>
        <div class="custom-vision-card"><h3 style="color: #1e3a8a;">👁️ رؤيتنا</h3><p>أن نكون الوجهة الأولى لأي موهبة كروية في مصر والوطن العربي، والجسر الذي يعبر من خلاله اللاعبون الموهوبون إلى العالمية.</p></div>
    </div>
    """, unsafe_allow_html=True)

# ====================================================================================================
# 10. صفحة البرامج التدريبية (Programs Page)
# ====================================================================================================
elif page == 'programs':
    st.markdown("""
    <div class="custom-page-header">
        <h1>البرامج التدريبية</h1>
        <p>مواعيد تدريبية مصممة لكل فئة عمرية وجنسية</p>
    </div>
    <div class="custom-programs-grid">
        <div class="custom-program-card"><div class="custom-program-header">📅 السبت</div><div class="custom-program-body"><h3>مواعيد تدريب السبت</h3><div class="custom-schedule-box"><div class="custom-schedule-item">🕔 ٥:٠٠ - ٦:٠٠ م → 🏃‍♀️ بنات (جميع الأعمار)</div><div class="custom-schedule-item">🕕 ٦:٠٠ - ٧:٣٠ م → 🏃 بنين (الصف الأول - الخامس الابتدائي)</div><div class="custom-schedule-item">🕢 ٧:٣٠ - ٩:٠٠ م → 🏃 بنين (الصف السادس الابتدائي - الثاني الإعدادي)</div></div></div></div>
        <div class="custom-program-card"><div class="custom-program-header">✅ الخميس</div><div class="custom-program-body"><h3>مواعيد تدريب الخميس</h3><div class="custom-schedule-box"><div class="custom-schedule-item">🕟 ٤:٣٠ - ٦:٠٠ م → 🏃‍♀️ بنات (جميع الأعمار)</div><div class="custom-schedule-item">🕕 ٦:٠٠ - ٨:٠٠ م → 🏃 بنين (الصف الأول - الخامس الابتدائي)</div><div class="custom-schedule-item">🕗 ٨:٠٠ - ١٠:٠٠ م → 🏃 بنين (الصف السادس الابتدائي - الثاني الإعدادي)</div></div></div></div>
    </div>
    """, unsafe_allow_html=True)

# ====================================================================================================
# 11. صفحة المدربون (Coaches Page)
# ====================================================================================================
elif page == 'coaches':
    st.markdown("""
    <div class="custom-page-header">
        <h1>المدربون</h1>
        <p>فريقنا من المدربين المحترفين ذوي الخبرة والكفاءة</p>
    </div>
    <div class="custom-coaches-grid">
        <div class="custom-coach-card"><div class="custom-coach-avatar">👨‍🏫</div><div class="custom-coach-info"><h3>كابتن/ميخائيل كميل رؤف</h3><div class="custom-coach-title">المدير الفني - مدرب معتمد (CAF)</div><div class="custom-coach-desc">🎓 بكالريوس تربية رياضية<br>📜 رخصة تدريب CAF لمراحل البراعم</div></div></div>
        <div class="custom-coach-card"><div class="custom-coach-avatar">🧤</div><div class="custom-coach-info"><h3>كابتن أحمد علي</h3><div class="custom-coach-title">مدرب حراس مرمى - معتمد (CAF)</div><div class="custom-coach-desc">🎓 بكالريوس تربية رياضية<br>📜 رخصة تدريب حراس مرمى CAF</div></div></div>
        <div class="custom-coach-card"><div class="custom-coach-avatar">🏃</div><div class="custom-coach-info"><h3>د. خالد السيد</h3><div class="custom-coach-title">مدرب لياقة بدنية - دكتوراه</div><div class="custom-coach-desc">🎓 دكتوراه في علوم الرياضة<br>📜 مدرب لياقة معتمد من الاتحاد المصري</div></div></div>
        <div class="custom-coach-card"><div class="custom-coach-avatar">⚽</div><div class="custom-coach-info"><h3>كابتن محمد جابر</h3><div class="custom-coach-title">مدرب مهارات فنية - معتمد (CAF)</div><div class="custom-coach-desc">🎓 بكالريوس تربية رياضية<br>📜 رخصة تدريب مهارات CAF</div></div></div>
    </div>
    """, unsafe_allow_html=True)

# ====================================================================================================
# 12. صفحة التسجيل (Registration Page)
# ====================================================================================================
elif page == 'registration':
    st.markdown("""
    <div class="custom-page-header">
        <h1>تسجيل لاعب جديد</h1>
        <p>انضم إلى الكوتش أكاديمي وابدأ رحلتك نحو الاحتراف</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.show_success:
        st.markdown('<div class="custom-success-message">✅ تم إرسال طلب التسجيل بنجاح! سنتواصل معكم خلال 24 ساعة.</div>', unsafe_allow_html=True)
        st.session_state.show_success = False
    
    with st.form("registration_form"):
        st.markdown("### 📋 معلومات اللاعب")
        player_name = st.text_input("اسم اللاعب الثلاثي *")
        age_group = st.selectbox("الفئة العمرية المطلوبة *", ["", "🏃‍♀️ بنات (جميع الأعمار)", "🏃 بنين (الصف الأول - الخامس الابتدائي)", "🏃 بنين (الصف السادس الابتدائي - الثاني الإعدادي)"])
        birth_date = st.date_input("تاريخ الميلاد", None)
        previous_club = st.text_input("النادي السابق (إن وجد)")
        
        st.markdown("### 👨‍👩‍👦 معلومات ولي الأمر")
        parent_name = st.text_input("اسم ولي الأمر *")
        parent_phone = st.text_input("رقم الهاتف *")
        parent_whatsapp = st.text_input("رقم الواتساب (للتواصل السريع)")
        
        st.markdown("### 📍 معلومات إضافية")
        address = st.text_area("العنوان بالكامل", height=70)
        medical_notes = st.text_area("ملاحظات طبية (إن وجدت)", height=60)
        notes = st.text_area("ملاحظات إضافية (اختياري)", height=70)
        
        submitted = st.form_submit_button("📝 تقديم طلب التسجيل", use_container_width=True)
        
        if submitted:
            if player_name and age_group and parent_name and parent_phone:
                data = {
                    'playerName': player_name, 'ageGroup': age_group,
                    'birthDate': str(birth_date) if birth_date else "",
                    'previousClub': previous_club, 'parentName': parent_name,
                    'parentPhone': parent_phone, 'parentWhatsapp': parent_whatsapp,
                    'address': address, 'medicalNotes': medical_notes, 'notes': notes,
                    'registrationDate': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                if save_registration(data):
                    st.session_state.show_success = True
                    st.rerun()
                else:
                    st.error("❌ حدث خطأ في حفظ البيانات")
            else:
                st.error("⚠️ يرجى ملء جميع الحقول المطلوبة")

# ====================================================================================================
# 13. صفحة الأسئلة الشائعة (FAQ Page)
# ====================================================================================================
elif page == 'faq':
    st.markdown("""
    <div class="custom-page-header">
        <h1>الأسئلة الشائعة</h1>
        <p>إجابات على أكثر الأسئلة شيوعًا من أولياء الأمور</p>
    </div>
    """, unsafe_allow_html=True)
    
    faqs = [
        ("ما الذي يميز الكوتش أكاديمي؟", "الكوتش أكاديمي تتبنى منهجية تدريب متكاملة تركز على التدريب الذهني وتطوير الذكاء الكروي."),
        ("ما هي مدة التدريب وأوقاته؟", "الموسم التدريبي 10 أشهر. التدريبات أيام السبت والخميس حسب الجدول المحدد."),
        ("ما هي متطلبات الانضمام؟", "إكمال نموذج التسجيل، أن يكون اللاعب في الفئة العمرية المحددة، الالتزام بمواعيد التدريب."),
        ("كيف يمكن متابعة تطور اللاعب؟", "نوفر تقييم فني دوري، تقارير شهرية، لقاءات دورية مع أولياء الأمور."),
        ("كيف يمكن التواصل مع الإدارة؟", "الاتصال 01069238878، واتساب 01285197778، أو زيارة الأكاديمية."),
        ("ما هي تكلفة الاشتراك؟", "تختلف حسب الفئة العمرية. يوجد خصومات للأشقاء ونظام تقسيط."),
        ("هل يوجد تدريبات للبنات؟", "نعم، لدينا برامج مخصصة للبنات مع مدربات متخصصات."),
    ]
    
    for q, a in faqs:
        with st.expander(f"❓ {q}"):
            st.markdown(f'<p style="color: #334155;">{a}</p>', unsafe_allow_html=True)

# ====================================================================================================
# 14. صفحة اتصل بنا (Contact Page)
# ====================================================================================================
elif page == 'contact':
    st.markdown("""
    <div class="custom-page-header">
        <h1>اتصل بنا</h1>
        <p>تواصل معنا لأي استفسارات أو معلومات إضافية</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="custom-contact-card">
            <h3 style="color: #1e3a8a;">📞 معلومات الاتصال</h3>
            <div class="custom-contact-item"><div>📱</div><div><strong>الهاتف:</strong><br><a href="tel:01069238878">01069238878</a></div></div>
            <div class="custom-contact-item"><div>💬</div><div><strong>الواتساب:</strong><br><a href="https://wa.me/201285197778">01285197778</a></div></div>
            <div class="custom-contact-item"><div>📍</div><div><strong>العنوان:</strong><br>أسيوط - مصر - ملاعب مدرسة السلام المتطورة</div></div>
            <div class="custom-contact-item"><div>⏰</div><div><strong>أوقات العمل:</strong><br>السبت والخميس: 4م - 9م</div></div>
        </div>
        <div class="custom-map-container">
            <iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d113686.258448786!2d31.156289!3d27.186696!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x1438a5f5c5b5b5b5%3A0x5b5b5b5b5b5b5b5b!2z2YXZg9mF2YrYp9mG2Ykg2KfZhNiq2YbYqSDYp9mE2YXYqtmG2Kkg2KfZhNir2YTYp9mG2Ykg2KfZhNi52YjYp9mG!5e0!3m2!1sar!2seg!4v1700000000000!5m2!1sar!2seg"></iframe>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="custom-contact-card"><h3 style="color: #1e3a8a;">✉️ أرسل رسالة</h3></div>', unsafe_allow_html=True)
        with st.form("contact_form"):
            c_name = st.text_input("الاسم الكامل *")
            c_phone = st.text_input("رقم الهاتف *")
            c_subject = st.selectbox("نوع الاستفسار *", ["", "استفسار عام", "معلومات عن البرامج", "التسجيل والاشتراك", "شكوى أو اقتراح"])
            c_msg = st.text_area("الرسالة *", height=100)
            submitted = st.form_submit_button("📨 إرسال الرسالة", use_container_width=True)
            if submitted:
                if c_name and c_phone and c_subject and c_msg:
                    data = {'name': c_name, 'phone': c_phone, 'subject': c_subject, 'message': c_msg, 'contactDate': datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                    if save_contact(data):
                        st.success("✅ تم إرسال رسالتك بنجاح!")
                    else:
                        st.error("❌ حدث خطأ")
                else:
                    st.error("⚠️ يرجى ملء جميع الحقول المطلوبة")

# ====================================================================================================
# 15. صفحة معرض الصور (Gallery Page)
# ====================================================================================================
elif page == 'gallery':
    st.markdown("""
    <div class="custom-page-header">
        <h1>📸 معرض الصور</h1>
        <p>لحظات من التدريبات والمباريات في الكوتش أكاديمي</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.image("https://via.placeholder.com/300x200/1e3a8a/ffffff?text=تدريبات+يومية", caption="تدريبات يومية", use_container_width=True)
        st.image("https://via.placeholder.com/300x200/3b82f6/ffffff?text=مباريات+ودية", caption="مباريات ودية", use_container_width=True)
    with col2:
        st.image("https://via.placeholder.com/300x200/f59e0b/ffffff?text=فريق+المدربين", caption="فريق المدربين", use_container_width=True)
        st.image("https://via.placeholder.com/300x200/10b981/ffffff?text=تكريم+اللاعبين", caption="تكريم المتميزين", use_container_width=True)
    with col3:
        st.image("https://via.placeholder.com/300x200/ef4444/ffffff?text=البطولات", caption="المشاركات والبطولات", use_container_width=True)
        st.image("https://via.placeholder.com/300x200/8b5cf6/ffffff?text=الاحتفالات", caption="الاحتفالات", use_container_width=True)

# ====================================================================================================
# 16. صفحة الأخبار (News Page)
# ====================================================================================================
elif page == 'news':
    st.markdown("""
    <div class="custom-page-header">
        <h1>📰 آخر الأخبار</h1>
        <p>أحدث المستجدات والإعلانات من الكوتش أكاديمي</p>
    </div>
    """, unsafe_allow_html=True)
    
    news_items = [
        {"title": "بدء التسجيل للموسم الجديد 2025", "date": "2025-01-15", "content": "يعلن الكوتش أكاديمي عن بدء التسجيل للموسم الجديد 2025. خصومات خاصة للمسجلين المبكرين."},
        {"title": "فوز فريق الأكاديمية ببطولة أسيوط", "date": "2025-01-10", "content": "حقق فريق تحت 12 سنة فوزًا مستحقًا في بطولة أسيوط بعد تفوقه على 8 فرق."},
        {"title": "محاضرة تدريبية للمدربين", "date": "2025-01-05", "content": "أقيمت محاضرة تدريبية للمدربين حول أحدث أساليب التدريب الحديثة."},
        {"title": "افتتاح فرع جديد للأكاديمية", "date": "2024-12-20", "content": "يعلن الكوتش أكاديمي عن افتتاح فرع جديد في مدينة نصر قريبًا."},
    ]
    
    for news in news_items:
        st.markdown(f"""
        <div style="background: white; border-radius: 20px; padding: 25px; margin-bottom: 20px; border-right: 4px solid #f59e0b;">
            <h3 style="color: #1e3a8a;">📌 {news['title']}</h3>
            <p style="color: #64748b;">📅 {news['date']}</p>
            <p style="color: #334155;">{news['content']}</p>
        </div>
        """, unsafe_allow_html=True)

# إغلاق حاوية المحتوى
st.markdown('</div>', unsafe_allow_html=True)

# ====================================================================================================
# 17. الفوتر (Footer)
# ====================================================================================================
st.markdown(f"""
<div class="custom-main-footer">
    <div class="custom-footer-grid">
        <div>
            <div style="display: flex; align-items: center; gap: 15px;">
                <div style="width: 55px; height: 55px; background: linear-gradient(135deg, #3b82f6, #1e3a8a); border-radius: 16px; display: flex; align-items: center; justify-content: center;">⚽</div>
                <h3 style="color: white;">الكوتش أكاديمي</h3>
            </div>
            <p style="color: #cbd5e1;">تأسست عام 2020 على ملاعب مدرسة السلام المتطورة. أول أكاديمية متخصصة في مصر.</p>
        </div>
        <div>
            <h4 style="color: white;">روابط سريعة</h4>
            <ul style="list-style: none;">
                <li><a href="#" onclick="customNavigateToPage('home'); return false;" class="custom-footer-link">← الرئيسية</a></li>
                <li><a href="#" onclick="customNavigateToPage('about'); return false;" class="custom-footer-link">← من نحن</a></li>
                <li><a href="#" onclick="customNavigateToPage('programs'); return false;" class="custom-footer-link">← البرامج التدريبية</a></li>
                <li><a href="#" onclick="customNavigateToPage('coaches'); return false;" class="custom-footer-link">← المدربون</a></li>
                <li><a href="#" onclick="customNavigateToPage('registration'); return false;" class="custom-footer-link">← تسجيل لاعب جديد</a></li>
                <li><a href="#" onclick="customNavigateToPage('faq'); return false;" class="custom-footer-link">← الأسئلة الشائعة</a></li>
                <li><a href="#" onclick="customNavigateToPage('contact'); return false;" class="custom-footer-link">← اتصل بنا</a></li>
                <li><a href="#" onclick="customNavigateToPage('gallery'); return false;" class="custom-footer-link">← معرض الصور</a></li>
                <li><a href="#" onclick="customNavigateToPage('news'); return false;" class="custom-footer-link">← الأخبار</a></li>
            </ul>
        </div>
        <div>
            <h4 style="color: white;">معلومات الاتصال</h4>
            <ul style="list-style: none;">
                <li>📍 أسيوط - مصر</li>
                <li>📞 01069238878</li>
                <li>💬 01285197778</li>
                <li>⏰ السبت والخميس: 4م - 9م</li>
            </ul>
        </div>
    </div>
    <div style="text-align: center;">
        <p style="color: #94a3b8;">© 2025 الكوتش أكاديمي - جميع الحقوق محفوظة</p>
        <p style="color: #94a3b8;">عدد زوار الموقع: {st.session_state.visitor_count:,}+ زائر</p>
    </div>
</div>

<script>
window.customNavigateToPage = function(page) {{
    const url = new URL(window.location);
    url.searchParams.set('page', page);
    window.location.href = url.toString();
}};
</script>
""", unsafe_allow_html=True)

# ====================================================================================================
# نهاية الكود
# ====================================================================================================
