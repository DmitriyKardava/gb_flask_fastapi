from fastapi import FastAPI
from fastapi.params import Path
from models import tasks, Task
from typing import List

app = FastAPI()


@app.get('/tasks', response_model=List[Task])
async def get_tasks():
    print(tasks)
    return tasks


@app.get('/task/{task_id}', response_model=Task)
async def get_task(task_id: int = Path(..., ge=0, lt=len(tasks))):
    return tasks[task_id]


@app.post('/tasks', response_model=Task)
async def create_task(task: Task):
    tasks.append(task)
    return task


@app.put('/task/{task_id}', response_model=Task)
async def update_task(task_id: int, new_task: Task):
    tasks[task_id] = new_task
    return new_task


@app.delete('/tasks/{task_id}', response_model=Task)
async def delete_task(task_id: int):
    return tasks.pop(task_id)
