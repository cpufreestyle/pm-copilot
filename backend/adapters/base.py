"""
适配层标准接口 —— 多平台 Agent 接入的核心抽象
任何新接入的 Agent 平台只需实现本类的方法
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List


class BaseAdapter(ABC):
    """统一 Agent 平台适配器接口"""

    platform_name: str = "base"

    @abstractmethod
    def register(self, agent_config: Dict[str, Any]) -> str:
        """注册一个 Agent，返回 agent_id"""

    @abstractmethod
    def start(self, agent_id: str, payload: Dict[str, Any]) -> str:
        """启动一次运行，返回 run_id"""

    @abstractmethod
    def stop(self, run_id: str) -> bool:
        """停止运行"""

    @abstractmethod
    def status(self, run_id: str) -> Dict[str, Any]:
        """查询状态：running / success / failed"""

    @abstractmethod
    def logs(self, run_id: str) -> List[Dict[str, Any]]:
        """拉取调用链日志"""

    @abstractmethod
    def cost(self, run_id: str) -> Dict[str, float]:
        """导出本次运行的成本（tokens / 金额）"""
