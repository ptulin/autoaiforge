import json
from typing import List, Dict, Optional
from pydantic import BaseModel, ValidationError
from celery import Celery

# Initialize Celery app
celery_app = Celery('agent_task_manager', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

class TaskDefinition(BaseModel):
    agent_id: int
    task_name: str
    dependencies: Optional[List[str]] = []
    priority: Optional[int] = 1

class AgentTaskManager:
    def __init__(self):
        self.tasks: Dict[str, TaskDefinition] = {}

    def add_task(self, agent_id: int, task_name: str, dependencies: Optional[List[str]] = None, priority: Optional[int] = 1):
        task_id = f"{agent_id}_{task_name}"
        if task_id in self.tasks:
            raise ValueError(f"Task {task_id} already exists.")

        task = TaskDefinition(agent_id=agent_id, task_name=task_name, dependencies=dependencies or [], priority=priority)
        self.tasks[task_id] = task
        return task

    def get_task(self, task_id: str) -> Optional[TaskDefinition]:
        return self.tasks.get(task_id)

    def execute_tasks(self):
        for task_id, task in sorted(self.tasks.items(), key=lambda x: x[1].priority):
            if all(dep in self.tasks for dep in task.dependencies):
                self._execute_task(task_id, task)
            else:
                print(f"Task {task_id} has unmet dependencies: {task.dependencies}")

    def _execute_task(self, task_id: str, task: TaskDefinition):
        print(f"Executing task {task_id}: {task.task_name}")
        execute_task.apply_async((task_id, task.dict()))

@celery_app.task
def execute_task(task_id: str, task_data: Dict):
    print(f"Task {task_id} is being processed with data: {task_data}")
    return {"task_id": task_id, "status": "completed"}

if __name__ == "__main__":
    manager = AgentTaskManager()
    manager.add_task(agent_id=1, task_name="fetch_data")
    manager.add_task(agent_id=1, task_name="process_data", dependencies=["fetch_data"])
    manager.execute_tasks()
