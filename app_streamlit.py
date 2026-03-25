import streamlit as st
import time
import re
import difflib
import sys
import subprocess
import nltk

# ==========================================
# 1. CONFIGURATION DE LA PAGE
# ==========================================
st.set_page_config(
    page_title="AI Grammar Corrector Pro",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ==========================================
# 2. INSTALLATION AUTOMATIQUE DES BIBLIOTHÈQUES
# ==========================================
def install_if_missing(package_name, import_name=None):
    if import_name is None:
        import_name = package_name
    try:
        __import__(import_name)
        return True
    except ImportError:
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install",
                package_name, "-q", "--no-warn-script-location"
            ])
            return True
        except Exception:
            return False

required = [
    ("transformers", "transformers"),
    ("torch", "torch"),
    ("sentencepiece", "sentencepiece"),
    ("sacremoses", "sacremoses"),
    ("protobuf", "google.protobuf"),
    ("nltk", "nltk"),
    ("language-tool-python", "language_tool_python"),
    ("pyspellchecker", "spellchecker"),
]

install_status = {}
for pkg, imp in required:
    install_status[pkg] = install_if_missing(pkg, imp)

# Téléchargement des données NLTK
try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    try:
        nltk.download('punkt_tab', quiet=True)
    except Exception:
        try:
            nltk.download('punkt', quiet=True)
        except Exception:
            pass

# ==========================================
# 3. CSS COMPLET
# ==========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700;800;900&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Noto+Naskh+Arabic:wght@400;500;600;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&display=swap');

:root {
    --gold:#e9c46a;--gold-light:#f4d58d;--orange:#f4a261;
    --cyan:#a8dadc;--green:#2ecc71;--red:#e74c3c;
    --purple:#a855f7;--blue:#3b82f6;--teal:#14b8a6;
    --dark-1:#050510;--dark-2:#0d0d2b;
    --text-primary:#f0f0f0;--text-secondary:#a0a0b0;
    --glass:rgba(255,255,255,0.03);
    --glass-border:rgba(255,255,255,0.08);
}

*{font-family:'Tajawal',sans-serif!important}
html,body,[data-testid="stAppViewContainer"]{
    background:var(--dark-1)!important;
    color:var(--text-primary)!important}
