from typing import Dict, Any, Optional
from datetime import datetime
import asyncio
import uuid

from agent.core import AgentFactory
from agent.tools import ToolRegistry

class AgentExecutor:
    """Agent 执行器 - 负责任务调度和执行"""
    
    def __init__(self):
        self.tool_registry = ToolRegistry()
        self.active_tasks: Dict[str, Dict[str, Any]] = {}
    
    async def execute_chat(self, agent_id: str, user_message: str, session_id: str = None) -> Dict[str, Any]:
        """执行对话任务"""
        agent = AgentFactory.get(agent_id)
        if not agent:
            return {"error": f"Agent {agent_id} not found"}
        
        session_id = session_id or str(uuid.uuid4())
        task_id = str(uuid.uuid4())
        
        self.active_tasks[task_id] = {
            "id": task_id,
            "agent_id": agent_id,
            "session_id": session_id,
            "status": "running",
            "started_at": datetime.now(),
        }
        
        try:
            # 构建输入
            input_data = {
                "message": user_message,
                "session_id": session_id,
                "history": agent.get_memory(limit=20),
            }
            
            # 执行思考
            agent.status = "running"
            result = await agent.execute(input_data)
            
            # 记录记忆
            agent.add_memory("user", user_message)
            agent.add_memory("assistant", result.get("response", ""))
            
            # 更新任务状态
            self.active_tasks[task_id].update({
                "status": "completed",
                "result": result,
                "completed_at": datetime.now(),
            })
            agent.status = "idle"
            
            return {
                "task_id": task_id,
                "session_id": session_id,
                "response": result.get("response", ""),
                "agent_id": agent_id,
            }
            
        except Exception as e:
            self.active_tasks[task_id].update({
                "status": "failed",
                "error": str(e),
                "completed_at": datetime.now(),
            })
            agent.status = "error"
            return {"error": str(e), "task_id": task_id}
    
    async def execute_task(self, agent_id: str, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """执行通用任务"""
        agent = AgentFactory.get(agent_id)
        if not agent:
            return {"error": f"Agent {agent_id} not found"}
        
        task_id = str(uuid.uuid4())
        
        try:
            result = await agent.execute(task_data)
            return {"task_id": task_id, "result": result}
        except Exception as e:
            return {"task_id": task_id, "error": str(e)}
    
    def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """获取任务状态"""
        return self.active_tasks.get(task_id)
    
    def list_active_tasks(self) -> list:
        """列出活跃任务"""
        return list(self.active_tasks.values())

# 全局执行器实例
executor = AgentExecutor()
