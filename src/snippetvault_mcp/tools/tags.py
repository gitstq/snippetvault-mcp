"""Tag management tools."""

from typing import List

from ..storage.base import StorageBackend


class TagTools:
    """Tools for managing snippet tags."""
    
    def __init__(self, storage: StorageBackend):
        """
        Initialize tag tools.
        
        Args:
            storage: Storage backend instance
        """
        self.storage = storage
    
    async def list_tags(self) -> dict:
        """
        List all unique tags.
        
        Returns:
            List of tags with counts
        """
        tags = await self.storage.get_all_tags()
        
        if not tags:
            return {
                "tags": [],
                "total": 0,
                "message": "🏷️ No tags found"
            }
        
        return {
            "tags": tags,
            "total": len(tags),
            "message": f"🏷️ Found {len(tags)} unique tag(s)"
        }
    
    async def get_stats(self) -> dict:
        """
        Get storage statistics.
        
        Returns:
            Statistics information
        """
        stats = await self.storage.get_stats()
        
        return {
            "total_snippets": stats["total_snippets"],
            "total_tags": stats["total_tags"],
            "total_usage": stats["total_usage"],
            "languages": stats["languages"],
            "storage_path": stats["storage_path"],
            "message": f"📊 SnippetVault Stats: {stats['total_snippets']} snippets, {stats['total_tags']} tags, {stats['total_usage']} total uses"
        }
