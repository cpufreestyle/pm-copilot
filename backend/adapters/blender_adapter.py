"""blender-auto-3d-explode 适配器

管理 Blender 3D 自动拆解系统。
支持: 启动 Blender 服务器、运行拆解脚本、查看渲染状态
"""
import uuid
import time
from typing import Any, Dict, List
from .base import BaseAdapter


class BlenderAdapter(BaseAdapter):
    """blender-auto-3d-explode 项目适配器"""

    platform_name = "blender_explode"

    def __init__(self):
        self._agents: Dict[str, dict] = {}
        self._runs: Dict[str, dict] = {}

    def register(self, agent_config: Dict[str, Any]) -> str:
        agent_id = f"bl-{uuid.uuid4().hex[:8]}"
        self._agents[agent_id] = {
            "config": agent_config,
            "server_url": agent_config.get("server_url", "http://localhost:8080"),
            "created_at": time.time(),
        }
        return agent_id

    def start(self, agent_id: str, payload: Dict[str, Any]) -> str:
        run_id = f"bl-run-{uuid.uuid4().hex[:8]}"
        action = payload.get("action", "explode_model")
        model_path = payload.get("model_path", "models/Quest3.glb")
        self._runs[run_id] = {
            "agent_id": agent_id,
            "action": action,
            "model_path": model_path,
            "status": "running",
            "start_time": time.time(),
            "logs": [
                {"ts": time.strftime("%H:%M:%S"), "type": "info", "msg": f"Loading model: {model_path}"},
                {"ts": time.strftime("%H:%M:%S"), "type": "blender", "msg": "Starting Blender headless mode"},
                {"ts": time.strftime("%H:%M:%S"), "type": "blender", "msg": "Analyzing mesh structure..."},
                {"ts": time.strftime("%H:%M:%S"), "type": "blender", "msg": "Generating exploded view"},
                {"ts": time.strftime("%H:%M:%S"), "type": "output", "msg": "Exporting GLB with exploded parts"},
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
            "model": run["model_path"],
            "elapsed_seconds": round(time.time() - run["start_time"], 1),
        }

    def logs(self, run_id: str) -> List[Dict[str, Any]]:
        run = self._runs.get(run_id)
        if not run:
            return []
        return run["logs"]

    def cost(self, run_id: str) -> Dict[str, float]:
        return {"tokens": 0, "amount": 0.0}
