import streamlit as st
import time
import re
import difflib
import subprocess
import sys
import os

# ==========================================
# 1. إعدادات الصفحة
# ==========================================
st.set_page_config(
    page_title="AI Grammar Corrector | Gramformer",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ==========================================
# 2. CSS الكامل
# ==========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@200;300;400;500;700;800;900&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&display=swap');

:root {
    --gold: #e9c46a;
    --gold-light: #f4d58d;
    --orange: #f4a261;
    --cyan: #a8dadc;
    --green: #2ecc71;
    --green-bg: rgba(46, 204, 113, 0.08);
    --red: #e74c3c;
    --red-bg: rgba(231, 76, 60, 0.08);
    --purple: #a855f7;
    --dark-1: #050510;
    --dark-2: #0d0d2b;
    --dark-3: #1a1a3e;
    --dark-4: #252552;
    --text-primary: #f0f0f0;
    --text-secondary: #a0a0b0;
    --glass: rgba(255, 255, 255, 0.03);
    --glass-border: rgba(255, 255, 255, 0.08);
    --glass-hover: rgba(255, 255, 255, 0.06);
}

* {
    font-family: 'Tajawal', 'Inter', sans-serif !important;
    box-sizing: border-box;
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--dark-1) !important;
    color: var(--text-primary) !important;
}

.main .block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

#MainMenu, footer, header,
[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"] {
    display: none !important;
}

/* ═══════ الخلفية ═══════ */
.bg-effects {
    position: fixed;
    inset: 0;
    z-index: 0;
    pointer-events: none;
    overflow: hidden;
}

.bg-orb {
    position: absolute;
    border-radius: 50%;
    filter: blur(100px);
    opacity: 0.12;
    animation: float 25s ease-in-out infinite;
}

.orb-1 {
    width: 500px; height: 500px;
    background: var(--gold);
    top: -200px; right: -100px;
}

.orb-2 {
    width: 400px; height: 400px;
    background: var(--purple);
    bottom: -150px; left: -100px;
    animation-delay: -8s;
}

.orb-3 {
    width: 350px; height: 350px;
    background: var(--cyan);
    top: 40%; left: 30%;
    animation-delay: -16s;
}

.bg-grid {
    position: absolute;
    inset: 0;
    background-image:
        linear-gradient(rgba(233,196,106,0.02) 1px, transparent 1px),
        linear-gradient(90deg, rgba(233,196,106,0.02) 1px, transparent 1px);
    background-size: 80px 80px;
}

@keyframes float {
    0%, 100% { transform: translate(0, 0) scale(1); }
    33% { transform: translate(50px, -60px) scale(1.08); }
    66% { transform: translate(-40px, 50px) scale(0.92); }
}

/* ═══════ الشريط العلوي ═══════ */
.topbar {
    position: relative;
    z-index: 10;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1rem 3rem;
    background: rgba(13, 13, 43, 0.75);
    backdrop-filter: blur(25px);
    border-bottom: 1px solid var(--glass-border);
}

.topbar-brand {
    display: flex;
    align-items: center;
    gap: 0.7rem;
}

.topbar-logo {
    width: 38px; height: 38px;
    background: linear-gradient(135deg, var(--gold), var(--orange));
    border-radius: 11px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.2rem;
    box-shadow: 0 4px 12px rgba(233, 196, 106, 0.25);
}

.topbar-name {
    font-size: 1.15rem;
    font-weight: 800;
    color: var(--gold);
    letter-spacing: -0.3px;
}

.topbar-tag {
    background: rgba(168, 85, 247, 0.15);
    border: 1px solid rgba(168, 85, 247, 0.3);
    color: var(--purple);
    padding: 0.3rem 0.9rem;
    border-radius: 50px;
    font-size: 0.78rem;
    font-weight: 700;
}

/* ═══════ Hero ═══════ */
.hero {
    position: relative;
    z-index: 1;
    text-align: center;
    padding: 3.5rem 2rem 2.5rem;
}

.hero-chip {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: rgba(233, 196, 106, 0.08);
    border: 1px solid rgba(233, 196, 106, 0.18);
    padding: 0.4rem 1.2rem;
    border-radius: 50px;
    font-size: 0.82rem;
    color: var(--gold);
    margin-bottom: 1.5rem;
    animation: fadeDown 0.6s ease;
}

.hero h1 {
    font-size: 3.2rem;
    font-weight: 900;
    line-height: 1.15;
    margin-bottom: 1rem;
    animation: fadeUp 0.7s ease;
}

