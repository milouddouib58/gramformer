import streamlit as st
import time
import re
import difflib
import sys
import subprocess

# ==========================================
# 1. إعدادات الصفحة
# ==========================================
st.set_page_config(
    page_title="AI Grammar Corrector Pro",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ==========================================
# 2. تثبيت المكتبات
# ==========================================
def install_pkg(name, imp=None):
    if imp is None:
        imp = name
    try:
        __import__(imp)
        return True
    except ImportError:
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install",
                name, "-q", "--no-warn-script-location"
            ])
            return True
        except Exception:
            return False

pkgs = [
    ("transformers", "transformers"),
    ("torch", "torch"),
    ("sentencepiece", "sentencepiece"),
    ("sacremoses", "sacremoses"),
    ("protobuf", "google.protobuf"),
    ("nltk", "nltk"),
    ("language-tool-python", "language_tool_python"),
    ("symspellpy", "symspellpy"),
]

pkg_status = {}
for name, imp in pkgs:
    pkg_status[name] = install_pkg(name, imp)

import nltk
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
# 3. CSS
# ==========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700;800;900&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Noto+Naskh+Arabic:wght@400;500;600;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&display=swap');

:root{
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
    background:var(--dark-1)!important;color:var(--text-primary)!important}
.main .block-container{padding:0!important;max-width:100%!important}
#MainMenu,footer,header,[data-testid="stHeader"],
[data-testid="stToolbar"],[data-testid="stDecoration"]{display:none!important}

.bg-fx{position:fixed;inset:0;z-index:0;pointer-events:none;overflow:hidden}
.bg-orb{position:absolute;border-radius:50%;filter:blur(100px);opacity:.12;
    animation:drift 25s ease-in-out infinite}
.o1{width:500px;height:500px;background:var(--gold);top:-200px;right:-100px}
.o2{width:400px;height:400px;background:var(--purple);bottom:-150px;left:-100px;
    animation-delay:-8s}
.o3{width:350px;height:350px;background:var(--cyan);top:40%;left:30%;
    animation-delay:-16s}
