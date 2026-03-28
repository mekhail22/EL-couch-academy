from flask import Flask, render_template_string, request, jsonify, redirect, url_for
import json
import os
from datetime import datetime

app = Flask(__name__)

# HTML template (نسخة من الكود الأصلي)
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>الكوتش أكاديمي - أكاديمية كرة القدم المتخصصة</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        /* ===== التنسيقات العامة ===== */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        :root {
            --primary-color: #1e3a8a;
            --secondary-color: #3b82f6;
            --accent-color: #f59e0b;
            --light-color: #f8fafc;
            --dark-color: #1e293b;
            --success-color: #10b981;
            --text-color: #334155;
            --shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            --transition: all 0.3s ease;
        }
        
        body {
            color: var(--text-color);
            line-height: 1.6;
            background-color: #fff;
        }
        
        .container {
            width: 90%;
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }
        
        .btn {
            display: inline-block;
            padding: 12px 30px;
            background-color: var(--secondary-color);
            color: white;
            text-decoration: none;
            border-radius: 5px;
            font-weight: 600;
            border: none;
            cursor: pointer;
            transition: var(--transition);
            box-shadow: var(--shadow);
        }
        
        .btn:hover {
            background-color: var(--primary-color);
            transform: translateY(-3px);
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.15);
        }
        
        .btn-accent {
            background-color: var(--accent-color);
            color: var(--dark-color);
        }
        
        .btn-accent:hover {
            background-color: #e59400;
        }
        
        section {
            padding: 80px 0;
        }
        
        h1, h2, h3, h4 {
            color: var(--dark-color);
            margin-bottom: 1rem;
            font-weight: 700;
        }
        
        h1 {
            font-size: 2.8rem;
        }
        
        h2 {
            font-size: 2.2rem;
            color: var(--primary-color);
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
            background-color: var(--accent-color);
            border-radius: 2px;
        }
        
        .section-title {
            text-align: center;
            margin-bottom: 50px;
        }
        
        .section-title h2:after {
            right: 50%;
            transform: translateX(50%);
        }
        
        .section-title p {
            color: #64748b;
            max-width: 700px;
            margin: 0 auto;
            font-size: 1.1rem;
        }
        
        /* ===== الهيدر مع برجر ميني ===== */
        header {
            background-color: rgba(255, 255, 255, 0.95);
            box-shadow: var(--shadow);
            position: fixed;
            top: 0;
            width: 100%;
            z-index: 1000;
            transition: var(--transition);
        }
        
        .header-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 15px 0;
        }
        
        .logo {
            display: flex;
            align-items: center;
            gap: 10px;
            z-index: 1001;
        }
        
        .logo-img {
            width: 60px;
            height: 60px;
            border-radius: 10px;
            object-fit: cover;
            border: 2px solid var(--secondary-color);
        }
        
        .logo-text h1 {
            font-size: 1.6rem;
            margin: 0;
            color: var(--primary-color);
        }
        
        .logo-text span {
            color: var(--accent-color);
        }
        
        .logo-text p {
            font-size: 0.9rem;
            color: #666;
            margin: 0;
        }
        
        /* برجر ميني - للهواتف فقط */
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
            background-color: var(--primary-color);
            border-radius: 2px;
            transition: var(--transition);
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
        
        /* القائمة الجانبية - للهواتف فقط */
        .side-nav {
            position: fixed;
            top: 0;
            right: -300px;
            width: 300px;
            height: 100vh;
            background-color: white;
            box-shadow: -5px 0 15px rgba(0, 0, 0, 0.1);
            z-index: 1000;
            transition: var(--transition);
            overflow-y: auto;
            padding-top: 80px;
            display: none;
        }
        
        .side-nav.active {
            right: 0;
            display: block;
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
            color: var(--dark-color);
            text-decoration: none;
            font-weight: 600;
            padding: 12px 15px;
            border-radius: 8px;
            transition: var(--transition);
        }
        
        .side-nav a:hover, .side-nav a.active {
            background-color: rgba(59, 130, 246, 0.1);
            color: var(--secondary-color);
        }
        
        .side-nav i {
            font-size: 1.2rem;
            width: 24px;
            text-align: center;
        }
        
        /* ===== القائمة العلوية للشاشات المتوسطة والكبيرة ===== */
        .top-nav {
            display: flex;
            align-items: center;
            gap: 5px;
        }
        
        .top-nav ul {
            display: flex;
            list-style: none;
            gap: 5px;
            flex-wrap: wrap;
            justify-content: flex-end;
        }
        
        .top-nav li {
            margin-left: 0;
        }
        
        .top-nav a {
            display: flex;
            align-items: center;
            gap: 8px;
            color: var(--dark-color);
            text-decoration: none;
            font-weight: 600;
            padding: 10px 15px;
            border-radius: 6px;
            transition: var(--transition);
            font-size: 0.9rem;
            white-space: nowrap;
        }
        
        .top-nav a:hover, .top-nav a.active {
            background-color: rgba(59, 130, 246, 0.1);
            color: var(--secondary-color);
        }
        
        .top-nav i {
            font-size: 1rem;
        }
        
        /* ===== الصفحات ===== */
        .page {
            display: none;
            opacity: 0;
            transition: opacity 0.5s ease;
            min-height: calc(100vh - 400px);
        }
        
        .page.active {
            display: block;
            opacity: 1;
        }
        
        .page-header {
            background: linear-gradient(rgba(30, 58, 138, 0.9), rgba(30, 58, 138, 0.85)), url('https://images.unsplash.com/photo-1575361204480-aadea25e6e68?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80');
            background-size: cover;
            background-position: center;
            color: white;
            text-align: center;
            padding: 120px 0 60px;
            margin-top: 70px;
        }
        
        .page-header h1 {
            color: white;
            font-size: 2.5rem;
        }
        
        .page-header p {
            max-width: 700px;
            margin: 0 auto;
            font-size: 1.1rem;
            color: #e2e8f0;
        }
        
        /* ===== القسم الرئيسي ===== */
        .hero {
            background: linear-gradient(rgba(0, 0, 0, 0.75), rgba(0, 0, 0, 0.7)), url('https://images.unsplash.com/photo-1575361204480-aadea25e6e68?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80');
            background-size: cover;
            background-position: center;
            color: white;
            padding: 160px 0 100px;
            text-align: center;
            margin-top: 70px;
        }
        
        .hero h1 {
            font-size: 3.2rem;
            color: white;
            margin-bottom: 20px;
        }
        
        .hero p {
            font-size: 1.2rem;
            max-width: 800px;
            margin: 0 auto 30px;
            color: #e2e8f0;
        }
        
        .hero-buttons {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-top: 30px;
        }
        
        /* ===== قسم الإحصائيات ===== */
        .stats {
            background-color: var(--light-color);
            padding: 60px 0;
        }
        
        .stats-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 30px;
            text-align: center;
        }
        
        .stat-box {
            padding: 30px 20px;
            background-color: white;
            border-radius: 10px;
            box-shadow: var(--shadow);
            transition: var(--transition);
        }
        
        .stat-box:hover {
            transform: translateY(-10px);
        }
        
        .stat-box i {
            font-size: 2.5rem;
            color: var(--secondary-color);
            margin-bottom: 15px;
        }
        
        .stat-number {
            font-size: 2.5rem;
            font-weight: bold;
            color: var(--primary-color);
            display: block;
        }
        
        .stat-label {
            color: #666;
            font-size: 1.1rem;
        }
        
        /* ===== قسم المميزات ===== */
        .features-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
        }
        
        .feature-card {
            background-color: var(--light-color);
            padding: 30px;
            border-radius: 10px;
            box-shadow: var(--shadow);
            transition: var(--transition);
            text-align: center;
        }
        
        .feature-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 15px 30px rgba(0, 0, 0, 0.1);
        }
        
        .feature-icon {
            font-size: 2.5rem;
            color: var(--secondary-color);
            margin-bottom: 20px;
        }
        
        .feature-card h3 {
            color: var(--primary-color);
            margin-bottom: 15px;
        }
        
        /* ===== قسم البرامج التدريبية ===== */
        .programs-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
        }
        
        .program-card {
            background-color: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: var(--shadow);
            transition: var(--transition);
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
        
        .program-content h3 {
            color: var(--primary-color);
            margin-bottom: 10px;
        }
        
        .program-content p {
            color: #666;
            margin-bottom: 20px;
        }
        
        .program-age {
            display: inline-block;
            background-color: var(--accent-color);
            color: var(--dark-color);
            padding: 5px 15px;
            border-radius: 20px;
            font-weight: 600;
        }
        
        /* ===== قسم المدربين ===== */
        .coaches-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 30px;
        }
        
        .coach-card {
            background-color: white;
            border-radius: 10px;
            overflow: hidden;
            text-align: center;
            box-shadow: var(--shadow);
            transition: var(--transition);
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
            color: var(--primary-color);
            margin-bottom: 5px;
        }
        
        .coach-info p {
            color: var(--secondary-color);
            margin-bottom: 10px;
            font-weight: 600;
        }
        
        .coach-experience {
            color: #666;
            font-size: 0.9rem;
        }
        
        /* ===== قسم التسجيل ===== */
        .registration-form {
            max-width: 700px;
            margin: 0 auto;
            background-color: var(--light-color);
            padding: 40px;
            border-radius: 10px;
            box-shadow: var(--shadow);
        }
        
        .form-group {
            margin-bottom: 20px;
            text-align: right;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 8px;
            font-weight: 500;
            color: var(--dark-color);
        }
        
        .form-group input, .form-group select, .form-group textarea {
            width: 100%;
            padding: 12px 15px;
            border: 1px solid #cbd5e1;
            border-radius: 5px;
            background-color: white;
            font-size: 1rem;
        }
        
        .form-group input:focus, .form-group select:focus, .form-group textarea:focus {
            outline: none;
            border-color: var(--secondary-color);
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
        }
        
        .form-row {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
        }
        
        /* ===== قسم الأسئلة الشائعة ===== */
        .faq-container {
            max-width: 800px;
            margin: 0 auto;
        }
        
        .faq-item {
            margin-bottom: 15px;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            overflow: hidden;
            transition: var(--transition);
        }
        
        .faq-item:hover {
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }
        
        .faq-question {
            padding: 20px;
            background-color: var(--light-color);
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-weight: 600;
            color: var(--primary-color);
        }
        
        .faq-answer {
            padding: 0 20px;
            max-height: 0;
            overflow: hidden;
            transition: max-height 0.3s ease, padding 0.3s ease;
        }
        
        .faq-item.active .faq-answer {
            padding: 20px;
            max-height: 500px;
        }
        
        .faq-question i {
            transition: transform 0.3s ease;
        }
        
        .faq-item.active .faq-question i {
            transform: rotate(180deg);
        }
        
        /* ===== قسم من نحن ===== */
        .about-content {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 50px;
            align-items: center;
        }
        
        .about-image {
            height: 400px;
            background: linear-gradient(45deg, #3b82f6, #1e3a8a);
            border-radius: 10px;
            box-shadow: var(--shadow);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 8rem;
        }
        
        .about-text {
            padding-right: 20px;
        }
        
        .mission-vision {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            margin-top: 50px;
        }
        
        .mission-card, .vision-card {
            padding: 30px;
            border-radius: 10px;
            box-shadow: var(--shadow);
        }
        
        .mission-card {
            background-color: #f0f9ff;
            border-right: 4px solid var(--secondary-color);
        }
        
        .vision-card {
            background-color: #fef3c7;
            border-right: 4px solid var(--accent-color);
        }
        
        /* ===== قسم الاتصال ===== */
        .contact-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 40px;
        }
        
        .contact-info {
            background-color: var(--light-color);
            padding: 30px;
            border-radius: 10px;
            box-shadow: var(--shadow);
        }
        
        .contact-info h3 {
            color: var(--primary-color);
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid var(--accent-color);
        }
        
        .contact-item {
            display: flex;
            align-items: flex-start;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 1px solid #e2e8f0;
        }
        
        .contact-icon {
            font-size: 1.2rem;
            color: var(--secondary-color);
            margin-left: 15px;
            width: 24px;
            text-align: center;
        }
        
        .contact-form {
            background-color: var(--light-color);
            padding: 30px;
            border-radius: 10px;
            box-shadow: var(--shadow);
        }
        
        /* ===== الفوتر ===== */
        footer {
            background-color: var(--dark-color);
            color: white;
            padding: 60px 0 20px;
            margin-top: 50px;
        }
        
        .footer-content {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 40px;
            margin-bottom: 40px;
        }
        
        .footer-logo {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 20px;
        }
        
        .footer-logo img {
            width: 50px;
            height: 50px;
            border-radius: 8px;
            object-fit: cover;
            border: 2px solid var(--secondary-color);
        }
        
        .footer-logo h3 {
            font-size: 1.5rem;
            color: white;
        }
        
        .footer-about p {
            margin-bottom: 20px;
            color: #cbd5e1;
        }
        
        .footer-links h4, .footer-contact h4 {
            font-size: 1.2rem;
            margin-bottom: 20px;
            color: white;
            position: relative;
            padding-bottom: 10px;
        }
        
        .footer-links h4:after, .footer-contact h4:after {
            content: '';
            position: absolute;
            width: 40px;
            height: 2px;
            background-color: var(--secondary-color);
            bottom: 0;
            right: 0;
        }
        
        .footer-links ul {
            list-style: none;
        }
        
        .footer-links li {
            margin-bottom: 10px;
        }
        
        .footer-links a {
            color: #cbd5e1;
            text-decoration: none;
            transition: color 0.3s;
        }
        
        .footer-links a:hover {
            color: var(--secondary-color);
        }
        
        .contact-info-footer {
            list-style: none;
        }
        
        .contact-info-footer li {
            margin-bottom: 15px;
            display: flex;
            align-items: flex-start;
            gap: 10px;
        }
        
        .contact-info-footer i {
            color: var(--secondary-color);
            margin-top: 3px;
        }
        
        .social-icons {
            display: flex;
            gap: 15px;
            margin-top: 20px;
        }
        
        .social-icons a {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 40px;
            height: 40px;
            background-color: rgba(255, 255, 255, 0.1);
            border-radius: 50%;
            color: white;
            transition: background-color 0.3s;
        }
        
        .social-icons a:hover {
            background-color: var(--secondary-color);
        }
        
        .copyright {
            text-align: center;
            padding-top: 20px;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            color: #94a3b8;
            font-size: 0.9rem;
        }
        
        /* ===== تصميم متجاوب ===== */
        @media (max-width: 1200px) {
            .top-nav a {
                padding: 8px 12px;
                font-size: 0.85rem;
            }
            
            .top-nav ul {
                gap: 3px;
            }
        }
        
        @media (max-width: 992px) {
            h1 {
                font-size: 2.5rem;
            }
            
            .hero h1 {
                font-size: 2.8rem;
            }
            
            .about-content {
                grid-template-columns: 1fr;
            }
            
            .about-text {
                padding-right: 0;
            }
            
            .form-row {
                grid-template-columns: 1fr;
            }
            
            /* إخفاء القائمة العلوية وإظهار برجر ميني */
            .top-nav {
                display: none;
            }
            
            .burger-menu {
                display: flex;
            }
            
            .side-nav {
                display: block;
            }
            
            .register-btn-nav {
                display: none;
            }
        }
        
        @media (max-width: 768px) {
            .hero h1 {
                font-size: 2.2rem;
            }
            
            h2 {
                font-size: 1.8rem;
            }
            
            section {
                padding: 60px 0;
            }
            
            .page-header {
                padding: 100px 0 50px;
            }
            
            .hero-buttons {
                flex-direction: column;
                align-items: center;
            }
            
            .side-nav {
                width: 280px;
            }
        }
        
        @media (max-width: 576px) {
            .hero {
                padding: 120px 0 70px;
            }
            
            .hero h1 {
                font-size: 1.8rem;
            }
            
            .programs-grid, .coaches-grid, .features-grid {
                grid-template-columns: 1fr;
            }
            
            .registration-form {
                padding: 25px;
            }
            
            .page-header h1 {
                font-size: 2rem;
            }
        }
        
        /* تحسينات لعناصر النموذج */
        .form-note {
            font-size: 0.85rem;
            color: #64748b;
            margin-top: 5px;
        }
        
        /* نجاح الإرسال */
        .success-message {
            background-color: #10b981;
            color: white;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
            display: none;
            text-align: center;
        }
        
        /* تحسينات للشعار الجديد */
        .coach-logo-section {
            text-align: center;
            margin: 40px 0;
        }
        
        .coach-logo-large {
            max-width: 200px;
            border-radius: 15px;
            margin: 20px auto;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
        }
        
        /* خريطة الموقع - تمت إزالته */
        .map-container {
            display: none;
        }
        
        /* مواعيد البرامج */
        .program-schedule {
            background-color: var(--light-color);
            padding: 15px;
            border-radius: 8px;
            margin-top: 15px;
            border-right: 4px solid var(--accent-color);
        }
        
        .program-schedule h4 {
            color: var(--primary-color);
            margin-bottom: 10px;
            font-size: 1.2rem;
        }
        
        .schedule-day {
            font-weight: bold;
            color: var(--primary-color);
            margin: 15px 0 10px;
            padding-right: 10px;
            border-right: 3px solid var(--secondary-color);
            font-size: 1.1rem;
        }
        
        .time-slot {
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            border-bottom: 1px solid #e2e8f0;
        }
        
        .time-slot:last-child {
            border-bottom: none;
        }
        
        .time-range {
            color: var(--secondary-color);
            font-weight: 600;
            font-size: 1rem;
        }
        
        .category {
            color: var(--dark-color);
            font-weight: 600;
            text-align: left;
        }
        
        /* إصلاح الصور */
        .fallback-icon {
            font-size: 3rem;
            color: white;
        }
        
        /* صور محلية */
        .local-logo {
            background-color: var(--secondary-color);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
        }
        
        /* تنسيق أرقام الهواتف القابلة للضغط */
        .phone-link {
            color: inherit;
            text-decoration: none;
            transition: color 0.3s;
        }
        
        .phone-link:hover {
            color: var(--secondary-color);
            text-decoration: underline;
        }
        
        .whatsapp-link {
            color: #25D366;
            text-decoration: none;
            transition: color 0.3s;
        }
        
        .whatsapp-link:hover {
            color: #128C7E;
            text-decoration: underline;
        }
        
        /* تنسيق روابط الخرائط */
        .map-link {
            color: inherit;
            text-decoration: none;
            transition: color 0.3s;
        }
        
        .map-link:hover {
            color: var(--secondary-color);
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <!-- الهيدر مع برجر ميني -->
    <header id="header">
        <div class="container header-container">
            <div class="logo">
                <!-- تم تغيير الصورة لقراءة من ملف محلي -->
                <div class="logo-img local-logo">
                    <i class="fas fa-futbol fallback-icon"></i>
                </div>
                <div class="logo-text">
                    <h1>الكوتش <span>أكاديمي</span></h1>
                    <p>أكاديمية كرة القدم المتخصصة</p>
                </div>
            </div>
            
            <!-- قائمة علوية للشاشات المتوسطة والكبيرة -->
            <div class="top-nav">
                <ul>
                    <li><a href="/" class="nav-link" data-page="home"><i class="fas fa-home"></i> الرئيسية</a></li>
                    <li><a href="/about" class="nav-link" data-page="about"><i class="fas fa-info-circle"></i> من نحن</a></li>
                    <li><a href="/programs" class="nav-link" data-page="programs"><i class="fas fa-futbol"></i> البرامج</a></li>
                    <li><a href="/coaches" class="nav-link" data-page="coaches"><i class="fas fa-users"></i> المدربون</a></li>
                    <li><a href="/registration" class="nav-link" data-page="registration"><i class="fas fa-edit"></i> التسجيل</a></li>
                    <li><a href="/faq" class="nav-link" data-page="faq"><i class="fas fa-question-circle"></i> الأسئلة</a></li>
                    <li><a href="/contact" class="nav-link" data-page="contact"><i class="fas fa-phone"></i> اتصل بنا</a></li>
                </ul>
            </div>
            
            <!-- زر برجر ميني للشاشات الصغيرة فقط -->
            <button class="burger-menu" id="burgerMenu">
                <span></span>
                <span></span>
                <span></span>
            </button>
        </div>
        
        <!-- القائمة الجانبية للهواتف فقط -->
        <div class="side-nav" id="sideNav">
            <ul>
                <li><a href="/" class="nav-link" data-page="home"><i class="fas fa-home"></i> الرئيسية</a></li>
                <li><a href="/about" class="nav-link" data-page="about"><i class="fas fa-info-circle"></i> من نحن</a></li>
                <li><a href="/programs" class="nav-link" data-page="programs"><i class="fas fa-futbol"></i> البرامج التدريبية</a></li>
                <li><a href="/coaches" class="nav-link" data-page="coaches"><i class="fas fa-users"></i> المدربون</a></li>
                <li><a href="/registration" class="nav-link" data-page="registration"><i class="fas fa-edit"></i> تسجيل لاعب جديد</a></li>
                <li><a href="/faq" class="nav-link" data-page="faq"><i class="fas fa-question-circle"></i> الأسئلة الشائعة</a></li>
                <li><a href="/contact" class="nav-link" data-page="contact"><i class="fas fa-phone"></i> اتصل بنا</a></li>
            </ul>
        </div>
        
        <!-- طبقة التعتيم للهواتف فقط -->
        <div class="nav-overlay" id="navOverlay"></div>
    </header>

    <!-- ===== الصفحة الرئيسية ===== -->
    <div class="page active" id="home-page">
        <!-- القسم الرئيسي -->
        <section class="hero">
            <div class="container">
                <h1>⚽ الكوتش أكاديمي</h1>
                <p>أول أكاديمية متخصصة في مصر تركز على بناء اللاعب الشامل من الناحية الفنية والبدنية والنفسية، تحت إشراف مدربين معتمدين دوليًا.</p>
                <p style="font-weight: 600; margin-bottom: 20px;">نحن لا نصنع لاعبين فقط.. نحن نصنع قادة!</p>
                <div class="hero-buttons">
                    <!-- تعديل الأزرار للانتقال للصفحات المطلوبة -->
                    <a href="/registration" class="btn btn-accent nav-link" data-page="registration">سجل ابنك الآن</a>
                    <a href="/programs" class="btn nav-link" data-page="programs" style="background-color: transparent; border: 2px solid white;">اكتشف برامجنا</a>
                </div>
            </div>
        </section>

        <!-- قسم شعار الأكاديمية -->
        <div class="coach-logo-section">
            <div class="container">
                <!-- تم تغيير الصورة لقراءة من ملف محلي -->
                <div class="coach-logo-large local-logo">
                    <i class="fas fa-futbol fallback-icon" style="font-size: 8rem;"></i>
                </div>
            </div>
        </div>

        <!-- قسم الإحصائيات -->
        <section class="stats">
            <div class="container">
                <div class="section-title">
                    <h2>إنجازات الأكاديمية</h2>
                    <p>أرقام تتحدث عن نجاح مسيرتنا في صناعة أبطال المستقبل</p>
                </div>
                
                <div class="stats-container">
                    <div class="stat-box">
                        <i class="fas fa-users"></i>
                        <span class="stat-number">300+</span>
                        <span class="stat-label">لاعب مدرب</span>
                    </div>
                    <div class="stat-box">
                        <i class="fas fa-user-tie"></i>
                        <span class="stat-number">8</span>
                        <span class="stat-label">مدرب محترف</span>
                    </div>
                    <div class="stat-box">
                        <i class="fas fa-trophy"></i>
                        <span class="stat-number">100+</span>
                        <span class="stat-label">لاعب محترف</span>
                    </div>
                </div>
            </div>
        </section>

        <!-- قسم لماذا نختارنا -->
        <section class="why-us">
            <div class="container">
                <div class="section-title">
                    <h2>لماذا تختار الكوتش أكاديمي؟</h2>
                    <p>نحن نؤمن أن الموهبة تحتاج إلى منهجية علمية وتدريب منظم</p>
                </div>
                
                <div class="features-grid">
                    <div class="feature-card">
                        <div class="feature-icon">
                            <i class="fas fa-brain"></i>
                        </div>
                        <h3>منهجية التدريب الذهني</h3>
                        <p>نركز على تطوير الذكاء الكروي والقدرة على اتخاذ القرارات السريعة والصحيحة داخل الملعب.</p>
                    </div>
                    <div class="feature-card">
                        <div class="feature-icon">
                            <i class="fas fa-user-shield"></i>
                        </div>
                        <h3>بيئة آمنة محفزة</h3>
                        <p>نوفر بيئة تدريب آمنة تحترم الفروق الفردية وتشجع على الإبداع والتميز.</p>
                    </div>
                    <div class="feature-card">
                        <div class="feature-icon">
                            <i class="fas fa-handshake"></i>
                        </div>
                        <h3>شراكات مع الأندية</h3>
                        <p>لدينا شراكات مع أندية محلية لتمكين الموهوبين من الانضمام للمنتخبات والأندية الكبرى.</p>
                    </div>
                </div>
            </div>
        </section>
    </div>

    <!-- ===== صفحة من نحن ===== -->
    <div class="page" id="about-page">
        <div class="page-header">
            <div class="container">
                <h1>من نحن</h1>
                <p>الكوتش أكاديمي.. رؤية جديدة في عالم تدريب كرة القدم</p>
            </div>
        </div>
        
        <section class="about-section">
            <div class="container">
                <div class="about-content">
                    <div class="about-image">
                        <i class="fas fa-futbol"></i>
                    </div>
                    <div class="about-text">
                        <h2>تأسيس الأكاديمية</h2>
                        <p>تأسست الأكاديمية عام 2020 على يد:</p>
                        <ul style="margin-top: 10px; margin-right: 20px; color: #666;">
                            <li>كابتن ميخا</li>
                            <li>كابتن اندرو</li>
                            <li>كابتن مينا</li>
                        </ul>
                        <p style="margin-top: 15px;">على ملاعب مدرسة السلام المتطورة</p>
                        <p style="margin-top: 10px; font-weight: 600; color: var(--primary-color);">
                            بدعم من الأب الروحي للأكاديمية: مستر / مؤنس منير
                        </p>
                    </div>
                </div>
                
                <div class="mission-vision">
                    <div class="mission-card">
                        <h3><i class="fas fa-bullseye"></i> رسالتنا</h3>
                        <p>تطوير جيل جديد من اللاعبين المبدعين القادرين على التألق محليًا ودوليًا، من خلال تقديم تدريب عصري يعتمد على أحدث الأساليب العلمية والتكنولوجية في عالم كرة القدم.</p>
                        <ul style="margin-top: 15px;">
                            <li>تطوير المهارات الفنية الأساسية والمتقدمة</li>
                            <li>بناء اللياقة البدنية المخصصة لكل لاعب</li>
                            <li>تعزيز الذكاء الكروي والقدرات الذهنية</li>
                            <li>غرس القيم الرياضية والسلوك القيادي</li>
                        </ul>
                    </div>
                    
                    <div class="vision-card">
                        <h3><i class="fas fa-eye"></i> أهدافنا</h3>
                        <p>أن نكون الوجهة الأولى لأي موهبة كروية في مصر والوطن العربي، والجسر الذي يعبر من خلاله اللاعبون الموهوبون إلى العالمية.</p>
                        <ul style="margin-top: 15px;">
                            <li>صناعة لاعبين مؤهلين للدوريات العالمية</li>
                            <li>تطوير منهج تدريبي يُدرس في المعاهد الرياضية</li>
                            <li>المساهمة في تطوير كرة القدم العربية</li>
                            <li>بناء قاعدة بيانات للمواهب الكروية</li>
                        </ul>
                    </div>
                </div>
            </div>
        </section>
    </div>

    <!-- ===== صفحة البرامج التدريبية ===== -->
    <div class="page" id="programs-page">
        <div class="page-header">
            <div class="container">
                <h1>البرامج التدريبية</h1>
                <p>مواعيد تدريبية مصممة لكل فئة عمرية وجنسية</p>
            </div>
        </div>
        
        <section class="programs">
            <div class="container">
                <div class="section-title">
                    <h2>المواعيد التدريبية</h2>
                    <p>جدول مواعيد تدريبية متنوعة تناسب جميع الأعمار</p>
                </div>
                
                <div class="programs-grid">
                    <div class="program-card">
                        <div class="program-image">
                            <i class="fas fa-calendar-alt"></i>
                        </div>
                        <div class="program-content">
                            <h3>السبت</h3>
                            <p>مواعيد تدريب السبت المخصصة للبنين والبنات</p>
                            <div class="program-schedule">
                                <h4>المواعيد:</h4>
                                
                                <div class="schedule-day">⏰ التدريبات</div>
                                
                                <div class="time-slot">
                                    <span class="time-range">[٥:٠٠ - ٦:٠٠ م]</span>
                                    <span class="category">بنات</span>
                                </div>
                                
                                <div class="time-slot">
                                    <span class="time-range">[٦:٠٠ - ٧:٣٠ م]</span>
                                    <span class="category">بنين<br>(١ ابتدائي - ٥ ابتدائي)</span>
                                </div>
                                
                                <div class="time-slot">
                                    <span class="time-range">[٧:٣٠ - ٩:٠٠ م]</span>
                                    <span class="category">بنين<br>(٦ ابتدائي - ٢ إعدادي)</span>
                                </div>
                                
                                <div style="margin-top: 15px; color: #666; font-size: 0.9rem;">
                                    <p><i class="fas fa-info-circle"></i> جميع التدريبات في ملاعب مدرسة السلام المتطورة</p>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="program-card">
                        <div class="program-image">
                            <i class="fas fa-calendar-check"></i>
                        </div>
                        <div class="program-content">
                            <h3>الخميس</h3>
                            <p>مواعيد تدريب الخميس المخصصة للبنين والبنات</p>
                            <div class="program-schedule">
                                <h4>المواعيد:</h4>
                                
                                <div class="schedule-day">⏰ التدريبات</div>
                                
                                <div class="time-slot">
                                    <span class="time-range">[٤:٣٠ - ٦:٠٠ م]</span>
                                    <span class="category">بنات</span>
                                </div>
                                
                                <div class="time-slot">
                                    <span class="time-range">[٦:٠٠ - ٨:٠٠ م]</span>
                                    <span class="category">بنين<br>(١ ابتدائي - ٥ ابتدائي)</span>
                                </div>
                                
                                <div class="time-slot">
                                    <span class="time-range">[٨:٠٠ - ١٠:٠٠ م]</span>
                                    <span class="category">بنين<br>(٦ ابتدائي - ٢ إعدادي)</span>
                                </div>
                                
                                <div style="margin-top: 15px; color: #666; font-size: 0.9rem;">
                                    <p><i class="fas fa-info-circle"></i> جميع التدريبات في ملاعب مدرسة السلام المتطورة</p>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="program-card">
                        <div class="program-image">
                            <i class="fas fa-futbol"></i>
                        </div>
                        <div class="program-content">
                            <h3>معلومات عامة</h3>
                            <p>معلومات هامة حول البرامج التدريبية</p>
                            <div class="program-schedule">
                                <h4>تفاصيل البرامج:</h4>
                                
                                <div style="margin: 15px 0;">
                                    <h4>🎯 أهداف التدريب:</h4>
                                    <ul style="margin-right: 20px; color: #666;">
                                        <li>تنمية المهارات الفنية الأساسية</li>
                                        <li>تطوير القدرات البدنية</li>
                                        <li>تعزيز العمل الجماعي</li>
                                        <li>بناء الشخصية الرياضية</li>
                                    </ul>
                                </div>
                                
                                <div style="margin: 15px 0;">
                                    <h4>💼 ما يقدمه النادي:</h4>
                                    <ul style="margin-right: 20px; color: #666;">
                                        <li>ملابس التدريب</li>
                                        <li>مسابقات دورية</li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    </div>

    <!-- ===== صفحة المدربون ===== -->
    <div class="page" id="coaches-page">
        <div class="page-header">
            <div class="container">
                <h1>المدربون</h1>
                <p>فريقنا من المدربين المحترفين ذوي الخبرة والكفاءة</p>
            </div>
        </div>
        
        <section class="coaches">
            <div class="container">
                <div class="section-title">
                    <h2>فريق التدريب المتكامل</h2>
                    <p>مدربون معتمدون دوليًا بخبرات محلية وعالمية</p>
                </div>
                
                <div class="coaches-grid">
                    <div class="coach-card">
                        <div class="coach-image">
                            <i class="fas fa-user-tie"></i>
                        </div>
                        <div class="coach-info">
                            <h3>كابتن/ميخائيل كميل رؤف</h3>
                            <p>مدرب معتمد</p>
                            <ul class="coach-experience" style="list-style: none; padding-right: 10px; text-align: right;">
                                <li>• بكالريوس/تربية رياضية</li>
                                <li>• حاصل على الرخصة التدريبية لمراحل البراعم والمعتمدة من الاتحاد الأفريقي لكرة القدم</li>
                                <li>• حاصل على دبلومة الإعداد البدني</li>
                                <li>• حاصل على دبلومة في إصابات الملاعب والعلاج الطبيعي</li>
                                <li>• مدرس تربية رياضية بمدارس السلام الخاصة</li>
                            </ul>
                        </div>
                    </div>
                    
                    <div class="coach-card">
                        <div class="coach-image">
                            <i class="fas fa-hands"></i>
                        </div>
                        <div class="coach-info">
                            <h3>كابتن أحمد علي</h3>
                            <p>مدرب حراس مرمى</p>
                            <p class="coach-experience">مدرب معتمد من الاتحاد الأفريقي CAF</p>
                            <p style="margin-top: 10px; color: #666; font-size: 0.9rem;">خبرة 15 عامًا في تدريب الحراس</p>
                        </div>
                    </div>
                    
                    <div class="coach-card">
                        <div class="coach-image">
                            <i class="fas fa-running"></i>
                        </div>
                        <div class="coach-info">
                            <h3>د. خالد السيد</h3>
                            <p>مدرب لياقة بدنية</p>
                            <p class="coach-experience">دكتوراه في علوم الرياضة</p>
                            <p style="margin-top: 10px; color: #666; font-size: 0.9rem;">مختص في تطوير قدرات الناشئين</p>
                        </div>
                    </div>
                    
                    <div class="coach-card">
                        <div class="coach-image">
                            <i class="fas fa-futbol"></i>
                        </div>
                        <div class="coach-info">
                            <h3>كابتن محمد جابر</h3>
                            <p>مدرب مهارات فنية</p>
                            <p class="coach-experience">مدرب مهارات معتمد من الاتحاد الأفريقي CAF</p>
                            <p style="margin-top: 10px; color: #666; font-size: 0.9rem;">خبرة 12 عامًا في المهارات الفنية</p>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    </div>

    <!-- ===== صفحة تسجيل لاعب جديد ===== -->
    <div class="page" id="registration-page">
        <div class="page-header">
            <div class="container">
                <h1>تسجيل لاعب جديد</h1>
                <p>انضم إلى الكوتش أكاديمي وابدأ رحلتك نحو الاحتراف</p>
            </div>
        </div>
        
        <section class="registration">
            <div class="container">
                <div class="section-title">
                    <h2>نموذج التسجيل</h2>
                    <p>املأ النموذج التالي لتسجيل لاعب جديد في الأكاديمية</p>
                </div>
                
                <div class="success-message" id="successMessage">
                    <i class="fas fa-check-circle"></i> تم إرسال طلب التسجيل بنجاح! سنتواصل معكم خلال 24 ساعة.
                </div>
                
                <form class="registration-form" id="registrationForm">
                    <h3 style="color: var(--primary-color); margin-bottom: 20px;">معلومات اللاعب</h3>
                    
                    <div class="form-row">
                        <div class="form-group">
                            <label for="playerName">اسم اللاعب الثلاثي <span style="color: red;">*</span></label>
                            <input type="text" id="playerName" name="playerName" placeholder="اسم اللاعب" required>
                        </div>
                        <div class="form-group">
                            <label for="ageGroup">الفئة العمرية المطلوبة <span style="color: red;">*</span></label>
                            <select id="ageGroup" name="ageGroup" required>
                                <option value="">اختر الفئة العمرية</option>
                                <option value="بنات">بنات</option>
                                <option value="١ ابتدائي - ٥ ابتدائي">١ ابتدائي - ٥ ابتدائي</option>
                                <option value="٦ ابتدائي - ٢ إعدادي">٦ ابتدائي - ٢ إعدادي</option>
                            </select>
                        </div>
                    </div>
                    
                    <h3 style="color: var(--primary-color); margin: 30px 0 20px;">معلومات ولي الأمر</h3>
                    
                    <div class="form-row">
                        <div class="form-group">
                            <label for="parentName">اسم ولي الأمر <span style="color: red;">*</span></label>
                            <input type="text" id="parentName" name="parentName" placeholder="اسم ولي الأمر" required>
                        </div>
                        <div class="form-group">
                            <label for="parentPhone">رقم الهاتف <span style="color: red;">*</span></label>
                            <input type="tel" id="parentPhone" name="parentPhone" placeholder="01XXXXXXXXX" required>
                        </div>
                    </div>
                    
                    <div class="form-group">
                        <label for="notes">ملاحظات إضافية (اختياري)</label>
                        <textarea id="notes" name="notes" rows="3" placeholder="أي معلومات أخرى ترغب في إضافتها"></textarea>
                    </div>
                    
                    <div class="form-group" style="text-align: center; margin-top: 30px;">
                        <button type="submit" class="btn">تقديم طلب التسجيل</button>
                    </div>
                </form>
            </div>
        </section>
    </div>

    <!-- ===== صفحة الأسئلة الشائعة ===== -->
    <div class="page" id="faq-page">
        <div class="page-header">
            <div class="container">
                <h1>الأسئلة الشائعة</h1>
                <p>إجابات على أكثر الأسئلة شيوعًا من أولياء الأمور</p>
            </div>
        </div>
        
        <section class="faq">
            <div class="container">
                <div class="section-title">
                    <h2>أسئلة متكررة</h2>
                    <p>إجابات مفصلة على استفساراتكم</p>
                </div>
                
                <div class="faq-container">
                    <div class="faq-item">
                        <div class="faq-question">
                            <span>ما الذي يميز الكوتش أكاديمي عن غيرها؟</span>
                            <i class="fas fa-chevron-down"></i>
                        </div>
                        <div class="faq-answer">
                            <p>الكوتش أكاديمي تتبنى منهجية تدريب متكاملة تركز على:</p>
                            <ul style="margin-top: 10px; padding-right: 20px;">
                                <li>التدريب الذهني وتطوير الذكاء الكروي</li>
                                <li>متابعة فردية لكل لاعب مع خطة تطوير شخصية</li>
                                <li>استخدام التكنولوجيا في تحليل الأداء</li>
                                <li>شراكات مع أندية محلية لدعم الموهوبين</li>
                            </ul>
                        </div>
                    </div>
                    
                    <div class="faq-item">
                        <div class="faq-question">
                            <span>ما هي مدة التدريب وأوقاته؟</span>
                            <i class="fas fa-chevron-down"></i>
                        </div>
                        <div class="faq-answer">
                            <p>الموسم التدريبي يمتد لمدة 10 أشهر، من سبتمبر إلى يونيو. التدريبات في الفترة المسائية حسب الجدول المحدد لكل فئة عمرية، بما يتناسب مع أوقات المدارس.</p>
                        </div>
                    </div>
                    
                    <div class="faq-item">
                        <div class="faq-question">
                            <span>ما هي تكلفة الاشتراك وآلية الدفع؟</span>
                            <i class="fas fa-chevron-down"></i>
                        </div>
                        <div class="faq-answer">
                            <p>تختلف التكلفة حسب الفئة العمرية وعدد أيام التدريب. نقدم:</p>
                            <ul style="margin-top: 10px; padding-right: 20px;">
                                <li>خصومات للأشقاء</li>
                                <li>نظام تقسيط شهري</li>
                                <li>منح جزئية للمتميزين</li>
                            </ul>
                            <p style="margin-top: 10px;">يرجى التواصل معنا لمعرفة التفاصيل الدقيقة.</p>
                        </div>
                    </div>
                    
                    <div class="faq-item">
                        <div class="faq-question">
                            <span>ما هي متطلبات الانضمام للأكاديمية؟</span>
                            <i class="fas fa-chevron-down"></i>
                        </div>
                        <div class="faq-answer">
                            <p>للانضمام للأكاديمية نحتاج إلى:</p>
                            <ul style="margin-top: 10px; padding-right: 20px;">
                                <li>إكمال نموذج التسجيل عبر الموقع</li>
                                <li>أن يكون اللاعب في الفئة العمرية المحددة</li>
                                <li>الرغبة الحقيقية في التعلم والتطوير</li>
                                <li>الالتزام بمواعيد التدريب</li>
                            </ul>
                        </div>
                    </div>
                    
                    <div class="faq-item">
                        <div class="faq-question">
                            <span>هل هناك تدريبات خاصة للمبتدئين؟</span>
                            <i class="fas fa-chevron-down"></i>
                        </div>
                        <div class="faq-answer">
                            <p>نعم، لدينا برامج خاصة للمبتدئين تركز على:</p>
                            <ul style="margin-top: 10px; padding-right: 20px;">
                                <li>تعلم أساسيات كرة القدم</li>
                                <li>تطوير المهارات الحركية الأساسية</li>
                                <li>بناء الثقة بالنفس</li>
                                <li>تعزيز حب الرياضة واللعب الجماعي</li>
                            </ul>
                        </div>
                    </div>
                    
                    <div class="faq-item">
                        <div class="faq-question">
                            <span>كيف يمكن متابعة تطور اللاعب؟</span>
                            <i class="fas fa-chevron-down"></i>
                        </div>
                        <div class="faq-answer">
                            <p>نوفر نظام متابعة شامل يشمل:</p>
                            <ul style="margin-top: 10px; padding-right: 20px;">
                                <li>تقييم دوري للمهارات الفنية</li>
                                <li>متابعة التطور البدني</li>
                                <li>تقرير عن المشاركة والالتزام</li>
                                <li>لقاءات دورية مع أولياء الأمور</li>
                            </ul>
                        </div>
                    </div>
                    
                    <div class="faq-item">
                        <div class="faq-question">
                            <span>ماذا عن السلامة والإصابات خلال التدريب؟</span>
                            <i class="fas fa-chevron-down"></i>
                        </div>
                        <div class="faq-answer">
                            <p>السلامة أولوية لدينا، ونوفر:</p>
                            <ul style="margin-top: 10px; padding-right: 20px;">
                                <li>إشراف مستمر من مدربين مؤهلين</li>
                                <li>بيئة تدريب آمنة ومجهزة</li>
                                <li>برنامج إحماء وتبريد مناسب</li>
                                <li>مدربين حاصلين على شهادات في الإسعافات الأولية</li>
                            </ul>
                        </div>
                    </div>
                    
                    <div class="faq-item">
                        <div class="faq-question">
                            <span>هل يمكن للاعب الانتقال بين الفئات العمرية؟</span>
                            <i class="fas fa-chevron-down"></i>
                        </div>
                        <div class="faq-answer">
                            <p>نعم، يمكن للاعب الانتقال بين الفئات بناءً على:</p>
                            <ul style="margin-top: 10px; padding-right: 20px;">
                                <li>تطور مهاراته وقدراته</li>
                                <li>توصية المدرب المسؤول</li>
                                <li>موافقة ولي الأمر</li>
                                <li>التقييم الدوري للأداء</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    </div>

    <!-- ===== صفحة اتصل بنا ===== -->
    <div class="page" id="contact-page">
        <div class="page-header">
            <div class="container">
                <h1>اتصل بنا</h1>
                <p>تواصل معنا لأي استفسارات أو معلومات إضافية</p>
            </div>
        </div>
        
        <section class="contact">
            <div class="container">
                <div class="contact-container">
                    <div class="contact-info">
                        <h3>معلومات الاتصال</h3>
                        
                        <div class="contact-item">
                            <div class="contact-icon">
                                <i class="fas fa-phone"></i>
                            </div>
                            <div>
                                <h4>الهاتف</h4>
                                <p>
                                    <a href="tel:01069238878" class="phone-link">
                                        01069238878
                                    </a>
                                </p>
                            </div>
                        </div>
                        
                        <div class="contact-item">
                            <div class="contact-icon">
                                <i class="fab fa-whatsapp"></i>
                            </div>
                            <div>
                                <h4>الواتساب</h4>
                                <p>
                                    <a href="https://wa.me/201285197778" target="_blank" class="whatsapp-link">
                                        01285197778
                                    </a>
                                </p>
                            </div>
                        </div>
                        
                        <div class="contact-item">
                            <div class="contact-icon">
                                <i class="fas fa-map-marker-alt"></i>
                            </div>
                            <div>
                                <h4>العنوان الرئيسي</h4>
                                <p>
                                    <a href="https://maps.google.com/?q=مدرسة السلام المتطورة، أسيوط، مصر" 
                                       target="_blank" 
                                       class="map-link">
                                        أسيوط - مصر
                                    </a>
                                </p>
                                <p style="color: #666; font-size: 0.9rem;">
                                    على ملاعب مدرسة السلام المتطورة
                                </p>
                            </div>
                        </div>
                        
                        <div class="contact-item">
                            <div class="contact-icon">
                                <i class="fas fa-clock"></i>
                            </div>
                            <div>
                                <h4>أوقات العمل</h4>
                                <p>السبت - الخميس: 4:00 مساءً - 9:00 مساءً</p>
                                <p>الجمعة: إجازة</p>
                            </div>
                        </div>
                    </div>
                    
                    <div class="contact-form">
                        <h3>أرسل رسالة</h3>
                        <form id="contactForm">
                            <div class="form-group">
                                <label for="contactName">الاسم</label>
                                <input type="text" id="contactName" name="contactName" placeholder="أدخل اسمك">
                            </div>
                            
                            <div class="form-row">
                                <div class="form-group">
                                    <label for="contactPhone">رقم الهاتف</label>
                                    <input type="tel" id="contactPhone" name="contactPhone" placeholder="010XXXXXXXX">
                                </div>
                            </div>
                            
                            <div class="form-group">
                                <label for="contactSubject">الموضوع</label>
                                <select id="contactSubject" name="contactSubject">
                                    <option value="">اختر الموضوع</option>
                                    <option value="general">استفسار عام</option>
                                    <option value="programs">معلومات عن البرامج</option>
                                    <option value="registration">التسجيل</option>
                                    <option value="other">أخرى</option>
                                </select>
                            </div>
                            
                            <div class="form-group">
                                <label for="contactMessage">الرسالة</label>
                                <textarea id="contactMessage" name="contactMessage" rows="5" placeholder="اكتب رسالتك هنا..."></textarea>
                            </div>
                            
                            <div class="form-group" style="text-align: center; margin-top: 30px;">
                                <button type="submit" class="btn">إرسال الرسالة</button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </section>
    </div>

    <!-- ===== الفوتر ===== -->
    <footer>
        <div class="container">
            <div class="footer-content">
                <div class="footer-about">
                    <div class="footer-logo">
                        <!-- تم تغيير الصورة لقراءة من ملف محلي -->
                        <div class="local-logo" style="width: 50px; height: 50px; border-radius: 8px;">
                            <i class="fas fa-futbol fallback-icon" style="font-size: 2rem;"></i>
                        </div>
                        <h3>الكوتش أكاديمي</h3>
                    </div>
                    <p>تأسست عام 2020 على ملاعب مدرسة السلام المتطورة. أول أكاديمية في مصر تركز على تطوير اللاعب الشامل من الناحية الفنية والبدنية والنفسية، تحت إشراف مدربين معتمدين من الاتحاد الأفريقي CAF.</p>
                    <div class="social-icons">
                        <a href="#"><i class="fab fa-facebook-f"></i></a>
                        <a href="#"><i class="fab fa-instagram"></i></a>
                        <a href="#"><i class="fab fa-tiktok"></i></a>
                        <a href="#"><i class="fab fa-youtube"></i></a>
                    </div>
                </div>
                
                <div class="footer-links">
                    <h4>روابط سريعة</h4>
                    <ul>
                        <li><a href="/" class="nav-link" data-page="home"><i class="fas fa-chevron-left"></i> الرئيسية</a></li>
                        <li><a href="/about" class="nav-link" data-page="about"><i class="fas fa-chevron-left"></i> من نحن</a></li>
                        <li><a href="/programs" class="nav-link" data-page="programs"><i class="fas fa-chevron-left"></i> البرامج التدريبية</a></li>
                        <li><a href="/coaches" class="nav-link" data-page="coaches"><i class="fas fa-chevron-left"></i> المدربون</a></li>
                        <li><a href="/faq" class="nav-link" data-page="faq"><i class="fas fa-chevron-left"></i> الأسئلة الشائعة</a></li>
                    </ul>
                </div>
                
                <div class="footer-contact">
                    <h4>معلومات الاتصال</h4>
                    <ul class="contact-info-footer">
                        <li>
                            <i class="fas fa-map-marker-alt"></i>
                            <span>
                                <a href="https://maps.google.com/?q=مدرسة السلام المتطورة، أسيوط، مصر" 
                                   target="_blank" 
                                   class="map-link">
                                    مصر، أسيوط - على ملاعب مدرسة السلام المتطورة
                                </a>
                            </span>
                        </li>
                        <li>
                            <i class="fas fa-phone"></i>
                            <span>
                                <a href="tel:01069238878" class="phone-link">
                                    01069238878
                                </a>
                            </span>
                        </li>
                        <li>
                            <i class="fab fa-whatsapp"></i>
                            <span>
                                <a href="https://wa.me/201285197778" target="_blank" class="whatsapp-link">
                                    01285197778
                                </a>
                            </span>
                        </li>
                        <li>
                            <i class="fas fa-clock"></i>
                            <span>السبت - الخميس: 4:00م - 9:00م</span>
                        </li>
                    </ul>
                </div>
            </div>
            
            <div class="copyright">
                <p>© 2024 الكوتش أكاديمي. جميع الحقوق محفوظة.</p>
                <p style="margin-top: 5px;">أكاديمية كرة القدم المتخصصة | صناعة أبطال المستقبل</p>
                <p style="margin-top: 5px; font-size: 0.8rem;">تأسست عام 2020 على يد: كابتن ميخا، كابتن اندرو، كابتن مينا</p>
            </div>
        </div>
    </footer>

    <script>
        // ===== التنقل بين الصفحات =====
        document.addEventListener('DOMContentLoaded', function() {
            // عناصر القائمة
            const navLinks = document.querySelectorAll('.nav-link');
            const pages = document.querySelectorAll('.page');
            const burgerMenu = document.getElementById('burgerMenu');
            const sideNav = document.getElementById('sideNav');
            const navOverlay = document.getElementById('navOverlay');
            
            // تحديث الصفحة بناءً على URL
            function updatePageFromUrl() {
                let page = window.location.pathname.substring(1);
                if (page === '' || page === 'index') {
                    page = 'home';
                }
                switchPage(page);
            }
            
            // وظيفة تبديل الصفحة
            function switchPage(pageId) {
                // إخفاء جميع الصفحات
                pages.forEach(page => {
                    page.classList.remove('active');
                });
                
                // إظهار الصفحة المطلوبة
                const targetPage = document.getElementById(pageId + '-page');
                if (targetPage) {
                    targetPage.classList.add('active');
                }
                
                // تحديث القائمة النشطة
                navLinks.forEach(link => {
                    link.classList.remove('active');
                    const linkPage = link.getAttribute('data-page');
                    if (linkPage === pageId) {
                        link.classList.add('active');
                    }
                });
                
                // إغلاق القائمة الجانبية على الهواتف فقط
                if (window.innerWidth <= 992) {
                    if (sideNav) sideNav.classList.remove('active');
                    if (navOverlay) navOverlay.classList.remove('active');
                    if (burgerMenu) burgerMenu.classList.remove('active');
                }
                
                // التمرير لأعلى الصفحة
                window.scrollTo({ top: 0, behavior: 'smooth' });
            }
            
            // إضافة مستمعي الأحداث لروابط التنقل
            navLinks.forEach(link => {
                link.addEventListener('click', function(e) {
                    e.preventDefault();
                    const pageId = this.getAttribute('data-page');
                    window.history.pushState({}, '', '/' + pageId);
                    switchPage(pageId);
                });
            });
            
            // ===== القائمة الجانبية للهواتف فقط =====
            if (burgerMenu) {
                burgerMenu.addEventListener('click', function() {
                    this.classList.toggle('active');
                    if (sideNav) sideNav.classList.toggle('active');
                    if (navOverlay) navOverlay.classList.toggle('active');
                });
            }
            
            if (navOverlay) {
                navOverlay.addEventListener('click', function() {
                    this.classList.remove('active');
                    if (sideNav) sideNav.classList.remove('active');
                    if (burgerMenu) burgerMenu.classList.remove('active');
                });
            }
            
            // إغلاق القائمة الجانبية عند تغيير حجم النافذة
            window.addEventListener('resize', function() {
                if (window.innerWidth > 992) {
                    if (sideNav) sideNav.classList.remove('active');
                    if (navOverlay) navOverlay.classList.remove('active');
                    if (burgerMenu) burgerMenu.classList.remove('active');
                }
            });
            
            // ===== الأسئلة الشائعة =====
            const faqItems = document.querySelectorAll('.faq-item');
            faqItems.forEach(item => {
                const question = item.querySelector('.faq-question');
                if (question) {
                    question.addEventListener('click', function() {
                        // إغلاق جميع العناصر الأخرى
                        faqItems.forEach(otherItem => {
                            if (otherItem !== item) {
                                otherItem.classList.remove('active');
                            }
                        });
                        
                        // تبديل العنصر الحالي
                        item.classList.toggle('active');
                    });
                }
            });
            
            // ===== إرسال نموذج التسجيل =====
            const registrationForm = document.getElementById('registrationForm');
            const successMessage = document.getElementById('successMessage');
            
            if (registrationForm) {
                registrationForm.addEventListener('submit', async function(e) {
                    e.preventDefault();
                    
                    // جمع البيانات
                    const formData = {
                        playerName: document.getElementById('playerName').value,
                        ageGroup: document.getElementById('ageGroup').value,
                        parentName: document.getElementById('parentName').value,
                        parentPhone: document.getElementById('parentPhone').value,
                        notes: document.getElementById('notes').value
                    };
                    
                    try {
                        const response = await fetch('/api/register', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify(formData)
                        });
                        
                        const result = await response.json();
                        
                        if (result.success) {
                            successMessage.style.display = 'block';
                            window.scrollTo({ top: 0, behavior: 'smooth' });
                            
                            setTimeout(() => {
                                successMessage.style.display = 'none';
                                registrationForm.reset();
                                window.history.pushState({}, '', '/');
                                switchPage('home');
                            }, 3000);
                        } else {
                            alert('حدث خطأ في إرسال الطلب. يرجى المحاولة مرة أخرى.');
                        }
                    } catch (error) {
                        console.error('Error:', error);
                        alert('حدث خطأ في الاتصال بالخادم. يرجى المحاولة مرة أخرى.');
                    }
                });
            }
            
            // ===== إرسال نموذج الاتصال =====
            const contactForm = document.getElementById('contactForm');
            if (contactForm) {
                contactForm.addEventListener('submit', async function(e) {
                    e.preventDefault();
                    
                    const formData = {
                        name: document.getElementById('contactName')?.value || '',
                        phone: document.getElementById('contactPhone')?.value || '',
                        subject: document.getElementById('contactSubject')?.value || '',
                        message: document.getElementById('contactMessage')?.value || ''
                    };
                    
                    try {
                        const response = await fetch('/api/contact', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify(formData)
                        });
                        
                        const result = await response.json();
                        
                        if (result.success) {
                            alert('شكراً لتواصلك معنا! تم إرسال رسالتك بنجاح وسنرد عليك خلال 24 ساعة.');
                            contactForm.reset();
                        } else {
                            alert('حدث خطأ في إرسال الرسالة. يرجى المحاولة مرة أخرى.');
                        }
                    } catch (error) {
                        console.error('Error:', error);
                        alert('حدث خطأ في الاتصال بالخادم. يرجى المحاولة مرة أخرى.');
                    }
                });
            }
            
            // ===== تأثيرات التمرير للهيدر =====
            let lastScrollTop = 0;
            const header = document.getElementById('header');
            
            window.addEventListener('scroll', function() {
                const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
                
                if (scrollTop > 100) {
                    header.style.backgroundColor = 'rgba(255, 255, 255, 0.98)';
                    header.style.boxShadow = '0 4px 20px rgba(0, 0, 0, 0.1)';
                } else {
                    header.style.backgroundColor = 'rgba(255, 255, 255, 0.95)';
                    header.style.boxShadow = 'var(--shadow)';
                }
                
                lastScrollTop = scrollTop;
            });
            
            // ===== معالج التنقل عبر التاريخ =====
            window.addEventListener('popstate', function() {
                updatePageFromUrl();
            });
            
            // ===== الصفحة الافتراضية =====
            updatePageFromUrl();
            
            // ===== تحميل الصور المحلية =====
            function loadLocalImages() {
                // محاولة تحميل الصورة المحلية
                const logoImg = new Image();
                logoImg.src = 'logo.jpg'; // اسم ملف الصورة المحلية
                logoImg.onload = function() {
                    // استبدال الأيقونات بالصورة
                    document.querySelectorAll('.local-logo').forEach(el => {
                        if (el.tagName === 'DIV') {
                            el.style.backgroundImage = `url('logo.jpg')`;
                            el.style.backgroundSize = 'cover';
                            el.style.backgroundPosition = 'center';
                            el.innerHTML = ''; // إزالة الأيقونة
                        }
                    });
                };
                logoImg.onerror = function() {
                    // إذا فشل تحميل الصورة، استمر باستخدام الأيقونات
                    console.log('لم يتم العثور على صورة محلية، سيتم استخدام الأيقونات');
                };
            }
            
            // محاولة تحميل الصور المحلية
            loadLocalImages();
        });
    </script>
