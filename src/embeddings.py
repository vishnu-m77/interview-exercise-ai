import openai
import faiss
import numpy as np
from .config import settings

class Encoder:
    def __init__(self):
        self.client = openai.OpenAI(api_key=settings.openai_api_key)
        self.model = settings.embedding_model
        self.dimensions = settings.vector_dimension

    def get_encoding(self, text):
        response = self.client.embeddings.create(
            model=self.model,
            input=text,
            dimensions=self.dimensions
        )
        return np.array([item.embedding for item in response.data])
    

class VectorStore:
    def __init__(self):
        self.dimension = settings.vector_dimension
        self.index = None
        self.top_k_results = settings.top_k_results
        self.documents = []
    
    def add_documents(self, documents, embeddings):
        embeddings = np.asarray(embeddings, dtype=np.float32, order="C")

        if self.index is None:
            self.dimension = embeddings.shape[1]
            faiss.normalize_L2(embeddings)
            self.index = faiss.IndexFlatIP(self.dimension)
        else:
            if embeddings.shape[1] != self.dimension:
                raise ValueError("Embedding dimension mismatch")
            faiss.normalize_L2(embeddings)
        
        self.index.add(embeddings)
        self.documents.extend(documents)
    
    def search(self, query_embedding):
        query_embedding = np.asarray(query_embedding, dtype=np.float32, order="C")
        query_embedding = query_embedding.reshape(1, -1)
        if query_embedding.shape[1] != self.dimension:
            raise ValueError("Query embedding dimension mismatch")

        faiss.normalize_L2(query_embedding)
        k = min(self.top_k_results, self.index.ntotal)
        scores, indices = self.index.search(query_embedding, k)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < len(self.documents):
                document = self.documents[idx]
                similarity_score = float(score)
                results.append((document, similarity_score))
        
        return results