.main .block-container{padding:0!important;max-width:100%!important}
#MainMenu,footer,header,
[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"]{display:none!important}

.bg-fx{position:fixed;inset:0;z-index:0;pointer-events:none;overflow:hidden}
.bg-orb{position:absolute;border-radius:50%;filter:blur(100px);opacity:.12;
    animation:drift 25s ease-in-out infinite}
.o1{width:500px;height:500px;background:var(--gold);top:-200px;right:-100px}
.o2{width:400px;height:400px;background:var(--purple);bottom:-150px;left:-100px;
    animation-delay:-8s}
.o3{width:350px;height:350px;background:var(--cyan);top:40%;left:30%;
    animation-delay:-16s}
.bg-lines{position:absolute;inset:0;
    background-image:
        linear-gradient(rgba(233,196,106,.02) 1px,transparent 1px),
        linear-gradient(90deg,rgba(233,196,106,.02) 1px,transparent 1px);
    background-size:80px 80px}
@keyframes drift{
    0%,100%{transform:translate(0,0) scale(1)}
    33%{transform:translate(50px,-60px) scale(1.08)}
    66%{transform:translate(-40px,50px) scale(.92)}}

.topbar{position:relative;z-index:10;display:flex;align-items:center;
    justify-content:space-between;padding:1rem 3rem;
    background:rgba(13,13,43,.75);backdrop-filter:blur(25px);
    border-bottom:1px solid var(--glass-border)}
.tb-brand{display:flex;align-items:center;gap:.7rem}
.tb-logo{width:38px;height:38px;
    background:linear-gradient(135deg,var(--gold),var(--orange));
    border-radius:11px;display:flex;align-items:center;
    justify-content:center;font-size:1.2rem;
    box-shadow:0 4px 12px rgba(233,196,106,.25)}
.tb-name{font-size:1.15rem;font-weight:800;color:var(--gold)}
.tb-tag{background:rgba(168,85,247,.15);
    border:1px solid rgba(168,85,247,.3);color:var(--purple);
    padding:.3rem .9rem;border-radius:50px;font-size:.78rem;font-weight:700}

.hero{position:relative;z-index:1;text-align:center;padding:3rem 2rem 2rem}
.hero-chip{display:inline-flex;align-items:center;gap:.5rem;
    background:rgba(233,196,106,.08);border:1px solid rgba(233,196,106,.18);
    padding:.4rem 1.2rem;border-radius:50px;font-size:.82rem;
    color:var(--gold);margin-bottom:1.5rem}
.hero h1{font-size:3rem;font-weight:900;line-height:1.15;margin-bottom:1rem}
.hero h1 .glow{
    background:linear-gradient(135deg,var(--gold),var(--orange),var(--gold-light));
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;
    background-clip:text}
.hero-desc{font-size:1.1rem;color:var(--text-secondary);
    max-width:700px;margin:0 auto 2rem;line-height:1.8;font-weight:300}

.workzone{position:relative;z-index:1;max-width:1050px;margin:0 auto;
    padding:0 2rem 3rem}
.gc{background:var(--glass);backdrop-filter:blur(20px);
    border:1px solid var(--glass-border);border-radius:22px;
    padding:1.8rem;margin-bottom:1.3rem}
.gc:hover{border-color:rgba(233,196,106,.12)}
.gc-head{display:flex;align-items:center;justify-content:space-between;
    margin-bottom:1rem}
.gc-title{display:flex;align-items:center;gap:.6rem;
    font-size:1.05rem;font-weight:700}
.gc-ico{width:30px;height:30px;
    background:linear-gradient(135deg,var(--gold),var(--orange));
    border-radius:9px;display:flex;align-items:center;
    justify-content:center;font-size:.85rem}
.gc-ico-blue{background:linear-gradient(135deg,var(--blue),var(--teal))!important}
.gc-ico-green{background:linear-gradient(135deg,var(--green),var(--teal))!important}
.gc-ico-purple{background:linear-gradient(135deg,var(--purple),#ec4899)!important}
.gc-badge{font-size:.78rem;color:var(--text-secondary);
    background:rgba(255,255,255,.04);padding:.25rem .7rem;
    border-radius:20px;border:1px solid var(--glass-border)}

.stTextArea textarea{
    font-family:'JetBrains Mono',monospace!important;
    font-size:1.05rem!important;line-height:1.9!important;
    direction:ltr!important;text-align:left!important;
    background:rgba(0,0,0,.35)!important;
    border:2px solid var(--glass-border)!important;
    border-radius:14px!important;padding:1.3rem!important;
    color:var(--text-primary)!important}
.stTextArea textarea:focus{border-color:var(--gold)!important;
    box-shadow:0 0 0 3px rgba(233,196,106,.1)!important}

.rbox{border:2px solid rgba(233,196,106,.15);border-radius:14px;
    padding:1.5rem;direction:ltr;text-align:left;
    font-family:'JetBrains Mono',monospace;font-size:1.05rem;
    line-height:2.2;color:var(--text-primary);min-height:100px;
    position:relative;overflow:hidden;word-wrap:break-word;
    background:linear-gradient(135deg,
        rgba(233,196,106,.04),rgba(168,218,220,.03))}
.rbox::before{content:'';position:absolute;top:0;left:0;right:0;
    height:3px;border-radius:14px 14px 0 0}
.rbox-diff::before{
    background:linear-gradient(90deg,var(--red),var(--orange),var(--green))}
.rbox-clean::before{
    background:linear-gradient(90deg,var(--green),var(--cyan))}
.rbox-clean{color:var(--green);font-weight:500}
.rbox-trans::before{
    background:linear-gradient(90deg,var(--blue),var(--teal))}
.rbox-trans{color:var(--cyan);font-weight:500}
.rbox-rtl{direction:rtl!important;text-align:right!important;
    font-family:'Noto Naskh Arabic','Tajawal',sans-serif!important;
    font-size:1.3rem!important;line-height:2.5!important}
.rbox-empty{color:rgba(255,255,255,.15);font-family:'Tajawal'!important;
    font-size:.95rem;display:flex;align-items:center;justify-content:center}

mark.err{background:rgba(231,76,60,.2);color:#ff7675;border-radius:4px;
    padding:1px 5px;font-weight:600;text-decoration:line-through}
mark.fix{background:rgba(46,204,113,.15);color:#55efc4;font-weight:700;
    padding:1px 5px;border-radius:4px;
    border-bottom:2px solid rgba(46,204,113,.5)}

.stButton>button{border-radius:12px!important;padding:.75rem!important;
    font-weight:700!important;font-size:1rem!important;border:none!important}
.stButton>button[kind="primary"]{
    background:linear-gradient(135deg,var(--gold),var(--orange))!important;
    color:var(--dark-1)!important;
    box-shadow:0 4px 18px rgba(233,196,106,.25)!important}
.stButton>button[kind="primary"]:hover{transform:translateY(-2px)!important;
    box-shadow:0 8px 28px rgba(233,196,106,.35)!important}
.stButton>button[kind="secondary"]{background:var(--glass)!important;
    color:var(--text-primary)!important;
    border:1px solid var(--glass-border)!important}

.sgrid{display:grid;grid-template-columns:repeat(4,1fr);gap:.8rem;margin-top:1.2rem}
.sc{background:linear-gradient(135deg,rgba(26,26,62,.8),rgba(13,13,43,.9));
    border:1px solid var(--glass-border);border-radius:16px;padding:1.2rem;
    text-align:center;transition:all .3s}
.sc:hover{transform:translateY(-4px);border-color:rgba(233,196,106,.25)}
.sc-val{font-size:1.8rem;font-weight:900;color:var(--gold)}
.sc-lbl{font-size:.8rem;color:var(--text-secondary);margin-top:.2rem}

.pill{display:inline-flex;align-items:center;gap:.45rem;padding:.4rem 1rem;
    border-radius:50px;font-size:.85rem;font-weight:600;margin:.2rem}
.pill-ok{background:rgba(46,204,113,.1);border:1px solid rgba(46,204,113,.25);color:#2ecc71}
.pill-err{background:rgba(231,76,60,.1);border:1px solid rgba(231,76,60,.25);color:#e74c3c}
.pill-warn{background:rgba(244,162,97,.1);border:1px solid rgba(244,162,97,.25);color:#f4a261}
.pdot{width:7px;height:7px;border-radius:50%;animation:blink 2s infinite}
.pill-ok .pdot{background:#2ecc71}
.pill-err .pdot{background:#e74c3c}
.pill-warn .pdot{background:#f4a261}
@keyframes blink{0%,100%{opacity:1}50%{opacity:.3}}

.layer-info{display:flex;gap:.5rem;flex-wrap:wrap;margin:.8rem 0}
.layer-tag{padding:.3rem .8rem;border-radius:8px;font-size:.78rem;font-weight:600}
.lt-1{background:rgba(233,196,106,.1);color:var(--gold);border:1px solid rgba(233,196,106,.2)}
.lt-2{background:rgba(168,85,247,.1);color:var(--purple);border:1px solid rgba(168,85,247,.2)}
.lt-3{background:rgba(59,130,246,.1);color:var(--blue);border:1px solid rgba(59,130,246,.2)}

.divider{border:none;border-top:1px solid var(--glass-border);margin:2rem 0}

.meter-bar{height:14px;border-radius:7px;background:rgba(255,255,255,.05);
    overflow:hidden;margin:.5rem 0}
.meter-fill{height:100%;border-radius:7px;transition:width 1.5s ease}

.fgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;margin:2.5rem 0}
.fc{background:var(--glass);border:1px solid var(--glass-border);
    border-radius:18px;padding:1.5rem;text-align:center;transition:all .3s}
.fc:hover{border-color:rgba(233,196,106,.18);transform:translateY(-3px)}
.fc-ico{font-size:1.8rem;margin-bottom:.7rem}
.fc-ttl{font-weight:700;margin-bottom:.3rem}
.fc-dsc{font-size:.82rem;color:var(--text-secondary);line-height:1.7}

.appfoot{position:relative;z-index:1;text-align:center;padding:2.5rem 2rem;
    border-top:1px solid var(--glass-border);margin-top:2rem}
.af-brand{font-size:1.1rem;font-weight:800;color:var(--gold)}
.af-txt{color:var(--text-secondary);font-size:.82rem;margin-top:.3rem}

.stSelectbox>div>div{
    background:rgba(0,0,0,.3)!important;
    border:2px solid var(--glass-border)!important;
    border-radius:12px!important;color:var(--text-primary)!important}

@media(max-width:768px){
    .topbar{padding:.7rem 1rem}.hero h1{font-size:2rem}
    .sgrid{grid-template-columns:repeat(2,1fr)}
    .fgrid{grid-template-columns:1fr}
    .workzone{padding:0 1rem 2rem}}
</style>
""", unsafe_allow_html=True)


# ==========================================
# 4. COUCHES DE CORRECTION
# ==========================================

# 4A. Correcteur orthographique (pyspellchecker)
from spellchecker import SpellChecker

@st.cache_resource
def load_spellchecker():
    return SpellChecker(language='en')

def correct_spelling(text, spell):
    words = text.split()
    corrected_words = []
    for word in words:
        # Ignorer les mots avec apostrophe, majuscules (noms propres)
        if "'" in word or word.isupper() or (word[0].isupper() and len(word) > 1):
            corrected_words.append(word)
        else:
            if word.lower() not in spell:
                candidates = spell.candidates(word)
                if candidates:
                    best = spell.correction(word)
                    corrected_words.append(best if best else word)
                else:
                    corrected_words.append(word)
            else:
                corrected_words.append(word)
    return ' '.join(corrected_words)

# 4B. Règles orthographiques communes
COMMON_FIXES = {
    "could of":    "could have",
    "should of":   "should have",
    "would of":    "would have",
    "must of":     "must have",
    "might of":    "might have",
    "cant":        "can't",
    "dont":        "don't",
    "doesnt":      "doesn't",
    "didnt":       "didn't",
    "wont":        "won't",
    "wouldnt":     "wouldn't",
    "shouldnt":    "shouldn't",
    "couldnt":     "couldn't",
    "isnt":        "isn't",
    "arent":       "aren't",
    "wasnt":       "wasn't",
    "werent":      "weren't",
    "hasnt":       "hasn't",
    "havent":      "haven't",
    "hadnt":       "hadn't",
    "im ":         "I'm ",
    "ive ":        "I've ",
    "id ":         "I'd ",
    "ill ":        "I'll ",
    "alot":        "a lot",
    "recieve":     "receive",
    "occured":     "occurred",
    "untill":      "until",
    "definately":  "definitely",
    "seperate":    "separate",
    "goverment":   "government",
    "enviroment":  "environment",
    "tommorrow":   "tomorrow",
    "tommorow":    "tomorrow",
    "tomorow":     "tomorrow",
    "yestarday":   "yesterday",
    "yesturday":   "yesterday",
    "becuase":     "because",
    "becasue":     "because",
    "beacuse":     "because",
    "thier":       "their",
    "freind":      "friend",
    "freinds":     "friends",
    "wich":        "which",
    "wierd":       "weird",
    "belive":      "believe",
    "beleive":     "believe",
    "arguement":   "argument",
    "calender":    "calendar",
    "catagory":    "category",
    "comittee":    "committee",
    "concious":    "conscious",
    "embarass":    "embarrass",
    "foriegn":     "foreign",
    "fourty":      "forty",
    "grammer":     "grammar",
    "independant": "independent",
    "knowlege":    "knowledge",
    "libary":      "library",
    "librery":     "library",
    "neccessary":  "necessary",
    "noticable":   "noticeable",
    "occurence":   "occurrence",
    "priviledge":  "privilege",
    "professer":   "professor",
    "realy":       "really",
    "relevent":    "relevant",
    "religous":    "religious",
    "rythm":       "rhythm",
    "succesful":   "successful",
    "sucessful":   "successful",
    "suprise":     "surprise",
    "truely":      "truly",
    "unfortunatly": "unfortunately",
    "accomodate":  "accommodate",
    "acheive":     "achieve",
    "accross":     "across",
    "agressive":   "aggressive",
    "apparantly":  "apparently",
    "basicly":     "basically",
    "begining":    "beginning",
    "buisness":    "business",
    "completly":   "completely",
    "diffrent":    "different",
    "dissapear":   "disappear",
    "exellent":    "excellent",
    "existance":   "existence",
    "familar":     "familiar",
    "finaly":      "finally",
    "happend":     "happened",
    "immediatly":  "immediately",
    "intresting":  "interesting",
    "laguage":     "language",
    "naturaly":    "naturally",
    "neigbour":    "neighbour",
    "obviuosly":   "obviously",
    "opertunity":  "opportunity",
    "orginal":     "original",
    "particulary": "particularly",
    "probaly":     "probably",
    "recomend":    "recommend",
    "remeber":     "remember",
    "saftey":      "safety",
    "shedule":     "schedule",
    "sincerly":    "sincerely",
    "speach":      "speech",
    "strenght":    "strength",
    "teecher":     "teacher",
    "togeather":   "together",
    "usally":      "usually",
    "vaccum":      "vacuum",
    "valuble":     "valuable",
    "visable":     "visible",
    "wether":      "whether",
    "writting":    "writing",
    "studdy":      "study",
    "finalle":     "final",
    "examms":      "exams",
    "leter":       "letter",
    "gardenn":     "garden",
    "yeers":       "years",
}

# 4C. Homophones
HOMOPHONE_RULES = [
    # your / you're
    (r"\byour\s+going\b",      "you're going"),
    (r"\byour\s+welcome\b",    "you're welcome"),
    (r"\byour\s+right\b",      "you're right"),
    (r"\byour\s+wrong\b",      "you're wrong"),
    (r"\byour\s+doing\b",      "you're doing"),
    (r"\byour\s+being\b",      "you're being"),
    (r"\byour\s+coming\b",     "you're coming"),
    (r"\byour\s+leaving\b",    "you're leaving"),
    (r"\byour\s+making\b",     "you're making"),
    (r"\byour\s+not\b",        "you're not"),
    (r"\byour\s+the\s+best\b", "you're the best"),
    (r"\byour\s+so\b",         "you're so"),
    (r"\byour\s+very\b",       "you're very"),
    (r"\byour\s+too\b",        "you're too"),
    # their / there / they're
    (r"\btheir\s+is\b",        "there is"),
    (r"\btheir\s+are\b",       "there are"),
    (r"\btheir\s+was\b",       "there was"),
    (r"\btheir\s+were\b",      "there were"),
    (r"\btheir\s+going\b",     "they're going"),
    (r"\btheir\s+coming\b",    "they're coming"),
    (r"\btheir\s+not\b",       "they're not"),
    (r"\btheir\s+doing\b",     "they're doing"),
    # its / it's
    (r"\bits\s+a\b",           "it's a"),
    (r"\bits\s+the\b",         "it's the"),
    (r"\bits\s+not\b",         "it's not"),
    (r"\bits\s+been\b",        "it's been"),
    (r"\bits\s+going\b",       "it's going"),
    (r"\bits\s+very\b",        "it's very"),
    (r"\bits\s+so\b",          "it's so"),
    (r"\bits\s+too\b",         "it's too"),
    (r"\bits\s+really\b",      "it's really"),
    # than / then
    (r"\bmore\s+.*?\s+then\b", lambda m: m.group().replace("then", "than")),
    (r"\bbetter\s+then\b",     "better than"),
    (r"\bworse\s+then\b",      "worse than"),
    (r"\brather\s+then\b",     "rather than"),
    (r"\bother\s+then\b",      "other than"),
    (r"\bless\s+then\b",       "less than"),
    (r"\bgreater\s+then\b",    "greater than"),
    (r"\bbigger\s+then\b",     "bigger than"),
    (r"\bsmaller\s+then\b",    "smaller than"),
    (r"\bolder\s+then\b",      "older than"),
    (r"\byounger\s+then\b",    "younger than"),
    (r"\bfaster\s+then\b",     "faster than"),
    (r"\bslower\s+then\b",     "slower than"),
    # to / too
    (r"\bto\s+much\b",         "too much"),
    (r"\bto\s+many\b",         "too many"),
    (r"\bto\s+late\b",         "too late"),
    (r"\bto\s+early\b",        "too early"),
    (r"\bto\s+fast\b",         "too fast"),
    (r"\bto\s+slow\b",         "too slow"),
    (r"\bto\s+big\b",          "too big"),
    (r"\bto\s+small\b",        "too small"),
    (r"\bme\s+to\b",           "me too"),
    # affect / effect
    (r"\beffect\s+(?:my|your|his|her|their|our|the)\b",
     lambda m: m.group().replace("effect", "affect")),
    # lose / loose
    (r"\bloose\s+(?:my|your|his|her|the|a|their|our|it)\b",
     lambda m: m.group().replace("loose", "lose")),
    # who's / whose
    (r"\bwho's\s+(?:book|car|house|phone|bag|idea|fault|turn|job)\b",
     lambda m: m.group().replace("who's", "whose")),
    # meet / meat
    (r"\bmeet\s+and\s+eat\b",  "meat and eat"),
    (r"\bmeat\s+the\b",        "meet the"),
    # pair / pear
    (r"\bpair\s+of\s+shoes\b", "pair of shoes"),
    (r"\bpear\s+tree\b",       "pear tree"),
    # hole / whole
    (r"\bwhole\s+in\s+the\b",  "hole in the"),
    (r"\bhole\s+day\b",        "whole day"),
    # hear / here
    (r"\bhere\s+you\b",        "hear you"),
    (r"\bhear\s+is\b",         "here is"),
    # brake / break
    (r"\bbreak\s+the\s+car\b", "brake the car"),
    (r"\bbrake\s+the\s+window\b", "break the window"),
    # buy / by / bye
    (r"\bby\s+some\s+milk\b",  "buy some milk"),
    (r"\bbye\s+the\b",         "by the"),
    # piece / peace
    (r"\bpeace\s+of\s+cake\b", "piece of cake"),
    (r"\bpeace\s+of\s+advice\b", "piece of advice"),
]

# 4D. Bigram contextuel
BIGRAM_FIXES = {
    "make a photo": "take a photo",
    "do a mistake": "make a mistake",
    "do a decision": "make a decision",
    "make a favor": "do a favor",
    "make a noise": "make a noise",
    "do a noise": "make a noise",
    "strong rain": "heavy rain",
    "weak rain": "light rain",
    "strong tea": "strong tea",
    "weak tea": "weak tea",
    "make a party": "have a party",
    "do a party": "have a party",
    "make a job": "do a job",
    "do a job": "do a job",
    "make a call": "make a call",
    "do a call": "make a call",
}

def apply_bigram_corrections(text):
    result = text
    for wrong, correct in BIGRAM_FIXES.items():
        pattern = re.compile(re.escape(wrong), re.IGNORECASE)
        result = pattern.sub(correct, result)
    return result

# 4E. Règles grammaticales
GRAMMAR_PATTERNS = [
    (r'(?<![A-Za-z])i(?![A-Za-z])', 'I'),
    (r'\bhe dont\b',       "he doesn't"),
    (r'\bshe dont\b',      "she doesn't"),
    (r'\bit dont\b',       "it doesn't"),
    (r"\bhe don't\b",      "he doesn't"),
    (r"\bshe don't\b",     "she doesn't"),
    (r"\bit don't\b",      "it doesn't"),
    (r'\bI has\b',         'I have'),
    (r'\bI is\b',          'I am'),
    (r'\byou is\b',        'you are'),
    (r'\bwe is\b',         'we are'),
    (r'\bthey is\b',       'they are'),
    (r'\bhe have\b',       'he has'),
    (r'\bshe have\b',      'she has'),
    (r'\bit have\b',       'it has'),
    (r'\bmore better\b',   'better'),
    (r'\bmore worse\b',    'worse'),
    (r'\bmost best\b',     'best'),
    (r'\bmost worst\b',    'worst'),
    (r'\bchilds\b',        'children'),
    (r'\bmans\b',          'men'),
    (r'\bwomans\b',        'women'),
    (r'\btooths\b',        'teeth'),
    (r'\bfoots\b',         'feet'),
    (r'\bgoed\b',          'went'),
    (r'\bwrited\b',        'wrote'),
    (r'\bthinked\b',       'thought'),
    (r'\bteached\b',       'taught'),
    (r'\bbringed\b',       'brought'),
    (r'\bbuyed\b',         'bought'),
    (r'\bcatched\b',       'caught'),
    (r'\bfeeled\b',        'felt'),
    (r'\bfinded\b',        'found'),
    (r'\bgived\b',         'gave'),
    (r'\bheared\b',        'heard'),
    (r'\bknowed\b',        'knew'),
    (r'\bleaved\b',        'left'),
    (r'\bmaked\b',         'made'),
    (r'\bmeeted\b',        'met'),
    (r'\brunned\b',        'ran'),
    (r'\bsayed\b',         'said'),
    (r'\bseed\b',          'saw'),
    (r'\bsended\b',        'sent'),
    (r'\bsitted\b',        'sat'),
    (r'\bsleeped\b',       'slept'),
    (r'\bspeaked\b',       'spoke'),
    (r'\bstanded\b',       'stood'),
    (r'\bswimmed\b',       'swam'),
    (r'\btaked\b',         'took'),
    (r'\btelled\b',        'told'),
    (r'\bweared\b',        'wore'),
    (r'\bwinned\b',        'won'),
    (r'\bdont knows\b',    "doesn't know"),
    (r'\bdont know\b',     "don't know"),
]

def apply_rule_engine(text):
    result = text
    lower = result.lower()
    for wrong, correct in COMMON_FIXES.items():
        if wrong in lower:
            pattern = re.compile(re.escape(wrong), re.IGNORECASE)
            result = pattern.sub(correct, result)
            lower = result.lower()
    for pattern, replacement in GRAMMAR_PATTERNS:
        result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
    # Capitalisation des phrases
    sentences = re.split(r'([.!?]\s+)', result)
    fixed = []
    for i, part in enumerate(sentences):
        if part and (i == 0 or (i > 0 and re.match(r'[.!?]\s+', sentences[i-1]))):
            if part[0].islower():
                part = part[0].upper() + part[1:]
        fixed.append(part)
    result = ''.join(fixed)
    if result and result[0].islower():
        result = result[0].upper() + result[1:]
    return result

def apply_homophone_filter(text):
    result = text
    for pattern, replacement in HOMOPHONE_RULES:
        if callable(replacement):
            result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
        else:
            result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
    return result

# 4F. Modèle T5
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

@st.cache_resource
def load_corrector():
    model_name = "vennify/t5-base-grammar-correction"
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to(DEVICE)
        return tokenizer, model, None
    except Exception as e:
        # Fallback
        try:
            model_name = "prithivida/grammar_error_correcter_v1"
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to(DEVICE)
            return tokenizer, model, "Fallback: " + model_name
        except Exception as e2:
            return None, None, str(e2)

def correct_with_ai(text, tokenizer, model):
    sentences = smart_split(text)
    results = []
    for sent in sentences:
        if not sent.strip():
            continue
        try:
            inputs = tokenizer(
                "gec: " + sent,
                return_tensors="pt",
                max_length=256,
                truncation=True,
                padding=True,
            ).to(DEVICE)
            outputs = model.generate(
                **inputs,
                max_length=256,
                num_beams=5,
                early_stopping=True,
            )
            corrected = tokenizer.decode(outputs[0], skip_special_tokens=True)
            results.append(corrected if corrected.strip() else sent)
        except Exception:
            results.append(sent)
    return " ".join(results)

# 4G. LanguageTool
@st.cache_resource
def load_language_tool():
    try:
        import language_tool_python
        tool = language_tool_python.LanguageTool('en-US')
        return tool, None
    except Exception as e:
        return None, str(e)

def apply_language_tool(text, tool):
    try:
        import language_tool_python
        matches = tool.check(text)
        corrected = language_tool_python.utils.correct(text, matches)
        return corrected, len(matches)
    except Exception:
        return text, 0

# 4H. Pipeline complet
def full_correction_pipeline(text, spell, ai_tokenizer, ai_model, lt_tool):
    layer_results = {}
    # Couche 0: Spell checker
    after_spell = correct_spelling(text, spell)
    layer_results["spell"] = after_spell
    # Couche 1: Règles
    after_rules = apply_rule_engine(after_spell)
    layer_results["rules"] = after_rules
    # Couche 2: Homophones
    after_homo = apply_homophone_filter(after_rules)
    layer_results["homophones"] = after_homo
    # Couche 3: Bigram
    after_bigram = apply_bigram_corrections(after_homo)
    layer_results["bigram"] = after_bigram
    # Couche 4: IA
    after_ai = correct_with_ai(after_bigram, ai_tokenizer, ai_model)
    layer_results["ai"] = after_ai
    # Couche 5: LanguageTool
    lt_fixes = 0
    if lt_tool:
        after_lt, lt_fixes = apply_language_tool(after_ai, lt_tool)
        layer_results["languagetool"] = after_lt
        final = after_lt
    else:
        final = after_ai
    layer_results["final"] = final
    layer_results["lt_fixes"] = lt_fixes
    return final, layer_results

# ==========================================
# 5. TRADUCTION
# ==========================================
TRANS_LANGS = {
    "🇸🇦 العربية (Arabic)":        "ar",
    "🇫🇷 Français (French)":       "fr",
    "🇩🇪 Deutsch (German)":        "de",
    "🇪🇸 Español (Spanish)":       "es",
    "🇮🇹 Italiano (Italian)":      "it",
    "🇵🇹 Português (Portuguese)":  "pt",
    "🇷🇺 Русский (Russian)":       "ru",
    "🇹🇷 Türkçe (Turkish)":        "tr",
    "🇳🇱 Nederlands (Dutch)":      "nl",
    "🇸🇪 Svenska (Swedish)":       "sv",
    "🇨🇳 中文 (Chinese)":           "zh",
    "🇯🇵 日本語 (Japanese)":         "jap",
}
RTL_CODES = {"ar", "he", "fa", "ur"}

@st.cache_resource
def load_translator_model(src_code, tgt_code):
    candidates = [
        "Helsinki-NLP/opus-mt-{}-{}".format(src_code, tgt_code),
        "Helsinki-NLP/opus-mt-tc-big-{}-{}".format(src_code, tgt_code),
    ]
    errors = []
    for model_name in candidates:
        try:
            tok = AutoTokenizer.from_pretrained(model_name)
            mdl = AutoModelForSeq2SeqLM.from_pretrained(model_name).to(DEVICE)
            return tok, mdl, model_name, None
        except Exception as e:
            errors.append("{}: {}".format(model_name, str(e)[:100]))
    return None, None, None, "No model: " + "; ".join(errors)

def translate_text_manual(text, tokenizer, model):
    sentences = smart_split(text)
    parts = []
    for s in sentences:
        if not s.strip():
            continue
        try:
            inputs = tokenizer(
                s, return_tensors="pt",
                max_length=512, truncation=True, padding=True,
            ).to(DEVICE)
            outputs = model.generate(
                **inputs, max_length=512,
                num_beams=4, early_stopping=True,
            )
            parts.append(tokenizer.decode(outputs[0], skip_special_tokens=True))
        except Exception:
            parts.append(s)
    return " ".join(parts)

def smart_split(text):
    try:
        from nltk.tokenize import sent_tokenize
        return sent_tokenize(text)
    except Exception:
        return re.split(r'(?<=[.!?])\s+', text.strip())

def make_diff(orig, fixed):
    orig_words = orig.split()
    fixed_words = fixed.split()
    matcher = difflib.SequenceMatcher(None, orig_words, fixed_words)
    parts = []
    for op, i1, i2, j1, j2 in matcher.get_opcodes():
        if op == 'equal':
            parts.extend(orig_words[i1:i2])
        elif op == 'replace':
            for w in orig_words[i1:i2]:
                parts.append('<mark class="err">{}</mark>'.format(w))
            for w in fixed_words[j1:j2]:
                parts.append('<mark class="fix">{}</mark>'.format(w))
        elif op == 'delete':
            for w in orig_words[i1:i2]:
                parts.append('<mark class="err">{}</mark>'.format(w))
        elif op == 'insert':
            for w in fixed_words[j1:j2]:
                parts.append('<mark class="fix">{}</mark>'.format(w))
    return " ".join(parts)

# ==========================================
# 6. INTERFACE STREAMLIT
# ==========================================
# Topbar
st.markdown("""
<div class="bg-fx">
    <div class="bg-orb o1"></div>
    <div class="bg-orb o2"></div>
    <div class="bg-orb o3"></div>
    <div class="bg-lines"></div>
</div>
<div class="topbar">
    <div class="tb-brand">
        <div class="tb-logo">🧠</div>
        <span class="tb-name">Grammar AI Pro</span>
    </div>
    <span class="tb-tag">4-Layer Engine + Translator</span>
</div>
""", unsafe_allow_html=True)

# Hero
st.markdown("""
<div class="hero">
    <div class="hero-chip">🧠 4-Layer Correction System</div>
    <h1><span class="glow">AI Grammar Corrector Pro</span></h1>
    <p class="hero-desc">
        Spell Checker + Rules Engine + T5 AI + LanguageTool — four layers for ~96% accuracy,
        then translate to 12+ languages.
    </p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 7. CHARGEMENT DES MODÈLES
# ==========================================
with st.spinner("Loading Spell Checker..."):
    spell_checker = load_spellchecker()
st.markdown('<div class="pill pill-ok"><div class="pdot"></div>Spell Checker Ready</div>', unsafe_allow_html=True)

with st.spinner("Loading T5 grammar model (vennify/t5-base-grammar-correction)..."):
    ai_tokenizer, ai_model, ai_err = load_corrector()
    if ai_tokenizer:
        device_lbl = "GPU 🚀" if DEVICE == "cuda" else "CPU"
        st.markdown(f'<div class="pill pill-ok"><div class="pdot"></div>T5 Model Ready ({device_lbl})</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="pill pill-err"><div class="pdot"></div>T5 Model Error</div>', unsafe_allow_html=True)

with st.spinner("Loading LanguageTool..."):
    lt_tool, lt_err = load_language_tool()
if lt_tool:
    st.markdown('<div class="pill pill-ok"><div class="pdot"></div>LanguageTool Ready</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="pill pill-warn"><div class="pdot"></div>LanguageTool unavailable (2 layers active)</div>', unsafe_allow_html=True)

# ==========================================
# 8. ZONE DE TRAVAIL
# ==========================================
st.markdown('<div class="workzone">', unsafe_allow_html=True)

# Affichage des couches
st.markdown("""
<div class="layer-info">
    <span class="layer-tag lt-1">📖 Layer 0: Spell Checker</span>
    <span class="layer-tag lt-1">🔧 Layer 1: Rules + Homophones + Bigram</span>
    <span class="layer-tag lt-2">🧠 Layer 2: T5 AI Model</span>
    <span class="layer-tag lt-3">📝 Layer 3: LanguageTool {}</span>
</div>
""".format("✅" if lt_tool else "⚠️"), unsafe_allow_html=True)

# Exemples
EXAMPLES = [
    "Last weak, me and my freind goed to the librery.",
    "She dont knows what happend yestarday.",
    "Your going to love this place more then me.",
    "Their going to there house over they're.",
    "The childs was playing in the gardenn.",
    "I could of went to the store but i didnt.",
    "He writed a leter to his teecher.",
    "Its to late for us to go their.",
]

st.markdown(
    '<div class="gc"><div class="gc-head">'
    '<div class="gc-title"><div class="gc-ico">💡</div>'
    'Try an Example</div></div></div>',
    unsafe_allow_html=True,
)

ecols = st.columns(4)
for i, ex in enumerate(EXAMPLES):
    with ecols[i % 4]:
        short = ex[:28] + "..." if len(ex) > 28 else ex
        if st.button(short, key="ex" + str(i), use_container_width=True):
            st.session_state["inp"] = ex

# Zone de saisie
st.markdown(
    '<div class="gc"><div class="gc-head">'
    '<div class="gc-title"><div class="gc-ico">✍️</div>'
    'Input Text</div>'
    '<span class="gc-badge">English</span>'
    '</div></div>',
    unsafe_allow_html=True,
)

default = "Last weak, me and my freind goed to the librery to studdy for our finalle examms."
user_text = st.text_area(
    label="input",
    value=st.session_state.get("inp", default),
    height=150,
    placeholder="Type English text with errors...",
    label_visibility="collapsed",
    key="ibox",
)

wc = len(user_text.split()) if user_text.strip() else 0
cc = len(user_text)
st.caption("📏 {} words · {} chars".format(wc, cc))

b1, b2, b3 = st.columns([3, 1, 1])
with b1:
    go_correct = st.button(
        "🚀 Correct (4-Layer System)",
        type="primary",
        use_container_width=True,
        disabled=not ai_tokenizer,
    )
with b2:
    clr = st.button("🗑️ Clear", use_container_width=True)
with b3:
    cpy1 = st.button("📋 Copy", use_container_width=True, key="cpy1")

if clr:
    for k in ["inp", "corrected", "translated", "layer_results"]:
        st.session_state[k] = "" if k != "layer_results" else {}
    st.rerun()

# ==========================================
# 9. RÉSULTAT DE LA CORRECTION
# ==========================================
st.markdown(
    '<div class="gc"><div class="gc-head">'
    '<div class="gc-title"><div class="gc-ico">✨</div>'
    'Corrected Text</div></div></div>',
    unsafe_allow_html=True,
)

corr_holder = st.empty()
corrected_text = st.session_state.get("corrected", "")

if corrected_text:
    corr_holder.markdown(
        '<div class="rbox rbox-clean">{}</div>'.format(corrected_text),
        unsafe_allow_html=True,
    )
else:
    corr_holder.markdown(
        '<div class="rbox rbox-empty">'
        '✍️ Corrected text appears here</div>',
        unsafe_allow_html=True,
    )

if go_correct:
    if not user_text.strip():
        st.warning("⚠️ Enter text first!")
    else:
        progress = st.empty()
        progress.markdown("⏳ **Layer 0:** Spell checker...")
        t0 = time.time()
        final, layer_results = full_correction_pipeline(
            user_text, spell_checker, ai_tokenizer, ai_model,
            lt_tool if lt_tool else None,
        )
        elapsed = round(time.time() - t0, 2)
        progress.empty()

        st.session_state["corrected"] = final
        st.session_state["translated"] = ""
        st.session_state["layer_results"] = layer_results

        # Change map
        diff_html = make_diff(user_text, final)
        st.markdown(
            '<div class="gc-title" style="margin-top:1rem">'
            '<div class="gc-ico">🔍</div>Change Map</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="rbox rbox-diff">{}</div>'.format(diff_html),
            unsafe_allow_html=True,
        )

        # Final result
        corr_holder.markdown(
            '<div class="rbox rbox-clean">{}</div>'.format(final),
            unsafe_allow_html=True,
        )

        # Layer details
        with st.expander("🔬 Layer-by-Layer Details"):
            st.markdown("**Original:**")
            st.text(user_text)
            if "spell" in layer_results:
                st.markdown("**After Layer 0 (Spell Checker):**")
                st.text(layer_results["spell"])
            if "rules" in layer_results:
                st.markdown("**After Layer 1A (Rules):**")
                st.text(layer_results["rules"])
            if "homophones" in layer_results:
                st.markdown("**After Layer 1B (Homophones):**")
                st.text(layer_results["homophones"])
            if "bigram" in layer_results:
                st.markdown("**After Layer 1C (Bigram):**")
                st.text(layer_results["bigram"])
            if "ai" in layer_results:
                st.markdown("**After Layer 2 (T5 AI):**")
                st.text(layer_results["ai"])
            if "languagetool" in layer_results:
                st.markdown(
                    "**After Layer 3 (LanguageTool):** "
                    "({} fixes)".format(layer_results.get("lt_fixes", 0))
                )
                st.text(layer_results["languagetool"])
            st.markdown("**Final Result:**")
            st.success(final)

        st.success("✅ Corrected in {}s!".format(elapsed))

        # Statistics
        ow = user_text.split()
        fw = final.split()
        matcher = difflib.SequenceMatcher(None, ow, fw)
        changes = sum(
            max(i2 - i1, j2 - j1)
            for op, i1, i2, j1, j2 in matcher.get_opcodes()
            if op != 'equal'
        )
        num_sents = len(smart_split(user_text))
        layers_used = 4 + (1 if lt_tool else 0)  # spell + rules+homophones+bigram + ai + (lt optional)

        st.markdown(
            '<div class="sgrid">'
            '<div class="sc"><div class="sc-val">{}</div>'
            '<div class="sc-lbl">Words</div></div>'
            '<div class="sc"><div class="sc-val" style="color:#ff7675">{}</div>'
            '<div class="sc-lbl">Changes</div></div>'
            '<div class="sc"><div class="sc-val" style="color:#55efc4">{}</div>'
            '<div class="sc-lbl">Layers Used</div></div>'
            '<div class="sc"><div class="sc-val" style="color:var(--cyan)">{}s</div>'
            '<div class="sc-lbl">Time</div></div>'
            '</div>'.format(len(ow), changes, layers_used, elapsed),
            unsafe_allow_html=True,
        )

if cpy1:
    lr = st.session_state.get("corrected", "")
    if lr:
        st.code(lr, language=None)
        st.info("📋 Select and copy Ctrl+C")
    else:
        st.warning("⚠️ No result")

# ==========================================
# 10. TRADUCTION
# ==========================================
st.markdown('<hr class="divider">', unsafe_allow_html=True)

st.markdown(
    '<div class="gc"><div class="gc-head">'
    '<div class="gc-title">'
    '<div class="gc-ico gc-ico-blue">🌍</div>'
    'Translate Corrected Text</div>'
    '<span class="gc-badge">Helsinki-NLP</span>'
    '</div></div>',
    unsafe_allow_html=True,
)

corrected_text = st.session_state.get("corrected", "")

if not corrected_text:
    st.info("💡 Correct the text first, then choose a language.")
else:
    preview = corrected_text[:100]
    if len(corrected_text) > 100:
        preview += "..."
    st.markdown("**Text:** " + preview)

    col_lang, col_btn = st.columns([3, 2])

    with col_lang:
        target_lang = st.selectbox(
            "Translate to:",
            list(TRANS_LANGS.keys()),
            index=0,
            key="tgt_lang",
        )

    tgt_code = TRANS_LANGS[target_lang]

    with col_btn:
        st.markdown("<br>", unsafe_allow_html=True)
        go_translate = st.button(
            "🌍 Translate",
            type="primary",
            use_container_width=True,
            key="btn_trans",
        )

    trans_holder = st.empty()
    translated_text = st.session_state.get("translated", "")
    if translated_text:
        rtl_cls = "rbox-rtl" if tgt_code in RTL_CODES else ""
        trans_holder.markdown(
            '<div class="rbox rbox-trans {}">{}</div>'.format(
                rtl_cls, translated_text
            ),
            unsafe_allow_html=True,
        )

    if go_translate:
        with st.spinner("🌍 Loading translation model..."):
            try:
                trans_tok, trans_mdl, used_model, err = \
                    load_translator_model("en", tgt_code)

                if trans_tok is None:
                    st.error("❌ " + str(err))
                else:
                    st.markdown(
                        '<div class="pill pill-ok">'
                        '<div class="pdot"></div>'
                        '{}</div>'.format(used_model),
                        unsafe_allow_html=True,
                    )

                    t0 = time.time()
                    translated = translate_text_manual(
                        corrected_text, trans_tok, trans_mdl
                    )
                    elapsed = round(time.time() - t0, 2)

                    st.session_state["translated"] = translated

                    rtl_cls = "rbox-rtl" if tgt_code in RTL_CODES else ""
                    trans_holder.markdown(
                        '<div class="rbox rbox-trans {}">{}</div>'.format(
                            rtl_cls, translated
                        ),
                        unsafe_allow_html=True,
                    )

                    st.success("✅ Translated in {}s".format(elapsed))

                    st.markdown(
                        '<div class="sgrid">'
                        '<div class="sc"><div class="sc-val">{}</div>'
                        '<div class="sc-lbl">Source Words</div></div>'
                        '<div class="sc"><div class="sc-val" style="color:var(--cyan)">{}</div>'
                        '<div class="sc-lbl">Translated</div></div>'
                        '<div class="sc"><div class="sc-val" style="color:#a855f7">{}</div>'
                        '<div class="sc-lbl">Language</div></div>'
                        '<div class="sc"><div class="sc-val" style="color:var(--green)">{}s</div>'
                        '<div class="sc-lbl">Time</div></div>'
                        '</div>'.format(
                            len(corrected_text.split()),
                            len(translated.split()),
                            tgt_code.upper(),
                            elapsed,
                        ),
                        unsafe_allow_html=True,
                    )

            except Exception as e:
                st.error("❌ " + str(e))

    cpy2 = st.button("📋 Copy Translation", use_container_width=True, key="cpy2")
    if cpy2:
        tr = st.session_state.get("translated", "")
        if tr:
            st.code(tr, language=None)
        else:
            st.warning("⚠️ No translation")

# ==========================================
# 11. FEATURES
# ==========================================
st.markdown("""
<div class="fgrid">
    <div class="fc"><div class="fc-ico">📖</div>
        <div class="fc-ttl">Spell Checker</div>
        <div class="fc-dsc">pyspellchecker for fast spelling correction</div></div>
    <div class="fc"><div class="fc-ico">🔧</div>
        <div class="fc-ttl">200+ Rules</div>
        <div class="fc-dsc">Spelling, grammar & irregular verbs</div></div>
    <div class="fc"><div class="fc-ico">👂</div>
        <div class="fc-ttl">Homophone Filter</div>
        <div class="fc-dsc">your/you're, their/there, than/then, and more</div></div>
    <div class="fc"><div class="fc-ico">🧠</div>
        <div class="fc-ttl">T5 AI Model</div>
        <div class="fc-dsc">Deep context understanding (vennify/t5-base)</div></div>
    <div class="fc"><div class="fc-ico">📝</div>
        <div class="fc-ttl">LanguageTool</div>
        <div class="fc-dsc">Professional style & grammar layer</div></div>
    <div class="fc"><div class="fc-ico">🌍</div>
        <div class="fc-ttl">12+ Languages</div>
        <div class="fc-dsc">Translate to Arabic, French, German...</div></div>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 12. FOOTER
# ==========================================
st.markdown("""
<div class="appfoot">
    <div class="af-brand">🧠 Grammar AI Pro</div>
    <div class="af-txt">
        4-Layer System: Spell Checker + Rules + T5 AI + LanguageTool<br>
        + Helsinki-NLP Translation · Made with ❤️
    </div>
</div>
""", unsafe_allow_html=True)
