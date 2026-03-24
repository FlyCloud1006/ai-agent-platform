from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
from datetime import datetime
import uuid

from agent.core import AgentFactory, BaseAgent
from agent.executor import executor
from agent.memory import Memory
from models.agent import Agent, AgentCreate, AgentUpdate
from models.task import Task, ChatMessage

router = APIRouter()

# 内存存储（生产环境应使用数据库）
agents_db: Dict[str, Agent] = {}
memories_db: Dict[str, Memory] = {}

# ==================== Agent 管理 ====================

@router.post("/agents", response_model=Agent)
async def create_agent(data: AgentCreate):
    """创建 Agent"""
    agent_id = str(uuid.uuid4())
    agent = Agent(
        id=agent_id,
        name=data.name,
        role=data.role,
        description=data.description,
        instructions=data.instructions,
        config=data.config,
    )
    agents_db[agent_id] = agent
    memories_db[agent_id] = Memory(agent_id)
    
    return agent

@router.get("/agents")
async def list_agents():
    """列出所有 Agent"""
    return list(agents_db.values())

@router.get("/agents/{agent_id}")
async def get_agent(agent_id: str):
    """获取 Agent 详情"""
    if agent_id not in agents_db:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agents_db[agent_id]

@router.delete("/agents/{agent_id}")
async def delete_agent(agent_id: str):
    """删除 Agent"""
    if agent_id not in agents_db:
        raise HTTPException(status_code=404, detail="Agent not found")
    del agents_db[agent_id]
    if agent_id in memories_db:
        del memories_db[agent_id]
    return {"message": "Agent deleted"}

@router.patch("/agents/{agent_id}")
async def update_agent(agent_id: str, data: AgentUpdate):
    """更新 Agent"""
    if agent_id not in agents_db:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    agent = agents_db[agent_id]
    if data.name is not None:
        agent.name = data.name
    if data.instructions is not None:
        agent.instructions = data.instructions
    if data.config is not None:
        agent.config = data.config
    agent.updated_at = datetime.now()
    
    return agent

# ==================== Chat 对话 ====================

class ChatRequest(BaseModel):
    agent_id: str
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    task_id: str
    session_id: str
    response: str
    agent_id: str

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """发送消息给 Agent"""
    if request.agent_id not in agents_db:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    result = await executor.execute_chat(
        agent_id=request.agent_id,
        user_message=request.message,
        session_id=request.session_id,
    )
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return ChatResponse(**result)

# ==================== 任务管理 ====================

@router.get("/tasks/{task_id}")
async def get_task(task_id: str):
    """获取任务状态"""
    task = executor.get_task_status(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.get("/tasks")
async def list_tasks():
    """列出活跃任务"""
    return executor.list_active_tasks()

# ==================== 记忆管理 ====================

@router.get("/agents/{agent_id}/memory")
async def get_agent_memory(agent_id: str, limit: int = 20):
    """获取 Agent 记忆"""
    if agent_id not in memories_db:
        raise HTTPException(status_code=404, detail="Memory not found")
    memory = memories_db[agent_id]
    return {
        "short_term": memory.get_short_term(limit=limit),
        "long_term": memory.get_long_term(),
    }

@router.delete("/agents/{agent_id}/memory")
async def clear_agent_memory(agent_id: str):
    """清空 Agent 短期记忆"""
    if agent_id not in memories_db:
        raise HTTPException(status_code=404, detail="Memory not found")
    memories_db[agent_id].clear_short_term()
    return {"message": "Short-term memory cleared"}
