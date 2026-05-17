"""Utility functions for SnippetVault MCP."""

from .language import detect_language, get_language_from_extension
from .embedding import EmbeddingGenerator

__all__ = ["detect_language", "get_language_from_extension", "EmbeddingGenerator"]
