from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, Set
import json
import asyncio

class ConnectionManager:
    """WebSocket 连接管理器"""
    
    def __init__(self):
        # session_id -> WebSocket
        self.active_connections: Dict[str, WebSocket] = {}
        # agent_id -> Set[session_ids]
        self.agent_subscriptions: Dict[str, Set[str]] = {}
    
    async def connect(self, websocket: WebSocket, session_id: str):
        """建立连接"""
        await websocket.accept()
        self.active_connections[session_id] = websocket
    
    def disconnect(self, session_id: str):
        """断开连接"""
        if session_id in self.active_connections:
            del self.active_connections[session_id]
        # 从所有订阅中移除
        for agent_id in self.agent_subscriptions:
            self.agent_subscriptions[agent_id].discard(session_id)
    
    async def send_message(self, session_id: str, message: dict):
        """发送消息"""
        if session_id in self.active_connections:
            await self.active_connections[session_id].send_json(message)
    
    async def broadcast_to_agent(self, agent_id: str, message: dict):
        """广播消息给订阅某 Agent 的所有连接"""
        if agent_id in self.agent_subscriptions:
            for session_id in self.agent_subscriptions[agent_id]:
                await self.send_message(session_id, message)
    
    def subscribe(self, session_id: str, agent_id: str):
        """订阅 Agent 消息"""
        if agent_id not in self.agent_subscriptions:
            self.agent_subscriptions[agent_id] = set()
        self.agent_subscriptions[agent_id].add(session_id)

manager = ConnectionManager()

async def websocket_endpoint(websocket: WebSocket, session_id: str = None):
    """WebSocket 端点"""
    session_id = session_id or str(id(websocket))
    await manager.connect(websocket, session_id)
    
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            msg_type = message.get("type")
            
            if msg_type == "subscribe":
                agent_id = message.get("agent_id")
                manager.subscribe(session_id, agent_id)
                await manager.send_message(session_id, {
                    "type": "subscribed",
                    "agent_id": agent_id,
                })
            
            elif msg_type == "chat":
                # 处理聊天消息
                from agent.executor import executor
                agent_id = message.get("agent_id")
                user_message = message.get("message")
                
                result = await executor.execute_chat(
                    agent_id=agent_id,
                    user_message=user_message,
                    session_id=session_id,
                )
                
                await manager.send_message(session_id, {
                    "type": "response",
                    "data": result,
                })
                
                # 同时广播给所有订阅者
                await manager.broadcast_to_agent(agent_id, {
                    "type": "agent_message",
                    "data": result,
                })
            
            elif msg_type == "ping":
                await manager.send_message(session_id, {"type": "pong"})
    
    except WebSocketDisconnect:
        manager.disconnect(session_id)
