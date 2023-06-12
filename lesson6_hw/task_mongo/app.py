from bson import ObjectId
from fastapi import FastAPI, HTTPException
from typing import List

from starlette import status
from starlette.responses import JSONResponse

import models

app = FastAPI()
tasks_db = models.TasksDB()


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this tasks app!"}


@app.on_event("startup")
async def startup():
    await tasks_db.connect()


@app.on_event("shutdown")
async def shutdown():
    await tasks_db.disconnect()


@app.get('/tasks', response_model=List[models.Task])
async def get_tasks():
    cursor = tasks_db.collection.find()
    tasks = await cursor.to_list(length=100)
    for _t in tasks:
        _t = tasks_db.serialize(_t)
    return tasks


@app.get('/task/{task_id}', response_model=models.Task)
async def get_task_by_id(task_id: str):
    task = await tasks_db.collection.find_one(ObjectId(task_id))
    if task:
        return tasks_db.serialize(task)
    else:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Задача не найдена"}
        )


@app.get('/tasks/{task_title}', response_model=models.Task)
async def get_task_by_name(task_title: str):
    task = await tasks_db.collection.find_one({"title": task_title})
    if task:
        return tasks_db.serialize(task)
    else:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Задача не найдена"}
        )


@app.post('/tasks', response_model=models.Task)
async def create_task(task: models.Task):
    _id = await tasks_db.collection.insert_one(dict(task))
    task = await tasks_db.collection.find_one(ObjectId(_id.inserted_id))
    return tasks_db.serialize(task)


@app.put('/task/{task_title}', response_model=models.Task)
async def update_task(task_title: str, new_task: models.Task):
    task = {k: v for k, v in new_task.dict().items() if v is not None}
    update_result = await tasks_db.collection.update_one({"title": task_title}, {"$set": task})
    if update_result.modified_count == 1:
        return await tasks_db.collection.find_one({"title": task['title']})
    raise HTTPException(status_code=404, detail=f"Task {task_title} not found")


@app.delete('/tasks/{task_title}')
async def delete_task(task_title: str):
    delete_result = await tasks_db.collection.delete_one({"title": task_title})
    print(delete_result.raw_result)
    if delete_result.deleted_count == 1:
        return {"message": "task deleted"}
    raise HTTPException(status_code=404, detail=f"Task {task_title} not found")
