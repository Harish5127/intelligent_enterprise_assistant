import os, random, sqlite3, time
from itsdangerous import TimestampSigner
from dotenv import load_dotenv
import smtplib
from email.message import EmailMessage

load_dotenv()
DB = 'users.db'
SIGNER = TimestampSigner(os.environ.get('FLASK_SECRET', 'dev-secret'))

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS otps (email TEXT PRIMARY KEY, otp TEXT, expires_at REAL)''')
    c.execute('''CREATE TABLE IF NOT EXISTS users (email TEXT PRIMARY KEY, created_at REAL)''')
    conn.commit()
    conn.close()

def send_email(to_email, subject, body):
    host = os.environ.get('SMTP_HOST')
    port = int(os.environ.get('SMTP_PORT', '587'))
    user = os.environ.get('SMTP_USER')
    pwd = os.environ.get('SMTP_PASS')
    from_addr = os.environ.get('FROM_EMAIL', user)
    if not host or not user or not pwd:
        print('SMTP not configured -- skipping actual send. Check .env.')
        print('Email would be:', to_email, subject, body)
        return False
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = from_addr
    msg['To'] = to_email
    msg.set_content(body)
    try:
        with smtplib.SMTP(host, port) as s:
            s.starttls()
            s.login(user, pwd)
            s.send_message(msg)
        return True
    except Exception as e:
        print('Error sending email:', e)
        return False

def send_otp(email):
    otp = '%06d' % random.randint(0,999999)
    expires = time.time() + 5*60  # 5 minutes
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('REPLACE INTO otps (email, otp, expires_at) VALUES (?, ?, ?)', (email, otp, expires))
    conn.commit()
    conn.close()
    body = f'Your Intelligent Assistant OTP is: {otp} (valid 5 minutes)'
    ok = send_email(email, 'Your OTP for Intelligent Assistant', body)
    # even if email fails (e.g. no SMTP), still return True so demo can continue (but OTP printed to console)
    print(f'[DEBUG] OTP for {email}:', otp)
    return True

def verify_otp(email, otp):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('SELECT otp, expires_at FROM otps WHERE email=?', (email,))
    row = c.fetchone()
    conn.close()
    if not row:
        return False
    saved_otp, expires = row
    import time
    if time.time() > expires:
        return False
    return saved_otp == otp

def login_user(email):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('REPLACE INTO users (email, created_at) VALUES (?, ?)', (email, time.time()))
    conn.commit()
    conn.close()
