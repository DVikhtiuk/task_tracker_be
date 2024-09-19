import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.settings import settings
from app.routers.auth_routers import router as auth_router
from app.routers.healthcheck_routers import router as healthcheck_router
from app.routers.task_routers import router as task_router

app = FastAPI(
    title="Task Tracker Back-End",
    description="""
    Task Tracker Back-End - Test task
    """,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(healthcheck_router)
app.include_router(auth_router)
app.include_router(task_router)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host=settings.APP_HOST, port=settings.APP_PORT, reload=True)
