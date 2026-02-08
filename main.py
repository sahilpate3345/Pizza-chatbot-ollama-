from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import retriever

# ✅ Local Ollama model (matches: ollama list)
llm = OllamaLLM(
    model="llama3.2:latest",
    num_ctx=1024,      # faster on low RAM
    temperature=0.1   # reduces hallucination
)

# 🎯 Strict RAG prompt (allows inference only from reviews)
template = """
You are an AI assistant answering questions about a pizza restaurant
using ONLY customer reviews.

RULES:
- If the user greets (hi, hello, hey), respond politely.
- Use ONLY the information present in the reviews.
- You MAY summarize or infer patterns ONLY if supported by multiple reviews.
- Do NOT invent menu items, ingredients, timings, or features.
- If reviews do not support an answer, reply EXACTLY:
  "The reviews do not mention this."

Reviews:
{context}

Question:
{question}

Answer:
"""

prompt = ChatPromptTemplate.from_template(template)

def ask_pizza_bot(question: str) -> str:
    q = question.lower().strip()

    # 👋 Greeting shortcut (no LLM call)
    if q in {"hi", "hello", "hey"}:
        return "Hi! 👋 Ask me anything about the pizza restaurant based on customer reviews."

    # 🔍 Retrieve relevant reviews
    docs = retriever.invoke(question)
    if not docs:
        return "The reviews do not mention this."

    context = "\n".join(doc.page_content for doc in docs)

    # 🧠 Run RAG chain
    chain = prompt | llm
    response = chain.invoke({
        "context": context,
        "question": question
    })

    return response