.hero h1 .glow {
    background: linear-gradient(135deg, var(--gold), var(--orange), var(--gold-light));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.hero-desc {
    font-size: 1.15rem;
    color: var(--text-secondary);
    max-width: 650px;
    margin: 0 auto 2rem;
    line-height: 1.9;
    font-weight: 300;
    animation: fadeUp 0.7s ease 0.15s both;
}

.hero-metrics {
    display: flex;
    justify-content: center;
    gap: 3.5rem;
    animation: fadeUp 0.7s ease 0.3s both;
}

.hero-metric-val {
    font-size: 1.7rem;
    font-weight: 900;
    color: var(--gold);
}

.hero-metric-lbl {
    font-size: 0.82rem;
    color: var(--text-secondary);
    margin-top: 0.15rem;
}

@keyframes fadeUp {
    from { opacity: 0; transform: translateY(18px); }
    to   { opacity: 1; transform: translateY(0); }
}

@keyframes fadeDown {
    from { opacity: 0; transform: translateY(-15px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* ═══════ حاوية العمل ═══════ */
.work-area {
    position: relative;
    z-index: 1;
    max-width: 1000px;
    margin: 0 auto;
    padding: 0 2rem 3rem;
}

/* ═══════ بطاقة زجاجية ═══════ */
.gcard {
    background: var(--glass);
    backdrop-filter: blur(20px);
    border: 1px solid var(--glass-border);
    border-radius: 22px;
    padding: 1.8rem;
    margin-bottom: 1.3rem;
    transition: border-color 0.3s;
}

.gcard:hover {
    border-color: rgba(233, 196, 106, 0.12);
}

.gcard-head {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1rem;
}

.gcard-title {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    font-size: 1.05rem;
    font-weight: 700;
    color: var(--text-primary);
}

.gcard-icon {
    width: 30px; height: 30px;
    background: linear-gradient(135deg, var(--gold), var(--orange));
    border-radius: 9px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.85rem;
}

.gcard-badge {
    font-size: 0.78rem;
    color: var(--text-secondary);
    background: rgba(255,255,255,0.04);
    padding: 0.25rem 0.7rem;
    border-radius: 20px;
    border: 1px solid var(--glass-border);
}

/* ═══════ TextArea ═══════ */
.stTextArea textarea {
    font-family: 'JetBrains Mono', 'Inter', monospace !important;
    font-size: 1.1rem !important;
    line-height: 1.9 !important;
    direction: ltr !important;
    text-align: left !important;
    background: rgba(0, 0, 0, 0.35) !important;
    border: 2px solid var(--glass-border) !important;
    border-radius: 14px !important;
    padding: 1.3rem !important;
    color: var(--text-primary) !important;
    transition: border-color 0.3s, box-shadow 0.3s !important;
}

.stTextArea textarea:focus {
    border-color: var(--gold) !important;
    box-shadow: 0 0 0 3px rgba(233, 196, 106, 0.1) !important;
}

.stTextArea textarea::placeholder {
    color: rgba(255, 255, 255, 0.18) !important;
    font-family: 'Tajawal' !important;
}

/* ═══════ النتيجة ═══════ */
.result-box {
    background: linear-gradient(135deg,
        rgba(233, 196, 106, 0.04),
        rgba(168, 218, 220, 0.03));
    border: 2px solid rgba(233, 196, 106, 0.15);
    border-radius: 14px;
    padding: 1.5rem;
    direction: ltr;
    text-align: left;
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.1rem;
    line-height: 2.2;
    color: var(--text-primary);
    min-height: 120px;
    position: relative;
    overflow: hidden;
    word-wrap: break-word;
}

.result-box::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    border-radius: 14px 14px 0 0;
}

.result-diff::before {
    background: linear-gradient(90deg, var(--red), var(--orange), var(--green));
}

.result-clean::before {
    background: linear-gradient(90deg, var(--green), var(--cyan));
}

.result-clean {
    color: var(--green);
    font-weight: 500;
}

.result-empty {
    color: rgba(255, 255, 255, 0.15);
    font-family: 'Tajawal' !important;
    font-size: 0.95rem;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.6rem;
    min-height: 120px;
}

/* ═══════ Diff marks ═══════ */
mark.err {
    background: rgba(231, 76, 60, 0.2);
    color: #ff7675;
    border-radius: 4px;
    padding: 1px 5px;
    font-weight: 600;
    text-decoration: line-through;
    text-decoration-color: rgba(231, 76, 60, 0.5);
}

mark.fix {
    background: rgba(46, 204, 113, 0.15);
    color: #55efc4;
    font-weight: 700;
    padding: 1px 5px;
    border-radius: 4px;
    border-bottom: 2px solid rgba(46, 204, 113, 0.5);
}

/* ═══════ الأزرار ═══════ */
.stButton > button {
    font-family: 'Tajawal' !important;
    font-weight: 700 !important;
    border-radius: 12px !important;
    padding: 0.75rem 1.2rem !important;
    font-size: 1.05rem !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    border: none !important;
}

.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, var(--gold), var(--orange)) !important;
    color: var(--dark-1) !important;
    box-shadow: 0 4px 18px rgba(233, 196, 106, 0.25) !important;
}

.stButton > button[kind="primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(233, 196, 106, 0.35) !important;
}

.stButton > button[kind="secondary"] {
    background: var(--glass) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--glass-border) !important;
}

