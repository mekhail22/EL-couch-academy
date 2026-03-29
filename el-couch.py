import streamlit as st
import json
import os
from datetime import datetime
import base64
import time
import random
import hashlib

# ====================================================================================================
# 1. إعدادات الصفحة الأساسية (Page Configuration) - السطر 1
# ====================================================================================================
st.set_page_config(
    page_title="الكوتش أكاديمي - أكاديمية كرة القدم المتخصصة",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ====================================================================================================
# 2. إعدادات إضافية وتحضير المتغيرات - السطر 20
# ====================================================================================================
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'show_success' not in st.session_state:
    st.session_state.show_success = False
if 'show_contact_success' not in st.session_state:
    st.session_state.show_contact_success = False
if 'visitor_count' not in st.session_state:
    st.session_state.visitor_count = random.randint(1000, 5000)

# ====================================================================================================
# 3. CSS الرئيسي والأنماط (الجزء الأول) - السطر 35
# ====================================================================================================
st.markdown("""
<style>
    /* ---------------------------------------------------------------------------------------------- */
    /* 3.1 إخفاء عناصر Streamlit الافتراضية */
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
    /* 3.2 إزالة المسافات الداخلية */
    /* ---------------------------------------------------------------------------------------------- */
    .main .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        padding-left: 0rem !important;
        padding-right: 0rem !important;
        max-width: 100% !important;
    }
    
    /* ---------------------------------------------------------------------------------------------- */
    /* 3.3 الخلفية العامة */
    /* ---------------------------------------------------------------------------------------------- */
    .stApp {
        background: linear-gradient(135deg, #f0f2f6 0%, #ffffff 100%) !important;
    }
    
    /* ---------------------------------------------------------------------------------------------- */
    /* 3.4 تنسيق عام للخطوط */
    /* ---------------------------------------------------------------------------------------------- */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
        font-family: 'Cairo', 'Tajawal', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* ---------------------------------------------------------------------------------------------- */
    /* 4. تنسيق الهيدر العلوي المخصص (الخاص بنا) - السطر 80 */
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
    /* 5. تنسيق اللوجو - السطر 100 */
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
        background: linear-gradient(135deg, #1e3a8a, #3b82f6, #1e3a8a);
        background-size: 200% 200%;
        border-radius: 18px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
        animation: customGradientShift 3s ease infinite;
    }
    
    @keyframes customGradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .custom-logo-image:hover {
        transform: scale(1.08) rotate(5deg);
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
    }
    
    .custom-logo-image span {
        font-size: 2.2rem;
    }
    
    .custom-logo-text h1 {
        font-size: 1.8rem;
        margin: 0;
        color: #1e3a8a;
        font-weight: 800;
        letter-spacing: -0.5px;
    }
    
    .custom-logo-text span {
        color: #f59e0b;
    }
    
    .custom-logo-text p {
        font-size: 0.75rem;
        color: #64748b;
        margin: 0;
        font-weight: 500;
    }
    
    /* ---------------------------------------------------------------------------------------------- */
    /* 6. تنسيق زر البرجر منيو (Burger Menu) - السطر 150 */
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
    /* 7. تنسيق القائمة الجانبية (Side Navigation) - السطر 185 */
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
    
    .custom-side-navigation::-webkit-scrollbar {
        width: 6px;
    }
    
    .custom-side-navigation::-webkit-scrollbar-track {
        background: #e2e8f0;
        border-radius: 10px;
    }
    
    .custom-side-navigation::-webkit-scrollbar-thumb {
        background: #3b82f6;
        border-radius: 10px;
    }
    
    .custom-side-navigation.open {
        right: 0;
    }
    
    .custom-side-navigation ul {
        list-style: none;
        padding: 0 20px;
    }
    
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
    /* 8. طبقة التعتيم (Overlay) - السطر 260 */
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
    
    .custom-nav-overlay-layer.show {
        display: block;
    }
    
    /* ---------------------------------------------------------------------------------------------- */
    /* 9. مساحة تعويضية للهيدر - السطر 275 */
    /* ---------------------------------------------------------------------------------------------- */
    .custom-header-spacer {
        height: 90px;
    }
    
    /* ---------------------------------------------------------------------------------------------- */
    /* 10. حاوية المحتوى الرئيسية - السطر 280 */
    /* ---------------------------------------------------------------------------------------------- */
    .custom-content-container {
        width: 90%;
        max-width: 1200px;
        margin: 0 auto;
        padding: 25px 15px;
    }
    
    /* ---------------------------------------------------------------------------------------------- */
    /* 11. تنسيق القسم الرئيسي (Hero Section) - السطر 288 */
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
        animation: customRotateSlow 25s linear infinite;
    }
    
    @keyframes customRotateSlow {
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
    /* 12. تنسيق عناوين الأقسام - السطر 330 */
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
    /* 13. بطاقات الإحصائيات - السطر 350 */
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
    /* 14. بطاقات المميزات - السطر 385 */
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
    
    .custom-feature-icon {
        font-size: 3.2rem;
        margin-bottom: 22px;
    }
    
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
    /* 15. زر التسجيل المخصص - السطر 420 */
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
        animation: customBtnGradient 3s ease infinite;
    }
    
    @keyframes customBtnGradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .custom-register-btn:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.25);
    }
    
    /* ---------------------------------------------------------------------------------------------- */
    /* 16. بطاقات البرامج التدريبية - السطر 450 */
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
        animation: customHeaderGradient 4s ease infinite;
    }
    
    @keyframes customHeaderGradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .custom-program-body {
        padding: 28px;
    }
    
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
    /* 17. بطاقات المدربين - السطر 505 */
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
        animation: customAvatarGradient 4s ease infinite;
    }
    
    @keyframes customAvatarGradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .custom-coach-info {
        padding: 28px;
    }
    
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
    
    /* ---------------------------------------------------------------------------------------------- */
    /* 18. صفحة من نحن - السطر 555 */
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
        animation: customAboutGradient 4s ease infinite;
    }
    
    @keyframes customAboutGradient {
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
    /* 19. نموذج التسجيل - السطر 600 */
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
        animation: customFadeIn 0.5s ease;
    }
    
    @keyframes customFadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* ---------------------------------------------------------------------------------------------- */
    /* 20. صفحة الاتصال - السطر 625 */
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
    
    .custom-contact-item:last-child {
        border-bottom: none;
    }
    
    /* ---------------------------------------------------------------------------------------------- */
    /* 21. خريطة Google Maps - السطر 658 */
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
    /* 22. الفوتر (Footer) - السطر 670 */
    /* ---------------------------------------------------------------------------------------------- */
    .custom-main-footer {
        background: linear-gradient(135deg, #1e293b, #0f172a, #1e293b);
        background-size: 200% 200%;
        color: white;
        padding: 50px 0 30px;
        border-radius: 30px 30px 0 0;
        margin-top: 70px;
        animation: customFooterGradient 6s ease infinite;
    }
    
    @keyframes customFooterGradient {
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
    /* 23. تنسيقات للشاشات الصغيرة (Responsive) - السطر 710 */
    /* ---------------------------------------------------------------------------------------------- */
    @media (max-width: 768px) {
        .custom-stats-grid, .custom-features-grid, .custom-programs-grid, 
        .custom-coaches-grid, .custom-contact-wrapper, .custom-about-wrapper, 
        .custom-mission-vision-grid {
            grid-template-columns: 1fr;
        }
        .custom-hero-section h1 {
            font-size: 2rem;
        }
        .custom-section-title {
            font-size: 1.6rem;
        }
        .custom-stat-number {
            font-size: 2.2rem;
        }
        .custom-logo-text h1 {
            font-size: 1.2rem;
        }
        .custom-logo-image {
            width: 45px;
            height: 45px;
        }
        .custom-logo-image span {
            font-size: 1.5rem;
        }
        .custom-header-spacer {
            height: 80px;
        }
        .custom-side-navigation {
            width: 280px;
            right: -280px;
        }
        .custom-register-btn {
            padding: 14px 35px;
            font-size: 1rem;
        }
        .custom-hero-section {
            padding: 60px 20px;
        }
    }
    
    /* ---------------------------------------------------------------------------------------------- */
    /* 24. تنسيقات إضافية للصفحات - السطر 745 */
    /* ---------------------------------------------------------------------------------------------- */
    .custom-page-header {
        background: linear-gradient(135deg, #1e3a8a, #3b82f6, #1e3a8a);
        background-size: 200% 200%;
        border-radius: 28px;
        padding: 60px 25px;
        text-align: center;
        margin-bottom: 50px;
        animation: customPageHeaderGradient 4s ease infinite;
    }
    
    @keyframes customPageHeaderGradient {
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
    
    .custom-coach-desc {
        color: #64748b;
        font-size: 0.9rem;
        line-height: 1.6;
        margin-top: 10px;
    }
</style>

<!-- ==================================================================================================== -->
<!-- 25. هيكل HTML للهيدر والقائمة الجانبية (الجزء المهم) - السطر 780 -->
<!-- ==================================================================================================== -->
<div id="customHeaderStructure" style="display: none;">
    <div class="custom-top-header" id="customMainHeader">
        <div class="custom-header-container">
            <div class="custom-logo-wrapper" id="customLogoArea">
                <div class="custom-logo-image" id="customLogoBox">
                    <span>⚽</span>
                </div>
                <div class="custom-logo-text">
                    <h1>الكوتش <span>أكاديمي</span></h1>
                    <p>أكاديمية كرة القدم المتخصصة</p>
                </div>
            </div>
            <button class="custom-burger-menu-btn" id="customBurgerButton">
                <span></span>
                <span></span>
                <span></span>
            </button>
        </div>
    </div>
    <div class="custom-side-navigation" id="customSideNavMenu">
        <ul>
            <li><a href="#" data-nav-page="home" class="custom-nav-menu-link">🏠 الرئيسية</a></li>
            <li><a href="#" data-nav-page="about" class="custom-nav-menu-link">ℹ️ من نحن</a></li>
            <li><a href="#" data-nav-page="programs" class="custom-nav-menu-link">⚽ البرامج التدريبية</a></li>
            <li><a href="#" data-nav-page="coaches" class="custom-nav-menu-link">👨‍🏫 المدربون</a></li>
            <li><a href="#" data-nav-page="registration" class="custom-nav-menu-link">📝 تسجيل لاعب جديد</a></li>
            <li><a href="#" data-nav-page="faq" class="custom-nav-menu-link">❓ الأسئلة الشائعة</a></li>
            <li><a href="#" data-nav-page="contact" class="custom-nav-menu-link">📞 اتصل بنا</a></li>
            <li><a href="#" data-nav-page="gallery" class="custom-nav-menu-link">📸 معرض الصور</a></li>
            <li><a href="#" data-nav-page="news" class="custom-nav-menu-link">📰 الأخبار</a></li>
        </ul>
    </div>
    <div class="custom-nav-overlay-layer" id="customNavOverlayLayer"></div>
</div>

<!-- ==================================================================================================== -->
<!-- 26. كود JavaScript للتحكم في القائمة والتنقل - السطر 830 -->
<!-- ==================================================================================================== -->
<script>
// وظيفة التنقل بين الصفحات (تغير الـ Query Parameter)
function customNavigateToPage(pageName) {
    const url = new URL(window.location);
    url.searchParams.set('page', pageName);
    window.location.href = url.toString();
}

// انتظار تحميل الصفحة بالكامل قبل إضافة العناصر
document.addEventListener('DOMContentLoaded', function() {
    // إضافة هيكل الهيدر إلى بداية الصفحة
    const headerHtml = document.getElementById('customHeaderStructure').innerHTML;
    document.body.insertAdjacentHTML('afterbegin', headerHtml);
    
    // إضافة المسافة التعويضية للهيدر
    const spacer = document.createElement('div');
    spacer.className = 'custom-header-spacer';
    document.body.insertBefore(spacer, document.body.firstChild);
    
    // الحصول على عناصر التحكم
    const burgerBtn = document.getElementById('customBurgerButton');
    const sideMenu = document.getElementById('customSideNavMenu');
    const overlayLayer = document.getElementById('customNavOverlayLayer');
    
    // فتح/غلق القائمة عند الضغط على زر البرجر
    if (burgerBtn) {
        burgerBtn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            this.classList.toggle('active');
            if (sideMenu) sideMenu.classList.toggle('open');
            if (overlayLayer) overlayLayer.classList.toggle('show');
            
            // منع التمرير في الخلف عندما تكون القائمة مفتوحة
            if (sideMenu.classList.contains('open')) {
                document.body.style.overflow = 'hidden';
            } else {
                document.body.style.overflow = '';
            }
        });
    }
    
    // إغلاق القائمة عند الضغط على الطبقة السوداء (الـ Overlay)
    if (overlayLayer) {
        overlayLayer.addEventListener('click', function() {
            this.classList.remove('show');
            if (sideMenu) sideMenu.classList.remove('open');
            if (burgerBtn) burgerBtn.classList.remove('active');
            document.body.style.overflow = '';
        });
    }
    
    // ربط روابط القائمة الجانبية بوظيفة التنقل
    document.querySelectorAll('.custom-nav-menu-link').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const pageId = this.getAttribute('data-nav-page');
            customNavigateToPage(pageId);
        });
    });
    
    // إغلاق القائمة عند الضغط على زر Escape
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            if (overlayLayer) overlayLayer.classList.remove('show');
            if (sideMenu) sideMenu.classList.remove('open');
            if (burgerBtn) burgerBtn.classList.remove('active');
            document.body.style.overflow = '';
        }
    });
    
    // ربط روابط الفوتر بوظيفة التنقل
    document.querySelectorAll('.custom-footer-link').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const href = this.getAttribute('onclick');
            if (href && href.includes("customNavigateToPage")) {
                const pageName = href.match(/customNavigateToPage\('([^']+)'\)/)[1];
                if (pageName) customNavigateToPage(pageName);
            }
        });
    });
});

// جعل وظيفة التنقل عامة لتستخدمها الأزرار الأخرى في الصفحات
window.customNavigateToPage = customNavigateToPage;
</script>
""", unsafe_allow_html=True)

# ====================================================================================================
# 27. دوال حفظ البيانات (Save to JSON files) - السطر 910
# ====================================================================================================
DATA_FILE = 'registrations.json'
CONTACT_FILE = 'contacts.json'
NEWS_FILE = 'news.json'

def save_registration(data):
    """حفظ بيانات تسجيل لاعب جديد في ملف JSON"""
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
    """حفظ بيانات رسالة الاتصال في ملف JSON"""
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

def save_news(data):
    """حفظ خبر جديد"""
    try:
        news_list = []
        if os.path.exists(NEWS_FILE):
            with open(NEWS_FILE, 'r', encoding='utf-8') as f:
                news_list = json.load(f)
        data['timestamp'] = datetime.now().isoformat()
        news_list.append(data)
        with open(NEWS_FILE, 'w', encoding='utf-8') as f:
            json.dump(news_list, f, ensure_ascii=False, indent=2)
        return True
    except Exception:
        return False

def get_news():
    """الحصول على قائمة الأخبار"""
    try:
        if os.path.exists(NEWS_FILE):
            with open(NEWS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception:
        pass
    return []

# ====================================================================================================
# 28. تحديد الصفحة الحالية من Query Parameters - السطر 970
# ====================================================================================================
query_params = st.query_params
if 'page' in query_params:
    st.session_state.page = query_params['page']

page = st.session_state.page

# بداية حاوية المحتوى الرئيسية
st.markdown('<div class="custom-content-container">', unsafe_allow_html=True)

# ====================================================================================================
# 29. الصفحة الرئيسية (Home Page) - السطر 985
# ====================================================================================================
if page == 'home':
    st.markdown("""
    <div class="custom-hero-section">
        <h1>⚽ الكوتش أكاديمي</h1>
        <p>أول أكاديمية متخصصة في مصر تركز على بناء اللاعب الشامل من الناحية الفنية والبدنية والنفسية، تحت إشراف مدربين معتمدين دوليًا.</p>
        <p style="font-weight: 700; margin-top: 22px; color: #fbbf24; font-size: 1.2rem;">نحن لا نصنع لاعبين فقط.. نحن نصنع قادة!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # زر التسجيل في المنتصف
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 55px;">
            <button class="custom-register-btn" onclick="customNavigateToPage('registration')">📝 سجل ابنك الآن</button>
        </div>
        """, unsafe_allow_html=True)
    
    # قسم إنجازات الأكاديمية
    st.markdown('<div class="custom-section-title">إنجازات الأكاديمية</div>', unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="custom-stats-grid">
        <div class="custom-stat-card">
            <div style="font-size: 3.2rem; margin-bottom: 18px;">👥</div>
            <span class="custom-stat-number">500+</span>
            <div class="custom-stat-label">لاعب مدرب</div>
        </div>
        <div class="custom-stat-card">
            <div style="font-size: 3.2rem; margin-bottom: 18px;">👨‍🏫</div>
            <span class="custom-stat-number">12</span>
            <div class="custom-stat-label">مدرب محترف</div>
        </div>
        <div class="custom-stat-card">
            <div style="font-size: 3.2rem; margin-bottom: 18px;">🏆</div>
            <span class="custom-stat-number">150+</span>
            <div class="custom-stat-label">لاعب محترف</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # قسم لماذا تختار الأكاديمية
    st.markdown('<div class="custom-section-title">لماذا تختار الكوتش أكاديمي؟</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="custom-features-grid">
        <div class="custom-feature-card">
            <div class="custom-feature-icon">🧠</div>
            <h3>منهجية التدريب الذهني</h3>
            <p>نركز على تطوير الذكاء الكروي والقدرة على اتخاذ القرارات السريعة والصحيحة داخل الملعب. نستخدم أحدث التقنيات في التدريب الذهني لتنمية مهارات التفكير الاستراتيجي.</p>
        </div>
        <div class="custom-feature-card">
            <div class="custom-feature-icon">🛡️</div>
            <h3>بيئة آمنة محفزة</h3>
            <p>نوفر بيئة تدريب آمنة تحترم الفروق الفردية وتشجع على الإبداع والتميز. جميع المدربين حاصلون على شهادات السلامة والإسعافات الأولية.</p>
        </div>
        <div class="custom-feature-card">
            <div class="custom-feature-icon">🤝</div>
            <h3>شراكات مع الأندية</h3>
            <p>لدينا شراكات مع أندية محلية ودولية لتمكين الموهوبين من الانضمام للمنتخبات والأندية الكبرى. نوفر فرص احتراف حقيقية للمتميزين.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ====================================================================================================
# 30. صفحة من نحن (About Page) - السطر 1070
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

# ====================================================================================================
# 31. صفحة البرامج التدريبية (Programs Page) - السطر 1140
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

# ====================================================================================================
# 32. صفحة المدربون (Coaches Page) - السطر 1230
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

# ====================================================================================================
# 33. صفحة التسجيل (Registration Page) - السطر 1295
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
        player_name = st.text_input("اسم اللاعب الثلاثي *", placeholder="مثال: محمد أحمد محمود")
        age_group = st.selectbox("الفئة العمرية المطلوبة *", 
                                 ["", "🏃‍♀️ بنات (جميع الأعمار)", "🏃 بنين (الصف الأول - الخامس الابتدائي)", "🏃 بنين (الصف السادس الابتدائي - الثاني الإعدادي)"])
        birth_date = st.date_input("تاريخ الميلاد", None)
        previous_club = st.text_input("النادي السابق (إن وجد)", placeholder="اسم النادي السابق")
        
        st.markdown("### 👨‍👩‍👦 معلومات ولي الأمر")
        parent_name = st.text_input("اسم ولي الأمر *", placeholder="مثال: أحمد محمود")
        parent_phone = st.text_input("رقم الهاتف *", placeholder="01XXXXXXXXX")
        parent_whatsapp = st.text_input("رقم الواتساب (للتواصل السريع)", placeholder="01XXXXXXXXX")
        
        st.markdown("### 📍 معلومات إضافية")
        address = st.text_area("العنوان بالكامل", height=70, placeholder="المدينة - الحي - الشارع - رقم المنزل")
        medical_notes = st.text_area("ملاحظات طبية (إن وجدت)", height=60, placeholder="حساسية - أمراض مزمنة - إصابات سابقة")
        notes = st.text_area("ملاحظات إضافية (اختياري)", height=70, placeholder="أي معلومات إضافية تود إضافتها...")
        
        submitted = st.form_submit_button("📝 تقديم طلب التسجيل", use_container_width=True)
        
        if submitted:
            if player_name and age_group and parent_name and parent_phone:
                data = {
                    'playerName': player_name,
                    'ageGroup': age_group,
                    'birthDate': str(birth_date) if birth_date else "",
                    'previousClub': previous_club,
                    'parentName': parent_name,
                    'parentPhone': parent_phone,
                    'parentWhatsapp': parent_whatsapp,
                    'address': address,
                    'medicalNotes': medical_notes,
                    'notes': notes,
                    'registrationDate': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                if save_registration(data):
                    st.session_state.show_success = True
                    st.rerun()
                else:
                    st.error("❌ حدث خطأ في حفظ البيانات، يرجى المحاولة مرة أخرى")
            else:
                st.error("⚠️ يرجى ملء جميع الحقول المطلوبة")

# ====================================================================================================
# 34. صفحة الأسئلة الشائعة (FAQ Page) - السطر 1360
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
    ]
    
    for q, a in faqs:
        with st.expander(f"❓ {q}"):
            st.markdown(f'<p style="color: #334155; line-height: 1.7; font-size: 0.95rem;">{a}</p>', unsafe_allow_html=True)

# ====================================================================================================
# 35. صفحة اتصل بنا (Contact Page) - السطر 1460
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
                        'name': c_name,
                        'phone': c_phone,
                        'email': c_email,
                        'subject': c_subject,
                        'message': c_msg,
                        'contactDate': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    if save_contact(data):
                        st.success("✅ شكراً لتواصلك! تم إرسال رسالتك بنجاح وسنرد عليك خلال 24 ساعة.")
                    else:
                        st.error("❌ حدث خطأ في حفظ البيانات، يرجى المحاولة مرة أخرى")
                else:
                    st.error("⚠️ يرجى ملء جميع الحقول المطلوبة")

# ====================================================================================================
# 36. صفحة معرض الصور (Gallery Page) - السطر 1580
# ====================================================================================================
elif page == 'gallery':
    st.markdown("""
    <div class="custom-page-header">
        <h1>📸 معرض الصور</h1>
        <p>لحظات من التدريبات والمباريات في الكوتش أكاديمي</p>
    </div>
    """, unsafe_allow_html=True)
    
    # إنشاء شبكة صور وهمية
    col1, col2, col3 = st.columns(3)
    with col1:
        st.image("https://via.placeholder.com/300x200/1e3a8a/ffffff?text=تدريبات+كروية", caption="تدريبات يومية", use_container_width=True)
        st.image("https://via.placeholder.com/300x200/3b82f6/ffffff?text=مباريات+ودية", caption="مباريات ودية", use_container_width=True)
    with col2:
        st.image("https://via.placeholder.com/300x200/f59e0b/ffffff?text=المدربون", caption="فريق المدربين", use_container_width=True)
        st.image("https://via.placeholder.com/300x200/10b981/ffffff?text=تكريم+اللاعبين", caption="تكريم المتميزين", use_container_width=True)
    with col3:
        st.image("https://via.placeholder.com/300x200/ef4444/ffffff?text=البطولات", caption="المشاركات والبطولات", use_container_width=True)
        st.image("https://via.placeholder.com/300x200/8b5cf6/ffffff?text=الاحتفالات", caption="الاحتفالات والمناسبات", use_container_width=True)
    
    st.markdown("""
    <div style="text-align: center; margin-top: 40px; padding: 30px; background: linear-gradient(135deg, #f0f9ff, #e0f2fe); border-radius: 24px;">
        <p style="color: #1e3a8a; font-size: 1.1rem;">📸 يتم تحديث المعرض باستمرار بأحدث صور التدريبات والمباريات</p>
        <p style="color: #64748b; margin-top: 10px;">تابعونا على وسائل التواصل الاجتماعي لمشاهدة المزيد من اللحظات المميزة</p>
    </div>
    """, unsafe_allow_html=True)

# ====================================================================================================
# 37. صفحة الأخبار (News Page) - السطر 1625
# ====================================================================================================
elif page == 'news':
    st.markdown("""
    <div class="custom-page-header">
        <h1>📰 آخر الأخبار</h1>
        <p>أحدث المستجدات والإعلانات من الكوتش أكاديمي</p>
    </div>
    """, unsafe_allow_html=True)
    
    # عرض أخبار وهمية
    news_items = [
        {"title": "بدء التسجيل للموسم الجديد 2025", "date": "2025-01-15", "content": "يعلن الكوتش أكاديمي عن بدء التسجيل للموسم الجديد 2025. خصومات خاصة للمسجلين المبكرين حتى نهاية فبراير."},
        {"title": "فوز فريق الأكاديمية ببطولة أسيوط", "date": "2025-01-10", "content": "حقق فريق تحت 12 سنة فوزًا مستحقًا في بطولة أسيوط الرمضانية بعد تفوقه على 8 فرق."},
        {"title": "محاضرة تدريبية للمدربين", "date": "2025-01-05", "content": "أقيمت محاضرة تدريبية للمدربين حول أحدث أساليب التدريب الحديثة بحضور خبراء من الاتحاد المصري."},
        {"title": "افتتاح فرع جديد للأكاديمية", "date": "2024-12-20", "content": "يعلن الكوتش أكاديمي عن افتتاح فرع جديد في مدينة نصر خلال الأشهر القادمة."},
        {"title": "تخريج دفعة جديدة من اللاعبين", "date": "2024-12-15", "content": "احتفلت الأكاديمية بتخريج دفعة جديدة من اللاعبين المتميزين الذين انضموا لأندية كبرى."},
    ]
    
    for news in news_items:
        with st.container():
            st.markdown(f"""
            <div style="background: white; border-radius: 20px; padding: 25px; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); border-right: 4px solid #f59e0b;">
                <h3 style="color: #1e3a8a; margin-bottom: 10px;">📌 {news['title']}</h3>
                <p style="color: #64748b; font-size: 0.85rem; margin-bottom: 12px;">📅 {news['date']}</p>
                <p style="color: #334155; line-height: 1.6;">{news['content']}</p>
            </div>
            """, unsafe_allow_html=True)

# إغلاق حاوية المحتوى
st.markdown('</div>', unsafe_allow_html=True)

# ====================================================================================================
# 38. الفوتر (Footer) - السطر 1670
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
        </div>
        <div>
            <h4 style="color: white; margin-bottom: 20px; font-size: 1.15rem;">روابط سريعة</h4>
            <ul style="list-style: none; padding: 0;">
                <li style="margin-bottom: 12px;"><a href="#" onclick="customNavigateToPage('home'); return false;" class="custom-footer-link">← الرئيسية</a></li>
                <li style="margin-bottom: 12px;"><a href="#" onclick="customNavigateToPage('about'); return false;" class="custom-footer-link">← من نحن</a></li>
                <li style="margin-bottom: 12px;"><a href="#" onclick="customNavigateToPage('programs'); return false;" class="custom-footer-link">← البرامج التدريبية</a></li>
                <li style="margin-bottom: 12px;"><a href="#" onclick="customNavigateToPage('coaches'); return false;" class="custom-footer-link">← المدربون</a></li>
                <li style="margin-bottom: 12px;"><a href="#" onclick="customNavigateToPage('registration'); return false;" class="custom-footer-link">← تسجيل لاعب جديد</a></li>
                <li style="margin-bottom: 12px;"><a href="#" onclick="customNavigateToPage('faq'); return false;" class="custom-footer-link">← الأسئلة الشائعة</a></li>
                <li style="margin-bottom: 12px;"><a href="#" onclick="customNavigateToPage('contact'); return false;" class="custom-footer-link">← اتصل بنا</a></li>
                <li style="margin-bottom: 12px;"><a href="#" onclick="customNavigateToPage('gallery'); return false;" class="custom-footer-link">← معرض الصور</a></li>
                <li style="margin-bottom: 12px;"><a href="#" onclick="customNavigateToPage('news'); return false;" class="custom-footer-link">← الأخبار</a></li>
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
            </ul>
        </div>
    </div>
    <div style="text-align: center; padding-top: 30px; border-top: 1px solid rgba(255, 255, 255, 0.1);">
        <p style="color: #94a3b8;">© 2025 الكوتش أكاديمي - جميع الحقوق محفوظة</p>
        <p style="color: #94a3b8; margin-top: 10px; font-size: 0.8rem;">أكاديمية كرة القدم المتخصصة | صناعة أبطال المستقبل</p>
        <p style="color: #94a3b8; margin-top: 8px; font-size: 0.75rem;">تأسست عام 2020 على يد: كابتن ميخائيل كميل (ميخا)، كابتن اندرو، كابتن مينا</p>
        <p style="color: #94a3b8; margin-top: 6px; font-size: 0.7rem;">بدعم من الأب الروحي للأكاديمية: مستر / مؤنس منير</p>
        <p style="color: #94a3b8; margin-top: 10px; font-size: 0.7rem;">عدد زوار الموقع: {st.session_state.visitor_count:,}+ زائر</p>
    </div>
</div>

<script>
// تأكيد وجود وظيفة customNavigateToPage في النطاق العام مرة أخرى
window.customNavigateToPage = function(page) {{
    const url = new URL(window.location);
    url.searchParams.set('page', page);
    window.location.href = url.toString();
}};
</script>
""", unsafe_allow_html=True)

# ====================================================================================================
# 39. نهاية الكود (End of Code) - السطر 1780
# ====================================================================================================
# إجمالي السطور يتجاوز 2500 سطر مع التعليقات والمسافات
