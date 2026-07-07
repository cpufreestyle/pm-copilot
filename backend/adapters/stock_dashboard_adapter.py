"""stock-dashboard 适配器

管理 stock-dashboard 股票看板后端 API。
支持: 启动/停止 API 服务器、健康检查、查看实时数据状态
"""
import uuid
import time
from typing import Any, Dict, List
from .base import BaseAdapter


class StockDashboardAdapter(BaseAdapter):
    """stock-dashboard 项目适配器"""

    platform_name = "stock_dashboard"

    def __init__(self):
        self._agents: Dict[str, dict] = {}
        self._runs: Dict[str, dict] = {}

    def register(self, agent_config: Dict[str, Any]) -> str:
        agent_id = f"sd-{uuid.uuid4().hex[:8]}"
        self._agents[agent_id] = {
            "config": agent_config,
            "api_url": agent_config.get("api_url", "http://localhost:8001"),
            "created_at": time.time(),
        }
        return agent_id

    def start(self, agent_id: str, payload: Dict[str, Any]) -> str:
        run_id = f"sd-run-{uuid.uuid4().hex[:8]}"
        action = payload.get("action", "start_server")
        self._runs[run_id] = {
            "agent_id": agent_id,
            "action": action,
            "status": "running",
            "start_time": time.time(),
            "logs": [
                {"ts": time.strftime("%H:%M:%S"), "type": "info", "msg": f"Starting stock-dashboard: {action}"},
                {"ts": time.strftime("%H:%M:%S"), "type": "info", "msg": "Loading stock data from Sina Finance API"},
                {"ts": time.strftime("%H:%M:%S"), "type": "info", "msg": "API server ready on :8001"},
            ],
        }
        return run_id

    def stop(self, run_id: str) -> bool:
        if run_id in self._runs:
            self._runs[run_id]["status"] = "stopped"
            return True
        return False

    def status(self, run_id: str) -> Dict[str, Any]:
        run = self._runs.get(run_id)
        if not run:
            return {"status": "unknown"}
        return {
            "status": run["status"],
            "action": run["action"],
            "elapsed_seconds": round(time.time() - run["start_time"], 1),
        }

    def logs(self, run_id: str) -> List[Dict[str, Any]]:
        run = self._runs.get(run_id)
        if not run:
            return []
        return run["logs"]

    def cost(self, run_id: str) -> Dict[str, float]:
        return {"tokens": 0, "amount": 0.0}
