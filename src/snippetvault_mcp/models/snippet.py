"""Code snippet data models."""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
import uuid


class Snippet(BaseModel):
    """Code snippet model."""
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str = Field(..., description="Snippet title")
    code: str = Field(..., description="Code content")
    description: Optional[str] = Field(None, description="Snippet description")
    language: Optional[str] = Field(None, description="Programming language")
    tags: List[str] = Field(default_factory=list, description="Tags for categorization")
    embedding: Optional[List[float]] = Field(None, description="Vector embedding")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    usage_count: int = Field(default=0, description="Number of times snippet was retrieved")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "title": "Python List Comprehension",
                "code": "squares = [x**2 for x in range(10)]",
                "description": "Create a list of squares using list comprehension",
                "language": "python",
                "tags": ["python", "list", "comprehension"],
                "created_at": "2025-01-01T00:00:00",
                "updated_at": "2025-01-01T00:00:00",
                "usage_count": 5
            }
        }


class SnippetCreate(BaseModel):
    """Model for creating a new snippet."""
    
    title: str = Field(..., min_length=1, max_length=200, description="Snippet title")
    code: str = Field(..., min_length=1, description="Code content")
    description: Optional[str] = Field(None, max_length=1000, description="Snippet description")
    language: Optional[str] = Field(None, description="Programming language (auto-detected if not provided)")
    tags: List[str] = Field(default_factory=list, description="Tags for categorization")


class SnippetUpdate(BaseModel):
    """Model for updating an existing snippet."""
    
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    code: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = Field(None, max_length=1000)
    language: Optional[str] = None
    tags: Optional[List[str]] = None


class SnippetSearchResult(BaseModel):
    """Search result model with similarity score."""
    
    snippet: Snippet
    similarity: float = Field(..., ge=0.0, le=1.0, description="Similarity score (0-1)")


class SearchQuery(BaseModel):
    """Search query model."""
    
    query: str = Field(..., min_length=1, description="Search query text")
    language: Optional[str] = Field(None, description="Filter by programming language")
    tags: Optional[List[str]] = Field(None, description="Filter by tags")
    limit: int = Field(default=10, ge=1, le=50, description="Maximum number of results")
    threshold: float = Field(default=0.3, ge=0.0, le=1.0, description="Minimum similarity threshold")