.stButton > button[kind="secondary"]:hover {
    border-color: rgba(233,196,106,0.25) !important;
}

/* ═══════ الإحصائيات ═══════ */
.stats-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0.8rem;
    margin-top: 1.2rem;
}

.scard {
    background: linear-gradient(135deg, rgba(26,26,62,0.8), rgba(13,13,43,0.9));
    border: 1px solid var(--glass-border);
    border-radius: 16px;
    padding: 1.2rem;
    text-align: center;
    transition: all 0.3s;
    position: relative;
    overflow: hidden;
}

.scard::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    opacity: 0;
    transition: opacity 0.3s;
}

.scard:hover {
    transform: translateY(-4px);
    border-color: rgba(233,196,106,0.25);
}

.scard:hover::after { opacity: 1; }

.scard:nth-child(1)::after { background: var(--gold); }
.scard:nth-child(2)::after { background: var(--red); }
.scard:nth-child(3)::after { background: var(--green); }
.scard:nth-child(4)::after { background: var(--cyan); }

.scard-icon { font-size: 1.3rem; margin-bottom: 0.4rem; }
.scard-val { font-size: 1.8rem; font-weight: 900; color: var(--gold); }
.scard-lbl { font-size: 0.8rem; color: var(--text-secondary); margin-top: 0.2rem; }

/* ═══════ النماذج ═══════ */
.examples-wrap {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin: 0.8rem 0;
}

/* ═══════ حالة النموذج ═══════ */
.model-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.45rem;
    padding: 0.4rem 1rem;
    border-radius: 50px;
    font-size: 0.85rem;
    font-weight: 600;
}

.pill-ok {
    background: rgba(46,204,113,0.1);
    border: 1px solid rgba(46,204,113,0.25);
    color: #2ecc71;
}

.pill-err {
    background: rgba(231,76,60,0.1);
    border: 1px solid rgba(231,76,60,0.25);
    color: #e74c3c;
}

.pill-dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    animation: blink 2s infinite;
}

