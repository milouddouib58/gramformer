"""
🌍 المترجم الذكي - AI Translator
ترجمة متعددة اللغات باستخدام نماذج Helsinki-NLP
يدعم: العربية، الإنجليزية، الفرنسية، الألمانية، الإسبانية، وغيرها

التشغيل:
    streamlit run trans.py
"""

import streamlit as st
import time
import sys

# ==========================================
# 1. إعدادات الصفحة
# ==========================================
st.set_page_config(
    page_title="AI Translator | المترجم الذكي",
    page_icon="🌍",
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
    --blue:#3b82f6;--blue-light:#60a5fa;--blue-dark:#2563eb;
    --teal:#14b8a6;--teal-light:#2dd4bf;
    --gold:#e9c46a;--orange:#f4a261;
    --purple:#a855f7;--pink:#ec4899;
    --green:#2ecc71;--red:#e74c3c;
    --dark-1:#030712;--dark-2:#0f172a;--dark-3:#1e293b;
    --text-primary:#f1f5f9;--text-secondary:#94a3b8;
    --glass:rgba(255,255,255,0.03);
    --glass-border:rgba(255,255,255,0.08);
    --glass-hover:rgba(255,255,255,0.06);
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

/* الخلفية */
.bg-fx{position:fixed;inset:0;z-index:0;pointer-events:none;overflow:hidden}
.bg-orb{position:absolute;border-radius:50%;filter:blur(120px);opacity:.1;
    animation:drift 30s ease-in-out infinite}
.o1{width:600px;height:600px;background:var(--blue);top:-250px;right:-150px}
.o2{width:450px;height:450px;background:var(--teal);bottom:-200px;left:-150px;
    animation-delay:-10s}
.o3{width:350px;height:350px;background:var(--purple);top:50%;left:40%;
    animation-delay:-20s}
.bg-dots{position:absolute;inset:0;
    background-image:radial-gradient(rgba(59,130,246,.06) 1px,transparent 1px);
    background-size:40px 40px}
@keyframes drift{
    0%,100%{transform:translate(0,0) scale(1)}
    33%{transform:translate(60px,-70px) scale(1.1)}
    66%{transform:translate(-50px,60px) scale(.9)}}

/* الشريط العلوي */
.topbar{position:relative;z-index:10;display:flex;align-items:center;
    justify-content:space-between;padding:1rem 3rem;
    background:rgba(15,23,42,.8);backdrop-filter:blur(25px);
    border-bottom:1px solid var(--glass-border)}
.tb-brand{display:flex;align-items:center;gap:.7rem}
.tb-logo{width:38px;height:38px;
    background:linear-gradient(135deg,var(--blue),var(--teal));
    border-radius:11px;display:flex;align-items:center;
    justify-content:center;font-size:1.2rem;
    box-shadow:0 4px 12px rgba(59,130,246,.3)}
.tb-name{font-size:1.15rem;font-weight:800;color:var(--blue-light)}
.tb-links{display:flex;gap:1.5rem;align-items:center}
.tb-link{color:var(--text-secondary);font-size:.9rem;
    text-decoration:none;cursor:pointer;transition:color .3s}
.tb-link:hover{color:var(--blue-light)}
.tb-tag{background:rgba(59,130,246,.15);
    border:1px solid rgba(59,130,246,.3);color:var(--blue-light);
    padding:.3rem .9rem;border-radius:50px;font-size:.78rem;font-weight:700}

/* Hero */
.hero{position:relative;z-index:1;text-align:center;padding:3rem 2rem 2rem}
.hero-chip{display:inline-flex;align-items:center;gap:.5rem;
    background:rgba(59,130,246,.08);border:1px solid rgba(59,130,246,.18);
    padding:.4rem 1.2rem;border-radius:50px;font-size:.82rem;
    color:var(--blue-light);margin-bottom:1.5rem}
.hero h1{font-size:3rem;font-weight:900;line-height:1.15;margin-bottom:1rem}
.hero h1 .glow{
    background:linear-gradient(135deg,var(--blue-light),var(--teal),var(--blue));
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;
    background-clip:text}
.hero-desc{font-size:1.1rem;color:var(--text-secondary);
    max-width:600px;margin:0 auto 2rem;line-height:1.8;font-weight:300}
.hero-row{display:flex;justify-content:center;gap:3rem}
.hr-val{font-size:1.5rem;font-weight:900;color:var(--blue-light)}
.hr-lbl{font-size:.8rem;color:var(--text-secondary)}

/* منطقة العمل */
.workzone{position:relative;z-index:1;max-width:1100px;margin:0 auto;
    padding:0 2rem 3rem}

/* بطاقة */
.gc{background:var(--glass);backdrop-filter:blur(20px);
    border:1px solid var(--glass-border);border-radius:22px;
    padding:1.8rem;margin-bottom:1.3rem;transition:border-color .3s}
.gc:hover{border-color:rgba(59,130,246,.12)}
.gc-head{display:flex;align-items:center;justify-content:space-between;
    margin-bottom:1rem}
.gc-title{display:flex;align-items:center;gap:.6rem;
    font-size:1.05rem;font-weight:700}
.gc-ico{width:30px;height:30px;
    background:linear-gradient(135deg,var(--blue),var(--teal));
    border-radius:9px;display:flex;align-items:center;
    justify-content:center;font-size:.85rem}
.gc-badge{font-size:.78rem;color:var(--text-secondary);
    background:rgba(255,255,255,.04);padding:.25rem .7rem;
    border-radius:20px;border:1px solid var(--glass-border)}

/* TextArea */
.stTextArea textarea{
    font-size:1.15rem!important;line-height:2!important;
    background:rgba(0,0,0,.3)!important;
    border:2px solid var(--glass-border)!important;
    border-radius:14px!important;padding:1.3rem!important;
    color:var(--text-primary)!important;
    transition:border-color .3s,box-shadow .3s!important}
.stTextArea textarea:focus{border-color:var(--blue)!important;
    box-shadow:0 0 0 3px rgba(59,130,246,.1)!important}
.stTextArea textarea::placeholder{color:rgba(255,255,255,.18)!important}

/* نتيجة */
.rbox{border:2px solid rgba(59,130,246,.2);border-radius:14px;
    padding:1.5rem;font-size:1.15rem;line-height:2.2;
    color:var(--text-primary);min-height:150px;position:relative;
    overflow:hidden;word-wrap:break-word;
    background:linear-gradient(135deg,
        rgba(59,130,246,.04),rgba(20,184,166,.03))}
.rbox::before{content:'';position:absolute;top:0;left:0;right:0;
    height:3px;border-radius:14px 14px 0 0;
    background:linear-gradient(90deg,var(--blue),var(--teal))}
.rbox-rtl{direction:rtl;text-align:right;
    font-family:'Noto Naskh Arabic','Tajawal',sans-serif!important}
.rbox-ltr{direction:ltr;text-align:left;
    font-family:'JetBrains Mono',monospace!important}
.rbox-empty{color:rgba(255,255,255,.15);font-family:'Tajawal'!important;
    font-size:.95rem;display:flex;align-items:center;justify-content:center}

/* أزرار */
.stButton>button{border-radius:12px!important;padding:.75rem!important;
    font-weight:700!important;font-size:1.05rem!important;border:none!important}
.stButton>button[kind="primary"]{
    background:linear-gradient(135deg,var(--blue),var(--teal))!important;
    color:white!important;
    box-shadow:0 4px 18px rgba(59,130,246,.25)!important}
.stButton>button[kind="primary"]:hover{transform:translateY(-2px)!important;
    box-shadow:0 8px 28px rgba(59,130,246,.35)!important}
.stButton>button[kind="secondary"]{background:var(--glass)!important;
    color:var(--text-primary)!important;
    border:1px solid var(--glass-border)!important}

/* إحصائيات */
.sgrid{display:grid;grid-template-columns:repeat(4,1fr);gap:.8rem;
    margin-top:1.2rem}
.sc{background:linear-gradient(135deg,rgba(30,41,59,.8),rgba(15,23,42,.9));
    border:1px solid var(--glass-border);border-radius:16px;padding:1.2rem;
    text-align:center;transition:all .3s}
.sc:hover{transform:translateY(-4px);border-color:rgba(59,130,246,.25)}
.sc-val{font-size:1.8rem;font-weight:900;color:var(--blue-light)}
.sc-lbl{font-size:.8rem;color:var(--text-secondary);margin-top:.2rem}

/* حالة */
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

/* اختيار اللغة */
.lang-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:1rem;
    margin:1rem 0}
