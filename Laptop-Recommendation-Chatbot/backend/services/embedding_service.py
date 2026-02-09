"""
Embedding service using OpenAI text-embedding-3-small
Includes caching for performance optimization
"""
from typing import List, Dict, Optional
import hashlib
import json
import os
from openai import OpenAI
from core.config import settings
import pickle
from pathlib import Path

class EmbeddingService:
    """Generate and cache embeddings using OpenAI"""
    
    def __init__(self, cache_dir: str = "./embeddings_cache"):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = "text-embedding-3-small"
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self._cache = {}
        self._load_cache()
    
    def _get_cache_key(self, text: str) -> str:
        """Generate cache key from text"""
        return hashlib.md5(text.encode()).hexdigest()
    
    def _get_cache_path(self, cache_key: str) -> Path:
        """Get file path for cached embedding"""
        return self.cache_dir / f"{cache_key}.pkl"
    
    def _load_cache(self):
        """Load existing cache from disk"""
        try:
            cache_index = self.cache_dir / "cache_index.json"
            if cache_index.exists():
                with open(cache_index, 'r') as f:
                    self._cache = json.load(f)
                print(f"Loaded {len(self._cache)} cached embeddings")
        except Exception as e:
            print(f"Could not load cache: {e}")
            self._cache = {}
    
    def _save_cache_index(self):
        """Save cache index to disk"""
        try:
            cache_index = self.cache_dir / "cache_index.json"
            with open(cache_index, 'w') as f:
                json.dump(self._cache, f)
        except Exception as e:
            print(f"Could not save cache index: {e}")
    
    def _get_from_cache(self, cache_key: str) -> Optional[List[float]]:
        """Retrieve embedding from cache"""
        if cache_key in self._cache:
            cache_path = self._get_cache_path(cache_key)
            if cache_path.exists():
                try:
                    with open(cache_path, 'rb') as f:
                        return pickle.load(f)
                except Exception as e:
                    print(f"Error loading cached embedding: {e}")
        return None
    
    def _save_to_cache(self, cache_key: str, embedding: List[float]):
        """Save embedding to cache"""
        try:
            cache_path = self._get_cache_path(cache_key)
            with open(cache_path, 'wb') as f:
                pickle.dump(embedding, f)
            self._cache[cache_key] = True
            self._save_cache_index()
        except Exception as e:
            print(f"Error saving to cache: {e}")
    
    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for text with caching
        
        Args:
            text: Text to embed
            
        Returns:
            List of floats representing the embedding vector
        """
        # Check cache first
        cache_key = self._get_cache_key(text)
        cached_embedding = self._get_from_cache(cache_key)
        
        if cached_embedding is not None:
            return cached_embedding
        
        # Generate new embedding
        try:
            response = self.client.embeddings.create(
                model=self.model,
                input=text,
                encoding_format="float"
            )
            embedding = response.data[0].embedding
            
            # Cache the result
            self._save_to_cache(cache_key, embedding)
            
            return embedding
            
        except Exception as e:
            print(f"Error generating embedding: {e}")
            raise
    
    def generate_embeddings_batch(
        self,
        texts: List[str],
        batch_size: int = 100
    ) -> List[List[float]]:
        """
        Generate embeddings for multiple texts with batching
        
        Args:
            texts: List of texts to embed
            batch_size: Number of texts to process at once
            
        Returns:
            List of embedding vectors
        """
        embeddings = []
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            
            # Check cache for each text
            batch_embeddings = []
            texts_to_generate = []
            indices_to_generate = []
            
            for idx, text in enumerate(batch):
                cache_key = self._get_cache_key(text)
                cached = self._get_from_cache(cache_key)
                
                if cached is not None:
                    batch_embeddings.append((idx, cached))
                else:
                    texts_to_generate.append(text)
                    indices_to_generate.append(idx)
            
            # Generate embeddings for uncached texts
            if texts_to_generate:
                try:
                    response = self.client.embeddings.create(
                        model=self.model,
                        input=texts_to_generate,
                        encoding_format="float"
                    )
                    
                    for idx, text, data in zip(
                        indices_to_generate,
                        texts_to_generate,
                        response.data
                    ):
                        embedding = data.embedding
                        batch_embeddings.append((idx, embedding))
                        
                        # Cache the result
                        cache_key = self._get_cache_key(text)
                        self._save_to_cache(cache_key, embedding)
                        
                except Exception as e:
                    print(f"Error generating batch embeddings: {e}")
                    raise
            
            # Sort by original index and extract embeddings
            batch_embeddings.sort(key=lambda x: x[0])
            embeddings.extend([emb for _, emb in batch_embeddings])
        
        return embeddings
    
    def clear_cache(self):
        """Clear all cached embeddings"""
        try:
            for file in self.cache_dir.glob("*.pkl"):
                file.unlink()
            
            cache_index = self.cache_dir / "cache_index.json"
            if cache_index.exists():
                cache_index.unlink()
            
            self._cache = {}
            print("Cache cleared successfully")
        except Exception as e:
            print(f"Error clearing cache: {e}")
    
    def get_cache_stats(self) -> Dict[str, int]:
        """Get cache statistics"""
        return {
            "cached_embeddings": len(self._cache),
            "cache_size_mb": sum(
                f.stat().st_size for f in self.cache_dir.glob("*.pkl")
            ) / (1024 * 1024)
        }
