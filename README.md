# 🔍 ReddiProfile — Reddit User Persona Generator

**ReddiProfile** is an AI-powered tool that analyzes any Reddit user’s posts and comments to automatically generate a **detailed User Persona** — including personality traits, interests, writing style, goals, frustrations, and supporting evidence from real posts.

Built with **Python**, **LangChain**, **Groq LLM**, **PRAW**, and **Streamlit**, ReddiProfile turns a Reddit profile link into a rich behavioral snapshot — in just one click.

---

## Features

**Live Reddit Scraping** — Uses PRAW to securely fetch a user’s recent posts & comments.  
**Smart LLM Analysis** — Uses the Groq-powered LLaMA-3 model via LangChain to build a structured, realistic persona.  
**Persona Blueprint** — Outputs a clear markdown report: name, age group, traits, motivations, pain points, top subreddits, writing style, quotes, and evidence.  
**Streamlit UI** — Clean, no-code interface for easy persona generation.  
**Save & Download**

---

## ⚙️ Tech Stack

- Python 3.10+
- LangChain
- Groq LLM
- PRAW (Python Reddit API Wrapper)
- Streamlit
- dotenv for secure API keys

---

## 🗂️ Setup & Usage



1️⃣ **Clone this repo**

```bash
git clone https://github.com/RohanJose/ReddiProfile.git
cd ReddiProfile
```

2️⃣**Add your .env**
```bash
Create a .env file in the project root and add your keys:

groq_api_key=YOUR_GROQ_API_KEY
REDDIT_CLIENT_ID=YOUR_REDDIT_CLIENT_ID
REDDIT_CLIENT_SECRET=YOUR_REDDIT_CLIENT_SECRET
REDDIT_USER_AGENT=YOUR_REDDIT_USER_AGENT
```
3️⃣ **Install dependencies**
```bash
pip install -r requirements.txt
```
4️⃣ **Run the app**
```bash
streamlit run app.py
```

