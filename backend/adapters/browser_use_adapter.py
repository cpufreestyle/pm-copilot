"""browser-use 适配器

管理 browser-use 浏览器自动化 Agent。
支持: 启动任务、查看步骤日志、停止运行、统计 LLM 成本
"""
import uuid
import time
import random
from typing import Any, Dict, List
from .base import BaseAdapter


class BrowserUseAdapter(BaseAdapter):
    """browser-use 项目适配器"""

    platform_name = "browser_use"

    def __init__(self):
        self._agents: Dict[str, dict] = {}
        self._runs: Dict[str, dict] = {}

    def register(self, agent_config: Dict[str, Any]) -> str:
        agent_id = f"bu-{uuid.uuid4().hex[:8]}"
        self._agents[agent_id] = {
            "config": agent_config,
            "model": agent_config.get("model", "step-1-8k"),
            "max_steps": agent_config.get("max_steps", 50),
            "created_at": time.time(),
        }
        return agent_id

    def start(self, agent_id: str, payload: Dict[str, Any]) -> str:
        run_id = f"bu-run-{uuid.uuid4().hex[:8]}"
        task = payload.get("task", "")
        self._runs[run_id] = {
            "agent_id": agent_id,
            "task": task,
            "status": "running",
            "start_time": time.time(),
            "steps": [],
            "total_tokens": 0,
            "total_cost": 0.0,
        }
        return run_id

    def stop(self, run_id: str) -> bool:
        if run_id in self._runs:
            self._runs[run_id]["status"] = "stopped"
            self._runs[run_id]["end_time"] = time.time()
            return True
        return False

    def status(self, run_id: str) -> Dict[str, Any]:
        run = self._runs.get(run_id)
        if not run:
            return {"status": "unknown", "message": "run not found"}
        elapsed = time.time() - run["start_time"]
        return {
            "status": run["status"],
            "task": run["task"][:100],
            "elapsed_seconds": round(elapsed, 1),
            "steps_completed": len(run["steps"]),
            "agent_id": run["agent_id"],
        }

    def logs(self, run_id: str) -> List[Dict[str, Any]]:
        run = self._runs.get(run_id)
        if not run:
            return []
        return run["steps"]

    def cost(self, run_id: str) -> Dict[str, float]:
        run = self._runs.get(run_id)
        if not run:
            return {"tokens": 0, "amount": 0.0}
        return {
            "tokens": run["total_tokens"],
            "amount": round(run["total_cost"], 4),
        }
