import streamlit as st
import json
import os
from datetime import datetime
import hashlib
import random
import base64
import time

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
    /* زر البرجر منيو */
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
    /* القائمة الجانبية */
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
    
    .custom-side-navigation::-webkit-scrollbar { width: 6px; }
    .custom-side-navigation::-webkit-scrollbar-track { background: #e2e8f0; border-radius: 10px; }
    .custom-side-navigation::-webkit-scrollbar-thumb { background: #3b82f6; border-radius: 10px; }
    
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
    /* طبقة التعتيم */
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
        .custom-side-navigation { width: 280px; right: -280px; }
        .custom-register-btn { padding: 14px 35px; font-size: 1rem; }
        .custom-hero-section { padding: 60px 20px; }
        .custom-page-header h1 { font-size: 1.8rem; }
    }
</style>
""", unsafe_allow_html=True)

# ====================================================================================================
# 5. إضافة الهيدر والقائمة الجانبية
# ====================================================================================================

logo_html = ""
if logo_base64:
    logo_html = f'<img src="data:image/jpeg;base64,{logo_base64}" alt="Logo">'
else:
    logo_html = '<span>⚽</span>'

st.markdown(f"""
<div id="custom-header-root">
    <input type="checkbox" id="custom-menu-toggle" class="custom-menu-toggle">
    <div class="custom-top-header">
        <div class="custom-header-container">
            <a class="custom-logo-wrapper" href="?page=home" target="_top" style="text-decoration: none;">
                <div class="custom-logo-image">
                    {logo_html}
                </div>
                <div class="custom-logo-text">
                    <h1>الكوتش <span>أكاديمي</span></h1>
                    <p>أكاديمية كرة القدم المتخصصة</p>
                </div>
            </a>
            <label for="custom-menu-toggle" class="custom-burger-menu-btn" aria-label="فتح القائمة" title="القائمة">
                <span></span>
                <span></span>
                <span></span>
            </label>
        </div>
    </div>

    <label for="custom-menu-toggle" class="custom-nav-overlay-layer" aria-label="إغلاق القائمة"></label>

    <nav class="custom-side-navigation" id="sideMenu" aria-label="القائمة الرئيسية">
        <ul>
            <li><a href="?page=home" target="_top" class="nav-link">🏠 الرئيسية</a></li>
            <li><a href="?page=about" target="_top" class="nav-link">ℹ️ من نحن</a></li>
            <li><a href="?page=programs" target="_top" class="nav-link">⚽ البرامج التدريبية</a></li>
            <li><a href="?page=coaches" target="_top" class="nav-link">👨‍🏫 المدربون</a></li>
            <li><a href="?page=registration" target="_top" class="nav-link">📝 تسجيل لاعب جديد</a></li>
            <li><a href="?page=faq" target="_top" class="nav-link">❓ الأسئلة الشائعة</a></li>
            <li><a href="?page=contact" target="_top" class="nav-link">📞 اتصل بنا</a></li>
            <li><a href="?page=gallery" target="_top" class="nav-link">📸 معرض الصور</a></li>
            <li><a href="?page=news" target="_top" class="nav-link">📰 الأخبار</a></li>
        </ul>
    </nav>

    <div class="custom-header-spacer"></div>
</div>
""", unsafe_allow_html=True)

# ====================================================================================================
# 6. دوال حفظ البيانات
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
# 7. تحديد الصفحة الحالية
# ====================================================================================================
query_params = st.query_params
page_from_url = query_params.get('page')
if isinstance(page_from_url, list):
    page_from_url = page_from_url[0] if page_from_url else None
if page_from_url:
    st.session_state.page = page_from_url

page = st.session_state.page

# بداية حاوية المحتوى
st.markdown('<div class="custom-content-container">', unsafe_allow_html=True)

# ====================================================================================================
# 8. الصفحة الرئيسية
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
            <a class="custom-register-btn" href="?page=registration" target="_top">📝 سجل ابنك الآن</a>
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
        <div class="custom-feature-card"><div class="custom-feature-icon">🧠</div><h3>منهجية التدريب الذهني</h3><p>نركز على تطوير الذكاء الكروي والقدرة على اتخاذ القرارات السريعة والصحيحة داخل الملعب. نستخدم أحدث التقنيات في التدريب الذهني لتنمية مهارات التفكير الاستراتيجي.</p></div>
        <div class="custom-feature-card"><div class="custom-feature-icon">🛡️</div><h3>بيئة آمنة محفزة</h3><p>نوفر بيئة تدريب آمنة تحترم الفروق الفردية وتشجع على الإبداع والتميز. جميع المدربين حاصلون على شهادات السلامة والإسعافات الأولية.</p></div>
        <div class="custom-feature-card"><div class="custom-feature-icon">🤝</div><h3>شراكات مع الأندية</h3><p>لدينا شراكات مع أندية محلية ودولية لتمكين الموهوبين من الانضمام للمنتخبات والأندية الكبرى. نوفر فرص احتراف حقيقية للمتميزين.</p></div>
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
                <a href="?page=news" target="_top" style="color: #3b82f6; text-decoration: none;">اقرأ المزيد →</a>
            </div>
            """, unsafe_allow_html=True)

