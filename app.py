"""
app.py — AI Social Media Content Studio
========================================
55/45 workspace split, top header with hamburger toggle,
persistent sidebar (260px / 70px).
"""

import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="AI Content Studio", page_icon="🚀",
                   layout="wide", initial_sidebar_state="expanded")

from theme_system import inject_css
from ui_layout import (
    render_sidebar, render_top_header, render_workflow_steps, push_history,
)
from components import (
    result_card, result_card_copy, hashtag_chips, platform_preview,
    copy_btn, char_counter, empty_state, dl_text, dl_csv,
)
from content_modules import (
    run_caption_generator, run_image_prompt_generator,
    run_calendar_generator, run_hashtag_generator,
    run_quick_idea_inference,
)
from utils import format_caption_output, format_image_prompts, format_hashtag_output

inject_css()
active = render_sidebar()


# ═══════════════════════════════════════════════════════════════════════════
# CAPTION GENERATOR
# ═══════════════════════════════════════════════════════════════════════════

if active == "Caption Generator":
    def handle_generate_caption():
        qi = st.session_state.get("c_qi", "")
        if qi.strip() and qi != st.session_state.get("c_qi_last_inferred"):
            try:
                inferred = run_quick_idea_inference(qi)
                if not st.session_state.get("c_aud", "").strip(): 
                    st.session_state["c_aud"] = inferred["audience"]
                st.session_state["c_tone"] = inferred["tone"]
                st.session_state["c_goal"] = inferred["goal"]
                if not st.session_state.get("c_kw", "").strip(): 
                    st.session_state["c_kw"] = inferred["keywords"]
                st.session_state["c_qi_last_inferred"] = qi
            except Exception as e:
                st.session_state["c_qi_error"] = str(e)
        st.session_state["c_do_generate"] = True

    render_top_header(active)

    work, out = st.columns([55, 45])

    with work:
        cur_step = 3 if "c_res" in st.session_state else 1
        render_workflow_steps(active, cur_step)
        
        st.markdown('<div id="step-1"></div>', unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown('<div class="in-card-title">Quick Idea</div>', unsafe_allow_html=True)
            quick_idea = st.text_input("Quick Idea", placeholder="Describe your post idea. Example: launching a summer skincare product for Gen Z.", key="c_qi", label_visibility="collapsed")
            st.markdown('<p class="qi-tip">Tip: Write a short idea and AI will fill the rest.</p>', unsafe_allow_html=True)

        with st.container(border=True):
            st.markdown('<div class="in-card-title">Detailed Inputs</div>', unsafe_allow_html=True)

        r1a, r1b = st.columns(2)
        with r1a:
            brand = st.text_input("Brand Name", placeholder="e.g. Nike, Apple",
                                  key="c_brand", help="Your brand or company name")
        with r1b:
            audience = st.text_input("Target Audience", placeholder="e.g. Gen Z fitness enthusiasts",
                                     key="c_aud", help="Who you want to reach")

        r2a, r2b = st.columns(2)
        with r2a:
            platform = st.selectbox("Platform", ["Instagram","LinkedIn","Twitter / X","Facebook"],
                                    key="c_plat", help="Social media platform")
        with r2b:
            tone = st.selectbox("Tone", ["Professional","Luxury","Funny","Bold","Minimal","Emotional"],
                                key="c_tone", help="Voice and style of captions")

        r3a, r3b = st.columns(2)
        with r3a:
            goal = st.selectbox("Content Goal",
                                ["Engagement","Sales","Awareness","Launch","Festive Campaign","Corporate"],
                                key="c_goal", help="What you want to achieve")
        with r3b:
            kw = st.text_input("Keywords (optional)", placeholder="e.g. summer, launch",
                               key="c_kw", help="Words to include in captions")

        emoji = st.toggle("Include Emojis 😀", value=True, key="c_emo")

        st.markdown('<div id="step-2"></div>', unsafe_allow_html=True)
        b1, b2 = st.columns(2)
        with b1:
            st.button("🚀  Generate Content", key="c_go", on_click=handle_generate_caption, use_container_width=True)
        with b2:
            clr = st.button("🗑️  Clear Inputs", key="c_clr", use_container_width=True)

    if clr:
        for k in ["c_qi","c_brand","c_aud","c_kw"]:
            st.session_state[k] = ""
        st.session_state.pop("c_qi_last_inferred", None)
        st.session_state.pop("c_do_generate", None)
        st.session_state.pop("c_res", None)
        st.rerun()

    if st.session_state.get("c_do_generate"):
        st.session_state["c_do_generate"] = False
        
        if "c_qi_error" in st.session_state:
            st.error(f"Inference error: {st.session_state.pop('c_qi_error')}")

        if not brand.strip():
            st.error("Fill in **Brand Name** to continue.")
        else:
            with st.spinner("✨ Generating captions..."):
                try:
                    res = run_caption_generator(brand=brand, audience=audience,
                                                platform=platform, tone=tone,
                                                goal=goal, keywords=kw,
                                                use_emojis=emoji)
                    st.session_state["c_res"] = res
                    push_history("cap_h", {"brand": brand, "pv": res.get("short_caption","")[:50]})
                    st.toast("Captions generated! 🎉")
                except Exception as e:
                    st.error(f"Error: {e}")

    with out:
        st.markdown('<div id="step-3"></div>', unsafe_allow_html=True)
        if "c_res" in st.session_state:
            d = st.session_state["c_res"]
            for i, cap in enumerate(d.get("captions",[]), 1):
                result_card_copy(f"Caption {i}", cap, "📝", f"cc{i}", 2200)

            short = d.get("short_caption","")
            result_card("Short Caption", short, "⚡")
            c1, c2 = st.columns([1, 2])
            with c1: copy_btn(short, "cs")
            with c2: char_counter(short, 120)

            story = d.get("storytelling_caption","")
            result_card("Story Caption", story, "📖")
            copy_btn(story, "cst")

            hashtag_chips(d.get("hashtags",[]), "Suggested Hashtags")
            copy_btn(" ".join(d.get("hashtags",[])), "ct")

            st.markdown("---")
            st.markdown("##### 📱 Post Preview")
            pv_cap = d["captions"][0] if d.get("captions") else short
            platform_preview(pv_cap, brand, platform)

            dc1, dc2 = st.columns(2)
            with dc1:
                dl_text(format_caption_output(d), f"captions_{brand.replace(' ','_')}.txt")
            with dc2:
                if st.button("🔄 Regenerate", key="c_re"):
                    st.session_state.pop("c_res", None)
                    st.rerun()
        else:
            empty_state("✍️", "Your AI-generated captions will appear here.")


# ═══════════════════════════════════════════════════════════════════════════
# IMAGE PROMPTS
# ═══════════════════════════════════════════════════════════════════════════

elif active == "Image Prompts":
    render_top_header(active)

    work, out = st.columns([55, 45])

    with work:
        render_workflow_steps(active)
        st.markdown('<div class="in-card">', unsafe_allow_html=True)
        st.markdown('<div class="in-card-title">Input Details</div>', unsafe_allow_html=True)

        r1a, r1b = st.columns(2)
        with r1a:
            ib = st.text_input("Brand Name", placeholder="e.g. Gucci", key="i_brand",
                               help="Brand or product name")
        with r1b:
            ist = st.selectbox("Visual Style",
                               ["Luxury","Minimal","Modern","Festive","Cinematic","Retro"],
                               key="i_style", help="Aesthetic direction for the image")

        idesc = st.text_area("Product / Scene Description",
                             placeholder="e.g. A luxury handbag on marble with golden hour lighting",
                             key="i_desc", height=90, help="Describe the scene to visualise")

        ipl = st.selectbox("Platform",
                           ["Instagram","LinkedIn","Twitter / X","Facebook","Pinterest"],
                           key="i_plat", help="Platform for image dimensions")

        b1, b2 = st.columns(2)
        with b1:
            igo = st.button("🚀  Generate Prompts", key="i_go", use_container_width=True)
        with b2:
            icl = st.button("🗑️  Clear Inputs", key="i_cl", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    if icl:
        for k in ["i_brand","i_desc"]:
            st.session_state[k] = ""
        st.session_state.pop("i_res", None)
        st.rerun()

    if igo:
        if not ib.strip() or not idesc.strip():
            st.error("Fill in **Brand Name** and **Description**.")
        else:
            with st.spinner("🎨 Crafting image prompts…"):
                try:
                    prompts = run_image_prompt_generator(brand=ib, product_description=idesc,
                                                         visual_style=ist, platform=ipl)
                    st.session_state["i_res"] = prompts
                    push_history("img_h", {"brand": ib, "pv": prompts[0][:50] if prompts else ""})
                    st.toast("Image prompts ready! 🎉")
                except Exception as e:
                    st.error(f"Error: {e}")

    with out:
        if "i_res" in st.session_state:
            for i, p in enumerate(st.session_state["i_res"], 1):
                result_card(f"Prompt {i}", p, "🎨")
                copy_btn(p, f"ci{i}")

            dc1, dc2 = st.columns(2)
            with dc1:
                dl_text(format_image_prompts(st.session_state["i_res"]),
                        f"prompts_{ib.replace(' ','_')}.txt")
            with dc2:
                if st.button("🔄 Regenerate", key="i_re"):
                    st.session_state.pop("i_res", None)
                    st.rerun()
        else:
            empty_state("🎨", "Your AI image prompts will appear here.")


# ═══════════════════════════════════════════════════════════════════════════
# CONTENT CALENDAR
# ═══════════════════════════════════════════════════════════════════════════

elif active == "Content Calendar":
    render_top_header(active)

    work, out = st.columns([55, 45])

    with work:
        render_workflow_steps(active)
        st.markdown('<div class="in-card">', unsafe_allow_html=True)
        st.markdown('<div class="in-card-title">Input Details</div>', unsafe_allow_html=True)

        r1a, r1b = st.columns(2)
        with r1a:
            cb = st.text_input("Brand Name", placeholder="e.g. Spotify", key="cl_brand",
                               help="Brand to plan for")
        with r1b:
            ca = st.text_input("Target Audience", placeholder="e.g. Young professionals 25-35",
                               key="cl_aud", help="Audience demographics")

        r2a, r2b = st.columns(2)
        with r2a:
            ci = st.selectbox("Industry",
                              ["Technology","Fashion","Food","Lifestyle","Business",
                               "Health & Fitness","Education","Entertainment"],
                              key="cl_ind", help="Industry vertical")
        with r2b:
            cg = st.selectbox("Content Goal",
                              ["Engagement","Sales","Awareness","Launch",
                               "Community Building","Thought Leadership"],
                              key="cl_goal", help="Primary content objective")

        b1, b2 = st.columns(2)
        with b1:
            cgo = st.button("🚀  Generate Calendar", key="cl_go", use_container_width=True)
        with b2:
            ccl = st.button("🗑️  Clear Inputs", key="cl_cl", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    if ccl:
        for k in ["cl_brand","cl_aud"]:
            st.session_state[k] = ""
        st.session_state.pop("cl_res", None)
        st.rerun()

    if cgo:
        if not cb.strip() or not ca.strip():
            st.error("Fill in **Brand Name** and **Target Audience**.")
        else:
            with st.spinner("📅 Building 7-day plan…"):
                try:
                    df = run_calendar_generator(brand=cb, industry=ci,
                                                audience=ca, goal=cg)
                    st.session_state["cl_res"] = df
                    push_history("cal_h", {"brand": cb, "pv": f"{len(df)} days planned"})
                    st.toast("Calendar ready! 🎉")
                except Exception as e:
                    st.error(f"Error: {e}")

    with out:
        if "cl_res" in st.session_state:
            df = st.session_state["cl_res"]
            st.dataframe(df, use_container_width=True, hide_index=True)

            for _, row in df.iterrows():
                st.markdown(
                    f'<div class="r-card">'
                    f'<h4>📌 {row["Day"]}</h4>'
                    f'<p><strong>Post:</strong> {row["Post Idea"]}</p>'
                    f'<p><strong>Theme:</strong> {row["Caption Theme"]}</p>'
                    f'<p><strong>Tags:</strong> {row["Hashtags"]}</p></div>',
                    unsafe_allow_html=True,
                )

            dc1, dc2 = st.columns(2)
            with dc1:
                dl_csv(df, f"calendar_{cb.replace(' ','_')}.csv")
            with dc2:
                if st.button("🔄 Regenerate", key="cl_re"):
                    st.session_state.pop("cl_res", None)
                    st.rerun()
        else:
            empty_state("📅", "Your AI content calendar will appear here.")


# ═══════════════════════════════════════════════════════════════════════════
# HASHTAG ENGINE
# ═══════════════════════════════════════════════════════════════════════════

elif active == "Hashtag Engine":
    render_top_header(active)

    work, out = st.columns([55, 45])

    with work:
        render_workflow_steps(active)
        st.markdown('<div class="in-card">', unsafe_allow_html=True)
        st.markdown('<div class="in-card-title">Input Details</div>', unsafe_allow_html=True)

        r1a, r1b = st.columns(2)
        with r1a:
            hb = st.text_input("Brand Name", placeholder="e.g. Tesla", key="h_brand",
                               help="Brand or company name")
        with r1b:
            ha = st.text_input("Target Audience", placeholder="e.g. Tech-savvy millennials",
                               key="h_aud", help="Target demographics")

        r2a, r2b = st.columns(2)
        with r2a:
            hi = st.selectbox("Industry / Category",
                              ["Technology","Fashion","Food","Lifestyle","Business",
                               "Health & Fitness","Education","Entertainment"],
                              key="h_ind", help="Industry vertical")
        with r2b:
            hg = st.selectbox("Content Goal",
                              ["Engagement","Sales","Awareness","Launch","Community Building"],
                              key="h_goal", help="What you want to achieve")

        b1, b2 = st.columns(2)
        with b1:
            hgo = st.button("🚀  Generate Hashtags", key="h_go", use_container_width=True)
        with b2:
            hcl = st.button("🗑️  Clear Inputs", key="h_cl", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    if hcl:
        for k in ["h_brand","h_aud"]:
            st.session_state[k] = ""
        st.session_state.pop("h_res", None)
        st.rerun()

    if hgo:
        if not hb.strip() or not ha.strip():
            st.error("Fill in **Brand Name** and **Target Audience**.")
        else:
            with st.spinner("#️⃣ Optimizing hashtags…"):
                try:
                    tags = run_hashtag_generator(brand=hb, industry=hi,
                                                 audience=ha, goal=hg)
                    st.session_state["h_res"] = tags
                    push_history("ht_h", {"brand": hb, "pv": " ".join(tags[:4])})
                    st.toast("Hashtags optimized! 🎉")
                except Exception as e:
                    st.error(f"Error: {e}")

    with out:
        if "h_res" in st.session_state:
            tags = st.session_state["h_res"]
            hashtag_chips(tags, "Optimized Hashtags")

            st.code(" ".join(tags), language=None)
            copy_btn(" ".join(tags), "ch")

            dc1, dc2 = st.columns(2)
            with dc1:
                dl_text(format_hashtag_output(tags), f"hashtags_{hb.replace(' ','_')}.txt")
            with dc2:
                if st.button("🔄 Regenerate", key="h_re"):
                    st.session_state.pop("h_res", None)
                    st.rerun()
        else:
            empty_state("#️⃣", "Your optimized hashtags will appear here.")


# ── Footer ────────────────────────────────────────────────────────────────
st.markdown('<p class="ft">AI Content Studio · Streamlit & Groq · © 2026</p>', unsafe_allow_html=True)
