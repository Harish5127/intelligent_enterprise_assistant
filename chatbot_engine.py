import os, json, re
from pathlib import Path
from profanity_filter import clean_text
DATA_DIR = Path('data')

# Load sample KB JSONs
def load_kb():
    kb = {}
    for fn in ('hr_faq.json','it_support.json'):
        p = DATA_DIR / fn
        if p.exists():
            try:
                kb[fn.replace('.json','')] = json.loads(p.read_text(encoding='utf-8'))
            except Exception:
                kb[fn.replace('.json','')] = []
        else:
            kb[fn.replace('.json','')] = []
    return kb

KB = load_kb()

# Try to use sentence transformers if available for semantic matching
USE_ST = False
try:
    from sentence_transformers import SentenceTransformer, util
    import numpy as np
    model = SentenceTransformer('all-MiniLM-L6-v2')  # will download on first run
    USE_ST = True
except Exception as e:
    # fallback to simple keyword matching
    USE_ST = False

def simple_match(query, items, top_k=1):
    # items: list of dicts with 'question' and 'answer'
    q = query.lower()
    scored = []
    for it in items:
        score = 0
        qtext = it.get('question','').lower()
        # simple word overlap score
        for w in re.findall(r"\w+", q):
            if w in qtext:
                score += 1
        scored.append((score, it.get('answer','')))
    scored.sort(reverse=True, key=lambda x: x[0])
    return [s[1] for s in scored[:top_k] if s[0] > 0]

def semantic_match(query, items, top_k=1):
    if not USE_ST:
        return simple_match(query, items, top_k)
    sentences = [it.get('question','') for it in items]
    if not sentences:
        return []
    q_emb = model.encode(query, convert_to_tensor=True)
    emb = model.encode(sentences, convert_to_tensor=True)
    scores = util.cos_sim(q_emb, emb)[0].cpu().numpy()
    idx = scores.argsort()[::-1][:top_k]
    return [items[int(i)]['answer'] for i in idx if float(scores[int(i)])>0.3]

def get_reply(message, user=None):
    # Clean profanity in outgoing reply before send
    # 1) Search KBs
    for section, items in KB.items():
        res = semantic_match(message, items, top_k=1)
        if res:
            reply = res[0]
            return clean_text(reply)
    # 2) Simple FAQs fallback
    if re.search(r'\btime\b|\bdate\b', message, re.I):
        import datetime
        return f"Current server time: {datetime.datetime.now().isoformat()}"
    # 3) If asks for document help
    if re.search(r'\bsummary\b|\bsummariz(e|ation)\b|\bupload\b', message, re.I):
        return "You can upload a document in the Documents tab — I will extract and summarize it."
    # 4) Generic fallback
    return clean_text("I'm sorry — I don't know that yet. Try asking about HR policy, IT support, or upload a document.")
