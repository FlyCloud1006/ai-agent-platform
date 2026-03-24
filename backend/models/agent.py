from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum

class AgentStatus(str, Enum):
    IDLE = "idle"
    RUNNING = "running"
    ERROR = "error"

class Agent(BaseModel):
    id: str
    name: str
    role: str  # 如 "writer", "coder", "reviewer"
    description: str
    instructions: str  # Agent 的系统提示词
    status: AgentStatus = AgentStatus.IDLE
    config: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    class Config:
        use_enum_values = True

class AgentCreate(BaseModel):
    name: str
    role: str
    description: str = ""
    instructions: str
    config: Dict[str, Any] = Field(default_factory=dict)

class AgentUpdate(BaseModel):
    name: Optional[str] = None
    instructions: Optional[str] = None
    config: Optional[Dict[str, Any]] = None
