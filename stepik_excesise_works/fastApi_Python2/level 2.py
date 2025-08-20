from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class todos(BaseModel):
    title: str
    description: str
    completed: bool
class Description(BaseModel):
    description: str


f_db = []

@app.post("/todos")
def create_todo(todo: todos):
    todo_id = len(f_db) + 1
    todo_data = {"id": todo_id, **todo.dict()}
    f_db.append(todo_data)
    return todo_data
@app.get("/todo")
def get_todos():
    return f_db
@app.put("/todos/{todo_id}/complete")
def  complete_todo(todo_id: int):
    for el in f_db:
        if el["id"]==todo_id:
            el["completed"]=True
            return el, {"msg": "todo is completed"}
    return{"error": "todo not found"}
@app.patch("/todos/{todo_id}/description")
def update_description(todo_id: int , des:Description):
    for el in f_db:
        if el["id"]==todo_id:
            el["description"]=des.description
            return el
    return {"error": "todo not found"}
