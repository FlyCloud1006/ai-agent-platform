# 第4周：多 Agent 协作 — CrewAI 模式 + 任务分发

> 目标：理解多 Agent 协作模式，实现 Agent 之间的通信与协作

---

## 1. 为什么需要多 Agent 协作？

```
单一 Agent 的问题：
- 一个人能力有限（写作 Agent ≠ 编程 Agent）
- 复杂任务由单一 Agent 完成容易出错
- 难以分工合作

多 Agent 协作的优势：
- 分工明确：专业的事交给专业的 Agent
- 互相协作：规划 Agent → 执行 Agent → 审查 Agent
- 能力叠加：1+1 > 2
```

---

## 2. 多 Agent 架构模式

### 模式一：分层协作（Hierarchical）

```
用户请求
    │
    ▼
┌──────────────┐
│  主管 Agent   │  ← 理解意图、分解任务
│ (Manager)     │
└──────┬───────┘
       │ 分发任务
       ▼
┌──────────────┐
│  执行 Agent  │ ← 编程 Agent / 写作 Agent / 搜索 Agent
│ (Worker)     │
└──────┬───────┘
       │ 返回结果
       ▼
┌──────────────┐
│  主管 Agent   │  ← 整合结果、返回给用户
└──────────────┘
```

### 模式二：并行协作（Parallel）

```
用户请求：研究 + 写作 + 发布
    │
    ├──► 研究 Agent ──► 结果 A
    │
    ├──► 写作 Agent ──► 结果 B
    │
    └──► 发布 Agent ──► 结果 C
                │
                ▼
           整合结果
```

### 模式三：审查协作（Supervisor）

```
用户请求
    │
    ▼
┌──────────────┐
│  执行 Agent   │ ← 执行任务
└──────┬───────┘
       │ 产出
       ▼
┌──────────────┐
│  审查 Agent   │ ← 检查质量
└──────┬───────┘
       │ 通过/打回
       ▼
    通过 ✓ ──► 返回用户
    打回 ✗ ──► 返回执行 Agent 重新做
```

---

## 3. CrewAI 多 Agent 协作

### 什么是 CrewAI？

一个 Python 多 Agent 协作框架，核心概念：

| 概念 | 含义 |
|------|------|
| **Agent** | 一个人物角色（分析师、作家、编辑...） |
| **Task** | 一个具体任务 |
| **Crew** | Agent 团队 |
| **Process** | 协作流程（sequential / hierarchical） |

### 安装

```bash
pip install crewai crewai-tools
```

### 实战示例：小说创作团队

```python
# crew_demo.py
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerpApiWrapper

# 定义工具
search_tool = SerpApiWrapper()

# ============ Agent 定义 ============

# 1. 研究员 Agent
researcher = Agent(
    role="网络小说研究员",
    goal="研究当前最热门的小说题材、写作技巧和读者喜好",
    backstory="""你是一位资深的网络小说研究员，
    对晋江、起点、番茄等平台了如指掌。
    擅长分析读者心理和市场趋势。""",
    tools=[search_tool],
    verbose=True,
)

# 2. 作家 Agent
writer = Agent(
    role="网络小说作家",
    goal="根据研究报告，创作引人入胜的小说章节",
    backstory="""你是白金级网络小说作家，
    擅长都市、玄幻、穿越等题材。
    文笔流畅，情节跌宕起伏。""",
    verbose=True,
)

# 3. 编辑 Agent
editor = Agent(
    role="资深编辑",
    goal="审查稿件，确保质量和连贯性",
    backstory="""你是十年经验的资深编辑，
    眼睛毒辣，能发现任何逻辑漏洞和文笔问题。""",
    verbose=True,
)

# ============ Task 定义 ============

# 研究任务
research_task = Task(
    description="""
    搜索并分析当前热门的网络小说：
    1. 找出10部各平台热门小说
    2. 分析它们的题材、开头、人设、爽点
    3. 总结写作技巧和读者喜好趋势
    """,
    expected_output="一份详细的热门小说分析报告",
    agent=researcher,
)

# 写作任务
writing_task = Task(
    description="""
    根据研究报告，创作《星海纪元》小说的下一章节：
    1. 参考热门小说的开头写法
    2. 设定鲜明的人物和冲突
    3. 每章2000-3000字
    4. 章末留下悬念
    """,
    expected_output="完整的小说章节正文",
    agent=writer,
    context=[research_task],  # 依赖研究任务
)

# 编辑任务
editing_task = Task(
    description="""
    审查作家完成的章节：
    1. 检查逻辑连贯性
    2. 优化文笔和节奏
    3. 提出修改意见
    """,
    expected_output="修改建议或通过意见",
    agent=editor,
    context=[writing_task],  # 依赖写作任务
)

# ============ Crew 编排 ============

novel_crew = Crew(
    agents=[researcher, writer, editor],
    tasks=[research_task, writing_task, editing_task],
    process=Process.sequential,  # 顺序执行（研究→写作→编辑）
    verbose=True,
)

# 启动协作
result = novel_crew.kickoff()
print(result)
```

