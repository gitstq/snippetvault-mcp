"""
SnippetVault MCP Server - Main entry point

A lightweight MCP server for intelligent code snippet management.
"""

import os
import sys
from typing import Optional

from mcp.server import Server
from mcp.types import TextContent, Tool
from pydantic_settings import BaseSettings

from .storage.local import LocalStorage
from .tools.snippets import SnippetTools
from .tools.tags import TagTools


class Settings(BaseSettings):
    """Server settings."""
    
    snippetvault_data_dir: Optional[str] = None
    snippetvault_embedding_model: str = "all-MiniLM-L6-v2"
    
    class Config:
        env_prefix = "SNIPPETVAULT_"


# Initialize settings
settings = Settings()

# Initialize storage and tools
data_dir = settings.snippetvault_data_dir or os.path.expanduser("~/.snippetvault")
storage = LocalStorage(data_dir)
snippet_tools = SnippetTools(storage)
tag_tools = TagTools(storage)

# Create MCP server
app = Server("snippetvault-mcp")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="save_snippet",
            description="Save a new code snippet to the vault. Auto-detects programming language and generates embeddings for semantic search.",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "A descriptive title for the code snippet"
                    },
                    "code": {
                        "type": "string",
                        "description": "The code content to save"
                    },
                    "description": {
                        "type": "string",
                        "description": "Optional description explaining what the code does"
                    },
                    "language": {
                        "type": "string",
                        "description": "Programming language (auto-detected if not provided)"
                    },
                    "tags": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Tags for categorizing the snippet"
                    }
                },
                "required": ["title", "code"]
            }
        ),
        Tool(
            name="get_snippet",
            description="Retrieve a specific code snippet by its ID.",
            inputSchema={
                "type": "object",
                "properties": {
                    "snippet_id": {
                        "type": "string",
                        "description": "The unique identifier of the snippet"
                    }
                },
                "required": ["snippet_id"]
            }
        ),
        Tool(
            name="search_snippets",
            description="Search code snippets using semantic similarity. Finds snippets that are conceptually similar to your query, not just keyword matches.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Natural language search query describing what you're looking for"
                    },
                    "language": {
                        "type": "string",
                        "description": "Filter by programming language"
                    },
                    "tags": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Filter by tags"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of results (default: 10)",
                        "default": 10
                    },
                    "threshold": {
                        "type": "number",
                        "description": "Minimum similarity threshold 0-1 (default: 0.3)",
                        "default": 0.3
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="list_snippets",
            description="List all saved code snippets with optional filtering by language or tags.",
            inputSchema={
                "type": "object",
                "properties": {
                    "language": {
                        "type": "string",
                        "description": "Filter by programming language"
                    },
                    "tags": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Filter by tags"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of results (default: 20)",
                        "default": 20
                    },
                    "offset": {
                        "type": "integer",
                        "description": "Pagination offset (default: 0)",
                        "default": 0
                    }
                }
            }
        ),
        Tool(
            name="delete_snippet",
            description="Delete a code snippet by its ID.",
            inputSchema={
                "type": "object",
                "properties": {
                    "snippet_id": {
                        "type": "string",
                        "description": "The unique identifier of the snippet to delete"
                    }
                },
                "required": ["snippet_id"]
            }
        ),
        Tool(
            name="update_snippet",
            description="Update an existing code snippet. Only provided fields will be updated.",
            inputSchema={
                "type": "object",
                "properties": {
                    "snippet_id": {
                        "type": "string",
                        "description": "The unique identifier of the snippet to update"
                    },
                    "title": {
                        "type": "string",
                        "description": "New title for the snippet"
                    },
                    "code": {
                        "type": "string",
                        "description": "New code content"
                    },
                    "description": {
                        "type": "string",
                        "description": "New description"
                    },
                    "language": {
                        "type": "string",
                        "description": "Programming language"
                    },
                    "tags": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "New tags for the snippet"
                    }
                },
                "required": ["snippet_id"]
            }
        ),
        Tool(
            name="list_tags",
            description="List all unique tags used across all snippets.",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="get_stats",
            description="Get statistics about the snippet vault including total count, languages, and usage.",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls."""
    import json
    
    try:
        if name == "save_snippet":
            result = await snippet_tools.save_snippet(
                title=arguments["title"],
                code=arguments["code"],
                description=arguments.get("description"),
                language=arguments.get("language"),
                tags=arguments.get("tags")
            )
            return [TextContent(type="text", text=json.dumps(result, indent=2, ensure_ascii=False))]
        
        elif name == "get_snippet":
            result = await snippet_tools.get_snippet(arguments["snippet_id"])
            return [TextContent(type="text", text=json.dumps(result, indent=2, ensure_ascii=False))]
        
        elif name == "search_snippets":
            result = await snippet_tools.search_snippets(
                query=arguments["query"],
                language=arguments.get("language"),
                tags=arguments.get("tags"),
                limit=arguments.get("limit", 10),
                threshold=arguments.get("threshold", 0.3)
            )
            return [TextContent(type="text", text=json.dumps(result, indent=2, ensure_ascii=False))]
        
        elif name == "list_snippets":
            result = await snippet_tools.list_snippets(
                language=arguments.get("language"),
                tags=arguments.get("tags"),
                limit=arguments.get("limit", 20),
                offset=arguments.get("offset", 0)
            )
            return [TextContent(type="text", text=json.dumps(result, indent=2, ensure_ascii=False))]
        
        elif name == "delete_snippet":
            result = await snippet_tools.delete_snippet(arguments["snippet_id"])
            return [TextContent(type="text", text=json.dumps(result, indent=2, ensure_ascii=False))]
        
        elif name == "update_snippet":
            result = await snippet_tools.update_snippet(
                snippet_id=arguments["snippet_id"],
                title=arguments.get("title"),
                code=arguments.get("code"),
                description=arguments.get("description"),
                language=arguments.get("language"),
                tags=arguments.get("tags")
            )
            return [TextContent(type="text", text=json.dumps(result, indent=2, ensure_ascii=False))]
        
        elif name == "list_tags":
            result = await tag_tools.list_tags()
            return [TextContent(type="text", text=json.dumps(result, indent=2, ensure_ascii=False))]
        
        elif name == "get_stats":
            result = await tag_tools.get_stats()
            return [TextContent(type="text", text=json.dumps(result, indent=2, ensure_ascii=False))]
        
        else:
            return [TextContent(type="text", text=json.dumps({"error": f"Unknown tool: {name}"}))]
    
    except Exception as e:
        return [TextContent(type="text", text=json.dumps({"error": str(e)}))]


def main():
    """Main entry point."""
    import asyncio
    from mcp.server.stdio import stdio_server
    
    async def run():
        async with stdio_server() as (read_stream, write_stream):
            await app.run(
                read_stream,
                write_stream,
                app.create_initialization_options()
            )
    
    asyncio.run(run())


if __name__ == "__main__":
    main()
