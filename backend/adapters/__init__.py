from .base import BaseAdapter
from .platform_a import PlatformAAdapter
from .platform_b import PlatformBAdapter

ADAPTERS = {
    "platform_a": PlatformAAdapter(),
    "platform_b": PlatformBAdapter(),
}
