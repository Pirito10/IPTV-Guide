import pytest
import requests
from unittest.mock import patch
from datetime import datetime, timedelta

from backend.config import cache
from backend.services.utils import fetch_file, convert_epg_time, is_url_accessible, get_valid_logo

# Tests para la función fetch_file
class TestFetchFile:
    @pytest.mark.parametrize("side_effect, expected", [
        (None, "test content"),
        (requests.exceptions.Timeout, None),
        (requests.exceptions.HTTPError, None),
        (requests.exceptions.ConnectionError, None),
        (requests.exceptions.RequestException, None)
    ])
    @patch('backend.services.utils.requests.get')
    def test_fetch(self, mock_get, side_effect, expected):
        url = "http://example.com/test.txt"

        if side_effect is None:
            mock_response = mock_get.return_value
            mock_response.raise_for_status.return_value = None
            mock_response.text = "test content"
        elif side_effect == requests.exceptions.HTTPError:
            mock_response = mock_get.return_value
            mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(response=mock_response)
        else:
            mock_get.side_effect = side_effect
        
        assert fetch_file(url) == expected


# Tests para la función convert_epg_time
class TestConvertEpgTime:
    def test_valid(self):
        input_time = "20250427180000 +0200"
        expected_iso = "2025-04-27T16:00:00Z"

        assert convert_epg_time(input_time) == expected_iso

    def test_invalid(self):
        input_time = "invalid_string"

        assert convert_epg_time(input_time) is None


# Tests para la función get_valid_logo
class TestGetValidLogo:
    @patch('backend.services.utils.is_url_accessible', return_value=True)
    def test_direct_ok(self, _):
        channel_id = "channel1"
        logo_url = "http://example.com/logo.png"

        assert get_valid_logo(channel_id, logo_url) == logo_url

    @patch('backend.services.utils.is_url_accessible', side_effect=[False, True])
    def test_fallback_epg(self, _, monkeypatch):
        channel_id = "channel1"
        logo_url = "http://example.com/bad_logo.png"
        epg_logo_url = "http://example.com/epg_logo.png"
        monkeypatch.setitem(cache.cached_epg_data, channel_id, {"logo": epg_logo_url})

        assert get_valid_logo(channel_id, logo_url) == epg_logo_url


    @patch('backend.services.utils.is_url_accessible', side_effect=[False, False])
    def test_none(self, _, monkeypatch):
        channel_id = "channel1"
        logo_url = "http://example.com/bad_logo.png"
        monkeypatch.setitem(cache.cached_epg_data, channel_id, {})

        assert get_valid_logo(channel_id, logo_url) is None

# Tests para la función is_url_accessible
class TestIsUrlAccessible:
    @patch('backend.services.utils.requests.head')
    def test_status_ok(self, mock_head):
        url = "http://example.com/logo.png"
        mock_head.return_value.status_code = 200

        assert is_url_accessible(url) is True

    @patch('backend.services.utils.requests.head')
    def test_status_forbidden(self, mock_head):
        url = "http://example.com/logo.png"
        mock_head.return_value.status_code = 403

        assert is_url_accessible(url) is True

    @patch('backend.services.utils.requests.head', side_effect=requests.exceptions.SSLError)
    def test_ssl_error(self, _):
        url = "http://example.com/bad_ssl.png"

        assert is_url_accessible(url) is True

    @patch('backend.services.utils.requests.head', side_effect=requests.exceptions.RequestException)
    def test_exception(self, _):
        url = "http://example.com/error.png"

        assert is_url_accessible(url) is False

    def test_cached_valid(self, monkeypatch):
        url = "http://example.com/logo.png"
        expiry_time = datetime.now() + timedelta(minutes=5)
        monkeypatch.setitem(cache.cached_logos, url, (expiry_time, True))

        assert is_url_accessible(url) is True

    def test_cached_invalid(self, monkeypatch):
        url = "http://example.com/logo.png"
        expiry_time = datetime.now() + timedelta(minutes=5)
        monkeypatch.setitem(cache.cached_logos, url, (expiry_time, False))

        assert is_url_accessible(url) is False

    @patch('backend.services.utils.requests.head')
    def test_expired_cache(self, mock_head, monkeypatch):
        url = "http://example.com/logo.png"
        mock_head.return_value.status_code = 200
        expiry_time = datetime.now() - timedelta(minutes=5)
        monkeypatch.setitem(cache.cached_logos, url, (expiry_time, True))

        assert is_url_accessible(url) is True