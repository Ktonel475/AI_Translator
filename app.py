import streamlit as st
from Agent.translator import Translator

st.title("🌐 Smart KB Translator")

translate = Translator()

# Text input
text = st.text_area("📄 Paste your article here:", height=300)

# Language selection
col1, col2 = st.columns(2)
with col1:
    src_lang = st.selectbox(
        "Source language (optional)",
        ["Auto Detect", "English", "French", "Chinese", "Thai", "Japanese"],
        index=0,
    )
    src_lang = None if src_lang == "Auto Detect" else src_lang

with col2:
    target_lang = st.selectbox(
        "Target language",
        ["French", "Spanish", "Arabic", "Chinese", "Thai", "Japanese"],
        index=0
    )

# Translate button
if st.button("Translate"):
    if not text.strip():
        st.warning("Please paste some text before translating.")
    else:
        with st.spinner("Translating..."):
            translated = translate.translate(text, src_lang=src_lang, target_lang=target_lang)
            st.text_area("✅ Translated Output", translated, height=300)
            st.download_button("💾 Download", translated, file_name="translated.md")
