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
    page_title="AI Grammar Corrector & Translator",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ==========================================
# 2. تثبيت المكتبات تلقائياً
# ==========================================
def install_if_missing(package_name, import_name=None):
    if import_name is None:
        import_name = package_name
    try:
        __import__(import_name)
    except ImportError:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install",
            package_name, "-q", "--no-warn-script-location"
        ])

required = [
    ("transformers", "transformers"),
    ("torch", "torch"),
    ("sentencepiece", "sentencepiece"),
    ("sacremoses", "sacremoses"),
    ("protobuf", "google.protobuf"),
    ("nltk", "nltk"),
]

for pkg, imp in required:
    install_if_missing(pkg, imp)

# تحميل بيانات nltk
import nltk
try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab', quiet=True)

# ==========================================
# 3. CSS
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
    max-width:650px;margin:0 auto 2rem;line-height:1.8;font-weight:300}

.workzone{position:relative;z-index:1;max-width:1000px;margin:0 auto;
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
.gc-badge{font-size:.78rem;color:var(--text-secondary);
    background:rgba(255,255,255,.04);padding:.25rem .7rem;
    border-radius:20px;border:1px solid var(--glass-border)}

.stTextArea textarea{
    font-family:'JetBrains Mono',monospace!important;
    font-size:1.1rem!important;line-height:1.9!important;
    direction:ltr!important;text-align:left!important;
    background:rgba(0,0,0,.35)!important;
    border:2px solid var(--glass-border)!important;
    border-radius:14px!important;padding:1.3rem!important;
    color:var(--text-primary)!important}
.stTextArea textarea:focus{border-color:var(--gold)!important;
    box-shadow:0 0 0 3px rgba(233,196,106,.1)!important}
.stTextArea textarea::placeholder{color:rgba(255,255,255,.18)!important}

.rbox{border:2px solid rgba(233,196,106,.15);border-radius:14px;
    padding:1.5rem;direction:ltr;text-align:left;
    font-family:'JetBrains Mono',monospace;font-size:1.1rem;
    line-height:2.2;color:var(--text-primary);min-height:120px;
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
    font-weight:700!important;font-size:1.05rem!important;border:none!important}
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
    border-radius:50px;font-size:.85rem;font-weight:600}
