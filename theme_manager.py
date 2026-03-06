"""
theme_manager.py — Dark / Light Theme System
=============================================
Provides the complete CSS for both themes, a session-state toggle,
and the header theme-switch renderer for the Content Studio.
"""

import streamlit as st


# ---------------------------------------------------------------------------
# Theme initialisation
# ---------------------------------------------------------------------------

def init_theme():
    """Initialise the theme in session state if not set."""
    if "theme" not in st.session_state:
        st.session_state.theme = "dark"


def toggle_theme():
    """Flip the current theme between dark and light."""
    st.session_state.theme = (
        "light" if st.session_state.theme == "dark" else "dark"
    )


def is_dark() -> bool:
    """Return True when the active theme is dark."""
    return st.session_state.get("theme", "dark") == "dark"


# ---------------------------------------------------------------------------
# CSS — shared tokens + theme-specific overrides
# ---------------------------------------------------------------------------

_SHARED_CSS = """
/* ── Google Fonts ───────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

/* ── Reset & base ───────────────────────────────────── */
html, body, [class*="st-"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}
h1, h2, h3, h4, h5, h6, p, span, label, div {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

/* Hide default Streamlit chrome */
#MainMenu, header, footer { visibility: hidden; }
.block-container { padding-top: 1rem !important; max-width: 1260px; }
div[data-testid="stToolbar"] { display: none; }

/* ── Smooth transitions ────────────────────────────── */
.result-card, .stButton > button, .input-panel, .output-panel,
.chip, .platform-preview, .history-entry {
    transition: all 0.25s cubic-bezier(.4,0,.2,1);
}

/* ── Hero header ────────────────────────────────────── */
.hero {
    background: linear-gradient(135deg, #1e1b4b 0%, #312e81 30%, #4f46e5 65%, #7c3aed 100%);
    padding: 2.2rem 2.5rem 1.8rem;
    border-radius: 18px;
    margin-bottom: 0.6rem;
    position: relative;
    overflow: hidden;
    box-shadow: 0 8px 40px rgba(79,70,229,0.30);
}
.hero::before {
    content: '';
    position: absolute;
    top: -60%; right: -15%;
    width: 440px; height: 440px;
    background: radial-gradient(circle, rgba(167,139,250,0.35) 0%, transparent 70%);
    border-radius: 50%;
    pointer-events: none;
}
.hero::after {
    content: '';
    position: absolute;
    bottom: -40%; left: -10%;
    width: 320px; height: 320px;
    background: radial-gradient(circle, rgba(99,102,241,0.20) 0%, transparent 70%);
    border-radius: 50%;
    pointer-events: none;
}
.hero-content { position: relative; z-index: 2; }
.hero h1 {
    color: #fff;
    font-size: 1.85rem;
    font-weight: 800;
    letter-spacing: -0.6px;
    margin: 0 0 0.3rem;
    line-height: 1.2;
}
.hero p {
    color: #c7d2fe;
    font-size: 0.95rem;
    margin: 0;
    font-weight: 400;
    line-height: 1.5;
}
.hero-badges {
    display: flex;
    gap: 10px;
    margin-top: 1rem;
    flex-wrap: wrap;
}
.hero-badge {
    background: rgba(255,255,255,0.12);
    backdrop-filter: blur(6px);
    padding: 5px 14px;
    border-radius: 20px;
    color: #e0e7ff;
    font-size: 0.75rem;
    font-weight: 600;
    border: 1px solid rgba(255,255,255,0.15);
    letter-spacing: 0.2px;
}

/* ── Theme toggle button ────────────────────────────── */
.theme-toggle-wrap {
    position: absolute;
    top: 1.5rem;
    right: 1.8rem;
    z-index: 10;
}

/* ── Pill tab bar ───────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    gap: 6px;
    padding: 5px 6px;
    border-radius: 14px;
    margin-bottom: 0.3rem;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 10px;
    padding: 10px 22px;
    font-weight: 600;
    font-size: 0.84rem;
    letter-spacing: 0.1px;
    transition: all 0.2s ease;
    border: none;
}

/* ── Primary buttons ────────────────────────────────── */
.stButton > button {
    border-radius: 10px;
    font-weight: 600;
    font-size: 0.85rem;
    padding: 0.6rem 1.6rem;
    border: none;
    letter-spacing: 0.1px;
}
.stButton > button[kind="primary"],
.stButton > button:first-child {
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    color: white !important;
    box-shadow: 0 3px 12px rgba(99,102,241,0.35);
}
.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 20px rgba(99,102,241,0.40);
}

/* ── Hashtag chips ──────────────────────────────────── */
.chip {
    display: inline-block;
    padding: 5px 13px;
    border-radius: 20px;
    margin: 3px 4px;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.1px;
}

/* ── Section label  ─────────────────────────────────── */
.section-label {
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.8px;
    margin-bottom: 0.4rem;
}

/* ── Character counter ──────────────────────────────── */
.char-counter {
    font-size: 0.78rem;
    font-weight: 600;
    margin-top: 2px;
}

/* ── Tooltip icon ───────────────────────────────────── */
.tooltip-icon {
    display: inline-block;
    width: 16px; height: 16px;
    border-radius: 50%;
    text-align: center;
    font-size: 11px;
    line-height: 16px;
    cursor: help;
    margin-left: 4px;
    font-weight: 700;
    vertical-align: middle;
}

/* ── Platform preview card ──────────────────────────── */
.platform-preview {
    border-radius: 14px;
    padding: 1.2rem 1.4rem;
    margin-top: 0.8rem;
}
.platform-preview .preview-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 0.7rem;
}
.platform-preview .avatar {
    width: 36px; height: 36px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
    font-weight: 700;
}
.platform-preview .preview-name {
    font-weight: 700;
    font-size: 0.88rem;
}
.platform-preview .preview-body {
    font-size: 0.87rem;
    line-height: 1.6;
    white-space: pre-wrap;
}
.platform-preview .preview-engagement {
    display: flex;
    gap: 18px;
    margin-top: 0.8rem;
    font-size: 0.78rem;
    font-weight: 500;
    opacity: 0.7;
}

/* ── Footer ─────────────────────────────────────────── */
.app-footer {
    text-align: center;
    font-size: 0.75rem;
    padding: 1.5rem 0 0.5rem;
    opacity: 0.5;
    font-weight: 500;
}

/* ── Download button override ───────────────────────── */
.stDownloadButton > button {
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
}

/* ── Keyframe: card entrance ────────────────────────── */
@keyframes cardSlideIn {
    from { opacity: 0; transform: translateY(12px); }
    to   { opacity: 1; transform: translateY(0); }
}
.result-card {
    animation: cardSlideIn 0.35s ease-out forwards;
}
"""

