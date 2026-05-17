# 🚀 SnippetVault MCP

<p align="center">
  <b>🧠 Intelligent Code Snippet Management for AI Assistants</b><br>
  <i>A lightweight MCP server that brings semantic search to your code snippets</i>
</p>

<p align="center">
  <a href="#-english">English</a> •
  <a href="#-简体中文">简体中文</a> •
  <a href="#-繁體中文">繁體中文</a>
</p>

---

## 🇺🇸 English

### 🎉 Introduction

**SnippetVault MCP** is a lightweight [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server that enables AI assistants like Claude and Cursor to intelligently manage and retrieve your code snippets.

**Why SnippetVault?**
- 🔍 **Semantic Search** - Find code by meaning, not just keywords
- 🤖 **AI-Native** - Designed specifically for MCP-compatible AI assistants
- 🏷️ **Auto-Tagging** - Automatic language detection and smart tagging
- ⚡ **Lightweight** - Minimal dependencies, fast startup
- 🔒 **Local-First** - Your code stays on your machine

### ✨ Core Features

| Feature | Description |
|---------|-------------|
| 💾 **Save Snippets** | Store code with titles, descriptions, and tags |
| 🔍 **Semantic Search** | Find snippets by natural language queries |
| 🏷️ **Smart Tagging** | Auto-detect programming languages |
| 📊 **Usage Analytics** | Track how often snippets are retrieved |
| 🎯 **Filter & Sort** | By language, tags, or usage count |

### 🚀 Quick Start

#### Requirements
- Python 3.9+
- ~100MB disk space (for embedding model)

#### Installation

```bash
pip install snippetvault-mcp
```

#### Configure Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "snippetvault": {
      "command": "python",
      "args": ["-m", "snippetvault_mcp"],
      "env": {
        "SNIPPETVAULT_DATA_DIR": "~/.snippetvault"
      }
    }
  }
}
```

**Config file locations:**
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%/Claude/claude_desktop_config.json`
- Linux: `~/.config/Claude/claude_desktop_config.json`

#### Configure Cursor

Add to Cursor's MCP settings:

```json
{
  "mcpServers": {
    "snippetvault": {
      "command": "python",
      "args": ["-m", "snippetvault_mcp"]
    }
  }
}
```

### 📖 Usage Guide

Once configured, you can ask Claude/Cursor to:

**Save a snippet:**
```
"Save this Python function for quick sort: [paste code]"
```

**Search snippets:**
```
"Find my code for sorting algorithms"
"Search for database connection examples"
```

**List snippets:**
```
"Show all my Python snippets"
"List snippets tagged with 'api'"
```

**Get statistics:**
```
"How many snippets do I have?"
"Show my snippet vault stats"
```

### 🔧 Available Tools

| Tool | Description |
|------|-------------|
| `save_snippet` | Save a new code snippet |
| `get_snippet` | Retrieve a snippet by ID |
| `search_snippets` | Semantic search through snippets |
| `list_snippets` | List all snippets with filters |
| `delete_snippet` | Delete a snippet |
| `update_snippet` | Update an existing snippet |
| `list_tags` | List all unique tags |
| `get_stats` | Get vault statistics |

### 💡 Design Philosophy

SnippetVault was built with these principles:

1. **AI-First** - Designed from the ground up for AI assistant integration
2. **Developer-Friendly** - Natural language interaction, no complex queries
3. **Privacy-First** - All data stays local, no cloud dependencies
4. **Extensible** - Clean architecture for easy customization

### 📦 Development

```bash
# Clone repository
git clone https://github.com/gitstq/snippetvault-mcp.git
cd snippetvault-mcp

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black src/
ruff check src/
```

### 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 🇨🇳 简体中文

### 🎉 项目介绍

**SnippetVault MCP** 是一个轻量级的 [Model Context Protocol (MCP)](https://modelcontextprotocol.io) 服务器，让 Claude、Cursor 等 AI 助手能够智能地管理和检索您的代码片段。

**为什么选择 SnippetVault？**
- 🔍 **语义搜索** - 通过含义而不仅是关键词查找代码
- 🤖 **AI原生设计** - 专为兼容 MCP 的 AI 助手设计
- 🏷️ **智能标签** - 自动检测编程语言和智能标记
- ⚡ **轻量级** - 依赖最少，启动快速
- 🔒 **本地优先** - 您的代码保存在本地

### ✨ 核心特性

| 特性 | 描述 |
|------|-------------|
| 💾 **保存片段** | 存储带标题、描述和标签的代码 |
| 🔍 **语义搜索** | 用自然语言查询查找片段 |
| 🏷️ **智能标记** | 自动检测编程语言 |
| 📊 **使用分析** | 追踪片段被检索的频率 |
| 🎯 **筛选排序** | 按语言、标签或使用次数筛选 |

### 🚀 快速开始

#### 环境要求
- Python 3.9+
- ~100MB 磁盘空间（用于嵌入模型）

#### 安装

```bash
pip install snippetvault-mcp
```

#### 配置 Claude Desktop

添加到 `claude_desktop_config.json`：

```json
{
  "mcpServers": {
    "snippetvault": {
      "command": "python",
      "args": ["-m", "snippetvault_mcp"],
      "env": {
        "SNIPPETVAULT_DATA_DIR": "~/.snippetvault"
      }
    }
  }
}
```

**配置文件位置：**
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%/Claude/claude_desktop_config.json`
- Linux: `~/.config/Claude/claude_desktop_config.json`

#### 配置 Cursor

添加到 Cursor 的 MCP 设置：

```json
{
  "mcpServers": {
    "snippetvault": {
      "command": "python",
      "args": ["-m", "snippetvault_mcp"]
    }
  }
}
```

### 📖 使用指南

配置完成后，您可以这样问 Claude/Cursor：

**保存片段：**
```
"保存这个 Python 快速排序函数：[粘贴代码]"
```

**搜索片段：**
```
"查找我的排序算法代码"
"搜索数据库连接示例"
```

**列示片段：**
```
"显示我所有的 Python 片段"
"列出标记为 'api' 的片段"
```

**获取统计：**
```
"我有多少个片段？"
"显示我的片段库统计"
```

### 🔧 可用工具

| 工具 | 描述 |
|------|-------------|
| `save_snippet` | 保存新代码片段 |
| `get_snippet` | 通过 ID 检索片段 |
| `search_snippets` | 语义搜索片段 |
| `list_snippets` | 列出所有片段（支持筛选）|
| `delete_snippet` | 删除片段 |
| `update_snippet` | 更新现有片段 |
| `list_tags` | 列出所有唯一标签 |
| `get_stats` | 获取库统计信息 |

### 💡 设计理念

SnippetVault 遵循以下设计原则：

1. **AI优先** - 从一开始就专为 AI 助手集成设计
2. **开发者友好** - 自然语言交互，无需复杂查询
3. **隐私优先** - 所有数据本地保存，无云依赖
4. **可扩展** - 简洁架构，易于定制

### 📦 开发指南

```bash
# 克隆仓库
git clone https://github.com/gitstq/snippetvault-mcp.git
cd snippetvault-mcp

# 开发模式安装
pip install -e ".[dev]"

# 运行测试
pytest

# 格式化代码
black src/
ruff check src/
```

### 🤝 贡献指南

欢迎贡献！请遵循：

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/新功能`)
3. 提交更改 (`git commit -m 'feat: 添加新功能'`)
4. 推送到分支 (`git push origin feature/新功能`)
5. 提交 Pull Request

### 📄 开源协议

MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

---

## 🇹