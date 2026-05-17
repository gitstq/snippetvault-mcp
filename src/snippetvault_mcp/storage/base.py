"""Abstract base class for storage backends."""

from abc import ABC, abstractmethod
from typing import List, Optional

from ..models.snippet import Snippet, SnippetSearchResult


class StorageBackend(ABC):
    """Abstract base class for snippet storage."""
    
    @abstractmethod
    async def create(self, snippet: Snippet) -> Snippet:
        """Create a new snippet."""
        pass
    
    @abstractmethod
    async def get(self, snippet_id: str) -> Optional[Snippet]:
        """Get a snippet by ID."""
        pass
    
    @abstractmethod
    async def update(self, snippet: Snippet) -> Snippet:
        """Update an existing snippet."""
        pass
    
    @abstractmethod
    async def delete(self, snippet_id: str) -> bool:
        """Delete a snippet by ID."""
        pass
    
    @abstractmethod
    async def list_all(
        self,
        language: Optional[str] = None,
        tags: Optional[List[str]] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Snippet]:
        """List snippets with optional filtering."""
        pass
    
    @abstractmethod
    async def search(
        self,
        query_embedding: List[float],
        language: Optional[str] = None,
        tags: Optional[List[str]] = None,
        limit: int = 10,
        threshold: float = 0.3
    ) -> List[SnippetSearchResult]:
        """Search snippets by embedding similarity."""
        pass
    
    @abstractmethod
    async def get_all_tags(self) -> List[str]:
        """Get all unique tags."""
        pass
    
    @abstractmethod
    async def get_stats(self) -> dict:
        """Get storage statistics."""
        pass
