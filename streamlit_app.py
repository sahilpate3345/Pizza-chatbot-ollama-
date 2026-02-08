import streamlit as st
import requests

st.set_page_config(
    page_title="🍕 Pizza AI Agent",
    page_icon="🍕",
    layout="centered"
)

st.title("🍕 Pizza Restaurant Chatbot")
st.write("Ask questions based on real customer reviews.")

# Input box
question = st.text_input(
    "Ask a question about the restaurant:",
    placeholder="e.g. Is the pizza fresh?"
)

# Ask button
if st.button("Ask"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        try:
            response = requests.post(
                "http://127.0.0.1:8000/ask",
                json={"question": question},
                timeout=120
            )

            if response.status_code == 200:
                st.markdown("### ✅ Answer")
                st.write(response.json()["answer"])
            else:
                st.error("❌ Server error. Try again.")

        except requests.exceptions.ConnectionError:
            st.error("❌ FastAPI server is not running on port 8000.")
        except Exception as e:
            st.error(f"❌ Error: {e}")
