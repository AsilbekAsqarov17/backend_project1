from app.database import get_db
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException,status, Path

from app.models.user import user_define, column_update

from app.services.user import (
    user_create,
    get_users,
    get_user_by_id,
    user_replace,
    user_update,
    user_delete
)

router = APIRouter()

UserID = Annotated[int, Path(gt=0, title = "User ID", example=21)]

#Create user route function 
@router.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(user:user_define, db = Depends(get_db)):
    result = user_create(user, db)
    return {"message": result}

#Get all users route function
@router.get("/users", status_code=status.HTTP_200_OK)
def get_all_users(db = Depends(get_db)):
    users = get_users(db)
    return {"message":users}

#Get one user route function
@router.get("/users/{user_id}", status_code=status.HTTP_200_OK)
def get_user(user_id:UserID, db = Depends(get_db)):
    user = get_user_by_id(user_id,db)
    if not user:
        raise HTTPException(status_code=404,detail="User not found")
    return {"message": user}

#Put/Replace user route function
@router.put("/users/{user_id}",status_code=status.HTTP_200_OK)
def replace_user(user:user_define, user_id:UserID, db = Depends(get_db)):
    row_affected = user_replace(user, user_id, db)
    if not row_affected:
        raise HTTPException(
            status_code=404,
            detail=f"User with id {user_id} doesn't exist or update failed"
        )
    return {"message":f"User {user_id} updated successfully"}


#Patch/Update user route function
@router.patch("/users/{user_id}",status_code=status.HTTP_200_OK)
def update_user(user_id:UserID, column:column_update, db = Depends(get_db)):
    rows_affected = user_update(user_id, column.column_name, column.value, db)
    if not rows_affected:
        raise HTTPException(
            status_code=404,
            detail=f"User with id {user_id} doesn't exist or update failed"
        )
    return {"message":f"User {user_id} updated successfully"}


#Delete user route function
@router.delete("/users/{user_id}", status_code=status.HTTP_200_OK)
def delete_user(user_id:UserID, db = Depends(get_db)):
    rows_affected = user_delete(user_id, db)
    if not rows_affected:
        raise HTTPException(
            status_code=404,
            detail=f"User with id {user_id} doesn't exist"
        )
    return {"message":f"User {user_id} deleted successfully"}