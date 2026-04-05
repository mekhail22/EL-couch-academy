import streamlit as st
import os
import base64
import requests
from datetime import datetime


# ====================================================================================================
# Google Sheets Integration
# ====================================================================================================
def save_to_google_sheets(data_row):
    """Save a row of data to Google Sheets using gspread and a service account."""
    try:
        import gspread
        from google.oauth2.service_account import Credentials
        import json

        # قراءة البيانات من Streamlit Secrets
        try:
            service_account_info = json.dumps(st.secrets["google"]["service_account"])
            spreadsheet_id = st.secrets["google"]["spreadsheet_id"]
        except KeyError:
            return False, "❌ لم يتم العثور على بيانات جوجل في Secrets.\n\nأضف البيانات إلى .streamlit/secrets.toml"

        creds_dict = json.loads(service_account_info)
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]
        credentials = Credentials.from_service_account_info(creds_dict, scopes=scopes)
        gc = gspread.authorize(credentials)
        sheet = gc.open_by_key(spreadsheet_id).sheet1

        sheet.append_row(data_row, value_input_option="USER_ENTERED")
        return True, "✅ تم التسجيل بنجاح!"
    except json.JSONDecodeError:
        return False, "❌ خطأ: صيغة البيانات غير صحيحة في Secrets"
    except Exception as e:
        return False, f"❌ خطأ: {str(e)}"


# ====================================================================================================
# Telegram Integration
# ====================================================================================================
def send_telegram_message(text):
    """Send a message to a Telegram chat using Bot API."""
    try:
        # قراءة البيانات من Streamlit Secrets
        try:
            bot_token = st.secrets["telegram"]["bot_token"]
            chat_id = st.secrets["telegram"]["chat_id"]
        except KeyError:
            return False, "❌ لم يتم العثور على بيانات التلجرام في Secrets.\n\nأضف البيانات إلى .streamlit/secrets.toml"

        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
        resp = requests.post(url, json=payload, timeout=10)
        if resp.status_code == 200:
            return True, "✅ تم الإرسال بنجاح!"
        return False, f"❌ فشل الإرسال: {resp.text}"
    except Exception as e:
        return False, f"❌ خطأ: {str(e)}"


