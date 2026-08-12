from tasks.task_engine import Task

task = Task("Morning Routine")

task.add_step("Check battery")

task.add_step("Check weather")

task.add_step("Read today's calendar")

print(task.run())