import pytest
import numpy as np
from src.embeddings import Encoder, VectorStore
from src.config import settings

def test_encoder_init():
    encoder = Encoder()
    assert encoder.model == settings.embedding_model
    assert encoder.dimensions == settings.vector_dimension
    assert encoder.client is not None

def test_vector_store_init():
    store = VectorStore()
    assert store.dimension == settings.vector_dimension
    assert store.top_k_results == settings.top_k_results
    assert store.index is None
    assert store.documents == []

def test_add_documents():
    store = VectorStore()
    documents = [{"content" : "test_1", "content": "test_2"}]
    embeddings = [[0.1, 0.2], [0.3, 0.4]]
    embeddings = np.array(embeddings, dtype=np.float32)
    store.add_documents(documents=documents, embeddings=embeddings)

    assert store.index is not None
    assert store.documents[0] is not None
    assert store.index.ntotal == 2

def test_search():
    store = VectorStore()
    documents = [{"content" : "test_1", "content": "test_2"}]
    embeddings = [[0.1, 0.2], [0.3, 0.4]]
    embeddings = np.array(embeddings, dtype=np.float32)
    store.add_documents(documents=documents, embeddings=embeddings)

    query = [0.1, 0.2]
    query = np.array(query, dtype=np.float32)
    results = store.search(query)

    assert results is not None
    assert all(isinstance(score, float) for _, score in results)
    assert all(isinstance(doc, dict) for doc, _ in results)

def test_dimensions():
    store = VectorStore()
    documents = [{"content" : "test_1", "content": "test_2"}]
    embeddings1 = [[0.1, 0.2]]
    embeddings2 = [[0.3, 0.4, 0.5]]
    embeddings1 = np.array(embeddings1, dtype=np.float32)
    embeddings2 = np.array(embeddings2, dtype=np.float32)
    store.add_documents(documents=documents, embeddings=embeddings1)

    with pytest.raises(ValueError):
        store.add_documents(documents=documents, embeddings=embeddings2)


