import html
import json
import os
import re

import streamlit as st


# ============================================================
# PAGE
# ============================================================

st.set_page_config(
    page_title="Semiconductor Learning Hub",
    layout="wide",
)


# ============================================================
# DESIGN TOKENS + CSS
# ------------------------------------------------------------
# Palette drawn from the semiconductor world itself:
#   ink      #16161A  graphite / die
#   paper    #F7F7F5  cleanroom surface
#   amber    #C98A05  lithography bay light (photoresist is UV-sensitive)
#   copper   #9A5B32  interconnect layer
#   line     #DCDCD6  hairline rule
# Type: IBM Plex in three roles -- Mono for labels and terms,
# Serif for reading, Sans for interface.
# ============================================================

st.html("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Serif:wght@400;500;600&display=swap');

:root {
    --ink:         #16161A;
    --ink-2:       #45454F;
    --muted:       #8B8B95;
    --paper:       #F7F7F5;
    --surface:     #FFFFFF;
    --line:        #DCDCD6;
    --amber:       #C98A05;
    --amber-fill:  #E9A70B;
    --amber-bg:    #FBF4E2;
    --copper:      #9A5B32;
}

.stApp { background: var(--paper); }

.block-container {
    max-width: 1080px;
    padding-top: 2.2rem;
    padding-bottom: 5rem;
}

/* Font is applied to text-bearing elements only.
   A blanket rule on span/div would also hit Streamlit's Material icon
   spans, which render their glyph through a font ligature -- overriding
   that font makes the raw name (keyboard_double_arrow_right) show up
   as literal text. */

.stApp,
.stApp p,
.stApp li,
.stApp label,
.stApp .stMarkdown,
.stApp h1, .stApp h2, .stApp h3, .stApp h4 {
    font-family: 'IBM Plex Sans', -apple-system, sans-serif;
    color: var(--ink-2);
}

/* Safety net: restore the icon font wherever Streamlit uses it. */

.stApp [data-testid="stIconMaterial"],
.stApp [class*="material-symbols"],
.stApp .material-icons {
    font-family: 'Material Symbols Rounded',
                 'Material Symbols Outlined',
                 'Material Icons' !important;
}

header[data-testid="stHeader"] { background: transparent; }

/* ---------- MASTHEAD ---------- */

.masthead {
    border-top: 2px solid var(--ink);
    padding-top: 18px;
    margin-bottom: 34px;
}

.mast-eyebrow {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11.5px;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 14px;
}

.mast-title {
    font-size: 40px;
    font-weight: 600;
    line-height: 1.12;
    letter-spacing: -0.02em;
    color: var(--ink);
    max-width: 24ch;
}

.mast-rule {
    height: 1px;
    background: var(--line);
    margin-top: 26px;
}

/* ---------- SECTION EYEBROW ---------- */

.eyebrow {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11.5px;
    font-weight: 500;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: var(--ink);
    border-top: 1px solid var(--ink);
    padding-top: 9px;
    margin: 52px 0 22px 0;
}

/* ---------- CONTENT ---------- */

.prose {
    font-family: 'IBM Plex Serif', serif;
    font-size: 16.5px;
    line-height: 1.62;
    color: var(--ink-2);
    max-width: 68ch;
    margin-bottom: 12px;
}

/* The topic body is emitted as ONE html block, so spacing is decided
   here rather than by Streamlit's per-element gap. */

.content > *:first-child { margin-top: 0; }
.content > *:last-child  { margin-bottom: 0; }

/* Trim the gap Streamlit puts between stacked elements. */

.block-container [data-testid="stVerticalBlock"] { gap: 0.7rem; }

.prose code {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.88em;
    background: var(--amber-bg);
    padding: 1px 5px;
}

/* Headings coming from HTML inside the JSON content */

.h-major {
    font-size: 21px;
    font-weight: 600;
    letter-spacing: -0.01em;
    color: var(--ink);
    border-top: 1px solid var(--line);
    padding-top: 13px;
    margin: 30px 0 11px 0;
    max-width: 68ch;
}

.h-minor {
    font-size: 17px;
    font-weight: 600;
    color: var(--ink);
    margin: 22px 0 8px 0;
    max-width: 68ch;
}

.h-minor::before {
    content: "";
    display: inline-block;
    width: 14px;
    height: 2px;
    background: var(--amber);
    vertical-align: middle;
    margin-right: 10px;
}

.bullet {
    display: grid;
    grid-template-columns: 24px 1fr;
    max-width: 68ch;
    margin: 4px 0;
    font-family: 'IBM Plex Serif', serif;
    font-size: 16px;
    line-height: 1.55;
    color: var(--ink-2);
}

.bullet-mark {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 12px;
    color: var(--amber);
    padding-top: 3px;
}

.sublabel {
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 0.04em;
    color: var(--ink);
    margin: 20px 0 7px 0;
}

/* ---------- FLOW / SIGNAL PATH ---------- */

.flow {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 14px;
    line-height: 1.9;
    color: var(--ink);
    background: var(--amber-bg);
    border-left: 2px solid var(--amber);
    padding: 13px 18px;
    margin: 16px 0;
    max-width: 68ch;
}

/* ---------- NUMBERED SECTIONS FROM THE CONTENT ---------- */

.h-sec {
    display: grid;
    grid-template-columns: 48px 1fr;
    font-size: 16.5px;
    font-weight: 600;
    color: var(--ink);
    margin: 24px 0 8px 0;
    max-width: 68ch;
}

.h-sec--major {
    font-size: 20px;
    letter-spacing: -0.01em;
    border-top: 1px solid var(--line);
    padding-top: 14px;
    margin-top: 34px;
}

.h-sec-idx {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 12px;
    font-weight: 500;
    color: var(--amber);
    padding-top: 4px;
}

.h-sec--major .h-sec-idx { padding-top: 7px; }

/* ---------- TABLES FROM THE CONTENT ---------- */

.table-wrap {
    overflow-x: auto;
    margin: 22px 0;
}

.table-wrap table {
    border-collapse: collapse;
    width: 100%;
    font-size: 14px;
}

.table-wrap th {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10.5px;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    text-align: left;
    color: var(--ink);
    border-bottom: 1px solid var(--ink);
    padding: 9px 18px 9px 0;
    white-space: nowrap;
}

.table-wrap td {
    font-family: 'IBM Plex Sans', sans-serif;
    color: var(--ink-2);
    border-bottom: 1px solid var(--line);
    padding: 10px 18px 10px 0;
    vertical-align: top;
    line-height: 1.5;
}

.table-wrap tr td:first-child {
    font-weight: 500;
    color: var(--ink);
}

/* ---------- ABOUT ---------- */

.about-lede {
    font-family: 'IBM Plex Serif', serif;
    font-size: 20px;
    line-height: 1.55;
    color: var(--ink);
    max-width: 58ch;
    margin-bottom: 24px;
}

.statbar {
    display: flex;
    flex-wrap: wrap;
    gap: 44px;
    border-top: 1px solid var(--ink);
    border-bottom: 1px solid var(--line);
    padding: 20px 0;
    margin: 34px 0;
}

.stat-num {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 30px;
    font-weight: 600;
    color: var(--ink);
    line-height: 1;
}

.stat-cap {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10.5px;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--muted);
    margin-top: 8px;
}

