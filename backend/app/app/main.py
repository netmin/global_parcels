import os

from app.api import health_check, parcel
from app.db import init_db
from fastapi import FastAPI, Request
from loguru import logger
from starlette.middleware.sessions import SessionMiddleware

from app.utils import SessionManager
from fastapi.middleware.cors import CORSMiddleware


SECRET_KEY = os.getenv("APP_SECRET_KEY", "default-secret-key")

ORIGINS = [
    "*",  # Only local development
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]


# Initialize your FastAPI app and session manager
session_manager = SessionManager(SECRET_KEY)


def create_app() -> FastAPI:
    application = FastAPI()
    application.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)
    application.include_router(health_check.router)
    application.include_router(parcel.router)

    return application


app = create_app()


app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_session_id_to_request(request: Request, call_next):
    session_id = request.cookies.get("session_id")
    if not session_id or not session_manager.validate_session_id(session_id):
        session_id = session_manager.create_session_id()
        response = await call_next(request)
        response.set_cookie(key="session_id", value=session_id, httponly=True)
        return response
    return await call_next(request)


@app.on_event("startup")
async def startup() -> None:
    logger.info("Starting up...")
    init_db(app)


@app.on_event("shutdown")
async def shutdown() -> None:
    logger.info("Shutting down...")
