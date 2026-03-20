# 第3周：后端 Agent 核心 — Python + FastAPI + LangGraph

> 目标：构建 Agent 调度核心，支持 LLM 调用、工具系统、记忆系统

---

## 1. 项目结构

```
backend/
├── main.py                 # FastAPI 入口
├── requirements.txt         # 依赖
├── agent/
│   ├── __init__.py
│   ├── core.py             # Agent 核心类
│   ├── llm.py              # LLM 调用封装
│   ├── tools.py            # 工具注册系统
│   ├── memory.py           # 记忆系统
│   └── prompts.py          # 提示词模板
├── api/
│   ├── __init__.py
│   ├── routes.py           # API 路由
│   ├── schemas.py           # Pydantic 模型
│   └── deps.py             # 依赖注入
├── models/
│   └── database.py         # 数据库模型
└── services/
    ├── task_service.py     # 任务服务
    └── agent_service.py    # Agent 服务
```

---

## 2. requirements.txt

```
fastapi==0.104.1
uvicorn[standard]==0.24.0
langchain==0.1.20
langgraph==0.0.62
pydantic==2.5.0
python-dotenv==1.0.0
redis==5.0.1
sqlalchemy==2.0.23
asyncpg==0.29.0
httpx==0.25.2
python-multipart==0.0.6
```

---

## 3. LLM 调用封装

```python
# agent/llm.py
import os
from typing import Optional
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage

class LLMManager:
    """LLM 调用管理器，支持多模型切换"""
    
    def __init__(self):
        self.models: dict[str, ChatOpenAI] = {}
        self.default_model = os.getenv("DEFAULT_MODEL", "gpt-4")
    
    def get_model(self, model_name: str) -> ChatOpenAI:
        if model_name not in self.models:
            self.models[model_name] = ChatOpenAI(
                model_name=model_name,
                temperature=0.7,
                api_key=os.getenv("OPENAI_API_KEY"),
                streaming=True,
            )
        return self.models[model_name]
    
    async def chat(
        self,
        messages: list[dict],
        model: Optional[str] = None,
        temperature: float = 0.7,
    ) -> str:
        """对话生成"""
        model_name = model or self.default_model
        llm = self.get_model(model_name)
        
        # 转换消息格式
        langchain_messages = self._convert_messages(messages)
        
        response = await llm.agenerate([langchain_messages])
        return response.generations[0][0].text
    
    def _convert_messages(self, messages: list[dict]) -> list:
        result = []
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            
            if role == "system":
                result.append(SystemMessage(content=content))
            elif role == "user":
                result.append(HumanMessage(content=content))
            elif role == "assistant":
                result.append(AIMessage(content=content))
        
        return result

# 全局单例
llm_manager = LLMManager()
```

---

## 4. 工具系统

```python
# agent/tools.py
from abc import ABC, abstractmethod
from typing import Any, Callable, get_type_hints
import inspect

class BaseTool(ABC):
    """工具基类"""
    
    name: str = ""           # 工具名称
    description: str = ""    # 工具描述
    parameters: dict = {}     # JSON Schema 参数定义
    
    @abstractmethod
    def execute(self, **kwargs) -> str:
        """执行工具，返回结果"""
        pass

class WebSearchTool(BaseTool):
    """网络搜索工具"""
    
    name = "web_search"
    description = "搜索网络获取最新信息。输入关键词，返回搜索结果摘要。"
    parameters = {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "搜索关键词"},
            "count": {"type": "integer", "description": "返回结果数量", "default": 5},
        },
        "required": ["query"]
    }
    
    def execute(self, query: str, count: int = 5) -> str:
        # 实际调用搜索 API
        return f"搜索「{query}」的结果：1. xxx 2. xxx 3. xxx"

class FileReadTool(BaseTool):
    """文件读取工具"""
    
    name = "file_read"
    description = "读取本地文件内容"
    parameters = {
        "type": "object",
        "properties": {
            "path": {"type": "string", "description": "文件路径"},
        },
        "required": ["path"]
    }
    
    def execute(self, path: str) -> str:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

class ToolRegistry:
    """工具注册中心"""
    
    def __init__(self):
        self._tools: dict[str, BaseTool] = {}
    
    def register(self, tool: BaseTool):
        self._tools[tool.name] = tool
    
    def get_tool(self, name: str) -> BaseTool | None:
        return self._tools.get(name)
    
    def list_tools(self) -> list[dict]:
        return [
            {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.parameters,
            }
            for tool in self._tools.values()
        ]
    
    def execute(self, tool_name: str, arguments: dict) -> str:
        tool = self.get_tool(tool_name)
        if not tool:
            return f"错误：未找到工具 '{tool_name}'"
        
        try:
            return tool.execute(**arguments)
        except Exception as e:
            return f"工具执行错误：{str(e)}"

# 全局工具注册表
tool_registry = ToolRegistry()
tool_registry.register(WebSearchTool())
tool_registry.register(FileReadTool())
```

