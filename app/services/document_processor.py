from typing import List, Dict
from pathlib import Path
import pandas as pd
from .vector_store import VectorStore
import re

class DocumentProcessor:
    def __init__(self, data_dir: str = "resources/data"):
        self.data_dir = Path(data_dir)
        self.vector_store = VectorStore()
        self.chunk_size = 500  # words per chunk
        self.chunk_overlap = 50  # overlap between chunks

    def chunk_text(self, text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
        # Split by paragraphs, then merge into chunks of ~chunk_size words
        paragraphs = re.split(r'\n{2,}', text)
        chunks = []
        current_chunk = []
        current_len = 0
        for para in paragraphs:
            words = para.split()
            if current_len + len(words) > chunk_size and current_chunk:
                chunks.append(' '.join(current_chunk))
                # Overlap
                if overlap > 0:
                    current_chunk = current_chunk[-overlap:]
                    current_len = len(current_chunk)
                else:
                    current_chunk = []
                    current_len = 0
            current_chunk.extend(words)
            current_len += len(words)
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        return chunks

    def load_documents(self):
        """Load, chunk, and index all documents from the data directory for RAG."""
        for role_dir in self.data_dir.iterdir():
            if not role_dir.is_dir():
                continue
            role = role_dir.name
            for file_path in role_dir.glob("**/*"):
                if file_path.is_file():
                    try:
                        if file_path.suffix in ['.md', '.txt']:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                        elif file_path.suffix == '.csv':
                            df = pd.read_csv(file_path)
                            content = df.to_string()
                        else:
                            continue
                        # Chunk the content
                        chunks = self.chunk_text(content, self.chunk_size, self.chunk_overlap)
                        documents = []
                        metadatas = []
                        ids = []
                        for i, chunk in enumerate(chunks):
                            documents.append(chunk)
                            metadatas.append({
                                "source": str(file_path),
                                "role": role,
                                "chunk_index": i
                            })
                            ids.append(f"{file_path}::chunk_{i}")
                        if documents:
                            self.vector_store.add_documents(
                                role=role,
                                documents=documents,
                                metadatas=metadatas,
                                ids=ids
                            )
                    except Exception as e:
                        print(f"Error processing {file_path}: {e}")

    def get_relevant_documents(self, role: str, query: str, n_results: int = 8) -> List[Dict]:
        """Get relevant document chunks for a query based on role (or all roles if role='all')."""
        if role == 'all':
            results = []
            for r in [d.name for d in self.data_dir.iterdir() if d.is_dir()]:
                results.extend(self.vector_store.search(r, query, n_results=n_results))
            # Sort by score descending
            results = sorted(results, key=lambda x: -x.get('score', 0))
            return results[:n_results]
        else:
            return self.vector_store.search(role, query, n_results=n_results) 