.lang-card{background:var(--glass);border:1px solid var(--glass-border);
    border-radius:14px;padding:1rem;text-align:center;cursor:pointer;
    transition:all .3s}
.lang-card:hover{border-color:rgba(59,130,246,.3)}
.lang-card.active{border-color:var(--blue);
    background:rgba(59,130,246,.08)}
.lang-flag{font-size:2rem;margin-bottom:.3rem}
.lang-name{font-weight:700;font-size:.9rem}

/* سهم التبديل */
.swap-arrow{text-align:center;font-size:1.5rem;color:var(--blue-light);
    padding:.5rem;cursor:pointer;transition:transform .3s}
.swap-arrow:hover{transform:scale(1.2)}

/* ميزات */
.fgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;
    margin:2.5rem 0}
.fc{background:var(--glass);border:1px solid var(--glass-border);
    border-radius:18px;padding:1.5rem;text-align:center;transition:all .3s}
.fc:hover{border-color:rgba(59,130,246,.18);transform:translateY(-3px)}
.fc-ico{font-size:1.8rem;margin-bottom:.7rem}
.fc-ttl{font-weight:700;margin-bottom:.3rem}
.fc-dsc{font-size:.82rem;color:var(--text-secondary);line-height:1.7}

/* فوتر */
.appfoot{position:relative;z-index:1;text-align:center;padding:2.5rem 2rem;
    border-top:1px solid var(--glass-border);margin-top:2rem}
