"""平台 B 适配器示例"""
import uuid, time, random
from .base import BaseAdapter


class PlatformBAdapter(BaseAdapter):
    platform_name = "platform_b"

    def __init__(self):
        self._runs = {}

    def register(self, agent_config):
        return f"b-{uuid.uuid4().hex[:8]}"

    def start(self, agent_id, payload):
        run_id = f"runB-{uuid.uuid4().hex[:8]}"
        self._runs[run_id] = {"status": "running", "start": time.time()}
        return run_id

    def stop(self, run_id):
        if run_id in self._runs:
            self._runs[run_id]["status"] = "stopped"
            return True
        return False

    def status(self, run_id):
        return self._runs.get(run_id, {"status": "unknown"})

    def logs(self, run_id):
        return [
            {"ts": "10:22:01", "type": "input",  "msg": "接收任务"},
            {"ts": "10:22:02", "type": "reason", "msg": "规划步骤"},
            {"ts": "10:22:03", "type": "tool",   "msg": "call_api(endpoint='/orders')"},
            {"ts": "10:22:04", "type": "output", "msg": "返回结果"},
        ]

    def cost(self, run_id):
        return {"tokens": random.randint(500, 2500), "amount": round(random.uniform(0.05, 0.6), 2)}
