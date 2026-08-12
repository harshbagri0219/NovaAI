import os
import importlib


def load_plugins():

    plugins = {}

    plugin_folder = "plugins"

    for file in os.listdir(plugin_folder):

        if file.endswith(".py") and file != "__init__.py":

            name = file[:-3]

            module = importlib.import_module(f"plugins.{name}")

            if hasattr(module, "run"):

                plugins[name] = module.run

    return plugins
