import pytest
from fastapi.testclient import TestClient

from app.data.order_store import order_store
from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_orders():
    """Each test starts from the sample orders, whatever the previous test changed."""
    order_store.reset()
    yield
    order_store.reset()
