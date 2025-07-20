import streamlit as st
import requests

st.title("💬 DeepSeek Q&A Bot")
question = st.text_input("Ask your question:")
button = st.button("Get Answer")

if button and question:
    with st.spinner("Thinking..."):
        headers = {
            "Authorization": "Bearer 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", 
            "HTTP-Referer": "https://deepseek.com",
            "Content-Type": "application/json"
        }
        data = {
            "model": "mistralai/mistral-7b-instruct:free",
            "messages": [
                {"role": "user", "content": question}
            ]
        }
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        if response.status_code == 200:
            answer = response.json()["choices"][0]["message"]["content"]
            st.write("**Answer:**", answer)
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