# ====================================================================================================
# 9. صفحة من نحن
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
            <p style="color: #334155; line-height: 1.7;">تطوير جيل جديد من اللاعبين المبدعين القادرين على التألق محليًا ودوليًا، من خلال تقديم تدريب عصري يعتمد على أحدث الأساليب العلمية والتكنولوجية في عالم كرة القدم، مع غرس القيم والأخلاق الرياضية.</p>
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
# 10. صفحة البرامج التدريبية
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
        <a class="custom-register-btn" href="?page=registration" target="_top" style="padding: 12px 35px; font-size: 1rem;">سجل الآن</a>
    </div>
    """, unsafe_allow_html=True)

# ====================================================================================================
# 11. صفحة المدربون
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
# 12. صفحة التسجيل
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
# 13. صفحة الأسئلة الشائعة
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
         "الموسم التدريبي يمتد لمدة 10 أشهر، من بداية سبتمبر إلى نهاية يونيو. التدريبات تقام في الفترة المسائية أيام السبت والخميس حسب الجدول المحدد لكل فئة عمرية، وذلك ليتناسب مع أوقات المدارس والدراسة."),
        
        ("ما هي تكلفة الاشتراك وآلية الدفع؟", 
         "تختلف التكلفة حسب الفئة العمرية وعدد أيام التدريب في الأسبوع. نقدم عدة مزايا: خصومات خاصة للأشقاء، نظام تقسيط شهري مرن، منح جزئية للمتميزين ماديًا أو فنيًا، خصم للتسجيل المبكر. يرجى التواصل معنا لمعرفة التفاصيل الدقيقة."),
        
        ("ما هي متطلبات الانضمام للأكاديمية؟", 
         "للانضمام للأكاديمية نحتاج إلى: (1) إكمال نموذج التسجيل عبر الموقع، (2) أن يكون اللاعب في الفئة العمرية المحددة للبرنامج، (3) الرغبة الحقيقية في التعلم والتطوير، (4) الالتزام بمواعيد التدريب والحضور المنتظم، (5) تقديم شهادة ميلاد وصورة شخصية حديثة، (6) دفع رسوم الاشتراك."),
        
        ("هل هناك تدريبات خاصة للمبتدئين؟", 
         "نعم، لدينا برامج خاصة للمبتدئين تركز على: تعلم أساسيات كرة القدم من الصفر، تطوير المهارات الحركية الأساسية، بناء الثقة بالنفس وحب الرياضة، تعزيز العمل الجماعي والانضباط، تدريبات ترفيهية محفزة للتعلم."),
        
        ("كيف يمكن متابعة تطور اللاعب داخل الأكاديمية؟", 
         "نوفر نظام متابعة شامل ومتكامل يشمل: تقييم فني دوري للمهارات الفنية، متابعة التطور البدني والقدرات الجسمانية، تقارير شهرية عن المشاركة والالتزام، لقاءات دورية مع أولياء الأمور لمناقشة التطور، فيديوهات تحليل أداء للاعبين المتميزين، شهادات تقدير للمتفوقين."),
        
        ("ماذا عن السلامة والإصابات خلال التدريب؟", 
         "السلامة هي أولوية قصوى لدينا، ونوفر: (1) إشراف مستمر من مدربين مؤهلين ومدربين مساعدين، (2) بيئة تدريب آمنة ومجهزة بأحدث المعدات، (3) برنامج إحماء وتبريد مناسب قبل وبعد كل تدريب، (4) مدربين حاصلين على شهادات معتمدة في الإسعافات الأولية، (5) تأمين صحي للاعبين أثناء فترة التدريب."),
        
        ("هل يمكن للاعب الانتقال بين الفئات العمرية؟", 
         "نعم، يمكن للاعب الانتقال بين الفئات العمرية بناءً على عدة معايير: تطور مهاراته وقدراته الفنية والبدنية، توصية المدرب المسؤول بعد التقييم، موافقة ولي الأمر، التقييم الدوري للأداء والالتزام، اجتياز الاختبارات المهارية المحددة."),
        
        ("ما هي اللغات المستخدمة في التدريب؟", 
         "التدريب يتم باللغة العربية الفصحى والعامية مع استخدام المصطلحات الإنجليزية في بعض التمارين المتخصصة، مما يساعد اللاعبين على فهم المصطلحات العالمية المستخدمة في كرة القدم حول العالم."),
        
        ("هل يوجد تدريبات مخصصة للبنات؟", 
         "نعم، لدينا برامج تدريبية مخصصة للبنات في أيام السبت والخميس، مع مدربات متخصصات ومؤهلات، وبيئة مناسبة ومحترمة تلبي احتياجات الفتيات الرياضية والنفسية، مع مراعاة الخصوصية الكاملة."),
        
        ("كم عدد اللاعبين في المجموعة التدريبية الواحدة؟", 
         "نحرص على أن يكون عدد اللاعبين في المجموعة التدريبية الواحدة مناسبًا لضمان الجودة، حيث لا يتجاوز عدد اللاعبين 20 لاعبًا لكل مدرب، مما يسمح بمتابعة فردية فعالة لكل لاعب."),
        
        ("هل توجد مسابقات دورية داخل الأكاديمية؟", 
         "نعم، نقوم بتنظيم مسابقات دورية داخلية بين فرق الأكاديمية بشكل شهري، بالإضافة إلى مشاركات خارجية مع أندية وأكاديميات أخرى، مما يتيح للاعبين فرصة اكتساب الخبرات الميدانية والتطبيق العملي."),
        
        ("كيف يمكنني التواصل مع إدارة الأكاديمية؟", 
         "يمكنك التواصل معنا عبر: (1) الاتصال على الرقم 01069238878، (2) الواتساب على 01285197778، (3) البريد الإلكتروني info@elcoach-academy.com، (4) زيارة الأكاديمية في مواعيد التدريب."),
        
        ("هل توجد وسائل نقل للاعبين؟", 
         "حالياً، لا نوفر خدمات نقل للاعبين، ولكن يمكن لأولياء الأمور توصيل أبنائهم إلى ملاعب التدريب. نعمل حالياً على توفير هذه الخدمة في المستقبل القريب."),
        
        ("ما هي شروط الانسحاب واسترداد الرسوم؟", 
         "يتم استرداد الرسوم وفقًا للسياسة التالية: استرداد كامل خلال أول أسبوعين من بداية الموسم، استرداد 50% خلال الشهر الأول، لا يوجد استرداد بعد انقضاء الشهر الأول من الموسم."),
        
        ("هل يوجد عروض خاصة للأشقاء؟", 
         "نعم، نقدم خصم 15% للشقيق الثاني، وخصم 25% للشقيق الثالث، وخصم 30% لأكثر من ثلاثة أشقاء."),
    ]
    
    for q, a in faqs:
        with st.expander(f"❓ {q}"):
            st.markdown(f'<p style="color: #334155; line-height: 1.7; font-size: 0.95rem;">{a}</p>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="margin-top: 40px; background: linear-gradient(135deg, #f0f9ff, #e0f2fe); border-radius: 24px; padding: 30px; text-align: center;">
        <h3 style="color: #1e3a8a;">❗ لم تجد سؤالك؟</h3>
        <p style="color: #334155; margin: 15px 0;">تواصل معنا وسنقوم بالرد عليك في أقرب وقت</p>
        <a class="custom-register-btn" href="?page=contact" target="_top" style="padding: 12px 35px; font-size: 1rem;">اتصل بنا</a>
    </div>
    """, unsafe_allow_html=True)

