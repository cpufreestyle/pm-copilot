"""
小浣熊 PM Copilot - 后端 Mock 服务
"""
import threading
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from mock_data import PROJECTS, AGENTS, RUNS, AUDITS, GOVERNANCE, DASHBOARD
from adapters import ADAPTERS

app = FastAPI(title="PM Copilot API", version="1.0.0",
              description="小浣熊 PM Copilot 后端接口")

# ── CORS：仅允许已知的开发/生产域名 ──────────────────────────────────────
ALLOWED_ORIGINS = [
    "http://localhost:5173",   # Vite dev server
    "http://localhost:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── 全局状态锁（防止并发写入冲突）─────────────────────────────────────────
_state_lock = threading.Lock()


# ── 通用响应 ──────────────────────────────────────────────────────────────
def ok(data=None, msg="ok"):
    return {"code": 0, "msg": msg, "data": data}


# ── 健康检查 ──────────────────────────────────────────────────────────────
@app.get("/health", summary="健康检查")
def health():
    return {"status": "ok", "version": "1.0.0"}


# ── 总览 ────────────────────────────────────────────────────────────────
@app.get("/api/dashboard", summary="总览数据")
def get_dashboard():
    return ok(DASHBOARD)


# ── 项目 ────────────────────────────────────────────────────────────────
@app.get("/api/projects", summary="项目列表")
def list_projects(status: Optional[str] = None):
    data = PROJECTS
    if status:
        data = [p for p in data if p["status"] == status]
    return ok(data)


@app.get("/api/projects/{pid}", summary="项目详情")
def get_project(pid: str):
    p = next((x for x in PROJECTS if x["id"] == pid), None)
    if not p:
        raise HTTPException(404, "project not found")
    related_agents = [a for a in AGENTS if a["project"] == pid]
    related_runs = [r for r in RUNS if r["project"] == pid]
    return ok({**p, "agent_list": related_agents, "run_list": related_runs})


# ── Agent ───────────────────────────────────────────────────────────────
@app.get("/api/agents", summary="Agent 列表")
def list_agents(platform: Optional[str] = None, status: Optional[str] = None):
    data = AGENTS
    if platform: data = [a for a in data if a["platform"] == platform]
    if status:   data = [a for a in data if a["status"] == status]
    return ok(data)


class AgentCreate(BaseModel):
    name: str
    platform: str
    owner: str

@app.post("/api/agents", summary="新建 Agent（演示适配层调用）")
def create_agent(req: AgentCreate):
    if req.platform not in ADAPTERS:
        raise HTTPException(400, f"unsupported platform: {req.platform}")
    adapter = ADAPTERS[req.platform]
    agent_id = adapter.register({"name": req.name, "owner": req.owner})
    return ok({"agent_id": agent_id, "platform": req.platform})


# ── 运行 ────────────────────────────────────────────────────────────────
@app.get("/api/runs", summary="运行记录列表")
def list_runs():
    return ok(RUNS)


@app.get("/api/runs/{rid}", summary="运行详情（含 trace）")
def get_run(rid: str):
    r = next((x for x in RUNS if x["id"] == rid), None)
    if not r:
        raise HTTPException(404, "run not found")
    adapter = ADAPTERS["platform_a"]
    trace = adapter.logs(rid)
    return ok({**r, "trace": trace,
               "prompt": "请分析项目 P001 当前进度并给出风险提示。",
               "output": "项目 P001 当前进度 65%，按当前速度可按期交付，建议关注 Agent-03 异常。"})


@app.post("/api/runs/{rid}/replay", summary="回放运行")
def replay(rid: str):
    return ok({"new_run_id": f"replay-{rid}"}, msg="已发起回放")


# ── 治理 ────────────────────────────────────────────────────────────────
@app.get("/api/governance", summary="治理总览")
def governance():
    return ok(GOVERNANCE)


@app.post("/api/governance/circuit-breaker", summary="切换熔断开关")
def toggle_circuit_breaker(enable: bool):
    # 线程安全写入全局状态
    with _state_lock:
        GOVERNANCE["circuit_breaker"] = enable
    return ok(GOVERNANCE, msg=f"熔断已{'开启' if enable else '关闭'}"})


# ── 审计 ────────────────────────────────────────────────────────────────
@app.get("/api/audits", summary="审计日志")
def list_audits(user: Optional[str] = None):
    data = AUDITS
    if user: data = [a for a in data if a["user"] == user]
    return ok(data)


# ── 适配层 ─────────────────────────────────────────────────────────────
@app.get("/api/adapters", summary="已接入的平台适配器")
def list_adapters():
    return ok([{"platform": k, "class": v.__class__.__name__} for k, v in ADAPTERS.items()])


@app.get("/", summary="根路径")
def root():
    return {"name": "PM Copilot API", "docs": "/docs"}
