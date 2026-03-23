# Skill 与 MCP 深度解析 — 从原理到实战

> 作者：FlyCloud1006  
> 日期：2026-03-23  
> 目标：深入理解 AI Agent 中的 Skill 和 MCP 核心概念，并通过真实案例掌握如何编写

---

![Skill & MCP Architecture](https://lightai.cloud.tencent.com/cosmanager/getFileStream?filePath=1774237657678/skill-mcp-architecture.png)

---

## 目录

1. [什么是 Skill？](#1-什么是-skill)
2. [Skill 的核心组成](#2-skill-的核心组成)
3. [Skill 的编写规范](#3-skill-的编写规范)
4. [真实案例：从零编写一个 Skill](#4-真实案例从零编写一个-skill)
5. [什么是 MCP？](#5-什么是-mcp)
6. [MCP 的核心组成](#6-mcp-的核心组成)
7. [MCP 的编写规范](#7-mcp-的编写规范)
8. [真实案例：编写一个 MCP Server](#8-真实案例编写一个-mcp-server)
9. [Skill 与 MCP 的区别与联系](#9-skill-与-mcp-的区别与联系)
10. [高级技巧](#10-高级技巧)
11. [OpenClaw 中的 Skill 生态](#11-openclaw-中的-skill-生态)

---

## 1. 什么是 Skill？

**Skill（技能）** 是 AI Agent 能力的扩展单元。它是一种结构化的任务封装，让 Agent 能够执行特定领域的操作。

### 通俗理解

| 概念 | 类比 | 说明 |
|------|------|------|
| Skill | 员工的技能培训手册 | 告诉 Agent "遇到 X 情况时怎么做" |
| Tool | 具体工具 | Skill 内部调用的具体执行手段 |
| Agent | 员工 | 具备多种 Skill 的执行者 |

### Skill vs Tool vs Plugin

```
┌─────────────────────────────────────────────────┐
│                   AI Agent                       │
├─────────────────────────────────────────────────┤
│                                                  │
│  ┌─────────────┐  ┌─────────────┐              │
│  │   Skill 1   │  │   Skill 2   │  ...        │
│  │ ┌─────────┐ │  │ ┌─────────┐ │              │
│  │ │ Tool A  │ │  │ │ Tool C  │ │              │
│  │ │ Tool B  │ │  │ │ Tool D  │ │              │
│  │ └─────────┘ │  │ └─────────┘ │              │
│  └─────────────┘  └─────────────┘              │
│                                                  │
└─────────────────────────────────────────────────┘
```

**关系解释：**
- **Skill** = 技能手册（包含判断逻辑 + 工具调用规则）
- **Tool** = 具体工具（可被多个 Skill 共用）
- **Plugin** = 功能插件（通常指 Channel 或扩展模块）

---

## 2. Skill 的核心组成

一个完整的 Skill 由以下部分构成：

```
my-skill/
├── SKILL.md          # 核心文件：技能描述、触发条件、执行逻辑
├── scripts/          # 辅助脚本（如有）
├── references/       # 参考资料（如有）
└── metadata.json     # 元数据（可选）
```

### 2.1 SKILL.md 的核心结构

```markdown
# Skill 名称

## description（必填）
> 简短描述：这个 Skill 什么时候被触发

## metadata（可选）
```json
{
  "openclaw": {
    "emoji": "🎯",           # Skill 图标
    "always": false,          # 是否始终激活
    "requires": {             # 前置依赖
      "bins": ["python3"]
    }
  }
}
```

## 触发条件（必填）
> 描述什么时候应该使用这个 Skill

## 执行逻辑（必填）
> 具体如何执行
```

### 2.2 各组成部分详解

#### description（描述字段）

**作用：** 告诉 Agent 什么时候应该使用这个 Skill

**编写技巧：**
- 覆盖多种表达方式（同义词、近义词）
- 包含具体的使用场景
- 使用 trigger phrases（触发短语）

**示例：**
```markdown
description: |
  当用户说"创建文档"、"新建文档"、"帮我写个文档"等
  **不指定平台**的请求时激活。
  触发词包括：写文档、新建文档、创建文档、编辑文档、智能表格
```

#### metadata（元数据）

**作用：** 提供 Skill 的配置信息和依赖声明

**常用字段：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `emoji` | string | Skill 图标 |
| `always` | boolean | 是否始终处于激活状态 |
| `requires.bins` | string[] | 依赖的可执行文件 |
| `requires.env` | string[] | 依赖的环境变量 |
| `install` | array | 自动安装脚本 |

**示例：**
```json
{
  "openclaw": {
    "emoji": "📄",
    "always": true,
    "requires": {
      "bins": ["mcporter"],
      "env": ["WECOM_CORP_ID"]
    },
    "install": [
      {
        "id": "mcporter",
        "kind": "node",
        "package": "mcporter",
        "bins": ["mcporter"]
      }
    ]
  }
}
```

#### 执行逻辑

**作用：** 定义 Skill 的具体执行步骤

**编写规范：**
1. 分步骤编写，每步清晰
2. 包含错误处理
3. 提供分支判断（不同情况不同处理）

---

## 3. Skill 的编写规范

### 3.1 命名规范

```
skill-name/
└── SKILL.md

命名规则：
- 全部小写
- 使用连字符分隔
- 体现功能域
```

**正确示例：**
- `wecom-doc` — 企业微信文档
- `github-pr` — GitHub PR 操作
- `weather-query` — 天气查询

**错误示例：**
- `WecomDoc` — 包含大写
- `wecom doc` — 包含空格
- `doc` — 太模糊

### 3.2 文件路径规范

```
~/.openclaw/
├── extensions/              # 扩展技能
│   └── wecom/
│       └── skills/
│           └── wecom-doc/
│               └── SKILL.md
└── workspace/
    └── skills/              # 工作区技能
        └── github/
            └── SKILL.md
```

### 3.3 触发条件编写技巧

**技巧1：覆盖多种表达**
```markdown
description: |
  触发条件（满足任一即可）：
  1. 用户说"创建/新建/写一个文档"
  2. 用户说"编辑文档内容"
  3. 用户说"用 Markdown 写文档"
  4. 用户提到企业微信文档 + 创建/编辑操作
```

**技巧2：使用场景标签**
```markdown
description: |
  场景标签：#文档 #创建 #编辑 #企业微信
  当用户意图涉及文档操作时激活
```

**技巧3：排除非目标场景**
```markdown
description: |
  激活条件：用户请求创建或编辑文档
  排除条件：
  - 用户只是询问文档操作方法（不含具体创建意图）
  - 用户指定了其他平台（如 Notion、Google Docs）
```

### 3.4 执行逻辑编写规范

**必做：**
1. 前置检查（依赖是否满足）
2. 参数验证（输入是否合法）
3. 错误处理（异常情况处理）

**示例模板：**
```markdown
## 执行流程

### 步骤1：检查依赖
检查必要工具是否已安装：
```bash
which <tool-name>
```
如果不存在，提示用户安装。

### 步骤2：验证配置
检查必要配置是否存在：
```bash
cat ~/.config/<app>/config.json
```

### 步骤3：执行操作
根据用户请求执行具体操作。

### 步骤4：结果处理
- 成功：返回结果给用户
- 失败：提供错误信息和解决方案
```

---

## 4. 真实案例：从零编写一个 Skill

### 案例：天气查询 Skill

**需求：** 用户说"查一下天气"、"今天多少度"、"明天会下雨吗"时，调用天气查询。

### 步骤1：创建目录结构

```bash
mkdir -p ~/.openclaw/workspace/skills/weather-query
```

### 步骤2：编写 SKILL.md

```markdown
# Weather Query Skill

> 查询天气的技能，支持当前天气和预报查询

## description

当用户提到以下表达时激活：
- "天气怎么样"
- "今天多少度"
- "明天会下雨吗"
- "查一下天气"
- "气温"
- "下雨"
- "晴天"

## metadata

```json
{
  "openclaw": {
    "emoji": "🌤️",
    "always": false,
    "requires": {
      "bins": ["curl"]
    }
  }
}
```

## 触发条件

用户请求查询天气（当前或预报）

## 执行逻辑

### 步骤1：解析用户意图

用户说"[地点]的天气怎么样"或"[时间]的天气"

提取：
- 地点（默认为当前城市，或从消息中提取）
- 时间（今天/明天/本周等）

### 步骤2：调用天气 API

使用 wttr.in 服务（无需 API key）：

```bash
curl -s "https://wttr.in/{地点}?format=j1"
```

### 步骤3：解析结果

返回的 JSON 包含：
- `current_condition`：当前天气
- `weather`：预报数据

### 步骤4：格式化输出

以友好的方式展示给用户：
```
📍 北京
🌡️ 温度：15°C
🌤️ 天气：多云
💧 湿度：45%
风速：12 km/h
```

## 注意事项

1. 如果用户未指定地点，尝试从 IP 获取当前位置
2. 如果 API 调用失败，返回错误信息并建议用户稍后重试
3. 支持中文地点名称（自动转拼音）
```

### 步骤3：注册 Skill

在 OpenClaw 的 skills 配置中添加：

```json
{
  "skills": {
    "weather-query": {
      "path": "~/.openclaw/workspace/skills/weather-query"
    }
  }
}
```

---

## 5. 什么是 MCP？

**MCP（Model Context Protocol）** 是一种标准化协议，用于让 AI Agent 与外部工具和服务进行交互。

### 通俗理解

| 概念 | 类比 |
|------|------|
| MCP Server | API 服务（提供工具） |
| MCP Client | API 消费者（Agent） |
| MCP Protocol | HTTP 协议（通信规则） |

### MCP 的核心价值

```
┌─────────────────┐         MCP Protocol          ┌─────────────────┐
│   AI Agent      │ ◄──────────────────────────► │   MCP Server    │
│   (MCP Client)  │                               │   (外部工具)    │
└─────────────────┘                               └─────────────────┘
         │                                                 │
         │ 1. list tools                                   │
         │ ─────────────────────────────────────────────►  │
         │                                                 │
         │ 2. tool list (name, description, schema)        │
         │ ◄───────────────────────────────────────────── │
         │                                                 │
         │ 3. call tool (tool_name, arguments)            │
         │ ─────────────────────────────────────────────►  │
         │                                                 │
         │ 4. tool result                                 │
         │ ◄───────────────────────────────────────────── │
```

---

## 6. MCP 的核心组成

### 6.1 MCP Server

**作用：** 暴露一组工具（Tools）供 AI 调用

**结构：**
```json
{
  "name": "wecom-doc",
  "description": "企业微信文档操作",
  "tools": [
    {
      "name": "createDoc",
      "description": "创建新文档",
      "inputSchema": {
        "type": "object",
        "properties": {
          "title": {"type": "string"},
          "content": {"type": "string"}
        },
        "required": ["title"]
      }
    }
  ]
}
```

### 6.2 MCP Client

**作用：** 调用 MCP Server 的工具

**OpenClaw 中的 MCP Client：**
```javascript
// 通过 wecom_mcp 工具调用
wecom_mcp list <category>   // 列出可用工具
wecom_mcp call <category> <method> '<jsonArgs>'  // 调用工具
```

### 6.3 MCP 工具定义

**标准结构：**
```json
{
  "name": "tool_name",
  "description": "工具描述（AI 会看到）",
  "inputSchema": {
    "type": "object",
    "properties": {
      "param1": {
        "type": "string",
        "description": "参数描述"
      }
    },
    "required": ["param1"]
  }
}
```

---

## 7. MCP 的编写规范

### 7.1 MCP Server 编写模板

```javascript
// my-mcp-server/index.js
const http = require('http');

const TOOLS = [
  {
    name: 'get_weather',
    description: '查询指定地点的天气',
    inputSchema: {
      type: 'object',
      properties: {
        location: {
          type: 'string',
          description: '地点名称（中文或英文）'
        },
        days: {
          type: 'number',
          description: '预报天数（1-3）',
          default: 1
        }
      },
      required: ['location']
    }
  }
];

// 工具执行逻辑
async function executeTool(toolName, args) {
  switch (toolName) {
    case 'get_weather':
      return await getWeather(args.location, args.days);
    default:
      throw new Error(`Unknown tool: ${toolName}`);
  }
}

async function getWeather(location, days = 1) {
  // 实现天气查询逻辑
  const response = await fetch(`https://wttr.in/${encodeURI(location)}?format=j1`);
  const data = await response.json();
  return {
    location,
    current: data.current_condition[0],
    forecast: data.weather.slice(0, days)
  };
}

module.exports = { TOOLS, executeTool };
```

### 7.2 MCP Server 配置

```json
// ~/.openclaw/mcp-servers/my-mcp-server.json
{
  "type": "http",
  "url": "http://localhost:3000/mcp",
  "name": "my-weather-server",
  "description": "天气查询服务"
}
```

### 7.3 MCP 工具命名规范

| 规则 | 正确 | 错误 |
|------|------|------|
| 小写 + 下划线 | `get_weather` | `getWeather`, `GetWeather` |
| 动词 + 名词 | `create_doc`, `list_files` | `doc_create`, `files_list` |
| 体现功能 | `search_web`, `read_file` | `do_action`, `handle_stuff` |

---

## 8. 真实案例：编写一个 MCP Server

### 案例：企业文档 MCP Server

**需求：** 提供文档的创建、读取、编辑能力

### 完整代码

```javascript
// doc-mcp-server/index.js
const express = require('express');
const cors = require('cors');

const app = express();
app.use(cors());
app.use(express.json());

// ============ 工具定义 ============
const TOOLS = [
  {
    name: 'create_document',
    description: '创建新文档',
    inputSchema: {
      type: 'object',
      properties: {
        title: { type: 'string', description: '文档标题' },
        content: { type: 'string', description: '文档内容（Markdown格式）' },
        platform: { 
          type: 'string', 
          enum: ['wecom', 'notion'],
          description: '平台类型，默认 wecom'
        }
      },
      required: ['title']
    }
  },
  {
    name: 'read_document',
    description: '读取文档内容',
    inputSchema: {
      type: 'object',
      properties: {
        doc_id: { type: 'string', description: '文档ID' },
        platform: { type: 'string', enum: ['wecom', 'notion'] }
      },
      required: ['doc_id']
    }
  },
  {
    name: 'update_document',
    description: '更新文档内容',
    inputSchema: {
      type: 'object',
      properties: {
        doc_id: { type: 'string', description: '文档ID' },
        content: { type: 'string', description: '新内容（Markdown格式）' },
        platform: { type: 'string', enum: ['wecom', 'notion'] }
      },
      required: ['doc_id', 'content']
    }
  },
  {
    name: 'list_documents',
    description: '列出所有文档',
    inputSchema: {
      type: 'object',
      properties: {
        platform: { type: 'string', enum: ['wecom', 'notion'] },
        limit: { type: 'number', description: '返回数量，默认20' }
      }
    }
  }
];

// ============ 工具执行器 ============
const toolExecutors = {
  async create_document({ title, content = '', platform = 'wecom' }) {
    // 根据平台调用不同的 API
    if (platform === 'wecom') {
      return await createWecomDoc(title, content);
    } else if (platform === 'notion') {
      return await createNotionDoc(title, content);
    }
    throw new Error(`Unsupported platform: ${platform}`);
  },

  async read_document({ doc_id, platform = 'wecom' }) {
    if (platform === 'wecom') {
      return await getWecomDoc(doc_id);
    } else if (platform === 'notion') {
      return await getNotionDoc(doc_id);
    }
    throw new Error(`Unsupported platform: ${platform}`);
  },

  async update_document({ doc_id, content, platform = 'wecom' }) {
    if (platform === 'wecom') {
      return await updateWecomDoc(doc_id, content);
    } else if (platform === 'notion') {
      return await updateNotionDoc(doc_id, content);
    }
    throw new Error(`Unsupported platform: ${platform}`);
  },

  async list_documents({ platform = 'wecom', limit = 20 }) {
    if (platform === 'wecom') {
      return await listWecomDocs(limit);
    } else if (platform === 'notion') {
      return await listNotionDocs(limit);
    }
    throw new Error(`Unsupported platform: ${platform}`);
  }
};

// ============ API 路由 ============

// 列出所有工具
app.get('/mcp', (req, res) => {
  res.json({ tools: TOOLS });
});

// 调用工具
app.post('/mcp', async (req, res) => {
  try {
    const { tool, arguments: args } = req.body;
    const executor = toolExecutors[tool];
    
    if (!executor) {
      return res.status(404).json({ error: `Tool ${tool} not found` });
    }
    
    const result = await executor(args || {});
    res.json({ result });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// ============ 启动 ============
const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Doc MCP Server running on port ${PORT}`);
});
```

---

## 9. Skill 与 MCP 的区别与联系

### 9.1 核心区别

| 维度 | Skill | MCP |
|------|-------|-----|
| **定位** | 任务封装 + 执行策略 | 工具调用协议 |
| **范围** | 可包含多个 Tool | 通常是单一工具集 |
| **智能** | 包含判断逻辑 | 仅暴露接口 |
| **编写语言** | Markdown + 脚本 | JavaScript/Python/Go |
| **执行方式** | Agent 解析后调用 Tool | 直接通过 Protocol 调用 |

### 9.2 关系图

```
┌────────────────────────────────────────────────────────┐
│                    AI Agent                           │
├────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────────────────────────────────────────┐  │
│  │                    Skill                          │  │
│  │  ┌─────────────────────────────────────────┐    │  │
│  │  │  描述：当用户说"创建文档"时              │    │  │
│  │  │  策略：                                    │    │  │
│  │  │    1. 检查平台参数                        │    │  │
│  │  │    2. 调用对应 MCP 工具                  │    │  │
│  │  │    3. 处理结果并返回                      │    │  │
│  │  └─────────────────────────────────────────┘    │  │
│  └──────────────────────┬──────────────────────────┘  │
│                         │                              │
│                         ▼                              │
│  ┌─────────────────────────────────────────────────┐  │
│  │                   MCP Server                     │  │
│  │  tools: create_document, read_document, ...     │  │
│  └─────────────────────────────────────────────────┘  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 9.3 使用场景选择

**使用 Skill 的场景：**
- 需要复杂的判断逻辑
- 需要多步骤执行流程
- 需要条件分支处理
- 需要状态管理和记忆

**使用 MCP 的场景：**
- 简单的工具调用
- 需要标准化接口
- 跨平台工具封装
- 第三方 API 集成

---

## 10. 高级技巧

### 10.1 Skill 触发优化

**技巧1：使用正则表达式增强匹配**

```markdown
description: |
  触发条件（正则匹配）：
  - /创建.*文档/i
  - /新建.*(doc|文档)/i
  - /(write|写).*document/i
```

**技巧2：设置优先级**

```json
{
  "openclaw": {
    "priority": 10,  // 数值越大优先级越高
    "emoji": "📄"
  }
}
```

### 10.2 MCP 工具设计模式

**模式1：链式调用**

```javascript
// 工具返回可继续调用的引用
async function search_documents({ query }) {
  const results = await db.search(query);
  return {
    count: results.length,
    results,
    // 可用于下一步操作的引用
    next_action: 'read_document',
    ref: results[0].id
  };
}
```

**模式2：批量操作**

```javascript
const TOOLS = [
  {
    name: 'batch_create',
    description: '批量创建文档',
    inputSchema: {
      type: 'object',
      properties: {
        documents: {
          type: 'array',
          items: {
            type: 'object',
            properties: {
              title: { type: 'string' },
              content: { type: 'string' }
            }
          }
        }
      }
    }
  }
];
```

### 10.3 Skill 与 MCP 联动

```markdown
## 联动示例

当用户说"帮我创建并分享文档"时：

1. Skill 解析意图 → "创建文档 + 分享"
2. Skill 调用 MCP tool: `create_document`
3. Skill 调用 MCP tool: `share_document`
4. Skill 整合结果返回给用户
```

---

## 11. OpenClaw 中的 Skill 生态

### 11.1 OpenClaw Skill 目录结构

```
~/.openclaw/
├── extensions/              # 官方/第三方扩展
│   ├── wecom/              # 企业微信插件
│   │   └── skills/
│   │       ├── wecom-doc/
│   │       ├── wecom-todo/
│   │       └── wecom-meeting/
│   ├── qqbot/              # QQ 插件
│   │   └── skills/
│   └── lightclawbot/       # LightClaw 插件
│       └── skills/
└── workspace/
    └── skills/             # 用户自定义技能
        ├── github/
        ├── weather/
        ├── novel-generator/
        └── ...
```

### 11.2 OpenClaw 内置 Skill 一览

| Skill | 功能 | 触发词 |
|-------|------|--------|
| `wecom-doc` | 企业微信文档 | 创建文档、编辑文档 |
| `wecom-todo` | 企业微信待办 | 创建待办、标记完成 |
| `wecom-meeting` | 企业微信会议 | 创建会议、预约会议 |
| `wecom-schedule` | 企业微信日程 | 添加日程、查看日程 |
| `github` | GitHub 操作 | 查看 Issue、PR |
| `weather` | 天气查询 | 天气怎么样 |
| `cron` | 定时任务 | 设置提醒、定时任务 |
| `novel-generator` | 小说生成 | 写小说、创作故事 |

### 11.3 从 OpenClaw Skill 源码学习

**推荐学习顺序：**

1. **简单 Skill**：`weather` — 最基础的 Skill 结构
2. **中等复杂度**：`github` — 包含参数处理和分支逻辑
3. **复杂 Skill**：`wecom-doc` — 包含 MCP 调用和多步骤流程

**源码阅读重点：**

```markdown
# 阅读 SKILL.md 的重点

1. description — 如何编写触发条件
2. metadata — 如何声明依赖
3. 执行逻辑 — 如何设计步骤
4. 错误处理 — 如何处理异常情况
```

---

## 附录：常用资源

### A. SKILL.md 模板

```markdown
# Skill Name

> Short description of what this skill does

## description

When the user says:
- trigger phrase 1
- trigger phrase 2
- trigger phrase 3

## metadata

```json
{
  "openclaw": {
    "emoji": "🎯",
    "always": false
  }
}
```

## 触发条件

描述在什么情况下激活此 Skill

## 执行逻辑

### 步骤1：前置检查
检查必要条件

### 步骤2：执行操作
执行主要操作

### 步骤3：结果处理
处理返回结果

## 注意事项

1. 注意1
2. 注意2
```

### B. MCP Server 快速模板

```javascript
const express = require('express');
const app = express();
app.use(express.json());

const TOOLS = [
  {
    name: 'tool_name',
    description: 'Tool description',
    inputSchema: {
      type: 'object',
      properties: {
        param1: { type: 'string', description: 'Parameter 1' }
      },
      required: ['param1']
    }
  }
];

const executors = {
  tool_name: async ({ param1 }) => {
    // 执行逻辑
    return { success: true, data: {} };
  }
};

app.get('/mcp', (req, res) => res.json({ tools: TOOLS }));

app.post('/mcp', async (req, res) => {
  try {
    const { tool, arguments: args } = req.body;
    const result = await executors[tool](args);
    res.json({ result });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.listen(3000);
```

---

## 下一步学习路径

1. **阅读 OpenClaw 内置 Skill 源码** — 理解最佳实践
2. **编写自己的 Skill** — 从简单开始，逐步复杂化
3. **了解 MCP 协议细节** — 阅读 MCP 官方规范
4. **实现自己的 MCP Server** — 封装外部 API
5. **Skill 与 MCP 联动** — 构建完整的功能模块

---

*文档版本：v1.0 | 编写日期：2026-03-23*