.af-brand{font-size:1.1rem;font-weight:800;color:var(--blue-light)}
.af-txt{color:var(--text-secondary);font-size:.82rem;margin-top:.3rem}

/* Radio مخصص */
div[role="radiogroup"]{direction:ltr!important;gap:.5rem!important}
div[role="radiogroup"] label{
    background:var(--glass)!important;
    border:1px solid var(--glass-border)!important;
    border-radius:12px!important;padding:.8rem 1.2rem!important;
    color:var(--text-primary)!important;transition:all .3s!important}
div[role="radiogroup"] label:hover{
    border-color:rgba(59,130,246,.3)!important}
div[role="radiogroup"] label[data-checked="true"]{
    border-color:var(--blue)!important;
    background:rgba(59,130,246,.1)!important}

/* Selectbox */
.stSelectbox > div > div{
    background:rgba(0,0,0,.3)!important;
    border:2px solid var(--glass-border)!important;
    border-radius:12px!important;
    color:var(--text-primary)!important}

@media(max-width:768px){
    .topbar{padding:.7rem 1rem}.tb-links{display:none}
    .hero h1{font-size:2rem}.hero-row{gap:1.5rem}
    .sgrid{grid-template-columns:repeat(2,1fr)}
    .fgrid{grid-template-columns:1fr}
    .workzone{padding:0 1rem 2rem}
    .lang-grid{grid-template-columns:1fr}
}
</style>
""", unsafe_allow_html=True)


# ==========================================
# 3. اللغات المدعومة ونماذج الترجمة
# ==========================================

LANGUAGES = {
    "🇬🇧 English": "en",
    "🇸🇦 العربية": "ar",
    "🇫🇷 Français": "fr",
    "🇩🇪 Deutsch": "de",
    "🇪🇸 Español": "es",
    "🇮🇹 Italiano": "it",
    "🇵🇹 Português": "pt",
    "🇷🇺 Русский": "ru",
    "🇨🇳 中文": "zh",
    "🇯🇵 日本語": "ja",
    "🇰🇷 한국어": "ko",
    "🇹🇷 Türkçe": "tr",
    "🇳🇱 Nederlands": "nl",
    "🇵🇱 Polski": "pl",
    "🇸🇪 Svenska": "sv",
}

RTL_LANGS = {"ar", "he", "fa", "ur"}


def get_model_name(src_code, tgt_code):
    """الحصول على اسم النموذج من Helsinki-NLP"""
    return f"Helsinki-NLP/opus-mt-{src_code}-{tgt_code}"


def get_fallback_models(src_code, tgt_code):
    """نماذج بديلة إذا لم يوجد نموذج مباشر"""
    models = [
        f"Helsinki-NLP/opus-mt-{src_code}-{tgt_code}",
    ]

    # عبر الإنجليزية كوسيط
    if src_code != "en" and tgt_code != "en":
        models.append(f"Helsinki-NLP/opus-mt-{src_code}-en")
        models.append(f"Helsinki-NLP/opus-mt-en-{tgt_code}")

    # نماذج متعددة اللغات
    models.append("facebook/mbart-large-50-many-to-many-mmt")

    return models


# ==========================================
# 4. تحميل نموذج الترجمة
# ==========================================

@st.cache_resource
def load_translator(src_code, tgt_code):
    """تحميل نموذج الترجمة"""
    from transformers import (
        AutoTokenizer,
        AutoModelForSeq2SeqLM,
        pipeline,
    )

    model_name = get_model_name(src_code, tgt_code)

    try:
        translator = pipeline(
            "translation",
            model=model_name,
            tokenizer=model_name,
            device=-1,
        )
        return translator, model_name, None

    except Exception as e1:
        # محاولة بديلة: عكس tc/mul
        alternatives = [
            f"Helsinki-NLP/opus-mt-tc-big-{src_code}-{tgt_code}",
            f"Helsinki-NLP/opus-mt-mul-{tgt_code}",
            f"Helsinki-NLP/opus-mt-{src_code}-mul",
        ]

        for alt in alternatives:
            try:
                translator = pipeline(
                    "translation",
                    model=alt,
                    tokenizer=alt,
                    device=-1,
                )
                return translator, alt, None
            except Exception:
                continue

        return None, model_name, str(e1)


def translate_text(text, translator):
    """ترجمة النص"""
    # تقسيم النص الطويل
    max_len = 400
    if len(text) <= max_len:
        result = translator(
            text, max_length=512, num_beams=4
        )
        return result[0]["translation_text"]

    # تقسيم بالجمل
    import re
    sentences = re.split(r'(?<=[.!?。！？])\s+', text)
    translated = []

    for sent in sentences:
        if sent.strip():
            try:
                r = translator(
                    sent, max_length=512, num_beams=4
                )
                translated.append(r[0]["translation_text"])
            except Exception:
                translated.append(sent)

    return " ".join(translated)


# ==========================================
# 5. الواجهة
# ==========================================

# الخلفية
st.markdown("""
<div class="bg-fx">
    <div class="bg-orb o1"></div>
    <div class="bg-orb o2"></div>
    <div class="bg-orb o3"></div>
    <div class="bg-dots"></div>
