"""Snippet management tools."""

from typing import List, Optional

from ..models.snippet import Snippet, SnippetCreate, SnippetSearchResult
from ..storage.base import StorageBackend
from ..utils.language import detect_language
from ..utils.embedding import get_embedding_generator


class SnippetTools:
    """Tools for managing code snippets."""
    
    def __init__(self, storage: StorageBackend):
        """
        Initialize snippet tools.
        
        Args:
            storage: Storage backend instance
        """
        self.storage = storage
        self.embedding_generator = get_embedding_generator()
    
    async def save_snippet(
        self,
        title: str,
        code: str,
        description: Optional[str] = None,
        language: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> dict:
        """
        Save a new code snippet.
        
        Args:
            title: Snippet title
            code: Code content
            description: Optional description
            language: Programming language (auto-detected if not provided)
            tags: List of tags
            
        Returns:
            Saved snippet information
        """
        # Auto-detect language if not provided
        if not language:
            language = detect_language(code)
        
        # Clean up tags
        tags = tags or []
        tags = [t.strip().lower() for t in tags if t.strip()]
        
        # Create snippet
        create_data = SnippetCreate(
            title=title,
            code=code,
            description=description,
            language=language,
            tags=tags
        )
        
        snippet = Snippet(**create_data.model_dump())
        
        # Generate embedding for semantic search
        text_to_embed = f"{snippet.title} {snippet.description or ''} {snippet.code}"
        snippet.embedding = self.embedding_generator.generate(text_to_embed)
        
        # Save to storage
        saved = await self.storage.create(snippet)
        
        return {
            "id": saved.id,
            "title": saved.title,
            "language": saved.language,
            "tags": saved.tags,
            "created_at": saved.created_at.isoformat(),
            "message": f"✅ Snippet '{saved.title}' saved successfully!"
        }
    
    async def get_snippet(self, snippet_id: str) -> dict:
        """
        Get a snippet by ID.
        
        Args:
            snippet_id: The snippet ID
            
        Returns:
            Snippet information
        """
        snippet = await self.storage.get(snippet_id)
        
        if not snippet:
            return {
                "error": f"❌ Snippet with ID '{snippet_id}' not found"
            }
        
        return {
            "id": snippet.id,
            "title": snippet.title,
            "code": snippet.code,
            "description": snippet.description,
            "language": snippet.language,
            "tags": snippet.tags,
            "created_at": snippet.created_at.isoformat(),
            "updated_at": snippet.updated_at.isoformat(),
            "usage_count": snippet.usage_count
        }
    
    async def search_snippets(
        self,
        query: str,
        language: Optional[str] = None,
        tags: Optional[List[str]] = None,
        limit: int = 10,
        threshold: float = 0.3
    ) -> dict:
        """
        Search snippets by semantic similarity.
        
        Args:
            query: Search query text
            language: Filter by programming language
            tags: Filter by tags
            limit: Maximum number of results
            threshold: Minimum similarity threshold (0-1)
            
        Returns:
            Search results
        """
        # Generate query embedding
        query_embedding = self.embedding_generator.generate(query)
        
        # Search storage
        results = await self.storage.search(
            query_embedding=query_embedding,
            language=language,
            tags=tags,
            limit=limit,
            threshold=threshold
        )
        
        if not results:
            return {
                "query": query,
                "results": [],
                "total": 0,
                "message": "🔍 No snippets found matching your query"
            }
        
        return {
            "query": query,
            "results": [
                {
                    "id": r.snippet.id,
                    "title": r.snippet.title,
                    "code": r.snippet.code[:200] + "..." if len(r.snippet.code) > 200 else r.snippet.code,
                    "description": r.snippet.description,
                    "language": r.snippet.language,
                    "tags": r.snippet.tags,
                    "similarity": round(r.similarity, 3),
                    "usage_count": r.snippet.usage_count
                }
                for r in results
            ],
            "total": len(results),
            "message": f"✅ Found {len(results)} snippet(s) matching your query"
        }
    
    async def list_snippets(
        self,
        language: Optional[str] = None,
        tags: Optional[List[str]] = None,
        limit: int = 20,
        offset: int = 0
    ) -> dict:
        """
        List all snippets with optional filtering.
        
        Args:
            language: Filter by programming language
            tags: Filter by tags
            limit: Maximum number of results
            offset: Pagination offset
            
        Returns:
            List of snippets
        """
        snippets = await self.storage.list_all(
            language=language,
            tags=tags,
            limit=limit,
            offset=offset
        )
        
        if not snippets:
            return {
                "snippets": [],
                "total": 0,
                "message": "📭 No snippets found"
            }
        
        return {
            "snippets": [
                {
                    "id": s.id,
                    "title": s.title,
                    "language": s.language,
                    "tags": s.tags,
                    "updated_at": s.updated_at.isoformat(),
                    "usage_count": s.usage_count
                }
                for s in snippets
            ],
            "total": len(snippets),
            "offset": offset,
            "limit": limit,
            "message": f"📋 Showing {len(snippets)} snippet(s)"
        }
    
    async def delete_snippet(self, snippet_id: str) -> dict:
        """
        Delete a snippet by ID.
        
        Args:
            snippet_id: The snippet ID to delete
            
        Returns:
            Deletion result
        """
        deleted = await self.storage.delete(snippet_id)
        
        if deleted:
            return {
                "success": True,
                "message": f"🗑️ Snippet '{snippet_id}' deleted successfully"
            }
        else:
            return {
                "success": False,
                "error": f"❌ Snippet with ID '{snippet_id}' not found"
            }
    
    async def update_snippet(
        self,
        snippet_id: str,
        title: Optional[str] = None,
        code: Optional[str] = None,
        description: Optional[str] = None,
        language: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> dict:
        """
        Update an existing snippet.
        
        Args:
            snippet_id: The snippet ID to update
            title: New title
            code: New code content
            description: New description
            language: New language
            tags: New tags
            
        Returns:
            Updated snippet information
        """
        # Get existing snippet
        existing = await self.storage.get(snippet_id)
        
        if not existing:
            return {
                "error": f"❌ Snippet with ID '{snippet_id}' not found"
            }
        
        # Update fields
        if title:
            existing.title = title
        if code:
            existing.code = code
            # Re-detect language if code changed
            if not language:
                language = detect_language(code)
        if description is not None:
            existing.description = description
        if language:
            existing.language = language
        if tags is not None:
            existing.tags = [t.strip().lower() for t in tags if t.strip()]
        
        # Regenerate embedding
        text_to_embed = f"{existing.title} {existing.description or ''} {existing.code}"
        existing.embedding = self.embedding_generator.generate(text_to_embed)
        
        # Save updates
        updated = await self.storage.update(existing)
        
        return {
            "id": updated.id,
            "title": updated.title,
            "language": updated.language,
            "tags": updated.tags,
            "updated_at": updated.updated_at.isoformat(),
            "message": f"✅ Snippet '{updated.title}' updated successfully!"
        }
