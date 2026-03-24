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
    page_title="AI Grammar Corrector",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ==========================================
# 2. CSS
# ==========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700;800;900&display=swap');
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&display=swap');

:root {
    --gold: #e9c46a; --gold-light: #f4d58d; --orange: #f4a261;
    --cyan: #a8dadc; --green: #2ecc71; --red: #e74c3c;
    --purple: #a855f7; --dark-1: #050510; --dark-2: #0d0d2b;
    --text-primary: #f0f0f0; --text-secondary: #a0a0b0;
    --glass: rgba(255,255,255,0.03);
    --glass-border: rgba(255,255,255,0.08);
}

* { font-family: 'Tajawal', sans-serif !important; }

html, body, [data-testid="stAppViewContainer"] {
    background: var(--dark-1) !important;
    color: var(--text-primary) !important;
}
.main .block-container { padding: 0 !important; max-width: 100% !important; }

#MainMenu, footer, header,
[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"] { display: none !important; }

.bg-fx { position:fixed; inset:0; z-index:0; pointer-events:none; overflow:hidden; }
.bg-orb { position:absolute; border-radius:50%; filter:blur(100px); opacity:0.12; animation:drift 25s ease-in-out infinite; }
.o1 { width:500px; height:500px; background:var(--gold); top:-200px; right:-100px; }
.o2 { width:400px; height:400px; background:var(--purple); bottom:-150px; left:-100px; animation-delay:-8s; }
.o3 { width:350px; height:350px; background:var(--cyan); top:40%; left:30%; animation-delay:-16s; }
.bg-lines { position:absolute; inset:0; background-image:linear-gradient(rgba(233,196,106,0.02) 1px,transparent 1px),linear-gradient(90deg,rgba(233,196,106,0.02) 1px,transparent 1px); background-size:80px 80px; }
@keyframes drift { 0%,100%{transform:translate(0,0) scale(1)} 33%{transform:translate(50px,-60px) scale(1.08)} 66%{transform:translate(-40px,50px) scale(0.92)} }

.topbar { position:relative; z-index:10; display:flex; align-items:center; justify-content:space-between; padding:1rem 3rem; background:rgba(13,13,43,0.75); backdrop-filter:blur(25px); border-bottom:1px solid var(--glass-border); }
.tb-brand { display:flex; align-items:center; gap:0.7rem; }
.tb-logo { width:38px; height:38px; background:linear-gradient(135deg,var(--gold),var(--orange)); border-radius:11px; display:flex; align-items:center; justify-content:center; font-size:1.2rem; box-shadow:0 4px 12px rgba(233,196,106,0.25); }
.tb-name { font-size:1.15rem; font-weight:800; color:var(--gold); }
.tb-tag { background:rgba(168,85,247,0.15); border:1px solid rgba(168,85,247,0.3); color:var(--purple); padding:0.3rem 0.9rem; border-radius:50px; font-size:0.78rem; font-weight:700; }

.hero { position:relative; z-index:1; text-align:center; padding:3.5rem 2rem 2.5rem; }
.hero-chip { display:inline-flex; align-items:center; gap:0.5rem; background:rgba(233,196,106,0.08); border:1px solid rgba(233,196,106,0.18); padding:0.4rem 1.2rem; border-radius:50px; font-size:0.82rem; color:var(--gold); margin-bottom:1.5rem; }
.hero h1 { font-size:3.2rem; font-weight:900; line-height:1.15; margin-bottom:1rem; }
.hero h1 .glow { background:linear-gradient(135deg,var(--gold),var(--orange),var(--gold-light)); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; }
.hero-desc { font-size:1.15rem; color:var(--text-secondary); max-width:650px; margin:0 auto 2rem; line-height:1.9; font-weight:300; }
.hero-row { display:flex; justify-content:center; gap:3.5rem; }
.hr-val { font-size:1.7rem; font-weight:900; color:var(--gold); }
.hr-lbl { font-size:0.82rem; color:var(--text-secondary); }

.workzone { position:relative; z-index:1; max-width:1000px; margin:0 auto; padding:0 2rem 3rem; }

.gc { background:var(--glass); backdrop-filter:blur(20px); border:1px solid var(--glass-border); border-radius:22px; padding:1.8rem; margin-bottom:1.3rem; }
.gc:hover { border-color:rgba(233,196,106,0.12); }
.gc-head { display:flex; align-items:center; justify-content:space-between; margin-bottom:1rem; }
.gc-title { display:flex; align-items:center; gap:0.6rem; font-size:1.05rem; font-weight:700; }
.gc-ico { width:30px; height:30px; background:linear-gradient(135deg,var(--gold),var(--orange)); border-radius:9px; display:flex; align-items:center; justify-content:center; font-size:0.85rem; }
.gc-badge { font-size:0.78rem; color:var(--text-secondary); background:rgba(255,255,255,0.04); padding:0.25rem 0.7rem; border-radius:20px; border:1px solid var(--glass-border); }

.stTextArea textarea { font-family:'JetBrains Mono',monospace !important; font-size:1.1rem !important; line-height:1.9 !important; direction:ltr !important; text-align:left !important; background:rgba(0,0,0,0.35) !important; border:2px solid var(--glass-border) !important; border-radius:14px !important; padding:1.3rem !important; color:var(--text-primary) !important; }
.stTextArea textarea:focus { border-color:var(--gold) !important; box-shadow:0 0 0 3px rgba(233,196,106,0.1) !important; }
.stTextArea textarea::placeholder { color:rgba(255,255,255,0.18) !important; }

.rbox { border:2px solid rgba(233,196,106,0.15); border-radius:14px; padding:1.5rem; direction:ltr; text-align:left; font-family:'JetBrains Mono',monospace; font-size:1.1rem; line-height:2.2; color:var(--text-primary); min-height:120px; position:relative; overflow:hidden; word-wrap:break-word; background:linear-gradient(135deg,rgba(233,196,106,0.04),rgba(168,218,220,0.03)); }
.rbox::before { content:''; position:absolute; top:0; left:0; right:0; height:3px; border-radius:14px 14px 0 0; }
.rbox-diff::before { background:linear-gradient(90deg,var(--red),var(--orange),var(--green)); }
.rbox-clean::before { background:linear-gradient(90deg,var(--green),var(--cyan)); }
.rbox-clean { color:var(--green); font-weight:500; }
.rbox-empty { color:rgba(255,255,255,0.15); font-family:'Tajawal' !important; font-size:0.95rem; display:flex; align-items:center; justify-content:center; }

mark.err { background:rgba(231,76,60,0.2); color:#ff7675; border-radius:4px; padding:1px 5px; font-weight:600; text-decoration:line-through; }
mark.fix { background:rgba(46,204,113,0.15); color:#55efc4; font-weight:700; padding:1px 5px; border-radius:4px; border-bottom:2px solid rgba(46,204,113,0.5); }

.stButton > button { border-radius:12px !important; padding:0.75rem !important; font-weight:700 !important; font-size:1.05rem !important; border:none !important; }
.stButton > button[kind="primary"] { background:linear-gradient(135deg,var(--gold),var(--orange)) !important; color:var(--dark-1) !important; box-shadow:0 4px 18px rgba(233,196,106,0.25) !important; }
.stButton > button[kind="primary"]:hover { transform:translateY(-2px) !important; box-shadow:0 8px 28px rgba(233,196,106,0.35) !important; }
.stButton > button[kind="secondary"] { background:var(--glass) !important; color:var(--text-primary) !important; border:1px solid var(--glass-border) !important; }

.sgrid { display:grid; grid-template-columns:repeat(4,1fr); gap:0.8rem; margin-top:1.2rem; }
.sc { background:linear-gradient(135deg,rgba(26,26,62,0.8),rgba(13,13,43,0.9)); border:1px solid var(--glass-border); border-radius:16px; padding:1.2rem; text-align:center; transition:all 0.3s; }
.sc:hover { transform:translateY(-4px); border-color:rgba(233,196,106,0.25); }
.sc-val { font-size:1.8rem; font-weight:900; color:var(--gold); }
.sc-lbl { font-size:0.8rem; color:var(--text-secondary); margin-top:0.2rem; }

.pill { display:inline-flex; align-items:center; gap:0.45rem; padding:0.4rem 1rem; border-radius:50px; font-size:0.85rem; font-weight:600; }
.pill-ok { background:rgba(46,204,113,0.1); border:1px solid rgba(46,204,113,0.25); color:#2ecc71; }
.pill-err { background:rgba(231,76,60,0.1); border:1px solid rgba(231,76,60,0.25); color:#e74c3c; }
.pill-load { background:rgba(233,196,106,0.1); border:1px solid rgba(233,196,106,0.25); color:var(--gold); }
.pdot { width:7px; height:7px; border-radius:50%; animation:blink 2s infinite; }
.pill-ok .pdot { background:#2ecc71; } .pill-err .pdot { background:#e74c3c; } .pill-load .pdot { background:var(--gold); }
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.3} }

.fgrid { display:grid; grid-template-columns:repeat(3,1fr); gap:1rem; margin:2.5rem 0; }
.fc { background:var(--glass); border:1px solid var(--glass-border); border-radius:18px; padding:1.5rem; text-align:center; transition:all 0.3s; }
.fc:hover { border-color:rgba(233,196,106,0.18); transform:translateY(-3px); }
.fc-ico { font-size:1.8rem; margin-bottom:0.7rem; }
.fc-ttl { font-weight:700; margin-bottom:0.3rem; }
.fc-dsc { font-size:0.82rem; color:var(--text-secondary); line-height:1.7; }

.appfoot { position:relative; z-index:1; text-align:center; padding:2.5rem 2rem; border-top:1px solid var(--glass-border); margin-top:2rem; }
.af-brand { font-size:1.1rem; font-weight:800; color:var(--gold); }
.af-txt { color:var(--text-secondary); font-size:0.82rem; margin-top:0.3rem; }

@media (max-width:768px) {
    .topbar{padding:0.7rem 1rem} .hero h1{font-size:2rem}
    .sgrid{grid-template-columns:repeat(2,1fr)} .fgrid{grid-template-columns:1fr}
    .workzone{padding:0 1rem 2rem}
}
</style>
""", unsafe_allow_html=True)


# ==========================================
# 3. تثبيت المتطلبات الناقصة
# ==========================================

def run_cmd(args, timeout=300):
    """تشغيل أمر بشكل آمن"""
    try:
        r = subprocess.run(
            args,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return r.returncode == 0, r.stderr
    except Exception as e:
        return False, str(e)


def install_spacy_model():
    """تثبيت نموذج spaCy بعدة طرق"""
    # فحص أولاً
    try:
        import spacy
        spacy.load("en_core_web_sm")
        return True
    except Exception:
        pass

    # طريقة 1: spacy download
    ok, _ = run_cmd([
        sys.executable, "-m", "spacy",
        "download", "en_core_web_sm"
    ])
    if ok:
        return True

    # طريقة 2: pip مباشر
    urls = [
        "https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl",
        "https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.1/en_core_web_sm-3.7.1-py3-none-any.whl",
        "https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.0/en_core_web_sm-3.7.0-py3-none-any.whl",
    ]

    for url in urls:
        ok, _ = run_cmd([
            sys.executable, "-m", "pip", "install",
            url, "--quiet", "--no-deps"
        ])
        if ok:
            return True

    return False


def install_gramformer():
    """تثبيت gramformer"""
    try:
        from gramformer import Gramformer
        return True
    except ImportError:
        pass

    ok, err = run_cmd([
        sys.executable, "-m", "pip", "install",
        "git+https://github.com/PrithivirajDamodaran/Gramformer.git",
        "--quiet", "--no-cache-dir"
    ])

    if not ok:
        # محاولة بديلة بدون git
        ok2, _ = run_cmd([
            sys.executable, "-m", "pip", "install",
            "gramformer", "--quiet", "--no-cache-dir"
        ])
        return ok2

    return ok


def install_errant():
    """تثبيت errant"""
    try:
        import errant
        return True
    except ImportError:
        pass

    ok, _ = run_cmd([
        sys.executable, "-m", "pip", "install",
        "errant", "--quiet", "--no-cache-dir"
    ])
    return ok


# ==========================================
# 4. تحميل النموذج
# ==========================================

@st.cache_resource
def load_grammar_model():
    """تثبيت كل المتطلبات الناقصة ثم تحميل النموذج"""
    steps = []

    # errant
    if install_errant():
        steps.append("✅ errant")
    else:
        steps.append("⚠️ errant (optional)")

    # spaCy model
    if install_spacy_model():
        steps.append("✅ spaCy en_core_web_sm")
    else:
        steps.append("❌ spaCy model failed")
        return None, steps

    # gramformer
    if install_gramformer():
        steps.append("✅ gramformer")
    else:
        steps.append("❌ gramformer failed")
        return None, steps

    # تحميل النموذج
    try:
        import torch
        torch.manual_seed(1212)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(1212)

        from gramformer import Gramformer
        gf = Gramformer(models=1, use_gpu=False)
        steps.append("✅ Model loaded")
        return gf, steps

    except Exception as e:
        steps.append(f"❌ Load error: {e}")
        return None, steps


# ==========================================
# 5. الواجهة
# ==========================================

# الخلفية
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
        <span class="tb-name">Gramformer AI</span>
    </div>
    <span class="tb-tag">Deep Learning</span>
</div>
""", unsafe_allow_html=True)

# Hero
st.markdown("""
<div class="hero">
    <div class="hero-chip">🧠 Powered by Transformer Models</div>
    <h1><span class="glow">AI Grammar Corrector</span></h1>
    <p class="hero-desc">
        Fix complex spelling &amp; grammar errors with deep learning
    </p>
    <div class="hero-row">
        <div><div class="hr-val">T5</div><div class="hr-lbl">Architecture</div></div>
        <div><div class="hr-val">&lt;3s</div><div class="hr-lbl">Speed</div></div>
        <div><div class="hr-val">Free</div><div class="hr-lbl">No Limits</div></div>
    </div>
</div>
""", unsafe_allow_html=True)


# تحميل النموذج
gf = None
model_ok = False

try:
    with st.spinner("🔄 Setting up AI model (first time takes ~2 min)..."):
        gf, setup_steps = load_grammar_model()

    if gf is not None:
        model_ok = True
        st.markdown(
            '<div class="pill pill-ok"><div class="pdot"></div>Model Ready ✓</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="pill pill-err"><div class="pdot"></div>Setup Failed</div>',
            unsafe_allow_html=True,
        )
        with st.expander("🔍 Setup Details"):
            for step in setup_steps:
                st.markdown(step)
            st.markdown(
                "**Run locally:**\n"
                "```bash\n"
                "pip install gramformer spacy errant torch transformers\n"
                "python -m spacy download en_core_web_sm\n"
                "streamlit run app_streamlit.py\n"
                "```"
            )

except Exception as e:
    st.markdown(
        f'<div class="pill pill-err"><div class="pdot"></div>Error</div>',
        unsafe_allow_html=True,
    )
    st.error(str(e))


# ==========================================
# 6. منطقة العمل
# ==========================================

st.markdown('<div class="workzone">', unsafe_allow_html=True)

# نماذج
EXAMPLES = [
    "Last weak, me and my freind goed to the librery.",
    "She dont knows what happend yestarday.",
    "I has been working hear for too yeers now.",
    "Their going to there house over they're.",
    "The childs was playing in the gardenn.",
    "He writed a leter to his teecher.",
]

st.markdown("""
<div class="gc"><div class="gc-head">
    <div class="gc-title"><div class="gc-ico">💡</div>Try an Example</div>
</div></div>
""", unsafe_allow_html=True)

ecols = st.columns(3)
for i, ex in enumerate(EXAMPLES):
    with ecols[i % 3]:
        short = ex[:32] + "..." if len(ex) > 32 else ex
        if st.button(short, key=f"ex{i}", use_container_width=True):
            st.session_state["inp"] = ex

# الإدخال
st.markdown("""
<div class="gc"><div class="gc-head">
    <div class="gc-title"><div class="gc-ico">✍️</div>Input Text</div>
    <span class="gc-badge">English</span>
</div></div>
""", unsafe_allow_html=True)

default = "Last weak, me and my freind goed to the librery to studdy for our finalle examms."

user_text = st.text_area(
    label="t",
    value=st.session_state.get("inp", default),
    height=150,
    placeholder="Type English text with errors...",
    label_visibility="collapsed",
    key="ibox",
)

wc = len(user_text.split()) if user_text.strip() else 0
st.caption(f"📏 {wc} words · {len(user_text)} chars")

b1, b2, b3 = st.columns([3, 1, 1])
with b1:
    go = st.button("🚀 Correct with AI", type="primary",
                    use_container_width=True, disabled=not model_ok)
with b2:
    clr = st.button("🗑️ Clear", use_container_width=True)
with b3:
    cpy = st.button("📋 Copy", use_container_width=True)

if clr:
    st.session_state["inp"] = ""
    st.session_state["result"] = ""
    st.rerun()


# Diff
def make_diff(orig, fixed):
    d = difflib.ndiff(orig.split(), fixed.split())
    parts = []
    for t in d:
        if t.startswith("- "):
            parts.append(f'<mark class="err">{t[2:]}</mark>')
        elif t.startswith("+ "):
            parts.append(f'<mark class="fix">{t[2:]}</mark>')
        elif t.startswith("  "):
            parts.append(t[2:])
    return " ".join(parts)


# النتائج
st.markdown("""
<div class="gc"><div class="gc-head">
    <div class="gc-title"><div class="gc-ico">✨</div>Results</div>
</div></div>
""", unsafe_allow_html=True)

rhold = st.empty()

if "result" in st.session_state and st.session_state["result"]:
    rhold.markdown(
        f'<div class="rbox rbox-clean">{st.session_state["result"]}</div>',
        unsafe_allow_html=True,
    )
else:
    rhold.markdown(
        '<div class="rbox rbox-empty">✍️ Results appear here</div>',
        unsafe_allow_html=True,
    )

if go:
    if not user_text.strip():
        st.warning("⚠️ Enter text first!")
    elif not model_ok:
        st.error("❌ Model not loaded")
    else:
        with st.spinner("🧠 Correcting..."):
            t0 = time.time()
            sents = re.split(r'(?<=[.!?])\s+', user_text.strip())
            fixed = []

            for s in sents:
                if s.strip():
                    try:
                        r = gf.correct(s, max_candidates=1)
                        fixed.append(list(r)[0] if r else s)
                    except Exception:
                        fixed.append(s)

            final = " ".join(fixed)
            elapsed = round(time.time() - t0, 2)

        st.session_state["result"] = final

        diff_html = make_diff(user_text, final)
        st.markdown(
            '<div class="gc-title" style="margin-top:1rem">'
            '<div class="gc-ico">🔍</div>Change Map</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="rbox rbox-diff">{diff_html}</div>',
            unsafe_allow_html=True,
        )

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            '<div class="gc-title"><div class="gc-ico">✅</div>Corrected</div>',
            unsafe_allow_html=True,
        )
        rhold.markdown(
            f'<div class="rbox rbox-clean">{final}</div>',
            unsafe_allow_html=True,
        )

        st.success(f"✅ Done in {elapsed}s!")

        ow = user_text.split()
        fw = final.split()
        changes = sum(1 for a, b in zip(ow, fw) if a != b) + abs(len(ow) - len(fw))

        st.markdown(f"""
        <div class="sgrid">
            <div class="sc"><div class="sc-val">{len(ow)}</div><div class="sc-lbl">Words</div></div>
            <div class="sc"><div class="sc-val" style="color:#ff7675">{changes}</div><div class="sc-lbl">Changes</div></div>
            <div class="sc"><div class="sc-val" style="color:#55efc4">{len(sents)}</div><div class="sc-lbl">Sentences</div></div>
            <div class="sc"><div class="sc-val" style="color:var(--cyan)">{elapsed}s</div><div class="sc-lbl">Time</div></div>
        </div>
        """, unsafe_allow_html=True)

if cpy:
    lr = st.session_state.get("result", "")
    if lr:
        st.code(lr, language=None)
        st.info("📋 Select and copy Ctrl+C")
    else:
        st.warning("⚠️ No result")


# ==========================================
# 7. الميزات
# ==========================================

st.markdown("""
<div class="fgrid">
    <div class="fc"><div class="fc-ico">🧠</div><div class="fc-ttl">Deep Context</div><div class="fc-dsc">T5 understands meaning beyond spell-check</div></div>
    <div class="fc"><div class="fc-ico">🔍</div><div class="fc-ttl">Visual Diff</div><div class="fc-dsc">Color-coded changes show what was fixed</div></div>
    <div class="fc"><div class="fc-ico">⚡</div><div class="fc-ttl">Fast</div><div class="fc-dsc">Sentence-by-sentence for speed</div></div>
    <div class="fc"><div class="fc-ico">📊</div><div class="fc-ttl">Statistics</div><div class="fc-dsc">Detailed correction metrics</div></div>
    <div class="fc"><div class="fc-ico">🎯</div><div class="fc-ttl">Grammar + Spelling</div><div class="fc-dsc">Fixes both error types</div></div>
    <div class="fc"><div class="fc-ico">🆓</div><div class="fc-ttl">Free</div><div class="fc-dsc">No limits or sign-up</div></div>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)


# ==========================================
# 8. الفوتر
# ==========================================

st.markdown("""
<div class="appfoot">
    <div class="af-brand">🤖 Gramformer AI</div>
    <div class="af-txt">Built with Gramformer + HuggingFace<br>Made with ❤️</div>
</div>
""", unsafe_allow_html=True)
