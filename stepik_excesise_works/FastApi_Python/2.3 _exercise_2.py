
from fastapi import FastAPI
from pydantic import BaseModel, Field, field_validator

app = FastAPI()

md = []
FORBIDDEN_WORDS = ["редиска", "бяка", "козявка"]

class Feedback(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    message: str = Field(..., min_length=10, max_length=500)

    @field_validator("message")
    def check_forbidden_words(cls, value):
        l_msg = value.lower()
        for word in FORBIDDEN_WORDS:
            if word in l_msg:
                raise ValueError(f"Message contains forbidden word: '{word}'")
        return value

@app.post("/feedback")
def add_feedback(feedback: Feedback):
    md.append(feedback.model_dump())
    return {"message": f"thank you, {feedback.name}! Your feedback has been saved."}

@app.get("/feedbacks")
def get_all_feedbacks():
    return {"feedbacks": md}
