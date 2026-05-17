"""Local JSON file storage backend."""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from .base import StorageBackend
from ..models.snippet import Snippet, SnippetSearchResult
from ..utils.embedding import get_embedding_generator


class LocalStorage(StorageBackend):
    """Local file-based storage using JSON."""
    
    def __init__(self, data_dir: Optional[str] = None):
        """
        Initialize local storage.
        
        Args:
            data_dir: Directory to store data files. Defaults to ~/.snippetvault
        """
        if data_dir is None:
            data_dir = os.path.expanduser("~/.snippetvault")
        
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.snippets_file = self.data_dir / "snippets.json"
        self._cache: Dict[str, Snippet] = {}
        self._loaded = False
    
    def _load_data(self):
        """Load all snippets from disk."""
        if self._loaded:
            return
        
        self._cache = {}
        
        if self.snippets_file.exists():
            try:
                with open(self.snippets_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for item in data:
                        # Convert datetime strings back to datetime objects
                        if "created_at" in item and isinstance(item["created_at"], str):
                            item["created_at"] = datetime.fromisoformat(item["created_at"])
                        if "updated_at" in item and isinstance(item["updated_at"], str):
                            item["updated_at"] = datetime.fromisoformat(item["updated_at"])
                        snippet = Snippet(**item)
                        self._cache[snippet.id] = snippet
            except (json.JSONDecodeError, Exception) as e:
                print(f"Warning: Could not load snippets: {e}")
                self._cache = {}
        
        self._loaded = True
    
    def _save_data(self):
        """Save all snippets to disk."""
        try:
            data = []
            for snippet in self._cache.values():
                item = snippet.model_dump()
                # Convert datetime objects to ISO format strings
                if isinstance(item.get("created_at"), datetime):
                    item["created_at"] = item["created_at"].isoformat()
                if isinstance(item.get("updated_at"), datetime):
                    item["updated_at"] = item["updated_at"].isoformat()
                data.append(item)
            
            with open(self.snippets_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving snippets: {e}")
            raise
    
    async def create(self, snippet: Snippet) -> Snippet:
        """Create a new snippet."""
        self._load_data()
        self._cache[snippet.id] = snippet
        self._save_data()
        return snippet
    
    async def get(self, snippet_id: str) -> Optional[Snippet]:
        """Get a snippet by ID."""
        self._load_data()
        snippet = self._cache.get(snippet_id)
        if snippet:
            # Update usage count
            snippet.usage_count += 1
            self._save_data()
        return snippet
    
    async def update(self, snippet: Snippet) -> Snippet:
        """Update an existing snippet."""
        self._load_data()
        if snippet.id not in self._cache:
            raise ValueError(f"Snippet with ID {snippet.id} not found")
        
        snippet.updated_at = datetime.utcnow()
        self._cache[snippet.id] = snippet
        self._save_data()
        return snippet
    
    async def delete(self, snippet_id: str) -> bool:
        """Delete a snippet by ID."""
        self._load_data()
        if snippet_id in self._cache:
            del self._cache[snippet_id]
            self._save_data()
            return True
        return False
    
    async def list_all(
        self,
        language: Optional[str] = None,
        tags: Optional[List[str]] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Snippet]:
        """List snippets with optional filtering."""
        self._load_data()
        
        snippets = list(self._cache.values())
        
        # Apply filters
        if language:
            snippets = [s for s in snippets if s.language == language]
        
        if tags:
            snippets = [s for s in snippets if any(t in s.tags for t in tags)]
        
        # Sort by updated_at (newest first)
        snippets.sort(key=lambda s: s.updated_at, reverse=True)
        
        # Apply pagination
        return snippets[offset:offset + limit]
    
    async def search(
        self,
        query_embedding: List[float],
        language: Optional[str] = None,
        tags: Optional[List[str]] = None,
        limit: int = 10,
        threshold: float = 0.3
    ) -> List[SnippetSearchResult]:
        """Search snippets by embedding similarity."""
        self._load_data()
        
        generator = get_embedding_generator()
        results = []
        
        for snippet in self._cache.values():
            # Apply filters
            if language and snippet.language != language:
                continue
            
            if tags and not any(t in snippet.tags for t in tags):
                continue
            
            # Calculate similarity if embedding exists
            if snippet.embedding:
                similarity = generator.cosine_similarity(query_embedding, snippet.embedding)
                if similarity >= threshold:
                    results.append(SnippetSearchResult(snippet=snippet, similarity=similarity))
            else:
                # Fallback: use title and code for simple matching
                text = f"{snippet.title} {snippet.code}"
                text_embedding = generator.generate(text)
                similarity = generator.cosine_similarity(query_embedding, text_embedding)
                if similarity >= threshold:
                    results.append(SnippetSearchResult(snippet=snippet, similarity=similarity))
        
        # Sort by similarity (highest first)
        results.sort(key=lambda r: r.similarity, reverse=True)
        
        return results[:limit]
    
    async def get_all_tags(self) -> List[str]:
        """Get all unique tags."""
        self._load_data()
        
        tags = set()
        for snippet in self._cache.values():
            tags.update(snippet.tags)
        
        return sorted(list(tags))
    
    async def get_stats(self) -> dict:
        """Get storage statistics."""
        self._load_data()
        
        total_snippets = len(self._cache)
        languages = {}
        total_tags = set()
        total_usage = 0
        
        for snippet in self._cache.values():
            lang = snippet.language or "unknown"
            languages[lang] = languages.get(lang, 0) + 1
            total_tags.update(snippet.tags)
            total_usage += snippet.usage_count
        
        return {
            "total_snippets": total_snippets,
            "total_tags": len(total_tags),
            "total_usage": total_usage,
            "languages": languages,
            "storage_path": str(self.data_dir),
        }
