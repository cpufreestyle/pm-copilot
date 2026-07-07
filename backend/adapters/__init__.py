from .base import BaseAdapter
from .platform_a import PlatformAAdapter
from .platform_b import PlatformBAdapter
from .browser_use_adapter import BrowserUseAdapter
from .stock_dashboard_adapter import StockDashboardAdapter
from .sanguosha_adapter import SanguoshaAdapter
from .blender_adapter import BlenderAdapter
from .win_optimizer_adapter import WinOptimizerAdapter

ADAPTERS = {
    "platform_a": PlatformAAdapter(),
    "platform_b": PlatformBAdapter(),
    "browser_use": BrowserUseAdapter(),
    "stock_dashboard": StockDashboardAdapter(),
    "sanguosha_mobile": SanguoshaAdapter(),
    "blender_explode": BlenderAdapter(),
    "win_optimizer": WinOptimizerAdapter(),
}
