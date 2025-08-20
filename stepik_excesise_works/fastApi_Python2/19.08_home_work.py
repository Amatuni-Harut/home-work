from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
f_db = [] 

class Todos(BaseModel):
    title: str
    description: str
    completed: bool

@app.post("/todos")
def create_todo(todo: Todos):
    todo_id = len(f_db) + 1
    todo_data = {"id": todo_id, **todo.dict()}
    f_db.append(todo_data)
    return todo_data

@app.get("/todos")
def get_todos(skip: int = 0, limit: int = 10):
    return {
        "total": len(f_db),
        "skip": skip,
        "limit": limit,
        "items": f_db[skip: skip + limit]
    }

@app.get("/todos/{todo_id}")
def get_todo_id(todo_id: int):
    for el in f_db:
        if el["id"] == todo_id:
            return el
    return {"error": "todo not found"}

@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, todo: Todos):
    for el in f_db:
        if el["id"] == todo_id:
            el.update(todo.dict())
            return {"msg": "id is updated"}
    return {"error": "todo not found"}

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    for el in f_db:
        if el["id"] == todo_id:
            f_db.remove(el)
            return {"msg": "todo deleted"}
    return {"error": "todo id not found"}
