import os

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.fastapi_reference.host.routers.person_router import person_router
from src.fastapi_reference.host.routers.todo_router import todo_router

app = FastAPI(
    title="FastAPI Reference",
    description="Clean reference architecture for FastAPI",
    version="0.1.0"
)

app.include_router(person_router)
app.include_router(todo_router)

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def start():
    uvicorn.run(
        "src.resume_ai.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        access_log=True,
        log_level="debug",
        root_path=os.environ.get("ROOT_PATH", ""),
    )


if __name__ == "__main__":
    start()