_DARK_CSS = """
/* ── Dark mode overrides ────────────────────────────── */
.stApp {
    background-color: #0f0f14 !important;
    color: #e2e8f0 !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: #1a1a24;
    border: 1px solid #2d2d3d;
}
.stTabs [data-baseweb="tab"] {
    color: #94a3b8;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    color: #fff !important;
    box-shadow: 0 2px 10px rgba(99,102,241,0.35);
}

/* Cards */
.result-card {
    background: #1a1a24;
    border: 1px solid #2d2d3d;
    border-radius: 14px;
    padding: 1.4rem 1.5rem;
    margin-bottom: 1rem;
    box-shadow: 0 2px 12px rgba(0,0,0,0.25);
}
.result-card:hover {
    border-color: #6366f1;
    box-shadow: 0 4px 24px rgba(99,102,241,0.18);
    transform: translateY(-2px);
}
.result-card h4 {
    color: #e0e7ff;
    font-weight: 700;
    font-size: 0.95rem;
    margin-bottom: 0.5rem;
}
.result-card p, .result-card li {
    color: #cbd5e1;
    line-height: 1.65;
    font-size: 0.88rem;
}

/* Input panel */
.input-panel {
    background: #1a1a24;
    border: 1px solid #2d2d3d;
    border-radius: 14px;
    padding: 1.5rem;
}

/* Section label */
.section-label { color: #818cf8; }

/* Chips */
.chip {
    background: linear-gradient(135deg, #2e1065, #3730a3);
    color: #c4b5fd;
    border: 1px solid #4338ca;
}

/* Tooltips */
.tooltip-icon {
    background: #2d2d3d;
    color: #818cf8;
    border: 1px solid #3d3d50;
}

/* Platform preview */
.platform-preview {
    background: #111118;
    border: 1px solid #2d2d3d;
}
.platform-preview .avatar {
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    color: #fff;
}
.platform-preview .preview-name { color: #e0e7ff; }
.platform-preview .preview-body { color: #cbd5e1; }

/* History */
.history-entry {
    background: #111118;
    border-left: 3px solid #6366f1;
    padding: 0.9rem 1.1rem;
    border-radius: 0 10px 10px 0;
    margin-bottom: 0.6rem;
    cursor: pointer;
}
.history-entry:hover {
    background: #1a1a24;
    border-left-color: #a78bfa;
}
.history-entry strong { color: #e0e7ff; }
.history-entry span { color: #94a3b8; font-size: 0.8rem; }

/* API warning */
.api-warning {
    background: rgba(245,158,11,0.12);
    border: 1px solid rgba(245,158,11,0.35);
    padding: 0.9rem 1.3rem;
    border-radius: 12px;
    color: #fbbf24;
    font-weight: 500;
    margin-bottom: 0.8rem;
    font-size: 0.88rem;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #111118 !important;
    border-right: 1px solid #2d2d3d;
}
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #c7d2fe !important;
}

/* Streamlit input overrides for dark */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div {
    background-color: #111118 !important;
    border: 1px solid #2d2d3d !important;
    color: #e2e8f0 !important;
    border-radius: 10px !important;
}

/* Footer */
.app-footer { color: #475569; }

/* Dataframe */
.stDataFrame { border-radius: 12px; overflow: hidden; }
"""

