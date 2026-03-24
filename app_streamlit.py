import streamlit as st
import time
import re
import difflib
import sys

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
# 2. CSS
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

.sgrid{display:grid;grid-template-columns:repeat(4,1fr);gap:.8rem;
    margin-top:1.2rem}
.sc{background:linear-gradient(135deg,rgba(26,26,62,.8),rgba(13,13,43,.9));
    border:1px solid var(--glass-border);border-radius:16px;padding:1.2rem;
    text-align:center;transition:all .3s}
.sc:hover{transform:translateY(-4px);border-color:rgba(233,196,106,.25)}
.sc-val{font-size:1.8rem;font-weight:900;color:var(--gold)}
.sc-lbl{font-size:.8rem;color:var(--text-secondary);margin-top:.2rem}

.pill{display:inline-flex;align-items:center;gap:.45rem;padding:.4rem 1rem;
    border-radius:50px;font-size:.85rem;font-weight:600}
.pill-ok{background:rgba(46,204,113,.1);border:1px solid rgba(46,204,113,.25);
    color:#2ecc71}
.pill-err{background:rgba(231,76,60,.1);border:1px solid rgba(231,76,60,.25);
    color:#e74c3c}
.pdot{width:7px;height:7px;border-radius:50%;animation:blink 2s infinite}
.pill-ok .pdot{background:#2ecc71}
.pill-err .pdot{background:#e74c3c}
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
    border-radius:12px!important;
    color:var(--text-primary)!important}

@media(max-width:768px){
    .topbar{padding:.7rem 1rem}.hero h1{font-size:2rem}
    .sgrid{grid-template-columns:repeat(2,1fr)}
    .fgrid{grid-template-columns:1fr}
    .workzone{padding:0 1rem 2rem}}
</style>
""", unsafe_allow_html=True)


# ==========================================
# 3. نماذج التصحيح والترجمة
# ==========================================

@st.cache_resource
def load_corrector():
    """تحميل نموذج التصحيح النحوي T5"""
    from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
    name = "prithivida/grammar_error_correcter_v1"
    tok = AutoTokenizer.from_pretrained(name)
    mdl = AutoModelForSeq2SeqLM.from_pretrained(name)
    return tok, mdl


@st.cache_resource
def load_translator(src, tgt):
    """تحميل نموذج ترجمة Helsinki-NLP"""
    from transformers import pipeline

    names = [
        f"Helsinki-NLP/opus-mt-{src}-{tgt}",
        f"Helsinki-NLP/opus-mt-tc-big-{src}-{tgt}",
    ]

    for name in names:
        try:
            pipe = pipeline(
                "translation", model=name,
                tokenizer=name, device=-1,
            )
            return pipe, name, None
        except Exception:
            continue

    return None, names[0], f"Model not found for {src}→{tgt}"


# اللغات المدعومة للترجمة
TRANS_LANGS = {
    "🇸🇦 العربية (Arabic)": "ar",
    "🇫🇷 الفرنسية (French)": "fr",
    "🇩🇪 الألمانية (German)": "de",
    "🇪🇸 الإسبانية (Spanish)": "es",
    "🇮🇹 الإيطالية (Italian)": "it",
    "🇵🇹 البرتغالية (Portuguese)": "pt",
    "🇷🇺 الروسية (Russian)": "ru",
    "🇹🇷 التركية (Turkish)": "tr",
    "🇳🇱 الهولندية (Dutch)": "nl",
    "🇸🇪 السويدية (Swedish)": "sv",
    "🇨🇳 الصينية (Chinese)": "zh",
    "🇯🇵 اليابانية (Japanese)": "ja",
}

RTL_CODES = {"ar", "he", "fa", "ur"}


def correct_text(text, tokenizer, model):
    """تصحيح نص كامل"""
    sents = re.split(r'(?<=[.!?])\s+', text.strip())
    results = []
    for s in sents:
        if s.strip():
            try:
                inp = tokenizer(
                    "gec: " + s, return_tensors="pt",
                    max_length=128, truncation=True, padding=True,
                )
                out = model.generate(
                    **inp, max_length=128,
                    num_beams=5, early_stopping=True,
                )
                results.append(
                    tokenizer.decode(out[0], skip_special_tokens=True)
                )
            except Exception:
                results.append(s)
    return " ".join(results)


def translate_text(text, translator):
    """ترجمة نص"""
    max_chunk = 400
    if len(text) <= max_chunk:
        r = translator(text, max_length=512, num_beams=4)
        return r[0]["translation_text"]

    sents = re.split(r'(?<=[.!?])\s+', text.strip())
    parts = []
    for s in sents:
        if s.strip():
            try:
                r = translator(s, max_length=512, num_beams=4)
                parts.append(r[0]["translation_text"])
            except Exception:
                parts.append(s)
    return " ".join(parts)


def make_diff(orig, fixed):
    """HTML للفروقات"""
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


# ==========================================
# 4. الواجهة
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
    <span class="tb-tag">T5 + Helsinki-NLP</span>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <div class="hero-chip">🧠 Correct &amp; Translate</div>
    <h1><span class="glow">AI Grammar Corrector</span></h1>
    <p class="hero-desc">
        صحّح الأخطاء النحوية والإملائية ثم ترجم النص المُصحَّح
        إلى أي لغة — كل ذلك في مكان واحد
    </p>
</div>
""", unsafe_allow_html=True)


# ==========================================
# 5. تحميل نموذج التصحيح
# ==========================================

corrector_tok = None
corrector_mdl = None
corrector_ok = False

try:
    with st.spinner("🔄 Loading grammar model..."):
        corrector_tok, corrector_mdl = load_corrector()
    corrector_ok = True
    st.markdown(
        '<div class="pill pill-ok">'
        '<div class="pdot"></div>'
        'Grammar Model Ready ✓</div>',
        unsafe_allow_html=True,
    )
except Exception as e:
    st.markdown(
        '<div class="pill pill-err">'
        '<div class="pdot"></div>'
        f'Grammar Model Error</div>',
        unsafe_allow_html=True,
    )
    with st.expander("🔍 Details"):
        st.error(str(e))


# ==========================================
# 6. منطقة التصحيح
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

st.markdown(
    '<div class="gc"><div class="gc-head">'
    '<div class="gc-title"><div class="gc-ico">💡</div>'
    'Try an Example</div></div></div>',
    unsafe_allow_html=True,
)

ecols = st.columns(3)
for i, ex in enumerate(EXAMPLES):
    with ecols[i % 3]:
        short = ex[:32] + "..." if len(ex) > 32 else ex
        if st.button(short, key=f"ex{i}", use_container_width=True):
            st.session_state["inp"] = ex

# الإدخال
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
st.caption(f"📏 {wc} words · {len(user_text)} chars")

# أزرار التصحيح
b1, b2, b3 = st.columns([3, 1, 1])
with b1:
    go_correct = st.button(
        "🚀 Correct with AI", type="primary",
        use_container_width=True, disabled=not corrector_ok,
    )
with b2:
    clr = st.button("🗑️ Clear", use_container_width=True)
with b3:
    cpy_corr = st.button("📋 Copy", use_container_width=True, key="cpy1")

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

if "corrected" in st.session_state and st.session_state["corrected"]:
    corr_holder.markdown(
        f'<div class="rbox rbox-clean">'
        f'{st.session_state["corrected"]}</div>',
        unsafe_allow_html=True,
    )
else:
    corr_holder.markdown(
        '<div class="rbox rbox-empty">'
        '✍️ Corrected text appears here</div>',
        unsafe_allow_html=True,
    )

# التصحيح
if go_correct:
    if not user_text.strip():
        st.warning("⚠️ Enter text first!")
    else:
        with st.spinner("🧠 Correcting..."):
            t0 = time.time()
            final = correct_text(user_text, corrector_tok, corrector_mdl)
            elapsed = round(time.time() - t0, 2)

        st.session_state["corrected"] = final
        st.session_state["translated"] = ""

        # خريطة التعديلات
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

        corr_holder.markdown(
            f'<div class="rbox rbox-clean">{final}</div>',
            unsafe_allow_html=True,
        )
        st.success(f"✅ Corrected in {elapsed}s!")

        # إحصائيات
        ow = user_text.split()
        fw = final.split()
        changes = sum(1 for a, b in zip(ow, fw) if a != b) + abs(len(ow) - len(fw))

        st.markdown(f"""
        <div class="sgrid">
            <div class="sc"><div class="sc-val">{len(ow)}</div>
                <div class="sc-lbl">Words</div></div>
            <div class="sc"><div class="sc-val" style="color:#ff7675">{changes}</div>
                <div class="sc-lbl">Changes</div></div>
            <div class="sc"><div class="sc-val" style="color:#55efc4">
                {len(re.split(r'(?<=[.!?])\\s+', user_text.strip()))}</div>
                <div class="sc-lbl">Sentences</div></div>
            <div class="sc"><div class="sc-val" style="color:var(--cyan)">{elapsed}s</div>
                <div class="sc-lbl">Time</div></div>
        </div>
        """, unsafe_allow_html=True)

if cpy_corr:
    lr = st.session_state.get("corrected", "")
    if lr:
        st.code(lr, language=None)
        st.info("📋 Select and copy Ctrl+C")
    else:
        st.warning("⚠️ No result")


# ==========================================
# 7. قسم الترجمة
# ==========================================

st.markdown('<hr class="divider">', unsafe_allow_html=True)

st.markdown(
    '<div class="gc"><div class="gc-head">'
    '<div class="gc-title">'
    '<div class="gc-ico gc-ico-blue">🌍</div>'
    'ترجمة النص المُصحَّح</div>'
    '<span class="gc-badge">Translate Corrected Text</span>'
    '</div></div>',
    unsafe_allow_html=True,
)

# هل يوجد نص مصحح؟
corrected_text = st.session_state.get("corrected", "")

if not corrected_text:
    st.info("💡 صحّح النص أولاً ثم اختر لغة الترجمة")
else:
    # عرض النص المصحح الذي سيُترجم
    st.markdown(
        f"**النص الذي سيُترجم:** _{corrected_text[:100]}"
        f'{"..." if len(corrected_text) > 100 else ""}_'
    )

    # اختيار اللغة
    col_lang, col_btn = st.columns([3, 2])

    with col_lang:
        target_lang = st.selectbox(
            "ترجم إلى:",
            list(TRANS_LANGS.keys()),
            index=0,
            key="tgt_lang",
        )

    tgt_code = TRANS_LANGS[target_lang]

    with col_btn:
        st.markdown("<br>", unsafe_allow_html=True)
        go_translate = st.button(
            f"🌍 ترجم إلى {target_lang.split('(')[0].strip()}",
            type="primary",
            use_container_width=True,
            key="btn_trans",
        )

    # نتيجة الترجمة
    trans_holder = st.empty()

    if (
        "translated" in st.session_state
        and st.session_state["translated"]
    ):
        rtl_cls = "rbox-rtl" if tgt_code in RTL_CODES else ""
        trans_holder.markdown(
            f'<div class="rbox rbox-trans {rtl_cls}">'
            f'{st.session_state["translated"]}</div>',
            unsafe_allow_html=True,
        )

    # الترجمة
    if go_translate:
        with st.spinner(f"🌍 Translating to {target_lang}..."):
            try:
                translator, used_model, err = load_translator(
                    "en", tgt_code
                )

                if translator is None:
                    st.error(f"❌ {err}")
                else:
                    t0 = time.time()
                    translated = translate_text(
                        corrected_text, translator
                    )
                    elapsed = round(time.time() - t0, 2)

                    st.session_state["translated"] = translated

                    rtl_cls = "rbox-rtl" if tgt_code in RTL_CODES else ""
                    trans_holder.markdown(
                        f'<div class="rbox rbox-trans {rtl_cls}">'
                        f'{translated}</div>',
                        unsafe_allow_html=True,
                    )

                    st.success(
                        f"✅ Translated in {elapsed}s "
                        f"using `{used_model}`"
                    )

                    # إحصائيات
                    st.markdown(f"""
                    <div class="sgrid">
                        <div class="sc">
                            <div class="sc-val">{len(corrected_text.split())}</div>
                            <div class="sc-lbl">Source Words</div></div>
                        <div class="sc">
                            <div class="sc-val" style="color:var(--cyan)">
                                {len(translated.split())}</div>
                            <div class="sc-lbl">Translated Words</div></div>
                        <div class="sc">
                            <div class="sc-val" style="color:#a855f7">
                                {tgt_code.upper()}</div>
                            <div class="sc-lbl">Language</div></div>
                        <div class="sc">
                            <div class="sc-val" style="color:var(--green)">
                                {elapsed}s</div>
                            <div class="sc-lbl">Time</div></div>
                    </div>
                    """, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"❌ Translation error: {e}")

    # نسخ الترجمة
    cpy_trans = st.button(
        "📋 نسخ الترجمة", use_container_width=True, key="cpy2"
    )
    if cpy_trans:
        tr = st.session_state.get("translated", "")
        if tr:
            st.code(tr, language=None)
            st.info("📋 حدّد وانسخ Ctrl+C")
        else:
            st.warning("⚠️ لا توجد ترجمة")


# ==========================================
# 8. الميزات
# ==========================================

st.markdown("""
<div class="fgrid">
    <div class="fc"><div class="fc-ico">🧠</div>
        <div class="fc-ttl">تصحيح ذكي</div>
        <div class="fc-dsc">نموذج T5 يفهم السياق ويصحح الأخطاء</div></div>
    <div class="fc"><div class="fc-ico">🌍</div>
        <div class="fc-ttl">ترجمة فورية</div>
        <div class="fc-dsc">ترجم النص المصحح إلى 12+ لغة</div></div>
    <div class="fc"><div class="fc-ico">🔍</div>
        <div class="fc-ttl">خريطة التعديلات</div>
        <div class="fc-dsc">شاهد كل تغيير بالألوان</div></div>
    <div class="fc"><div class="fc-ico">⚡</div>
        <div class="fc-ttl">سريع</div>
        <div class="fc-dsc">تصحيح وترجمة في ثوانٍ</div></div>
    <div class="fc"><div class="fc-ico">📊</div>
        <div class="fc-ttl">إحصائيات</div>
        <div class="fc-dsc">كلمات، تغييرات، ووقت</div></div>
    <div class="fc"><div class="fc-ico">🆓</div>
        <div class="fc-ttl">مجاني</div>
        <div class="fc-dsc">بدون حدود أو تسجيل</div></div>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)


# ==========================================
# 9. الفوتر
# ==========================================

st.markdown("""
<div class="appfoot">
    <div class="af-brand">🤖 Grammar AI + 🌍 Translator</div>
    <div class="af-txt">
        T5 Grammar Correction + Helsinki-NLP Translation<br>
        Made with ❤️
    </div>
</div>
""", unsafe_allow_html=True)
