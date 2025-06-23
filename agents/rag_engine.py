import os
import fitz  # PyMuPDF
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from utils.llm import ask_llm

PDF_DIR = "source"
EMBEDDING_MODEL = "intfloat/multilingual-e5-large-instruct"

def extract_text_from_pdfs(folder):
    texts = []
    for filename in os.listdir(folder):
        if filename.endswith(".pdf"):
            path = os.path.join(folder, filename)
            with fitz.open(path) as doc:
                text = "".join([page.get_text() for page in doc])
                texts.append(text.strip())
    return texts

def embed_documents(docs, model):
    docs_prefixed = [f"passage: {doc}" for doc in docs]
    return model.encode(docs_prefixed)

def retrieve(query, embedder, docs, doc_embeddings, k=2):
    query_embedding = embedder.encode([f"query: {query}"])
    similarities = cosine_similarity(query_embedding, doc_embeddings)[0]
    top_k = np.argsort(similarities)[::-1][:k]
    return [(docs[i], similarities[i]) for i in top_k]

def rag_answer(query, embedder, docs, doc_embeddings, k=2):
    retrieved_docs = retrieve(query, embedder, docs, doc_embeddings, k)
    context = "\n".join([doc for doc, _ in retrieved_docs])

    prompt = f"Voici les documents :\n{context}\n\nQuestion : {query}"
    system = "Tu es un assistant qui répond à des questions à partir des documents suivants. Si tu ne sais pas, n'invente pas. Réponds uniquement en français. </no_think>"

    return ask_llm(prompt=prompt, system=system)

def initialize_rag():
    docs = extract_text_from_pdfs(PDF_DIR)
    embedder = SentenceTransformer(EMBEDDING_MODEL)
    doc_embeddings = embed_documents(docs, embedder)
    return docs, embedder, doc_embeddings
