import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.settings import settings

app = FastAPI(
    title="Task Tracker Back-End",
    description="""
    Task Tracker Back-End - Test task
    """,)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["healthcheck"])
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app", host=settings.APP_HOST, port=settings.APP_PORT, reload=True
    )
