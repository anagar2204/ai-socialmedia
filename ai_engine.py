"""
ai_engine.py — Core AI/LLM Integration Layer
=============================================
All Groq API calls are routed through this module.
Handles prompt construction, API communication, error handling,
and response parsing for every feature in the Content Studio.
"""

import os
import json
from groq import Groq
from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

load_dotenv()

def _get_client():
    """Return a Groq client, raising a clear error if the key is missing."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or api_key == "your-key-here":
        raise EnvironmentError(
            "GROQ_API_KEY is not set. Please add it to your .env file."
        )
    return Groq(api_key=api_key)


# ---------------------------------------------------------------------------
# Internal helper
# ---------------------------------------------------------------------------

def _call_llm(prompt: str, temperature: float = 0.8, max_tokens: int = 2048) -> str:
    """
    Send a prompt to the Groq Chat API and return the assistant's reply.

    Parameters
    ----------
    prompt : str
        The user-role message content.
    temperature : float
        Creativity dial (0 = deterministic, 1 = creative).
    max_tokens : int
        Maximum response length.

    Returns
    -------
    str
        The model's text response.

    Raises
    ------
    Exception
        Wraps any API or network error with a user-friendly message.
    """
    try:
        client = _get_client()
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert social-media marketing strategist "
                        "and copywriter. Always return output in the exact JSON "
                        "structure requested by the user. Do not include markdown "
                        "code fences in your response — return raw JSON only."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content.strip()
    except EnvironmentError:
        raise  # re-raise key-missing errors as-is
    except Exception as exc:
        raise RuntimeError(
            f"AI engine error: {exc}. Please check your API key and network connection."
        ) from exc


def _parse_json(raw: str) -> dict | list:
    """
    Safely parse a JSON string, stripping markdown fences if the model
    accidentally includes them.
    """
    cleaned = raw.strip()
    if cleaned.startswith("```"):
        # Remove opening fence (```json or ```)
        cleaned = cleaned.split("\n", 1)[1] if "\n" in cleaned else cleaned[3:]
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]
    return json.loads(cleaned.strip())


# ---------------------------------------------------------------------------
# Public API — Caption Generator
# ---------------------------------------------------------------------------

def build_caption_prompt(
    brand: str,
    audience: str,
    platform: str,
    tone: str,
    goal: str,
    keywords: str = "",
    use_emojis: bool = True,
) -> str:
    """
    Construct the prompt for caption generation.

    Returns a fully-formed instruction string that tells the LLM exactly
    what JSON structure to produce.
    """
    emoji_instruction = (
        "Use relevant emojis throughout the captions."
        if use_emojis
        else "Do NOT use any emojis."
    )

    keyword_line = f"Incorporate these keywords naturally: {keywords}" if keywords else ""

    return f"""
Generate social media captions for the brand "{brand}".

Target audience : {audience}
Platform        : {platform}
Tone            : {tone}
Content goal    : {goal}
{keyword_line}
{emoji_instruction}

Return a JSON object with exactly these keys:
{{
  "caption_variation_1": "...",
  "caption_variation_2": "...",
  "caption_variation_3": "...",
  "short_caption": "... (under 120 characters)",
  "storytelling_caption": "... (a longer, narrative-style caption)",
  "hashtags": ["#tag1", "#tag2", ... ]   // exactly 10 hashtags
}}
""".strip()


def generate_caption(
    brand: str,
    audience: str,
    platform: str,
    tone: str,
    goal: str,
    keywords: str = "",
    use_emojis: bool = True,
) -> dict:
    """
    Generate captions, a short caption, a storytelling caption,
    and 10 hashtags for a social-media post.

    Returns
    -------
    dict
        Parsed JSON with caption variations, short caption,
        storytelling caption, and hashtags list.
    """
    prompt = build_caption_prompt(brand, audience, platform, tone, goal, keywords, use_emojis)
    raw = _call_llm(prompt, temperature=0.85)
    return _parse_json(raw)


# ---------------------------------------------------------------------------
# Public API — Quick Inference
# ---------------------------------------------------------------------------

def infer_caption_fields(quick_idea: str) -> dict:
    """
    Infer target audience, tone, content goal, and keywords from a short idea.

    Returns
    -------
    dict
        Parsed JSON with inferred fields.
    """
    prompt = f"""
