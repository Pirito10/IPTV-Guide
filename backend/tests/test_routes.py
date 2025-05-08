import pytest
from unittest.mock import patch

from backend.app import app
from backend.routes import routes as routes_module

@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client

@patch('backend.routes.update_m3u')
def test_channels_no_data(_, client):
    routes_module.cached_m3u_data = None
    response = client.get('/api/channels')

    assert response.status_code == 500
    assert response.json == {"error": "No channels available"}