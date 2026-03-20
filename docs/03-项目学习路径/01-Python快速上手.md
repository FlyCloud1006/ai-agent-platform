# Python 快速上手 — 有编程经验的开发者指南

> 适用对象：已有编程经验（JavaScript/TypeScript），零 Python 基础  
> 目标：快速掌握 Python 语法，能读懂和编写 Agent 相关代码  
> 重点：Python 和 TS 的差异 + 常用语法速查

---

## 1. Python vs TypeScript 语法对比

| 概念 | TypeScript | Python |
|------|-----------|--------|
| 变量声明 | `let x: number = 1` | `x = 1` |
| 常量 | `const PI = 3.14` | `PI = 3.14` |
| 函数 | `function add(a: number, b: number): number { return a + b }` | `def add(a, b): return a + b` |
| 箭头函数 | `(a, b) => a + b` | `lambda a, b: a + b` |
| 列表 | `const arr: number[] = [1, 2, 3]` | `arr = [1, 2, 3]` |
| 字典 | `const obj: Record<string, number> = {a: 1}` | `obj = {"a": 1}` |
| 类 | `class Person { name: string; constructor(name: string) { this.name = name } }` | `class Person: def __init__(self, name): self.name = name` |
| 类型注解 | `let x: string = "hello"` | `x: str = "hello"` |
| 空值 | `null` / `undefined` | `None` |
| 布尔 | `true` / `false` | `True` / `False` |
| 打印 | `console.log(x)` | `print(x)` |
| 字符串插值 | `` `Hello ${name}` `` | `f"Hello {name}"` |

---

## 2. 基础语法

### 2.1 变量与数据类型

```python
# 变量（不用声明类型）
name = "张三"           # str
age = 25                # int
height = 1.75           # float
is_active = True        # bool
skills = ["JS", "TS"]  # list（类似 JS 数组）
user = {"name": "张三", "age": 25}  # dict（类似 JS 对象）

# 类型注解（可选，Python 3.5+）
name: str = "张三"
age: int = 25
items: list[str] = ["a", "b", "c"]  # Python 3.9+
```

### 2.2 函数

```python
# 基本函数
def greet(name: str) -> str:
    return f"你好，{name}！"

# 默认参数
def greet(name: str, age: int = 18) -> str:
    return f"{name}，{age}岁"

# 可变参数
def sum(*numbers: int) -> int:
    total = 0
    for n in numbers:
        total += n
    return total

sum(1, 2, 3, 4, 5)  # 15

# 匿名函数（lambda）
square = lambda x: x ** 2
square(5)  # 25

# 多返回值
def get_user():
    return "张三", 25, True

name, age, is_active = get_user()
```

### 2.3 条件与循环

```python
# 条件
age = 20
if age >= 18:
    print("成年人")
elif age >= 6:
    print("未成年人")
else:
    print("儿童")

# 三元表达式
status = "成年人" if age >= 18 else "未成年"

# for 循环
for i in range(5):  # range(5) = [0, 1, 2, 3, 4]
    print(i)

for item in ["苹果", "香蕉", "橙子"]:
    print(item)

# while 循环
count = 0
while count < 5:
    print(count)
    count += 1

# 列表推导式（常用！）
squares = [x ** 2 for x in range(10)]
# [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

even_squares = [x ** 2 for x in range(10) if x % 2 == 0]
# [0, 4, 16, 36, 64]
```

### 2.4 列表和字典

```python
# 列表
fruits = ["苹果", "香蕉", "橙子"]
fruits.append("葡萄")     # 追加
fruits.insert(0, "草莓")  # 插入
fruits.remove("香蕉")    # 删除
last = fruits.pop()      # 弹出最后一个

# 切片（类似 JS 的 slice）
arr = [0, 1, 2, 3, 4, 5]
arr[1:4]    # [1, 2, 3]  （索引1到3）
arr[:3]     # [0, 1, 2]  （开头到索引2）
arr[3:]     # [3, 4, 5]  （索引3到结尾）
arr[-2:]    # [4, 5]     （最后2个）

# 字典
user = {"name": "张三", "age": 25}
user["city"] = "北京"       # 添加
user["age"] = 26             # 修改
del user["age"]              # 删除
name = user.get("name")     # 获取（不抛异常）
name = user.get("age", 0)    # 获取并提供默认值

# 遍历字典
for key, value in user.items():
    print(f"{key}: {value}")

for key in user.keys():
    print(key)

for value in user.values():
    print(value)
```

### 2.5 类与对象

```python
class Agent:
    # 类变量（所有实例共享）
    version = "1.0"
    
    # 初始化方法（类似 TS 的 constructor）
    def __init__(self, name: str, model: str = "gpt-4"):
        self.name = name          # 实例变量
        self.model = model
        self.is_running = False
    
    # 实例方法
    def start(self):
        self.is_running = True
        print(f"{self.name} 已启动（模型：{self.model}）")
    
    def stop(self):
        self.is_running = False
        print(f"{self.name} 已停止")
    
    # 字符串表示（类似 JS 的 toString()）
    def __str__(self):
        return f"Agent({self.name}, {self.model}, running={self.is_running})"

# 继承
class MusicAgent(Agent):
    def __init__(self, name: str):
        super().__init__(name, model="gpt-4o-music")
    
    def compose(self, style: str) -> str:
        return f"创作{style}风格的音乐"

# 使用
agent = Agent("小雅", "gpt-4")
print(agent)           # Agent(小雅, gpt-4, running=False)
agent.start()          # 小雅 已启动（模型：gpt-4）
print(agent.is_running) # True
```