.pill-ok{background:rgba(46,204,113,.1);border:1px solid rgba(46,204,113,.25);color:#2ecc71}
.pill-err{background:rgba(231,76,60,.1);border:1px solid rgba(231,76,60,.25);color:#e74c3c}
.pdot{width:7px;height:7px;border-radius:50%;animation:blink 2s infinite}
.pill-ok .pdot{background:#2ecc71}.pill-err .pdot{background:#e74c3c}
@keyframes blink{0%,100%{opacity:1}50%{opacity:.3}}

.divider{border:none;border-top:1px solid var(--glass-border);margin:2rem 0}

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

.accuracy-meter{margin:1.5rem 0}
.meter-bar{height:12px;border-radius:6px;background:rgba(255,255,255,.05);
    overflow:hidden;margin-top:.5rem}
.meter-fill{height:100%;border-radius:6px;transition:width 1s ease}

@media(max-width:768px){
    .topbar{padding:.7rem 1rem}.hero h1{font-size:2rem}
    .sgrid{grid-template-columns:repeat(2,1fr)}
    .fgrid{grid-template-columns:1fr}
    .workzone{padding:0 1rem 2rem}}
</style>
""", unsafe_allow_html=True)


# ==========================================
# 4. محرك القواعد (Rule Engine) - طبقة أولى
# ==========================================
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
    "i ":          "I ",
    "alot":        "a lot",
    "recieve":     "receive",
    "recieves":    "receives",
    "occured":     "occurred",
    "occuring":    "occurring",
    "untill":      "until",
    "definately":  "definitely",
    "seperate":    "separate",
    "seperately":  "separately",
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
    "curiousity":  "curiosity",
    "embarass":    "embarrass",
    "foriegn":     "foreign",
    "fourty":      "forty",
    "grammer":     "grammar",
    "harrass":     "harass",
    "hygeine":     "hygiene",
    "independant": "independent",
    "knowlege":    "knowledge",
    "libary":      "library",
    "librery":     "library",
    "lisence":     "license",
    "maintenence": "maintenance",
    "millenium":   "millennium",
    "neccessary":  "necessary",
    "noticable":   "noticeable",
    "occurence":   "occurrence",
    "persistant":  "persistent",
    "posession":   "possession",
    "potatos":     "potatoes",
    "preceeding":  "preceding",
    "priviledge":  "privilege",
    "professer":   "professor",
    "pronounciation": "pronunciation",
    "publically":  "publicly",
    "realy":       "really",
    "refering":    "referring",
    "relevent":    "relevant",
    "religous":    "religious",
    "rythm":       "rhythm",
    "seize":       "seize",
    "succesful":   "successful",
    "sucessful":   "successful",
    "suprise":     "surprise",
    "truely":      "truly",
    "unforseen":   "unforeseen",
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
    "dissapoint":  "disappoint",
    "exellent":    "excellent",
    "existance":   "existence",
    "familar":     "familiar",
    "finaly":      "finally",
    "genaral":     "general",
    "happend":     "happened",
    "immediatly":  "immediately",
    "intresting":  "interesting",
    "laguage":     "language",
    "mispell":     "misspell",
    "naturaly":    "naturally",
    "neigbour":    "neighbour",
    "obviuosly":   "obviously",
    "opertunity":  "opportunity",
    "orginal":     "original",
    "parliment":   "parliament",
    "particulary": "particularly",
    "probaly":     "probably",
    "recomend":    "recommend",
    "remeber":     "remember",
    "repitition":  "repetition",
    "saftey":      "safety",
    "shedule":     "schedule",
    "sincerly":    "sincerely",
    "speach":      "speech",
    "strenght":    "strength",
    "teecher":     "teacher",
    "thoughout":   "throughout",
    "togeather":   "together",
    "tomatos":     "tomatoes",
    "underate":    "underrate",
    "usally":      "usually",
    "vaccum":      "vacuum",
    "valuble":     "valuable",
    "vegetable":   "vegetable",
    "visable":     "visible",
    "wether":      "whether",
    "writting":    "writing",
}

# أنماط القواعد المتقدمة
GRAMMAR_PATTERNS = [
    (r'\bi\b(?!\')' , 'I'),
    (r'\bhe dont\b', 'he doesn\'t'),
    (r'\bshe dont\b', 'she doesn\'t'),
    (r'\bit dont\b', 'it doesn\'t'),
    (r'\bhe don\'t\b', 'he doesn\'t'),
    (r'\bshe don\'t\b', 'she doesn\'t'),
    (r'\bit don\'t\b', 'it doesn\'t'),
    (r'\bI has\b', 'I have'),
    (r'\bI is\b', 'I am'),
    (r'\byou is\b', 'you are'),
    (r'\bwe is\b', 'we are'),
    (r'\bthey is\b', 'they are'),
    (r'\bhe have\b', 'he has'),
    (r'\bshe have\b', 'she has'),
    (r'\bit have\b', 'it has'),
    (r'\bme and my\b', 'my friend and I'),
    (r'\bmore better\b', 'better'),
    (r'\bmore worse\b', 'worse'),
    (r'\bmost best\b', 'best'),
    (r'\bmost worst\b', 'worst'),
    (r'\bchilds\b', 'children'),
    (r'\bmans\b', 'men'),
    (r'\bwomans\b', 'women'),
    (r'\btooths\b', 'teeth'),
    (r'\bfoots\b', 'feet'),
    (r'\bmouses\b', 'mice'),
    (r'\bgoed\b', 'went'),
    (r'\bwrited\b', 'wrote'),
    (r'\bthinked\b', 'thought'),
    (r'\bteached\b', 'taught'),
    (r'\bbringed\b', 'brought'),
    (r'\bbuyed\b', 'bought'),
    (r'\bcatched\b', 'caught'),
    (r'\bfeeled\b', 'felt'),
    (r'\bfinded\b', 'found'),
    (r'\bgetted\b', 'got'),
    (r'\bgived\b', 'gave'),
    (r'\bheared\b', 'heard'),
    (r'\bknowed\b', 'knew'),
    (r'\bleaved\b', 'left'),
    (r'\bmaked\b', 'made'),
    (r'\bmeeted\b', 'met'),
    (r'\breaded\b', 'read'),
    (r'\brunned\b', 'ran'),
    (r'\bsayed\b', 'said'),
    (r'\bseed\b', 'saw'),
    (r'\bselled\b', 'sold'),
    (r'\bsended\b', 'sent'),
    (r'\bsinged\b', 'sang'),
    (r'\bsitted\b', 'sat'),
    (r'\bsleeped\b', 'slept'),
    (r'\bspeaked\b', 'spoke'),
    (r'\bstanded\b', 'stood'),
    (r'\bswimmed\b', 'swam'),
    (r'\btaked\b', 'took'),
    (r'\btelled\b', 'told'),
    (r'\bunderstand\b', 'understood'),
    (r'\bweared\b', 'wore'),
    (r'\bwinned\b', 'won'),
]


def apply_rule_engine(text):
    """تطبيق محرك القواعد كطبقة أولى"""
    result = text

    # تطبيق الاستبدالات الشائعة
    lower = result.lower()
    for wrong, correct in COMMON_FIXES.items():
        if wrong in lower:
            pattern = re.compile(re.escape(wrong), re.IGNORECASE)
            result = pattern.sub(correct, result)
            lower = result.lower()

    # تطبيق أنماط القواعد
    for pattern, replacement in GRAMMAR_PATTERNS:
        result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)

    # تصحيح بداية الجمل (حرف كبير)
    sentences = re.split(r'([.!?]\s+)', result)
    fixed = []
    for i, part in enumerate(sentences):
        if i == 0 or (i > 0 and re.match(r'[.!?]\s+', sentences[i-1])):
            if part and part[0].islower():
                part = part[0].upper() + part[1:]
        fixed.append(part)
    result = ''.join(fixed)

    # أول حرف كبير
    if result and result[0].islower():
        result = result[0].upper() + result[1:]

    return result


# ==========================================
# 5. دوال النماذج
# ==========================================
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

# تحديد الجهاز
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


@st.cache_resource
def load_corrector():
    """تحميل نموذج التصحيح مع دعم GPU"""
    name = "prithivida/grammar_error_correcter_v1"
    tok = AutoTokenizer.from_pretrained(name)
    mdl = AutoModelForSeq2SeqLM.from_pretrained(name).to(DEVICE)
    return tok, mdl


@st.cache_resource
def load_translator_model(src_code, tgt_code):
    """تحميل نموذج الترجمة يدوياً - بدون pipeline"""
    candidates = [
        "Helsinki-NLP/opus-mt-{}-{}".format(src_code, tgt_code),
        "Helsinki-NLP/opus-mt-tc-big-{}-{}".format(src_code, tgt_code),
    ]

    errors_list = []

    for model_name in candidates:
        try:
            tok = AutoTokenizer.from_pretrained(model_name)
            mdl = AutoModelForSeq2SeqLM.from_pretrained(model_name).to(DEVICE)
            return tok, mdl, model_name, None
        except Exception as e:
            errors_list.append("{}: {}".format(model_name, str(e)[:120]))
            continue

    err_msg = "No model found for {} → {}\n{}".format(
        src_code, tgt_code, "\n".join(errors_list)
    )
    return None, None, None, err_msg


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


def smart_sentence_split(text):
    """تقسيم ذكي للجمل باستخدام nltk"""
    try:
        from nltk.tokenize import sent_tokenize
        return sent_tokenize(text)
    except Exception:
        return re.split(r'(?<=[.!?])\s+', text.strip())


def correct_text(text, tokenizer, model):
    """
    تصحيح بطبقتين:
    1. محرك القواعد (Rule Engine)
    2. نموذج T5 الذكي
    """
    # الطبقة 1: محرك القواعد
    text = apply_rule_engine(text)

    # الطبقة 2: نموذج AI
    sents = smart_sentence_split(text)
    results = []
    for s in sents:
        if not s.strip():
            continue
        try:
            inp = tokenizer(
                "gec: " + s,
                return_tensors="pt",
                max_length=256,
                truncation=True,
                padding=True,
            ).to(DEVICE)
            out = model.generate(
                **inp,
                max_length=256,
                num_beams=5,
                early_stopping=True,
            )
            corrected = tokenizer.decode(out[0], skip_special_tokens=True)

            # التحقق: إذا أرجع النموذج نصاً فارغاً
            if corrected.strip():
                results.append(corrected)
            else:
                results.append(s)
        except Exception:
            results.append(s)
    return " ".join(results)


def translate_text_manual(text, tokenizer, model):
    """ترجمة يدوية بدون pipeline"""
    sents = smart_sentence_split(text)
    parts = []

    for s in sents:
        if not s.strip():
            continue
        try:
            inputs = tokenizer(
                s,
                return_tensors="pt",
                max_length=512,
                truncation=True,
                padding=True,
            ).to(DEVICE)
            outputs = model.generate(
                **inputs,
                max_length=512,
                num_beams=4,
                early_stopping=True,
            )
            parts.append(
                tokenizer.decode(outputs[0], skip_special_tokens=True)
            )
        except Exception:
            parts.append(s)
    return " ".join(parts)


def make_diff(orig, fixed):
    """HTML للفروقات مع SequenceMatcher للدقة"""
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


def calculate_accuracy(original, corrected):
    """حساب نسبة الدقة التقريبية"""
    orig_words = original.split()
    corr_words = corrected.split()
    if not orig_words:
        return 100.0

    matcher = difflib.SequenceMatcher(None, orig_words, corr_words)
    changes = 0
    for op, i1, i2, j1, j2 in matcher.get_opcodes():
        if op != 'equal':
            changes += max(i2 - i1, j2 - j1)

    total = max(len(orig_words), len(corr_words))
    if total == 0:
        return 100.0

    similarity = matcher.ratio() * 100
    return round(similarity, 1)


# ==========================================
# 6. الواجهة العلوية
# ==========================================
st.markdown("""
<div class="bg-fx">
    <div class="bg-orb o1"></div>
    <div class="bg-orb o2"></div>
    <div class="bg-orb o3"></div>
    <div class="bg-lines"></div>
</div>
<div class="topbar">
    <div class="tb-brand">
        <div class="tb-logo">🤖</div>
        <span class="tb-name">Grammar AI + Translator</span>
    </div>
    <span class="tb-tag">Rule Engine + T5 + Helsinki-NLP</span>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <div class="hero-chip">🧠 Dual-Layer Correction + Translation</div>
    <h1><span class="glow">AI Grammar Corrector</span></h1>
    <p class="hero-desc">
        Rule Engine + T5 AI for higher accuracy correction,
        then translate to 12+ languages — all in one place
    </p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 7. تحميل نموذج التصحيح
# ==========================================
corrector_tok = None
corrector_mdl = None
corrector_ok = False

try:
    with st.spinner("🔄 Loading grammar model on {}...".format(DEVICE.upper())):
        corrector_tok, corrector_mdl = load_corrector()
    corrector_ok = True

    device_label = "GPU 🚀" if DEVICE == "cuda" else "CPU"
    st.markdown(
        '<div class="pill pill-ok">'
        '<div class="pdot"></div>'
        'Grammar Model Ready ({})</div>'.format(device_label),
        unsafe_allow_html=True,
    )
except Exception as e:
    st.markdown(
        '<div class="pill pill-err">'
        '<div class="pdot"></div>'
        'Grammar Model Error</div>',
        unsafe_allow_html=True,
    )
    with st.expander("Details"):
        st.error(str(e))

# ==========================================
# 8. منطقة العمل
# ==========================================
st.markdown('<div class="workzone">', unsafe_allow_html=True)

EXAMPLES = [
    "Last weak, me and my freind goed to the librery.",
    "She dont knows what happend yestarday.",
    "I has been working hear for too yeers now.",
    "Their going to there house over they're.",
    "The childs was playing in the gardenn.",
    "He writed a leter to his teecher.",
    "I could of went to the store but i didnt.",
    "The goverment should of seperated the departments.",
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

st.markdown(
    '<div class="gc"><div class="gc-head">'
    '<div class="gc-title"><div class="gc-ico">✍️</div>'
    'Input Text</div>'
    '<span class="gc-badge">English</span>'
    '</div></div>',
    unsafe_allow_html=True,
)

default = (
    "Last weak, me and my freind goed to the "
    "librery to studdy for our finalle examms."
)

user_text = st.text_area(
    label="t",
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
        "🚀 Correct with AI (Dual-Layer)",
        type="primary",
        use_container_width=True,
        disabled=not corrector_ok,
    )
with b2:
    clr = st.button("🗑️ Clear", use_container_width=True)
with b3:
    cpy1 = st.button("📋 Copy", use_container_width=True, key="cpy1")

if clr:
    st.session_state["inp"] = ""
    st.session_state["corrected"] = ""
    st.session_state["translated"] = ""
    st.rerun()

# نتيجة التصحيح
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
        with st.spinner("🧠 Layer 1: Rule Engine → Layer 2: T5 AI..."):
            t0 = time.time()
            final = correct_text(user_text, corrector_tok, corrector_mdl)
            elapsed = round(time.time() - t0, 2)

        st.session_state["corrected"] = final
        st.session_state["translated"] = ""

        # خريطة التغييرات
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

        st.markdown("<br>", unsafe_allow_html=True)

        corr_holder.markdown(
            '<div class="rbox rbox-clean">{}</div>'.format(final),
            unsafe_allow_html=True,
        )

        st.success("✅ Corrected in {}s!".format(elapsed))

        # إحصائيات
        ow = user_text.split()
        fw = final.split()

        matcher = difflib.SequenceMatcher(None, ow, fw)
        changes = 0
        for op, i1, i2, j1, j2 in matcher.get_opcodes():
            if op != 'equal':
                changes += max(i2 - i1, j2 - j1)

        num_sents = len(smart_sentence_split(user_text))
        accuracy = calculate_accuracy(user_text, final)

        # شريط الدقة
        if changes > 0:
            bar_color = "var(--green)" if accuracy > 80 else "var(--orange)" if accuracy > 60 else "var(--red)"
            st.markdown(
                '<div class="accuracy-meter">'
                '<span style="font-weight:700">📊 Correction Confidence</span>'
                '<div class="meter-bar">'
                '<div class="meter-fill" style="width:{}%;background:{}"></div>'
                '</div>'
                '<span style="font-size:.85rem;color:var(--text-secondary)">'
                '{}% text modified</span>'
                '</div>'.format(
                    min(100, changes * 10),
                    bar_color,
                    round(100 - accuracy, 1),
                ),
                unsafe_allow_html=True,
            )

        st.markdown(
            '<div class="sgrid">'
            '<div class="sc"><div class="sc-val">{}</div>'
            '<div class="sc-lbl">Words</div></div>'
            '<div class="sc"><div class="sc-val" style="color:#ff7675">{}</div>'
            '<div class="sc-lbl">Changes</div></div>'
            '<div class="sc"><div class="sc-val" style="color:#55efc4">{}</div>'
            '<div class="sc-lbl">Sentences</div></div>'
            '<div class="sc"><div class="sc-val" style="color:var(--cyan)">{}s</div>'
            '<div class="sc-lbl">Time</div></div>'
            '</div>'.format(len(ow), changes, num_sents, elapsed),
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
# 9. قسم الترجمة
# ==========================================
st.markdown('<hr class="divider">', unsafe_allow_html=True)

st.markdown(
    '<div class="gc"><div class="gc-head">'
    '<div class="gc-title">'
    '<div class="gc-ico gc-ico-blue">🌍</div>'
    'Translate Corrected Text</div>'
    '<span class="gc-badge">Helsinki-NLP · Manual Mode</span>'
    '</div></div>',
    unsafe_allow_html=True,
)

corrected_text = st.session_state.get("corrected", "")

if not corrected_text:
    st.info("💡 Correct the text first, then choose a language to translate to.")
else:
    preview = corrected_text[:100]
    if len(corrected_text) > 100:
        preview += "..."
    st.markdown("**Text to translate:** " + preview)

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
            "🌍 Translate to " + target_lang,
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
                trans_tok, trans_mdl, used_model, err = load_translator_model(
                    "en", tgt_code
                )

                if trans_tok is None:
                    st.error("❌ " + str(err))
                else:
                    st.markdown(
                        '<div class="pill pill-ok">'
                        '<div class="pdot"></div>'
                        'Model: {}</div>'.format(used_model),
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

                    st.success(
                        "✅ Translated in {}s · Model: {}".format(
                            elapsed, used_model
                        )
                    )

                    src_wc = len(corrected_text.split())
                    tgt_wc = len(translated.split())

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
                            src_wc, tgt_wc,
                            tgt_code.upper(), elapsed
                        ),
                        unsafe_allow_html=True,
                    )

            except Exception as e:
                st.error("❌ Translation error: " + str(e))
                with st.expander("🔍 Full error"):
                    st.code(str(e))

    cpy2 = st.button(
        "📋 Copy Translation",
        use_container_width=True,
        key="cpy2",
    )
    if cpy2:
        tr = st.session_state.get("translated", "")
        if tr:
            st.code(tr, language=None)
            st.info("📋 Select and copy Ctrl+C")
        else:
            st.warning("⚠️ No translation yet")


# ==========================================
# 10. الميزات
# ==========================================
st.markdown("""
<div class="fgrid">
    <div class="fc"><div class="fc-ico">🧠</div>
        <div class="fc-ttl">Dual-Layer Correction</div>
        <div class="fc-dsc">Rule Engine + T5 AI for maximum accuracy</div></div>
    <div class="fc"><div class="fc-ico">🌍</div>
        <div class="fc-ttl">12+ Languages</div>
        <div class="fc-dsc">Translate to Arabic, French, German & more</div></div>
    <div class="fc"><div class="fc-ico">🔍</div>
        <div class="fc-ttl">Smart Diff</div>
        <div class="fc-dsc">SequenceMatcher for accurate change detection</div></div>
    <div class="fc"><div class="fc-ico">⚡</div>
        <div class="fc-ttl">GPU Support</div>
        <div class="fc-dsc">Auto-detects CUDA for 10x speed</div></div>
    <div class="fc"><div class="fc-ico">📊</div>
        <div class="fc-ttl">Statistics</div>
        <div class="fc-dsc">Words, changes, accuracy & timing</div></div>
    <div class="fc"><div class="fc-ico">🆓</div>
        <div class="fc-ttl">Free Forever</div>
        <div class="fc-dsc">No limits, no sign-up needed</div></div>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 11. الفوتر
# ==========================================
st.markdown("""
<div class="appfoot">
    <div class="af-brand">🤖 Grammar AI + 🌍 Translator</div>
    <div class="af-txt">
        Rule Engine + T5 Correction + Helsinki-NLP Translation<br>
        Dual-Layer Architecture · Made with ❤️
    </div>
</div>
""", unsafe_allow_html=True)
