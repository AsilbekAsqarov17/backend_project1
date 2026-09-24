from app.database import get_db

from fastapi import APIRouter, Depends, HTTPException,status

from app.models.task import task_define, column_update, TaskFilterParams

from app.services.task import (
    task_create,
    get_tasks,
    task_get_by_id,
    task_replace,
    task_update,
    task_delete,
    task_get_by_userid,
    check_user_exists
)

router = APIRouter()

@router.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(task:task_define, db = Depends(get_db)):
    result = task_create(task, db)
    return {"message":result}

@router.get("/tasks", status_code=status.HTTP_200_OK)
def get_all_tasks(filters:TaskFilterParams = Depends(),db=Depends(get_db)):
    tasks, total_count = get_tasks(filters,db)
    return {
        "total": total_count,
        "count": len(tasks),
        "skip": filters.skip,
        "limit": filters.limit,
        "tasks": tasks
    }

@router.get("/tasks/{task_id}", status_code=status.HTTP_200_OK)
def get_task(task_id:int, db=Depends(get_db)):
    result = task_get_by_id(task_id,db)

    if not result:
        raise HTTPException(
            status_code=404,
            detail=f"Task with id {task_id} does not exist"
        )

    return {"message":result}

@router.get("/tasks/user/{user_id}", status_code=status.HTTP_200_OK)
def get_task_userid(user_id:int, db = Depends(get_db)):

    if not check_user_exists(user_id, db):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} does not exist"
        )

    task = task_get_by_userid(user_id,db)

    return {"message": task}

@router.put("/tasks/{task_id}", status_code=status.HTTP_200_OK)
def replace_task(task_id:int,task:task_define ,db = Depends(get_db)):
    row_affected = task_replace(task_id, task, db)
    if not row_affected:
        raise HTTPException(
            status_code=404,
            detail=f"Task with id {task_id} doesn't exist or update failed"
        )
    return {"message":f"Task {task_id} updated successfully"} 

#Patch/Update user route function
@router.patch("/tasks/{task_id}", status_code=status.HTTP_200_OK)
def update_task(task_id:int, column:column_update, db = Depends(get_db)):
    rows_affected = task_update(task_id, column.column_name, column.value, db)
    if not rows_affected:
        raise HTTPException(
            status_code=404,
            detail=f"Task with id {task_id} doesn't exist or update failed"
        )
    return {"message":f"Task {task_id} updated successfully"}

#Delete user route function
@router.delete("/tasks/{task_id}", status_code=status.HTTP_200_OK)
def delete_task(task_id:int, db = Depends(get_db)):
    rows_affected = task_delete(task_id, db)
    if not rows_affected:
        raise HTTPException(
            status_code=404,
            detail=f"Task with id {task_id} doesn't exist"
        )
    return {"message":f"Task {task_id} deleted successfully"}