# ====================================================================================================
# Page Config
# ====================================================================================================
st.set_page_config(
    page_title="الكوتش أكاديمي - أكاديمية كرة القدم المتخصصة",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ====================================================================================================
# Session State
# ====================================================================================================
if "page" not in st.session_state:
    st.session_state.page = "home"
if "show_success" not in st.session_state:
    st.session_state.show_success = False
if "show_contact_success" not in st.session_state:
    st.session_state.show_contact_success = False
if "menu_open" not in st.session_state:
    st.session_state.menu_open = False
if "registration_submitted" not in st.session_state:
    st.session_state.registration_submitted = False

# ====================================================================================================
# Logo Base64
# ====================================================================================================
def get_image_base64(image_path):
    try:
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except Exception:
        return None

logo_base64 = get_image_base64("logo.jpg")

# ====================================================================================================
# Main CSS
# ====================================================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;600;700;800;900&display=swap');

/* ---- Hide Streamlit defaults ---- */
header[data-testid="stHeader"] { display: none !important; }
.stApp > header { display: none !important; }
#MainMenu { display: none !important; }
footer { display: none !important; }
.st-emotion-cache-18ni7ap { display: none !important; }
[data-testid="stSidebar"] { display: none !important; }
div[data-testid="stDecoration"] { display: none !important; }

/* ---- Reset ---- */
*, *::before, *::after {
    box-sizing: border-box;
    font-family: 'Cairo', 'Segoe UI', Tahoma, sans-serif;
}

.main .block-container {
    padding-top: 0 !important;
    padding-bottom: 0 !important;
    padding-left: 0 !important;
    padding-right: 0 !important;
    max-width: 100% !important;
}

.stApp {
    background: linear-gradient(135deg, #f0f4f8 0%, #ffffff 50%, #f8fafc 100%) !important;
    direction: rtl;
}

/* ---- Fixed Header ---- */
.ec-header {
    position: fixed;
    top: 0; left: 0; right: 0;
    background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
    box-shadow: 0 4px 30px rgba(0,0,0,0.08);
    z-index: 10000;
    padding: 14px 0;
    border-bottom: 3px solid #e2e8f0;
    backdrop-filter: blur(10px);
}
.ec-header-inner {
    width: 92%; max-width: 1250px; margin: 0 auto;
    display: flex; justify-content: space-between; align-items: center;
}
.ec-logo-wrap {
    display: flex; align-items: center; gap: 14px;
    text-decoration: none; color: inherit; cursor: pointer;
}
.ec-logo-img {
    width: 58px; height: 58px; border-radius: 16px;
    display: flex; align-items: center; justify-content: center;
    overflow: hidden; flex-shrink: 0;
    background: linear-gradient(135deg, #1e3a8a, #3b82f6);
    box-shadow: 0 6px 20px rgba(30,58,138,0.3);
    transition: all 0.3s ease;
}
.ec-logo-img img { width: 100%; height: 100%; object-fit: cover; }
.ec-logo-img span { font-size: 2rem; color: white; }
.ec-logo-wrap:hover .ec-logo-img {
    transform: scale(1.08) rotate(3deg);
    box-shadow: 0 10px 30px rgba(30,58,138,0.4);
}
.ec-logo-txt h1 {
    font-size: 1.7rem; margin: 0; color: #1e3a8a;
    font-weight: 900; line-height: 1.1;
}
.ec-logo-txt h1 span { color: #f59e0b; }
.ec-logo-txt p {
    font-size: 0.75rem; color: #64748b; margin: 3px 0 0; font-weight: 600;
}

/* ---- Menu Toggle (Pure CSS) ---- */
.ec-menu-toggle { display: none; }
.ec-menu-btn {
    display: inline-flex; align-items: center; gap: 10px;
    background: linear-gradient(135deg, #1e3a8a, #3b82f6);
    color: white; font-weight: 800; border-radius: 999px;
    padding: 12px 22px; cursor: pointer;
    box-shadow: 0 8px 25px rgba(59,130,246,0.2);
    transition: all 0.25s ease; user-select: none; font-size: 0.95rem;
}
.ec-menu-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 30px rgba(59,130,246,0.3);
}

/* ---- Overlay ---- */
.ec-overlay {
    position: fixed; inset: 0;
    background: rgba(15,23,42,0.55);
    z-index: 10001; display: none;
    backdrop-filter: blur(4px);
}
.ec-menu-toggle:checked ~ .ec-overlay { display: block; }

/* ---- Side Navigation ---- */
.ec-sidenav {
    position: fixed; top: 82px; right: 16px;
    width: 370px; max-width: calc(100vw - 32px);
    height: calc(100vh - 98px);
    background: linear-gradient(180deg, #ffffff, #f8fafc);
    box-shadow: -12px 0 50px rgba(15,23,42,0.18);
    z-index: 10002;
    transform: translateX(120%);
    transition: transform 0.35s cubic-bezier(0.4,0,0.2,1);
    padding: 18px 14px; overflow-y: auto;
    border-radius: 24px;
    border: 1px solid rgba(226,232,240,0.9);
}
.ec-menu-toggle:checked ~ .ec-sidenav { transform: translateX(0); }
.ec-sidenav::-webkit-scrollbar { width: 5px; }
.ec-sidenav::-webkit-scrollbar-track { background: #e2e8f0; border-radius: 10px; }
.ec-sidenav::-webkit-scrollbar-thumb { background: #3b82f6; border-radius: 10px; }

.ec-sidenav-header {
    display: flex; align-items: center; justify-content: space-between;
    padding: 8px 10px 16px; margin-bottom: 8px;
    border-bottom: 1px solid #e2e8f0;
}
.ec-sidenav-brand {
    display: flex; align-items: center; gap: 12px;
}
.ec-sidenav-logo {
    width: 50px; height: 50px; border-radius: 14px;
    background: linear-gradient(135deg, #1e3a8a, #3b82f6);
    display: flex; align-items: center; justify-content: center;
    overflow: hidden; flex-shrink: 0;
    box-shadow: 0 6px 16px rgba(59,130,246,0.2);
}
.ec-sidenav-logo img { width: 100%; height: 100%; object-fit: cover; }
.ec-sidenav-logo span { color: white; font-size: 1.6rem; }
.ec-sidenav-brand h2 { margin: 0; font-size: 1.15rem; color: #1e3a8a; font-weight: 800; }
.ec-sidenav-brand p { margin: 3px 0 0; color: #64748b; font-size: 0.75rem; font-weight: 600; }
.ec-close-btn {
    width: 40px; height: 40px; border-radius: 50%; border: none;
    display: inline-flex; align-items: center; justify-content: center;
    cursor: pointer; background: #f1f5f9; color: #0f172a;
    font-size: 1.8rem; text-decoration: none; user-select: none;
    transition: background 0.2s;
}
.ec-close-btn:hover { background: #e2e8f0; }

.ec-sidenav a {
    display: flex; align-items: center; gap: 14px;
    padding: 14px 18px; color: #1e293b; text-decoration: none;
    font-weight: 700; border-radius: 16px;
    transition: all 0.25s ease; cursor: pointer;
    font-size: 15px; margin: 6px 4px;
}
.ec-sidenav a:hover {
    background: linear-gradient(135deg, #eff6ff, #dbeafe);
    color: #1d4ed8; transform: translateX(-6px);
}

/* ---- Spacer ---- */
.ec-spacer { height: 96px; }

/* ---- Content Container ---- */
.ec-container {
    width: 90%; max-width: 1200px;
    margin: 0 auto; padding: 25px 15px;
}

/* ---- Hero Section ---- */
.ec-hero {
    background: linear-gradient(135deg, rgba(15,23,42,0.88), rgba(30,58,138,0.75)),
                url('https://images.unsplash.com/photo-1575361204480-aadea25e6e68?w=1600&q=80');
    background-size: cover; background-position: center;
    border-radius: 28px; padding: 100px 30px;
    text-align: center; margin-bottom: 55px;
    position: relative; overflow: hidden;
    box-shadow: 0 20px 60px rgba(0,0,0,0.2);
}
.ec-hero::before {
    content: ''; position: absolute;
    top: -50%; right: -50%; width: 200%; height: 200%;
    background: radial-gradient(circle, rgba(245,158,11,0.1) 0%, transparent 60%);
    animation: ec-rotate 30s linear infinite;
}
@keyframes ec-rotate { from{transform:rotate(0deg)} to{transform:rotate(360deg)} }

.ec-hero h1 {
    color: white; font-size: 3.5rem; margin: 0 0 18px;
    font-weight: 900; text-shadow: 2px 4px 12px rgba(0,0,0,0.4);
    position: relative; z-index: 1;
}
.ec-hero h1 span { color: #fbbf24; }
.ec-hero .ec-hero-desc {
    color: #e2e8f0; max-width: 700px; margin: 0 auto 12px;
    font-size: 1.15rem; line-height: 1.7; position: relative; z-index: 1;
}
.ec-hero .ec-hero-slogan {
    color: #fbbf24; font-weight: 800; font-size: 1.3rem;
    margin: 20px 0 30px; position: relative; z-index: 1;
    text-shadow: 1px 2px 6px rgba(0,0,0,0.3);
}
.ec-hero-btns {
    display: flex; justify-content: center; gap: 16px;
    flex-wrap: wrap; position: relative; z-index: 1;
}
.ec-btn {
    display: inline-flex; align-items: center; justify-content: center;
    padding: 16px 45px; border-radius: 60px; font-weight: 800;
    font-size: 1.15rem; text-decoration: none; cursor: pointer;
    transition: all 0.3s ease; border: none;
    box-shadow: 0 8px 25px rgba(0,0,0,0.2);
}
.ec-btn-gold {
    background: linear-gradient(135deg, #f59e0b, #d97706);
    color: white;
}
.ec-btn-gold:hover {
    transform: translateY(-4px);
    box-shadow: 0 14px 35px rgba(245,158,11,0.4);
}
.ec-btn-outline {
    background: rgba(255,255,255,0.15);
    color: white; border: 2px solid rgba(255,255,255,0.4);
    backdrop-filter: blur(4px);
}
.ec-btn-outline:hover {
    background: rgba(255,255,255,0.25);
    transform: translateY(-4px);
    box-shadow: 0 14px 35px rgba(255,255,255,0.15);
}

/* ---- Section Title ---- */
.ec-section-title {
    font-size: 2.2rem; font-weight: 900; color: #1e293b;
    text-align: center; margin-bottom: 45px;
    position: relative; padding-bottom: 18px;
}
.ec-section-title::after {
    content: ''; position: absolute;
    bottom: 0; right: 50%; transform: translateX(50%);
    width: 90px; height: 4px;
    background: linear-gradient(90deg, #f59e0b, #fbbf24, #f59e0b);
    border-radius: 2px;
}

/* ---- Stats Grid ---- */
.ec-stats {
    display: grid; grid-template-columns: repeat(3, 1fr);
    gap: 28px; margin-bottom: 60px;
}
.ec-stat-card {
    background: white; padding: 38px 20px; border-radius: 22px;
    text-align: center; border: 1px solid #e2e8f0;
    box-shadow: 0 6px 22px rgba(0,0,0,0.06);
    transition: all 0.35s ease;
}
.ec-stat-card:hover {
    transform: translateY(-10px);
    box-shadow: 0 22px 50px rgba(0,0,0,0.12);
    border-color: #3b82f6;
}
.ec-stat-icon { font-size: 2.8rem; margin-bottom: 10px; }
.ec-stat-num {
    font-size: 3rem; font-weight: 900; color: #1e3a8a;
    display: block; line-height: 1;
}
.ec-stat-label {
    color: #64748b; margin-top: 10px; font-weight: 600; font-size: 1rem;
}

/* ---- Feature Cards ---- */
.ec-features {
    display: grid; grid-template-columns: repeat(3, 1fr);
    gap: 28px; margin-bottom: 60px;
}
.ec-feature-card {
    background: white; padding: 38px 26px; border-radius: 22px;
    text-align: center; transition: all 0.35s ease;
    box-shadow: 0 6px 22px rgba(0,0,0,0.06);
    border: 1px solid transparent;
}
.ec-feature-card:hover {
    transform: translateY(-10px);
    box-shadow: 0 22px 50px rgba(0,0,0,0.12);
    border-color: #f59e0b;
}
.ec-feature-icon { font-size: 3rem; margin-bottom: 18px; }
.ec-feature-card h3 {
    color: #1e3a8a; margin: 0 0 14px; font-size: 1.35rem; font-weight: 800;
}
.ec-feature-card p {
    color: #64748b; font-size: 0.93rem; line-height: 1.7; margin: 0;
}

/* ---- Page Header ---- */
.ec-page-header {
    background: linear-gradient(135deg, #1e3a8a, #3b82f6, #1e3a8a);
    background-size: 200% 200%;
    border-radius: 28px; padding: 60px 25px;
    text-align: center; margin-bottom: 45px;
    animation: ec-hdr-grad 5s ease infinite;
    box-shadow: 0 12px 40px rgba(30,58,138,0.2);
}
@keyframes ec-hdr-grad {
    0%{background-position:0% 50%}
    50%{background-position:100% 50%}
    100%{background-position:0% 50%}
}
.ec-page-header h1 {
    color: white; font-size: 2.4rem; margin: 0 0 12px; font-weight: 900;
}
.ec-page-header p { color: #e2e8f0; font-size: 1.05rem; margin: 0; }

/* ---- About Page ---- */
.ec-about-grid {
    display: grid; grid-template-columns: 1fr 1fr;
    gap: 40px; margin-bottom: 50px; align-items: center;
}
.ec-about-visual {
    background: linear-gradient(135deg, #3b82f6, #1e3a8a);
    border-radius: 28px; height: 360px;
    display: flex; align-items: center; justify-content: center;
    font-size: 6rem; color: white;
    box-shadow: 0 15px 40px rgba(30,58,138,0.25);
    position: relative; overflow: hidden;
}
.ec-about-visual::after {
    content: ''; position: absolute; inset: 0;
    background: radial-gradient(circle at 30% 70%, rgba(245,158,11,0.15), transparent 60%);
}
.ec-mv-grid {
    display: grid; grid-template-columns: 1fr 1fr;
    gap: 30px; margin-top: 35px;
}
.ec-mission-card, .ec-vision-card {
    padding: 32px; border-radius: 22px; transition: all 0.35s ease;
}
.ec-mission-card {
    background: linear-gradient(135deg, #f0f9ff, #e0f2fe);
    border-right: 5px solid #3b82f6;
}
.ec-vision-card {
    background: linear-gradient(135deg, #fffbeb, #fef3c7);
    border-right: 5px solid #f59e0b;
}
.ec-mission-card:hover, .ec-vision-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 18px 40px rgba(0,0,0,0.1);
}
.ec-mission-card h3, .ec-vision-card h3 {
    color: #1e3a8a; font-size: 1.5rem; margin: 0 0 14px; font-weight: 800;
}
.ec-mission-card p, .ec-vision-card p {
    color: #334155; line-height: 1.7; margin: 0 0 14px; font-size: 0.95rem;
}
.ec-mission-card ul, .ec-vision-card ul {
    margin: 0 20px 0 0; padding: 0; color: #334155; font-size: 0.93rem;
}
.ec-mission-card li, .ec-vision-card li { margin-bottom: 6px; }

/* ---- Programs ---- */
.ec-programs-grid {
    display: grid; grid-template-columns: repeat(2, 1fr);
    gap: 28px; margin-bottom: 50px;
}
.ec-program-card {
    background: white; border-radius: 22px; overflow: hidden;
    box-shadow: 0 6px 22px rgba(0,0,0,0.06);
    transition: all 0.35s ease; border: 1px solid #e2e8f0;
}
.ec-program-card:hover {
    transform: translateY(-10px);
    box-shadow: 0 22px 50px rgba(0,0,0,0.12);
}
.ec-program-hdr {
    height: 160px;
    background: linear-gradient(135deg, #3b82f6, #1e3a8a);
    display: flex; align-items: center; justify-content: center;
    font-size: 3.5rem; color: white;
}
.ec-program-body { padding: 26px; }
.ec-program-body h3 {
    color: #1e3a8a; margin: 0 0 16px; font-size: 1.4rem; font-weight: 800;
}
.ec-schedule-box {
    background: #f8fafc; padding: 18px; border-radius: 16px;
}
.ec-schedule-item {
    padding: 12px 0; border-bottom: 1px solid #e2e8f0;
    color: #334155; font-size: 0.95rem;
}
.ec-schedule-item:last-child { border-bottom: none; }

/* ---- Captains Page ---- */
.ec-lead-captain {
    max-width: 600px; margin: 0 auto 40px;
    background: white; border-radius: 24px; overflow: hidden;
    box-shadow: 0 12px 40px rgba(0,0,0,0.1);
    border: 2px solid #f59e0b;
    transition: all 0.35s ease;
}
.ec-lead-captain:hover {
    transform: translateY(-8px);
    box-shadow: 0 25px 60px rgba(0,0,0,0.15);
}
.ec-lead-avatar {
    height: 240px;
    background: linear-gradient(135deg, #f59e0b, #d97706, #f59e0b);
    background-size: 200% 200%;
    display: flex; align-items: center; justify-content: center;
    font-size: 5rem; color: white;
    animation: ec-hdr-grad 4s ease infinite;
    position: relative;
}
.ec-lead-info {
    padding: 30px; text-align: center;
}
.ec-lead-info h3 {
    color: #1e3a8a; font-size: 1.6rem; font-weight: 900; margin: 0 0 8px;
}
.ec-lead-info .ec-title-badge {
    display: inline-block; background: linear-gradient(135deg, #f59e0b, #d97706);
    color: white; padding: 4px 18px; border-radius: 20px;
    font-size: 0.85rem; font-weight: 700; margin-bottom: 16px;
}
.ec-lead-info .ec-qualifications {
    color: #475569; font-size: 0.93rem; line-height: 1.8;
    text-align: right;
}

.ec-captains-grid {
    display: grid; grid-template-columns: repeat(3, 1fr);
    gap: 28px; margin-bottom: 50px;
}
.ec-captain-card {
    background: white; border-radius: 22px; overflow: hidden;
    text-align: center; border: 1px solid #e2e8f0;
    box-shadow: 0 6px 22px rgba(0,0,0,0.06);
    transition: all 0.35s ease;
}
.ec-captain-card:hover {
    transform: translateY(-10px);
    box-shadow: 0 22px 50px rgba(0,0,0,0.12);
    border-color: #3b82f6;
}
.ec-captain-avatar {
    height: 200px;
    background: linear-gradient(135deg, #3b82f6, #1e3a8a);
    display: flex; align-items: center; justify-content: center;
    font-size: 4rem; color: white;
}
.ec-captain-info { padding: 24px; }
.ec-captain-info h3 {
    color: #1e3a8a; margin: 0 0 8px; font-size: 1.25rem; font-weight: 800;
}
.ec-captain-info .ec-coach-title {
    color: #3b82f6; font-weight: 700; margin-bottom: 12px; font-size: 0.9rem;
}
.ec-captain-info .ec-coach-desc {
    color: #64748b; font-size: 0.88rem; line-height: 1.7; text-align: right;
}

/* ---- Success / Error Messages ---- */
.ec-success-msg {
    background: linear-gradient(135deg, #10b981, #059669);
    color: white; padding: 20px; border-radius: 16px;
    margin-bottom: 25px; text-align: center;
    font-weight: 700; font-size: 1.05rem;
    animation: ec-fadeIn 0.5s ease;
    box-shadow: 0 6px 20px rgba(16,185,129,0.3);
}
.ec-error-msg {
    background: linear-gradient(135deg, #ef4444, #dc2626);
    color: white; padding: 20px; border-radius: 16px;
    margin-bottom: 25px; text-align: center;
    font-weight: 700; font-size: 1.05rem;
    animation: ec-fadeIn 0.5s ease;
}
@keyframes ec-fadeIn {
    from { opacity: 0; transform: translateY(-15px); }
    to { opacity: 1; transform: translateY(0); }
}

/* ---- Contact Page additions ---- */
.ec-contact-card {
    background: white; padding: 32px; border-radius: 22px;
    box-shadow: 0 6px 22px rgba(0,0,0,0.06);
    transition: all 0.35s ease; border: 1px solid #e2e8f0;
}
.ec-contact-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 18px 40px rgba(0,0,0,0.1);
}
.ec-contact-item {
    display: flex; align-items: center; gap: 16px;
    padding: 16px 0; border-bottom: 1px solid #f1f5f9;
}
.ec-contact-item:last-child { border-bottom: none; }
.ec-contact-item .ec-icon {
    font-size: 1.6rem; width: 45px; height: 45px;
    background: #f0f9ff; border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
}
.ec-map-container {
    margin-top: 25px;
    border-radius: 18px;
    overflow: hidden;
    box-shadow: 0 6px 22px rgba(0,0,0,0.1);
}
.ec-map-container iframe {
    width: 100%;
    height: 280px;
    border: 0;
}
.ec-whatsapp-btn {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    background: #25D366;
    color: white;
    padding: 12px 25px;
    border-radius: 50px;
    text-decoration: none;
    font-weight: 700;
    margin-top: 15px;
    transition: all 0.3s ease;
}
.ec-whatsapp-btn:hover {
    background: #128C7E;
    transform: scale(1.03);
}

/* ---- News Cards ---- */
.ec-news-card {
    background: white; border-radius: 20px; padding: 28px;
    margin-bottom: 20px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.05);
    border-right: 4px solid #f59e0b;
    transition: all 0.3s ease;
}
.ec-news-card:hover {
    transform: translateX(-8px);
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}
.ec-news-card h3 {
    color: #1e3a8a; font-size: 1.2rem; margin: 0 0 8px; font-weight: 800;
}
.ec-news-card .ec-news-date {
    color: #94a3b8; font-size: 0.82rem; margin-bottom: 10px;
}
.ec-news-card p {
    color: #475569; font-size: 0.93rem; line-height: 1.7; margin: 0;
}

/* ---- FAQ ---- */
.ec-faq-card {
    background: white; border-radius: 20px; padding: 28px;
    margin-bottom: 16px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.05);
    border: 1px solid #e2e8f0;
    transition: all 0.3s ease;
}
.ec-faq-card:hover {
    box-shadow: 0 10px 30px rgba(0,0,0,0.08);
    border-color: #3b82f6;
}
.ec-faq-card h4 {
    color: #1e3a8a; font-size: 1.1rem; margin: 0 0 12px;
    font-weight: 800; display: flex; align-items: center; gap: 10px;
}
.ec-faq-card p {
    color: #475569; font-size: 0.93rem; line-height: 1.8; margin: 0;
    padding-right: 32px;
}

/* ---- Footer ---- */
.ec-footer {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    color: white; padding: 50px 0 30px;
    border-radius: 28px 28px 0 0; margin-top: 60px;
}
.ec-footer-inner {
    width: 90%; max-width: 1200px; margin: 0 auto;
    display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    gap: 35px; margin-bottom: 35px;
}
.ec-footer h4 {
    color: #f59e0b; font-size: 1.15rem; margin: 0 0 16px; font-weight: 800;
}
.ec-footer p, .ec-footer li {
    color: #cbd5e1; font-size: 0.9rem; line-height: 1.7;
}
.ec-footer ul { list-style: none; padding: 0; margin: 0; }
.ec-footer li { margin-bottom: 8px; }
.ec-footer a {
    color: #cbd5e1; text-decoration: none; transition: color 0.2s;
}
.ec-footer a:hover { color: #f59e0b; }
.ec-footer-bottom {
    border-top: 1px solid rgba(255,255,255,0.1);
    padding-top: 20px; text-align: center;
    color: #64748b; font-size: 0.82rem;
    width: 90%; max-width: 1200px; margin: 0 auto;
}

/* ---- Info Banner ---- */
.ec-info-banner {
    background: linear-gradient(135deg, #1e3a8a, #3b82f6);
    border-radius: 24px; padding: 35px; text-align: center;
    color: white; margin-top: 40px;
    box-shadow: 0 12px 35px rgba(30,58,138,0.2);
}
.ec-info-banner h3 { font-size: 1.7rem; margin: 0 0 12px; font-weight: 900; }
.ec-info-banner p { margin: 0 0 20px; color: #e2e8f0; }
.ec-info-banner .ec-banner-stats {
    display: flex; justify-content: center; gap: 30px;
    flex-wrap: wrap; margin-top: 20px;
}
.ec-info-banner .ec-banner-stat {
    text-align: center;
}
.ec-info-banner .ec-banner-stat span {
    display: block; font-size: 1.6rem; font-weight: 900;
}

/* ---- Responsive ---- */
@media (max-width: 768px) {
    .ec-stats, .ec-features, .ec-programs-grid,
    .ec-captains-grid, .ec-about-grid,
    .ec-mv-grid {
        grid-template-columns: 1fr;
    }
    .ec-hero h1 { font-size: 2.2rem; }
    .ec-hero { padding: 70px 20px; }
    .ec-section-title { font-size: 1.6rem; }
    .ec-stat-num { font-size: 2.2rem; }
    .ec-logo-txt h1 { font-size: 1.2rem; }
    .ec-logo-img { width: 46px; height: 46px; }
    .ec-spacer { height: 84px; }
    .ec-sidenav {
        top: 72px; right: 8px;
        width: min(92vw, 380px);
        height: calc(100vh - 84px);
    }
    .ec-page-header h1 { font-size: 1.8rem; }
    .ec-btn { padding: 14px 32px; font-size: 1rem; }
    .ec-lead-captain { margin: 0 auto 30px; }
    .ec-info-banner .ec-banner-stats { gap: 16px; }
}
</style>
""", unsafe_allow_html=True)


# ====================================================================================================
# Helper function to generate navigation link (same tab)
# ====================================================================================================
def nav_link(text, page_name, icon=""):
    # Use target="_self" to ensure same tab
    return f'<a href="?page={page_name}" target="_self">{icon} {text}</a>'


# ====================================================================================================
# Header + Side Navigation
# ====================================================================================================
logo_html = ""
if logo_base64:
    logo_html = f'<img src="data:image/jpeg;base64,{logo_base64}" alt="Logo">'
else:
    logo_html = '<span>⚽</span>'

# Build header and side nav using the nav_link helper
sidenav_links = f"""
<nav class="ec-sidenav">
    <div class="ec-sidenav-header">
        <div class="ec-sidenav-brand">
            <div class="ec-sidenav-logo">{logo_html}</div>
            <div>
                <h2>الكوتش أكاديمي</h2>
                <p>القائمة الرئيسية</p>
            </div>
        </div>
        <label for="ec-menu-chk" class="ec-close-btn">&times;</label>
    </div>
    {nav_link("🏠 الرئيسية", "home")}
    {nav_link("ℹ️ من نحن", "about")}
    {nav_link("⚽ البرامج التدريبية", "programs")}
    {nav_link("👨‍🏫 صفحة الكباتن", "captains")}
    {nav_link("📝 سجل لاعب جديد", "registration")}
    {nav_link("❓ الأسئلة الشائعة", "faq")}
    {nav_link("📞 اتصل بنا", "contact")}
    {nav_link("📰 الأخبار", "news")}
</nav>
"""

header_html = f"""
<div class="ec-header">
    <div class="ec-header-inner">
        <a href="?page=home" target="_self" class="ec-logo-wrap">
            <div class="ec-logo-img">{logo_html}</div>
            <div class="ec-logo-txt">
                <h1>الكوتش <span>أكاديمي</span></h1>
                <p>أكاديمية كرة القدم المتخصصة</p>
            </div>
        </a>
        <label for="ec-menu-chk" class="ec-menu-btn">☰ القائمة</label>
    </div>
</div>

<input type="checkbox" id="ec-menu-chk" class="ec-menu-toggle" />

<label for="ec-menu-chk" class="ec-overlay"></label>

{sidenav_links}

<div class="ec-spacer"></div>
"""

st.markdown(header_html, unsafe_allow_html=True)

# ====================================================================================================
# Page Routing
# ====================================================================================================
query_page = st.query_params.get("page", "")
if isinstance(query_page, list):
    query_page = query_page[0] if query_page else ""
if query_page:
    st.session_state.page = query_page

page = st.session_state.page
if page == "coaches":
    page = "captains"
st.session_state.page = page

st.markdown('<div class="ec-container">', unsafe_allow_html=True)

# ====================================================================================================
# HOME PAGE
# ====================================================================================================
if page == "home":
    st.markdown("""
    <div class="ec-hero">
        <h1>⚽ الكوتش <span>أكاديمي</span></h1>
        <p class="ec-hero-desc">
            أول أكاديمية متخصصة تركز على بناء اللاعب الشامل من الناحية الفنية والبدنية والنفسية والذهنية،
            تحت إشراف مدربين معتمدين دوليًا.
        </p>
        <p class="ec-hero-slogan">نحن لا نصنع لاعبين فقط.. نحن نصنع قادة!</p>
        <div class="ec-hero-btns">
            <a href="?page=registration" target="_self" class="ec-btn ec-btn-gold">📝 سجل الآن</a>
            <a href="?page=contact" target="_self" class="ec-btn ec-btn-outline">📞 اتصل بنا</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="ec-section-title">إنجازات الأكاديمية</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="ec-stats">
        <div class="ec-stat-card">
            <div class="ec-stat-icon">👥</div>
            <span class="ec-stat-num">500+</span>
            <div class="ec-stat-label">لاعب مُدرَّب</div>
        </div>
        <div class="ec-stat-card">
            <div class="ec-stat-icon">👨‍🏫</div>
            <span class="ec-stat-num">12</span>
            <div class="ec-stat-label">مدرب محترف</div>
        </div>
        <div class="ec-stat-card">
            <div class="ec-stat-icon">🏆</div>
            <span class="ec-stat-num">150+</span>
            <div class="ec-stat-label">لاعب محترف</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="ec-section-title">لماذا تختار الكوتش أكاديمي؟</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="ec-features">
        <div class="ec-feature-card">
            <div class="ec-feature-icon">🧠</div>
            <h3>التدريب الذهني</h3>
            <p>نركز على تطوير الذكاء الكروي والقدرة على اتخاذ القرارات السريعة والصحيحة داخل الملعب، باستخدام أحدث التقنيات في التدريب الذهني.</p>
        </div>
        <div class="ec-feature-card">
            <div class="ec-feature-icon">🛡️</div>
            <h3>بيئة آمنة محفزة</h3>
            <p>نوفر بيئة تدريب آمنة تحترم الفروق الفردية وتشجع على الإبداع والتميز. جميع مدربينا حاصلون على شهادات السلامة والإسعافات الأولية.</p>
        </div>
        <div class="ec-feature-card">
            <div class="ec-feature-icon">🤝</div>
            <h3>شراكات مع الأندية</h3>
            <p>لدينا شراكات مع أندية محلية ودولية لتمكين الموهوبين من الانضمام للمنتخبات والأندية الكبرى. نوفر فرص احتراف حقيقية.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ====================================================================================================
# ABOUT PAGE
# ====================================================================================================
elif page == "about":
    st.markdown("""
    <div class="ec-page-header">
        <h1>من نحن</h1>
        <p>الكوتش أكاديمي.. رؤية جديدة في عالم تدريب كرة القدم</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="ec-about-grid">
        <div class="ec-about-visual">⚽</div>
        <div>
            <h2 style="color:#1e3a8a; font-size:1.8rem; margin:0 0 18px; font-weight:900;">تأسيس الأكاديمية</h2>
            <p style="color:#334155; font-size:1rem; line-height:1.8;">
                تأسست الأكاديمية عام 2020 على يد نخبة من المدربين المتخصصين بهدف
                إنشاء مؤسسة رياضية متكاملة تُعنى ببناء اللاعب من جميع الجوانب.
            </p>
            <ul style="margin:16px 25px 0 0; color:#334155; font-size:0.95rem; line-height:2;">
                <li><strong>كابتن ميخائيل كميل رؤف (ميخا)</strong> - المدير الفني والمؤسس</li>
                <li><strong>كابتن أندرو</strong> - مدرب مهارات</li>
                <li><strong>كابتن مينا</strong> - مدرب لياقة بدنية</li>
            </ul>
            <p style="margin-top:18px; color:#334155;">
                📍 مكان التدريب: <strong>ملاعب مدرسة السلام المتطورة - أسيوط</strong>
            </p>
            <p style="margin-top:14px; font-weight:800; color:#1e3a8a; font-size:1.05rem;">
                بدعم من الأب الروحي للأكاديمية: مستر / مؤنس منير
            </p>
        </div>
    </div>

    <div class="ec-mv-grid">
        <div class="ec-mission-card">
            <h3>🎯 رسالتنا</h3>
            <p>تطوير جيل جديد من اللاعبين المبدعين القادرين على التألق محليًا ودوليًا، من خلال تقديم تدريب عصري يعتمد على أحدث الأساليب العلمية، مع غرس القيم والأخلاق الرياضية.</p>
            <ul>
                <li>تطوير المهارات الفنية الأساسية والمتقدمة</li>
                <li>بناء اللياقة البدنية المخصصة لكل لاعب</li>
                <li>تعزيز الذكاء الكروي والقدرات الذهنية</li>
                <li>غرس القيم الرياضية والسلوك القيادي</li>
            </ul>
        </div>
        <div class="ec-vision-card">
            <h3>👁️ رؤيتنا</h3>
            <p>أن نكون الوجهة الأولى لأي موهبة كروية في مصر والوطن العربي، والجسر الذي يعبر من خلاله الموهوبون إلى العالمية.</p>
            <ul>
                <li>صناعة لاعبين مؤهلين للدوريات العالمية</li>
                <li>تطوير منهج تدريبي يُدرَّس في المعاهد الرياضية</li>
                <li>المساهمة في تطوير كرة القدم العربية</li>
                <li>بناء قاعدة بيانات للمواهب الكروية</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="ec-info-banner" style="margin-top:40px;">
        <h3>📊 أرقام وإحصائيات</h3>
        <div class="ec-banner-stats">
            <div class="ec-banner-stat"><span>🎓 4+</span>سنوات من التميز</div>
            <div class="ec-banner-stat"><span>👥 500+</span>لاعب تم تدريبهم</div>
            <div class="ec-banner-stat"><span>🏆 25+</span>بطولة محلية</div>
            <div class="ec-banner-stat"><span>⭐ 150+</span>لاعب محترف</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ====================================================================================================
# PROGRAMS PAGE
# ====================================================================================================
elif page == "programs":
    st.markdown("""
    <div class="ec-page-header">
        <h1>البرامج التدريبية</h1>
        <p>مواعيد تدريبية مصممة لكل فئة عمرية</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="ec-programs-grid">
        <div class="ec-program-card">
            <div class="ec-program-hdr">📅</div>
            <div class="ec-program-body">
                <h3>مواعيد تدريب السبت</h3>
                <div class="ec-schedule-box">
                    <div class="ec-schedule-item"><strong>🕔 ٥:٠٠ - ٦:٠٠ م</strong> ← 🏃‍♀️ بنات (جميع الأعمار)</div>
                    <div class="ec-schedule-item"><strong>🕕 ٦:٠٠ - ٧:٣٠ م</strong> ← 🏃 بنين (الصف الأول - الخامس الابتدائي)</div>
                    <div class="ec-schedule-item"><strong>🕢 ٧:٣٠ - ٩:٠٠ م</strong> ← 🏃 بنين (الصف السادس - الثاني الإعدادي)</div>
                    <div style="margin-top:14px; color:#64748b; font-size:0.88rem;">📍 ملاعب مدرسة السلام المتطورة - أسيوط</div>
                </div>
            </div>
        </div>
        <div class="ec-program-card">
            <div class="ec-program-hdr">📅</div>
            <div class="ec-program-body">
                <h3>مواعيد تدريب الخميس</h3>
                <div class="ec-schedule-box">
                    <div class="ec-schedule-item"><strong>🕟 ٤:٣٠ - ٦:٠٠ م</strong> ← 🏃‍♀️ بنات (جميع الأعمار)</div>
                    <div class="ec-schedule-item"><strong>🕕 ٦:٠٠ - ٨:٠٠ م</strong> ← 🏃 بنين (الصف الأول - الخامس الابتدائي)</div>
                    <div class="ec-schedule-item"><strong>🕗 ٨:٠٠ - ١٠:٠٠ م</strong> ← 🏃 بنين (الصف السادس - الثاني الإعدادي)</div>
                    <div style="margin-top:14px; color:#64748b; font-size:0.88rem;">📍 ملاعب مدرسة السلام المتطورة - أسيوط</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="ec-program-card" style="margin-bottom:30px;">
        <div class="ec-program-hdr">⚽</div>
        <div class="ec-program-body">
            <h3>ماذا يشمل التدريب؟</h3>
            <div class="ec-schedule-box">
                <h4 style="color:#1e3a8a; margin:0 0 14px; font-size:1.15rem;">🎯 محاور التدريب الأساسية:</h4>
                <ul style="margin:0 20px 18px 0; color:#334155; line-height:2;">
                    <li><strong>المهارات الفنية:</strong> التمرير - الاستلام - المراوغة - التسديد</li>
                    <li><strong>اللياقة البدنية:</strong> السرعة - الرشاقة - القوة - التحمل</li>
                    <li><strong>العمل الجماعي:</strong> التكتيك والانضباط الجماعي</li>
                    <li><strong>الذكاء الكروي:</strong> القراءة التحليلية للملعب واتخاذ القرار</li>
                    <li><strong>بناء الشخصية:</strong> الثقة بالنفس والقيم الرياضية</li>
                </ul>
                <h4 style="color:#1e3a8a; margin:0 0 14px; font-size:1.15rem;">💼 ما يقدمه النادي:</h4>
                <ul style="margin:0 20px 0 0; color:#334155; line-height:2;">
                    <li>ملابس تدريب رسمية (قميص - شورت - جوارب)</li>
                    <li>مسابقات دورية داخلية وخارجية</li>
                    <li>تقييمات شهرية وتقارير تطور الأداء</li>
                    <li>فيديوهات تحليل أداء للمتميزين</li>
                    <li>فرص احتراف في الأندية الكبرى</li>
                    <li>تأمين صحي للاعبين أثناء التدريبات</li>
                </ul>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="background:linear-gradient(135deg,#f0f9ff,#e0f2fe); border-radius:24px; padding:30px; text-align:center;">
        <h3 style="color:#1e3a8a; margin:0 0 12px;">📞 للتسجيل والاستفسار</h3>
        <p style="color:#334155; margin:0 0 18px;">تواصل معنا الآن للحصول على عرض تجريبي مجاني</p>
        <a href="?page=registration" target="_self" class="ec-btn ec-btn-gold" style="padding:12px 35px; font-size:1rem;">سجل الآن</a>
    </div>
    """, unsafe_allow_html=True)

# ====================================================================================================
# CAPTAINS PAGE
# ====================================================================================================
elif page in ("coaches", "captains"):
    st.markdown("""
    <div class="ec-page-header">
        <h1>صفحة الكباتن</h1>
        <p>فريقنا من الكباتن والمدربين ذوي الخبرة والكفاءة</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="ec-lead-captain">
        <div class="ec-lead-avatar">👨‍🏫</div>
        <div class="ec-lead-info">
            <h3>كابتن / ميخائيل كميل رؤف</h3>
            <div class="ec-title-badge">المدير الفني - مؤسس الأكاديمية</div>
            <div class="ec-qualifications">
                🎓 بكالوريوس تربية رياضية<br>
                📜 رخصة تدريب CAF لمراحل البراعم<br>
                📜 دبلومة الإعداد البدني المتقدم<br>
                📜 دبلومة إصابات الملاعب والعلاج الطبيعي<br>
                🏫 مدرس تربية رياضية بمدارس السلام الخاصة<br>
                ⭐ خبرة أكثر من 10 سنوات في تدريب الناشئين
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="ec-captains-grid">
        <div class="ec-captain-card">
            <div class="ec-captain-avatar">🧤</div>
            <div class="ec-captain-info">
                <h3>كابتن أحمد علي</h3>
                <div class="ec-coach-title">مدرب حراس مرمى - معتمد CAF</div>
                <div class="ec-coach-desc">
                    🎓 بكالوريوس تربية رياضية<br>
                    📜 رخصة تدريب حراس مرمى CAF<br>
                    📜 خبرة 15 عامًا في تدريب حراس المرمى<br>
                    📜 عمل مع عدة أندية في الدوري المصري
                </div>
            </div>
        </div>
        <div class="ec-captain-card">
            <div class="ec-captain-avatar">🏃</div>
            <div class="ec-captain-info">
                <h3>د. خالد السيد</h3>
                <div class="ec-coach-title">مدرب لياقة بدنية - دكتوراه</div>
                <div class="ec-coach-desc">
                    🎓 دكتوراه في علوم الرياضة<br>
                    📜 أستاذ مساعد بكلية التربية الرياضية<br>
                    📜 مختص في تطوير قدرات الناشئين<br>
                    📜 مدرب لياقة معتمد من الاتحاد المصري
                </div>
            </div>
        </div>
        <div class="ec-captain-card">
            <div class="ec-captain-avatar">⚽</div>
            <div class="ec-captain-info">
                <h3>كابتن محمد جابر</h3>
                <div class="ec-coach-title">مدرب مهارات فنية - معتمد CAF</div>
                <div class="ec-coach-desc">
                    🎓 بكالوريوس تربية رياضية<br>
                    📜 رخصة تدريب مهارات CAF<br>
                    📜 خبرة 12 عامًا في تدريب المهارات الفنية<br>
                    📜 دورات متقدمة في تدريب الناشئين
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="ec-info-banner">
        <h3>🌟 فريق تدريب متكامل</h3>
        <p>يجمع فريقنا بين الخبرات الأكاديمية والعملية لضمان أفضل تدريب</p>
        <div class="ec-banner-stats">
            <div class="ec-banner-stat"><span>12+</span>مدرب معتمد</div>
            <div class="ec-banner-stat"><span>100+</span>دورة تدريبية</div>
            <div class="ec-banner-stat"><span>20+</span>سنة خبرة</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ====================================================================================================
# REGISTRATION PAGE
# ====================================================================================================
elif page == "registration":
    st.markdown("""
    <div class="ec-page-header">
        <h1>تسجيل لاعب جديد</h1>
        <p>انضم إلى الكوتش أكاديمي وابدأ رحلتك نحو الاحتراف</p>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.show_success:
        st.markdown(
            '<div class="ec-success-msg">تم إرسال طلب التسجيل بنجاح! سنتواصل معكم خلال 24 ساعة.</div>',
            unsafe_allow_html=True,
        )
        st.session_state.show_success = False

    with st.form("registration_form"):
        st.markdown("### 📋 معلومات اللاعب")
        col1, col2 = st.columns(2)
        with col1:
            player_name = st.text_input("اسم اللاعب الثلاثي *", placeholder="مثال: محمد أحمد محمود")
            age_group = st.selectbox(
                "الفئة العمرية *",
                [
                    "",
                    "🏃‍♀️ بنات (جميع الأعمار)",
                    "🏃 بنين (الصف الأول - الخامس الابتدائي)",
                    "🏃 بنين (الصف السادس - الثاني الإعدادي)",
                ],
            )
        with col2:
            position = st.selectbox(
                "المركز المفضل",
                ["", "حارس مرمى", "مدافع", "لاعب وسط", "مهاجم", "أكثر من مركز"],
            )

        st.markdown("### 👨‍👩‍👦 معلومات ولي الأمر")
        col1, col2 = st.columns(2)
        with col1:
            parent_phone = st.text_input("رقم الهاتف *", placeholder="01XXXXXXXXX")

        notes = st.text_area("ملاحظات إضافية (اختياري)", placeholder="أي معلومات إضافية تود إضافتها...")

        submitted = st.form_submit_button("📝 تقديم طلب التسجيل", use_container_width=True)

        if submitted:
            if not player_name or not age_group or not parent_phone:
                st.markdown(
                    '<div class="ec-error-msg">⚠️ يرجى ملء جميع الحقول المطلوبة</div>',
                    unsafe_allow_html=True,
                )
            else:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                row = [player_name, age_group, position, parent_phone, notes, timestamp]
                success, msg = save_to_google_sheets(row)
                
                if success:
                    # إرسال البيانات إلى التلجرام
                    telegram_text = (
                        f"<b>⚽ طلب تسجيل لاعب جديد - الكوتش أكاديمي</b>\n\n"
                        f"<b>معلومات اللاعب:</b>\n"
                        f"• <b>الاسم:</b> {player_name}\n"
                        f"• <b>الفئة العمرية:</b> {age_group}\n"
                        f"• <b>المركز المفضل:</b> {position or 'لم يتم التحديد'}\n\n"
                        f"<b>معلومات ولي الأمر:</b>\n"
                        f"• <b>الهاتف:</b> {parent_phone}\n\n"
                        f"<b>ملاحظات:</b> {notes or 'بدون ملاحظات'}\n\n"
                        f"<b>وقت التسجيل:</b> {timestamp}"
                    )
                    telegram_success, _ = send_telegram_message(telegram_text)
                    
                    st.session_state.show_success = True
                    st.session_state.registration_submitted = True
                    st.rerun()
                else:
                    st.markdown(
                        f'<div class="ec-error-msg">❌ {msg}</div>',
                        unsafe_allow_html=True,
                    )

# ====================================================================================================
# FAQ PAGE
# ====================================================================================================
elif page == "faq":
    st.markdown("""
    <div class="ec-page-header">
        <h1>الأسئلة الشائعة</h1>
        <p>إجابات على أكثر الأسئلة شيوعًا من أولياء الأمور واللاعبين</p>
    </div>
    """, unsafe_allow_html=True)

    faqs = [
        (
            "ما هو سن القبول في الأكاديمية؟",
            "نستقبل اللاعبين والبنات من سن الصف الأول الابتدائي وحتى الصف الثاني الإعدادي. لدينا فئات عمرية مختلفة لكل مرحلة لضمان تدريب مناسب لكل سن.",
        ),
        (
            "ما هي مدة البرنامج التدريبي؟",
            "الموسم التدريبي يمتد لمدة 10 أشهر تقريبًا، من بداية سبتمبر إلى نهاية يونيو. التدريبات تقام أيام السبت والخميس في الفترة المسائية حسب الجدول المحدد لكل فئة.",
        ),
        (
            "هل يوجد تدريب للبنات؟",
            "نعم، لدينا برامج تدريبية مخصصة للبنات في أيام السبت والخميس مع مدربات متخصصات ومؤهلات، وبيئة مناسبة تلبي احتياجاتهن الرياضية والنفسية مع مراعاة الخصوصية الكاملة.",
        ),
        (
            "هل يوجد تدريب للمبتدئين؟",
            "بالتأكيد! لدينا برامج خاصة للمبتدئين تركز على تعلم أساسيات كرة القدم من الصفر، تطوير المهارات الحركية الأساسية، بناء الثقة بالنفس وحب الرياضة، وتدريبات ترفيهية محفزة للتعلم.",
        ),
        (
            "كيف يتم تقييم اللاعبين؟",
            "نوفر نظام تقييم شامل يشمل: تقييم فني دوري للمهارات، متابعة التطور البدني، تقارير شهرية عن الأداء، لقاءات دورية مع أولياء الأمور، فيديوهات تحليل أداء للمتميزين، وشهادات تقدير للمتفوقين.",
        ),
        (
            "أين تقام التدريبات؟",
            "تقام جميع التدريبات على ملاعب مدرسة السلام المتطورة في أسيوط، وهي ملاعب مجهزة بأحدث المعدات وتوفر بيئة آمنة ومناسبة للتدريب.",
        ),
        (
            "ما هي سياسة الرسوم والدفع؟",
            "تختلف الرسوم حسب الفئة العمرية وعدد أيام التدريب. نقدم: نظام تقسيط شهري مرن، خصومات خاصة للأشقاء، منح جزئية للمتميزين ماديًا أو فنيًا، وخصم للتسجيل المبكر. يرجى التواصل معنا لمعرفة التفاصيل.",
        ),
        (
            "هل توجد خصومات؟",
            "نعم! نقدم خصومات متعددة: خصم للأشقاء المسجلين معًا، خصم التسجيل المبكر قبل بداية الموسم، ومنح جزئية للمتميزين فنيًا أو المحتاجين ماديًا. تواصل معنا لمعرفة المزيد.",
        ),
    ]

    for question, answer in faqs:
        st.markdown(
            f"""
        <div class="ec-faq-card">
            <h4>❓ {question}</h4>
            <p>{answer}</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

# ====================================================================================================
# CONTACT PAGE (with Google Map and WhatsApp)
# ====================================================================================================
elif page == "contact":
    st.markdown("""
    <div class="ec-page-header">
        <h1>اتصل بنا</h1>
        <p>نسعد بتواصلكم معنا في أي وقت</p>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.show_contact_success:
        st.markdown(
            '<div class="ec-success-msg">تم إرسال رسالتك بنجاح! سنتواصل معك في أقرب وقت.</div>',
            unsafe_allow_html=True,
        )
        st.session_state.show_contact_success = False

    col_form, col_info = st.columns(2)

    with col_form:
        with st.form("contact_form"):
            st.markdown("### 📬 أرسل لنا رسالة")
            contact_name = st.text_input("الاسم *", placeholder="اسمك الكامل")
            contact_phone = st.text_input("رقم الهاتف *", placeholder="01XXXXXXXXX")
            inquiry_type = st.selectbox(
                "نوع الاستفسار *",
                ["", "استفسار عام", "تسجيل لاعب جديد", "مواعيد التدريب", "الرسوم والاشتراكات", "شكوى أو اقتراح", "أخرى"],
            )
            contact_message = st.text_area("الرسالة *", placeholder="اكتب رسالتك هنا...")

            contact_submitted = st.form_submit_button("📨 إرسال الرسالة", use_container_width=True)

            if contact_submitted:
                if not contact_name or not contact_phone or not inquiry_type or not contact_message:
                    st.markdown(
                        '<div class="ec-error-msg">⚠️ يرجى ملء جميع الحقول المطلوبة</div>',
                        unsafe_allow_html=True,
                    )
                else:
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    telegram_text = (
                        f"<b>📬 رسالة جديدة - الكوتش أكاديمي</b>\n\n"
                        f"<b>الاسم:</b> {contact_name}\n"
                        f"<b>الهاتف:</b> {contact_phone}\n"
                        f"<b>نوع الاستفسار:</b> {inquiry_type}\n"
                        f"<b>الرسالة:</b>\n{contact_message}\n\n"
                        f"<b>وقت الإرسال:</b> {timestamp}"
                    )
                    success, msg = send_telegram_message(telegram_text)
                    if success:
                        st.session_state.show_contact_success = True
                        st.rerun()
                    else:
                        st.markdown(
                            f'<div class="ec-error-msg">❌ {msg}</div>',
                            unsafe_allow_html=True,
                        )

    with col_info:
        st.markdown("""
        <div class="ec-contact-card">
            <h3 style="color:#1e3a8a; margin:0 0 18px; font-size:1.3rem; font-weight:800;">📍 معلومات التواصل</h3>
            <div class="ec-contact-item">
                <div class="ec-icon">📍</div>
                <div>
                    <strong style="color:#1e293b;">العنوان</strong><br>
                    <span style="color:#64748b;">ملاعب مدرسة السلام المتطورة - أسيوط</span>
                </div>
            </div>
            <div class="ec-contact-item">
                <div class="ec-icon">📞</div>
                <div>
                    <strong style="color:#1e293b;">الهاتف</strong><br>
                    <span style="color:#64748b;"><a href="tel:+201285197778" style="color:#64748b; text-decoration:none;">+20 12 851 97778</a></span>
                </div>
            </div>
            <div class="ec-contact-item">
                <div class="ec-icon">🕐</div>
                <div>
                    <strong style="color:#1e293b;">أوقات التدريب</strong><br>
                    <span style="color:#64748b;">السبت والخميس - الفترة المسائية</span>
                </div>
            </div>
            <div class="ec-contact-item">
                <div class="ec-icon">📧</div>
                <div>
                    <strong style="color:#1e293b;">التواصل الإلكتروني</strong><br>
                    <span style="color:#64748b;">أرسل رسالتك عبر النموذج وسنرد عليك</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # WhatsApp button
        st.markdown("""
        <div style="margin-top: 20px; text-align: center;">
            <a href="https://wa.me/201285197778?text=مرحباً%20بالكوتش%20أكاديمي" target="_blank" class="ec-whatsapp-btn">
                💬 تواصل معنا عبر واتساب
            </a>
        </div>
        """, unsafe_allow_html=True)

        # Google Map embed - using the actual link provided
        st.markdown("""
        <div style="margin-top: 25px; text-align: center;">
            <a href="https://maps.app.goo.gl/MX9GM7XC4jenPpgs8" target="_blank" style="display: inline-flex; align-items: center; gap: 8px; background: #4285F4; color: white; padding: 10px 20px; border-radius: 50px; text-decoration: none; font-weight: 700;">
                🗺️ عرض الموقع على خرائط جوجل
            </a>
        </div>
        <div class="ec-map-container" style="margin-top: 15px;">
            <iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3500.123456789!2d31.201543!3d27.171729!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x144c4d4b4b4b4b4b%3A0x4b4b4b4b4b4b4b4b!2z2YXYrdmF2K8g2KfZhNio2K8g2KfZhNipINmF2YjZgyDYp9mE2K_Ys9mF!5e0!3m2!1sar!2seg!4v1234567890123!5m2!1sar!2seg" allowfullscreen="" loading="lazy"></iframe>
        </div>
        """, unsafe_allow_html=True)
        # Note: The iframe uses placeholder coordinates. To get the exact map, replace the src with the actual embed code from Google Maps.

# ====================================================================================================
# NEWS PAGE
# ====================================================================================================
elif page == "news":
    st.markdown("""
    <div class="ec-page-header">
        <h1>الأخبار</h1>
        <p>آخر أخبار وأنشطة الكوتش أكاديمي</p>
    </div>
    """, unsafe_allow_html=True)

    news_items = [
        {
            "title": "بدء التسجيل للموسم الجديد 2025/2026",
            "date": "2025-08-15",
            "desc": "يسعدنا الإعلان عن فتح باب التسجيل للموسم التدريبي الجديد 2025/2026. سارعوا بالتسجيل للاستفادة من خصم التسجيل المبكر. البرامج متاحة لجميع الفئات العمرية للبنين والبنات.",
        },
        {
            "title": "فوز فريق الأكاديمية ببطولة أسيوط للناشئين",
            "date": "2025-06-20",
            "desc": "حقق فريق الأكاديمية إنجازًا رائعًا بالفوز ببطولة أسيوط للناشئين تحت 12 سنة، بعد مباراة نهائية مثيرة انتهت بنتيجة 3-1. تهانينا لجميع اللاعبين والمدربين!",
        },
        {
            "title": "دورة تدريبية متقدمة للمدربين",
            "date": "2025-05-10",
            "desc": "أتم مدربو الأكاديمية بنجاح دورة تدريبية متقدمة في أساليب التدريب الحديثة، بالتعاون مع الاتحاد المصري لكرة القدم. الدورة شملت أحدث المنهجيات في تطوير الناشئين.",
        },
        {
            "title": "انضمام لاعبين من الأكاديمية لمنتخب المحافظة",
            "date": "2025-04-05",
            "desc": "تم اختيار 5 لاعبين من الأكاديمية للانضمام لمنتخب محافظة أسيوط تحت 14 سنة، وهو ما يعكس مستوى التدريب المتميز الذي يحصل عليه لاعبونا.",
        },
        {
            "title": "محاضرة تثقيفية عن التغذية الرياضية",
            "date": "2025-03-15",
            "desc": "نظمت الأكاديمية محاضرة تثقيفية لأولياء الأمور واللاعبين حول أهمية التغذية السليمة وتأثيرها على الأداء الرياضي، قدمها أخصائي تغذية رياضية معتمد.",
        },
        {
            "title": "شراكة جديدة مع نادي أسيوط الرياضي",
            "date": "2025-02-20",
            "desc": "وقّعت الأكاديمية اتفاقية شراكة مع نادي أسيوط الرياضي لتسهيل انتقال اللاعبين الموهوبين إلى فرق النادي، مما يفتح آفاقًا جديدة للاحتراف أمام لاعبينا.",
        },
    ]

    for item in news_items:
        st.markdown(
            f"""
        <div class="ec-news-card">
            <h3>📌 {item['title']}</h3>
            <div class="ec-news-date">🗓️ {item['date']}</div>
            <p>{item['desc']}</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

# Close container
st.markdown("</div>", unsafe_allow_html=True)

# ====================================================================================================
# FOOTER (with fixed links)
# ====================================================================================================
current_year = datetime.now().year
footer_links = f"""
<div class="ec-footer">
    <div class="ec-footer-inner">
        <div>
            <h4>الكوتش أكاديمي</h4>
            <p>أكاديمية كرة القدم المتخصصة في بناء اللاعب الشامل فنيًا وبدنيًا وذهنيًا. نؤمن بأن كل لاعب يستحق فرصة حقيقية للتطور والاحتراف.</p>
        </div>
        <div>
            <h4>روابط سريعة</h4>
            <ul>
                <li>{nav_link("🏠 الرئيسية", "home")}</li>
                <li>{nav_link("ℹ️ من نحن", "about")}</li>
                <li>{nav_link("⚽ البرامج التدريبية", "programs")}</li>
                <li>{nav_link("👨‍🏫 الكباتن", "captains")}</li>
                <li>{nav_link("📝 سجل لاعب جديد", "registration")}</li>
            </ul>
        </div>
        <div>
            <h4>تواصل معنا</h4>
            <p>📍 ملاعب مدرسة السلام المتطورة - أسيوط</p>
            <p>🕐 السبت والخميس - الفترة المسائية</p>
            <p style="margin-top:12px;">
                {nav_link("📞 اتصل بنا", "contact")}
            </p>
        </div>
    </div>
    <div class="ec-footer-bottom">
        جميع الحقوق محفوظة &copy; {current_year} الكوتش أكاديمي - أكاديمية كرة القدم المتخصصة
    </div>
</div>
"""
st.markdown(footer_links, unsafe_allow_html=True)
