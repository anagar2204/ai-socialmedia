"""
components.py — Atomic UI Components
=====================================
Result cards, hashtag chips, platform preview, copy buttons,
character counters, and downloads. No business logic.
"""

import streamlit as st

# ── Result cards ──────────────────────────────────────────────────────────

def result_card(title: str, body: str, icon: str = "📝"):
    st.markdown(
        f'<div class="r-card"><h4>{icon} {title}</h4><p>{body}</p></div>',
        unsafe_allow_html=True,
    )

def result_card_copy(title: str, body: str, icon: str, key: str, limit: int = 0):
    result_card(title, body, icon)
    cols = st.columns([1, 2] if limit else [1])
    with cols[0]:
        copy_btn(body, key)
    if limit and len(cols) > 1:
        with cols[1]:
            char_counter(body, limit)

# ── Hashtag chips ─────────────────────────────────────────────────────────

def hashtag_chips(tags: list[str], title: str = "Hashtags"):
    html = " ".join(f'<span class="tag">{t}</span>' for t in tags)
    st.markdown(
        f'<div class="r-card"><h4>#️⃣ {title} ({len(tags)})</h4>'
        f'<div style="margin-top:8px">{html}</div></div>',
        unsafe_allow_html=True,
    )

# ── Platform preview ──────────────────────────────────────────────────────

_PF = {
    "Instagram":   {"ic":"📸","ini":"IG","a":["❤️ Like","💬 Comment","📤 Share","🔖 Save"]},
    "LinkedIn":    {"ic":"💼","ini":"LI","a":["👍 Like","💬 Comment","🔁 Repost","📤 Send"]},
    "Twitter / X": {"ic":"𝕏", "ini":"X", "a":["💬 Reply","🔁 Repost","❤️ Like","📊 View"]},
    "Facebook":    {"ic":"📘","ini":"FB","a":["👍 Like","💬 Comment","📤 Share"]},
}

def platform_preview(caption: str, brand: str, platform: str):
    c = _PF.get(platform, _PF["Instagram"])
    acts = "  ".join(f"<span>{a}</span>" for a in c["a"])
    txt = (caption[:277] + "…") if platform == "Twitter / X" and len(caption) > 280 else caption
    st.markdown(
        f'<div class="pv">'
        f'<div class="pv-head"><div class="pv-av">{c["ini"]}</div>'
        f'<div><div class="pv-nm">{brand} {c["ic"]}</div>'
        f'<span class="pv-time">Just now</span></div></div>'
        f'<div class="pv-body">{txt}</div>'
        f'<div class="pv-acts">{acts}</div></div>',
        unsafe_allow_html=True,
    )

# ── Copy button ───────────────────────────────────────────────────────────

def copy_btn(text: str, key: str):
    esc = text.replace("\\","\\\\").replace("`","\\`").replace("$","\\$")
    st.components.v1.html(
        f'<button onclick="navigator.clipboard.writeText(`{esc}`).then('
        f"()=>this.innerText='✅ Copied!',"
        f"()=>this.innerText='❌ Failed'"
        ')" style="background:linear-gradient(135deg,#6366f1,#7c3aed);color:#fff;'
        'border:none;padding:5px 14px;border-radius:8px;cursor:pointer;'
        'font-size:12px;font-weight:600">📋 Copy</button>',
        height=34,
    )

# ── Character counter ─────────────────────────────────────────────────────

def char_counter(text: str, limit: int = 280):
    n = len(text)
    r = n / limit if limit else 1
    c = "#22c55e" if r <= 0.7 else ("#f59e0b" if r <= 0.9 else "#ef4444")
    st.markdown(f'<p class="cc" style="color:{c}">{n}/{limit} chars</p>', unsafe_allow_html=True)

# ── Empty state ───────────────────────────────────────────────────────────

def empty_state(icon: str, text: str):
    st.markdown(
        f'<div class="empty-state">'
        f'<div class="es-icon">{icon}</div>'
        f'<div class="es-text">{text}</div></div>',
        unsafe_allow_html=True,
    )

# ── Downloads ─────────────────────────────────────────────────────────────

def dl_text(content: str, filename: str = "output.txt"):
    st.download_button("⬇️ Download", data=content, file_name=filename, mime="text/plain")

def dl_csv(df, filename: str = "output.csv"):
    st.download_button("⬇️ Download CSV", data=df.to_csv(index=False), file_name=filename, mime="text/csv")
