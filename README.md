# 🕵️‍♂️ FactCheck – AI-Powered Claim Verification App

**FactCheck** is a simple and accessible web app that allows anyone to verify the accuracy of a claim using:
- ✅ Verified sources via Google Fact Check Tools API
- 🤖 AI reasoning from OpenAI's GPT-3.5-turbo when no official fact-check is found

It's built using Python and Streamlit, designed for both educational and real-world use.

---

## 🌐 Live Demo
👉 [Launch the app](https://ketevan7-factcheck.streamlit.app/)

---

## 💡 Features
- 🔍 Paste a claim or Facebook post text
- 🧠 Checks official sources first (Google Fact Check API)
- 🤔 If no match, uses GPT to give a logical verdict
- 📊 Verdicts are labeled as:
  - ✅ Likely True
  - ❌ Likely False
  - ⚠️ Uncertain

---

## 🚀 Technologies
- [Streamlit](https://streamlit.io/) — UI framework
- [OpenAI API](https://platform.openai.com/) — GPT-3.5-turbo
- [Google Fact Check Tools API](https://developers.google.com/fact-check/tools/api) — verified claim sources
- `requests`, `openai` — Python libraries

---

## 📦 Installation

```bash
# Clone the repo
git clone https://github.com/Ketevan7/FactCheck.git
cd FactCheck

# Create virtual environment (optional but recommended)
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
