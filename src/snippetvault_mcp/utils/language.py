"""Language detection utilities."""

import re
from typing import Optional

# Language detection patterns
LANGUAGE_PATTERNS = {
    "python": [
        r"^\s*(def|class|import|from)\s+",
        r"^\s*#.*$",
        r"print\s*\(",
        r"^\s*@\w+",
    ],
    "javascript": [
        r"^\s*(const|let|var)\s+\w+\s*=",
        r"function\s*\w*\s*\(",
        r"=>\s*\{",
        r"console\.(log|error|warn)",
    ],
    "typescript": [
        r":\s*(string|number|boolean|any|void)",
        r"interface\s+\w+",
        r"type\s+\w+\s*=",
        r"export\s+(default\s+)?(class|interface|type)",
    ],
    "java": [
        r"^\s*(public|private|protected)\s+(class|interface|void|static)",
        r"System\.(out|err)\.(print|println)",
        r"import\s+java\.",
    ],
    "go": [
        r"^\s*package\s+\w+",
        r"^\s*func\s+\w+",
        r"fmt\.(Print|Printf|Println)",
    ],
    "rust": [
        r"^\s*fn\s+\w+",
        r"^\s*use\s+\w+",
        r"^\s*mod\s+\w+",
        r"println!\s*\(",
    ],
    "cpp": [
        r"#include\s*[<\"]",
        r"std::",
        r"cout\s*<<",
        r"^\s*(class|struct|namespace)\s+\w+",
    ],
    "c": [
        r"#include\s*[<\"]",
        r"printf\s*\(",
        r"^\s*(int|void|char|float|double)\s+\w+\s*\(",
    ],
    "ruby": [
        r"^\s*(def|class|module)\s+",
        r"puts\s+",
        r":\w+\s*=>",
        r"require\s+[\"']",
    ],
    "php": [
        r"<\?php",
        r"\$\w+",
        r"echo\s+",
        r"function\s+\w+\s*\(",
    ],
    "shell": [
        r"^#!/bin/(bash|sh|zsh)",
        r"^\s*(if|then|else|fi|for|while|do|done)\s",
        r"\$\w+",
        r"echo\s+",
    ],
    "sql": [
        r"\b(SELECT|INSERT|UPDATE|DELETE|CREATE|DROP|ALTER)\b",
        r"\b(FROM|WHERE|JOIN|GROUP BY|ORDER BY|HAVING)\b",
    ],
    "html": [
        r"<\w+[^>]*>",
        r"</\w+>",
        r"<!DOCTYPE\s+html",
    ],
    "css": [
        r"[.#]\w+\s*\{",
        r"\w+-\w+\s*:",
        r"@media\s+",
    ],
    "json": [
        r'^\s*[\{\[]',
        r'"\w+"\s*:',
    ],
    "yaml": [
        r"^\w+:\s*",
        r"^\s+-\s+",
        r"^---\s*$",
    ],
    "markdown": [
        r"^#{1,6}\s+",
        r"^\s*[-*+]\s+",
        r"^\s*\d+\.\s+",
        r"\[.*\]\(.*\)",
    ],
}

# File extension to language mapping
EXTENSION_MAP = {
    ".py": "python",
    ".pyw": "python",
    ".js": "javascript",
    ".jsx": "javascript",
    ".ts": "typescript",
    ".tsx": "typescript",
    ".java": "java",
    ".go": "go",
    ".rs": "rust",
    ".cpp": "cpp",
    ".cc": "cpp",
    ".cxx": "cpp",
    ".c": "c",
    ".h": "c",
    ".hpp": "cpp",
    ".rb": "ruby",
    ".php": "php",
    ".sh": "shell",
    ".bash": "shell",
    ".zsh": "shell",
    ".sql": "sql",
    ".html": "html",
    ".htm": "html",
    ".css": "css",
    ".scss": "css",
    ".sass": "css",
    ".less": "css",
    ".json": "json",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".md": "markdown",
    ".markdown": "markdown",
    ".xml": "xml",
    ".swift": "swift",
    ".kt": "kotlin",
    ".scala": "scala",
    ".r": "r",
    ".m": "objective-c",
    ".lua": "lua",
    ".perl": "perl",
    ".pl": "perl",
}


def detect_language(code: str, filename: Optional[str] = None) -> Optional[str]:
    """
    Detect programming language from code content and/or filename.
    
    Args:
        code: The code content to analyze
        filename: Optional filename for extension-based detection
        
    Returns:
        Detected language or None if unknown
    """
    # First try filename extension
    if filename:
        ext = "." + filename.split(".")[-1].lower() if "." in filename else ""
        if ext in EXTENSION_MAP:
            return EXTENSION_MAP[ext]
    
    # Then try content-based detection
    scores = {}
    lines = code.split("\n")[:50]  # Check first 50 lines
    
    for lang, patterns in LANGUAGE_PATTERNS.items():
        score = 0
        for line in lines:
            for pattern in patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    score += 1
        if score > 0:
            scores[lang] = score
    
    if scores:
        return max(scores, key=scores.get)
    
    return None


def get_language_from_extension(filename: str) -> Optional[str]:
    """
    Get language from file extension.
    
    Args:
        filename: The filename to check
        
    Returns:
        Language name or None if unknown
    """
    if "." not in filename:
        return None
    
    ext = "." + filename.split(".")[-1].lower()
    return EXTENSION_MAP.get(ext)


def get_all_supported_languages() -> list:
    """Get list of all supported languages."""
    return sorted(set(LANGUAGE_PATTERNS.keys()) | set(EXTENSION_MAP.values()))
