from typing import List, Dict
import faiss
import numpy as np
import pickle
import os
from pathlib import Path
from sentence_transformers import SentenceTransformer

class VectorStore:
    def __init__(self, persist_directory: str = "resources/vector_store"):
        self.persist_directory = Path(persist_directory)
        self.persist_directory.mkdir(exist_ok=True)
        
        # Initialize sentence transformer
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Initialize FAISS indices and document storage for each role
        self.indices = {}
        self.documents = {}
        self.metadatas = {}
        self._initialize_indices()

    def _initialize_indices(self):
        """Initialize FAISS indices for each role"""
        roles = ["engineering", "finance", "hr", "marketing", "general"]
        
        for role in roles:
            index_path = self.persist_directory / f"{role}_index.faiss"
            docs_path = self.persist_directory / f"{role}_docs.pkl"
            meta_path = self.persist_directory / f"{role}_meta.pkl"
            
            if index_path.exists() and docs_path.exists() and meta_path.exists():
                # Load existing index
                self.indices[role] = faiss.read_index(str(index_path))
                with open(docs_path, 'rb') as f:
                    self.documents[role] = pickle.load(f)
                with open(meta_path, 'rb') as f:
                    self.metadatas[role] = pickle.load(f)
            else:
                # Create new index
                dimension = self.encoder.get_sentence_embedding_dimension()
                self.indices[role] = faiss.IndexFlatIP(dimension)  # Inner product for cosine similarity
                self.documents[role] = []
                self.metadatas[role] = []

    def _save_index(self, role: str):
        """Save FAISS index and documents to disk"""
        index_path = self.persist_directory / f"{role}_index.faiss"
        docs_path = self.persist_directory / f"{role}_docs.pkl"
        meta_path = self.persist_directory / f"{role}_meta.pkl"
        
        faiss.write_index(self.indices[role], str(index_path))
        with open(docs_path, 'wb') as f:
            pickle.dump(self.documents[role], f)
        with open(meta_path, 'wb') as f:
            pickle.dump(self.metadatas[role], f)

    def add_documents(self, role: str, documents: List[str], metadatas: List[Dict], ids: List[str]):
        """Add document chunks to the specified role's index. Each chunk has its own metadata (including source and chunk index)."""
        if role not in self.indices:
            raise ValueError(f"Invalid role: {role}")
        
        # Encode documents
        embeddings = self.encoder.encode(documents, show_progress_bar=True)
        
        # Add to FAISS index
        self.indices[role].add(embeddings.astype('float32'))
        
        # Store documents and metadata
        for doc, meta, id_ in zip(documents, metadatas, ids):
            self.documents[role].append(doc)
            self.metadatas[role].append(meta)
        
        # Save to disk
        self._save_index(role)

    def search(self, role: str, query: str, n_results: int = 5) -> List[Dict]:
        """Search for relevant document chunks in the specified role's index. Returns chunk metadata."""
        if role not in self.indices:
            raise ValueError(f"Invalid role: {role}")
        if len(self.documents[role]) == 0:
            return []  # No documents to search!
        query_embedding = self.encoder.encode([query])
        k = min(n_results, len(self.documents[role]))
        if k == 0:
            return []
        scores, indices = self.indices[role].search(
            query_embedding.astype('float32'),
            k
        )
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < len(self.documents[role]):
                results.append({
                    "document": self.documents[role][idx],
                    "metadata": self.metadatas[role][idx],
                    "score": float(score)
                })
        return results

    def get_all_documents(self, role: str) -> List[Dict]:
        """Get all documents for a specific role"""
        if role not in self.indices:
            raise ValueError(f"Invalid role: {role}")
        
        return [
            {
                "document": doc,
                "metadata": meta
            }
            for doc, meta in zip(self.documents[role], self.metadatas[role])
        ] 