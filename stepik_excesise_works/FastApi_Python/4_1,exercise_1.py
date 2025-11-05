from fastapi import FastAPI, Depends, status, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()
security = HTTPBasic()
f_db = {
    "admin": "secret123",
    "user1": "pass1"
}
def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    username = credentials.username
    password = credentials.password
    if username not in f_db or f_db[username] != password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid authentication credentials")
    return username

@app.get("/user_info")
def login(user: str = Depends(get_current_user)):
    return {"message": "You got my secret, welcome"}
