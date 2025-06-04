import streamlit as st
import requests
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam


client = OpenAI(api_key=st.secrets["OpenAI_API_KEY"])
GOOGLE_FACT_CHECK_API_KEY = st.secrets["GOOGLE_FACT_CHECK_API_KEY"]

def ask_openai_about_claim(claim: str):
    messages: list[ChatCompletionMessageParam] = [
        {"role": "system", "content": "You are a fact-checking assistant. Respond with whether the claim is true, false, or uncertain. Be concise."},
        {"role": "user", "content": f"Is the following claim true or false? Explain briefly:\n\n{claim}"}
    ]

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.2,
            max_tokens=200
        )
        return response.choices[0].message.content.strip(), "openai"
    except Exception as e:
        return f"⚠️ OpenAI error: {e}", None


def search_google_fact_check(claim: str):
    url = "https://factchecktools.googleapis.com/v1alpha1/claims:search"
    params = {
        "query": claim,
        "key": GOOGLE_FACT_CHECK_API_KEY
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        return f"❌ API error: {response.status_code}"

    data = response.json()
    if "claims" not in data:
        return "❌ No matching fact check found."

    top = data["claims"][0]
    reviewed_text = top.get("text", "No text")
    review = top.get("claimReview", [{}])[0]
    verdict = review.get("textualRating", "Unknown")
    publisher = review.get("publisher", {}).get("name", "Unknown")
    url = review.get("url", "")

    return f"""
✅ **Claim**: {reviewed_text}  
📢 **Verdict**: {verdict}  
🔗 **Source**: {publisher}  
🌐 [Read more]({url})
"""

# UI layout
st.title("🕵️ Fact Checker")
st.write("Paste a claim or Facebook post text:")

claim_input = st.text_area("Claim:", height=150)

if st.button("Check Fact"):
    if "facebook.com" in claim_input:
        st.warning("Facebook links are not supported. Please paste the text instead.")
    elif not claim_input.strip():
        st.error("Please enter a claim.")
    else:
        with st.spinner("Checking with Google..."):
            result = search_google_fact_check(claim_input.strip())

        if result.startswith("❌"):
            st.info("No verified fact check found. Asking ChatGPT instead...")
            with st.spinner("Consulting AI..."):
                ai_result, source = ask_openai_about_claim(claim_input.strip())
                st.markdown("### 🧠 AI Verdict (GPT)")
                st.markdown(
                    f"""
                    <div style="background-color:#1e1e1e;padding:15px;border-radius:10px;border:1px solid #4A4A4A;">
                        <p style="font-size:16px;color:white;">{ai_result}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            st.markdown(result)
