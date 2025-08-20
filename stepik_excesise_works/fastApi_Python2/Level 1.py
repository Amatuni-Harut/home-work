from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class todos(BaseModel):
    title: str
    description: str
    completed: bool

f_db = []

@app.post("/todos")
def create_todo(todo: todos):
    todo_id = len(f_db) + 1
    todo_data = {"id": todo_id, **todo.dict()}
    f_db.append(todo_data)
    return todo_data
@app.get("/todo")
def get_todos_list():
    return f_db

@app.get("/todos")
def gettodos(q: str = None, completed: bool = None):
    result = f_db  

    if q is not None:
        result = [el for el in result if q.lower() in el["title"].lower()]

    if completed is True:
        result = [el for el in result if el["completed"] is True]
    elif completed is False:
        result = [el for el in result if el["completed"] is False]

    return result