---

## 4. 自己实现多 Agent 调度

### 4.1 Agent 通信协议

```python
# agent/communication.py
from enum import Enum
from typing import Any
from pydantic import BaseModel

class MessageType(str, Enum):
    TASK = "task"           # 分发任务
    RESULT = "result"       # 返回结果
    STATUS = "status"      # 状态更新
    ERROR = "error"        # 错误报告
    APPROVAL = "approval"  # 审批请求

class AgentMessage(BaseModel):
    """Agent 之间的通信消息"""
    from_agent: str
    to_agent: str | None   # None = 广播
    message_type: MessageType
    content: Any
    task_id: str | None = None
    timestamp: str

class AgentRegistry:
    """Agent 注册表"""
    
    def __init__(self):
        self._agents: dict[str, AIAgent] = {}
        self._message_queue: list[AgentMessage] = []
    
    def register(self, agent_id: str, agent: AIAgent):
        self._agents[agent_id] = agent
    
    def send_message(self, msg: AgentMessage):
        """发送消息"""
        self._message_queue.append(msg)
    
    def get_messages(self, agent_id: str) -> list[AgentMessage]:
        """获取发给某 Agent 的消息"""
        return [
            m for m in self._message_queue
            if m.to_agent == agent_id or m.to_agent is None
        ]
    
    def clear_processed(self, agent_id: str):
        """清除已处理的消息"""
        self._message_queue = [
            m for m in self._message_queue
            if m.to_agent != agent_id
        ]

# 全局注册表
agent_registry = AgentRegistry()
```

### 4.2 任务分发器

```python
# agent/task_dispatcher.py
import uuid
from datetime import datetime
from typing import Callable

from agent.communication import AgentMessage, MessageType, agent_registry

class Task:
    """任务"""
    def __init__(self, task_type: str, description: str, payload: dict):
        self.id = str(uuid.uuid4())[:8]
        self.task_type = task_type
        self.description = description
        self.payload = payload
        self.status = "pending"  # pending / running / completed / failed
        self.result = None
        self.created_at = datetime.now()
        self.completed_at = None

class TaskDispatcher:
    """任务分发器 — 负责任务分配给合适的 Agent"""
    
    def __init__(self):
        self.tasks: dict[str, Task] = {}
    
    def dispatch(self, task: Task) -> str:
        """分发任务，返回任务ID"""
        self.tasks[task.id] = task
        
        # 根据任务类型选择 Agent
        agent_map = {
            "research": "research_agent",
            "writing": "writer_agent",
            "editing": "editor_agent",
            "coding": "coder_agent",
            "music": "music_agent",
        }
        
        target_agent = agent_map.get(task.task_type, "default_agent")
        
        # 发送消息给对应 Agent
        msg = AgentMessage(
            from_agent="dispatcher",
            to_agent=target_agent,
            message_type=MessageType.TASK,
            content=task.description,
            task_id=task.id,
            timestamp=datetime.now().isoformat(),
        )
        agent_registry.send_message(msg)
        
        return task.id
    
    def get_result(self, task_id: str) -> dict | None:
        """获取任务结果"""
        task = self.tasks.get(task_id)
        if task and task.status == "completed":
            return task.result
        return None

# 全局分发器
task_dispatcher = TaskDispatcher()
```

### 4.3 主管 Agent（Supervisor）