.pill-ok .pill-dot { background: #2ecc71; }
.pill-err .pill-dot { background: #e74c3c; }

@keyframes blink {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
}

/* ═══════ الميزات ═══════ */
.feat-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    margin: 2.5rem 0;
}

.feat {
    background: var(--glass);
    border: 1px solid var(--glass-border);
    border-radius: 18px;
    padding: 1.5rem;
    text-align: center;
    transition: all 0.3s;
}

.feat:hover {
    border-color: rgba(233,196,106,0.18);
    transform: translateY(-3px);
}

.feat-ico { font-size: 1.8rem; margin-bottom: 0.7rem; }
.feat-ttl { font-weight: 700; color: var(--text-primary); margin-bottom: 0.3rem; }
.feat-dsc { font-size: 0.82rem; color: var(--text-secondary); line-height: 1.7; }

/* ═══════ الفوتر ═══════ */
.app-foot {
    position: relative;
    z-index: 1;
    text-align: center;
    padding: 2.5rem 2rem;
    border-top: 1px solid var(--glass-border);
    margin-top: 2rem;
}

.foot-brand { font-size: 1.1rem; font-weight: 800; color: var(--gold); }
.foot-txt { color: var(--text-secondary); font-size: 0.82rem; margin-top: 0.3rem; line-height: 1.7; }

/* ═══════ تجاوب ═══════ */
@media (max-width: 768px) {
    .topbar { padding: 0.7rem 1rem; }
    .hero h1 { font-size: 2rem; }
    .hero-metrics { gap: 1.5rem; }
    .stats-grid { grid-template-columns: repeat(2, 1fr); }
    .feat-grid { grid-template-columns: 1fr; }
    .work-area { padding: 0 1rem 2rem; }
}
</style>
""", unsafe_allow_html=True)


# ==========================================
# 3. تثبيت spaCy model بشكل صحيح
# ==========================================

def ensure_spacy_model():
    """تأكد من وجود نموذج spaCy"""
    try:
        import spacy
        spacy.load("en_core_web_sm")
        return True
    except (OSError, ImportError):
        pass

    # محاولة التثبيت
    try:
        result = subprocess.run(
            [sys.executable, "-m", "spacy", "download", "en_core_web_sm"],
            capture_output=True,
            text=True,
            timeout=120,
        )
        if result.returncode == 0:
            return True
    except Exception:
        pass

    # محاولة بديلة عبر pip
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install",
             "https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.1/en_core_web_sm-3.7.1-py3-none-any.whl"],
            capture_output=True,
            text=True,
            timeout=120,
        )
        if result.returncode == 0:
            return True
    except Exception:
        pass

    # محاولة ثالثة
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "en-core-web-sm",
             "--extra-index-url", "https://github.com/explosion/spacy-models/releases/expanded_assets/en_core_web_sm-3.7.1"],
            capture_output=True,
            text=True,
            timeout=120,
        )
        return result.returncode == 0
    except Exception:
        return False


# ==========================================
# 4. تحميل Gramformer
# ==========================================

@st.cache_resource
def load_gramformer():
    """تحميل النموذج مع كل المحاولات"""
    # الخطوة 1: تأكد من spaCy
    spacy_ok = ensure_spacy_model()

    if not spacy_ok:
        # محاولة أخيرة مباشرة
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install",
                 "spacy", "en-core-web-sm"],
                capture_output=True,
                timeout=120,
            )
        except Exception:
            pass

    # الخطوة 2: تحميل spaCy
    try:
        import spacy
        nlp = spacy.load("en_core_web_sm")
    except Exception as e:
        raise RuntimeError(
            f"فشل تحميل spaCy model.\n"
            f"الخطأ: {e}\n\n"
            f"الحل: أضف هذا السطر في setup.sh:\n"
            f"python -m spacy download en_core_web_sm"
        )

    # الخطوة 3: تحميل Gramformer
    import torch

    torch.manual_seed(1212)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(1212)

    from gramformer import Gramformer

    gf = Gramformer(models=1, use_gpu=False)
    return gf


# ==========================================
# 5. الخلفية + الشريط العلوي
# ==========================================

st.markdown("""
<div class="bg-effects">
    <div class="bg-orb orb-1"></div>
    <div class="bg-orb orb-2"></div>
    <div class="bg-orb orb-3"></div>
    <div class="bg-grid"></div>
</div>

<div class="topbar">
    <div class="topbar-brand">
        <div class="topbar-logo">🤖</div>
        <span class="topbar-name">Gramformer AI</span>
    </div>
    <span class="topbar-tag">Deep Learning</span>
</div>
""", unsafe_allow_html=True)


# ==========================================
# 6. Hero Section
# ==========================================

st.markdown("""
<div class="hero">
    <div class="hero-chip">🧠 Powered by Transformer Models</div>
    <h1><span class="glow">AI Grammar Corrector</span></h1>
    <p class="hero-desc">
        Advanced deep learning model that understands context
        and fixes complex spelling &amp; grammar errors in English text
    </p>
    <div class="hero-metrics">
        <div>
            <div class="hero-metric-val">T5-Based</div>
            <div class="hero-metric-lbl">Model Architecture</div>
        </div>
        <div>
            <div class="hero-metric-val">&lt;3s</div>
            <div class="hero-metric-lbl">Processing Time</div>
        </div>
        <div>
            <div class="hero-metric-val">Free</div>
            <div class="hero-metric-lbl">Unlimited Use</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ==========================================
# 7. تحميل النموذج
# ==========================================

gf = None
model_loaded = False

try:
    with st.spinner("🔄 Loading AI model (first time may take a minute)..."):
        gf = load_gramformer()
    model_loaded = True
except Exception as e:
    model_error = str(e)


# ==========================================
# 8. منطقة العمل
# ==========================================

st.markdown('<div class="work-area">', unsafe_allow_html=True)

# حالة النموذج
if model_loaded:
    st.markdown(
        '<div class="model-pill pill-ok">'
        '<div class="pill-dot"></div>'
        'Model Ready ✓'
        '</div>',
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        '<div class="model-pill pill-err">'
        '<div class="pill-dot"></div>'
        'Model Error'
        '</div>',
        unsafe_allow_html=True,
    )
    with st.expander("🔍 Error Details"):
        st.error(model_error)
        st.markdown(
            "**Fix for Streamlit Cloud:**\n\n"
            "Create a file `setup.sh` with:\n"
            "```bash\n"
            "python -m spacy download en_core_web_sm\n"
            "```\n\n"
            "Or add to `packages.txt`:\n"
            "```\n"
            "build-essential\n"
            "```\n\n"
            "**Fix locally:**\n"
            "```bash\n"
            "python -m spacy download en_core_web_sm\n"
            "pip install gramformer\n"
            "```"
        )


# ==========================================
# 9. نماذج جاهزة
# ==========================================

EXAMPLES = [
    "Last weak, me and my freind goed to the librery.",
    "She dont knows what happend yestarday.",
    "I has been working hear for too yeers now.",
    "Their going to there house over they're.",
    "The childs was playing in the gardenn.",
    "He writed a leter to his teecher.",
]

st.markdown("""
<div class="gcard">
    <div class="gcard-head">
        <div class="gcard-title">
            <div class="gcard-icon">💡</div>
            Try an Example
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

ex_cols = st.columns(3)
for i, ex in enumerate(EXAMPLES):
    with ex_cols[i % 3]:
        short = ex[:35] + "..." if len(ex) > 35 else ex
        if st.button(short, key=f"ex_{i}", use_container_width=True):
            st.session_state["user_input"] = ex


# ==========================================
# 10. الإدخال
# ==========================================

st.markdown("""
<div class="gcard">
    <div class="gcard-head">
        <div class="gcard-title">
            <div class="gcard-icon">✍️</div>
            Input Text
        </div>
        <span class="gcard-badge">English</span>
    </div>
</div>
""", unsafe_allow_html=True)

default_text = "Last weak, me and my freind goed to the librery to studdy for our finalle examms."

user_text = st.text_area(
    label="text",
    value=st.session_state.get("user_input", default_text),
    height=150,
    placeholder="Type or paste English text with errors...",
    label_visibility="collapsed",
    key="input_box",
)

# عدّاد
wc = len(user_text.split()) if user_text.strip() else 0
st.caption(f"📏 {wc} words · {len(user_text)} characters")

# أزرار
b1, b2, b3 = st.columns([3, 1, 1])

with b1:
    run_btn = st.button(
        "🚀 Correct with AI",
        type="primary",
        use_container_width=True,
        disabled=not model_loaded,
    )

with b2:
    clr_btn = st.button("🗑️ Clear", use_container_width=True)

with b3:
    cpy_btn = st.button("📋 Copy", use_container_width=True)

if clr_btn:
    st.session_state["user_input"] = ""
    st.session_state["last_corrected"] = ""
    st.rerun()


# ==========================================
# 11. دالة المقارنة
# ==========================================

def make_diff_html(original, corrected):
    """إنتاج HTML يُظهر الفروقات"""
    diff = difflib.ndiff(original.split(), corrected.split())
    parts = []
    for tok in diff:
        if tok.startswith("- "):
            parts.append(f'<mark class="err">{tok[2:]}</mark>')
        elif tok.startswith("+ "):
            parts.append(f'<mark class="fix">{tok[2:]}</mark>')
        elif tok.startswith("  "):
            parts.append(tok[2:])
    return " ".join(parts)


# ==========================================
# 12. المعالجة والنتائج
# ==========================================

# حاوية النتيجة
st.markdown("""
<div class="gcard">
    <div class="gcard-head">
        <div class="gcard-title">
            <div class="gcard-icon">✨</div>
            Results
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

result_area = st.empty()

# عرض نتيجة سابقة أو حالة فارغة
if "last_corrected" in st.session_state and st.session_state["last_corrected"]:
    result_area.markdown(
        f'<div class="result-box result-clean">'
        f'{st.session_state["last_corrected"]}</div>',
        unsafe_allow_html=True,
    )
else:
    result_area.markdown(
        '<div class="result-box result-empty">'
        '✍️ Results will appear here after correction'
        '</div>',
        unsafe_allow_html=True,
    )


if run_btn:
    if not user_text.strip():
        st.warning("⚠️ Please enter some text first!")

    elif not model_loaded:
        st.error("❌ Model not available")

    else:
        with st.spinner("🧠 Analyzing and correcting..."):
            t0 = time.time()

            # تقسيم إلى جمل
            sentences = re.split(r'(?<=[.!?])\s+', user_text.strip())
            corrected_parts = []

            for sent in sentences:
                if sent.strip():
                    try:
                        res = gf.correct(sent, max_candidates=1)
                        corrected_parts.append(list(res)[0] if res else sent)
                    except Exception:
                        corrected_parts.append(sent)

            final = " ".join(corrected_parts)
            elapsed = round(time.time() - t0, 2)

        st.session_state["last_corrected"] = final

        # عرض خريطة التعديلات
        diff_html = make_diff_html(user_text, final)

        st.markdown(
            '<div class="gcard-title" style="margin-top:1rem;">'
            '<div class="gcard-icon">🔍</div>'
            'Change Map'
            '</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="result-box result-diff">{diff_html}</div>',
            unsafe_allow_html=True,
        )

        st.markdown("<br>", unsafe_allow_html=True)

        # النص النهائي
        st.markdown(
            '<div class="gcard-title">'
            '<div class="gcard-icon">✅</div>'
            'Corrected Text'
            '</div>',
            unsafe_allow_html=True,
        )
        result_area.markdown(
            f'<div class="result-box result-clean">{final}</div>',
            unsafe_allow_html=True,
        )

        st.success(f"✅ Done in {elapsed}s!")

        # حساب التغييرات
        orig_words = user_text.split()
        fix_words = final.split()
        changes = sum(
            1 for a, b in zip(orig_words, fix_words) if a != b
        ) + abs(len(orig_words) - len(fix_words))

        st.markdown(f"""
        <div class="stats-grid">
            <div class="scard">
                <div class="scard-icon">📝</div>
                <div class="scard-val">{len(orig_words)}</div>
                <div class="scard-lbl">Words</div>
            </div>
            <div class="scard">
                <div class="scard-val" style="color:#ff7675">{changes}</div>
                <div class="scard-lbl">Changes</div>
            </div>
            <div class="scard">
                <div class="scard-val" style="color:#55efc4">{len(sentences)}</div>
                <div class="scard-lbl">Sentences</div>
            </div>
            <div class="scard">
                <div class="scard-val" style="color:var(--cyan)">{elapsed}s</div>
                <div class="scard-lbl">Time</div>
            </div>
        </div>
        """, unsafe_allow_html=True)


# نسخ
if cpy_btn:
    lr = st.session_state.get("last_corrected", "")
    if lr:
        st.code(lr, language=None)
        st.info("📋 Select and copy (Ctrl+C)")
    else:
        st.warning("⚠️ No result to copy")


# ==========================================
# 13. الميزات
# ==========================================

st.markdown("""
<div class="feat-grid">
    <div class="feat">
        <div class="feat-ico">🧠</div>
        <div class="feat-ttl">Deep Context</div>
        <div class="feat-dsc">T5 transformer understands context beyond simple spell-check</div>
    </div>
    <div class="feat">
        <div class="feat-ico">🔍</div>
        <div class="feat-ttl">Visual Diff</div>
        <div class="feat-dsc">See exactly what changed with color-coded highlights</div>
    </div>
    <div class="feat">
        <div class="feat-ico">⚡</div>
        <div class="feat-ttl">Fast Processing</div>
        <div class="feat-dsc">Sentence-by-sentence analysis for speed and accuracy</div>
    </div>
    <div class="feat">
        <div class="feat-ico">📊</div>
        <div class="feat-ttl">Statistics</div>
        <div class="feat-dsc">Detailed stats on words, changes, and processing time</div>
    </div>
    <div class="feat">
        <div class="feat-ico">🎯</div>
        <div class="feat-ttl">Grammar + Spelling</div>
        <div class="feat-dsc">Fixes both grammatical errors and spelling mistakes</div>
    </div>
    <div class="feat">
        <div class="feat-ico">🆓</div>
        <div class="feat-ttl">100% Free</div>
        <div class="feat-dsc">No limits, no sign-up, no tracking</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)


# ==========================================
# 14. الفوتر
# ==========================================

st.markdown("""
<div class="app-foot">
    <div class="foot-brand">🤖 Gramformer AI — Grammar Corrector</div>
    <div class="foot-txt">
        Built with Gramformer + Hugging Face Transformers<br>
        Made with ❤️ for better writing
    </div>
</div>
""", unsafe_allow_html=True)
