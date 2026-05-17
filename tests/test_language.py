"""Tests for language detection."""

import pytest

from snippetvault_mcp.utils.language import detect_language, get_language_from_extension


def test_detect_python():
    """Test Python detection."""
    code = """
def hello():
    print("Hello, World!")
    
class MyClass:
    def __init__(self):
        self.value = 42
"""
    assert detect_language(code) == "python"


def test_detect_javascript():
    """Test JavaScript detection."""
    code = """
const x = 10;
let y = 20;

function add(a, b) {
    return a + b;
}

console.log(add(x, y));
"""
    assert detect_language(code) == "javascript"


def test_detect_by_filename():
    """Test detection by filename extension."""
    code = "some code"
    
    assert detect_language(code, "test.py") == "python"
    assert detect_language(code, "test.js") == "javascript"
    assert detect_language(code, "test.ts") == "typescript"
    assert detect_language(code, "test.go") == "go"
    assert detect_language(code, "test.rs") == "rust"


def test_get_language_from_extension():
    """Test getting language from extension."""
    assert get_language_from_extension("file.py") == "python"
    assert get_language_from_extension("file.js") == "javascript"
    assert get_language_from_extension("file.java") == "java"
    assert get_language_from_extension("file.txt") is None
    assert get_language_from_extension("file") is None


def test_unknown_language():
    """Test unknown language returns None."""
    code = "some random text without code patterns"
    assert detect_language(code) is None
