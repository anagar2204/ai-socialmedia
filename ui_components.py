"""
ui_components.py — Reusable UI Renderers
=========================================
Modular Streamlit components for the Content Studio dashboard:
cards, hashtag chips, platform previews, history panel, headers,
and input helpers. All rendering logic is separated from business logic.
"""

import streamlit as st
import datetime


# ═══════════════════════════════════════════════════════════════════════════
# Hero Header
# ═══════════════════════════════════════════════════════════════════════════

def render_hero():
    """Render the gradient hero header with badges."""
    st.markdown("""
    <div class="hero">
        <div class="hero-content">
            <h1>🚀 AI Social Media Content Studio</h1>
            <p>Generate captions, image prompts, content calendars &amp; hashtags — powered by AI</p>
            <div class="hero-badges">
                <span class="hero-badge">✍️ Captions</span>
                <span class="hero-badge">🎨 Image Prompts</span>
                <span class="hero-badge">📅 Calendar</span>
                <span class="hero-badge">#️⃣ Hashtags</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
# API Warning
# ═══════════════════════════════════════════════════════════════════════════

def render_api_warning():
    """Show a styled warning when the API key is missing."""
    import os
    key = os.getenv("GROQ_API_KEY", "")
    if not key or key == "your-key-here":
        st.markdown(
            '<div class="api-warning">'
            '⚠️ <strong>Groq API key not configured.</strong> '
            'Add your key to <code>.env</code> as '
            '<code>GROQ_API_KEY=gsk_...</code> to enable AI generation.'
            '</div>',
            unsafe_allow_html=True,
        )


# ═══════════════════════════════════════════════════════════════════════════
# Result Cards
# ═══════════════════════════════════════════════════════════════════════════

def render_card(title: str, body: str, icon: str = "📝"):
    """Render a styled output card with title + body text."""
    st.markdown(
        f'<div class="result-card">'
        f'<h4>{icon} {title}</h4>'
        f'<p>{body}</p>'
        f'</div>',
        unsafe_allow_html=True,
    )


def render_card_with_actions(title: str, body: str, icon: str, card_key: str):
    """
    Render an output card with a copy button and character counter.
    """
    st.markdown(
        f'<div class="result-card">'
        f'<h4>{icon} {title}</h4>'
        f'<p>{body}</p>'
        f'</div>',
        unsafe_allow_html=True,
    )

    col_copy, col_char = st.columns([1, 2])
    with col_copy:
        _copy_button(body, card_key)
    with col_char:
        _char_counter(body, 2200)


# ═══════════════════════════════════════════════════════════════════════════
# Hashtag Chips
# ═══════════════════════════════════════════════════════════════════════════

def render_chips(tags: list[str], card_title: str = "Hashtags"):
    """Render hashtags as styled chips inside a card."""
    chips_html = " ".join(f'<span class="chip">{t}</span>' for t in tags)
    st.markdown(
        f'<div class="result-card">'
        f'<h4>#️⃣ {card_title} ({len(tags)})</h4>'
        f'<div style="margin-top:0.5rem">{chips_html}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


# ═══════════════════════════════════════════════════════════════════════════
# Platform Preview
# ═══════════════════════════════════════════════════════════════════════════

_PLATFORM_CONFIG = {
    "Instagram": {
        "icon": "📸",
        "engagement": ["❤️ Like", "💬 Comment", "📤 Share", "🔖 Save"],
        "initial": "IG",
    },
    "LinkedIn": {
        "icon": "💼",
        "engagement": ["👍 Like", "💬 Comment", "🔁 Repost", "📤 Send"],
        "initial": "LI",
    },
    "Twitter / X": {
        "icon": "𝕏",
        "engagement": ["💬 Reply", "🔁 Repost", "❤️ Like", "📊 View"],
        "initial": "X",
    },
    "Facebook": {
        "icon": "📘",
        "engagement": ["👍 Like", "💬 Comment", "📤 Share"],
        "initial": "FB",
    },
}


def render_platform_preview(caption: str, brand: str, platform: str):
    """
    Render a mock social-media post preview that looks like the actual
    platform feed card.
    """
    cfg = _PLATFORM_CONFIG.get(platform, _PLATFORM_CONFIG["Instagram"])
    engagement_html = "  ".join(
        f'<span>{e}</span>' for e in cfg["engagement"]
    )

    # Trim for Twitter
    display_caption = caption
    if platform == "Twitter / X" and len(caption) > 280:
        display_caption = caption[:277] + "..."

    st.markdown(
        f'<div class="platform-preview">'
        f'  <div class="preview-header">'
        f'    <div class="avatar">{cfg["initial"]}</div>'
        f'    <div>'
        f'      <div class="preview-name">{brand} {cfg["icon"]}</div>'
        f'      <span style="font-size:0.72rem;opacity:0.5">Just now</span>'
        f'    </div>'
        f'  </div>'
        f'  <div class="preview-body">{display_caption}</div>'
        f'  <div class="preview-engagement">{engagement_html}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


# ═══════════════════════════════════════════════════════════════════════════
# History Panel (Sidebar)
# ═══════════════════════════════════════════════════════════════════════════

def render_history_sidebar():
    """
    Render the 'Recent Generations' sidebar with clickable entries.
    """
    with st.sidebar:
        st.markdown("### 🕐 Recent Generations")

        # Combine all histories
        all_history = []
        for key, label in [
            ("cap_history", "Caption"),
            ("img_history", "Image Prompt"),
            ("cal_history", "Calendar"),
            ("ht_history", "Hashtag"),
        ]:
            items = st.session_state.get(key, [])
            for item in items:
                all_history.append({**item, "_module": label})

        # Sort by time descending and take 5
        all_history.sort(key=lambda x: x.get("time", ""), reverse=True)
        all_history = all_history[:5]

        if not all_history:
            st.caption("No generations yet. Start creating!")
            return

        for item in all_history:
            preview = item.get("short_preview", item.get("preview", ""))
            if len(preview) > 55:
                preview = preview[:55] + "…"

            st.markdown(
                f'<div class="history-entry">'
                f'<strong>{item.get("brand", "—")}</strong> · '
                f'<span>{item["_module"]}</span><br>'
                f'<span>{preview}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )

        st.markdown("---")


# ═══════════════════════════════════════════════════════════════════════════
# Input helpers
# ═══════════════════════════════════════════════════════════════════════════

def tooltip(text: str) -> str:
    """Return HTML for a small info-circle tooltip."""
    return f'<span class="tooltip-icon" title="{text}">?</span>'


def input_label(label: str, help_text: str = "") -> str:
    """Return a label with an optional tooltip icon."""
    tip = tooltip(help_text) if help_text else ""
    return f"{label} {tip}"


# ═══════════════════════════════════════════════════════════════════════════
# Copy-to-clipboard button
# ═══════════════════════════════════════════════════════════════════════════

def _copy_button(text: str, key: str):
    """Render a JS-powered copy button."""
    escaped = text.replace("\\", "\\\\").replace("`", "\\`").replace("$", "\\$")
    js = f"""
    <button onclick="navigator.clipboard.writeText(`{escaped}`).then(
        () => this.innerText = '✅ Copied!',
        () => this.innerText = '❌ Failed'
    )" style="
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        color: white; border: none;
        padding: 5px 14px; border-radius: 8px;
        cursor: pointer; font-size: 12px; font-weight: 600;
        transition: all 0.2s ease;
    ">📋 Copy</button>
    """
    st.components.v1.html(js, height=36)


def render_copy_button(text: str, key: str):
    """Public wrapper for the copy button."""
    _copy_button(text, key)


# ═══════════════════════════════════════════════════════════════════════════
# Character counter
# ═══════════════════════════════════════════════════════════════════════════

def _char_counter(text: str, limit: int):
    """Render a colour-coded character counter."""
    length = len(text)
    ratio = length / limit if limit > 0 else 1
    if ratio <= 0.7:
        color = "#22c55e"
    elif ratio <= 0.9:
        color = "#f59e0b"
    else:
        color = "#ef4444"
    st.markdown(
        f'<p class="char-counter" style="color:{color}">'
        f'{length} / {limit} characters</p>',
        unsafe_allow_html=True,
    )


def render_char_counter(text: str, limit: int = 280):
    """Public wrapper for character counter."""
    _char_counter(text, limit)


# ═══════════════════════════════════════════════════════════════════════════
# Session history helpers
# ═══════════════════════════════════════════════════════════════════════════

def add_to_history(key: str, entry: dict, max_items: int = 3):
    """Append an entry to the session history list."""
    if key not in st.session_state:
        st.session_state[key] = []
    entry["time"] = datetime.datetime.now().strftime("%H:%M:%S")
    st.session_state[key].insert(0, entry)
    st.session_state[key] = st.session_state[key][:max_items]
