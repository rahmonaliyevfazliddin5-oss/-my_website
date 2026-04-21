# -*- coding: utf-8 -*-
import os
import json
import uuid
from datetime import datetime
from flask import Flask, request, jsonify

app = Flask(__name__, static_folder=None)

# ---------- Ma'lumotlar papkasi ----------
DATA_DIR = 'data'
os.makedirs(DATA_DIR, exist_ok=True)

def read_json(filename):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def write_json(filename, data):
    path = os.path.join(DATA_DIR, filename)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ---------- API ----------
@app.route('/api/users', methods=['GET'])
def get_users():
    return jsonify(read_json('users.json'))

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.json
    users = read_json('users.json')
    if any(u['phone'] == data['phone'] for u in users):
        return jsonify({'error': 'Bu telefon allaqachon ro\'yxatdan o\'tgan'}), 400
    new_user = {
        'id': str(uuid.uuid4()),
        'firstName': data['firstName'],
        'lastName': data['lastName'],
        'phone': data['phone'],
        'password': data['password'],
        'photo': data.get('photo', ''),
        'registeredAt': datetime.now().isoformat()
    }
    users.append(new_user)
    write_json('users.json', users)
    return jsonify(new_user), 201

@app.route('/api/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    users = read_json('users.json')
    idx = next((i for i, u in enumerate(users) if u['id'] == user_id), None)
    if idx is None:
        return jsonify({'error': 'Foydalanuvchi topilmadi'}), 404
    data = request.json
    if 'oldPassword' in data and 'newPassword' in data:
        if users[idx]['password'] != data['oldPassword']:
            return jsonify({'error': 'Eski parol noto\'g\'ri'}), 400
        users[idx]['password'] = data['newPassword']
    if 'firstName' in data:
        users[idx]['firstName'] = data['firstName']
    if 'lastName' in data:
        users[idx]['lastName'] = data['lastName']
    if 'photo' in data:
        users[idx]['photo'] = data['photo']
    write_json('users.json', users)
    return jsonify(users[idx])

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    users = read_json('users.json')
    user = next((u for u in users if u['phone'] == data['phone'] and u['password'] == data['password']), None)
    if user:
        return jsonify(user)
    return jsonify({'error': 'Telefon yoki parol noto\'g\'ri'}), 401

@app.route('/api/events', methods=['GET'])
def get_events():
    return jsonify(read_json('events.json'))

@app.route('/api/events', methods=['POST'])
def create_event():
    data = request.json
    events = read_json('events.json')
    new_event = {
        'id': str(uuid.uuid4()),
        'name': data['name'],
        'date': data['date'],
        'desc': data.get('desc', ''),
        'plan': data['plan'],
        'traffic': data.get('traffic', '5K'),
        'user': data.get('user', 'Admin'),
        'createdAt': datetime.now().isoformat()
    }
    events.append(new_event)
    write_json('events.json', events)
    return jsonify(new_event), 201

@app.route('/api/requests', methods=['GET'])
def get_requests():
    return jsonify(read_json('requests.json'))

@app.route('/api/requests', methods=['POST'])
def create_request():
    data = request.json
    reqs = read_json('requests.json')
    new_req = {
        'id': str(uuid.uuid4()),
        'firstName': data['firstName'],
        'lastName': data['lastName'],
        'phone': data['phone'],
        'eventName': data['eventName'],
        'eventDate': data['eventDate'],
        'plan': data['plan'],
        'eventDesc': data.get('eventDesc', ''),
        'status': data.get('status', 'pending'),
        'createdAt': datetime.now().isoformat()
    }
    reqs.append(new_req)
    write_json('requests.json', reqs)
    return jsonify(new_req), 201

@app.route('/api/requests/<req_id>', methods=['PUT'])
def update_request(req_id):
    reqs = read_json('requests.json')
    idx = next((i for i, r in enumerate(reqs) if r['id'] == req_id), None)
    if idx is None:
        return jsonify({'error': 'Taklif topilmadi'}), 404
    data = request.json
    if 'status' in data:
        reqs[idx]['status'] = data['status']
    write_json('requests.json', reqs)
    return jsonify(reqs[idx])

@app.route('/api/requests/<req_id>', methods=['DELETE'])
def delete_request(req_id):
    reqs = read_json('requests.json')
    new_reqs = [r for r in reqs if r['id'] != req_id]
    write_json('requests.json', new_reqs)
    return '', 204

# ---------- FRONTEND (AYNAN SIZ BERGAN DIZAYN) ----------
@app.route('/')
def index():
    return HTML_CONTENT

# ---------- Demo ma'lumotlar ----------
def init_demo():
    users = read_json('users.json')
    if not any(u['phone'] == '998901234567' for u in users):
        users.append({
            'id': str(uuid.uuid4()),
            'firstName': 'Admin',
            'lastName': 'User',
            'phone': '998901234567',
            'password': '123',
            'photo': '',
            'registeredAt': datetime.now().isoformat()
        })
        write_json('users.json', users)
    events = read_json('events.json')
    if not events:
        events = [
            {'id': str(uuid.uuid4()), 'name': 'Texnologiya sammiti', 'date': '2026-06-15', 'desc': 'Sunʼiy intellekt', 'plan': 'Pro', 'traffic': '50K+', 'user': 'Admin'},
            {'id': str(uuid.uuid4()), 'name': 'Marketing konferensiyasi', 'date': '2026-05-22', 'desc': 'Raqamli strategiya', 'plan': 'Medium', 'traffic': '20K', 'user': 'Admin'}
        ]
        write_json('events.json', events)

# ---------- SIZNING HTML KODINGIZ (O'ZGARTIRILGAN) ----------
HTML_CONTENT = '''
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=yes, viewport-fit=cover">
  <title>✨ TadbirMarkaz – Admin tasdiqlovchi platforma</title>
  <!-- AOS animatsiya kutubxonasi -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/aos/2.3.4/aos.css">
  <!-- Font Awesome 6 -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.1/css/all.min.css">
  <!-- Google Fonts: Inter zamonaviy shrift -->
  <link href="https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400&display=swap" rel="stylesheet">
  <style>
    /* ==================== GLOBAL STILLAR ==================== */
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }

    body {
      font-family: 'Inter', sans-serif;
      background: #f9fafc;
      color: #1e1f2a;
      line-height: 1.6;
      overflow-x: hidden;
      -webkit-font-smoothing: antialiased;
    }

    /* CSS o'zgaruvchilari */
    :root {
      --primary: #4361ee;
      --primary-light: #4895ef;
      --primary-dark: #3a56d4;
      --secondary: #3f37c9;
      --accent: #f72585;
      --accent-light: #ff5fa2;
      --dark: #1e1f2a;
      --gray: #6c757d;
      --gray-light: #a0a8b8;
      --light-bg: #ffffff;
      --bg-soft: #f8faff;
      --card-shadow: 0 20px 35px -10px rgba(0, 0, 0, 0.05), 0 8px 15px -6px rgba(0, 0, 0, 0.02);
      --card-shadow-hover: 0 30px 45px -12px rgba(67, 97, 238, 0.15), 0 10px 20px -8px rgba(0,0,0,0.05);
      --glass-bg: rgba(255, 255, 255, 0.75);
      --border-radius-card: 28px;
      --border-radius-sm: 18px;
      --transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    }

    .container {
      max-width: 1300px;
      margin: 0 auto;
      padding: 0 28px;
    }

    section {
      padding: 90px 0;
      position: relative;
    }

    h1, h2, h3, h4 {
      font-weight: 700;
      letter-spacing: -0.02em;
      line-height: 1.2;
    }

    h2 {
      font-size: 2.9rem;
      margin-bottom: 20px;
      background: linear-gradient(135deg, #1e1f2a 0%, #3a3f5e 100%);
      -webkit-background-clip: text;
      background-clip: text;
      color: transparent;
    }

    .section-subhead {
      font-size: 1.2rem;
      color: var(--gray);
      margin-bottom: 50px;
      font-weight: 400;
      max-width: 700px;
    }

    /* Tugmalar */
    .btn {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 10px;
      padding: 15px 36px;
      border-radius: 60px;
      font-weight: 600;
      font-size: 1rem;
      transition: var(--transition);
      cursor: pointer;
      border: none;
      background: white;
      color: var(--dark);
      box-shadow: 0 6px 16px rgba(0, 0, 0, 0.03);
      text-decoration: none;
      border: 1.5px solid rgba(0,0,0,0.02);
      backdrop-filter: blur(4px);
      white-space: nowrap;
    }

    .btn-primary {
      background: var(--primary);
      color: white;
      box-shadow: 0 14px 28px -10px rgba(67, 97, 238, 0.4);
      border: none;
    }

    .btn-primary:hover {
      background: var(--primary-dark);
      transform: translateY(-5px);
      box-shadow: 0 24px 36px -12px rgba(67, 97, 238, 0.5);
    }

    .btn-outline {
      background: transparent;
      border: 1.8px solid var(--primary);
      color: var(--primary);
    }

    .btn-outline:hover {
      background: var(--primary);
      color: white;
      transform: scale(1.02);
    }

    .btn-accent {
      background: var(--accent);
      color: white;
      box-shadow: 0 10px 20px -5px rgba(247, 37, 133, 0.3);
    }

    .btn-sm {
      padding: 10px 22px;
      font-size: 0.9rem;
    }

    /* ==================== HEADER ==================== */
    .site-header {
      position: sticky;
      top: 0;
      z-index: 100;
      backdrop-filter: blur(18px);
      background: rgba(255, 255, 255, 0.8);
      border-bottom: 1px solid rgba(255,255,255,0.5);
      padding: 18px 0;
      transition: var(--transition);
    }

    .header-inner {
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    .logo {
      font-size: 2.2rem;
      font-weight: 800;
      letter-spacing: -0.03em;
      background: linear-gradient(145deg, var(--primary), var(--accent));
      -webkit-background-clip: text;
      background-clip: text;
      color: transparent;
      text-shadow: 0 2px 10px rgba(67,97,238,0.1);
    }

    .nav-links {
      display: flex;
      gap: 42px;
      align-items: center;
    }

    .nav-links a {
      text-decoration: none;
      color: var(--dark);
      font-weight: 600;
      font-size: 1.05rem;
      transition: color 0.2s;
      position: relative;
    }

    .nav-links a:hover {
      color: var(--primary);
    }

    .admin-btn-header {
      margin-left: 15px;
      background: rgba(67, 97, 238, 0.08);
      border: 1px solid rgba(67,97,238,0.2);
      padding: 12px 24px;
      border-radius: 40px;
      font-weight: 600;
      color: var(--primary);
      cursor: pointer;
      transition: var(--transition);
    }

    .admin-btn-header:hover {
      background: var(--primary);
      color: white;
    }

    .mobile-menu-btn {
      display: none;
      background: none;
      border: none;
      font-size: 2rem;
      color: var(--dark);
    }

    /* ==================== HERO ==================== */
    .hero {
      padding: 40px 0 100px;
    }

    .hero-grid {
      display: grid;
      grid-template-columns: 1.2fr 1fr;
      gap: 50px;
      align-items: center;
    }

    .hero h1 {
      font-size: 4rem;
      line-height: 1.15;
      margin-bottom: 28px;
    }

    .hero-highlight {
      color: var(--primary);
      position: relative;
      display: inline-block;
    }

    .hero-highlight::after {
      content: '';
      position: absolute;
      bottom: 8px;
      left: 0;
      width: 100%;
      height: 14px;
      background: rgba(247, 37, 133, 0.15);
      z-index: -1;
      border-radius: 20px;
    }

    .hero p {
      font-size: 1.25rem;
      color: #4a4e6b;
      margin-bottom: 40px;
    }

    .hero-buttons {
      display: flex;
      gap: 20px;
      flex-wrap: wrap;
    }

    .hero-visual {
      background: radial-gradient(circle at 30% 20%, rgba(67, 97, 238, 0.1), transparent 70%);
      padding: 30px;
      border-radius: 60px;
      animation: float 7s infinite ease-in-out;
    }

    .hero-visual i {
      font-size: 16rem;
      color: var(--primary-light);
      filter: drop-shadow(0 30px 40px rgba(67, 97, 238, 0.2));
    }

    @keyframes float {
      0%, 100% { transform: translateY(0px); }
      50% { transform: translateY(-20px); }
    }

    /* ==================== PRICING ==================== */
    .pricing-cards {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 35px;
    }

    .pricing-card {
      background: var(--light-bg);
      border-radius: var(--border-radius-card);
      padding: 42px 32px;
      box-shadow: var(--card-shadow);
      transition: var(--transition);
      border: 1.5px solid rgba(255,255,255,0.6);
      backdrop-filter: blur(8px);
      position: relative;
      text-align: left;
    }

    .pricing-card:hover {
      transform: translateY(-15px);
      box-shadow: var(--card-shadow-hover);
      border-color: var(--primary-light);
    }

    .popular-badge {
      position: absolute;
      top: -16px;
      left: 50%;
      transform: translateX(-50%);
      background: var(--accent);
      color: white;
      padding: 8px 22px;
      border-radius: 40px;
      font-size: 1rem;
      font-weight: 700;
      box-shadow: 0 10px 15px rgba(247, 37, 133, 0.3);
    }

    .plan-name {
      font-size: 2rem;
      font-weight: 700;
      margin-bottom: 15px;
    }

    .plan-price {
      font-size: 3.5rem;
      font-weight: 800;
      color: var(--dark);
      margin: 25px 0 10px;
    }

    .plan-features {
      list-style: none;
      margin: 35px 0 30px;
    }

    .plan-features li {
      padding: 12px 0;
      display: flex;
      align-items: center;
      gap: 15px;
      border-bottom: 1px dashed #e0e4f0;
    }

    /* ==================== TADBIRLAR RO'YXATI ==================== */
    .events-header {
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      flex-wrap: wrap;
      margin-bottom: 40px;
    }

    .events-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
      gap: 30px;
    }

    .event-card {
      background: white;
      border-radius: 26px;
      padding: 28px;
      box-shadow: var(--card-shadow);
      transition: var(--transition);
      border-left: 7px solid var(--primary);
      backdrop-filter: blur(4px);
    }

    .event-badge {
      display: inline-block;
      padding: 6px 18px;
      border-radius: 40px;
      font-size: 0.85rem;
      font-weight: 700;
      margin-bottom: 18px;
    }

    .badge-free { background: #e9ecef; color: #1e1f2a; }
    .badge-medium { background: #fff3cd; color: #856404; }
    .badge-pro { background: #d4edda; color: #0f5132; }

    .event-title {
      font-size: 1.6rem;
      margin-bottom: 14px;
    }

    .event-date {
      display: flex;
      align-items: center;
      gap: 10px;
      color: var(--gray);
      margin-bottom: 20px;
    }

    /* ==================== TADBIR QO'SHISH FORMASI ==================== */
    .add-event-section {
      background: linear-gradient(145deg, #ffffff 0%, #f2f7ff 100%);
      border-radius: 56px;
      padding: 56px 50px;
      margin-top: 50px;
      box-shadow: var(--card-shadow);
      border: 1px solid rgba(255,255,255,0.8);
    }

    .form-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 28px;
    }

    .form-group {
      display: flex;
      flex-direction: column;
      gap: 10px;
    }

    .form-control {
      padding: 16px 22px;
      border: 2px solid #e0e6f2;
      border-radius: 50px;
      font-size: 1rem;
      transition: 0.2s;
      background: white;
      font-family: inherit;
    }

    .form-control:focus {
      border-color: var(--primary);
      outline: none;
      box-shadow: 0 0 0 5px rgba(67,97,238,0.1);
    }

    /* ==================== ADMIN MODAL ==================== */
    .modal-overlay {
      position: fixed;
      top: 0; left: 0; width: 100%; height: 100%;
      background: rgba(0,0,0,0.3);
      backdrop-filter: blur(10px);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 1000;
      visibility: hidden;
      opacity: 0;
      transition: 0.25s;
    }

    .modal {
      background: white;
      border-radius: 48px;
      padding: 40px;
      max-width: 1100px;
      width: 95%;
      max-height: 85vh;
      overflow-y: auto;
      box-shadow: 0 50px 80px rgba(0,0,0,0.2);
    }

    .modal-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 30px;
    }

    .close-btn {
      font-size: 32px;
      background: none;
      border: none;
      cursor: pointer;
      color: var(--gray);
    }

    .admin-tabs {
      display: flex;
      gap: 15px;
      border-bottom: 1px solid #e0e6f2;
      padding-bottom: 15px;
      margin-bottom: 25px;
    }

    .admin-tab {
      padding: 10px 24px;
      border-radius: 40px;
      font-weight: 600;
      cursor: pointer;
      background: #f1f4fe;
      color: var(--dark);
    }

    .admin-tab.active {
      background: var(--primary);
      color: white;
    }

    .admin-table {
      width: 100%;
      border-collapse: collapse;
    }

    .admin-table th {
      text-align: left;
      padding: 16px 8px;
      background: #f4f6fc;
      font-weight: 600;
    }

    .admin-table td {
      padding: 16px 8px;
      border-bottom: 1px solid #eaeef5;
    }

    .status-badge {
      padding: 6px 16px;
      border-radius: 40px;
      background: #fff3cd;
      color: #856404;
      font-weight: 600;
    }

    .status-approved {
      background: #d4edda;
      color: #0f5132;
    }

    /* ==================== TOAST ==================== */
    .toast-message {
      background: #1e1f2a;
      color: white;
      padding: 16px 32px;
      border-radius: 60px;
      position: fixed;
      bottom: 35px;
      left: 50%;
      transform: translateX(-50%);
      z-index: 9999;
      box-shadow: 0 30px 40px rgba(0,0,0,0.25);
      animation: slideUp 0.35s;
      font-weight: 500;
    }

    @keyframes slideUp {
      from { opacity: 0; transform: translate(-50%, 30px); }
      to { opacity: 1; transform: translate(-50%, 0); }
    }

    /* ==================== RESPONSIVE ==================== */
    @media (max-width: 1000px) {
      h2 { font-size: 2.4rem; }
      .hero h1 { font-size: 3rem; }
      .hero-grid { grid-template-columns: 1fr; }
      .hero-visual i { font-size: 12rem; }
      .pricing-cards { grid-template-columns: 1fr; }
      .form-grid { grid-template-columns: 1fr; }
    }

    @media (max-width: 750px) {
      .nav-links { display: none; }
      .mobile-menu-btn { display: block; }
      .container { padding: 0 20px; }
      .add-event-section { padding: 36px 24px; }
      .modal { padding: 24px; }
    }

    /* qo'shimcha dekorativ stillar */
    .stat-badge {
      background: rgba(67,97,238,0.1);
      border-radius: 40px;
      padding: 6px 18px;
      display: inline-block;
    }
    footer {
      padding: 35px 0;
      border-top: 1px solid rgba(0,0,0,0.05);
    }
  </style>
</head>
<body>

<!-- HEADER -->
<header class="site-header" data-aos="fade-down" data-aos-duration="800">
  <div class="container header-inner">
    <div class="logo">✨ TadbirMarkaz</div>
    <nav class="nav-links">
      <a href="#home">Bosh sahifa</a>
      <a href="#events">Tadbirlar</a>
      <a href="#pricing">Narxlar</a>
      <a href="#contact">Bog‘lanish</a>
      <button class="admin-btn-header" id="adminBtn"><i class="fas fa-lock"></i> Admin panel</button>
    </nav>
    <button class="mobile-menu-btn"><i class="fas fa-bars"></i></button>
  </div>
</header>

<main>
  <!-- HERO -->
  <section id="home" class="hero">
    <div class="container hero-grid">
      <div data-aos="fade-right" data-aos-duration="1000">
        <h1>Katta tadbirlarni <span class="hero-highlight">osonlik bilan</span> rejalashtiring</h1>
        <p>Ro‘yxatdan o‘ting, sanani kiriting, tarif tanlang. Admin tasdiqlaydi – tadbiringiz saytda paydo bo‘ladi.</p>
        <div class="hero-buttons">
          <a href="#add-event" class="btn btn-primary"><i class="fas fa-calendar-plus"></i> Tadbir taklif qilish</a>
          <a href="#pricing" class="btn btn-outline"><i class="fas fa-tags"></i> Narxlarni solishtirish</a>
        </div>
      </div>
      <div class="hero-visual" data-aos="fade-left" data-aos-delay="200"><i class="fas fa-calendar-alt"></i></div>
    </div>
  </section>

  <!-- PRICING -->
  <section id="pricing" data-aos="fade-up">
    <div class="container">
      <h2>🚀 Trafik va narx paketlari</h2>
      <div class="section-subhead">Tadbiringiz ko‘lamiga mos variantni tanlang. Pullik tariflar admin tasdiqlashini kutadi.</div>
      <div class="pricing-cards">
        <div class="pricing-card" data-aos="zoom-in" data-aos-delay="0">
          <div class="plan-name">🆓 Free</div>
          <div class="plan-price">$0 <small>/ tadbir</small></div>
          <ul class="plan-features">
            <li><i class="fas fa-check-circle" style="color:var(--primary);"></i> 1 ta tadbir</li>
            <li><i class="fas fa-check-circle" style="color:var(--primary);"></i> 5K trafik</li>
            <li><i class="fas fa-check-circle" style="color:var(--primary);"></i> Avtomatik tasdiqlash</li>
          </ul>
        </div>
        <div class="pricing-card popular" data-aos="zoom-in" data-aos-delay="150">
          <div class="popular-badge">🔥 Ommabop</div>
          <div class="plan-name">📊 Medium</div>
          <div class="plan-price">$12 <small>/ oy</small></div>
          <ul class="plan-features">
            <li><i class="fas fa-check-circle" style="color:var(--primary);"></i> 3 ta tadbir</li>
            <li><i class="fas fa-check-circle" style="color:var(--primary);"></i> 20K trafik</li>
            <li><i class="fas fa-check-circle" style="color:var(--primary);"></i> Admin tasdiqlaydi</li>
          </ul>
        </div>
        <div class="pricing-card" data-aos="zoom-in" data-aos-delay="300">
          <div class="plan-name">💎 Pro</div>
          <div class="plan-price">$20 <small>/ oy</small></div>
          <ul class="plan-features">
            <li><i class="fas fa-check-circle" style="color:var(--primary);"></i> Cheksiz tadbirlar</li>
            <li><i class="fas fa-check-circle" style="color:var(--primary);"></i> 50K+ trafik</li>
            <li><i class="fas fa-check-circle" style="color:var(--primary);"></i> Admin tasdiqlaydi</li>
          </ul>
        </div>
      </div>
    </div>
  </section>

  <!-- TASDIQLANGAN TADBIRLAR -->
  <section id="events">
    <div class="container">
      <div class="events-header">
        <div>
          <h2 data-aos="fade-right">📅 Rejalashtirilgan tadbirlar</h2>
          <div class="section-subhead">Admin tomonidan tasdiqlangan tadbirlar ro‘yxati</div>
        </div>
        <button class="btn btn-primary" onclick="scrollToAddEvent()"><i class="fas fa-plus-circle"></i> Taklif yuborish</button>
      </div>
      <div id="eventsContainer" class="events-grid"></div>
    </div>
  </section>

  <!-- TADBIR TAKLIF QILISH FORMASI -->
  <section id="add-event">
    <div class="container">
      <div class="add-event-section" data-aos="flip-up">
        <h2 style="color: #1e1f2a;">📝 Ro‘yxatdan o‘ting va tadbir taklif qiling</h2>
        <p style="margin-bottom: 40px;">Ism, familiya, telefon raqamingizni kiriting. Free tarif avtomatik tasdiqlanadi, Medium/Pro admin tomonidan ochiladi.</p>
        <form id="eventRequestForm">
          <div class="form-grid">
            <div class="form-group"><label>Ismingiz</label><input type="text" id="firstName" class="form-control" placeholder="Ali" required></div>
            <div class="form-group"><label>Familiyangiz</label><input type="text" id="lastName" class="form-control" placeholder="Valiyev" required></div>
            <div class="form-group"><label>Telefon raqam</label><input type="tel" id="phone" class="form-control" placeholder="+998 90 123 45 67" required></div>
            <div class="form-group"><label>Tadbir nomi</label><input type="text" id="eventName" class="form-control" placeholder="Masalan: IT Sammit 2026" required></div>
            <div class="form-group"><label>Tadbir sanasi</label><input type="date" id="eventDate" class="form-control" required></div>
            <div class="form-group"><label>Tarif tanlang</label>
              <select id="eventPlan" class="form-control">
                <option value="Free">🆓 Free (avtomatik)</option>
                <option value="Medium" selected>📊 Medium ($12) - admin tasdiqlaydi</option>
                <option value="Pro">💎 Pro ($20) - admin tasdiqlaydi</option>
              </select>
            </div>
          </div>
          <div class="form-group"><label>Qo‘shimcha izoh</label><input id="eventDesc" class="form-control" placeholder="Tadbir haqida qisqacha"></div>
          <button type="submit" class="btn btn-primary" style="margin-top: 35px;"><i class="fas fa-paper-plane"></i> Taklifni yuborish</button>
        </form>
      </div>
    </div>
  </section>

  <!-- CONTACT -->
  <section id="contact">
    <div class="container">
      <h2>📞 Bog‘lanish</h2>
      <div style="display:flex; gap:40px; flex-wrap:wrap;">
        <div><i class="fas fa-phone"></i> +998 90 123 45 67</div>
        <div><i class="fas fa-envelope"></i> hello@tadbirmarkaz.uz</div>
        <div><i class="fas fa-map-marker-alt"></i> Toshkent, Amir Temur 15</div>
      </div>
    </div>
  </section>
</main>

<footer><div class="container">© 2026 TadbirMarkaz – Katta tadbirlar uchun ishonchli platforma</div></footer>

<!-- ADMIN MODAL -->
<div class="modal-overlay" id="adminModal">
  <div class="modal">
    <div class="modal-header">
      <h3><i class="fas fa-user-shield"></i> Admin panel – Boshqaruv</h3>
      <button class="close-btn" onclick="closeAdminModal()">&times;</button>
    </div>
    <div class="admin-tabs">
      <span class="admin-tab active" data-tab="users">👥 Foydalanuvchilar</span>
      <span class="admin-tab" data-tab="requests">📋 Takliflar</span>
      <span class="admin-tab" data-tab="addEvent">➕ Tadbir qo'shish</span>
    </div>
    <div id="adminUsersPanel"></div>
    <div id="adminRequestsPanel" style="display:none;"></div>
    <div id="adminAddEventPanel" style="display:none;">
      <form id="adminAddEventForm" style="display:grid; gap:20px; margin-top:20px;">
        <input type="text" id="adminEventName" class="form-control" placeholder="Tadbir nomi" required>
        <input type="date" id="adminEventDate" class="form-control" required>
        <input type="text" id="adminEventDesc" class="form-control" placeholder="Tavsif">
        <select id="adminEventPlan" class="form-control">
          <option value="Free">🆓 Free</option>
          <option value="Medium">📊 Medium ($12)</option>
          <option value="Pro">💎 Pro ($20)</option>
        </select>
        <button type="submit" class="btn btn-primary"><i class="fas fa-plus"></i> Tadbir qo'shish</button>
      </form>
    </div>
    <button class="btn btn-outline" style="margin-top: 25px;" onclick="closeAdminModal()">Yopish</button>
  </div>
</div>

<!-- TOAST -->
<div id="toast" class="toast-message" style="display: none;"></div>

<!-- AOS va asosiy JS -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/aos/2.3.4/aos.js"></script>
<script>
  const API_URL = '/api';
  const ADMIN_PASSWORD = 'farangiz a';

  // Toast
  function showToast(msg, isSuccess = true) {
    const toast = document.getElementById('toast');
    toast.style.display = 'block';
    toast.textContent = msg;
    toast.style.background = isSuccess ? '#1e1f2a' : '#b02a37';
    setTimeout(() => { toast.style.display = 'none'; }, 3500);
  }

  // API funksiyalar
  async function apiGet(url) { const res = await fetch(API_URL + url); return res.json(); }
  async function apiPost(url, data) { const res = await fetch(API_URL + url, { method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(data) }); return res.json(); }
  async function apiPut(url, data) { const res = await fetch(API_URL + url, { method:'PUT', headers:{'Content-Type':'application/json'}, body:JSON.stringify(data) }); return res.json(); }
  async function apiDelete(url) { await fetch(API_URL + url, { method:'DELETE' }); }

  // LocalStorage
  function getCurrentUser() { return JSON.parse(localStorage.getItem('currentUser')); }
  function setCurrentUser(u) { localStorage.setItem('currentUser', JSON.stringify(u)); }
  function logout() { localStorage.removeItem('currentUser'); location.reload(); }

  // ---------- TADBIRLARNI RENDER QILISH ----------
  async function renderEvents() {
    const container = document.getElementById('eventsContainer');
    const events = await apiGet('/events');
    if (!events.length) {
      container.innerHTML = '<p style="grid-column:1/-1; text-align:center; padding:50px;">Hali tasdiqlangan tadbirlar yo‘q.</p>';
      return;
    }
    let html = '';
    events.sort((a,b)=> new Date(a.date) - new Date(b.date));
    events.forEach(ev => {
      let badge = ev.plan === 'Free' ? 'badge-free' : (ev.plan==='Medium'?'badge-medium':'badge-pro');
      const sana = new Date(ev.date).toLocaleDateString('uz-UZ', {year:'numeric', month:'long', day:'numeric'});
      html += `<div class="event-card" data-aos="fade-up"><span class="event-badge ${badge}">${ev.plan}</span>
        <h3 class="event-title">${ev.name}</h3><div class="event-date"><i class="far fa-calendar-check"></i> ${sana}</div>
        <p>${ev.desc}</p><div>👥 ${ev.traffic}</div><small>${ev.user || ''}</small></div>`;
    });
    container.innerHTML = html;
  }

  // ---------- ADMIN PANEL ----------
  async function renderAdminPanel() {
    const users = await apiGet('/users');
    const reqs = await apiGet('/requests');

    // Users
    let usersHtml = `<table class="admin-table"><tr><th>Ism</th><th>Familiya</th><th>Telefon</th><th>Ro'yxatdan o'tgan</th></tr>`;
    users.forEach(u => usersHtml += `<tr><td>${u.firstName}</td><td>${u.lastName}</td><td>${u.phone}</td><td>${new Date(u.registeredAt).toLocaleString()}</td></tr>`);
    document.getElementById('adminUsersPanel').innerHTML = usersHtml;

    // Requests
    let reqHtml = `<table class="admin-table"><tr><th>F.I.Sh</th><th>Tel</th><th>Tadbir</th><th>Sana</th><th>Tarif</th><th>Holat</th><th>Amal</th></tr>`;
    reqs.forEach(req => {
      reqHtml += `<tr><td>${req.firstName} ${req.lastName}</td><td>${req.phone}</td><td>${req.eventName}</td><td>${req.eventDate}</td><td>${req.plan}</td><td>${req.status}</td><td>`;
      if(req.status!=='approved') reqHtml += `<button class="btn btn-sm btn-outline" onclick="window.approveRequest('${req.id}')">Tasdiqlash</button> `;
      reqHtml += `<button class="btn btn-sm" onclick="window.deleteRequest('${req.id}')">O'chirish</button></td></tr>`;
    });
    document.getElementById('adminRequestsPanel').innerHTML = reqHtml + '</table>';

    window.approveRequest = async (id) => {
      const req = reqs.find(r=>r.id===id);
      if(!req) return;
      await apiPut('/requests/'+id, {status:'approved'});
      await apiPost('/events', { name: req.eventName, date: req.eventDate, desc: req.eventDesc, plan: req.plan, traffic: req.plan==='Pro'?'50K+':(req.plan==='Medium'?'20K':'5K'), user: req.firstName+' '+req.lastName });
      renderAdminPanel(); renderEvents(); showToast('Tasdiqlandi'); AOS.refresh();
    };
    window.deleteRequest = async (id) => { await apiDelete('/requests/'+id); renderAdminPanel(); };

    // Tab
    document.querySelectorAll('.admin-tab').forEach(tab => {
      tab.addEventListener('click', () => {
        document.querySelectorAll('.admin-tab').forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        const t = tab.dataset.tab;
        document.getElementById('adminUsersPanel').style.display = t==='users'?'block':'none';
        document.getElementById('adminRequestsPanel').style.display = t==='requests'?'block':'none';
        document.getElementById('adminAddEventPanel').style.display = t==='addEvent'?'block':'none';
      });
    });
    document.getElementById('adminAddEventForm').onsubmit = async (e) => {
      e.preventDefault();
      const data = {
        name: document.getElementById('adminEventName').value, date: document.getElementById('adminEventDate').value,
        desc: document.getElementById('adminEventDesc').value, plan: document.getElementById('adminEventPlan').value,
        traffic: document.getElementById('adminEventPlan').value==='Pro'?'50K+':(document.getElementById('adminEventPlan').value==='Medium'?'20K':'5K'), user: 'Admin'
      };
      await apiPost('/events', data);
      showToast('Tadbir qo‘shildi'); e.target.reset(); renderEvents();
    };
  }

  function openAdminModal() {
    const pwd = prompt('Admin parolini kiriting:');
    if (pwd === ADMIN_PASSWORD) {
      document.getElementById('adminModal').style.visibility = 'visible';
      document.getElementById('adminModal').style.opacity = '1';
      renderAdminPanel();
    } else if (pwd !== null) showToast('❌ Parol noto‘g‘ri!', false);
  }
  function closeAdminModal() {
    document.getElementById('adminModal').style.visibility = 'hidden';
    document.getElementById('adminModal').style.opacity = '0';
  }

  // Taklif formasi
  document.getElementById('eventRequestForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const data = {
      firstName: document.getElementById('firstName').value.trim(),
      lastName: document.getElementById('lastName').value.trim(),
      phone: document.getElementById('phone').value.trim(),
      eventName: document.getElementById('eventName').value.trim(),
      eventDate: document.getElementById('eventDate').value,
      plan: document.getElementById('eventPlan').value,
      eventDesc: document.getElementById('eventDesc').value.trim(),
      status: document.getElementById('eventPlan').value === 'Free' ? 'approved' : 'pending'
    };
    if (!data.firstName || !data.lastName || !data.phone || !data.eventName || !data.eventDate) {
      showToast('Barcha maydonlarni to‘ldiring', false); return;
    }
    await apiPost('/requests', data);
    if (data.plan === 'Free') {
      await apiPost('/events', { name: data.eventName, date: data.eventDate, desc: data.eventDesc, plan: 'Free', traffic: '5K', user: `${data.firstName} ${data.lastName}` });
      renderEvents(); showToast('✅ Free tarif avtomatik ochildi!');
    } else {
      showToast('📬 Taklif adminga yuborildi.');
    }
    e.target.reset();
    AOS.refresh();
  });

  function scrollToAddEvent() { document.getElementById('add-event').scrollIntoView({ behavior: 'smooth' }); }

  AOS.init({ duration: 800, once: false, mirror: false });
  document.getElementById('adminBtn').addEventListener('click', openAdminModal);
  document.getElementById('adminModal').addEventListener('click', (e) => { if (e.target.classList.contains('modal-overlay')) closeAdminModal(); });
  document.querySelectorAll('a[href^="#"]').forEach(link => {
    link.addEventListener('click', function(e) {
      const href = this.getAttribute('href'); if (href === "#" || href === "") return;
      const target = document.querySelector(href); if (target) { e.preventDefault(); target.scrollIntoView({ behavior: 'smooth' }); }
    });
  });

  renderEvents();
</script>
</body>
</html>
'''

if __name__ == '__main__':
    init_demo()
    print("🚀 TadbirMarkaz serveri ishga tushdi: http://127.0.0.1:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)