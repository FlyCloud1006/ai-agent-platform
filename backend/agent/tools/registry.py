from typing import Dict, Any, List, Optional
from agent.tools.base import BaseTool

class ToolRegistry:
    """工具注册表"""
    
    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}
    
    def register(self, tool: BaseTool) -> None:
        """注册工具"""
        self._tools[tool.name] = tool
    
    def get(self, name: str) -> Optional[BaseTool]:
        """获取工具"""
        return self._tools.get(name)
    
    def list_tools(self) -> List[str]:
        """列出所有工具"""
        return list(self._tools.keys())
    
    def list_enabled_tools(self) -> List[str]:
        """列出已启用的工具"""
        return [name for name, tool in self._tools.items() if tool.is_enabled]
    
    async def execute_tool(self, name: str, **kwargs) -> Dict[str, Any]:
        """执行工具"""
        tool = self.get(name)
        if not tool:
            return {"success": False, "error": f"Tool {name} not found"}
        if not tool.is_enabled:
            return {"success": False, "error": f"Tool {name} is disabled"}
        return await tool.execute(**kwargs)
    
    def enable(self, name: str) -> bool:
        """启用工具"""
        tool = self.get(name)
        if tool:
            tool.enable()
            return True
        return False
    
    def disable(self, name: str) -> bool:
        """禁用工具"""
        tool = self.get(name)
        if tool:
            tool.disable()
            return True
        return False
