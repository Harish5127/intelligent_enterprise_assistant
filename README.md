# Intelligent Enterprise Assistant (SIH1706) - Full Version (Demo-ready)

## NAME : HARISH R
## REG NO: 212224230085
## Overview
This project is a full-version demo for the Hackathon problem **SIH1706**:
"Intelligent Enterprise Assistant: Enhancing Organizational Efficiency through AI-driven Chatbot Integration".

It contains:
- Email-based 2FA (OTP) login (SMTP required)
- Chat UI (Flask + frontend JS)
- NLP chatbot engine (uses Hugging Face transformers **if available**; otherwise a lightweight keyword-based fallback)
- Document upload (PDF) → text extraction → extractive summarization + keyword extraction
- Profanity filter (uses `better_profanity` if installed; otherwise a small built-in list)
- Simple SQLite-based storage for users and OTPs
- Concurrency-friendly Flask endpoints (suitable for demos / testing). For production use a WSGI server (gunicorn) + proper reverse proxy.

## Quick start (Windows / VS Code)
1. Open this folder in VS Code.
2. Create & activate a venv:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   *If you plan to use transformers models, you'll also need `torch` and internet to download models on first run.*
4. Configure email SMTP settings (for 2FA):
   - Create a file named `.env` in the project root (see `.env.example`)
     or export environment variables: `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS`, `FROM_EMAIL`.
5. Run the app:
   ```bash
   python app.py
   ```
6. Open `http://127.0.0.1:5000` in your browser.

## Notes & Limitations
- For a production-ready system, deploy with a WSGI server, use HTTPS, rate-limiting, robust auth,
  and a real LLM or retrieval-augmented generation (RAG) pipeline.
- This demo keeps models optional: if you have `transformers` + `sentence-transformers` + `torch` installed,
  the app will try to use them for better semantic matching. If not present, it uses a simple keyword matching engine.

## Structure
See `project_structure.txt` for a full layout.
## output 
<img width="1803" height="1141" alt="image" src="https://github.com/user-attachments/assets/09a32333-cfb6-4ce6-8d38-19a078e2a839" />

<img width="1919" height="1090" alt="image" src="https://github.com/user-attachments/assets/b18a3028-8f17-46e9-93d7-02dcb015d96d" />


