from pydantic import BaseModel, Field
from typing import Literal, Any, Optional

class task_define(BaseModel):
    title : str = Field(min_length=3, max_length=100)
    description :str = Field(min_length=1, max_length=1000)
    completed : bool
    priority : int|None = Field(default=None, ge=1,le=5)
    user_id : int = Field(gt=0)

class column_update(BaseModel):
    column_name : Literal["title", "description", "completed", "priority","user_id"]
    value : Any

class TaskFilterParams(BaseModel):
    completed: Optional[bool] = None
    priority: Optional[int] = Field(None, ge=1, le=5)
    user_id: Optional[int] = None
    skip: int = Field(0, ge=0)
    limit: int = Field(10, ge=1, le=100)
    sort_by: Optional[Literal["id", "title", "completed", "priority", "user_id"]] = "id"
    order: Literal["asc", "desc"] = "asc"
