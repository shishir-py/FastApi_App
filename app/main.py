from fastapi import FastAPI, HTTPException
from app.models import UserModel
from app.crud import create_user,create_users, get_user, update_user, delete_user, list_users
from app.database_conn import db
from typing import List


app = FastAPI()

@app.on_event("startup")
def startup_db_client():
    db.connect()

@app.on_event("shutdown")
def shutdown_db_client():
    db.close()




@app.post("/users/", response_model=str)
def create_user_route(user: UserModel):
    return create_user(user)

@app.post("/users/batch/", response_model=List[str])
def create_users_route(users: List[UserModel]):
    return create_users(users)

@app.get("/users/{user_id}", response_model=UserModel)
def get_user_route(user_id: str):
    user = get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{user_id}", response_model=UserModel)
def update_user_route(user_id: str, user: UserModel):
    updated_user = update_user(user_id, user)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@app.delete("/users/{user_id}", response_model=bool)
def delete_user_route(user_id: str):
    deleted = delete_user(user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return True

@app.get("/users/", response_model=list[UserModel])
def list_users_route():
    return list_users()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
