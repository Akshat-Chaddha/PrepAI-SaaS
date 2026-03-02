from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')

def calculate_ats_score(resume_text, job_description):

    # 1️⃣ Semantic similarity
    embeddings = model.encode([resume_text, job_description])
    similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]

    semantic_score = similarity * 100

    # 2️⃣ Keyword match
    vectorizer = TfidfVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform([resume_text, job_description])
    keyword_score = cosine_similarity(vectors[0], vectors[1])[0][0] * 100

    # 3️⃣ Combine
    final_score = int((semantic_score * 0.6) + (keyword_score * 0.4))

    strengths = []
    weaknesses = []

    if final_score > 75:
        strengths.append("Strong keyword alignment")
    else:
        weaknesses.append("Low keyword match")

    return final_score, strengths, weaknesses