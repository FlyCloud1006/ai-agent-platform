from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import httpx
import asyncio

class BaseTool(ABC):
    """工具基类"""
    
    name: str = ""
    description: str = ""
    
    def __init__(self):
        self._enabled = True
    
    @abstractmethod
    async def execute(self, **kwargs) -> Dict[str, Any]:
        """执行工具"""
        pass
    
    def enable(self):
        self._enabled = True
    
    def disable(self):
        self._enabled = False
    
    @property
    def is_enabled(self) -> bool:
        return self._enabled

class WebSearchTool(BaseTool):
    """网络搜索工具"""
    
    name = "web_search"
    description = "搜索互联网获取最新信息"
    
    def __init__(self, api_key: str = None):
        super().__init__()
        self.api_key = api_key
    
    async def execute(self, query: str, count: int = 5, **kwargs) -> Dict[str, Any]:
        """执行搜索"""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                # 使用 DuckDuckGo 搜索（免费，无需 API Key）
                response = await client.get(
                    "https://api.duckduckgo.com/",
                    params={
                        "q": query,
                        "format": "json",
                        "no_html": "1",
                    }
                )
                data = response.json()
                
                results = []
                for item in data.get("RelatedTopics", [])[:count]:
                    if "Text" in item:
                        results.append({
                            "title": item.get("Text", ""),
                            "url": item.get("FirstURL", ""),
                        })
                
                return {
                    "success": True,
                    "query": query,
                    "results": results,
                }
        except Exception as e:
            return {"success": False, "error": str(e)}

class CalculatorTool(BaseTool):
    """计算器工具"""
    
    name = "calculator"
    description = "执行数学计算"
    
    async def execute(self, expression: str, **kwargs) -> Dict[str, Any]:
        """执行计算"""
        try:
            # 安全计算（只允许基本运算）
            allowed_chars = set("0123456789+-*/.() ")
            if all(c in allowed_chars for c in expression):
                result = eval(expression)
                return {"success": True, "expression": expression, "result": result}
            else:
                return {"success": False, "error": "Invalid expression"}
        except Exception as e:
            return {"success": False, "error": str(e)}
