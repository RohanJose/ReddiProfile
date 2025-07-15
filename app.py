import os
import re
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain import PromptTemplate, LLMChain
import praw


load_dotenv()


model = ChatGroq(
    groq_api_key=os.getenv("groq_api_key"),
    model_name="llama-3.3-70b-versatile",
    streaming=True
)


prompt = """
You are an expert behavioral analyst AI.
Your job is to read the following **Reddit posts** and **Reddit comments** by a single user, and create a comprehensive **User Persona**.

---

**📝 Persona Structure**

1️⃣ **Name:** Create a creative nickname inspired by their username or style.

2️⃣ **Age Group:** Estimate an age bracket (e.g., 18–24, 25–34) using hints in their posts and comments.

3️⃣ **Occupation / Background:** Suggest what they might do for a living, their education, or general background clues.

4️⃣ **Personality Traits:** List 3–5 traits, each with a short reason (e.g., humorous, analytical, supportive, skeptical).

5️⃣ **Main Interests:** What topics do they care about? (Look at posts + comments.)

6️⃣ **Goals & Motivations:** What do they want or care about most?

7️⃣ **Pain Points & Frustrations:** Any complaints, struggles, or dislikes that repeat?

8️⃣ **Top Subreddits / Topics:** List the communities or topics they are most active in.

9️⃣ **Writing Style:** Describe their tone — formal, sarcastic, witty, supportive, short, long-winded, factual, ranting, etc.

🔟 **Sample Quotes:** Include 1 short post **and** 1 short comment that capture their tone.

1️⃣1️⃣ **Evidence:** For every trait or claim, include a matching snippet or short line that supports it.

---

**📌 Output Guidelines**

- Use clear markdown headings for each section.
- Be specific but do not make up information.
- Use exact snippets from posts/comments for evidence.
- Keep the final persona realistic, factual, and based only on the provided text.

---

**User Posts:**  
{USER_POSTS}

---

**User Comments:**  
{USER_COMMENTS}
"""


reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
)


def extract_username(url: str) -> str | None:
    match = re.search(r"reddit\.com\/user\/([A-Za-z0-9_\-]+)", url)
    return match.group(1) if match else None


def get_user_data(username: str):
    redditor = reddit.redditor(username)
    posts, comments = [], []
    for post in redditor.submissions.new(limit=10):
        posts.append(f"Title: {post.title}\nBody: {post.selftext}\n")
    for comment in redditor.comments.new(limit=10):
        comments.append(f"Comment: {comment.body}\n")
    return posts, comments


llm_chain = LLMChain(llm=model, prompt=PromptTemplate.from_template(prompt))


st.title("🔍 Reddit Persona Generator")
url = st.text_input("Enter Reddit Profile URL", "https://www.reddit.com/user/kojied")

if st.button("Generate Persona"):
    with st.spinner("Fetching Reddit data..."):
        username = extract_username(url)
        if not username:
            st.error("Invalid Reddit URL.")
        else:
            posts, comments = get_user_data(username)
            with st.spinner("Generating Persona..."):
                response = llm_chain.invoke({
                    "USER_POSTS": "\n".join(posts),
                    "USER_COMMENTS": "\n".join(comments)
                })
                st.markdown("### ✅ Persona Generated")
                st.markdown(response['text'])
                
                # Save to file
                filename = f"{username}_persona.txt"
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(response['text'])
                st.success(f"Persona saved to `{filename}`")
                st.download_button(
                    label="📄 Download Persona",
                    data=response['text'],
                    file_name=filename,
                    mime="text/plain"
                )