.byline {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11.5px;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--amber);
    margin-bottom: 12px;
}

.sb-author {
    font-family: 'IBM Plex Sans', sans-serif;
    font-size: 17px;
    font-weight: 600;
    color: var(--ink);
    margin-top: -12px;
}

.sb-role {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10.5px;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--muted);
    margin: 4px 0 22px 0;
    line-height: 1.6;
}

/* ---------- GLOSSARY ---------- */

.glossary {
    width: 100%;
    border-collapse: collapse;
    font-size: 15px;
}

.glossary td {
    padding: 11px 14px 11px 0;
    border-bottom: 1px solid var(--line);
    vertical-align: baseline;
}

.g-en {
    font-family: 'IBM Plex Mono', monospace;
    font-weight: 500;
    color: var(--ink);
    width: 52%;
}

.g-zh {
    font-family: 'IBM Plex Serif', serif;
    color: var(--copper);
}

/* ---------- TAKEAWAYS ---------- */

.take {
    display: grid;
    grid-template-columns: 42px 1fr;
    padding: 13px 0;
    border-bottom: 1px solid var(--line);
    max-width: 74ch;
}

.take-idx {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 12px;
    color: var(--amber);
    padding-top: 3px;
}

.take-text {
    font-family: 'IBM Plex Serif', serif;
    font-size: 15.5px;
    line-height: 1.65;
    color: var(--ink-2);
}