```python
# agent/supervisor.py
from agent.core import AIAgent
from agent.task_dispatcher import task_dispatcher, Task

class SupervisorAgent(AIAgent):
    """主管 Agent — 分解任务、协调多 Agent"""
    
    def __init__(self):
        system_prompt = """
        你是一个项目主管，负责：
        1. 理解用户的复杂请求
        2. 将任务分解为子任务
        3. 分发给合适的执行 Agent
        4. 协调各 Agent 的工作
        5. 整合结果返回给用户
        
        你协调的团队包括：
        - researcher：负责信息搜集和研究
        - writer：负责写作创作
        - editor：负责内容审查
        - coder：负责代码开发
        - music_agent：负责音乐创作
        """
        super().__init__(
            name="主管 Agent",
            system_prompt=system_prompt,
            model="gpt-4",
        )
    
    async def decompose_task(self, user_request: str) -> list[Task]:
        """将复杂任务分解为子任务"""
        # 使用 LLM 分析并分解任务
        response = await self.run(
            f"将以下任务分解为具体的子任务，"
            f"每个子任务包含 type 和 description：\n{user_request}"
        )
        
        # 解析响应，生成分解后的任务列表
        # （实际实现中需要更好的解析逻辑）
        tasks = []
        for i, line in enumerate(response.split("\n")):
            if line.strip():
                task = Task(
                    task_type="writing",
                    description=line.strip(),
                    payload={"step": i + 1}
                )
                tasks.append(task)
        
        return tasks
    
    async def coordinate(self, user_request: str) -> str:
        """协调多 Agent 完成复杂任务"""
        # 1. 分解任务
        tasks = await self.decompose_task(user_request)
        
        # 2. 逐个分发任务
        for task in tasks:
            task_id = task_dispatcher.dispatch(task)
            task.status = "running"
            
            # 3. 等待结果（实际用异步 + 回调）
            # 这里简化处理
            await self.wait_for_task(task_id)
        
        # 4. 整合结果
        results = [task_dispatcher.get_result(t.id) for t in tasks]
        final_response = self.integrate_results(results)
        
        return final_response
    
    async def wait_for_task(self, task_id: str):
        """等待任务完成（简化实现）"""
        import asyncio
        while True:
            result = task_dispatcher.get_result(task_id)
            if result:
                return result
            await asyncio.sleep(1)
    
    def integrate_results(self, results: list) -> str:
        """整合各 Agent 的结果"""
        return "\n\n".join([
            f"=== 结果 {i+1} ===\n{r}"
            for i, r in enumerate(results) if r
        ])
```

---

## 5. 多 Agent 消息流程图

```
用户：「帮我研究并创作一篇玄幻小说」

┌─────────────────────────────────────────────────────┐
│                    Supervisor Agent                    │
│  1. 理解请求：研究 + 写作 + 编辑                     │
│  2. 分解任务                                        │
└────────────────────┬────────────────────────────────┘
                     │
         ┌───────────┴───────────┐
         ▼                       ▼
┌─────────────────┐     ┌─────────────────┐
│ Research Agent  │     │ Writer Agent    │
│ 研究任务：搜索   │     │ 写作任务：创作   │
│ 10部热门小说     │     │ 小说第一章       │
└────────┬────────┘     └────────┬────────┘
         │                       │
         ▼                       ▼
    研究报告               小说初稿
         │                       │
         └───────────┬───────────┘
                     ▼
           ┌─────────────────┐
           │  Editor Agent   │
           │  审查：逻辑/文笔 │
           └────────┬────────┘
                    │
                    ▼
              最终稿件
                    │
                    ▼
              返回给用户
```

---

## 6. 任务协作状态机

