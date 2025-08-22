#kody eror kuda chdem inchce 
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

class todos(BaseModel):
    title: str
    description: str
    completed: bool
    due_date: datetime | None = None

f_db = []

@app.post("/todos")
def create_todo(todo: todos):
    for el in f_db:
        if el["title"] == todo.title:
            return {"msg": "use another title"}
    if todo.due_date is not None and todo.due_date < datetime.now():
        return {"msg": "error"}

    todo_id = len(f_db) + 1
    todo_data = {"id": todo_id, **todo.dict()}
    f_db.append(todo_data)
    return todo_data

@app.get("/todos")
def get_todos_list(skip: int = 0, limit: int = 10, sort_by: str = "id"):
    if sort_by == "title":
        todos_sorted = sorted(f_db, key=lambda x: x["title"].lower())
    elif sort_by == "due_date":
        todos_sorted = sorted(f_db, key=lambda x: x["due_date"] or datetime.max)
    else:
        todos_sorted = sorted(f_db, key=lambda x: x["id"])

    return todos_sorted[skip: skip + limit]

@app.get("/todos/overdue")
def get_overdue_todos():
    today = datetime.now()
    overdue = [el for el in f_db if el["due_date"] and el["due_date"] < today and not el["completed"]]
    return {"overdue_todos": overdue}