/* ---------- QUIZ ---------- */

.q-num {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11.5px;
    letter-spacing: 0.12em;
    color: var(--muted);
    margin-top: 26px;
}

.q-text {
    font-size: 17px;
    font-weight: 500;
    color: var(--ink);
    line-height: 1.5;
    margin: 6px 0 12px 0;
    max-width: 70ch;
}

.verdict {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 13px;
    padding: 10px 14px;
    margin-top: 4px;
    max-width: 70ch;
}

.verdict--ok { border-left: 2px solid var(--amber);  background: var(--amber-bg); color: var(--ink); }
.verdict--no { border-left: 2px solid var(--copper); background: #FAF0EA;         color: var(--ink); }

/* ---------- DIE MAP (signature) ---------- */

.diemap {
    display: flex;
    flex-wrap: wrap;
    gap: 4px;
    margin: 10px 0 6px 0;
}

.die {
    width: 13px;
    height: 13px;
    border: 1px solid var(--line);
    background: transparent;
}

.die--done { background: var(--ink);   border-color: var(--ink); }
.die--now  { background: var(--amber); border-color: var(--amber); }

.diemap-cap {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    letter-spacing: 0.1em;
    color: var(--muted);
}

/* ---------- SIDEBAR ---------- */

section[data-testid="stSidebar"] {
    background: var(--surface);
    border-right: 1px solid var(--line);
}

.sb-title {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 12px;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: var(--ink);
    border-top: 2px solid var(--ink);
    padding-top: 10px;
    margin-bottom: 22px;
}

/* ---------- WIDGETS ---------- */

/* Primary action: amber fill, dark text. Reads clearly against the
   near-white page, unlike the earlier solid black. */

.stFormSubmitButton > button {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    border-radius: 2px;
    border: 1px solid var(--amber);
    background: var(--amber-fill);
    color: var(--ink);
    padding: 7px 24px;
}

.stFormSubmitButton > button:hover {
    background: var(--amber);
    border-color: var(--amber);
    color: var(--ink);
}

.stFormSubmitButton > button:focus-visible {
    outline: 2px solid var(--ink);
    outline-offset: 2px;
}

/* Secondary action: outlined */

.stButton > button {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 12.5px;
    letter-spacing: 0.06em;
    border-radius: 2px;
    border: 1px solid var(--ink);
    background: transparent;
    color: var(--ink);
    padding: 6px 18px;
}

.stButton > button:hover {
    background: var(--ink);
    color: var(--paper);
    border-color: var(--ink);
}

.stTextInput input {
    font-family: 'IBM Plex Mono', monospace;
    border-radius: 2px;
    border: 1px solid var(--line);
    background: var(--surface);
    color: var(--ink);
}

.stTextInput input:focus {
    border-color: var(--amber);
    box-shadow: none;
}

div[data-testid="stForm"] {
    border: none;
    padding: 0;
}

.stSelectbox div[data-baseweb="select"] > div {
    border-radius: 2px;
    border-color: var(--line);
}

div[data-testid="stExpander"] details {
    border: 1px solid var(--line) !important;
    border-radius: 2px !important;
    background: var(--surface);
}

.footer {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    letter-spacing: 0.1em;
    color: var(--muted);
    border-top: 1px solid var(--line);
    margin-top: 70px;
    padding-top: 16px;
}

@media (prefers-reduced-motion: reduce) {
    * { transition: none !important; animation: none !important; }
}
</style>
""")


# ============================================================
# AUTHOR
# ------------------------------------------------------------
# Edit these four values and the ABOUT text below. Everything the
# reviewer reads about you comes from here.
# ============================================================

AUTHOR = "Jasmine Nguyen 阮氏金銀"
AUTHOR_ROLE = "Self-directed study &middot; Semiconductor engineering"
AUTHOR_CONTACT = "nguyenthikimngan218@gmail.com"
ABOUT_LABEL = "About this project"


# ============================================================
# TEXT HANDLING
# ============================================================

# Inline tags allowed through from the JSON content. Everything else is
# escaped, so a stray "<" in the source can never break the layout.

INLINE_TAGS = ("b", "strong", "i", "em", "u", "code", "sub", "sup", "small")

TABLE_TAGS = ("table", "thead", "tbody", "tfoot", "tr", "th", "td")

BLOCK_TAGS = "h1|h2|h3|h4|h5|h6|p|ul|ol|li|blockquote|div|section"


def esc(value):
    """Plain escape, for anything that should never contain markup."""
    return html.escape(str(value))


def rich(value, tags=INLINE_TAGS):
    """Escape, then re-enable a small whitelist of tags."""
    out = html.escape(str(value))
    for tag in tags:
        for written in (tag, tag.upper()):
            out = out.replace(f"&lt;{written}&gt;", f"<{tag}>")
            out = out.replace(f"&lt;/{written}&gt;", f"</{tag}>")
    return out


def table_html(raw):
    """Render a <table> from the JSON, keeping only structural tags."""

    # drop any attributes so the whitelist below matches
    raw = re.sub(
        r"<\s*(/?)(table|thead|tbody|tfoot|tr|th|td)\b[^>]*>",
        r"<\1\2>",
        raw,
        flags=re.I,
    )
    return f'<div class="table-wrap">{rich(raw, INLINE_TAGS + TABLE_TAGS)}</div>'


def normalize_blocks(text):
    """Put each block-level tag on its own line so content written as one
    long HTML string still parses into headings, list items and paragraphs.

    Also breaks apart numbered sections and labels that were typed inline,
    which is why 3.1 / 3.2 / 3.3 used to run together in one paragraph."""

    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"<\s*br\s*/?\s*>", "\n", text, flags=re.I)

    # newline before every opening block tag
    text = re.sub(rf"(?=<(?:{BLOCK_TAGS})\b)", "\n", text, flags=re.I)

    # newline after every closing block tag
    text = re.sub(rf"(</(?:{BLOCK_TAGS})>)", r"\1\n", text, flags=re.I)

    # newline before "3.1 Title" / "15. Title" written mid-paragraph.
    # Requires a following capital letter so decimals like "0.5 mm" survive.
    text = re.sub(
        r"(?<=[.。!?！？）)])\s+(?=\d{1,2}(?:\.\d{1,2})+\s+[A-Z\u4e00-\u9fff])",
        "\n",
        text,
    )
    text = re.sub(
        r"(?<=[.。!?！？）)])\s+(?=\d{1,2}\.\s+[A-Z\u4e00-\u9fff])",
        "\n",
        text,
    )

    # newline before a short capitalised label that ends in a colon,
    # e.g. "Examples（範例）:" sitting in the middle of a sentence
    text = re.sub(
        r"(?<=[.。!?！？）)])\s+"
        r"(?=[A-Z][A-Za-z]+(?:\s[A-Za-z]+){0,3}"
        r"(?:（[^）]{0,30}）)?\s*[:：])",
        "\n",
        text,
    )

    return text


# ============================================================
# DATA
# ============================================================

def get_json_files():
    files = [f for f in os.listdir() if f.lower().endswith(".json")]

    def module_number(filename):
        match = re.search(r"Module\s+(\d+)", filename, re.IGNORECASE)
        return int(match.group(1)) if match else 999

    files.sort(key=module_number)
    return files


@st.cache_data
def load_json(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)


json_files = get_json_files()

if not json_files:
    st.html(
        '<div class="masthead">'
        '<div class="mast-title">No modules found</div>'
        '<div class="prose">Put your module .json files in the same folder '
        'as app.py, then reload the page.</div></div>'
    )
    st.stop()


# ============================================================
# ABOUT PAGE
# ------------------------------------------------------------
# Rewrite ABOUT_TEXT in your own voice. A reviewer can tell the
# difference between a real motivation and filler.
# ============================================================

ABOUT_LEDE = (
    "I'm Jasmine. I built this site to teach myself semiconductor "
    "engineering from the ground up, and to keep myself honest about "
    "what I actually understand."
)

ABOUT_TEXT = [
    ("Why I built it",
     "Reading a textbook and understanding it are different things. I kept finishing chapters "
     "on wafer test and process flow without being able to explain them to anyone. "
     "I bought an introductory semiconductor textbook and found it is a great deal of "
     "information I could hold onto. I used AI tools to help me sort that material "
     "into eleven modules, then wrote up each topic myself from what I had read. "
     "Building the site is how I study: if I cannot put a topic into my own words, "
     "I do not understand it yet."),

    ("Why the glossary is bilingual",
     "Semiconductor work in Taiwan runs in two languages at once: specifications and "
     "equipment manuals are in English, while the fab floor and the meetings are in Chinese. "
     "I record every term in both. "
     "I know this program is taught in English, but in a lab or a job here I will need both. "
     "Keeping the two side by side means I recognise a term directly in either language, "
     "instead of translating it in my head every time."),

    ("How it works",
     "Content lives in JSON files, one per module, separated from the code that displays it. "
     "Adding a module means adding a file — no changes to the application. Each topic "
     "carries my written notes, a bilingual glossary, key takeaways, short-answer questions "
     "for active recall, and longer discussion prompts I answer from memory before checking."),

    ("What's next",
     "Right now this is a personal study tool. What I have learned so far comes from an "
     "introductory book and from reading online — I have not worked in a Lab, run a "
     "test program, or handled a real wafer, and I know that limits how far self-study can take me. "
     "That gap is why I am applying to the INTENSE Program at NATIONAL YANG MING CHIAO TUNG UNIVERSITY - "
     "International College of Semiconductor Technology.(Spring 2027). Formal coursework "
     "and lab access would let me correct what I have written here and build well past it. "
     "I would like to open the site to the public once the content is solid enough — for other "
     "international students, and for anyone in Taiwan starting from zero the way I did."),
]


@st.cache_data
def collect_stats(filenames):
    topics = terms = questions = 0
    for name in filenames:
        for topic_data in load_json(name).get("topics", []):
            topics += 1
            terms += len(topic_data.get("keywords", []))
            questions += len(topic_data.get("quiz_short", []))
            questions += len(topic_data.get("quiz_long", []))
    return len(filenames), topics, terms, questions


def render_about(filenames):
    modules, topics, terms, questions = collect_stats(tuple(filenames))

    st.html(
        f"""
        <div class="masthead">
            <div class="byline">Written and built by {esc(AUTHOR)}</div>
            <div class="mast-title">A semiconductor study log</div>
            <div class="mast-rule"></div>
        </div>
        <div class="about-lede">{esc(ABOUT_LEDE)}</div>
        """
    )

    stats = [
        (modules, "Modules"),
        (topics, "Topics"),
        (terms, "Glossary terms"),
        (questions, "Self-test questions"),
    ]

    st.html(
        '<div class="statbar">'
        + "".join(
            f'<div><div class="stat-num">{n}</div>'
            f'<div class="stat-cap">{esc(cap)}</div></div>'
            for n, cap in stats
        )
        + "</div>"
    )

    st.html(
        "".join(
            f'<div class="h-minor">{esc(head)}</div>'
            f'<div class="prose">{esc(body)}</div>'
            for head, body in ABOUT_TEXT
        )
    )

    st.html(
        f'<div class="footer">'
        f'{esc(AUTHOR).upper()} &middot; PYTHON + STREAMLIT &middot; '
        f'CONTENT WRITTEN BY HAND &middot; {esc(AUTHOR_CONTACT)}</div>'
    )


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.html(
    '<div class="sb-title">Semiconductor / Study Log</div>'
    f'<div class="sb-author">{esc(AUTHOR)}</div>'
    f'<div class="sb-role">{AUTHOR_ROLE}</div>'
)

module_names = [f[:-5] for f in json_files]

view = st.sidebar.selectbox("Section", [ABOUT_LABEL] + module_names)

if view == ABOUT_LABEL:
    render_about(json_files)
    st.stop()

selected_module = view
module_index = module_names.index(selected_module)
selected_file = json_files[module_index]

data = load_json(selected_file)
topics = data.get("topics", [])

if not topics:
    st.html(
        '<div class="masthead">'
        '<div class="mast-title">Empty module</div>'
        '<div class="prose">This file has no "topics" entry.</div></div>'
    )
    st.stop()

topic_names = [t["title"] for t in topics]
selected_topic = st.sidebar.selectbox("Topic", topic_names)
topic_index = topic_names.index(selected_topic)
topic = topics[topic_index]


# Signature element: a die map instead of a progress bar

dies = "".join(
    '<div class="die die--done"></div>' if i < topic_index
    else '<div class="die die--now"></div>' if i == topic_index
    else '<div class="die"></div>'
    for i in range(len(topics))
)

st.sidebar.html(
    f'<div class="diemap">{dies}</div>'
    f'<div class="diemap-cap">TOPIC {topic_index + 1:02d} / {len(topics):02d}</div>'
)


# ============================================================
# MASTHEAD
# ============================================================

st.html(
    f"""
    <div class="masthead">
        <div class="mast-eyebrow">
            Module {module_index + 1:02d}
            &nbsp;&middot;&nbsp; {esc(data.get("module_name", selected_module))}
            &nbsp;&middot;&nbsp; Topic {topic_index + 1:02d}
        </div>
        <div class="mast-title">{esc(topic["title"])}</div>
        <div class="mast-rule"></div>
    </div>
    """
)


# ============================================================
# CONTENT
# ============================================================

BULLET_CHARS = ("\uf0b7", "\u2022", "\u25cf", "\u00b7", "-", "*")

HEADING_RE = re.compile(r"^<h([1-6])[^>]*>(.*?)</h\1>$", re.I | re.S)
LI_RE = re.compile(r"^<li[^>]*>(.*?)(?:</li>)?$", re.I | re.S)
STRAY_RE = re.compile(rf"^</?(?:{BLOCK_TAGS})[^>]*>$", re.I)
P_OPEN_RE = re.compile(r"^<p[^>]*>", re.I)
P_CLOSE_RE = re.compile(r"</p>$", re.I)
TABLE_RE = re.compile(r"(<table\b.*?</table>)", re.I | re.S)

# "3.1 Detect Defective Dies（...）: rest of the paragraph"
NUM_SECTION_RE = re.compile(
    r"^(\d{1,2}(?:\.\d{1,2})*)\.?\s+(.{2,110}?)\s*[:：]\s*(.*)$", re.S
)

# "15. CP vs Final Testing (FT)（...）" with no colon
NUM_TITLE_RE = re.compile(r"^(\d{1,2}(?:\.\d{1,2})*)\.\s+(.{2,110})$")


def bullet_html(text):
    return (
        '<div class="bullet">'
        '<div class="bullet-mark">&mdash;</div>'
        f'<div>{rich(text)}</div>'
        '</div>'
    )


def section_html(number, title):
    depth = number.count(".") + 1
    css = "h-sec h-sec--major" if depth == 1 else "h-sec"
    return (
        f'<div class="{css}">'
        f'<div class="h-sec-idx">{esc(number)}</div>'
        f'<div>{rich(title)}</div>'
        f'</div>'
    )


def build_content(content):
    """Return the whole topic body as a single HTML string.

    Emitting one element per line would let Streamlit insert its own gap
    between every paragraph, which stacks on top of the CSS margins and
    makes the text feel airy. One block keeps spacing under CSS control."""

    parts = []

    # Tables are pulled out whole before line-by-line parsing, otherwise
    # the newline pass would tear their rows apart.
    for segment in TABLE_RE.split(content):

        if TABLE_RE.fullmatch(segment or ""):
            parts.append(table_html(segment))
            continue

        parts.extend(build_lines(segment or ""))

    return f'<div class="content">{"".join(parts)}</div>'


def build_lines(content):
    lines = [ln.strip() for ln in normalize_blocks(content).split("\n") if ln.strip()]

    parts = []
    buffer = []

    def flush():
        if buffer:
            parts.append(f'<div class="prose">{rich(" ".join(buffer))}</div>')
            buffer.clear()

    for line in lines:

        # <h1>-<h6> from the JSON
        heading = HEADING_RE.match(line)
        if heading:
            flush()
            level = int(heading.group(1))
            css = "h-major" if level <= 3 else "h-minor"
            parts.append(f'<div class="{css}">{rich(heading.group(2).strip())}</div>')
            continue

        # <li> from the JSON
        list_item = LI_RE.match(line)
        if list_item:
            flush()
            parts.append(bullet_html(list_item.group(1).strip()))
            continue

        # a lone <ul>, </p>, <div> and so on -- drop it
        if STRAY_RE.match(line):
            flush()
            continue

        # unwrap a paragraph written as <p>...</p>
        line = P_CLOSE_RE.sub("", P_OPEN_RE.sub("", line)).strip()
        if not line:
            continue

        # "3.1 Detect Defective Dies（...）: body text"
        section = NUM_SECTION_RE.match(line)
        if section and "\n" not in section.group(2):
            flush()
            parts.append(section_html(section.group(1), section.group(2).strip()))
            rest = section.group(3).strip()
            if rest:
                buffer.append(rest)
            continue

        # "15. CP vs Final Testing (FT)（...）"
        title = NUM_TITLE_RE.match(line)
        if title:
            flush()
            parts.append(section_html(title.group(1), title.group(2).strip()))
            continue

        # plain-text bullet
        if line.startswith(BULLET_CHARS) and len(line) > 1:
            flush()
            parts.append(bullet_html(line[1:].strip()))
            continue

        # process / signal path
        if "→" in line and len(line) < 200:
            flush()
            parts.append(f'<div class="flow">{esc(line)}</div>')
            continue

        # short label line such as "In simple terms:"
        if line.endswith(":") and len(line) < 80:
            flush()
            parts.append(f'<div class="sublabel">{rich(line)}</div>')
            continue

        buffer.append(line)

    flush()

    return parts


st.html('<div class="eyebrow">Content</div>')
st.html(build_content(topic.get("content", "")))


# ============================================================
# GLOSSARY
# ============================================================

keywords = topic.get("keywords", [])

if keywords:
    st.html('<div class="eyebrow">Terminology</div>')

    def glossary_table(items):
        rows = "".join(
            f'<tr><td class="g-en">{esc(k.get("english", ""))}</td>'
            f'<td class="g-zh">{esc(k.get("chinese", ""))}</td></tr>'
            for k in items
        )
        return f'<table class="glossary">{rows}</table>'

    col_a, col_b = st.columns(2, gap="large")
    with col_a:
        st.html(glossary_table(keywords[::2]))
    with col_b:
        st.html(glossary_table(keywords[1::2]))


# ============================================================
# TAKEAWAYS
# ============================================================

summary = topic.get("summary", [])

if summary:
    st.html('<div class="eyebrow">Key takeaways</div>')
    st.html(
        "".join(
            f'<div class="take">'
            f'<div class="take-idx">{i + 1:02d}</div>'
            f'<div class="take-text">{rich(item)}</div>'
            f'</div>'
            for i, item in enumerate(summary)
        )
    )


# ============================================================
# QUICK CHECK
# ============================================================

questions = topic.get("quiz_short", [])

if questions:
    st.html('<div class="eyebrow">Quick check</div>')

    state_key = f"quiz::{selected_file}::{topic_index}"
    if state_key not in st.session_state:
        st.session_state[state_key] = {}

    results = st.session_state[state_key]

    for i, q in enumerate(questions):

        st.html(
            f'<div class="q-num">QUESTION {i + 1:02d}</div>'
            f'<div class="q-text">{rich(q["question"])}</div>'
        )

        with st.form(key=f"form::{selected_file}::{topic_index}::{i}"):
            answer = st.text_input(
                "Your answer",
                key=f"input::{selected_file}::{topic_index}::{i}",
                label_visibility="collapsed",
                placeholder="Type your answer",
            )
            submitted = st.form_submit_button("Check answer")

        if submitted:
            # overwrite, never accumulate -- resubmitting cannot inflate the score
            results[i] = answer.strip().lower() == str(q["answer"]).strip().lower()

        if i in results:
            if results[i]:
                st.html(
                    f'<div class="verdict verdict--ok">'
                    f'CORRECT &middot; {esc(q["answer"])}</div>'
                )
            else:
                st.html(
                    f'<div class="verdict verdict--no">'
                    f'NOT YET &middot; answer: {esc(q["answer"])}</div>'
                )

    score = sum(1 for v in results.values() if v)
    answered = len(results)

    score_dies = "".join(
        f'<div class="die {"die--done" if results.get(i) else ""}"></div>'
        for i in range(len(questions))
    )

    st.html(
        f'<div style="margin-top:38px;border-top:1px solid var(--line);'
        f'padding-top:16px;">'
        f'<div class="diemap">{score_dies}</div>'
        f'<div class="diemap-cap">{score:02d} / {len(questions):02d} CORRECT '
        f'&middot; {answered:02d} ANSWERED</div></div>'
    )

    if answered:
        if st.button("Start over", key=f"reset::{selected_file}::{topic_index}"):
            st.session_state[state_key] = {}
            st.rerun()


# ============================================================
# DISCUSSION
# ============================================================

long_questions = topic.get("quiz_long", [])

if long_questions:
    st.html('<div class="eyebrow">Discussion</div>')
    st.html(
        '<div class="prose">Work through your own answer first, '
        'then open the note to compare.</div>'
    )

    for q in long_questions:
        with st.expander(q["question"]):
            st.html(f'<div class="prose">{rich(q["answer"])}</div>')


# ============================================================
# FOOTER
# ============================================================

st.html(
    f'<div class="footer">{esc(AUTHOR).upper()} &middot; SEMICONDUCTOR STUDY LOG '
    f'&middot; MODULE {module_index + 1:02d} &middot; {len(topics):02d} TOPICS '
    f'&middot; {esc(AUTHOR_CONTACT)}</div>'
)