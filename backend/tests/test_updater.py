from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

from backend.services import updater as updater_module
from backend.services.updater import update_m3u, update_epg

# Tests para la función update_m3u
class TestUpdateM3U:
    @patch('backend.services.updater.fetch_file')
    @patch('backend.services.updater.parse_m3u', return_value=[{'id': 'dummy_downloaded'}])
    @patch('backend.services.updater.save_file')
    def test_successful_download(self, mock_save, *_):
        updater_module.last_update = None
        updater_module.cache.cached_m3u_data = None
        update_m3u(skip_save=True)

        mock_save.assert_not_called()
        assert updater_module.cache.cached_m3u_data == [{'id': 'dummy_downloaded'}]
        assert isinstance(updater_module.last_update, datetime)
        assert datetime.now() - updater_module.last_update < timedelta(seconds=2)

    @patch('backend.services.updater.fetch_file', return_value=None)
    def test_use_cache(self, _):
        updater_module.last_update = None
        updater_module.cache.cached_m3u_data = [{'id': 'dummy_cached'}]
        update_m3u()

        assert updater_module.cache.cached_m3u_data == [{'id': 'dummy_cached'}]
        assert updater_module.last_update is None

    @patch('backend.services.updater.fetch_file', return_value=None)
    @patch('backend.services.updater.load_file')
    @patch('backend.services.updater.parse_m3u', return_value=[{'id': 'dummy_local'}])
    def test_use_local_backup(self, *_):
        updater_module.last_update = None
        updater_module.cache.cached_m3u_data = None
        update_m3u()

        assert updater_module.cache.cached_m3u_data == [{'id': 'dummy_local'}]
        assert isinstance(updater_module.last_update, datetime)
        assert datetime.now() - updater_module.last_update < timedelta(seconds=2)
        
    @patch('backend.services.updater.fetch_file', return_value=None)
    @patch('backend.services.updater.load_file', return_value=None)
    @patch('backend.services.updater.parse_m3u')
    def test_fail(self, mock_parse, *_):
        updater_module.last_update = None
        updater_module.cache.cached_m3u_data = None
        update_m3u()

        mock_parse.assert_not_called()
        assert updater_module.cache.cached_m3u_data is None
        assert updater_module.last_update is None


# Tests para la función update_epg
class TestUpdateEPG:
    @patch('backend.services.updater.fetch_file')
    @patch('backend.services.updater.save_file')
    @patch('backend.services.updater.parse_epg', return_value={'test_channel': 'test_channel_program'})
    def test_successful_download(self, mock_save, *_):
        updater_module.retry_count = 2
        updater_module.cache.cached_m3u_data = [{'id': 'test_channel'}]
        updater_module.cache.cached_epg_data = None
        scheduler = MagicMock()
        update_epg(scheduler)

        mock_save.assert_called_once()
        scheduler.add_job.assert_not_called()
        assert updater_module.cache.cached_epg_data == {'test_channel': 'test_channel_program'}
        assert updater_module.retry_count == 0

    @patch('backend.services.updater.fetch_file', return_value=None)
    def test_use_cache(self, _):
        updater_module.retry_count = 0
        updater_module.cache.cached_epg_data = {'test_channel': 'test_channel_program'}
        scheduler = MagicMock()
        update_epg(scheduler)

        assert updater_module.cache.cached_epg_data == {'test_channel': 'test_channel_program'}
        assert updater_module.retry_count == 1
        scheduler.add_job.assert_called_once()

    @patch('backend.services.updater.fetch_file', return_value=None)
    def test_max_retries(self, _):
        updater_module.retry_count = updater_module.config.EPG_MAX_RETRIES
        updater_module.cache.cached_epg_data = {'test_channel': 'test_channel_program'}
        scheduler = MagicMock()
        update_epg(scheduler)

        assert updater_module.cache.cached_epg_data == {'test_channel': 'test_channel_program'}
        scheduler.add_job.assert_not_called()

    @patch('backend.services.updater.fetch_file', return_value=None)
    @patch('backend.services.updater.load_file')
    @patch('backend.services.updater.parse_epg', return_value={'test_channel': 'test_channel_program'})
    def test_use_local_backup(self, *_):
        updater_module.retry_count = 0
        updater_module.cache.cached_m3u_data = [{'id': 'test_channel'}]
        updater_module.cache.cached_epg_data = None
        scheduler = MagicMock()
        update_epg(scheduler)

        assert updater_module.cache.cached_epg_data == {'test_channel': 'test_channel_program'}

    @patch('backend.services.updater.fetch_file', return_value=None)
    @patch('backend.services.updater.load_file', return_value=None)
    @patch('backend.services.updater.parse_epg')
    def test_fail(self, mock_parse, *_):
        updater_module.retry_count = 0
        updater_module.cache.cached_epg_data = None
        scheduler = MagicMock()
        update_epg(scheduler)

        mock_parse.assert_not_called()
        assert updater_module.cache.cached_epg_data is None

    @patch('backend.services.updater.fetch_file')
    @patch('backend.services.updater.save_file')
    @patch('backend.services.updater.parse_epg')
    @patch('backend.services.updater.update_m3u')
    def test_first_run(self, mock_m3u, *_):
        scheduler = MagicMock()
        update_epg(scheduler, first_run=True)

        mock_m3u.assert_called_once()