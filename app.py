import os
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from dotenv import load_dotenv
from auth import send_otp, verify_otp, init_db, login_user
from chatbot_engine import get_reply
from document_processor import extract_text_from_pdf, summarize_text, extract_keywords
from profanity_filter import clean_text, contains_profanity

load_dotenv()
app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = os.environ.get('FLASK_SECRET', 'dev-secret')

init_db()  # ensure DB and tables

@app.route('/')
def home():
    if 'user_email' in session:
        return render_template('index.html', user=session['user_email'])
    return redirect(url_for('login'))

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@app.route('/send_otp', methods=['POST'])
def route_send_otp():
    data = request.get_json() or {}
    email = data.get('email','').strip()
    if not email:
        return jsonify({'ok': False, 'error': 'Email required'}), 400
    success = send_otp(email)
    return jsonify({'ok': success})

@app.route('/verify_otp', methods=['POST'])
def route_verify_otp():
    data = request.get_json() or {}
    email = data.get('email','').strip()
    otp = data.get('otp','').strip()
    if verify_otp(email, otp):
        login_user(email)
        session['user_email'] = email
        return jsonify({'ok': True})
    return jsonify({'ok': False, 'error': 'Invalid OTP'}), 401

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/chat', methods=['POST'])
def chat():
    if 'user_email' not in session:
        return jsonify({'ok': False, 'error': 'Not authenticated'}), 401
    data = request.get_json() or {}
    message = data.get('message','').strip()
    if contains_profanity(message):
        return jsonify({'ok': True, 'reply': clean_text('[Message blocked due to profanity]')})
    reply = get_reply(message, user=session['user_email'])
    return jsonify({'ok': True, 'reply': reply})

@app.route('/upload', methods=['POST'])
def upload():
    if 'user_email' not in session:
        return jsonify({'ok': False, 'error': 'Not authenticated'}), 401
    f = request.files.get('file')
    if not f:
        return jsonify({'ok': False, 'error': 'No file uploaded'}), 400
    filename = f.filename
    saved = os.path.join('data','sample_documents', filename)
    os.makedirs(os.path.dirname(saved), exist_ok=True)
    f.save(saved)
    text = extract_text_from_pdf(saved)
    summary = summarize_text(text, num_sentences=5)
    keywords = extract_keywords(text, top_k=10)
    return jsonify({'ok': True, 'summary': summary, 'keywords': keywords})

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='127.0.0.1')
