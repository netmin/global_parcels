import asyncio
import os

import pytest
from app.config import get_settings, Settings
from app.main import create_app
from asgi_lifespan import LifespanManager
from httpx import AsyncClient
from starlette.testclient import TestClient
from tortoise.contrib.fastapi import register_tortoise

TORTOISE_ORM = {
    "connections": {"default": os.getenv("DATABASE_TEST_URL")},
    "apps": {
        "models": {
            "models": ["app.models.tortoise"],
            "default_connection": "default",
        },
    },
}


def get_settings_override():
    return Settings(testing=1, database_url=os.getenv("DATABASE_TEST_URL"))


@pytest.fixture(scope="module")
def test_app():
    app = create_app()
    app.dependency_overrides[get_settings] = get_settings_override
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="module")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="module")
async def client():
    app = create_app()
    app.dependency_overrides[get_settings] = get_settings_override

    register_tortoise(
        app,
        config=TORTOISE_ORM,
        generate_schemas=True,
        add_exception_handlers=True,
    )

    async with LifespanManager(app):
        async with AsyncClient(app=app, base_url="http://test") as c:
            yield c


@pytest.fixture(scope="session", autouse=True)
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
