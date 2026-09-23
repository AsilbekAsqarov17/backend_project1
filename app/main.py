from fastapi import FastAPI
from app.routers.user import router as user_router
from app.routers.task import router as task_router

app = FastAPI()

app.include_router(user_router)
app.include_router(task_router)