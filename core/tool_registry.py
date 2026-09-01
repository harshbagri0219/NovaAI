from core.interfaces import Capability
from core.tool_adapter import ToolAdapter


class ToolRegistry:

    def __init__(self):
        self._tools = {}

    def register(self, tool):
        if isinstance(tool, ToolAdapter):
            self._tools[tool.name] = tool
            return tool
        raise TypeError("Only ToolAdapter instances may be registered")

    def get(self, name):
        return self._tools.get(name)

    def all(self):
        return dict(self._tools)

    @classmethod
    def from_plugin_map(cls, plugin_map):
        registry = cls()
        for name, runnable in plugin_map.items():
            capability = registry._infer_capability(name, runnable)
            tool = ToolAdapter(name=name, runnable=runnable, capability=capability)
            registry.register(tool)
        return registry

    def _infer_capability(self, name, runnable):
        read_only_intents = {"time", "help"}
        if name in read_only_intents:
            return Capability.READ_ONLY
        return Capability.STATE_CHANGING
