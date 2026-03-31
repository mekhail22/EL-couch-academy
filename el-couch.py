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
    initial_sidebar_state="expanded"
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
if 'last_visit' not in st.session_state:
    st.session_state.last_visit = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# ====================================================================================================
# 3. تحويل الصورة إلى Base64
# ====================================================================================================
def get_image_base64(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    except:
        return None

logo_base64 = get_image_base64("logo.jpg")

# ====================================================================================================
# 4. CSS الرئيسي والأنماط
# ====================================================================================================
st.markdown("""
<style>
    /* ---------------------------------------------------------------------------------------------- */
    /* إخفاء عناصر Streamlit الافتراضية */
    /* ---------------------------------------------------------------------------------------------- */
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
    .stApp {
        background: linear-gradient(135deg, #f0f2f6 0%, #ffffff 100%) !important;
    }
    
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
        justify-content: center;
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
        background: linear-gradient(135deg, #1e3a8a, #3b82f6);
    }
    
    .custom-logo-image img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
    
    .custom-logo-image span {
        font-size: 2.2rem;
        color: white;
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
    /* تخصيص الـ Sidebar */
    /* ---------------------------------------------------------------------------------------------- */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
        padding-top: 90px;
    }
    
    section[data-testid="stSidebar"] .stMarkdown {
        color: white;
    }
    
    /* تخصيص عناصر الـ Sidebar */
    .sidebar-logo {
        text-align: center;
        padding: 20px 0;
        border-bottom: 1px solid rgba(255,255,255,0.1);
        margin-bottom: 20px;
    }
    
    .sidebar-logo-image {
        width: 80px;
        height: 80px;
        margin: 0 auto;
        border-radius: 25px;
        overflow: hidden;
        background: linear-gradient(135deg, #3b82f6, #1e3a8a);
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 15px;
    }
    
    .sidebar-logo-image img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
    
    .sidebar-logo-image span {
        font-size: 2.5rem;
        color: white;
    }
    
    .sidebar-logo h2 {
        color: white;
        font-size: 1.3rem;
        margin: 0;
    }
    
    .sidebar-logo p {
        color: #94a3b8;
        font-size: 0.7rem;
        margin-top: 5px;
    }
    
    /* تخصيص أزرار الـ Sidebar */
    .stButton button {
        background: transparent !important;
        border: none !important;
        color: #cbd5e1 !important;
        text-align: right !important;
        padding: 12px 20px !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
        justify-content: flex-start !important;
    }
    
    .stButton button:hover {
        background: linear-gradient(135deg, #3b82f6, #1e3a8a) !important;
        color: white !important;
        transform: translateX(5px);
    }
    
    /* تنسيق الأزرار النشطة */
    .active-nav-btn {
        background: linear-gradient(135deg, #3b82f6, #1e3a8a) !important;
        color: white !important;
        border-right: 3px solid #f59e0b !important;
    }
    
    /* ---------------------------------------------------------------------------------------------- */
    /* القسم الرئيسي Hero */
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
    
    .custom-hero-section::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.15) 0%, transparent 70%);
        animation: rotateSlow 25s linear infinite;
    }
    
    @keyframes rotateSlow {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
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
        background: linear-gradient(135deg, #ffffff, #f8fafc);
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
    /* زر التسجيل */
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
    .custom-registration-form-container {
        max-width: 750px;
        margin: 0 auto;
        background: white;
        padding: 40px;
        border-radius: 28px;
        box-shadow: 0 10px 35px rgba(0, 0, 0, 0.1);
    }
    
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
    /* بطاقات الأخبار */
    /* ---------------------------------------------------------------------------------------------- */
    .custom-news-card {
        background: white;
        border-radius: 20px;
        padding: 25px;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
        border-right: 4px solid #f59e0b;
        transition: all 0.3s ease;
    }
    
    .custom-news-card:hover {
        transform: translateX(-8px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
    }
    
    /* ---------------------------------------------------------------------------------------------- */
    /* بطاقات المعرض */
    /* ---------------------------------------------------------------------------------------------- */
    .custom-gallery-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 25px;
        margin-bottom: 40px;
    }
    
    .custom-gallery-item {
        background: white;
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
    }
    
    .custom-gallery-item:hover {
        transform: translateY(-8px);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
    }
    
    .custom-gallery-image {
        height: 200px;
        background: linear-gradient(135deg, #3b82f6, #1e3a8a);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 3rem;
        color: white;
    }
    
    .custom-gallery-caption {
        padding: 15px;
        text-align: center;
        color: #334155;
        font-weight: 500;
    }
    
    /* ---------------------------------------------------------------------------------------------- */
    /* الفوتر */
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
    
    .custom-social-icons {
        display: flex;
        gap: 15px;
        margin-top: 15px;
    }
    
    .custom-social-icon {
        width: 40px;
        height: 40px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .custom-social-icon:hover {
        background: #f59e0b;
        transform: translateY(-3px);
    }
    
    /* ---------------------------------------------------------------------------------------------- */
    /* تنسيقات للشاشات الصغيرة */
    /* ---------------------------------------------------------------------------------------------- */
    @media (max-width: 768px) {
        .custom-stats-grid, .custom-features-grid, .custom-programs-grid, 
        .custom-coaches-grid, .custom-contact-wrapper, .custom-about-wrapper, 
        .custom-mission-vision-grid, .custom-gallery-grid {
            grid-template-columns: 1fr;
        }
        .custom-hero-section h1 { font-size: 2rem; }
        .custom-section-title { font-size: 1.6rem; }
        .custom-stat-number { font-size: 2.2rem; }
        .custom-logo-text h1 { font-size: 1.2rem; }
        .custom-logo-image { width: 45px; height: 45px; }
        .custom-header-spacer { height: 80px; }
        .custom-register-btn { padding: 14px 35px; font-size: 1rem; }
        .custom-hero-section { padding: 60px 20px; }
        .custom-page-header h1 { font-size: 1.8rem; }
    }
</style>
""", unsafe_allow_html=True)

# ====================================================================================================
# 5. إضافة الهيدر العلوي
# ====================================================================================================
logo_html = ""
if logo_base64:
    logo_html = f'<img src="data:image/jpeg;base64,{logo_base64}" alt="Logo">'
else:
    logo_html = '<span>⚽</span>'

st.markdown(f"""
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
    </div>
</div>
<div class="custom-header-spacer"></div>

<script>
document.getElementById('logoClickArea').addEventListener('click', function() {{
    const url = new URL(window.location);
    url.searchParams.set('page', 'home');
    window.location.href = url.toString();
}});
</script>
""", unsafe_allow_html=True)

# ====================================================================================================
# 6. تخصيص الـ Sidebar
# ====================================================================================================
with st.sidebar:
    st.markdown(f"""
    <div class="sidebar-logo">
        <div class="sidebar-logo-image">
            {logo_html if logo_base64 else '<span>⚽</span>'}
        </div>
        <h2>الكوتش أكاديمي</h2>
        <p>أكاديمية كرة القدم المتخصصة</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # أزرار التنقل في الـ Sidebar
    nav_items = [
        {"page": "home", "icon": "🏠", "name": "الرئيسية"},
        {"page": "about", "icon": "ℹ️", "name": "من نحن"},
        {"page": "programs", "icon": "⚽", "name": "البرامج التدريبية"},
        {"page": "coaches", "icon": "👨‍🏫", "name": "المدربون"},
        {"page": "registration", "icon": "📝", "name": "تسجيل لاعب جديد"},
        {"page": "faq", "icon": "❓", "name": "الأسئلة الشائعة"},
        {"page": "contact", "icon": "📞", "name": "اتصل بنا"},
        {"page": "gallery", "icon": "📸", "name": "معرض الصور"},
        {"page": "news", "icon": "📰", "name": "الأخبار"},
    ]
    
    for item in nav_items:
        if st.button(f"{item['icon']} {item['name']}", key=f"nav_{item['page']}", use_container_width=True):
            st.session_state.page = item['page']
            st.rerun()
    
    st.markdown("---")
    
    # معلومات الاتصال في الـ Sidebar
    st.markdown("""
    <div style="padding: 15px 0;">
        <p style="color: #94a3b8; font-size: 0.8rem; margin-bottom: 10px;">📞 للاستفسار:</p>
        <p style="color: #cbd5e1; font-size: 0.9rem;">01069238878</p>
        <p style="color: #cbd5e1; font-size: 0.9rem; margin-top: 5px;">01285197778</p>
        <p style="color: #94a3b8; font-size: 0.8rem; margin-top: 15px;">⏰ أوقات العمل:</p>
        <p style="color: #cbd5e1; font-size: 0.8rem;">السبت والخميس: 4م - 9م</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # إحصائيات الزوار
    st.markdown(f"""
    <div style="text-align: center; padding: 15px 0;">
        <p style="color: #94a3b8; font-size: 0.7rem;">👥 زوار الموقع</p>
        <p style="color: #f59e0b; font-size: 1.2rem; font-weight: bold;">{st.session_state.visitor_count:,}+</p>
        <p style="color: #94a3b8; font-size: 0.6rem; margin-top: 5px;">آخر زيارة: {st.session_state.last_visit}</p>
    </div>
    """, unsafe_allow_html=True)

# ====================================================================================================
# 7. دوال حفظ البيانات
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
    except Exception:
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
    except Exception:
        return False

# ====================================================================================================
# 8. تحديد الصفحة الحالية
# ====================================================================================================
query_params = st.query_params
if 'page' in query_params:
    st.session_state.page = query_params['page']

page = st.session_state.page

# بداية حاوية المحتوى
st.markdown('<div class="custom-content-container">', unsafe_allow_html=True)

# ====================================================================================================
# 9. الصفحة الرئيسية
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
            <button class="custom-register-btn" onclick="navigateToPage('registration')">📝 سجل ابنك الآن</button>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="custom-section-title">إنجازات الأكاديمية</div>', unsafe_allow_html=True)
    st.markdown("""
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
    
    st.markdown('<div class="custom-section-title">أحدث الأخبار</div>', unsafe_allow_html=True)
    news_preview = [
        {"title": "بدء التسجيل للموسم الجديد 2025", "date": "2025-01-15"},
        {"title": "فوز فريق الأكاديمية ببطولة أسيوط", "date": "2025-01-10"},
        {"title": "محاضرة تدريبية للمدربين", "date": "2025-01-05"},
    ]
    cols = st.columns(3)
    for i, news in enumerate(news_preview):
        with cols[i]:
            st.markdown(f"""
            <div style="background: white; border-radius: 20px; padding: 20px; text-align: center; border-right: 3px solid #f59e0b;">
                <h4 style="color: #1e3a8a;">📌 {news['title']}</h4>
                <p style="color: #64748b; font-size: 0.8rem;">{news['date']}</p>
                <a href="#" onclick="navigateToPage('news'); return false;" style="color: #3b82f6; text-decoration: none;">اقرأ المزيد →</a>
            </div>
            """, unsafe_allow_html=True)

# ====================================================================================================
# 10. صفحة من نحن
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
            <ul style="margin-right: 25px; margin-top: 18px; color: #334155; font-size: 1rem;">
                <li>كابتن ميخائيل كميل رؤف (ميخا) - المدير الفني</li>
                <li>كابتن اندرو - مدرب مهارات</li>
                <li>كابتن مينا - مدرب لياقة بدنية</li>
            </ul>
            <p style="margin-top: 22px; color: #334155;">على ملاعب مدرسة السلام المتطورة - أسيوط</p>
            <p style="margin-top: 18px; font-weight: 700; color: #1e3a8a; font-size: 1.05rem;">بدعم من الأب الروحي للأكاديمية: مستر / مؤنس منير</p>
        </div>
    </div>
    <div class="custom-mission-vision-grid">
        <div class="custom-mission-card">
            <h3 style="color: #1e3a8a; font-size: 1.6rem; margin-bottom: 18px;">🎯 رسالتنا</h3>
            <p style="color: #334155; line-height: 1.7;">تطوير جيل جديد من اللاعبين المبدعين القادرين على التألق محليًا ودوليًا، من خلال تقديم تدريب عصري يعتمد على أحدث الأساليب العلمية والتكنولوجية في عالم كرة القدم.</p>
            <ul style="margin-right: 20px; margin-top: 20px; color: #334155;">
                <li>تطوير المهارات الفنية الأساسية والمتقدمة</li>
                <li>بناء اللياقة البدنية المخصصة لكل لاعب</li>
                <li>تعزيز الذكاء الكروي والقدرات الذهنية</li>
                <li>غرس القيم الرياضية والسلوك القيادي</li>
            </ul>
        </div>
        <div class="custom-vision-card">
            <h3 style="color: #1e3a8a; font-size: 1.6rem; margin-bottom: 18px;">👁️ رؤيتنا</h3>
            <p style="color: #334155; line-height: 1.7;">أن نكون الوجهة الأولى لأي موهبة كروية في مصر والوطن العربي، والجسر الذي يعبر من خلاله اللاعبون الموهوبون إلى العالمية، وأن نصنع جيلاً من القادة داخل وخارج الملعب.</p>
            <ul style="margin-right: 20px; margin-top: 20px; color: #334155;">
                <li>صناعة لاعبين مؤهلين للدوريات العالمية</li>
                <li>تطوير منهج تدريبي يُدرس في المعاهد الرياضية</li>
                <li>المساهمة في تطوير كرة القدم العربية</li>
                <li>بناء قاعدة بيانات للمواهب الكروية</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="margin-top: 45px; padding: 30px; background: linear-gradient(135deg, #1e3a8a, #3b82f6); border-radius: 28px; text-align: center; color: white;">
        <h3 style="font-size: 1.8rem;">📊 أرقام وإحصائيات</h3>
        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-top: 30px;">
            <div><div style="font-size: 2rem;">🎓</div><div style="font-weight: bold;">4+</div><div>سنوات من التميز</div></div>
            <div><div style="font-size: 2rem;">👥</div><div style="font-weight: bold;">500+</div><div>لاعب تم تدريبهم</div></div>
            <div><div style="font-size: 2rem;">🏆</div><div style="font-weight: bold;">25+</div><div>بطولة محلية</div></div>
            <div><div style="font-size: 2rem;">⭐</div><div style="font-weight: bold;">150+</div><div>لاعب محترف</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ====================================================================================================
# 11. صفحة البرامج التدريبية
# ====================================================================================================
elif page == 'programs':
    st.markdown("""
    <div class="custom-page-header">
        <h1>البرامج التدريبية</h1>
        <p>مواعيد تدريبية مصممة لكل فئة عمرية وجنسية</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="custom-programs-grid">
        <div class="custom-program-card">
            <div class="custom-program-header">📅 السبت</div>
            <div class="custom-program-body">
                <h3>مواعيد تدريب السبت</h3>
                <div class="custom-schedule-box">
                    <div class="custom-schedule-item"><strong>🕔 ٥:٠٠ - ٦:٠٠ م</strong> → 🏃‍♀️ بنات (جميع الأعمار)</div>
                    <div class="custom-schedule-item"><strong>🕕 ٦:٠٠ - ٧:٣٠ م</strong> → 🏃 بنين (الصف الأول - الخامس الابتدائي)</div>
                    <div class="custom-schedule-item"><strong>🕢 ٧:٣٠ - ٩:٠٠ م</strong> → 🏃 بنين (الصف السادس الابتدائي - الثاني الإعدادي)</div>
                    <div style="margin-top: 18px; color: #64748b; font-size: 0.9rem;">📍 ملاعب مدرسة السلام المتطورة - أسيوط</div>
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
                    <div style="margin-top: 18px; color: #64748b; font-size: 0.9rem;">📍 ملاعب مدرسة السلام المتطورة - أسيوط</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="custom-program-card" style="margin-top: 25px;">
        <div class="custom-program-header">⚽ معلومات عامة عن البرامج</div>
        <div class="custom-program-body">
            <h3>تفاصيل البرامج التدريبية</h3>
            <div class="custom-schedule-box">
                <h4 style="color: #1e3a8a; margin-bottom: 15px; font-size: 1.2rem;">🎯 أهداف التدريب:</h4>
                <ul style="margin-right: 20px; margin-bottom: 20px;">
                    <li>تنمية المهارات الفنية الأساسية (التمرير - الاستلام - المراوغة - التسديد)</li>
                    <li>تطوير القدرات البدنية (السرعة - الرشاقة - القوة - التحمل)</li>
                    <li>تعزيز العمل الجماعي والانضباط التكتيكي</li>
                    <li>بناء الشخصية الرياضية والثقة بالنفس</li>
                    <li>تطوير الذكاء الكروي والقدرة على القراءة التحليلية للملعب</li>
                </ul>
                <h4 style="color: #1e3a8a; margin-bottom: 15px; font-size: 1.2rem;">💼 ما يقدمه النادي للاعبين:</h4>
                <ul style="margin-right: 20px;">
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
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="margin-top: 40px; background: linear-gradient(135deg, #f0f9ff, #e0f2fe); border-radius: 24px; padding: 30px; text-align: center;">
        <h3 style="color: #1e3a8a;">📞 للتسجيل والاستفسار</h3>
        <p style="color: #334155; margin: 15px 0;">تواصل معنا الآن للحصول على عرض تجريبي مجاني</p>
        <button class="custom-register-btn" onclick="navigateToPage('registration')" style="padding: 12px 35px; font-size: 1rem;">سجل الآن</button>
    </div>
    """, unsafe_allow_html=True)

# ====================================================================================================
# 12. صفحة المدربون
# ====================================================================================================
elif page == 'coaches':
    st.markdown("""
    <div class="custom-page-header">
        <h1>المدربون</h1>
        <p>فريقنا من المدربين المحترفين ذوي الخبرة والكفاءة</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="custom-coaches-grid">
        <div class="custom-coach-card">
            <div class="custom-coach-avatar">👨‍🏫</div>
            <div class="custom-coach-info">
                <h3>كابتن/ميخائيل كميل رؤف</h3>
                <div class="custom-coach-title">المدير الفني - مدرب معتمد (CAF)</div>
                <div class="custom-coach-desc">🎓 بكالريوس تربية رياضية<br>📜 رخصة تدريب CAF لمراحل البراعم<br>📜 دبلومة الإعداد البدني المتقدم<br>📜 دبلومة إصابات الملاعب والعلاج الطبيعي</div>
            </div>
        </div>
        <div class="custom-coach-card">
            <div class="custom-coach-avatar">🧤</div>
            <div class="custom-coach-info">
                <h3>كابتن أحمد علي</h3>
                <div class="custom-coach-title">مدرب حراس مرمى - معتمد (CAF)</div>
                <div class="custom-coach-desc">🎓 بكالريوس تربية رياضية<br>📜 رخصة تدريب حراس مرمى CAF<br>📜 خبرة 15 عامًا في تدريب حراس المرمى</div>
            </div>
        </div>
        <div class="custom-coach-card">
            <div class="custom-coach-avatar">🏃</div>
            <div class="custom-coach-info">
                <h3>د. خالد السيد</h3>
                <div class="custom-coach-title">مدرب لياقة بدنية - دكتوراه</div>
                <div class="custom-coach-desc">🎓 دكتوراه في علوم الرياضة<br>📜 أستاذ مساعد بكلية التربية الرياضية<br>📜 مختص في تطوير قدرات الناشئين</div>
            </div>
        </div>
        <div class="custom-coach-card">
            <div class="custom-coach-avatar">⚽</div>
            <div class="custom-coach-info">
                <h3>كابتن محمد جابر</h3>
                <div class="custom-coach-title">مدرب مهارات فنية - معتمد (CAF)</div>
                <div class="custom-coach-desc">🎓 بكالريوس تربية رياضية<br>📜 رخصة تدريب مهارات CAF<br>📜 خبرة 12 عامًا في تدريب المهارات الفنية</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1e3a8a, #3b82f6); border-radius: 28px; padding: 40px; text-align: center; color: white;">
        <h3 style="font-size: 1.8rem;">🌟 فريق تدريب متكامل</h3>
        <p style="margin-top: 15px;">يجمع فريقنا بين الخبرات الأكاديمية والعملية لضمان أفضل تدريب للاعبين</p>
        <div style="display: flex; justify-content: center; gap: 20px; margin-top: 25px;">
            <div><span style="font-size: 1.5rem;">12+</span><br>مدرب معتمد</div>
            <div><span style="font-size: 1.5rem;">100+</span><br>دورة تدريبية</div>
            <div><span style="font-size: 1.5rem;">20+</span><br>سنة خبرة</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ====================================================================================================
# 13. صفحة التسجيل
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
        col1, col2 = st.columns(2)
        with col1:
            player_name = st.text_input("اسم اللاعب الثلاثي *", placeholder="مثال: محمد أحمد محمود")
            birth_date = st.date_input("تاريخ الميلاد *", None)
            previous_club = st.text_input("النادي السابق (إن وجد)", placeholder="اسم النادي السابق")
        with col2:
            age_group = st.selectbox("الفئة العمرية المطلوبة *", ["", "🏃‍♀️ بنات (جميع الأعمار)", "🏃 بنين (الصف الأول - الخامس الابتدائي)", "🏃 بنين (الصف السادس الابتدائي - الثاني الإعدادي)"])
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
                    'playerName': player_name, 'ageGroup': age_group, 'birthDate': str(birth_date) if birth_date else "",
                    'previousClub': previous_club, 'position': position, 'shirtSize': shirt_size,
                    'parentName': parent_name, 'parentPhone': parent_phone, 'parentWhatsapp': parent_whatsapp,
                    'parentEmail': parent_email, 'address': address, 'medicalNotes': medical_notes,
                    'notes': notes, 'trainingDays': training_days,
                    'registrationDate': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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

# ====================================================================================================
# 14. صفحة الأسئلة الشائعة
# ====================================================================================================
elif page == 'faq':
    st.markdown("""
    <div class="custom-page-header">
        <h1>الأسئلة الشائعة</h1>
        <p>إجابات على أكثر الأسئلة شيوعًا من أولياء الأمور</p>
    </div>
    """, unsafe_allow_html=True)
    
    faqs = [
        ("ما الذي يميز الكوتش أكاديمي عن غيرها من الأكاديميات؟", 
         "الكوتش أكاديمي تتبنى منهجية تدريب متكاملة وشاملة تركز على عدة محاور: (1) التدريب الذهني وتطوير الذكاء الكروي، (2) متابعة فردية لكل لاعب مع خطة تطوير شخصية، (3) استخدام التكنولوجيا الحديثة في تحليل الأداء، (4) شراكات مع أندية محلية ودولية لدعم الموهوبين، (5) مدربين معتمدين دوليًا من CAF."),
        
        ("ما هي مدة التدريب وأوقاته؟", 
         "الموسم التدريبي يمتد لمدة 10 أشهر، من بداية سبتمبر إلى نهاية يونيو. التدريبات تقام في الفترة المسائية أيام السبت والخميس حسب الجدول المحدد لكل فئة عمرية."),
        
        ("ما هي تكلفة الاشتراك وآلية الدفع؟", 
         "تختلف التكلفة حسب الفئة العمرية وعدد أيام التدريب في الأسبوع. نقدم خصومات خاصة للأشقاء، نظام تقسيط شهري مرن، منح جزئية للمتميزين، خصم للتسجيل المبكر."),
        
        ("ما هي متطلبات الانضمام للأكاديمية؟", 
         "إكمال نموذج التسجيل، أن يكون اللاعب في الفئة العمرية المحددة، الرغبة الحقيقية في التعلم، الالتزام بمواعيد التدريب، تقديم شهادة ميلاد وصورة شخصية، دفع رسوم الاشتراك."),
        
        ("هل هناك تدريبات خاصة للمبتدئين؟", 
         "نعم، لدينا برامج خاصة للمبتدئين تركز على تعلم أساسيات كرة القدم، تطوير المهارات الحركية الأساسية، بناء الثقة بالنفس، تعزيز العمل الجماعي."),
        
        ("كيف يمكن متابعة تطور اللاعب داخل الأكاديمية؟", 
         "نوفر تقييم فني دوري، متابعة التطور البدني، تقارير شهرية، لقاءات دورية مع أولياء الأمور، فيديوهات تحليل أداء للمتميزين."),
        
        ("ماذا عن السلامة والإصابات خلال التدريب؟", 
         "نوفر إشراف مستمر، بيئة تدريب آمنة، برنامج إحماء وتبريد مناسب، مدربين حاصلين على شهادات إسعافات أولية، تأمين صحي للاعبين."),
        
        ("هل يوجد تدريبات مخصصة للبنات؟", 
         "نعم، لدينا برامج تدريبية مخصصة للبنات مع مدربات متخصصات، وبيئة مناسبة ومحترمة مع مراعاة الخصوصية."),
        
        ("كيف يمكنني التواصل مع إدارة الأكاديمية؟", 
         "يمكنك التواصل عبر الهاتف 01069238878، الواتساب 01285197778، البريد الإلكتروني info@elcoach-academy.com، أو زيارة الأكاديمية."),
    ]
    
    for q, a in faqs:
        with st.expander(f"❓ {q}"):
            st.markdown(f'<p style="color: #334155; line-height: 1.7;">{a}</p>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="margin-top: 40px; background: linear-gradient(135deg, #f0f9ff, #e0f2fe); border-radius: 24px; padding: 30px; text-align: center;">
        <h3 style="color: #1e3a8a;">❗ لم تجد سؤالك؟</h3>
        <p style="color: #334155; margin: 15px 0;">تواصل معنا وسنقوم بالرد عليك في أقرب وقت</p>
        <button class="custom-register-btn" onclick="navigateToPage('contact')" style="padding: 12px 35px; font-size: 1rem;">اتصل بنا</button>
    </div>
    """, unsafe_allow_html=True)

# ====================================================================================================
# 15. صفحة اتصل بنا
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
            <h3 style="color: #1e3a8a; margin-bottom: 28px; font-size: 1.5rem;">📞 معلومات الاتصال</h3>
            <div class="custom-contact-item">
                <div style="font-size: 1.6rem;">📱</div>
                <div><strong>الهاتف:</strong><br><a href="tel:01069238878" style="text-decoration: none; color: #334155;">01069238878</a></div>
            </div>
            <div class="custom-contact-item">
                <div style="font-size: 1.6rem;">💬</div>
                <div><strong>الواتساب:</strong><br><a href="https://wa.me/201285197778" target="_blank" style="text-decoration: none; color: #25D366;">01285197778</a></div>
            </div>
            <div class="custom-contact-item">
                <div style="font-size: 1.6rem;">📍</div>
                <div><strong>العنوان الرئيسي:</strong><br>محافظة أسيوط - مصر<br>ملاعب مدرسة السلام المتطورة</div>
            </div>
            <div class="custom-contact-item">
                <div style="font-size: 1.6rem;">⏰</div>
                <div><strong>أوقات العمل:</strong><br>السبت والخميس: 4:00 م - 9:00 م</div>
            </div>
            <div class="custom-contact-item">
                <div style="font-size: 1.6rem;">📧</div>
                <div><strong>البريد الإلكتروني:</strong><br>info@elcoach-academy.com</div>
            </div>
        </div>
        
        <div class="custom-map-container">
            <iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d113686.258448786!2d31.156289!3d27.186696!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x1438a5f5c5b5b5b5%3A0x5b5b5b5b5b5b5b5b!2z2YXZg9mF2YrYp9mG2Ykg2KfZhNiq2YbYqSDYp9mE2YXYqtmG2Kkg2KfZhNir2YTYp9mG2Ykg2KfZhNi52YjYp9mG!5e0!3m2!1sar!2seg!4v1700000000000!5m2!1sar!2seg" 
                    allowfullscreen="" loading="lazy"></iframe>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="custom-contact-card"><h3 style="color: #1e3a8a;">✉️ أرسل رسالة</h3><p style="color: #64748b; margin-bottom: 20px;">سنقوم بالرد عليك في أقرب وقت ممكن خلال 24 ساعة</p></div>', unsafe_allow_html=True)
        
        with st.form("contact_form"):
            c_name = st.text_input("الاسم الكامل *")
            c_phone = st.text_input("رقم الهاتف *", placeholder="01XXXXXXXXX")
            c_email = st.text_input("البريد الإلكتروني", placeholder="example@email.com")
            c_subject = st.selectbox("نوع الاستفسار *", ["", "استفسار عام", "معلومات عن البرامج", "التسجيل والاشتراك", "شكوى أو اقتراح", "طلب شراكة", "أخرى"])
            c_msg = st.text_area("الرسالة *", height=130, placeholder="اكتب رسالتك هنا...")
            
            submitted = st.form_submit_button("📨 إرسال الرسالة", use_container_width=True)
            
            if submitted:
                if c_name and c_phone and c_subject and c_msg:
                    data = {
                        'name': c_name, 'phone': c_phone, 'email': c_email,
                        'subject': c_subject, 'message': c_msg,
                        'contactDate': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    if save_contact(data):
                        st.success("✅ شكراً لتواصلك! تم إرسال رسالتك بنجاح.")
                    else:
                        st.error("❌ حدث خطأ في حفظ البيانات")
                else:
                    st.error("⚠️ يرجى ملء جميع الحقول المطلوبة")
        
        st.markdown("""
        <div class="custom-contact-card" style="margin-top: 25px;">
            <h3 style="color: #1e3a8a;">🌐 تابعنا على وسائل التواصل</h3>
            <div class="custom-social-icons" style="justify-content: center;">
                <div class="custom-social-icon">📘</div>
                <div class="custom-social-icon">🐦</div>
                <div class="custom-social-icon">📷</div>
                <div class="custom-social-icon">💬</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ====================================================================================================
# 16. صفحة معرض الصور
# ====================================================================================================
elif page == 'gallery':
    st.markdown("""
    <div class="custom-page-header">
        <h1>📸 معرض الصور</h1>
        <p>لحظات من التدريبات والمباريات في الكوتش أكاديمي</p>
    </div>
    """, unsafe_allow_html=True)
    
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
            st.markdown(f"""
            <div class="custom-gallery-item">
                <div class="custom-gallery-image">{item['icon']}</div>
                <div class="custom-gallery-caption">
                    <h4 style="color: #1e3a8a;">{item['title']}</h4>
                    <p style="font-size: 0.85rem; color: #64748b;">{item['desc']}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; margin-top: 40px; padding: 30px; background: linear-gradient(135deg, #f0f9ff, #e0f2fe); border-radius: 24px;">
        <p style="color: #1e3a8a; font-size: 1.1rem;">📸 يتم تحديث المعرض باستمرار بأحدث الصور</p>
        <p style="color: #64748b; margin-top: 10px;">تابعونا على وسائل التواصل لمشاهدة المزيد</p>
    </div>
    """, unsafe_allow_html=True)

# ====================================================================================================
# 17. صفحة الأخبار
# ====================================================================================================
elif page == 'news':
    st.markdown("""
    <div class="custom-page-header">
        <h1>📰 آخر الأخبار</h1>
        <p>أحدث المستجدات والإعلانات من الكوتش أكاديمي</p>
    </div>
    """, unsafe_allow_html=True)
    
    news_items = [
        {"title": "بدء التسجيل للموسم الجديد 2025", "date": "2025-01-15", "content": "يعلن الكوتش أكاديمي عن بدء التسجيل للموسم الجديد 2025. خصومات خاصة للمسجلين المبكرين حتى نهاية فبراير.", "author": "إدارة الأكاديمية"},
        {"title": "فوز فريق الأكاديمية ببطولة أسيوط", "date": "2025-01-10", "content": "حقق فريق تحت 12 سنة فوزًا مستحقًا في بطولة أسيوط الرمضانية بعد تفوقه على 8 فرق.", "author": "كابتن ميخا"},
        {"title": "محاضرة تدريبية للمدربين", "date": "2025-01-05", "content": "أقيمت محاضرة تدريبية للمدربين حول أحدث أساليب التدريب الحديثة بحضور خبراء من الاتحاد المصري.", "author": "إدارة التدريب"},
        {"title": "افتتاح فرع جديد للأكاديمية", "date": "2024-12-20", "content": "يعلن الكوتش أكاديمي عن افتتاح فرع جديد في مدينة نصر خلال الأشهر القادمة.", "author": "الإدارة التنفيذية"},
        {"title": "تخريج دفعة جديدة من اللاعبين", "date": "2024-12-15", "content": "احتفلت الأكاديمية بتخريج دفعة جديدة من اللاعبين المتميزين الذين انضموا لأندية كبرى.", "author": "إدارة الأكاديمية"},
    ]
    
    for news in news_items:
        st.markdown(f"""
        <div class="custom-news-card">
            <h3 style="color: #1e3a8a;">📌 {news['title']}</h3>
            <div style="display: flex; gap: 15px; margin-bottom: 12px;">
                <p style="color: #64748b; font-size: 0.85rem;">📅 {news['date']}</p>
                <p style="color: #f59e0b; font-size: 0.85rem;">✍️ {news['author']}</p>
            </div>
            <p style="color: #334155; line-height: 1.6;">{news['content']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="margin-top: 40px; text-align: center;">
        <button class="custom-register-btn" onclick="navigateToPage('registration')" style="padding: 12px 35px; font-size: 1rem;">سجل الآن في الأكاديمية</button>
    </div>
    """, unsafe_allow_html=True)

# إغلاق حاوية المحتوى
st.markdown('</div>', unsafe_allow_html=True)

# ====================================================================================================
# 18. الفوتر
# ====================================================================================================
st.markdown(f"""
<div class="custom-main-footer">
    <div class="custom-footer-grid">
        <div>
            <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 20px;">
                <div style="width: 55px; height: 55px; background: linear-gradient(135deg, #3b82f6, #1e3a8a); border-radius: 16px; display: flex; align-items: center; justify-content: center; font-size: 1.8rem;">⚽</div>
                <h3 style="color: white;">الكوتش أكاديمي</h3>
            </div>
            <p style="color: #cbd5e1; font-size: 0.85rem;">تأسست عام 2020 على ملاعب مدرسة السلام المتطورة. أول أكاديمية متخصصة في مصر تركز على بناء اللاعب الشامل.</p>
        </div>
        <div>
            <h4 style="color: white;">روابط سريعة</h4>
            <ul style="list-style: none;">
                <li><a href="#" onclick="navigateToPage('home'); return false;" class="custom-footer-link">← الرئيسية</a></li>
                <li><a href="#" onclick="navigateToPage('about'); return false;" class="custom-footer-link">← من نحن</a></li>
                <li><a href="#" onclick="navigateToPage('programs'); return false;" class="custom-footer-link">← البرامج التدريبية</a></li>
                <li><a href="#" onclick="navigateToPage('coaches'); return false;" class="custom-footer-link">← المدربون</a></li>
                <li><a href="#" onclick="navigateToPage('registration'); return false;" class="custom-footer-link">← تسجيل لاعب جديد</a></li>
                <li><a href="#" onclick="navigateToPage('faq'); return false;" class="custom-footer-link">← الأسئلة الشائعة</a></li>
                <li><a href="#" onclick="navigateToPage('contact'); return false;" class="custom-footer-link">← اتصل بنا</a></li>
                <li><a href="#" onclick="navigateToPage('gallery'); return false;" class="custom-footer-link">← معرض الصور</a></li>
                <li><a href="#" onclick="navigateToPage('news'); return false;" class="custom-footer-link">← الأخبار</a></li>
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
    <div style="text-align: center; padding-top: 30px; border-top: 1px solid rgba(255,255,255,0.1);">
        <p style="color: #94a3b8;">© 2025 الكوتش أكاديمي - جميع الحقوق محفوظة</p>
        <p style="color: #94a3b8;">عدد زوار الموقع: {st.session_state.visitor_count:,}+ زائر</p>
    </div>
</div>

<script>
function navigateToPage(page) {{
    const url = new URL(window.location);
    url.searchParams.set('page', page);
    window.location.href = url.toString();
}}
window.navigateToPage = navigateToPage;
</script>
""", unsafe_allow_html=True)

# ====================================================================================================
# نهاية الكود
# ====================================================================================================
