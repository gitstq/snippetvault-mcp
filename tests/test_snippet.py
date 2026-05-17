"""Tests for snippet models and operations."""

import pytest
from datetime import datetime

from snippetvault_mcp.models.snippet import Snippet, SnippetCreate, SnippetUpdate


def test_snippet_creation():
    """Test creating a snippet."""
    snippet = Snippet(
        title="Test Snippet",
        code="print('hello')",
        description="A test snippet",
        language="python",
        tags=["test", "python"]
    )
    
    assert snippet.title == "Test Snippet"
    assert snippet.code == "print('hello')"
    assert snippet.description == "A test snippet"
    assert snippet.language == "python"
    assert snippet.tags == ["test", "python"]
    assert snippet.id is not None
    assert isinstance(snippet.created_at, datetime)


def test_snippet_create_model():
    """Test SnippetCreate model."""
    data = SnippetCreate(
        title="Test",
        code="code here",
        language="javascript",
        tags=["js", "test"]
    )
    
    assert data.title == "Test"
    assert data.code == "code here"
    assert data.language == "javascript"


def test_snippet_update_model():
    """Test SnippetUpdate model."""
    data = SnippetUpdate(title="Updated Title")
    
    assert data.title == "Updated Title"
    assert data.code is None


def test_snippet_default_values():
    """Test snippet default values."""
    snippet = Snippet(title="Test", code="code")
    
    assert snippet.description is None
    assert snippet.language is None
    assert snippet.tags == []
    assert snippet.usage_count == 0
    assert snippet.embedding is None
