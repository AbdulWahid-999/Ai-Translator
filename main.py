import streamlit as st
import requests
import os


# Load environment variables from .env file

API_KEY = os.getenv("OPENROUTER_API_KEY")

st.set_page_config(page_title="AI Translator", page_icon="🌍")
st.title("🌍 AI Translator with OpenRouter")

# User input
text = st.text_area("Enter text to translate")
src_lang = st.selectbox("From Language", ["English", "Urdu", "French", "Spanish", "German" , "Chinese", "Japanese", "Korean"])
tgt_lang = st.selectbox("To Language", ["English", "Urdu", "French", "Spanish", "German" , "Chinese", "Japanese", "Korean"])

if st.button("Translate"):
    if not API_KEY:
        st.error("❌ API key not found. Please check your `.env` file.")
    elif text.strip() == "":
        st.warning("⚠️ Please enter some text.")
    else:
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

       
        data = {
            "model": "deepseek/deepseek-chat",
            "messages": [
                {
                    "role": "user",
                    "content": f"Translate and summarize this from {src_lang} to {tgt_lang}:\n\n{text}"
                }
            ]
        }

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data
        )

        # Handle and display response
        try:
            result = response.json()
        except Exception as e:
            st.error("❌ Failed to parse API response.")
            st.write(response.text)
            raise e

        if response.status_code == 200 and "choices" in result:
            translated = result["choices"][0]["message"]["content"]
            st.success("✅ Translation:")
            st.write(translated)
        else:
            st.error(f"❌ Failed to translate (HTTP {response.status_code})")
            st.write("Full response from OpenRouter:")
            st.code(result, language='json')
