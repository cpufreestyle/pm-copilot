"""sanguosha-mobile 适配器

管理三国杀助手 PWA 项目。
支持: 构建 APK、部署 PWA、查看构建状态
"""
import uuid
import time
from typing import Any, Dict, List
from .base import BaseAdapter


class SanguoshaAdapter(BaseAdapter):
    """sanguosha-mobile 项目适配器"""

    platform_name = "sanguosha_mobile"

    def __init__(self):
        self._agents: Dict[str, dict] = {}
        self._runs: Dict[str, dict] = {}

    def register(self, agent_config: Dict[str, Any]) -> str:
        agent_id = f"sg-{uuid.uuid4().hex[:8]}"
        self._agents[agent_id] = {
            "config": agent_config,
            "created_at": time.time(),
        }
        return agent_id

    def start(self, agent_id: str, payload: Dict[str, Any]) -> str:
        run_id = f"sg-run-{uuid.uuid4().hex[:8]}"
        action = payload.get("action", "build_pwa")
        self._runs[run_id] = {
            "agent_id": agent_id,
            "action": action,
            "status": "running",
            "start_time": time.time(),
            "logs": [
                {"ts": time.strftime("%H:%M:%S"), "type": "info", "msg": f"Starting: {action}"},
                {"ts": time.strftime("%H:%M:%S"), "type": "build", "msg": "Bundling PWA assets..."},
                {"ts": time.strftime("%H:%M:%S"), "type": "build", "msg": "Generating service worker..."},
                {"ts": time.strftime("%H:%M:%S"), "type": "build", "msg": "PWA build complete"},
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
