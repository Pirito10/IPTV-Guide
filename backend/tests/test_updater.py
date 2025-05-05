from datetime import datetime, timedelta
from unittest.mock import patch

from backend.services import updater as updater_module

# Tests para la función update_m3u
class TestUpdateM3U:
    @patch('backend.services.updater.fetch_file')
    @patch('backend.services.updater.parse_m3u', return_value=[{'id': 'dummy_downloaded'}])
    def test_success(self, *_):
        updater_module.last_update = None
        updater_module.cache.cached_m3u_data = None
        updater_module.update_m3u(skip_save=True)

        assert updater_module.cache.cached_m3u_data == [{'id': 'dummy_downloaded'}]
        assert isinstance(updater_module.last_update, datetime)
        assert datetime.now() - updater_module.last_update < timedelta(seconds=2)

    @patch('backend.services.updater.fetch_file', return_value=None)
    def test_use_cache(self, _):
        updater_module.last_update = None
        updater_module.cache.cached_m3u_data = [{'id': 'dummy_cached'}]
        updater_module.update_m3u()

        assert updater_module.cache.cached_m3u_data == [{'id': 'dummy_cached'}]
        assert updater_module.last_update is None

    @patch('backend.services.updater.fetch_file', return_value=None)
    @patch('backend.services.updater.load_file')
    @patch('backend.services.updater.parse_m3u', return_value=[{'id': 'dummy_local'}])
    def test_use_local_backup(self, *_):
        updater_module.last_update = None
        updater_module.cache.cached_m3u_data = None
        updater_module.update_m3u()

        assert updater_module.cache.cached_m3u_data == [{'id': 'dummy_local'}]
        assert isinstance(updater_module.last_update, datetime)
        assert datetime.now() - updater_module.last_update < timedelta(seconds=2)
        
    @patch('backend.services.updater.fetch_file', return_value=None)
    @patch('backend.services.updater.load_file', return_value=None)
    @patch('backend.services.updater.parse_m3u')
    def test_fail(self, *_):
        updater_module.last_update = None
        updater_module.cache.cached_m3u_data = None
        updater_module.update_m3u()

        assert updater_module.cache.cached_m3u_data is None
        assert updater_module.last_update is None