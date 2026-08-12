import importlib

PLUGIN_NAMES = [
    "battery",
    "device",
    "storage",
    "time",
    "status",
    "help",
    "memory"
]


def load_plugins():
  
    plugins = {}

    for name in PLUGIN_NAMES:
        module = importlib.import_module(f"plugins.{name}")
        plugins[name] = module.run

    return plugins