---

## 5. 记忆系统

```python
# agent/memory.py
from datetime import datetime
from typing import Any
import json

class ShortTermMemory:
    """短期记忆 — 当前会话上下文"""
    
    def __init__(self, max_tokens: int = 200000):
        self.messages: list[dict] = []
        self.max_tokens = max_tokens
    
    def add(self, role: str, content: str):
        self.messages.append({
            "role": role,
            "content": content,
            "created_at": datetime.now().isoformat(),
        })
    
    def get_context(self) -> list[dict]:
        """获取上下文（自动截断）"""
        return self.messages[-50:]  # 保留最近50条
    
    def clear(self):
        self.messages = []

class LongTermMemory:
    """长期记忆 — PostgreSQL 持久化存储"""
    
    def __init__(self, db_session):
        self.db = db_session
    
    def store(self, key: str, value: Any, category: str = "general"):
        """存储记忆"""
        from models.database import MemoryEntry
        entry = MemoryEntry(
            key=key,
            value=json.dumps(value, ensure_ascii=False),
            category=category,
            created_at=datetime.now(),
        )
        self.db.add(entry)
        self.db.commit()
    
    def retrieve(self, key: str) -> Any | None:
        """检索记忆"""
        from models.database import MemoryEntry
        entry = self.db.query(MemoryEntry).filter_by(key=key).first()
        if entry:
            return json.loads(entry.value)
        return None
    
    def search(self, query: str, category: str | None = None, limit: int = 5):
        """语义搜索记忆（简单关键词匹配）"""
        from models.database import MemoryEntry
        q = self.db.query(MemoryEntry)
        if category:
            q = q.filter_by(category=category)
        
        results = q.filter(MemoryEntry.key.contains(query)).limit(limit).all()
        return [{"key": r.key, "value": json.loads(r.value)} for r in results]

class EntityMemory:
    """实体记忆 — 记录人物、事物的事实"""
    
    def __init__(self):
        self.entities: dict[str, dict] = {}
    
    def add_entity(self, name: str, facts: dict):
        if name not in self.entities:
            self.entities[name] = {"facts": [], "observations": []}
        self.entities[name]["facts"].append(facts)
    
    def observe(self, name: str, observation: str):
        if name not in self.entities:
            self.entities[name] = {"facts": [], "observations": []}
        self.entities[name]["observations"].append({
            "text": observation,
            "at": datetime.now().isoformat(),
        })
    
    def get_entity(self, name: str) -> dict | None:
        return self.entities.get(name)
```

---

## 6. Agent 核心（LangGraph）

```python
# agent/core.py
from typing import TypedDict, Annotated, Sequence
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.prebuilt import ToolNode

from agent.llm import llm_manager
from agent.tools import tool_registry
from agent.memory import ShortTermMemory, LongTermMemory

class AgentState(TypedDict):
    """Agent 状态"""
    messages: Sequence[HumanMessage | AIMessage]
    memory: ShortTermMemory
    long_term_memory: LongTermMemory
    next_action: str
    plan: list[str]

class AIAgent:
    """AI Agent 核心"""
    
    def __init__(
        self,
        name: str,
        system_prompt: str,
        model: str = "gpt-4",
    ):
        self.name = name
        self.system_prompt = system_prompt
        self.model = model
        self.short_memory = ShortTermMemory()
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """构建 LangGraph 状态图"""
        
        def should_continue(state: AgentState) -> str:
            """判断是否继续执行工具"""
            last_message = state["messages"][-1]
            if hasattr(last_message, "tool_calls") and last_message.tool_calls:
                return "execute_tool"
            return "respond"
        
        def agent_node(state: AgentState):
            """Agent 决策节点"""
            response = llm_manager.chat(
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    *[{"role": m.role, "content": m.content} for m in state["messages"]]
                ],
                model=self.model,
            )
            return {"messages": [AIMessage(content=response)]}
        
        def tool_node(state: AgentState):
            """工具执行节点"""
            last_message = state["messages"][-1]
            results = []
            for call in last_message.tool_calls:
                result = tool_registry.execute(call["name"], call["args"])
                results.append({
                    "tool_call_id": call["id"],
                    "content": result,
                })
            return {"messages": results}
        
        # 构建图
        workflow = StateGraph(AgentState)
        workflow.add_node("agent", agent_node)
        workflow.add_node("execute_tool", tool_node)
        workflow.set_entry_point("agent")
        workflow.add_conditional_edges(
            "agent",
            should_continue,
            {
                "execute_tool": "execute_tool",
                "respond": END,
            }
        )
        workflow.add_edge("execute_tool", "agent")
        
        return workflow.compile()
    
    async def run(self, user_input: str) -> str:
        """运行 Agent"""
        # 添加用户消息到短期记忆
        self.short_memory.add("user", user_input)
        
        # 运行图
        result = await self.graph.ainvoke(
            input={
                "messages": [HumanMessage(content=user_input)],
                "memory": self.short_memory,
            },
            config={"recursion_limit": 50}
        )
        
        # 提取最后一条 AI 消息
        response = result["messages"][-1].content
        
        # 存入短期记忆
        self.short_memory.add("assistant", response)
        
        return response
```

