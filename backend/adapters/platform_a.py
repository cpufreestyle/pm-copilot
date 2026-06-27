"""平台 A 适配器示例"""
import uuid, time, random
from .base import BaseAdapter


class PlatformAAdapter(BaseAdapter):
    platform_name = "platform_a"

    def __init__(self):
        self._runs = {}

    def register(self, agent_config):
        return f"a-{uuid.uuid4().hex[:8]}"

    def start(self, agent_id, payload):
        run_id = f"runA-{uuid.uuid4().hex[:8]}"
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
            {"ts": "10:21:01", "type": "input",  "msg": "解析用户请求"},
            {"ts": "10:21:02", "type": "tool",   "msg": "search_kb(query='项目状态')"},
            {"ts": "10:21:03", "type": "output", "msg": "生成回复"},
        ]

    def cost(self, run_id):
        return {"tokens": random.randint(800, 3000), "amount": round(random.uniform(0.1, 0.8), 2)}
