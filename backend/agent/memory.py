from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import json

class Memory:
    """Agent 记忆系统"""
    
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.short_term: List[Dict[str, Any]] = []  # 短期记忆（会话级）
        self.long_term: List[Dict[str, Any]] = []   # 长期记忆（持久化）
    
    def add_short_term(self, role: str, content: str, metadata: Dict[str, Any] = None):
        """添加短期记忆"""
        self.short_term.append({
            "role": role,
            "content": content,
            "metadata": metadata or {},
            "timestamp": datetime.now().isoformat(),
        })
        # 限制短期记忆长度
        if len(self.short_term) > 100:
            self.short_term = self.short_term[-100:]
    
    def add_long_term(self, key: str, value: Any, metadata: Dict[str, Any] = None):
        """添加长期记忆"""
        self.long_term.append({
            "key": key,
            "value": value,
            "metadata": metadata or {},
            "created_at": datetime.now().isoformat(),
        })
    
    def get_short_term(self, limit: int = 20) -> List[Dict[str, Any]]:
        """获取短期记忆"""
        return self.short_term[-limit:]
    
    def get_long_term(self, key: str = None) -> List[Dict[str, Any]]:
        """获取长期记忆"""
        if key:
            return [m for m in self.long_term if m.get("key") == key]
        return self.long_term
    
    def search_long_term(self, keyword: str) -> List[Dict[str, Any]]:
        """搜索长期记忆"""
        results = []
        for m in self.long_term:
            value = str(m.get("value", ""))
            if keyword.lower() in value.lower():
                results.append(m)
        return results
    
    def clear_short_term(self):
        """清空短期记忆"""
        self.short_term = []
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "agent_id": self.agent_id,
            "short_term": self.short_term,
            "long_term": self.long_term,
        }