</div>
<div class="topbar">
    <div class="tb-brand">
        <div class="tb-logo">🌍</div>
        <span class="tb-name">AI Translator</span>
    </div>
    <div class="tb-links">
        <span class="tb-link">الرئيسية</span>
        <span class="tb-link">اللغات</span>
        <span class="tb-tag">Helsinki-NLP</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Hero
st.markdown("""
<div class="hero">
    <div class="hero-chip">🌐 مدعوم بالذكاء الاصطناعي</div>
    <h1><span class="glow">المترجم الذكي</span></h1>
    <p class="hero-desc">
        ترجمة فورية بين أكثر من 15 لغة باستخدام نماذج
        Helsinki-NLP المتقدمة — دقيق، سريع، ومجاني
    </p>
    <div class="hero-row">
        <div><div class="hr-val">15+</div>
            <div class="hr-lbl">لغة مدعومة</div></div>
        <div><div class="hr-val">&lt;2s</div>
            <div class="hr-lbl">سرعة الترجمة</div></div>
        <div><div class="hr-val">∞</div>
            <div class="hr-lbl">بدون حدود</div></div>
    </div>
</div>
""", unsafe_allow_html=True)


st.markdown('<div class="workzone">', unsafe_allow_html=True)

# ==========================================
# 6. اختيار اللغات
# ==========================================