_LIGHT_CSS = """
/* ── Light mode overrides ───────────────────────────── */
.stApp {
    background-color: #f1f5f9 !important;
    color: #1e293b !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: #fff;
    border: 1px solid #e2e8f0;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}
.stTabs [data-baseweb="tab"] {
    color: #64748b;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    color: #fff !important;
    box-shadow: 0 2px 10px rgba(99,102,241,0.30);
}

/* Cards */
.result-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 1.4rem 1.5rem;
    margin-bottom: 1rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04), 0 4px 16px rgba(0,0,0,0.03);
}
.result-card:hover {
    border-color: #a5b4fc;
    box-shadow: 0 4px 24px rgba(99,102,241,0.12);
    transform: translateY(-2px);
}
.result-card h4 {
    color: #1e1b4b;
    font-weight: 700;
    font-size: 0.95rem;
    margin-bottom: 0.5rem;
}
.result-card p, .result-card li {
    color: #374151;
    line-height: 1.65;
    font-size: 0.88rem;
}

/* Input panel */
.input-panel {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 1.5rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}

/* Section label */
.section-label { color: #6366f1; }

/* Chips */
.chip {
    background: linear-gradient(135deg, #eef2ff, #e0e7ff);
    color: #3730a3;
    border: 1px solid #c7d2fe;
}

/* Tooltips */
.tooltip-icon {
    background: #eef2ff;
    color: #6366f1;
    border: 1px solid #c7d2fe;
}

/* Platform preview */
.platform-preview {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
}
.platform-preview .avatar {
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    color: #fff;
}
.platform-preview .preview-name { color: #1e293b; }
.platform-preview .preview-body { color: #334155; }

/* History */
.history-entry {
    background: #f8fafc;
    border-left: 3px solid #6366f1;
    padding: 0.9rem 1.1rem;
    border-radius: 0 10px 10px 0;
    margin-bottom: 0.6rem;
    cursor: pointer;
}
.history-entry:hover {
    background: #eef2ff;
    border-left-color: #8b5cf6;
}
.history-entry strong { color: #1e1b4b; }
.history-entry span { color: #64748b; font-size: 0.8rem; }

/* API warning */
.api-warning {
    background: linear-gradient(135deg, #fefce8, #fef3c7);
    border: 1px solid #f59e0b;
    padding: 0.9rem 1.3rem;
    border-radius: 12px;
    color: #92400e;
    font-weight: 500;
    margin-bottom: 0.8rem;
    font-size: 0.88rem;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #f8fafc 0%, #eef2ff 100%) !important;
    border-right: 1px solid #e0e7ff;
}
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #312e81 !important;
}

/* Inputs */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div {
    background-color: #f8fafc !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 10px !important;
}

/* Footer */
.app-footer { color: #94a3b8; }

/* Dataframe */
.stDataFrame { border-radius: 12px; overflow: hidden; }
"""


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def inject_theme_css():
    """Inject the full theme CSS into the Streamlit page."""
    init_theme()
    theme_css = _DARK_CSS if is_dark() else _LIGHT_CSS
    st.markdown(f"<style>{_SHARED_CSS}\n{theme_css}</style>", unsafe_allow_html=True)


def render_theme_toggle():
    """
    Render a theme toggle button. Must be called inside a column
    or container where the button should appear.
    """
    icon = "☀️" if is_dark() else "🌙"
    label = "Light Mode" if is_dark() else "Dark Mode"
    if st.button(f"{icon} {label}", key="theme_toggle_btn"):
        toggle_theme()
        st.rerun()
