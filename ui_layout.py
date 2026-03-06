"""
ui_layout.py — Layout Orchestration
====================================
Sidebar with dynamic collapse state (260px / 70px).
Top header with hamburger menu, title, and theme toggle.
"""

import streamlit as st
import datetime
from theme_system import toggle_theme, is_dark

MODULES = [
    ("✍️", "Caption Generator"),
    ("🎨", "Image Prompts"),
    ("📅", "Content Calendar"),
    ("#️⃣", "Hashtag Engine"),
]

_META = {
    "Caption Generator": {
        "title": "AI Caption Generator",
        "desc": "Create engaging captions for social media posts using AI.",
    },
    "Image Prompts": {
        "title": "AI Image Prompts",
        "desc": "Generate stunning image prompts for your visual content.",
    },
    "Content Calendar": {
        "title": "AI Content Calendar",
        "desc": "Plan a 7-day social media schedule tailored to your brand.",
    },
    "Hashtag Engine": {
        "title": "AI Hashtag Engine",
        "desc": "Get optimized hashtags blending trends and AI intelligence.",
    },
}

_STEPS = {
    "Caption Generator": [("1", "Enter brand details"), ("2", "Generate captions"), ("3", "Copy captions for your post")],
    "Image Prompts": [("1", "Describe visual"), ("2", "Generate prompts"), ("3", "Copy and use")],
    "Content Calendar": [("1", "Set brand details"), ("2", "Generate calendar"), ("3", "Download plan")],
    "Hashtag Engine": [("1", "Enter brand details"), ("2", "Generate hashtags"), ("3", "Copy & post")],
}

# ── Sidebar ───────────────────────────────────────────────────────────────

def render_sidebar() -> str:
    is_exp = st.session_state.get("sidebar_expanded", True)

    with st.sidebar:
        # Toggle Button at the top
        toggle_icon = "❮" if is_exp else "❯"
        toggle_help = "Collapse sidebar" if is_exp else "Expand sidebar"
        
        st.markdown('<div class="sb-toggle-area">', unsafe_allow_html=True)
        if st.button(toggle_icon, key="sb_toggle_btn", help=toggle_help, use_container_width=True):
            st.session_state.sidebar_expanded = not is_exp
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        # Logo
        if is_exp:
            st.markdown(
                '<div class="sb-logo"><div class="sb-logo-icon">🚀</div>'
                '<div><div class="sb-logo-name">Content Studio</div>'
                '<div class="sb-logo-sub">AI-Powered Toolkit</div></div></div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<div class="sb-logo"><div class="sb-logo-icon">🚀</div></div>',
                unsafe_allow_html=True,
            )

        # Nav buttons
        if "active_module" not in st.session_state:
            st.session_state.active_module = "Caption Generator"

        for ic, nm in MODULES:
            is_active = (st.session_state.active_module == nm)
            btn_type = "primary" if is_active else "secondary"
            label = f"{ic}  {nm}" if is_exp else ic
            tooltip = None if is_exp else nm
            
            if st.button(label, key=f"nav_{nm}", help=tooltip, use_container_width=True, type=btn_type):
                st.session_state.active_module = nm
                st.rerun()

        # History
        hist = []
        for k, mod in [("cap_h","Caption"),("img_h","Image"),("cal_h","Calendar"),("ht_h","Hashtag")]:
            for item in st.session_state.get(k, []):
                hist.append({**item, "_m": mod})
        hist.sort(key=lambda x: x.get("t",""), reverse=True)

        if is_exp:
            st.markdown('<div class="sb-sec">Recent Generations</div>', unsafe_allow_html=True)
            if not hist:
                st.caption("No generations yet.")
            else:
                for h in hist[:3]:
                    st.markdown(
                        f'<div class="hist"><strong>{h.get("brand","—")}</strong>'
                        f'<span>{h.get("t","")}&nbsp;·&nbsp;{h["_m"]}</span></div>',
                        unsafe_allow_html=True,
                    )
        else:
            st.markdown('<div class="sb-sec" style="text-align:center">🕒</div>', unsafe_allow_html=True)
            if hist:
                for h in hist[:3]:
                    st.markdown(f'<div class="hist" style="text-align:center" title="{h.get("brand","—")}">{h["_m"][0]}</div>', unsafe_allow_html=True)

    return st.session_state.active_module

# ── Top Header ────────────────────────────────────────────────────────────

def render_top_header(module: str):
    m = _META.get(module, _META["Caption Generator"])
    is_exp = st.session_state.get("sidebar_expanded", True)

    st.markdown('<div class="top-header">', unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 10, 1])

    with c1:
        st.markdown('<div class="th-hamburger">', unsafe_allow_html=True)
        if st.button("☰" if not is_exp else "✖", key="hb_btn"):
            st.session_state.sidebar_expanded = not is_exp
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown(
            f'<div class="th-content"><h1>{m["title"]}</h1><p>{m["desc"]}</p></div>',
            unsafe_allow_html=True,
        )

    with c3:
        st.markdown('<div class="th-theme">', unsafe_allow_html=True)
        icon = "☀️" if is_dark() else "🌙"
        if st.button(icon, key="thm_btn"):
            toggle_theme()
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ── Workflow steps ────────────────────────────────────────────────────────

def render_workflow_steps(module: str, current_step: int = 1):
    steps = _STEPS.get(module, _STEPS["Caption Generator"])
    anchors = ["step-1", "step-2", "step-3"]
    html = ""
    for i, (n, txt) in enumerate(steps):
        target = anchors[i] if i < len(anchors) else "top"
        active_cls = " active-step" if (i + 1 == current_step) else ""
        html += f'<a href="#{target}" target="_self" class="wf-step{active_cls}"><span class="wf-dot">{n}</span> {txt}</a>'
        
    st.markdown(f'<div class="wf-steps">{html}</div>', unsafe_allow_html=True)

# ── History writer ────────────────────────────────────────────────────────

def push_history(key: str, entry: dict, max_n: int = 3):
    if key not in st.session_state:
        st.session_state[key] = []
    entry["t"] = datetime.datetime.now().strftime("%I:%M %p")
    st.session_state[key].insert(0, entry)
    st.session_state[key] = st.session_state[key][:max_n]
