
from fastapi import FastAPI
from pydantic import BaseModel, Field, EmailStr, validator

app = FastAPI()
md = []
FORBIDDEN_WORDS = ["редиска", "бяка", "козявка"]

class Contact(BaseModel):
    email: EmailStr
    phone: str | None = None

    @validator("phone")
    def validate_phone(cls, value):
        if value is not None:
            if not value.isdigit() or not (7 <= len(value) <= 15):
                raise ValueError("number your phone  not (7–15 ) degist")
        return value

class Feedback(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    message: str = Field(..., min_length=10, max_length=500)
    contact: Contact

    @validator("message")
    def check_forbidden_words(cls, value):
        l_msg = value.lower()
        for word in FORBIDDEN_WORDS:
            if word in l_msg:
                raise ValueError(f"the message contains forbidden word: '{word}'")
        return value

@app.post("/feedback")
def receive_feedback(feedback: Feedback, is_premium="false"):
    premium_flag = str(is_premium).lower() in ["true", "1", "yes"]
    md.append(feedback.dict())
    message = f"Thank you, {feedback.name}! Your feedback has been saved."
    if premium_flag:
        message += " Your feedback will be reviewed on a priority basis."
    return {"message": message}

@app.get("/feedback")
def get_all_feedback():
    return {"feedback": md}
