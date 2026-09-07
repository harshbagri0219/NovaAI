from core.interfaces import Capability
from core.tool_adapter import ToolAdapter


class ToolRegistry:

    def __init__(self):
        self._tools = {}

    def register(self, tool):
        if isinstance(tool, ToolAdapter):
            if tool.capability is None:
                raise ValueError("Tool capability cannot be None")
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

        for name, entry in plugin_map.items():
            if not isinstance(entry, tuple) or len(entry) != 2:
                raise TypeError(
                    f"Plugin '{name}' must provide "
                    "(runnable, capability)"
                )

            runnable, capability = entry

            tool = ToolAdapter(
                name=name,
                runnable=runnable,
                capability=capability,
            )

            registry.register(tool)

        return registry