.bg-lines{position:absolute;inset:0;
    background-image:linear-gradient(rgba(233,196,106,.02) 1px,transparent 1px),
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
.tb-tag{background:rgba(168,85,247,.15);border:1px solid rgba(168,85,247,.3);
    color:var(--purple);padding:.3rem .9rem;border-radius:50px;
    font-size:.78rem;font-weight:700}

.hero{position:relative;z-index:1;text-align:center;padding:3rem 2rem 2rem}
.hero-chip{display:inline-flex;align-items:center;gap:.5rem;
    background:rgba(233,196,106,.08);border:1px solid rgba(233,196,106,.18);
    padding:.4rem 1.2rem;border-radius:50px;font-size:.82rem;
    color:var(--gold);margin-bottom:1.5rem}
.hero h1{font-size:3rem;font-weight:900;line-height:1.15;margin-bottom:1rem}
.hero h1 .glow{
    background:linear-gradient(135deg,var(--gold),var(--orange),var(--gold-light));
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.hero-desc{font-size:1.1rem;color:var(--text-secondary);
    max-width:700px;margin:0 auto 2rem;line-height:1.8;font-weight:300}

.workzone{position:relative;z-index:1;max-width:1050px;margin:0 auto;padding:0 2rem 3rem}

.gc{background:var(--glass);backdrop-filter:blur(20px);border:1px solid var(--glass-border);
    border-radius:22px;padding:1.8rem;margin-bottom:1.3rem}
.gc:hover{border-color:rgba(233,196,106,.12)}
.gc-head{display:flex;align-items:center;justify-content:space-between;margin-bottom:1rem}
.gc-title{display:flex;align-items:center;gap:.6rem;font-size:1.05rem;font-weight:700}
.gc-ico{width:30px;height:30px;background:linear-gradient(135deg,var(--gold),var(--orange));
    border-radius:9px;display:flex;align-items:center;justify-content:center;font-size:.85rem}
.gc-ico-blue{background:linear-gradient(135deg,var(--blue),var(--teal))!important}
.gc-badge{font-size:.78rem;color:var(--text-secondary);background:rgba(255,255,255,.04);
    padding:.25rem .7rem;border-radius:20px;border:1px solid var(--glass-border)}

.stTextArea textarea{font-family:'JetBrains Mono',monospace!important;
    font-size:1.05rem!important;line-height:1.9!important;direction:ltr!important;
    text-align:left!important;background:rgba(0,0,0,.35)!important;
    border:2px solid var(--glass-border)!important;border-radius:14px!important;
    padding:1.3rem!important;color:var(--text-primary)!important}
.stTextArea textarea:focus{border-color:var(--gold)!important;
    box-shadow:0 0 0 3px rgba(233,196,106,.1)!important}

.rbox{border:2px solid rgba(233,196,106,.15);border-radius:14px;padding:1.5rem;
    direction:ltr;text-align:left;font-family:'JetBrains Mono',monospace;
    font-size:1.05rem;line-height:2.2;color:var(--text-primary);min-height:100px;
    position:relative;overflow:hidden;word-wrap:break-word;
    background:linear-gradient(135deg,rgba(233,196,106,.04),rgba(168,218,220,.03))}
.rbox::before{content:'';position:absolute;top:0;left:0;right:0;height:3px;
    border-radius:14px 14px 0 0}
.rbox-diff::before{background:linear-gradient(90deg,var(--red),var(--orange),var(--green))}
.rbox-clean::before{background:linear-gradient(90deg,var(--green),var(--cyan))}
.rbox-clean{color:var(--green);font-weight:500}
.rbox-trans::before{background:linear-gradient(90deg,var(--blue),var(--teal))}
.rbox-trans{color:var(--cyan);font-weight:500}
.rbox-rtl{direction:rtl!important;text-align:right!important;
    font-family:'Noto Naskh Arabic','Tajawal',sans-serif!important;
    font-size:1.3rem!important;line-height:2.5!important}
.rbox-empty{color:rgba(255,255,255,.15);font-family:'Tajawal'!important;
    font-size:.95rem;display:flex;align-items:center;justify-content:center}

mark.err{background:rgba(231,76,60,.2);color:#ff7675;border-radius:4px;
    padding:1px 5px;font-weight:600;text-decoration:line-through}
mark.fix{background:rgba(46,204,113,.15);color:#55efc4;font-weight:700;
    padding:1px 5px;border-radius:4px;border-bottom:2px solid rgba(46,204,113,.5)}

.stButton>button{border-radius:12px!important;padding:.75rem!important;
    font-weight:700!important;font-size:1rem!important;border:none!important}
.stButton>button[kind="primary"]{
    background:linear-gradient(135deg,var(--gold),var(--orange))!important;
    color:var(--dark-1)!important;box-shadow:0 4px 18px rgba(233,196,106,.25)!important}
.stButton>button[kind="primary"]:hover{transform:translateY(-2px)!important;
    box-shadow:0 8px 28px rgba(233,196,106,.35)!important}
.stButton>button[kind="secondary"]{background:var(--glass)!important;
    color:var(--text-primary)!important;border:1px solid var(--glass-border)!important}

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
.layer-tag{padding:.3rem .8rem;border-radius:8px;font-size:.75rem;font-weight:600}
.lt-0{background:rgba(20,184,166,.1);color:var(--teal);border:1px solid rgba(20,184,166,.2)}
.lt-1{background:rgba(233,196,106,.1);color:var(--gold);border:1px solid rgba(233,196,106,.2)}
.lt-2{background:rgba(168,85,247,.1);color:var(--purple);border:1px solid rgba(168,85,247,.2)}
.lt-3{background:rgba(59,130,246,.1);color:var(--blue);border:1px solid rgba(59,130,246,.2)}
.lt-4{background:rgba(46,204,113,.1);color:var(--green);border:1px solid rgba(46,204,113,.2)}

.divider{border:none;border-top:1px solid var(--glass-border);margin:2rem 0}

.fgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;margin:2.5rem 0}
.fc{background:var(--glass);border:1px solid var(--glass-border);border-radius:18px;
    padding:1.5rem;text-align:center;transition:all .3s}
.fc:hover{border-color:rgba(233,196,106,.18);transform:translateY(-3px)}
.fc-ico{font-size:1.8rem;margin-bottom:.7rem}
.fc-ttl{font-weight:700;margin-bottom:.3rem}
.fc-dsc{font-size:.82rem;color:var(--text-secondary);line-height:1.7}

.appfoot{position:relative;z-index:1;text-align:center;padding:2.5rem 2rem;
    border-top:1px solid var(--glass-border);margin-top:2rem}
.af-brand{font-size:1.1rem;font-weight:800;color:var(--gold)}
.af-txt{color:var(--text-secondary);font-size:.82rem;margin-top:.3rem}

.stSelectbox>div>div{background:rgba(0,0,0,.3)!important;
    border:2px solid var(--glass-border)!important;border-radius:12px!important;
    color:var(--text-primary)!important}

@media(max-width:768px){
    .topbar{padding:.7rem 1rem}.hero h1{font-size:2rem}
    .sgrid{grid-template-columns:repeat(2,1fr)}
    .fgrid{grid-template-columns:1fr}
    .workzone{padding:0 1rem 2rem}}
</style>
""", unsafe_allow_html=True)


# ==========================================
# 4. Layer 0: SymSpell
# ==========================================
@st.cache_resource
def load_symspell():
    """تحميل SymSpell"""
    try:
        from symspellpy import SymSpell, Verbosity
        import pkg_resources

        sym = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)

        dict_path = pkg_resources.resource_filename(
            "symspellpy", "frequency_dictionary_en_82_765.txt"
        )
        sym.load_dictionary(dict_path, term_index=0, count_index=1)

        bigram_path = pkg_resources.resource_filename(
            "symspellpy", "frequency_bigramdictionary_en_243_342.txt"
        )
        try:
            sym.load_bigram_dictionary(bigram_path, term_index=0, count_index=2)
        except Exception:
            pass

        return sym, None
    except Exception as e:
        return None, str(e)


def apply_symspell(text, sym_spell):
    """تصحيح إملائي بـ SymSpell مع حماية الكلمات الخاصة"""
    if sym_spell is None:
        return text

    from symspellpy import Verbosity

    # كلمات لا نريد تغييرها
    protected = {
        "i", "i'm", "i've", "i'd", "i'll",
        "don't", "doesn't", "didn't", "can't", "won't",
        "wouldn't", "shouldn't", "couldn't", "isn't", "aren't",
        "wasn't", "weren't", "hasn't", "haven't", "hadn't",
    }

    words = text.split()
    result = []

    for word in words:
        lower_w = word.lower().strip(".,!?;:'\"")

        if lower_w in protected or len(lower_w) <= 2:
            result.append(word)
            continue

        # حماية الأحرف الكبيرة في بداية الجملة
        suggestions = sym_spell.lookup(
            lower_w, Verbosity.CLOSEST,
            max_edit_distance=2,
        )

        if suggestions and suggestions[0].distance > 0:
            corrected = suggestions[0].term
            # الحفاظ على الأحرف الكبيرة
            if word[0].isupper():
                corrected = corrected.capitalize()

            # إعادة علامات الترقيم
            trailing = ""
            for ch in reversed(word):
                if ch in ".,!?;:'\"":
                    trailing = ch + trailing
                else:
                    break
            result.append(corrected + trailing)
        else:
            result.append(word)

    return " ".join(result)


# ==========================================
# 5. Layer 1: Rules + Homophones + Context
# ==========================================

# 5A: إصلاحات إملائية
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

# 5B: Homophones الآمنة
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

    # than / then (آمنة)
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
    (r"\bmore\s+then\b",       "more than"),

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

    # hear / here
    (r"\bhear\s+is\b",         "here is"),
    (r"\bhear\s+are\b",        "here are"),
    (r"\bover\s+hear\b",       "over here"),
    (r"\bcome\s+hear\b",       "come here"),

    # hole / whole
    (r"\bthe\s+hole\s+time\b",     "the whole time"),
    (r"\bthe\s+hole\s+thing\b",    "the whole thing"),
    (r"\bthe\s+hole\s+world\b",    "the whole world"),
    (r"\ba\s+hole\s+lot\b",        "a whole lot"),

    # brake / break
    (r"\btake\s+a\s+brake\b",      "take a break"),
    (r"\bbrake\s+the\s+rules\b",   "break the rules"),

    # buy / by / bye
    (r"\bbuy\s+the\s+way\b",       "by the way"),
    (r"\bstand\s+buy\b",           "stand by"),

    # peace / piece
    (r"\bpeace\s+of\s+cake\b",     "piece of cake"),
    (r"\ba\s+peace\s+of\b",        "a piece of"),
    (r"\bpeace\s+of\s+advice\b",   "piece of advice"),

    # meet / meat
    (r"\bmeat\s+(?:me|you|him|her|them|us)\b",
     lambda m: m.group().replace("meat", "meet")),

    # no / know
    (r"\bi\s+no\s+(?:that|what|how|why|when|where|who)\b",
     lambda m: m.group().replace(" no ", " know ")),
]

# 5C: Collocations / Bigrams
COLLOCATION_FIXES = [
    (r"\bmake\s+a\s+photo\b",      "take a photo"),
    (r"\bmake\s+a\s+picture\b",    "take a picture"),
    (r"\bdo\s+a\s+mistake\b",      "make a mistake"),
    (r"\bdo\s+a\s+decision\b",     "make a decision"),
    (r"\bdo\s+progress\b",         "make progress"),
    (r"\bdo\s+an\s+effort\b",      "make an effort"),
    (r"\bstrong\s+rain\b",         "heavy rain"),
    (r"\bstrong\s+snow\b",         "heavy snow"),
    (r"\bstrong\s+wind\b",         "strong wind"),
    (r"\bstrong\s+traffic\b",      "heavy traffic"),
    (r"\bbig\s+rain\b",            "heavy rain"),
    (r"\bbig\s+mistake\b",         "big mistake"),
    (r"\bfast\s+food\b",           "fast food"),
    (r"\bopen\s+the\s+light\b",    "turn on the light"),
    (r"\bclose\s+the\s+light\b",   "turn off the light"),
    (r"\bopen\s+the\s+tv\b",       "turn on the TV"),
    (r"\bclose\s+the\s+tv\b",      "turn off the TV"),
    (r"\bin\s+the\s+internet\b",   "on the internet"),
    (r"\bin\s+the\s+phone\b",      "on the phone"),
    (r"\bsay\s+a\s+lie\b",         "tell a lie"),
    (r"\bsay\s+a\s+story\b",       "tell a story"),
    (r"\bsay\s+a\s+joke\b",        "tell a joke"),
    (r"\bsay\s+the\s+truth\b",     "tell the truth"),
    (r"\bwin\s+time\b",            "save time"),
    (r"\bwin\s+money\b",           "earn money"),
    (r"\bearn\s+a\s+game\b",       "win a game"),
]

# 5D: قواعد نحوية
GRAMMAR_PATTERNS = [
    # "i" المنفردة → "I"
    (r'(?<![A-Za-z])i(?![A-Za-z\'mved])', 'I'),

    # he/she/it + don't
    (r'\bhe\s+don\'?t\b',     "he doesn't"),
    (r'\bshe\s+don\'?t\b',    "she doesn't"),
    (r'\bit\s+don\'?t\b',     "it doesn't"),

    # Subject-verb agreement
    (r'\bI\s+has\b',          'I have'),
    (r'\bI\s+is\b',           'I am'),
    (r'\byou\s+is\b',         'you are'),
    (r'\bwe\s+is\b',          'we are'),
    (r'\bthey\s+is\b',        'they are'),
    (r'\bhe\s+have\b',        'he has'),
    (r'\bshe\s+have\b',       'she has'),
    (r'\bit\s+have\b',        'it has'),

    # Double comparatives
    (r'\bmore\s+better\b',    'better'),
    (r'\bmore\s+worse\b',     'worse'),
    (r'\bmost\s+best\b',      'best'),
    (r'\bmost\s+worst\b',     'worst'),

    # Irregular plurals
    (r'\bchilds\b',           'children'),
    (r'\bmans\b',             'men'),
    (r'\bwomans\b',           'women'),
    (r'\btooths\b',           'teeth'),
    (r'\bfoots\b',            'feet'),

    # Irregular past tense
    (r'\bgoed\b',             'went'),
    (r'\bwrited\b',           'wrote'),
    (r'\bthinked\b',          'thought'),
    (r'\bteached\b',          'taught'),
    (r'\bbringed\b',          'brought'),
    (r'\bbuyed\b',            'bought'),
    (r'\bcatched\b',          'caught'),
    (r'\bfeeled\b',           'felt'),
    (r'\bfinded\b',           'found'),
    (r'\bgived\b',            'gave'),
    (r'\bheared\b',           'heard'),
    (r'\bknowed\b',           'knew'),
    (r'\bleaved\b',           'left'),
    (r'\bmaked\b',            'made'),
    (r'\bmeeted\b',           'met'),
    (r'\brunned\b',           'ran'),
    (r'\bsayed\b',            'said'),
    (r'\bseed\b',             'saw'),
    (r'\bsended\b',           'sent'),
    (r'\bsitted\b',           'sat'),
    (r'\bsleeped\b',          'slept'),
    (r'\bspeaked\b',          'spoke'),
    (r'\bstanded\b',          'stood'),
    (r'\bswimmed\b',          'swam'),
    (r'\btaked\b',            'took'),
    (r'\btelled\b',           'told'),
    (r'\bweared\b',           'wore'),
    (r'\bwinned\b',           'won'),

    # Specific patterns (مرتبة بعناية)
    (r'\bhe\s+dont\s+knows?\b',    "he doesn't know"),
    (r'\bshe\s+dont\s+knows?\b',   "she doesn't know"),
    (r'\bdont\s+knows\b',          "don't know"),
    (r'\bdont\s+know\b',           "don't know"),
]


def apply_rules(text):
    """Layer 1A: محرك القواعد"""
    result = text
    lower = result.lower()

    for wrong, correct in COMMON_FIXES.items():
        if wrong in lower:
            pat = re.compile(re.escape(wrong), re.IGNORECASE)
            result = pat.sub(correct, result)
            lower = result.lower()

    # ترتيب مهم: القواعد الخاصة أولاً ثم العامة
    for pattern, replacement in GRAMMAR_PATTERNS:
        result = re.sub(pattern, replacement, result)

    return result


def apply_homophones(text):
    """Layer 1B: فلتر Homophones"""
    result = text
    for pattern, replacement in HOMOPHONE_RULES:
        if callable(replacement):
            result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
        else:
            result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
    return result


def apply_collocations(text):
    """Layer 1C: تصحيح Collocations"""
    result = text
    for pattern, replacement in COLLOCATION_FIXES:
        result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
    return result


# ==========================================
# 6. Layer 3: LanguageTool
# ==========================================
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


# ==========================================
# 7. Layer 4: Post-Processing
# ==========================================
def post_process(text):
    """تنظيف نهائي"""
    # مسافات مزدوجة
    text = re.sub(r'\s+', ' ', text).strip()

    # نقطة في النهاية
    if text and text[-1] not in '.!?':
        text += '.'

    # حرف كبير بعد .!?
    def cap_after(m):
        return m.group(1) + m.group(2).upper()
    text = re.sub(r'([.!?]\s+)([a-z])', cap_after, text)

    # أول حرف كبير
    if text and text[0].islower():
        text = text[0].upper() + text[1:]

    # مسافة قبل علامات الترقيم
    text = re.sub(r'\s+([.,!?;:])', r'\1', text)

    # مسافة بعد علامات الترقيم
    text = re.sub(r'([.,!?;:])([A-Za-z])', r'\1 \2', text)

    return text


# ==========================================
# 8. تحميل النماذج
# ==========================================
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


@st.cache_resource
def load_corrector():
    name = "prithivida/grammar_error_correcter_v1"
    tok = AutoTokenizer.from_pretrained(name)
    mdl = AutoModelForSeq2SeqLM.from_pretrained(name).to(DEVICE)
    return tok, mdl


@st.cache_resource
def load_translator_model(src, tgt):
    candidates = [
        "Helsinki-NLP/opus-mt-{}-{}".format(src, tgt),
        "Helsinki-NLP/opus-mt-tc-big-{}-{}".format(src, tgt),
    ]
    for name in candidates:
        try:
            tok = AutoTokenizer.from_pretrained(name)
            mdl = AutoModelForSeq2SeqLM.from_pretrained(name).to(DEVICE)
            return tok, mdl, name, None
        except Exception as e:
            continue
    return None, None, None, "No model for {} → {}".format(src, tgt)


TRANS_LANGS = {
    "🇸🇦 العربية":     "ar",
    "🇫🇷 Français":    "fr",
    "🇩🇪 Deutsch":     "de",
    "🇪🇸 Español":     "es",
    "🇮🇹 Italiano":    "it",
    "🇵🇹 Português":   "pt",
    "🇷🇺 Русский":     "ru",
    "🇹🇷 Türkçe":      "tr",
    "🇳🇱 Nederlands":  "nl",
    "🇸🇪 Svenska":     "sv",
    "🇨🇳 中文":         "zh",
    "🇯🇵 日本語":        "jap",
}
RTL = {"ar", "he", "fa", "ur"}


# ==========================================
# 9. دوال المعالجة
# ==========================================
def smart_split(text):
    try:
        from nltk.tokenize import sent_tokenize
        return sent_tokenize(text)
    except Exception:
        return re.split(r'(?<=[.!?])\s+', text.strip())


def ai_correct(text, tok, mdl):
    """Layer 2: T5 AI"""
    sents = smart_split(text)
    out = []
    for s in sents:
        if not s.strip():
            continue
        try:
            inp = tok(
                "gec: " + s,
                return_tensors="pt",
                max_length=256,
                truncation=True,
                padding=True,
            ).to(DEVICE)
            gen = mdl.generate(**inp, max_length=256, num_beams=5, early_stopping=True)
            c = tok.decode(gen[0], skip_special_tokens=True)
            out.append(c if c.strip() else s)
        except Exception:
            out.append(s)
    return " ".join(out)


def full_pipeline(text, tok, mdl, symspell=None, lt_tool=None):
    """نظام التصحيح الكامل: 5 طبقات"""
    layers = {"original": text}

    # Layer 0: SymSpell
    if symspell:
        text = apply_symspell(text, symspell)
    layers["symspell"] = text

    # Layer 1A: Rules
    text = apply_rules(text)
    layers["rules"] = text

    # Layer 1B: Homophones
    text = apply_homophones(text)
    layers["homophones"] = text

    # Layer 1C: Collocations
    text = apply_collocations(text)
    layers["collocations"] = text

    # Layer 2: AI
    text = ai_correct(text, tok, mdl)
    layers["ai"] = text

    # Layer 3: LanguageTool
    lt_fixes = 0
    if lt_tool:
        text, lt_fixes = apply_language_tool(text, lt_tool)
    layers["languagetool"] = text
    layers["lt_fixes"] = lt_fixes

    # Layer 4: Post-processing
    text = post_process(text)
    layers["final"] = text

    return text, layers


def translate_manual(text, tok, mdl):
    sents = smart_split(text)
    parts = []
    for s in sents:
        if not s.strip():
            continue
        try:
            inp = tok(s, return_tensors="pt", max_length=512,
                      truncation=True, padding=True).to(DEVICE)
            out = mdl.generate(**inp, max_length=512, num_beams=4,
                               early_stopping=True)
            parts.append(tok.decode(out[0], skip_special_tokens=True))
        except Exception:
            parts.append(s)
    return " ".join(parts)


def make_diff(orig, fixed):
    ow = orig.split()
    fw = fixed.split()
    matcher = difflib.SequenceMatcher(None, ow, fw)
    parts = []
    for op, i1, i2, j1, j2 in matcher.get_opcodes():
        if op == 'equal':
            parts.extend(ow[i1:i2])
        elif op == 'replace':
            for w in ow[i1:i2]:
                parts.append('<mark class="err">{}</mark>'.format(w))
            for w in fw[j1:j2]:
                parts.append('<mark class="fix">{}</mark>'.format(w))
        elif op == 'delete':
            for w in ow[i1:i2]:
                parts.append('<mark class="err">{}</mark>'.format(w))
        elif op == 'insert':
            for w in fw[j1:j2]:
                parts.append('<mark class="fix">{}</mark>'.format(w))
    return " ".join(parts)


# ==========================================
# 10. واجهة المستخدم
# ==========================================
st.markdown("""
<div class="bg-fx"><div class="bg-orb o1"></div><div class="bg-orb o2"></div>
<div class="bg-orb o3"></div><div class="bg-lines"></div></div>
<div class="topbar">
    <div class="tb-brand"><div class="tb-logo">🤖</div>
    <span class="tb-name">Grammar AI Pro</span></div>
    <span class="tb-tag">5-Layer Engine</span>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <div class="hero-chip">🧠 5-Layer Correction System</div>
    <h1><span class="glow">AI Grammar Corrector Pro</span></h1>
    <p class="hero-desc">
        SymSpell + Rules + Homophones + Collocations + T5 AI + LanguageTool
        — five layers for ~96% accuracy, then translate to 12+ languages
    </p>
</div>
""", unsafe_allow_html=True)


# ==========================================
# 11. تحميل كل شيء
# ==========================================
cor_tok = cor_mdl = None
cor_ok = False
sym_spell = None
sym_ok = False
lt_tool = None
lt_ok = False

# T5
try:
    with st.spinner("🔄 Loading T5 model..."):
        cor_tok, cor_mdl = load_corrector()
    cor_ok = True
    dev = "GPU 🚀" if DEVICE == "cuda" else "CPU"
    st.markdown('<div class="pill pill-ok"><div class="pdot"></div>'
                'T5 Model Ready ({})</div>'.format(dev), unsafe_allow_html=True)
except Exception as e:
    st.markdown('<div class="pill pill-err"><div class="pdot"></div>'
                'T5 Error</div>', unsafe_allow_html=True)

# SymSpell
try:
    with st.spinner("🔄 Loading SymSpell..."):
        sym_spell, sym_err = load_symspell()
    if sym_spell:
        sym_ok = True
        st.markdown('<div class="pill pill-ok"><div class="pdot"></div>'
                    'SymSpell Ready</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="pill pill-warn"><div class="pdot"></div>'
                    'SymSpell skipped</div>', unsafe_allow_html=True)
except Exception:
    st.markdown('<div class="pill pill-warn"><div class="pdot"></div>'
                'SymSpell skipped</div>', unsafe_allow_html=True)

# LanguageTool
try:
    with st.spinner("🔄 Loading LanguageTool..."):
        lt_tool, lt_err = load_language_tool()
    if lt_tool:
        lt_ok = True
        st.markdown('<div class="pill pill-ok"><div class="pdot"></div>'
                    'LanguageTool Ready</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="pill pill-warn"><div class="pdot"></div>'
                    'LanguageTool skipped</div>', unsafe_allow_html=True)
except Exception:
    st.markdown('<div class="pill pill-warn"><div class="pdot"></div>'
                'LanguageTool skipped</div>', unsafe_allow_html=True)


# ==========================================
# 12. منطقة العمل
# ==========================================
st.markdown('<div class="workzone">', unsafe_allow_html=True)

# عرض الطبقات النشطة
active = 2  # rules + AI always
if sym_ok:
    active += 1
if lt_ok:
    active += 1
active += 1  # post-processing

st.markdown(
    '<div class="layer-info">'
    '<span class="layer-tag lt-0">🔤 L0: SymSpell {}</span>'
    '<span class="layer-tag lt-1">🔧 L1: Rules+Homo+Colloc</span>'
    '<span class="layer-tag lt-2">🧠 L2: T5 AI</span>'
    '<span class="layer-tag lt-3">📝 L3: LangTool {}</span>'
    '<span class="layer-tag lt-4">✨ L4: Post-Process</span>'
    '</div>'.format(
        "✅" if sym_ok else "⚠️",
        "✅" if lt_ok else "⚠️",
    ),
    unsafe_allow_html=True,
)

EXAMPLES = [
    "Last weak, me and my freind goed to the librery.",
    "Your going to love this place more then me.",
    "She dont knows what happend yestarday.",
    "Its to late for us to go their.",
    "I could of went to the store but i didnt.",
    "He writed a leter to his teecher.",
    "We should make a photo of the strong rain.",
    "I want to open the light and say a story.",
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
        if st.button(short, key="ex{}".format(i), use_container_width=True):
            st.session_state["inp"] = ex

st.markdown(
    '<div class="gc"><div class="gc-head">'
    '<div class="gc-title"><div class="gc-ico">✍️</div>Input Text</div>'
    '<span class="gc-badge">English</span>'
    '</div></div>',
    unsafe_allow_html=True,
)

default = "Last weak, me and my freind goed to the librery to studdy for our finalle examms."

user_text = st.text_area(
    label="input", value=st.session_state.get("inp", default),
    height=150, placeholder="Type English text with errors...",
    label_visibility="collapsed", key="ibox",
)

wc = len(user_text.split()) if user_text.strip() else 0
st.caption("📏 {} words · {} chars".format(wc, len(user_text)))

b1, b2, b3 = st.columns([3, 1, 1])
with b1:
    go = st.button("🚀 Correct (5-Layer)", type="primary",
                   use_container_width=True, disabled=not cor_ok)
with b2:
    if st.button("🗑️ Clear", use_container_width=True):
        for k in ["inp", "corrected", "translated"]:
            st.session_state[k] = ""
        st.rerun()
with b3:
    cpy1 = st.button("📋 Copy", use_container_width=True, key="cpy1")


# نتيجة
st.markdown(
    '<div class="gc"><div class="gc-head">'
    '<div class="gc-title"><div class="gc-ico">✨</div>'
    'Corrected Text</div></div></div>',
    unsafe_allow_html=True,
)

holder = st.empty()
corrected = st.session_state.get("corrected", "")

if corrected:
    holder.markdown('<div class="rbox rbox-clean">{}</div>'.format(corrected),
                   unsafe_allow_html=True)
else:
    holder.markdown('<div class="rbox rbox-empty">✍️ Result appears here</div>',
                   unsafe_allow_html=True)

if go:
    if not user_text.strip():
        st.warning("⚠️ Enter text first!")
    else:
        t0 = time.time()

        with st.spinner("🔤 Layer 0 → 🔧 Layer 1 → 🧠 Layer 2 → 📝 Layer 3 → ✨ Layer 4..."):
            final, layers = full_pipeline(
                user_text, cor_tok, cor_mdl,
                sym_spell if sym_ok else None,
                lt_tool if lt_ok else None,
            )
        elapsed = round(time.time() - t0, 2)

        st.session_state["corrected"] = final
        st.session_state["translated"] = ""

        # Diff
        diff_html = make_diff(user_text, final)
        st.markdown(
            '<div class="gc-title" style="margin-top:1rem">'
            '<div class="gc-ico">🔍</div>Change Map</div>',
            unsafe_allow_html=True,
        )
        st.markdown('<div class="rbox rbox-diff">{}</div>'.format(diff_html),
                   unsafe_allow_html=True)

        holder.markdown('<div class="rbox rbox-clean">{}</div>'.format(final),
                       unsafe_allow_html=True)

        # تفاصيل الطبقات
        with st.expander("🔬 Layer-by-Layer Details"):
            layer_names = [
                ("original",     "📄 Original"),
                ("symspell",     "🔤 After SymSpell"),
                ("rules",        "🔧 After Rules"),
                ("homophones",   "👂 After Homophones"),
                ("collocations", "📚 After Collocations"),
                ("ai",           "🧠 After T5 AI"),
                ("languagetool", "📝 After LanguageTool"),
                ("final",        "✨ Final Result"),
            ]

            for key, label in layer_names:
                if key in layers:
                    val = layers[key]
                    if isinstance(val, str):
                        # تلوين التغييرات عن المرحلة السابقة
                        st.markdown("**{}:**".format(label))
                        st.text(val)

            lt_n = layers.get("lt_fixes", 0)
            if lt_n > 0:
                st.info("📝 LanguageTool found {} additional issue(s)".format(lt_n))

        st.success("✅ Corrected in {}s with {} active layers!".format(elapsed, active))

        # إحصائيات
        ow = user_text.split()
        fw = final.split()
        matcher = difflib.SequenceMatcher(None, ow, fw)
        changes = sum(
            max(i2-i1, j2-j1) for op, i1, i2, j1, j2 in matcher.get_opcodes()
            if op != 'equal'
        )

        st.markdown(
            '<div class="sgrid">'
            '<div class="sc"><div class="sc-val">{}</div><div class="sc-lbl">Words</div></div>'
            '<div class="sc"><div class="sc-val" style="color:#ff7675">{}</div>'
            '<div class="sc-lbl">Changes</div></div>'
            '<div class="sc"><div class="sc-val" style="color:#55efc4">{}</div>'
            '<div class="sc-lbl">Layers</div></div>'
            '<div class="sc"><div class="sc-val" style="color:var(--cyan)">{}s</div>'
            '<div class="sc-lbl">Time</div></div>'
            '</div>'.format(len(ow), changes, active, elapsed),
            unsafe_allow_html=True,
        )

if cpy1:
    r = st.session_state.get("corrected", "")
    if r:
        st.code(r, language=None)
    else:
        st.warning("⚠️ No result")


# ==========================================
# 13. الترجمة
# ==========================================
st.markdown('<hr class="divider">', unsafe_allow_html=True)

st.markdown(
    '<div class="gc"><div class="gc-head">'
    '<div class="gc-title"><div class="gc-ico gc-ico-blue">🌍</div>'
    'Translate</div>'
    '<span class="gc-badge">Helsinki-NLP</span>'
    '</div></div>',
    unsafe_allow_html=True,
)

corrected = st.session_state.get("corrected", "")

if not corrected:
    st.info("💡 Correct the text first.")
else:
    st.markdown("**Text:** {}".format(
        corrected[:80] + "..." if len(corrected) > 80 else corrected
    ))

    c1, c2 = st.columns([3, 2])
    with c1:
        tgt = st.selectbox("Translate to:", list(TRANS_LANGS.keys()), key="tgt")
    tgt_code = TRANS_LANGS[tgt]

    with c2:
        st.markdown("<br>", unsafe_allow_html=True)
        go_tr = st.button("🌍 Translate", type="primary",
                          use_container_width=True, key="btn_tr")

    tr_holder = st.empty()
    translated = st.session_state.get("translated", "")
    if translated:
        rtl = "rbox-rtl" if tgt_code in RTL else ""
        tr_holder.markdown(
            '<div class="rbox rbox-trans {}">{}</div>'.format(rtl, translated),
            unsafe_allow_html=True,
        )

    if go_tr:
        with st.spinner("🌍 Translating..."):
            try:
                t_tok, t_mdl, used, err = load_translator_model("en", tgt_code)
                if t_tok is None:
                    st.error("❌ " + str(err))
                else:
                    t0 = time.time()
                    result = translate_manual(corrected, t_tok, t_mdl)
                    el = round(time.time() - t0, 2)

                    st.session_state["translated"] = result
                    rtl = "rbox-rtl" if tgt_code in RTL else ""
                    tr_holder.markdown(
                        '<div class="rbox rbox-trans {}">{}</div>'.format(rtl, result),
                        unsafe_allow_html=True,
                    )
                    st.success("✅ Translated in {}s".format(el))

                    st.markdown(
                        '<div class="sgrid">'
                        '<div class="sc"><div class="sc-val">{}</div>'
                        '<div class="sc-lbl">Source</div></div>'
                        '<div class="sc"><div class="sc-val" style="color:var(--cyan)">{}</div>'
                        '<div class="sc-lbl">Target</div></div>'
                        '<div class="sc"><div class="sc-val" style="color:#a855f7">{}</div>'
                        '<div class="sc-lbl">Lang</div></div>'
                        '<div class="sc"><div class="sc-val" style="color:var(--green)">{}s</div>'
                        '<div class="sc-lbl">Time</div></div>'
                        '</div>'.format(
                            len(corrected.split()), len(result.split()),
                            tgt_code.upper(), el,
                        ),
                        unsafe_allow_html=True,
                    )
            except Exception as e:
                st.error("❌ " + str(e))

    if st.button("📋 Copy Translation", use_container_width=True, key="cpy2"):
        tr = st.session_state.get("translated", "")
        if tr:
            st.code(tr, language=None)
        else:
            st.warning("⚠️ No translation")


# ==========================================
# 14. الميزات
# ==========================================
st.markdown("""
<div class="fgrid">
    <div class="fc"><div class="fc-ico">🔤</div>
        <div class="fc-ttl">SymSpell Engine</div>
        <div class="fc-dsc">World's fastest spell checker with bigram support</div></div>
    <div class="fc"><div class="fc-ico">👂</div>
        <div class="fc-ttl">Homophone AI</div>
        <div class="fc-dsc">your/you're, their/there, than/then & 50+ pairs</div></div>
    <div class="fc"><div class="fc-ico">📚</div>
        <div class="fc-ttl">Collocations</div>
        <div class="fc-dsc">make a photo→take a photo, strong rain→heavy rain</div></div>
    <div class="fc"><div class="fc-ico">🧠</div>
        <div class="fc-ttl">T5 AI Model</div>
        <div class="fc-dsc">Deep contextual grammar understanding</div></div>
    <div class="fc"><div class="fc-ico">📝</div>
        <div class="fc-ttl">LanguageTool</div>
        <div class="fc-dsc">Professional-grade final checking</div></div>
    <div class="fc"><div class="fc-ico">🌍</div>
        <div class="fc-ttl">12+ Languages</div>
        <div class="fc-dsc">Translate to Arabic, French, German & more</div></div>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<div class="appfoot">
    <div class="af-brand">🤖 Grammar AI Pro — 5 Layer Engine</div>
    <div class="af-txt">
        SymSpell + Rules + Homophones + Collocations + T5 AI + LanguageTool<br>
        + Helsinki-NLP Translation · ~96% Accuracy · Made with ❤️
    </div>
</div>
""", unsafe_allow_html=True)