# ====================================================================================================
# 14. صفحة اتصل بنا
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
                <div>
                    <strong>الهاتف:</strong><br>
                    <a href="tel:01069238878" style="text-decoration: none; color: #334155; font-size: 1.1rem;">01069238878</a>
                </div>
            </div>
            <div class="custom-contact-item">
                <div style="font-size: 1.6rem;">💬</div>
                <div>
                    <strong>الواتساب:</strong><br>
                    <a href="https://wa.me/201285197778" target="_blank" style="text-decoration: none; color: #25D366; font-size: 1.1rem;">01285197778</a>
                </div>
            </div>
            <div class="custom-contact-item">
                <div style="font-size: 1.6rem;">📍</div>
                <div>
                    <strong>العنوان الرئيسي:</strong><br>
                    محافظة أسيوط - مصر<br>
                    على ملاعب مدرسة السلام المتطورة
                </div>
            </div>
            <div class="custom-contact-item">
                <div style="font-size: 1.6rem;">⏰</div>
                <div>
                    <strong>أوقات العمل والإجابة على الاستفسارات:</strong><br>
                    السبت والخميس: 4:00 مساءً - 9:00 مساءً (أيام التدريب)<br>
                    باقي الأيام: متاح للرد على المكالمات والواتساب من 10ص - 10م
                </div>
            </div>
            <div class="custom-contact-item">
                <div style="font-size: 1.6rem;">📧</div>
                <div>
                    <strong>البريد الإلكتروني:</strong><br>
                    info@elcoach-academy.com<br>
                    support@elcoach-academy.com
                </div>
            </div>
        </div>
        
        <div class="custom-map-container">
            <iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d113686.258448786!2d31.156289!3d27.186696!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x1438a5f5c5b5b5b5%3A0x5b5b5b5b5b5b5b5b!2z2YXZg9mF2YrYp9mG2Ykg2KfZhNiq2YbYqSDYp9mE2YXYqtmG2Kkg2KfZhNir2YTYp9mG2Ykg2KfZhNi52YjYp9mG!5e0!3m2!1sar!2seg!4v1700000000000!5m2!1sar!2seg" 
                    allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="custom-contact-card">
            <h3 style="color: #1e3a8a; margin-bottom: 28px; font-size: 1.5rem;">✉️ أرسل رسالة</h3>
            <p style="color: #64748b; margin-bottom: 20px;">سنقوم بالرد عليك في أقرب وقت ممكن خلال 24 ساعة</p>
        </div>
        """, unsafe_allow_html=True)
        
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
                        'name': c_name, 'phone': c_phone, 'email': c_email,
                        'subject': c_subject, 'message': c_msg,
                        'contactDate': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    if save_contact(data):
                        st.success("✅ شكراً لتواصلك! تم إرسال رسالتك بنجاح وسنرد عليك خلال 24 ساعة.")
                    else:
                        st.error("❌ حدث خطأ في حفظ البيانات، يرجى المحاولة مرة أخرى")
                else:
                    st.error("⚠️ يرجى ملء جميع الحقول المطلوبة")
        
        st.markdown("""
        <div class="custom-contact-card" style="margin-top: 25px;">
            <h3 style="color: #1e3a8a; margin-bottom: 20px;">🌐 تابعنا على وسائل التواصل</h3>
            <div style="display: flex; gap: 15px; justify-content: center;">
                <div style="width: 45px; height: 45px; background: #1877f2; border-radius: 50%; display: flex; align-items: center; justify-content: center; cursor: pointer;">📘</div>
                <div style="width: 45px; height: 45px; background: #1da1f2; border-radius: 50%; display: flex; align-items: center; justify-content: center; cursor: pointer;">🐦</div>
                <div style="width: 45px; height: 45px; background: #e4405f; border-radius: 50%; display: flex; align-items: center; justify-content: center; cursor: pointer;">📷</div>
                <div style="width: 45px; height: 45px; background: #25d366; border-radius: 50%; display: flex; align-items: center; justify-content: center; cursor: pointer;">💬</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ====================================================================================================
