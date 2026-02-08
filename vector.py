from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
import pandas as pd
import os
import shutil

# Load CSV
df = pd.read_csv("realistic_restaurant_reviews.csv")

# Embeddings
embeddings = OllamaEmbeddings(model="mxbai-embed-large")

DB_DIR = "./chroma_langchain_db"

# Rebuild DB every time (important for correctness)
if os.path.exists(DB_DIR):
    shutil.rmtree(DB_DIR)

documents = []
ids = []

for i, row in df.iterrows():
    text = f"{row['Title']} {row['Review']}".lower()
    documents.append(
        Document(
            page_content=text,
            metadata={
                "rating": row["Rating"],
                "date": row["Date"]
            }
        )
    )
    ids.append(str(i))

vector_store = Chroma(
    collection_name="restaurant_reviews",
    persist_directory=DB_DIR,
    embedding_function=embeddings
)

vector_store.add_documents(documents=documents, ids=ids)

retriever = vector_store.as_retriever(search_kwargs={"k": 8})
