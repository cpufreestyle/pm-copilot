"""
小浣熊 PM Copilot - 后端 Mock 服务
"""
import os
import threading
from functools import wraps
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from mock_data import PROJECTS, AGENTS, RUNS, AUDITS, GOVERNANCE, DASHBOARD
from adapters import ADAPTERS

# ── 环境变量配置 ────────────────────────────────────────────────────────
from dotenv import load_dotenv
load_dotenv()

HOST       = os.getenv("HOST", "0.0.0.0")
PORT       = int(os.getenv("PORT", "8000"))
DEBUG      = os.getenv("DEBUG", "false").lower() == "true"
CORS_ORIGINS = [o.strip() for o in os.getenv("CORS_ORIGINS", "").split(",") if o.strip()] or [
    "http://localhost:5173",
    "http://localhost:3000",
]

# ── FastAPI 实例 ────────────────────────────────────────────────────────
app = FastAPI(
    title="PM Copilot API",
    version="1.1.0",
    description="小浣熊 PM Copilot 后端接口",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── 全局状态锁 ─────────────────────────────────────────────────────────
_state_lock = threading.Lock()


# ── 通用响应 ────────────────────────────────────────────────────────────
def ok(data=None, msg="ok"):
    return {"code": 0, "msg": msg, "data": data}


def paginate(data: list, page: int = 1, page_size: int = 20) -> dict:
    """分页辅助函数"""
    total = len(data)
    start = (page - 1) * page_size
    end   = start + page_size
    return {
        "items":   data[start:end],
        "total":   total,
        "page":    page,
        "page_size": page_size,
        "pages":   (total + page_size - 1) // page_size,
    }


# ── 健康检查 ────────────────────────────────────────────────────────────
@app.get("/health", summary="健康检查")
def health():
    return {"status": "ok", "version": "1.1.0", "debug": DEBUG}


# ── 总览 ────────────────────────────────────────────────────────────────
@app.get("/api/dashboard", summary="总览数据")
def get_dashboard():
    return ok(DASHBOARD)


# ── 项目 ────────────────────────────────────────────────────────────────
@app.get("/api/projects", summary="项目列表（分页）")
def list_projects(
    status:    Optional[str] = None,
    page:      int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页条数"),
):
    data = PROJECTS
    if status:
        data = [p for p in data if p["status"] == status]
    return ok(paginate(data, page, page_size))


@app.get("/api/projects/{pid}", summary="项目详情")
def get_project(pid: str):
    p = next((x for x in PROJECTS if x["id"] == pid), None)
    if not p:
        raise HTTPException(404, "project not found")
    related_agents = [a for a in AGENTS if a["project"] == pid]
    related_runs = [r for r in RUNS if r["project"] == pid]
    return ok({**p, "agent_list": related_agents, "run_list": related_runs})


# ── Agent ───────────────────────────────────────────────────────────────
@app.get("/api/agents", summary="Agent 列表（分页）")
def list_agents(
    platform:  Optional[str] = None,
    agent_status: Optional[str] = Query(None, alias="status", description="在线状态"),
    page:      int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    data = AGENTS
    if platform:     data = [a for a in data if a["platform"] == platform]
    if agent_status: data = [a for a in data if a["status"] == agent_status]
    return ok(paginate(data, page, page_size))


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
@app.get("/api/runs", summary="运行记录列表（分页）")
def list_runs(
    page:      int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    return ok(paginate(RUNS, page, page_size))


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
    with _state_lock:
        GOVERNANCE["circuit_breaker"] = enable
    return ok(GOVERNANCE, msg=f"熔断已{'开启' if enable else '关闭'}")


# ── 审计 ────────────────────────────────────────────────────────────────
@app.get("/api/audits", summary="审计日志（分页）")
def list_audits(
    user:      Optional[str] = None,
    page:      int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    data = AUDITS
    if user:
        data = [a for a in data if a["user"] == user]
    return ok(paginate(data, page, page_size))


# ── 适配层 ─────────────────────────────────────────────────────────────
@app.get("/api/adapters", summary="已接入的平台适配器")
def list_adapters():
    return ok([{"platform": k, "class": v.__class__.__name__} for k, v in ADAPTERS.items()])


@app.get("/", summary="根路径")
def root():
    return {"name": "PM Copilot API", "docs": "/docs", "health": "/health"}
