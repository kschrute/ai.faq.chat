from sentence_transformers import SentenceTransformer
import faiss
import json
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')
with open('faq.json', 'r') as f:
    faq = json.load(f)

questions = [q['question'] for q in faq]
answers = [q['answer'] for q in faq]
embeddings = model.encode(questions)

# Faiss index
index = faiss.IndexFlatL2(embeddings.shape[1])
embeddings = np.array(embeddings, dtype=np.float32)
index.add(embeddings)
faiss.write_index(index, 'faq_index.faiss')

# Save answers (for retrieval)
with open('answers.json', 'w') as f:
    json.dump(answers, f)