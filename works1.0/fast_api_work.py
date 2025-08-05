from fastapi import FastAPI

app = FastAPI()

users = [{"username": "James", "email": "james@gmail.com"},
        {"username": "John", "email": "john@gmail.com"}]

@app.get("/users")
def get_users():
    return users

@app.get("/users/username")
def get_user(username):
    for user in users:
        if user["username"] == username:
            return user
    return {"message": "User not found"}

@app.post("/users")
def add_user(username, email):
    for user in users:
        if user["email"] == email:
            return {"message": "User already exists"}
    tmp = {"username": username, "email": email}
    users.append(tmp)
    return {"message": "Added successfully"}
@app.put("/users/username")
def delete_user(email):
    for user in users:
        if user["email"] == email:
            users.remove(user)
            return {"message": "User is deleted "}
    return {"message": "Email not found in database"}