st.markdown(
    '<div class="gc"><div class="gc-head">'
    '<div class="gc-title"><div class="gc-ico">🔤</div>'
    'اختيار اللغات</div></div></div>',
    unsafe_allow_html=True,
)

lang_names = list(LANGUAGES.keys())

col_src, col_swap, col_tgt = st.columns([5, 1, 5])

with col_src:
    src_lang = st.selectbox(
        "من:", lang_names,
        index=0,
        key="src_lang",
    )

with col_swap:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄", key="swap", use_container_width=True):
        old_src = st.session_state.get("src_lang", lang_names[0])
        old_tgt = st.session_state.get("tgt_lang", lang_names[1])
        st.session_state["src_lang"] = old_tgt
        st.session_state["tgt_lang"] = old_src
        # تبديل النص أيضاً
        old_input = st.session_state.get("trans_input", "")
        old_result = st.session_state.get("trans_result", "")
        if old_result:
            st.session_state["trans_input"] = old_result
            st.session_state["trans_result"] = ""
        st.rerun()

with col_tgt:
    tgt_lang = st.selectbox(
        "إلى:", lang_names,
        index=1,
        key="tgt_lang",
    )

src_code = LANGUAGES[src_lang]
tgt_code = LANGUAGES[tgt_lang]


# ==========================================
# 7. تحميل النموذج
# ==========================================

translator = None
model_ok = False

if src_code == tgt_code:
    st.warning("⚠️ اختر لغتين مختلفتين")
else:
    try:
        with st.spinner(
            f"🔄 Loading {src_lang} → {tgt_lang} model..."
        ):
            translator, used_model, err = load_translator(
                src_code, tgt_code
            )

        if translator is not None:
            model_ok = True
            st.markdown(
                f'<div class="pill pill-ok">'
                f'<div class="pdot"></div>'
                f'Ready: {src_lang} → {tgt_lang}</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<div class="pill pill-err">'
                '<div class="pdot"></div>'
                'Model not available</div>',
                unsafe_allow_html=True,
            )
            with st.expander("🔍 Details"):
                st.error(err)
                st.info(
                    f"Model `{used_model}` not found.\n\n"
                    f"Try: English as source or target."
                )

    except Exception as e:
        st.markdown(
            '<div class="pill pill-err">'
            '<div class="pdot"></div>'
            'Error</div>',
            unsafe_allow_html=True,
        )
        with st.expander("🔍 Details"):
            st.error(str(e))


# ==========================================
# 8. نماذج جاهزة
# ==========================================

