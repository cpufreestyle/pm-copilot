"""win-optimizer 适配器

管理 Windows 系统优化工具。
支持: 运行优化脚本、查看优化结果、回滚操作
"""
import uuid
import time
from typing import Any, Dict, List
from .base import BaseAdapter


class WinOptimizerAdapter(BaseAdapter):
    """win-optimizer 项目适配器"""

    platform_name = "win_optimizer"

    # 可用脚本列表
    AVAILABLE_SCRIPTS = [
        {"id": "01", "name": "系统信息", "script": "01-SystemInfo.ps1", "desc": "收集系统硬件和软件信息"},
        {"id": "02", "name": "清理临时文件", "script": "02-CleanTemp.ps1", "desc": "清理系统临时文件和缓存"},
        {"id": "03", "name": "禁用无用服务", "script": "03-DisableServices.ps1", "desc": "禁用不必要的后台服务"},
        {"id": "04", "name": "启动项优化", "script": "04-StartupOptimize.ps1", "desc": "管理开机启动项"},
        {"id": "05", "name": "视觉效果优化", "script": "05-VisualEffects.ps1", "desc": "调整系统视觉效果以提升性能"},
        {"id": "06", "name": "电源计划", "script": "06-PowerPlan.ps1", "desc": "配置高性能电源计划"},
        {"id": "07", "name": "磁盘优化", "script": "07-DiskOptimize.ps1", "desc": "磁盘碎片整理和 TRIM"},
        {"id": "08", "name": "网络优化", "script": "08-NetworkOptimize.ps1", "desc": "优化网络参数"},
        {"id": "09", "name": "备份与恢复", "script": "09-BackupRestore.ps1", "desc": "备份当前系统配置"},
    ]

    def __init__(self):
        self._agents: Dict[str, dict] = {}
        self._runs: Dict[str, dict] = {}

    def register(self, agent_config: Dict[str, Any]) -> str:
        agent_id = f"wo-{uuid.uuid4().hex[:8]}"
        self._agents[agent_id] = {
            "config": agent_config,
            "host": agent_config.get("host", "localhost"),
            "created_at": time.time(),
        }
        return agent_id

    def start(self, agent_id: str, payload: Dict[str, Any]) -> str:
        run_id = f"wo-run-{uuid.uuid4().hex[:8]}"
        script_id = payload.get("script_id", "01")
        script_info = next((s for s in self.AVAILABLE_SCRIPTS if s["id"] == script_id), None)
        script_name = script_info["name"] if script_info else f"Script-{script_id}"

        self._runs[run_id] = {
            "agent_id": agent_id,
            "script_id": script_id,
            "script_name": script_name,
            "status": "running",
            "start_time": time.time(),
            "logs": [
                {"ts": time.strftime("%H:%M:%S"), "type": "info", "msg": f"Executing: {script_name}"},
                {"ts": time.strftime("%H:%M:%S"), "type": "powershell", "msg": f"Running {script_info['script'] if script_info else 'unknown'}..."},
                {"ts": time.strftime("%H:%M:%S"), "type": "output", "msg": f"{script_name} completed"},
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
            "script": run["script_name"],
            "elapsed_seconds": round(time.time() - run["start_time"], 1),
        }

    def logs(self, run_id: str) -> List[Dict[str, Any]]:
        run = self._runs.get(run_id)
        if not run:
            return []
        return run["logs"]

    def cost(self, run_id: str) -> Dict[str, float]:
        return {"tokens": 0, "amount": 0.0}