</body>
</html>
'''

# ملف لحفظ البيانات
DATA_FILE = 'registrations.json'
CONTACT_FILE = 'contacts.json'

def save_registration(data):
    """حفظ بيانات التسجيل في ملف JSON"""
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                registrations = json.load(f)
        else:
            registrations = []
        
        data['timestamp'] = datetime.now().isoformat()
        registrations.append(data)
        
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(registrations, f, ensure_ascii=False, indent=2)
        
        return True
    except Exception as e:
        print(f"Error saving registration: {e}")
        return False

def save_contact(data):
    """حفظ بيانات الاتصال في ملف JSON"""
    try:
        if os.path.exists(CONTACT_FILE):
            with open(CONTACT_FILE, 'r', encoding='utf-8') as f:
                contacts = json.load(f)
        else:
            contacts = []
        
        data['timestamp'] = datetime.now().isoformat()
        contacts.append(data)
        
        with open(CONTACT_FILE, 'w', encoding='utf-8') as f:
            json.dump(contacts, f, ensure_ascii=False, indent=2)
        
        return True
    except Exception as e:
        print(f"Error saving contact: {e}")
        return False

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/about')
def about():
    return render_template_string(HTML_TEMPLATE)

@app.route('/programs')
def programs():
    return render_template_string(HTML_TEMPLATE)

@app.route('/coaches')
def coaches():
    return render_template_string(HTML_TEMPLATE)

@app.route('/registration')
def registration():
    return render_template_string(HTML_TEMPLATE)

@app.route('/faq')
def faq():
    return render_template_string(HTML_TEMPLATE)

@app.route('/contact')
def contact():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/register', methods=['POST'])
def api_register():
    data = request.get_json()
    if save_registration(data):
        return jsonify({'success': True, 'message': 'تم تسجيل البيانات بنجاح'})
    return jsonify({'success': False, 'message': 'حدث خطأ في حفظ البيانات'}), 500

@app.route('/api/contact', methods=['POST'])
def api_contact():
    data = request.get_json()
    if save_contact(data):
        return jsonify({'success': True, 'message': 'تم إرسال الرسالة بنجاح'})
    return jsonify({'success': False, 'message': 'حدث خطأ في حفظ البيانات'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)