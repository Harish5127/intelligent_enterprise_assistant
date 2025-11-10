try:
    from better_profanity import profanity as bp
    bp.load_censor_words()
    USE_BP = True
except Exception:
    USE_BP = False
    _BAD = set(['badword','foo','bar'])  # sample list (extendable)

def contains_profanity(text):
    if USE_BP:
        return bp.contains_profanity(text)
    t = text.lower()
    for w in _BAD:
        if w in t:
            return True
    return False

def clean_text(text):
    if USE_BP:
        return bp.censor(text)
    # basic replacement
    t = text
    for w in _BAD:
        t = t.replace(w, '[filtered]')
    return t
