"""
theme_system.py — Design System
================================
Dynamic CSS variable architectural pattern for themes.
Strict contrast adherence based on #F5F6FA / #0F1117 tokens.
"""

import streamlit as st

def init_theme():
    if "theme" not in st.session_state:
        st.session_state.theme = "light"
    if "sidebar_expanded" not in st.session_state:
        st.session_state.sidebar_expanded = True

def toggle_theme():
    st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"

def is_dark() -> bool:
    return st.session_state.get("theme", "light") == "dark"


_VARS_LIGHT = """
:root {
    --bg-color: #F5F6FA;
    --card-bg: #FFFFFF;
    --primary: #6C5CE7;
    
    /* Text */
    --text-heading: #1F2937;
    --text-body: #374151;
    --text-label: #4B5563;
    
    /* Inputs */
    --input-bg: #FFFFFF;
    --input-text: #111827;
    --input-placeholder: #9CA3AF;
    
    /* Borders */
    --border-color: #E5E7EB;

    /* Components */
    --btn-prim-bg: linear-gradient(135deg, #6C5CE7, #8B7CFF);
    --btn-prim-text: #FFFFFF;
    
    --btn-sec-bg: transparent;
    --btn-sec-text: #6B7280;
    --btn-sec-hover: #F9FAFB;
    
    --sb-hover-bg: #F9FAFB;
    --sb-hover-text: #6C5CE7;
    
    --tag-bg: linear-gradient(135deg, #EEF2FF, #E0E7FF);
    --tag-border: #C7D2FE;
    --tag-text: #3730A3;
}
"""

_VARS_DARK = """
:root {
    --bg-color: #0F1117;
    --card-bg: #1A1D26;
    --primary: #8B7CFF;
    
    /* Text */
    --text-heading: #FFFFFF;
    --text-body: #D1D5DB;
    --text-label: #A1A1AA;
    
    /* Inputs */
    --input-bg: #11131A;
    --input-text: #F9FAFB;
    --input-placeholder: #6B7280;
    
    /* Borders */
    --border-color: #2A2E3A;

    /* Components */
    --btn-prim-bg: linear-gradient(135deg, #6C5CE7, #8B7CFF);
    --btn-prim-text: #FFFFFF;
    
    --btn-sec-bg: #1A1D26;
    --btn-sec-text: #D1D5DB;
    --btn-sec-hover: #11131A;
    
    --sb-hover-bg: #11131A;
    --sb-hover-text: #FFFFFF;
    
    --tag-bg: linear-gradient(135deg, #1A0F50, #271768);
    --tag-border: #362498;
    --tag-text: #C4B5FD;
}
"""


