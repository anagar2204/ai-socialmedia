"""
utils.py — Shared Utility Functions
====================================
Formatting helpers, clipboard integration, download content
generation, and character counting for the Streamlit UI.
"""

import streamlit as st
import pandas as pd


# ---------------------------------------------------------------------------
# Clipboard copy (JavaScript injection for Streamlit)
# ---------------------------------------------------------------------------

def copy_to_clipboard(text: str, button_key: str) -> None:
    """
    Render a small 'Copy' button that copies *text* to the clipboard
    using injected JavaScript.

    Parameters
    ----------
    text : str
        The content to copy.
    button_key : str
        Unique Streamlit widget key to avoid duplicate-ID errors.
    """
    # Escape backticks and backslashes for the JS template literal
    escaped = text.replace("\\", "\\\\").replace("`", "\\`").replace("$", "\\$")

    copy_js = f"""
    <button onclick="navigator.clipboard.writeText(`{escaped}`).then(
        () => this.innerText = '✅ Copied!',
        () => this.innerText = '❌ Failed'
    )" style="
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        color: white;
        border: none;
        padding: 6px 16px;
        border-radius: 8px;
        cursor: pointer;
        font-size: 13px;
        font-weight: 500;
        transition: all 0.2s ease;
    ">📋 Copy</button>
    """
    st.components.v1.html(copy_js, height=40)


# ---------------------------------------------------------------------------
# Download helpers
# ---------------------------------------------------------------------------

def generate_text_download(content: str, filename: str = "output.txt") -> None:
    """
    Render a Streamlit download button for plain-text content.
    """
    st.download_button(
        label="⬇️ Download as Text",
        data=content,
        file_name=filename,
        mime="text/plain",
    )


def generate_csv_download(df: pd.DataFrame, filename: str = "calendar.csv") -> None:
    """
    Render a Streamlit download button for a DataFrame as CSV.
    """
    csv_data = df.to_csv(index=False)
    st.download_button(
        label="⬇️ Download as CSV",
        data=csv_data,
        file_name=filename,
        mime="text/csv",
    )


# ---------------------------------------------------------------------------
# Formatting helpers
# ---------------------------------------------------------------------------

def format_caption_output(data: dict) -> str:
    """
    Format the caption generator output into a readable plain-text block
    suitable for downloading or displaying.

    Parameters
    ----------
    data : dict
        Output from run_caption_generator().

    Returns
    -------
    str
        Formatted multi-line string.
    """
    lines = []
    lines.append("=" * 50)
    lines.append("  AI CAPTION GENERATOR — RESULTS")
    lines.append("=" * 50)

    for i, cap in enumerate(data.get("captions", []), 1):
        lines.append(f"\n📝 Caption Variation {i}:")
        lines.append(cap)

    lines.append(f"\n⚡ Short Caption (< 120 chars):")
    lines.append(data.get("short_caption", ""))

    lines.append(f"\n📖 Storytelling Caption:")
    lines.append(data.get("storytelling_caption", ""))

    lines.append(f"\n#️⃣ Hashtags:")
    lines.append("  ".join(data.get("hashtags", [])))

    lines.append("\n" + "=" * 50)
    return "\n".join(lines)


def format_image_prompts(prompts: list[str]) -> str:
    """
    Format image prompts into a downloadable text block.
    """
    lines = []
    lines.append("=" * 50)
    lines.append("  AI IMAGE PROMPT GENERATOR — RESULTS")
    lines.append("=" * 50)

    for i, prompt in enumerate(prompts, 1):
        lines.append(f"\n🎨 Prompt {i}:")
        lines.append(prompt)

    lines.append("\n" + "=" * 50)
    return "\n".join(lines)


def format_hashtag_output(hashtags: list[str]) -> str:
    """
    Format hashtags into a downloadable text block.
    """
    lines = []
    lines.append("=" * 50)
    lines.append("  OPTIMIZED HASHTAGS")
    lines.append("=" * 50)
    lines.append("\n" + "  ".join(hashtags))
    lines.append("\n" + "=" * 50)
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Character counter widget
# ---------------------------------------------------------------------------

def character_counter(text: str, limit: int = 280) -> None:
    """
    Display a colour-coded character counter.
    Green if under limit, orange if near, red if over.
    """
    length = len(text)
    ratio = length / limit if limit > 0 else 1

    if ratio <= 0.7:
        color = "#22c55e"   # green
    elif ratio <= 0.9:
        color = "#f59e0b"   # amber
    else:
        color = "#ef4444"   # red

    st.markdown(
        f'<p style="font-size:13px; color:{color}; font-weight:600;">'
        f'{length} / {limit} characters</p>',
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Session history helpers
# ---------------------------------------------------------------------------

def add_to_history(key: str, entry: dict, max_items: int = 3) -> None:
    """
    Append an entry to the session history list stored at
    st.session_state[key], keeping only the latest *max_items*.
    """
    if key not in st.session_state:
        st.session_state[key] = []
    st.session_state[key].insert(0, entry)
    st.session_state[key] = st.session_state[key][:max_items]


def get_history(key: str) -> list[dict]:
    """Return the session history list for a given key."""
    return st.session_state.get(key, [])
