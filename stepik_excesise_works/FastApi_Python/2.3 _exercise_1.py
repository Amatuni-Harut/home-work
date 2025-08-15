from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()
md = []
class Feedback(BaseModel):
    name: str
    message: str
@app.post("/feedback")
def receive_feedback(feedback: Feedback):
    md.append(feedback.dict())
    return {"message": f"Feedback received. Thank you, {feedback.name}."}

@app.get("/feedback")
def get_all_feedback():
    return md