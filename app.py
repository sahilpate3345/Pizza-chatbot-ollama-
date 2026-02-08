from fastapi import FastAPI
from pydantic import BaseModel
from main import ask_pizza_bot

app = FastAPI(title="🍕 Pizza AI Agent")

# Request body schema
class Question(BaseModel):
    question: str

# Health check (http://127.0.0.1:8000/)
@app.get("/")
def root():
    return {"message": "Pizza AI Agent is running 🚀"}

# Main API endpoint (http://127.0.0.1:8000/ask)
@app.post("/ask")
def ask(query: Question):
    answer = ask_pizza_bot(query.question)
    return {"answer": answer}
