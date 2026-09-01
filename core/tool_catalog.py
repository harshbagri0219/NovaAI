from core.interfaces import Capability
from core.tool_adapter import ToolAdapter
from core.tool_registry import ToolRegistry


def _load_battery():
    from plugins import battery
    return battery.run


def _load_storage():
    from plugins import storage
    return storage.run


def _load_device():
    from plugins import device
    return device.run


def _load_time():
    from plugins import time
    return time.run


def _load_status():
    from plugins import status
    return status.run


def _load_help():
    from plugins import help
    return help.run


def _load_memory():
    from plugins import memory
    return memory.run


def _load_check_phone():
    from plugins import check_phone
    return check_phone.run


def _load_hello():
    from plugins import hello
    return hello.run


_registry = None


def get_registry():
    global _registry
    if _registry is None:
        registry = ToolRegistry()
        registry.register(ToolAdapter(name="battery", runnable=_load_battery(), capability=Capability.READ_ONLY))
        registry.register(ToolAdapter(name="storage", runnable=_load_storage(), capability=Capability.READ_ONLY))
        registry.register(ToolAdapter(name="device", runnable=_load_device(), capability=Capability.READ_ONLY))
        registry.register(ToolAdapter(name="time", runnable=_load_time(), capability=Capability.READ_ONLY))
        registry.register(ToolAdapter(name="status", runnable=_load_status(), capability=Capability.READ_ONLY))
        registry.register(ToolAdapter(name="help", runnable=_load_help(), capability=Capability.READ_ONLY))
        registry.register(ToolAdapter(name="memory", runnable=_load_memory(), capability=Capability.READ_ONLY))
        registry.register(ToolAdapter(name="check_phone", runnable=_load_check_phone(), capability=Capability.READ_ONLY))
        registry.register(ToolAdapter(name="hello", runnable=_load_hello(), capability=Capability.READ_ONLY))
        _registry = registry
    return _registry
