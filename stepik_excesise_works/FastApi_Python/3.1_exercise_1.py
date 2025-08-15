from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, Field
app = FastAPI()
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    age: int | None = Field(None, gt=0)  
    is_subscribed: bool | None = None
@app.post("/create_user")
async def create_user(user: UserCreate):
    return user 