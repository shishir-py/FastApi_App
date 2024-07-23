from bson import ObjectId
from app.database_conn import get_collection
from app.models import UserModel
from typing import List
from fastapi import HTTPException


def create_user(user: UserModel) -> str:
    collection = get_collection()
    
    # Check for same email and tag them as already exists
    existing_user = collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this email already exists")
    
    user_dict = user.dict(by_alias=True, exclude={"id"})
    result = collection.insert_one(user_dict)
    return str(result.inserted_id)


def create_users(users: List[UserModel]) -> List[str]:
    collection = get_collection()
    
    # Check for same email and tag them as already exists
    email_set = set()
    for user in users:
        if user.email in email_set:
            raise HTTPException(status_code=400, detail=f"Duplicate email found: {user.email}")
        email_set.add(user.email)
    
    # Check for same email and tag them as already exists
    existing_emails = set(collection.distinct("email", {"email": {"$in": list(email_set)}}))
    if existing_emails:
        raise HTTPException(status_code=400, detail=f"Users with these emails already exist: {', '.join(existing_emails)}")
    
    user_dicts = [user.dict(by_alias=True, exclude={"id"}) for user in users]
    result = collection.insert_many(user_dicts)
    return [str(id) for id in result.inserted_ids]


def get_user(user_id: str) -> UserModel:
    collection = get_collection()
    user = collection.find_one({"_id": ObjectId(user_id)})
    if user:
        return UserModel(**user)
    return None

def update_user(user_id: str, user: UserModel) -> UserModel:
    collection = get_collection()
    
    # Check for same email and tag them as already exists
    if user.email is not None:
        existing_user = collection.find_one({"email": user.email, "_id": {"$ne": ObjectId(user_id)}})
        if existing_user:
            raise HTTPException(status_code=400, detail="Another user with this email already exists")
    
    user_dict = user.dict(by_alias=True, exclude={"id"})
    result = collection.update_one({"_id": ObjectId(user_id)}, {"$set": user_dict})
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    
    updated_user = collection.find_one({"_id": ObjectId(user_id)})
    return UserModel(**updated_user)

def delete_user(user_id: str) -> bool:
    collection = get_collection()
    result = collection.delete_one({"_id": ObjectId(user_id)})
    return result.deleted_count == 1

def list_users() -> List[UserModel]:
    collection = get_collection()
    users = collection.find()
    return [UserModel(**user) for user in users]