SAMPLES = {
    "en": [
        "Artificial intelligence is transforming the world.",
        "The weather is beautiful today.",
        "I love learning new languages.",
    ],
    "ar": [
        "الذكاء الاصطناعي يغير العالم بسرعة كبيرة.",
        "الطقس جميل اليوم والسماء صافية.",
        "أحب تعلم اللغات الجديدة.",
    ],
    "fr": [
        "L'intelligence artificielle transforme le monde.",
        "Le temps est magnifique aujourd'hui.",
        "J'adore apprendre de nouvelles langues.",
    ],
    "de": [
        "Künstliche Intelligenz verändert die Welt.",
        "Das Wetter ist heute wunderschön.",
        "Ich liebe es, neue Sprachen zu lernen.",
    ],
    "es": [
        "La inteligencia artificial está transformando el mundo.",
        "El clima es hermoso hoy.",
        "Me encanta aprender nuevos idiomas.",
    ],
}

samples = SAMPLES.get(src_code, SAMPLES["en"])

st.markdown(
    '<div class="gc"><div class="gc-head">'
    '<div class="gc-title"><div class="gc-ico">💡</div>'
    'جرّب نصاً</div></div></div>',
    unsafe_allow_html=True,
)

scols = st.columns(3)
for i, s in enumerate(samples):
    with scols[i % 3]:
        short = s[:30] + "..." if len(s) > 30 else s
        if st.button(
            short, key=f"ts{i}", use_container_width=True
        ):
            st.session_state["trans_input"] = s


# ==========================================
# 9. الإدخال
# ==========================================

is_src_rtl = src_code in RTL_LANGS
is_tgt_rtl = tgt_code in RTL_LANGS

st.markdown(
    '<div class="gc"><div class="gc-head">'
    '<div class="gc-title"><div class="gc-ico">✍️</div>'
    f'النص الأصلي ({src_lang})</div>'
    f'<span class="gc-badge">{src_code.upper()}</span>'
    '</div></div>',
    unsafe_allow_html=True,
)

user_text = st.text_area(
    label="input",
    value=st.session_state.get("trans_input", ""),
    height=150,
    placeholder="اكتب أو الصق النص هنا...",
    label_visibility="collapsed",
    key="tinput",
)

wc = len(user_text.split()) if user_text.strip() else 0
st.caption(f"📏 {wc} كلمة · {len(user_text)} حرف")


# أزرار
b1, b2, b3 = st.columns([3, 1, 1])
with b1:
    go = st.button(
        "🌍 ترجمة", type="primary",
        use_container_width=True,
        disabled=not model_ok,
    )
with b2:
    clr = st.button("🗑️ مسح", use_container_width=True)
with b3:
    cpy = st.button("📋 نسخ", use_container_width=True)

if clr:
    st.session_state["trans_input"] = ""
    st.session_state["trans_result"] = ""
    st.rerun()


# ==========================================
# 10. النتيجة
# ==========================================

st.markdown(
    '<div class="gc"><div class="gc-head">'
    '<div class="gc-title"><div class="gc-ico">✨</div>'
    f'الترجمة ({tgt_lang})</div>'
    f'<span class="gc-badge">{tgt_code.upper()}</span>'
    '</div></div>',
    unsafe_allow_html=True,
)

rhold = st.empty()
rtl_class = "rbox-rtl" if is_tgt_rtl else "rbox-ltr"

if (
    "trans_result" in st.session_state
    and st.session_state["trans_result"]
):
    rhold.markdown(
        f'<div class="rbox {rtl_class}">'
        f'{st.session_state["trans_result"]}</div>',
        unsafe_allow_html=True,
    )
else:
    rhold.markdown(
        '<div class="rbox rbox-empty">'
        '🌍 ستظهر الترجمة هنا</div>',
        unsafe_allow_html=True,
    )


