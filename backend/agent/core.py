from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid

class BaseAgent(ABC):
    """Agent 抽象基类"""
    
    def __init__(self, id: str, name: str, role: str, instructions: str, config: Dict[str, Any] = None):
        self.id = id or str(uuid.uuid4())
        self.name = name
        self.role = role
        self.instructions = instructions
        self.config = config or {}
        self.memory: List[Dict[str, Any]] = []
        self.status = "idle"
    
    @abstractmethod
    async def think(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """思考 - 处理输入并生成响应"""
        pass
    
    @abstractmethod
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """执行 - 调用工具完成任务"""
        pass
    
    def add_memory(self, role: str, content: str, metadata: Dict[str, Any] = None):
        """添加记忆"""
        self.memory.append({
            "role": role,
            "content": content,
            "metadata": metadata or {},
            "timestamp": datetime.now().isoformat(),
        })
    
    def get_memory(self, limit: int = 10) -> List[Dict[str, Any]]:
        """获取最近记忆"""
        return self.memory[-limit:]
    
    def clear_memory(self):
        """清空记忆"""
        self.memory = []

class AgentFactory:
    """Agent 工厂类"""
    
    _agents: Dict[str, BaseAgent] = {}
    _registry: Dict[str, type] = {}
    
    @classmethod
    def register(cls, agent_type: str, agent_class: type):
        """注册 Agent 类型"""
        cls._registry[agent_type] = agent_class
    
    @classmethod
    def create(cls, agent_type: str, **kwargs) -> BaseAgent:
        """创建 Agent 实例"""
        if agent_type not in cls._registry:
            raise ValueError(f"Unknown agent type: {agent_type}")
        return cls._registry[agent_type](**kwargs)
    
    @classmethod
    def get(cls, agent_id: str) -> Optional[BaseAgent]:
        """获取已创建的 Agent"""
        return cls._agents.get(agent_id)
    
    @classmethod
    def register_instance(cls, agent: BaseAgent):
        """注册 Agent 实例"""
        cls._agents[agent.id] = agent
    
    @classmethod
    def list_agents(cls) -> List[BaseAgent]:
        """列出所有 Agent"""
        return list(cls._agents.values())
