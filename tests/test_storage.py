"""Tests for storage backend."""

import pytest
import asyncio
import tempfile
import shutil
from pathlib import Path

from snippetvault_mcp.storage.local import LocalStorage
from snippetvault_mcp.models.snippet import Snippet


@pytest.fixture
def temp_storage():
    """Create a temporary storage instance."""
    temp_dir = tempfile.mkdtemp()
    storage = LocalStorage(temp_dir)
    yield storage
    shutil.rmtree(temp_dir)


@pytest.mark.asyncio
async def test_create_and_get_snippet(temp_storage):
    """Test creating and retrieving a snippet."""
    snippet = Snippet(
        title="Test",
        code="print('hello')",
        language="python",
        tags=["test"]
    )
    
    # Create
    created = await temp_storage.create(snippet)
    assert created.id == snippet.id
    
    # Get
    retrieved = await temp_storage.get(snippet.id)
    assert retrieved is not None
    assert retrieved.title == "Test"
    assert retrieved.code == "print('hello')"


@pytest.mark.asyncio
async def test_delete_snippet(temp_storage):
    """Test deleting a snippet."""
    snippet = Snippet(title="To Delete", code="code")
    
    await temp_storage.create(snippet)
    
    # Delete
    deleted = await temp_storage.delete(snippet.id)
    assert deleted is True
    
    # Verify deletion
    retrieved = await temp_storage.get(snippet.id)
    assert retrieved is None


@pytest.mark.asyncio
async def test_list_snippets(temp_storage):
    """Test listing snippets."""
    # Create multiple snippets
    for i in range(3):
        snippet = Snippet(
            title=f"Snippet {i}",
            code=f"code {i}",
            language="python" if i % 2 == 0 else "javascript"
        )
        await temp_storage.create(snippet)
    
    # List all
    all_snippets = await temp_storage.list_all()
    assert len(all_snippets) == 3
    
    # Filter by language
    python_snippets = await temp_storage.list_all(language="python")
    assert len(python_snippets) == 2


@pytest.mark.asyncio
async def test_get_all_tags(temp_storage):
    """Test getting all tags."""
    snippet1 = Snippet(title="Test 1", code="code", tags=["python", "tutorial"])
    snippet2 = Snippet(title="Test 2", code="code", tags=["python", "advanced"])
    
    await temp_storage.create(snippet1)
    await temp_storage.create(snippet2)
    
    tags = await temp_storage.get_all_tags()
    assert "python" in tags
    assert "tutorial" in tags
    assert "advanced" in tags


@pytest.mark.asyncio
async def test_get_stats(temp_storage):
    """Test getting statistics."""
    snippet = Snippet(title="Test", code="code", language="python", tags=["test"])
    await temp_storage.create(snippet)
    
    stats = await temp_storage.get_stats()
    assert stats["total_snippets"] == 1
    assert stats["total_tags"] == 1
    assert "python" in stats["languages"]