def get_base_css(sidebar_width: int) -> str:
    return f"""
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

*, html, body, [class*="st-"] {{
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}}
html {{ scroll-behavior: smooth !important; }}

/* Globals */
.stApp {{ background: var(--bg-color) !important; color: var(--text-body) !important; }}
#MainMenu, footer, div[data-testid="stToolbar"] {{ display: none !important; }}
header[data-testid="stHeader"] {{ background: transparent !important; height: 10px !important; }}

/* Typography Rules */
h1, h2, h3, h4, h5, h6, .th-content h1, .r-card h4, .sb-logo-name {{
    color: var(--text-heading) !important;
}}
p, .th-content p, .r-card p {{
    color: var(--text-body) !important;
}}
label, .stTextInput label, .stSelectbox label, .stTextArea label {{
    color: var(--text-label) !important;
}}

/* ── Layout (32px padding) ──────────────────────── */
.block-container {{
    padding: 32px 32px 40px !important;
    max-width: 1440px !important;
}}

/* ── Sidebar — Dynamic Width ────────────────────── */
section[data-testid="stSidebar"] {{
    background: var(--card-bg) !important;
    border-right: 1px solid var(--border-color) !important;
    min-width: {sidebar_width}px !important; max-width: {sidebar_width}px !important;
    width: {sidebar_width}px !important;
    transform: none !important;
    transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    position: relative !important;
    visibility: visible !important;
    display: flex !important;
}}
section[data-testid="stSidebar"] > div:first-child {{
    padding: 24px { '16px' if sidebar_width > 100 else '10px' };
    width: {sidebar_width}px !important;
    overflow-x: hidden !important;
}}
button[data-testid="stSidebarCollapseButton"],
button[data-testid="stSidebarCollapse"],
div[data-testid="collapsedControl"],
button[data-testid="collapsedControl"],
[data-testid="collapsedControl"] *,
div[data-testid="stSidebarNavSeparator"],
[data-testid="stSidebarNav"] button,
header[data-testid="stHeader"],
.stApp > header,
[data-testid="stDecoration"],
span.material-symbols-rounded,
button[kind="header"] {{
    position: absolute !important;
    top: -9999px !important;
    left: -9999px !important;
    width: 0 !important;
    height: 0 !important;
    overflow: hidden !important;
    visibility: hidden !important;
    opacity: 0 !important;
    pointer-events: none !important;
}}

/* Sidebar logo */
.sb-logo {{
    display: flex; align-items: center; gap: 12px;
    padding: 0 4px 20px; margin-bottom: 20px;
    border-bottom: 1px solid var(--border-color);
    justify-content: { 'flex-start' if sidebar_width > 100 else 'center' };
}}
.sb-logo-icon {{
    width: 38px; height: 38px; border-radius: 10px;
    background: var(--btn-prim-bg);
    display: flex; align-items: center; justify-content: center;
    font-size: 18px; flex-shrink: 0;
}}
.sb-logo-name {{ font-weight: 700; font-size: 0.98rem; letter-spacing: -0.4px; white-space: nowrap; }}
.sb-logo-sub  {{ font-size: 0.65rem; opacity: 0.65; font-weight: 400; white-space: nowrap; color: var(--text-label); }}

/* Sidebar navigation and toggle buttons */
[data-testid="stSidebar"] div[data-testid="stButton"] button {{
    border: none !important; background: transparent !important;
    color: var(--text-label) !important; box-shadow: none !important;
    border-radius: 10px !important;
    justify-content: { 'flex-start' if sidebar_width > 100 else 'center' } !important;
    font-weight: 500 !important;
    font-size: { '0.90rem' if sidebar_width > 100 else '1.2rem' } !important;
    padding: { '10px 16px' if sidebar_width > 100 else '12px 0' } !important;
    transition: all 0.2s ease !important;
    margin-bottom: 4px !important;
}}
[data-testid="stSidebar"] div[data-testid="stButton"] button:hover {{
    background: var(--sb-hover-bg) !important; color: var(--text-heading) !important;
}}
[data-testid="stSidebar"] div[data-testid="stButton"] button[kind="primary"] {{
    background: linear-gradient(135deg, #6C5CE7, #8B7CFF) !important; color: #FFFFFF !important;
    font-weight: 600 !important; box-shadow: 0 4px 16px rgba(108, 92, 231, 0.25) !important;
}}

/* Active, Focus, and Focus-Visible overrides to destroy Streamlit's default red */
[data-testid="stSidebar"] div[data-testid="stButton"] button:active,
[data-testid="stSidebar"] div[data-testid="stButton"] button:focus:active {{
    background: linear-gradient(135deg, #6C5CE7, #8B7CFF) !important;
    color: #FFFFFF !important;
    border-color: transparent !important;
    box-shadow: none !important;
}}

[data-testid="stSidebar"] div[data-testid="stButton"] button:focus,
[data-testid="stSidebar"] div[data-testid="stButton"] button:focus-visible {{
    box-shadow: 0 0 0 2px rgba(108,92,231,0.35) !important;
    border-color: transparent !important;
    color: var(--text-heading) !important;
}}

[data-testid="stSidebar"] div[data-testid="stButton"] button[kind="primary"]:focus,
[data-testid="stSidebar"] div[data-testid="stButton"] button[kind="primary"]:focus-visible {{
    color: #FFFFFF !important;
}}

.sb-sec {{
    font-size: 0.64rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: 1.5px; padding: 18px 4px 6px; opacity: 0.50;
    white-space: nowrap; color: var(--text-label);
}}
.hist {{
    padding: 10px 12px; border-radius: 9px; margin-bottom: 5px; font-size: 0.82rem;
    transition: all 0.15s ease; cursor: default; white-space: nowrap; overflow: hidden;
    background: var(--bg-color); border: 1px solid var(--border-color);
}}
.hist:hover {{ border-color: var(--primary); }}
.hist strong {{ display: block; font-size: 0.84rem; margin-bottom: 1px; text-overflow: ellipsis; overflow: hidden; color: var(--text-heading); }}
.hist span   {{ font-size: 0.70rem; color: var(--text-label); text-overflow: ellipsis; overflow: hidden; }}

/* ── Top Header ─────────────────────────────────── */
.top-header {{
    display: flex; align-items: flex-start;
    margin-bottom: 32px; padding-bottom: 24px;
    border-bottom: 1px solid var(--border-color); gap: 20px;
}}
.th-hamburger button {{
    width: 44px; height: 44px; border-radius: 12px !important;
    background: var(--bg-color) !important; color: var(--primary) !important;
    font-size: 18px; border: 1px solid var(--border-color) !important;
    transition: all 0.2s ease; cursor: pointer;
}}
.th-hamburger button:hover {{ background: var(--btn-sec-hover) !important; border-color: var(--primary) !important; }}
.th-content h1 {{
    font-size: 1.6rem; font-weight: 800; letter-spacing: -0.6px;
    margin: 0 0 6px; line-height: 1.2; padding: 0; border: none;
}}
.th-content p {{
    font-size: 0.90rem; margin: 0; font-weight: 400; opacity: 1; color: var(--text-body);
}}
.th-theme button {{
    width: 44px; height: 44px; border-radius: 12px !important; font-size: 18px;
    background: var(--bg-color) !important; border: 1px solid var(--border-color) !important; color: var(--text-label) !important;
    transition: all 0.2s ease;
}}
.th-theme button:hover {{ background: var(--btn-sec-hover) !important; color: var(--text-heading) !important; }}

/* ── Workflow guide ─────────────────────────────── */
.wf-steps {{
    display: flex; gap: 12px; padding: 0 0 16px; margin-bottom: 8px;
    font-size: 0.8rem; font-weight: 500;
}}
.wf-step {{
    display: flex; align-items: center; gap: 8px;
    padding: 8px 16px; border-radius: 24px;
    background: var(--btn-sec-bg); color: var(--text-label) !important;
    text-decoration: none !important; transition: all 0.2s ease;
}}
.wf-step:hover {{
    background: var(--btn-sec-hover); cursor: pointer; color: var(--text-heading) !important;
}}
.wf-step.active-step {{
    background: var(--btn-prim-bg); color: #FFFFFF !important;
    border: none; box-shadow: 0 4px 12px rgba(108, 92, 231, 0.2);
}}
.wf-step .wf-dot {{
    width: 20px; height: 20px; border-radius: 50%;
    display: inline-flex; align-items: center; justify-content: center;
    font-size: 11px; font-weight: 700; background: var(--tag-bg); color: var(--primary);
    transition: all 0.2s ease;
}}
.wf-step:hover .wf-dot {{
    background: var(--primary); color: #fff;
}}
.wf-step.active-step .wf-dot {{
    background: rgba(255,255,255,0.25); color: #FFF;
}}

/* ── Input card (native st.container borders) ──────────────────────── */
div[data-testid="stVerticalBlockBorderWrapper"] {{
    background: var(--card-bg) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 16px !important;
    padding: 24px 28px !important;
    box-shadow: 0 4px 16px rgba(0,0,0,0.03) !important;
    margin-bottom: 20px !important;
}}
.in-card-title {{
    font-size: 0.82rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: 1.4px; margin-bottom: 20px; color: var(--primary);
}}

/* Quick Idea overrides */
div[data-testid="stVerticalBlockBorderWrapper"]:has(.qi-tip) {{ padding: 20px 24px 16px !important; margin-bottom: 16px !important; }}
div[data-testid="stVerticalBlockBorderWrapper"]:has(.qi-tip) .stTextInput > div > div > input {{
    height: 56px !important; font-size: 0.98rem !important;
}}
.qi-tip {{ font-size: 0.76rem; color: var(--text-label); opacity: 0.85; margin: 4px 0 0; padding-left: 2px; }}

/* ── Forms ──────────────────────────────────────── */
div[data-testid="stHorizontalBlock"] {{ gap: 16px; }}
.stTextInput, .stSelectbox, .stTextArea {{ margin-bottom: 4px; }}

.stTextInput > div > div > input,
.stTextArea > div > div > textarea {{
    background: var(--input-bg) !important; border: 1px solid var(--border-color) !important;
    color: var(--input-text) !important;
    border-radius: 10px !important; padding: 12px 14px !important;
}}
.stTextInput > div > div > input::placeholder,
.stTextArea > div > div > textarea::placeholder {{
    color: var(--input-placeholder) !important; opacity: 1 !important; font-weight: 400;
}}
.stTextInput > div > div > input:focus, .stTextArea > div > div > textarea:focus {{
    border-color: var(--primary) !important; box-shadow: 0 0 0 2px rgba(108, 92, 231, 0.12) !important;
}}
.stSelectbox > div > div {{ padding: 2px !important; border-radius: 10px !important; background: var(--input-bg) !important; border: 1px solid var(--border-color) !important; color: var(--input-text) !important; }}

/* ── Buttons ────────────────────────────────────── */
.stButton > button {{
    border-radius: 10px; font-weight: 600; font-size: 0.88rem;
    height: 48px; transition: all 0.2s ease; width: 100%;
}}
div[data-testid="stHorizontalBlock"] > div:first-child .stButton > button {{
    background: var(--btn-prim-bg) !important;
    color: var(--btn-prim-text) !important; border: none !important;
    box-shadow: 0 4px 18px rgba(108, 92, 231, 0.28);
}}
div[data-testid="stHorizontalBlock"] > div:first-child .stButton > button:hover {{ transform: translateY(-1px); box-shadow: 0 6px 24px rgba(108, 92, 231, 0.38); }}

/* Outline button */
div[data-testid="stHorizontalBlock"] > div:nth-child(2) .stButton > button {{
    background: var(--btn-sec-bg) !important; color: var(--btn-sec-text) !important; border: 1px solid var(--btn-sec-border) !important;
}}
div[data-testid="stHorizontalBlock"] > div:nth-child(2) .stButton > button:hover {{ 
    transform: translateY(-1px); background: var(--btn-sec-hover) !important; color: var(--text-heading) !important; border-color: var(--primary) !important; 
}}

/* ── Result cards ───────────────────────────────── */
.r-card {{ 
    background: var(--card-bg); border: 1px solid var(--border-color);
    border-radius: 14px; padding: 22px 26px; margin-bottom: 16px; 
    transition: all 0.2s ease;
}}
@keyframes cardIn {{ from {{ opacity: 0; transform: translateY(10px); }} to {{ opacity: 1; transform: translateY(0); }} }}
.r-card {{ animation: cardIn 0.3s ease-out forwards; }}
.r-card:hover {{ border-color: var(--primary); box-shadow: 0 6px 20px rgba(108, 92, 231, 0.08); }}
.r-card h4 {{ font-size: 0.90rem; font-weight: 700; margin: 0 0 8px; }}
.r-card p  {{ font-size: 0.90rem; line-height: 1.65; margin: 0; }}

.tag {{ display: inline-block; padding: 5px 14px; border-radius: 18px; font-size: 0.78rem; font-weight: 600; margin: 3px 4px; background: var(--tag-bg); color: var(--tag-text); border: 1px solid var(--tag-border); }}

.empty-st {{ background: var(--card-bg); text-align: center; padding: 70px 20px; border-radius: 16px; border: 1px dashed var(--border-color); }}
.empty-st .es-icon {{ font-size: 2.8rem; margin-bottom: 14px; }}
.empty-st .es-text {{ font-size: 0.92rem; font-weight: 500; color: var(--text-label); }}

/* Tooltip */
.stTooltipIcon {{ margin-left: 6px !important; opacity: 0.5; color: var(--text-label) !important; }}
"""

def inject_css():
    init_theme()
    w = 260 if st.session_state.sidebar_expanded else 70
    
    css_vars = _VARS_DARK if is_dark() else _VARS_LIGHT
    base_css = get_base_css(w)
    
    st.markdown(f"<style>{css_vars}\n{base_css}</style>", unsafe_allow_html=True)