---

## 7. FastAPI 主入口

```python
# main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn

from api.routes import router as api_router
from models.database import engine, Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时创建数据库表
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # 关闭时
    await engine.dispose()

app = FastAPI(
    title="AI Agent Platform API",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(api_router, prefix="/api")

@app.get("/")
def root():
    return {"message": "AI Agent Platform API", "version": "1.0.0"}

@app.get("/health")
def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
```

---

## 8. API 路由

```python
# api/routes.py
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncIterator

from api.schemas import (
    AgentCreate, AgentResponse, MessageCreate, MessageResponse,
    TaskCreate, TaskResponse
)
from api.deps import get_db
from agent.core import AIAgent
from services import agent_service, task_service

router = APIRouter()

# ================== Agent ==================

@router.get("/agents", response_model=list[AgentResponse])
async def list_agents(db: AsyncSession = Depends(get_db)):
    return await agent_service.list_agents(db)

@router.post("/agents", response_model=AgentResponse)
async def create_agent(data: AgentCreate, db: AsyncSession = Depends(get_db)):
    return await agent_service.create_agent(db, data)

@router.delete("/agents/{agent_id}")
async def delete_agent(agent_id: str, db: AsyncSession = Depends(get_db)):
    await agent_service.delete_agent(db, agent_id)
    return {"success": True}

# ================== Chat ==================

@router.post("/agents/{agent_id}/chat", response_model=MessageResponse)
async def chat(
    agent_id: str,
    data: MessageCreate,
    db: AsyncSession = Depends(get_db)
):
    agent = await agent_service.get_agent(db, agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    # 调用 Agent
    ai_agent = AIAgent(
        name=agent.name,
        system_prompt=agent.system_prompt,
        model=agent.model,
    )
    response = await ai_agent.run(data.message)
    
    return MessageResponse(
        role="assistant",
        content=response,
        agent_id=agent_id,
    )

# ================== WebSocket 实时对话 ==================

@router.websocket("/ws/chat/{agent_id}")
async def websocket_chat(websocket: WebSocket, agent_id: str):
    await websocket.accept()
    
    try:
        while True:
            data = await websocket.receive_json()
            message = data.get("message")
            
            # 获取 Agent
            # agent = await agent_service.get_agent(db, agent_id)
            
            # 运行 Agent
            # response = await ai_agent.run(message)
            
            await websocket.send_json({
                "type": "message",
                "content": f"收到: {message}",
            })
    except WebSocketDisconnect:
        pass
```

---

## 9. 数据库模型

```python
# models/database.py
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, Integer, Boolean, JSON
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://user:password@localhost:5432/ai_agent_db"
)

engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

class Agent(Base):
    __tablename__ = "agents"
    
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    model = Column(String, default="gpt-4")
    system_prompt = Column(Text)
    status = Column(String, default="idle")
    created_at = Column(DateTime, default=datetime.utcnow)

class MemoryEntry(Base):
    __tablename__ = "memory_entries"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String, index=True)
    value = Column(Text)
    category = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(String, primary_key=True)
    name = Column(String)
    description = Column(Text)
    cron = Column(String)
    status = Column(String, default="idle")
    last_run_at = Column(DateTime)
    consecutive_errors = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
```

---

## 10. 启动命令

```bash
# 安装依赖
pip install -r requirements.txt

# 设置环境变量
export OPENAI_API_KEY=sk-xxxx
export DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/ai_agent_db

# 启动开发服务器
uvicorn main:app --reload --port 8000
```

---

*本周重点：理解 LangGraph 的状态机模式，理解 Agent 如何调用工具*