```python
# agent/workflow.py
from enum import Enum

class WorkflowStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    WAITING_APPROVAL = "waiting_approval"
    REVISION = "revision"
    COMPLETED = "completed"
    FAILED = "failed"

class WorkflowTask:
    """工作流任务"""
    
    def __init__(self, task_id: str, agent_id: str, description: str):
        self.task_id = task_id
        self.agent_id = agent_id
        self.description = description
        self.status = WorkflowStatus.PENDING
        self.attempts = 0
        self.max_attempts = 3
        self.output = None
    
    def transition(self, new_status: WorkflowStatus, output: str = None):
        self.status = new_status
        if output:
            self.output = output
        if new_status == WorkflowStatus.FAILED:
            self.attempts += 1
    
    def can_retry(self) -> bool:
        return self.attempts < self.max_attempts

class SequentialWorkflow:
    """顺序工作流 — 一个接一个执行"""
    
    def __init__(self, tasks: list[WorkflowTask]):
        self.tasks = tasks
        self.current_index = 0
    
    async def run(self, agent_registry) -> str:
        results = []
        
        for task in self.tasks:
            task.transition(WorkflowStatus.RUNNING)
            
            # 执行任务
            agent = agent_registry.get_agent(task.agent_id)
            result = await agent.execute(task.description)
            
            if result.success:
                task.transition(WorkflowStatus.COMPLETED, result.output)
                results.append(result.output)
            else:
                task.transition(WorkflowStatus.FAILED)
                if task.can_retry():
                    # 重试
                    task.status = WorkflowStatus.PENDING
                else:
                    return f"任务失败：{task.agent_id}"
        
        return "\n".join(results)

class ParallelWorkflow:
    """并行工作流 — 同时执行多个任务"""
    
    def __init__(self, tasks: list[WorkflowTask]):
        self.tasks = tasks
    
    async def run(self, agent_registry) -> list[str]:
        import asyncio
        
        async def run_task(task: WorkflowTask):
            task.transition(WorkflowStatus.RUNNING)
            agent = agent_registry.get_agent(task.agent_id)
            result = await agent.execute(task.description)
            if result.success:
                task.transition(WorkflowStatus.COMPLETED, result.output)
                return result.output
            task.transition(WorkflowStatus.FAILED)
            return None
        
        # 并发执行所有任务
        results = await asyncio.gather(*[
            run_task(task) for task in self.tasks
        ])
        
        return [r for r in results if r]
```

---

## 7. 多 Agent 平台的整体架构

```
┌──────────────────────────────────────────────────────────────┐
│                     前端（React + TS）                        │
│  用户界面  │  实时 WebSocket  │  任务监控面板              │
└────────────────────────┬─────────────────────────────────┘
                           │ HTTP / WebSocket
┌──────────────────────────▼─────────────────────────────────┐
│                    API 网关层（FastAPI）                      │
│  /api/agents    │  /api/tasks    │  /ws/chat              │
└───────┬─────────────────────┬────────────────────────────┘
        │                     │
        ▼                     ▼
┌───────────────┐    ┌────────────────────────────────────┐
│ Agent 注册表   │    │        任务调度中心                  │
│ (Redis)       │    │  (Celery + Redis)                  │
│ - agent_1      │    │  - 定时任务（Cron）                 │
│ - agent_2      │    │  - 队列管理                        │
│ - agent_3      │    │  - 重试机制                        │
└───────┬───────┘    └──────────┬─────────────────────────┘
        │                         │
        ▼                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    Agent 执行层                              │
│                                                             │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐   │
│  │Supervisor│  │Research │  │ Writer  │  │ Coder   │   │
│  │ Agent    │  │ Agent   │  │ Agent   │  │ Agent   │   │
│  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘   │
│       │              │              │              │        │
│       └──────────────┴───────┬──────┴──────────────┘        │
│                               │                              │
│                    ┌──────────▼──────────┐                │
│                    │   工具层（Tools）     │                │
│                    │ web_search │ file   │                │
│                    │ code_exec  │ api    │                │
│                    └────────────┬─────────┘                │
│                                 │                           │
└─────────────────────────────────┼───────────────────────────┘
                                  ▼
                    ┌────────────────────────────────────┐
                    │       记忆层（Memory）            │
                    │ Short-term │ Long-term │ Entity   │
                    │ (Redis)    │ (PG+Vector)│          │
                    └────────────────────────────────────┘
```

---

## 8. 下周预告：系统集成 + 部署

第5周内容预告：
- 前后端联调（WebSocket 实时对话）
- Docker 容器化
- Nginx 配置
- 云服务器（腾讯云轻量应用服务器）部署
- CI/CD 流水线

---

*多 Agent 协作的核心：分 → 做 → 查 → 合*
