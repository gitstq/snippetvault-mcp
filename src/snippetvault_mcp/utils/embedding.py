"""Embedding generation for semantic search."""

import os
from typing import List, Optional
import numpy as np


class EmbeddingGenerator:
    """Generate embeddings for text using sentence-transformers."""
    
    def __init__(self, model_name: Optional[str] = None):
        """
        Initialize the embedding generator.
        
        Args:
            model_name: Name of the sentence-transformers model to use.
                       If None, uses a lightweight default model.
        """
        self.model_name = model_name or "all-MiniLM-L6-v2"
        self._model = None
        self._embedding_dim = 384  # Default for all-MiniLM-L6-v2
    
    def _load_model(self):
        """Lazy load the embedding model."""
        if self._model is None:
            try:
                from sentence_transformers import SentenceTransformer
                
                # Check if model should be downloaded
                cache_dir = os.path.expanduser("~/.cache/snippetvault/models")
                os.makedirs(cache_dir, exist_ok=True)
                
                self._model = SentenceTransformer(
                    self.model_name,
                    cache_folder=cache_dir
                )
                self._embedding_dim = self._model.get_sentence_embedding_dimension()
            except ImportError:
                raise ImportError(
                    "sentence-transformers is required for semantic search. "
                    "Install with: pip install sentence-transformers"
                )
            except Exception as e:
                # Fallback to simple embeddings if model loading fails
                print(f"Warning: Could not load embedding model: {e}")
                print("Falling back to simple keyword-based embeddings")
                self._model = None
    
    def generate(self, text: str) -> List[float]:
        """
        Generate embedding for a single text.
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding vector as list of floats
        """
        self._load_model()
        
        if self._model is None:
            # Fallback: simple keyword-based embedding
            return self._simple_embedding(text)
        
        embedding = self._model.encode(text, convert_to_numpy=True)
        return embedding.tolist()
    
    def generate_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts.
        
        Args:
            texts: List of texts to embed
            
        Returns:
            List of embedding vectors
        """
        if not texts:
            return []
        
        self._load_model()
        
        if self._model is None:
            return [self._simple_embedding(t) for t in texts]
        
        embeddings = self._model.encode(texts, convert_to_numpy=True)
        return [e.tolist() for e in embeddings]
    
    def _simple_embedding(self, text: str, dim: int = 384) -> List[float]:
        """
        Generate a simple keyword-based embedding as fallback.
        This is not as good as neural embeddings but works without the model.
        
        Args:
            text: Text to embed
            dim: Embedding dimension
            
        Returns:
            Simple embedding vector
        """
        # Simple hash-based embedding
        words = text.lower().split()
        embedding = np.zeros(dim)
        
        for i, word in enumerate(words):
            # Hash the word and distribute across dimensions
            hash_val = hash(word) % dim
            embedding[hash_val] += 1.0
        
        # Normalize
        norm = np.linalg.norm(embedding)
        if norm > 0:
            embedding = embedding / norm
        
        return embedding.tolist()
    
    @property
    def embedding_dim(self) -> int:
        """Get the embedding dimension."""
        return self._embedding_dim
    
    def cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """
        Calculate cosine similarity between two vectors.
        
        Args:
            vec1: First vector
            vec2: Second vector
            
        Returns:
            Cosine similarity (0-1)
        """
        v1 = np.array(vec1)
        v2 = np.array(vec2)
        
        norm1 = np.linalg.norm(v1)
        norm2 = np.linalg.norm(v2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return float(np.dot(v1, v2) / (norm1 * norm2))


# Global embedding generator instance
_embedding_generator: Optional[EmbeddingGenerator] = None


def get_embedding_generator() -> EmbeddingGenerator:
    """Get or create the global embedding generator."""
    global _embedding_generator
    if _embedding_generator is None:
        model_name = os.getenv("SNIPPETVAULT_EMBEDDING_MODEL", "all-MiniLM-L6-v2")
        _embedding_generator = EmbeddingGenerator(model_name)
    return _embedding_generator
