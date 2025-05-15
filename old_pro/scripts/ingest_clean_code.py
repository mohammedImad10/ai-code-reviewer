import os
import fitz  # PyMuPDF
import pickle
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

# Step 1: Extract text from PDF
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

pdf_path = "../data/clean_code.pdf"
os.makedirs("data", exist_ok=True)
pdf_text = extract_text_from_pdf(pdf_path)

with open("../data/clean_code.txt", "w", encoding="utf-8") as f:
    f.write(pdf_text)
print("✅ Text extracted and saved to data/clean_code.txt")

# Step 2: Chunk the text
def load_and_chunk_text(file_path, chunk_size=500, overlap=100):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk.strip())
        start += chunk_size - overlap  # maintain overlap
    return chunks

chunks = load_and_chunk_text("../data/clean_code.txt")
print(f"✅ Total chunks created: {len(chunks)}")

# Step 3: Generate embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(chunks, show_progress_bar=True)
print("✅ Embeddings generated.")

# Step 4: Save embeddings to FAISS index
embedding_matrix = np.array(embeddings).astype("float32")
index = faiss.IndexFlatL2(embedding_matrix.shape[1])
index.add(embedding_matrix)

faiss.write_index(index, "../data/clean_code.index")
with open("../data/clean_code_chunks.pkl", "wb") as f:
    pickle.dump(chunks, f)

print("✅ FAISS index and chunk list saved.")
