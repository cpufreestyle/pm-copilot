# 小浣熊 PM Copilot

> 面向项目经理的 AI Agent 统一管理平台 · Demo 版  
> 设计原则：**一个核心控制台 + 多平台适配器**

## 项目结构

```
pm-copilot/
├── frontend/   # 前端 Vue 3 + Vite + Element Plus
├── backend/    # 后端 FastAPI Mock 服务
└── docs/       # 架构文档与图片
```

## 快速开始

### 1. 启动后端（端口 8000）

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

浏览器访问 `http://localhost:8000/docs` 查看接口文档。

### 2. 启动前端（端口 5173）

```bash
cd frontend
npm install
npm run dev
```

浏览器访问 `http://localhost:5173`。

## 核心功能

| 页面 | 路径 | 说明 |
|------|------|------|
| 总览 | `/` | 项目数、Agent 数、运行任务、今日成本 |
| 项目 | `/projects` | 项目列表、里程碑、任务 |
| Agent | `/agents` | Agent 列表、平台来源、状态 |
| 运行 | `/runtime` | 执行 Trace、工具调用链 |
| 治理 | `/governance` | 权限、预算、风控、熔断 |
| 审计 | `/audit` | 操作记录、调用链回放 |

## 架构亮点：适配层

`backend/adapters/` 定义了统一接口 `BaseAdapter`，新增 Agent 平台只需实现：
- `register()` · `start()` · `stop()` · `status()` · `logs()` · `cost()`

已内置示例：`platform_a.py`、`platform_b.py`。

## 推送到 Gitee

```bash
# 1. 在 Gitee 新建空仓库 pm-copilot
# 2. 在本目录执行：
git init
git add .
git commit -m "init: 小浣熊 PM Copilot demo"
git branch -M master
git remote add origin https://gitee.com/你的用户名/pm-copilot.git
git push -u origin master
```

## License

MIT
