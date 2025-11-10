import os, re, math
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter
try:
    import fitz  # PyMuPDF
except Exception:
    fitz = None

def extract_text_from_pdf(path):
    if fitz is None:
        # fallback: just read as plain text
        try:
            return open(path, 'r', encoding='utf-8').read()
        except Exception:
            return ''
    doc = fitz.open(path)
    parts = []
    for page in doc:
        parts.append(page.get_text())
    return '\n'.join(parts)

def split_sentences(text):
    # naive sentence splitter
    s = re.split(r'(?<=[.!?])\s+', text.strip())
    return [x.strip() for x in s if x.strip()]

def summarize_text(text, num_sentences=3):
    if not text: return ''
    sents = split_sentences(text)
    if len(sents) <= num_sentences:
        return '\n'.join(sents)
    # score by word frequency
    words = re.findall(r"\w+", text.lower())
    freq = Counter(words)
    scores = []
    for i, sent in enumerate(sents):
        score = 0
        for w in re.findall(r"\w+", sent.lower()):
            score += freq.get(w,0)
        scores.append((score, i, sent))
    scores.sort(reverse=True)
    selected = sorted(scores[:num_sentences], key=lambda x: x[1])
    return '\n'.join([s[2] for s in selected])

def extract_keywords(text, top_k=10):
    if not text: return []
    vect = TfidfVectorizer(stop_words='english', max_features=2000)
    tf = vect.fit_transform([text])
    scores = list(zip(vect.get_feature_names_out(), tf.toarray()[0]))
    scores.sort(key=lambda x: x[1], reverse=True)
    return [w for w, sc in scores[:top_k]]
