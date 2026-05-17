# 🚀 SnippetVault MCP

<p align="center">
  <b>🧠 智慧型程式碼片段管理工具，專為 AI 助手設計</b><br>
  <i>輕量級 MCP 伺服器，為您的程式碼片段帶來語義搜尋功能</i>
</p>

---

## 🎉 專案介紹

**SnippetVault MCP** 是一個輕量級的 [Model Context Protocol (MCP)](https://modelcontextprotocol.io) 伺服器，讓 Claude、Cursor 等 AI 助手能夠智慧地管理和檢索您的程式碼片段。

**為什麼選擇 SnippetVault？**
- 🔍 **語義搜尋** - 透過含義而非僅是關鍵字來尋找程式碼
- 🤖 **AI 原生設計** - 專為相容 MCP 的 AI 助手設計
- 🏷️ **智慧標籤** - 自動偵測程式語言和智慧標記
- ⚡ **輕量級** - 依賴最少，啟動快速
- 🔒 **本地優先** - 您的程式碼保存在本地

## ✨ 核心特性

| 特性 | 描述 |
|------|-------------|
| 💾 **儲存片段** | 儲存帶標題、描述和標籤的程式碼 |
| 🔍 **語義搜尋** | 用自然語言查詢尋找片段 |
| 🏷️ **智慧標記** | 自動偵測程式語言 |
| 📊 **使用分析** | 追蹤片段被檢索的頻率 |
| 🎯 **篩選排序** | 按語言、標籤或使用次數篩選 |

## 🚀 快速開始

### 環境要求
- Python 3.9+
- ~100MB 磁碟空間（用於嵌入模型）

### 安裝

```bash
pip install snippetvault-mcp
```

### 設定 Claude Desktop

新增到 `claude_desktop_config.json`：

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

**設定檔位置：**
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%/Claude/claude_desktop_config.json`
- Linux: `~/.config/Claude/claude_desktop_config.json`

### 設定 Cursor

新增到 Cursor 的 MCP 設定：

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

## 📖 使用指南

設定完成後，您可以這樣問 Claude/Cursor：

**儲存片段：**
```
"儲存這個 Python 快速排序函式：[貼上程式碼]"
```

**搜尋片段：**
```
"尋找我的排序演算法程式碼"
"搜尋資料庫連線範例"
```

**列示片段：**
```
"顯示我所有的 Python 片段"
"列出標記為 'api' 的片段"
```

**取得統計：**
```
"我有多少個片段？"
"顯示我的片段庫統計"
```

## 🔧 可用工具

| 工具 | 描述 |
|------|-------------|
| `save_snippet` | 儲存新程式碼片段 |
| `get_snippet` | 透過 ID 檢索片段 |
| `search_snippets` | 語義搜尋片段 |
| `list_snippets` | 列出所有片段（支援篩選）|
| `delete_snippet` | 刪除片段 |
| `update_snippet` | 更新現有片段 |
| `list_tags` | 列出所有唯一標籤 |
| `get_stats` | 取得庫統計資訊 |

## 💡 設計理念

SnippetVault 遵循以下設計原則：

1. **AI 優先** - 從一開始就專為 AI 助手整合設計
2. **開發者友善** - 自然語言互動，無需複雜查詢
3. **隱私優先** - 所有資料本地儲存，無雲端依賴
4. **可擴展** - 簡潔架構，易於定製

## 📦 開發指南

```bash
# 克隆倉庫
git clone https://github.com/gitstq/snippetvault-mcp.git
cd snippetvault-mcp

# 開發模式安裝
pip install -e ".[dev]"

# 執行測試
pytest

# 格式化程式碼
black src/
ruff check src/
```

## 🤝 貢獻指南

歡迎貢獻！請遵循：

1. Fork 本倉庫
2. 建立功能分支 (`git checkout -b feature/新功能`)
3. 提交更改 (`git commit -m 'feat: 新增新功能'`)
4. 推送到分支 (`git push origin feature/新功能`)
5. 提交 Pull Request

## 📄 開源協議

MIT 許可證 - 詳見 [LICENSE](LICENSE) 檔案。