# الترجمة
if go:
    if not user_text.strip():
        st.warning("⚠️ أدخل نصاً أولاً")
    elif not model_ok:
        st.error("❌ النموذج غير متاح")
    else:
        with st.spinner("🌍 جاري الترجمة..."):
            t0 = time.time()
            try:
                result = translate_text(user_text, translator)
                elapsed = round(time.time() - t0, 2)

                st.session_state["trans_result"] = result

                rhold.markdown(
                    f'<div class="rbox {rtl_class}">'
                    f'{result}</div>',
                    unsafe_allow_html=True,
                )

                st.success(f"✅ تمت الترجمة في {elapsed}s!")

                # إحصائيات
                src_words = len(user_text.split())
                tgt_words = len(result.split())

                st.markdown(f"""
                <div class="sgrid">
                    <div class="sc">
                        <div class="sc-val">{src_words}</div>
                        <div class="sc-lbl">كلمة (مصدر)</div>
                    </div>
                    <div class="sc">
                        <div class="sc-val">{tgt_words}</div>
                        <div class="sc-lbl">كلمة (هدف)</div>
                    </div>
                    <div class="sc">
                        <div class="sc-val">{len(user_text)}</div>
                        <div class="sc-lbl">حرف</div>
                    </div>
                    <div class="sc">
                        <div class="sc-val">{elapsed}s</div>
                        <div class="sc-lbl">الوقت</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"❌ خطأ: {e}")


# نسخ
if cpy:
    lr = st.session_state.get("trans_result", "")
    if lr:
        st.code(lr, language=None)
        st.info("📋 حدّد وانسخ Ctrl+C")
    else:
        st.warning("⚠️ لا نتيجة")


# ==========================================
# 11. اللغات المدعومة
# ==========================================

st.markdown(
    '<div class="gc"><div class="gc-head">'
    '<div class="gc-title"><div class="gc-ico">🗣️</div>'
    'اللغات المدعومة</div></div></div>',
    unsafe_allow_html=True,
)

lcols = st.columns(5)
for i, (name, code) in enumerate(LANGUAGES.items()):
    with lcols[i % 5]:
        st.markdown(
            f"<div style='text-align:center;padding:.5rem;'>"
            f"<div style='font-size:1.5rem;'>"
            f"{name.split()[0]}</div>"
            f"<div style='font-size:.75rem;color:var(--text-secondary);'>"
            f"{code.upper()}</div></div>",
            unsafe_allow_html=True,
        )


# ==========================================
# 12. الميزات
# ==========================================

st.markdown("""
<div class="fgrid">
    <div class="fc"><div class="fc-ico">🧠</div>
        <div class="fc-ttl">ذكاء اصطناعي</div>
        <div class="fc-dsc">نماذج Helsinki-NLP المدرّبة على ملايين الجمل</div></div>
    <div class="fc"><div class="fc-ico">🌍</div>
        <div class="fc-ttl">15+ لغة</div>
        <div class="fc-dsc">عربي، إنجليزي، فرنسي، ألماني، وأكثر</div></div>
    <div class="fc"><div class="fc-ico">⚡</div>
        <div class="fc-ttl">سريع</div>
        <div class="fc-dsc">ترجمة فورية في أقل من ثانيتين</div></div>
    <div class="fc"><div class="fc-ico">🔄</div>
        <div class="fc-ttl">ثنائي الاتجاه</div>
        <div class="fc-dsc">بدّل اللغات بضغطة زر واحدة</div></div>
    <div class="fc"><div class="fc-ico">📱</div>
        <div class="fc-ttl">متجاوب</div>
        <div class="fc-dsc">يعمل على جميع الأجهزة</div></div>
    <div class="fc"><div class="fc-ico">🆓</div>
        <div class="fc-ttl">مجاني</div>
        <div class="fc-dsc">بدون حدود أو تسجيل</div></div>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)


# ==========================================
# 13. الفوتر
# ==========================================

st.markdown("""
<div class="appfoot">
    <div class="af-brand">🌍 AI Translator — المترجم الذكي</div>
    <div class="af-txt">
        Built with Helsinki-NLP + HuggingFace Transformers<br>
        صُنع بـ ❤️ لكسر حواجز اللغة
    </div>
</div>
""", unsafe_allow_html=True)
