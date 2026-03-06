"""
content_modules.py — High-Level Content Orchestration
=====================================================
Bridges the AI engine with the Streamlit UI.
Each *run_** function validates inputs, calls the AI engine,
applies post-processing (formatting, merging, deduplication),
and returns display-ready data structures.
"""

import random
import pandas as pd

from ai_engine import (
    generate_caption,
    generate_image_prompt,
    generate_content_calendar,
    generate_hashtags,
    infer_caption_fields,
)
from hashtag_dataset import get_trending_hashtags


# ---------------------------------------------------------------------------
# Module 1 — Caption Generator
# ---------------------------------------------------------------------------

def run_caption_generator(
    brand: str,
    audience: str,
    platform: str,
    tone: str,
    goal: str,
    keywords: str = "",
    use_emojis: bool = True,
) -> dict:
    """
    Orchestrate caption generation.

    Returns
    -------
    dict
        {
          "captions": [str, str, str],
          "short_caption": str,
          "storytelling_caption": str,
          "hashtags": [str, ...]
        }
    """
    # Input validation
    if not brand.strip():
        raise ValueError("Brand name is required.")
    if not audience.strip():
        raise ValueError("Target audience is required.")

    data = generate_caption(
        brand=brand,
        audience=audience,
        platform=platform,
        tone=tone,
        goal=goal,
        keywords=keywords,
        use_emojis=use_emojis,
    )

    return {
        "captions": [
            data.get("caption_variation_1", ""),
            data.get("caption_variation_2", ""),
            data.get("caption_variation_3", ""),
        ],
        "short_caption": data.get("short_caption", ""),
        "storytelling_caption": data.get("storytelling_caption", ""),
        "hashtags": data.get("hashtags", []),
    }


def run_quick_idea_inference(quick_idea: str) -> dict:
    """
    Takes a rough post idea and infers the form fields using the AI Engine.
    
    Returns
    -------
    dict
        {
            "audience": str,
            "tone": str,
            "goal": str,
            "keywords": str
        }
    """
    if not quick_idea.strip():
        raise ValueError("Quick idea text is required.")
        
    inferred = infer_caption_fields(quick_idea=quick_idea)
    
    return {
        "audience": inferred.get("audience", ""),
        "tone": inferred.get("tone", "Professional"),
        "goal": inferred.get("goal", "Engagement"),
        "keywords": inferred.get("keywords", ""),
    }


# ---------------------------------------------------------------------------
# Module 2 — Image Prompt Generator
# ---------------------------------------------------------------------------

def run_image_prompt_generator(
    brand: str,
    product_description: str,
    visual_style: str,
    platform: str,
) -> list[str]:
    """
    Orchestrate AI image prompt generation.

    Returns
    -------
    list[str]
        Three detailed image-generation prompts.
    """
    if not brand.strip():
        raise ValueError("Brand name is required.")
    if not product_description.strip():
        raise ValueError("Product description is required.")

    return generate_image_prompt(
        brand=brand,
        product_description=product_description,
        visual_style=visual_style,
        platform=platform,
    )


# ---------------------------------------------------------------------------
# Module 3 — Content Calendar Generator
# ---------------------------------------------------------------------------

def run_calendar_generator(
    brand: str,
    industry: str,
    audience: str,
    goal: str,
) -> pd.DataFrame:
    """
    Orchestrate 7-day content calendar generation.

    Returns
    -------
    pd.DataFrame
        Columns: Day, Post Idea, Caption Theme, Hashtags
    """
    if not brand.strip():
        raise ValueError("Brand name is required.")
    if not industry.strip():
        raise ValueError("Industry is required.")

    calendar = generate_content_calendar(
        brand=brand,
        industry=industry,
        audience=audience,
        goal=goal,
    )

    rows = []
    for entry in calendar:
        rows.append(
            {
                "Day": entry.get("day", ""),
                "Post Idea": entry.get("post_idea", ""),
                "Caption Theme": entry.get("caption_theme", ""),
                "Hashtags": ", ".join(entry.get("hashtags", [])),
            }
        )

    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Module 4 — Trend-Based Hashtag Engine
# ---------------------------------------------------------------------------

def run_hashtag_generator(
    brand: str,
    industry: str,
    audience: str,
    goal: str,
) -> list[str]:
    """
    Merge AI-generated hashtags with the curated trending dataset,
    deduplicate, and return exactly 15 optimized hashtags.

    Strategy
    --------
    1. Get up to 15 AI-generated hashtags.
    2. Get up to 10 trending hashtags from the dataset (matched by industry).
    3. Merge, deduplicate (case-insensitive), shuffle, and trim to 15.

    Returns
    -------
    list[str]
        Exactly 15 unique hashtags.
    """
    if not brand.strip():
        raise ValueError("Brand name is required.")
    if not industry.strip():
        raise ValueError("Industry is required.")

    # AI-generated
    ai_tags = generate_hashtags(
        brand=brand,
        industry=industry,
        audience=audience,
        goal=goal,
    )

    # Trending dataset — try exact category, fall back to Business
    trending_tags = get_trending_hashtags(industry, count=10)
    if not trending_tags:
        trending_tags = get_trending_hashtags("Business", count=10)

    # Merge & deduplicate (case-insensitive, keep original casing)
    seen: set[str] = set()
    merged: list[str] = []
    for tag in ai_tags + trending_tags:
        normalised = tag.lower().strip()
        if normalised not in seen:
            seen.add(normalised)
            merged.append(tag)

    # Shuffle for variety, then trim to 15
    random.shuffle(merged)
    return merged[:15]
