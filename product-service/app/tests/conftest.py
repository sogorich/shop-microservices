import pytest

from httpx import AsyncClient, ASGITransport
from main import app


@pytest.fixture
def async_client() -> AsyncClient:
    return AsyncClient(transport=ASGITransport(app=app), base_url="http://")