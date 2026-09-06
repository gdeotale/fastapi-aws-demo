from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


# =========================================================
# DATA MODEL
# =========================================================

class User(BaseModel):
    name: str
    age: int
    city: str


# Fake database
users = {
    1: {
        "name": "Gunjan",
        "age": 38,
        "city": "Mumbai"
    },
    2: {
        "name": "Rahul",
        "age": 30,
        "city": "Pune"
    }
}


# =========================================================
# GET
# =========================================================

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}


# Get ALL users
@app.get("/users")
def get_users():
    return users


# Get ONE user
@app.get("/users/{user_id}")
def get_user(user_id: int):

    if user_id not in users:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return users[user_id]


# =========================================================
# POST
# =========================================================

# Create a NEW user
@app.post("/users")
def create_user(user: User):

    new_id = max(users.keys()) + 1

    users[new_id] = user.model_dump()

    return {
        "message": "User created successfully",
        "user_id": new_id,
        "user": users[new_id]
    }


# Your original example
@app.post("/greet")
def greet_user(name: str):
    return {
        "message": f"Hello, {name}!"
    }


# =========================================================
# PUT
# =========================================================

# Replace the ENTIRE user
@app.put("/users/{user_id}")
def replace_user(user_id: int, user: User):

    if user_id not in users:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    users[user_id] = user.model_dump()

    return {
        "message": "User replaced successfully",
        "user_id": user_id,
        "user": users[user_id]
    }


# =========================================================
# PATCH
# =========================================================

class UserUpdate(BaseModel):
    name: str | None = None
    age: int | None = None
    city: str | None = None


# Update ONLY the fields provided
@app.patch("/users/{user_id}")
def update_user(user_id: int, user: UserUpdate):

    if user_id not in users:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    update_data = user.model_dump(exclude_unset=True)

    users[user_id].update(update_data)

    return {
        "message": "User updated successfully",
        "user_id": user_id,
        "user": users[user_id]
    }


# =========================================================
# DELETE
# =========================================================

@app.delete("/users/{user_id}")
def delete_user(user_id: int):

    if user_id not in users:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    deleted_user = users.pop(user_id)

    return {
        "message": "User deleted successfully",
        "user_id": user_id,
        "user": deleted_user
    }