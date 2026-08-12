from task.task_engine import TaskEngine

from plugins import battery
from plugins import storage
from plugins import device


def run():

    engine = TaskEngine()

    engine.add(battery.run)

    engine.add(storage.run)

    engine.add(device.run)

    return engine.run()