from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Modelo de datos
class Task(BaseModel):
    id: int
    title: str
    description: str = None
    done: bool = False

# Base de datos en memoria
tasks: List[Task] = [
    Task(id=1, title="Tarea 1", description="Primera tarea", done=False),
    Task(id=2, title="Tarea 2", description="Segunda tarea", done=True),
    Task(id=3, title="Tarea 3", description="3ra tarea", done=False),
    Task(id=4, title="Tarea 4", description="4ta. tarea", done=True)
]

# Ruta para obtener todas las tareas
@app.get("/tasks", response_model=List[Task])
def get_tasks():
    return tasks

# Ruta para obtener una tarea por ID
@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    task = next((t for t in tasks if t.id == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

# Ruta para crear una nueva tarea
@app.post("/tasks", response_model=Task)
def create_task(task: Task):
    tasks.append(task)
    return task

# Ruta para actualizar una tarea existente
@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, updated_task: Task):
    task = next((t for t in tasks if t.id == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.title = updated_task.title
    task.description = updated_task.description
    task.done = updated_task.done
    return task

# Ruta para eliminar una tarea
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    global tasks
    tasks = [t for t in tasks if t.id != task_id]
    return {"message": "Task deleted"}