Analyze the following social media post idea and infer the best settings for generating a caption.

User's Idea: "{quick_idea}"

Infer the following four fields based on the idea. Keep them concise.
1. Target Audience (e.g. Gen Z fitness enthusiasts, Young professionals)
2. Tone (e.g. Professional, Luxury, Funny, Bold, Minimal, Emotional)
3. Content Goal (e.g. Engagement, Sales, Awareness, Launch, Festive Campaign, Corporate)
4. Keywords (e.g. summer, launch, sale - comma separated)

Return a JSON object with exactly these keys:
{{
  "audience": "...",
  "tone": "...",
  "goal": "...",
  "keywords": "..."
}}
"""
    raw = _call_llm(prompt.strip(), temperature=0.5, max_tokens=256)
    return _parse_json(raw)


# ---------------------------------------------------------------------------
# Public API — Image Prompt Generator
# ---------------------------------------------------------------------------

def generate_image_prompt(
    brand: str,
    product_description: str,
    visual_style: str,
    platform: str,
) -> list[str]:
    """
    Generate three high-quality AI image prompts suitable for
    Midjourney / DALL-E.

    Returns
    -------
    list[str]
        Three detailed image-generation prompts.
    """
    prompt = f"""
Create 3 high-quality AI image generation prompts for the brand "{brand}".

Product / Description : {product_description}
Visual style          : {visual_style}
Target platform       : {platform}

Each prompt must be highly detailed, specifying composition, lighting,
color palette, mood, and camera angle. Make them ready to paste into
Midjourney or DALL-E without any editing.

Return a JSON object:
{{
  "prompts": [
    "prompt 1 ...",
    "prompt 2 ...",
    "prompt 3 ..."
  ]
}}
""".strip()

    raw = _call_llm(prompt, temperature=0.9)
    data = _parse_json(raw)
    return data.get("prompts", [])


# ---------------------------------------------------------------------------
# Public API — Content Calendar Generator
# ---------------------------------------------------------------------------

def generate_content_calendar(
    brand: str,
    industry: str,
    audience: str,
    goal: str,
) -> list[dict]:
    """
    Generate a 7-day social media content calendar.

    Returns
    -------
    list[dict]
        Seven dicts, each with keys: day, post_idea, caption_theme, hashtags.
    """
    prompt = f"""
Create a 7-day social media content calendar for the brand "{brand}".

Industry        : {industry}
Target audience : {audience}
Content goal    : {goal}

For each day (Day 1 through Day 7), provide:
- A creative post idea
- A caption theme / angle
- 5 suggested hashtags

Return a JSON object:
{{
  "calendar": [
    {{
      "day": "Day 1",
      "post_idea": "...",
      "caption_theme": "...",
      "hashtags": ["#tag1", "#tag2", "#tag3", "#tag4", "#tag5"]
    }},
    ...
  ]
}}
""".strip()

    raw = _call_llm(prompt, temperature=0.8)
    data = _parse_json(raw)
    return data.get("calendar", [])


# ---------------------------------------------------------------------------
# Public API — Hashtag Generator
# ---------------------------------------------------------------------------

def generate_hashtags(
    brand: str,
    industry: str,
    audience: str,
    goal: str,
) -> list[str]:
    """
    Generate 15 AI-powered hashtags for a brand + industry combo.

    These are later blended with the trending dataset in content_modules.py.

    Returns
    -------
    list[str]
        Up to 15 hashtags (strings starting with #).
    """
    prompt = f"""
Generate 15 highly optimized social media hashtags for the brand "{brand}".

Industry        : {industry}
Target audience : {audience}
Content goal    : {goal}

Mix popular high-reach hashtags with niche community hashtags.
Return a JSON object:
{{
  "hashtags": ["#tag1", "#tag2", ... ]   // exactly 15
}}
""".strip()

    raw = _call_llm(prompt, temperature=0.7)
    data = _parse_json(raw)
    return data.get("hashtags", [])
