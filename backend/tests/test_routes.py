import pytest
from unittest.mock import patch

from backend.app import app
from backend import routes as routes_module

@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client

@patch('backend.routes.update_m3u')
def test_channels_no_data(_, client):
    routes_module.cache.cached_m3u_data = None
    response = client.get('/api/channels')

    assert response.status_code == 500
    assert response.json == {"error": "No channels available"}

@patch('backend.routes.update_m3u')
def test_channels_success(_, client):
    routes_module.cache.cached_m3u_data = [{'id': 'test_channel', 'name': 'Test Channel'}]
    response = client.get('/api/channels')

    assert response.status_code == 200
    assert response.json == [{'id': 'test_channel', 'name': 'Test Channel'}]

def test_epg_no_data(client):
    routes_module.cache.cached_epg_data = None
    response = client.get('/api/epg')

    assert response.status_code == 500
    assert response.json == {"error": "No EPG available"}

def test_epg_success(client):
    routes_module.cache.cached_epg_data = [{
            "title": "Program Title",
            "description": "Program description",
            "since": "Start Time",
            "till": "Stop Time",
        }]
    response = client.get('/api/epg')

    assert response.status_code == 200
    assert response.json == [{
            "title": "Program Title",
            "description": "Program description",
            "since": "Start Time",
            "till": "Stop Time",
        }]