---

## 3. Python 特有的重要概念（TS 没有的）

### 3.1 缩进（indent）—— Python 用缩进表示代码块！

```python
# ✅ 正确
if True:
    print("缩进一级")
    if True:
        print("缩进两级")

# ❌ 错误（会报错）
if True:
print("没缩进会报错")  # IndentationError
```

### 3.2 异常处理

```python
try:
    result = 10 / 0
except ZeroDivisionError:
    print("不能除以零")
except Exception as e:
    print(f"其他错误：{e}")
else:
    print("没有异常时执行")
finally:
    print("无论有没有异常都执行")
```

### 3.3 上下文管理器（with 语句）

```python
# 打开文件（自动关闭）
with open("test.txt", "w", encoding="utf-8") as f:
    f.write("Hello, Python!")

# 类似 JS 的 using（TS 5.2+）
# using console = console;
```

### 3.4 装饰器（Decorator）

```python
# 类似 JS 的装饰器（ES2018+）
def log_calls(func):
    def wrapper(*args, **kwargs):
        print(f"调用 {func.__name__}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} 执行完成")
        return result
    return wrapper

@log_calls
def add(a, b):
    return a + b

add(1, 2)
# 调用 add
# add 执行完成
```

### 3.5 生成器（Generator）

```python
# 类似 JS 的 Generator 函数
def count_to(n):
    i = 0
    while i < n:
        yield i  # 暂停并返回值
        i += 1

for num in count_to(5):
    print(num)  # 0, 1, 2, 3, 4

# vs 返回列表
def count_to_list(n):
    return list(range(n))
```

---

## 4. 常用标准库速查

```python
# 文件操作
import os
os.path.join("dir", "file.txt")    # 路径拼接
os.listdir(".")                     # 列出目录
os.makedirs("new_dir", exist_ok=True)  # 创建目录

# JSON 处理
import json
data = {"name": "张三", "age": 25}
json_str = json.dumps(data)         # 对象 → JSON 字符串
parsed = json.loads(json_str)       # JSON 字符串 → 对象

# 时间
import datetime
now = datetime.datetime.now()
later = now + datetime.timedelta(hours=2)

# HTTP 请求
import requests
response = requests.get("https://api.example.com/data")
print(response.status_code)
print(response.json())

# 日志
import logging
logger = logging.getLogger("my_agent")
logger.info("Agent 启动")
logger.error("出错了")
```

---

## 5. 异步编程（async / await）

```python
import asyncio

# 定义异步函数
async def fetch_data(url: str) -> dict:
    # 模拟网络请求
    await asyncio.sleep(1)  # 等待1秒（不阻塞其他任务）
    return {"url": url, "data": "some data"}

# 并发执行多个异步任务
async def main():
    # 同时发起多个请求
    results = await asyncio.gather(
        fetch_data("https://api1.com"),
        fetch_data("https://api2.com"),
        fetch_data("https://api3.com"),
    )
    for r in results:
        print(r)

# 运行异步程序
asyncio.run(main())
```

### 对比 TS 的异步：

```typescript
// TypeScript
async function fetchData(url: string): Promise<dict> {
  const response = await fetch(url);
  return response.json();
}

async function main() {
  const [r1, r2, r3] = await Promise.all([
    fetchData("https://api1.com"),
    fetchData("https://api2.com"),
    fetchData("https://api3.com"),
  ]);
}
```

---

## 6. 类型提示（Type Hints）

```python
from typing import List, Dict, Optional, Union, Callable

# 基础类型
name: str = "张三"
age: int = 25
items: List[int] = [1, 2, 3]

# 可选类型（类似 TS 的 ?）
def greet(name: Optional[str] = None):
    if name is None:
        print("你好")
    else:
        print(f"你好，{name}")

# 联合类型（类似 TS 的 |）
def process(value: Union[int, str]) -> str:
    return str(value)

# 字典类型
def get_user() -> Dict[str, str]:
    return {"name": "张三", "city": "北京"}

# 函数类型
def apply(func: Callable[[int, int], int], a: int, b: int) -> int:
    return func(a, b)

apply(lambda x, y: x + y, 1, 2)  # 3
```

---

## 7. pip 和虚拟环境

```bash
# 安装包
pip install langchain langgraph fastapi uvicorn

# 安装特定版本
pip install requests==2.28.0

# requirements.txt 批量安装
pip install -r requirements.txt

# 创建虚拟环境（类似 npm 的 node_modules 隔离）
python -m venv venv

# 激活虚拟环境
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# 退出虚拟环境
deactivate
```

**requirements.txt 示例：**
```
fastapi==0.104.1
uvicorn==0.24.0
langchain==0.1.0
langgraph==0.0.20
requests==2.28.0
python-dotenv==1.0.0
```

---

## 8. FastAPI 快速入门

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# 请求体模型（类似 TS 的 interface）
class User(BaseModel):
    name: str
    age: int
    email: str | None = None  # 可选字段

# GET 路由
@app.get("/")
def read_root():
    return {"message": "Hello, AI Agent!"}

# GET 带参数
@app.get("/agent/{agent_id}")
def get_agent(agent_id: int, verbose: bool = False):
    return {
        "id": agent_id,
        "name": f"Agent-{agent_id}",
        "verbose": verbose
    }

# POST 请求
@app.post("/agents")
def create_agent(user: User):
    return {
        "created": True,
        "name": user.name,
        "age": user.age
    }

# 启动命令：
# uvicorn main:app --reload --port 8000
```

---

*文档版本：v1.0 | Python 速查手册*