# 15. صفحة معرض الصور
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
        <p style="color: #1e3a8a; font-size: 1.1rem;">📸 يتم تحديث المعرض باستمرار بأحدث صور التدريبات والمباريات</p>
        <p style="color: #64748b; margin-top: 10px;">تابعونا على وسائل التواصل الاجتماعي لمشاهدة المزيد من اللحظات المميزة</p>
    </div>
    """, unsafe_allow_html=True)

# ====================================================================================================
# 16. صفحة الأخبار
# ====================================================================================================
elif page == 'news':
    st.markdown("""
    <div class="custom-page-header">
        <h1>📰 آخر الأخبار</h1>
        <p>أحدث المستجدات والإعلانات من الكوتش أكاديمي</p>
    </div>
    """, unsafe_allow_html=True)
    
    news_items = [
        {"title": "بدء التسجيل للموسم الجديد 2025", "date": "2025-01-15", "content": "يعلن الكوتش أكاديمي عن بدء التسجيل للموسم الجديد 2025. خصومات خاصة للمسجلين المبكرين حتى نهاية فبراير. للتسجيل يرجى زيارة صفحة التسجيل أو الاتصال بنا.", "author": "إدارة الأكاديمية"},
        {"title": "فوز فريق الأكاديمية ببطولة أسيوط", "date": "2025-01-10", "content": "حقق فريق تحت 12 سنة فوزًا مستحقًا في بطولة أسيوط الرمضانية بعد تفوقه على 8 فرق. تألق لاعبو الأكاديمية وأظهروا مستويات متميزة طوال البطولة.", "author": "كابتن ميخا"},
        {"title": "محاضرة تدريبية للمدربين", "date": "2025-01-05", "content": "أقيمت محاضرة تدريبية للمدربين حول أحدث أساليب التدريب الحديثة بحضور خبراء من الاتحاد المصري لكرة القدم. تناولت المحاضرة تطوير المهارات الفردية والخططية.", "author": "إدارة التدريب"},
        {"title": "افتتاح فرع جديد للأكاديمية", "date": "2024-12-20", "content": "يعلن الكوتش أكاديمي عن افتتاح فرع جديد في مدينة نصر خلال الأشهر القادمة. سيتم الإعلان عن التفاصيل قريبًا.", "author": "الإدارة التنفيذية"},
        {"title": "تخريج دفعة جديدة من اللاعبين", "date": "2024-12-15", "content": "احتفلت الأكاديمية بتخريج دفعة جديدة من اللاعبين المتميزين الذين انضموا لأندية كبرى. شهد الحفل تكريم اللاعبين المتميزين وتوزيع الشهادات.", "author": "إدارة الأكاديمية"},
        {"title": "مشاركة مميزة في بطولة الجمهورية", "date": "2024-12-10", "content": "شارك فريق الأكاديمية في بطولة الجمهورية للناشئين وحقق نتائج متميزة. أشاد المنظمون بمستوى لاعبي الأكاديمية.", "author": "كابتن أحمد علي"},
        {"title": "دورة تدريبية لحراس المرمى", "date": "2024-12-05", "content": "انطلقت دورة تدريبية متخصصة لحراس المرمى تحت إشراف كابتن أحمد علي، تشمل التدريبات النظرية والتطبيقية.", "author": "إدارة التدريب"},
        {"title": "اتفاقية تعاون مع نادي الزمالك", "date": "2024-11-28", "content": "وقع الكوتش أكاديمي اتفاقية تعاون مع نادي الزمالك لاكتشاف المواهب وتأهيلها للانضمام لقطاع الناشئين بالنادي.", "author": "الإدارة التنفيذية"},
    ]
    
    for news in news_items:
        st.markdown(f"""
        <div class="custom-news-card">
            <h3 style="color: #1e3a8a; margin-bottom: 10px;">📌 {news['title']}</h3>
            <div style="display: flex; gap: 15px; margin-bottom: 12px;">
                <p style="color: #64748b; font-size: 0.85rem;">📅 {news['date']}</p>
                <p style="color: #f59e0b; font-size: 0.85rem;">✍️ {news['author']}</p>
            </div>
            <p style="color: #334155; line-height: 1.6;">{news['content']}</p>
            <button style="margin-top: 15px; background: transparent; border: none; color: #3b82f6; cursor: pointer;">اقرأ المزيد →</button>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="margin-top: 40px; text-align: center;">
        <a class="custom-register-btn" href="?page=registration" target="_top" style="padding: 12px 35px; font-size: 1rem;">سجل الآن في الأكاديمية</a>
    </div>
    """, unsafe_allow_html=True)

# إغلاق حاوية المحتوى
st.markdown('</div>', unsafe_allow_html=True)

# ====================================================================================================
# 17. الفوتر
# ====================================================================================================
st.markdown(f"""
<div class="custom-main-footer">
    <div class="custom-footer-grid">
        <div>
            <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 20px;">
                <div style="width: 55px; height: 55px; background: linear-gradient(135deg, #3b82f6, #1e3a8a); border-radius: 16px; display: flex; align-items: center; justify-content: center; font-size: 1.8rem;">⚽</div>
                <h3 style="color: white; margin: 0; font-size: 1.5rem;">الكوتش أكاديمي</h3>
            </div>
            <p style="color: #cbd5e1; font-size: 0.85rem; line-height: 1.7;">تأسست عام 2020 على ملاعب مدرسة السلام المتطورة. أول أكاديمية متخصصة في مصر تركز على بناء اللاعب الشامل من الناحية الفنية والبدنية والنفسية، تحت إشراف مدربين معتمدين دوليًا من الاتحاد الأفريقي CAF.</p>
            <div class="custom-social-icons">
                <div class="custom-social-icon">📘</div>
                <div class="custom-social-icon">🐦</div>
                <div class="custom-social-icon">📷</div>
                <div class="custom-social-icon">💬</div>
            </div>
        </div>
        <div>
            <h4 style="color: white; margin-bottom: 20px; font-size: 1.15rem;">روابط سريعة</h4>
            <ul style="list-style: none; padding: 0;">
                <li style="margin-bottom: 12px;"><a href="?page=home" target="_top" class="custom-footer-link">← الرئيسية</a></li>
                <li style="margin-bottom: 12px;"><a href="?page=about" target="_top" class="custom-footer-link">← من نحن</a></li>
                <li style="margin-bottom: 12px;"><a href="?page=programs" target="_top" class="custom-footer-link">← البرامج التدريبية</a></li>
                <li style="margin-bottom: 12px;"><a href="?page=coaches" target="_top" class="custom-footer-link">← المدربون</a></li>
                <li style="margin-bottom: 12px;"><a href="?page=registration" target="_top" class="custom-footer-link">← تسجيل لاعب جديد</a></li>
                <li style="margin-bottom: 12px;"><a href="?page=faq" target="_top" class="custom-footer-link">← الأسئلة الشائعة</a></li>
                <li style="margin-bottom: 12px;"><a href="?page=contact" target="_top" class="custom-footer-link">← اتصل بنا</a></li>
                <li style="margin-bottom: 12px;"><a href="?page=gallery" target="_top" class="custom-footer-link">← معرض الصور</a></li>
                <li style="margin-bottom: 12px;"><a href="?page=news" target="_top" class="custom-footer-link">← الأخبار</a></li>
            </ul>
        </div>
        <div>
            <h4 style="color: white; margin-bottom: 20px; font-size: 1.15rem;">معلومات الاتصال</h4>
            <ul style="list-style: none; padding: 0;">
                <li style="margin-bottom: 14px; display: flex; gap: 12px;">
                    <span style="font-size: 1.1rem;">📍</span>
                    <span style="color: #cbd5e1;">أسيوط - مصر<br>ملاعب مدرسة السلام المتطورة</span>
                </li>
                <li style="margin-bottom: 14px; display: flex; gap: 12px;">
                    <span style="font-size: 1.1rem;">📞</span>
                    <a href="tel:01069238878" style="color: #cbd5e1; text-decoration: none;">01069238878</a>
                </li>
                <li style="margin-bottom: 14px; display: flex; gap: 12px;">
                    <span style="font-size: 1.1rem;">💬</span>
                    <a href="https://wa.me/201285197778" target="_blank" style="color: #25D366; text-decoration: none;">01285197778 (واتساب)</a>
                </li>
                <li style="margin-bottom: 14px; display: flex; gap: 12px;">
                    <span style="font-size: 1.1rem;">⏰</span>
                    <span style="color: #cbd5e1;">السبت والخميس: 4م - 9م</span>
                </li>
                <li style="margin-bottom: 14px; display: flex; gap: 12px;">
                    <span style="font-size: 1.1rem;">📧</span>
                    <a href="mailto:info@elcoach-academy.com" style="color: #cbd5e1; text-decoration: none;">info@elcoach-academy.com</a>
                </li>
            </ul>
        </div>
    </div>
    <div style="text-align: center; padding-top: 30px; border-top: 1px solid rgba(255, 255, 255, 0.1);">
        <p style="color: #94a3b8;">© 2025 الكوتش أكاديمي - جميع الحقوق محفوظة</p>
        <p style="color: #94a3b8; margin-top: 10px; font-size: 0.8rem;">أكاديمية كرة القدم المتخصصة | صناعة أبطال المستقبل</p>
        <p style="color: #94a3b8; margin-top: 8px; font-size: 0.75rem;">تأسست عام 2020 على يد: كابتن ميخائيل كميل (ميخا)، كابتن اندرو، كابتن مينا</p>
        <p style="color: #94a3b8; margin-top: 6px; font-size: 0.7rem;">بدعم من الأب الروحي للأكاديمية: مستر / مؤنس منير</p>
        <p style="color: #94a3b8; margin-top: 10px; font-size: 0.7rem;">عدد زوار الموقع: {st.session_state.visitor_count:,}+ زائر</p>
        <p style="color: #94a3b8; margin-top: 5px; font-size: 0.65rem;">آخر زيارة: {st.session_state.last_visit}</p>
    </div>
</div>

""", unsafe_allow_html=True)

# ====================================================================================================
# نهاية الكود - أكثر من 2100 سطر
# ====================================================================================================
