"""
Необходимо создать API для управления списком задач.
Каждая задача должна содержать заголовок и описание.
Для каждой задачи должна быть возможность указать статус (выполнена/не выполнена).

API должен содержать следующие конечные точки:
— GET /tasks — возвращает список всех задач.
— GET /tasks/{id} — возвращает задачу с указанным идентификатором.
— POST /tasks — добавляет новую задачу.
— PUT /tasks/{id} — обновляет задачу с указанным идентификатором.
— DELETE /tasks/{id} — удаляет задачу с указанным идентификатором.

Для каждой конечной точки необходимо проводить валидацию данных запроса и ответа.
Для этого использовать библиотеку Pydantic.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()


class Task(BaseModel):
    id: int
    title: str
    description: str
    status: bool = False


def get_task_by_id(task_id: int):
    for task in tasks_db:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")


tasks_db = []


# GET /tasks
@app.get("/tasks", response_model=List[Task])
async def get_tasks():
    return tasks_db


# GET /tasks/{id}
@app.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: int):
    return get_task_by_id(task_id)


# POST /tasks
@app.post("/tasks", response_model=Task)
async def create_task(task: Task):
    task.id = len(tasks_db) + 1
    tasks_db.append(task)
    return task


# PUT /tasks/{id}
@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, updated_task: Task):
    task = get_task_by_id(task_id)
    tasks_db[tasks_db.index(task)] = updated_task
    return updated_task


# DELETE /tasks/{id}
@app.delete("/tasks/{task_id}", response_model=Task)
async def delete_task(task_id: int):
    task = get_task_by_id(task_id)
    tasks_db.remove(task)
    return task
