from unittest.mock import patch

from backend.config import config
from backend.services.parsers import parse_m3u, parse_epg

# Tests para la función parse_m3u
class TestParseM3U:
    def test_parse_m3u_single_channel(self):
        m3u_content = '''
#EXTINF:-1 tvg-logo="http://test_logo.png" tvg-id="test_id"  group-title="Test Group", Test Channel
acestream://test-url
'''
        
        result = parse_m3u(m3u_content, True)
        assert len(result) == 1

        channel = result[0]
        assert channel["id"] == "test_id"
        assert channel["logo"] == "http://test_logo.png"
        assert channel["group"] == "Test Group"
        assert channel["streams"] == [{"name": "Test Channel", "url": "test-url"}]

    def test_parse_m3u_channel_without_id(self):
        m3u_content = '''
#EXTINF:-1 tvg-logo="http://test_logo.png" tvg-id=""  group-title="Test Group", Test Channel
acestream://test-url
'''
        
        result = parse_m3u(m3u_content, True)
        assert len(result) == 1
        
        channel = result[0]
        assert channel["id"] == f"{config.DEFAULT_ID}#1"
        assert channel["logo"] == "http://test_logo.png"
        assert channel["group"] == "Test Group"
        assert channel["streams"] == [{"name": "Test Channel", "url": "test-url"}]

    @patch('backend.services.parsers.get_valid_logo', return_value="http://valid_logo.png")
    def test_parse_m3u_calls_get_valid_logo(self, _):
        m3u_content = '''
#EXTINF:-1 tvg-logo="http://original_logo.png" tvg-id="test_id"  group-title="Test Group", Test Channel
acestream://test-url
'''

        result = parse_m3u(m3u_content, False)
        assert len(result) == 1

        channel = result[0]
        assert channel["logo"] == "http://valid_logo.png"

    def test_parse_m3u_duplicate_ids(self):
        m3u_content = '''
#EXTINF:-1 tvg-logo="http://test_logo.png" tvg-id="test_id"  group-title="Test Group", Test Channel 1
acestream://test-url-1
#EXTINF:-1 tvg-logo="http://test_logo.png" tvg-id="test_id"  group-title="Test Group", Test Channel 2
acestream://test-url-2
'''
        
        result = parse_m3u(m3u_content, True)
        assert len(result) == 1

        channel = result[0]
        assert channel["id"] == "test_id"
        assert channel["logo"] == "http://test_logo.png"
        assert channel["group"] == "Test Group"
        assert len(channel["streams"]) == 2

        stream_names = {s["name"] for s in channel["streams"]}
        stream_urls = {s["url"] for s in channel["streams"]}
        assert stream_names == {"Test Channel 1", "Test Channel 2"}
        assert stream_urls == {"test-url-1", "test-url-2"}


# Tests para la función parse_epg
class TestParseEPG:
    @patch('backend.services.parsers.convert_epg_time', return_value="dummy_time")
    def test_parse_epg_valid_program(self, _):
        xml_content = '''
<tv>
  <channel id="test_channel">
    <icon src="http://test_channel_logo.png"/>
  </channel>
  <programme start="20250501120000 +0200" stop="20250501130000 +0200" channel="test_channel">
    <title>Program Title</title>
    <desc>Program description</desc>
  </programme>
</tv>
'''
        
        result = parse_epg(xml_content, ["test_channel"])
        assert "test_channel" in result
        assert result["test_channel"]["programs"][0] == {
            "title": "Program Title",
            "description": "Program description",
            "since": "dummy_time",
            "till": "dummy_time"
        }
        assert result["test_channel"]["logo"] == "http://test_channel_logo.png"

    @patch('backend.services.parsers.convert_epg_time', return_value="dummy_time")
    def test_parse_epg_ignores_programs_not_in_channel_ids(self, _):
        xml_content = '''
<tv>
  <channel id="channel_not_in_list">
    <icon src="http://test_channel_logo.png"/>
  </channel>
  <programme start="20250501120000 +0200" stop="20250501130000 +0200" channel="channel_not_in_list">
    <title>Hidden Program</title>
    <desc>Should be ignored</desc>
  </programme>
</tv>
'''
        
        assert parse_epg(xml_content, ["other_channel"]) == {}

    @patch('backend.services.parsers.convert_epg_time', return_value=None)
    def test_parse_epg_ignores_program_with_invalid_time(self, _):
        xml_content = '''
<tv>
  <channel id="test_channel">
    <icon src="http://test_channel_logo.png"/>
  </channel>
  <programme start="invalid" stop="invalid" channel="test_channel">
    <title>Invalid Program</title>
    <desc>Should be ignored</desc>
  </programme>
</tv>
'''
        
        assert parse_epg(xml_content, ["test_channel"]) == {}

    @patch('backend.services.parsers.convert_epg_time', return_value="dummy_time")
    def test_parse_epg_channel_with_icon(self, _):
        xml_content = '''
<tv>
  <channel id="test_channel">
    <icon src="http://test_channel_logo.png"/>
  </channel>
  <programme start="20250501120000 +0200" stop="20250501130000 +0200" channel="test_channel">
    <title>Program Title</title>
    <desc>Program description</desc>
  </programme>
</tv>
'''
        
        result = parse_epg(xml_content, ["test_channel"])
        assert "test_channel" in result
        assert result["test_channel"]["logo"] == "http://test_channel_logo.png"

    @patch('backend.services.parsers.convert_epg_time', return_value="dummy_time")
    def test_parse_epg_channel_without_icon(self, _):
        xml_content = '''
<tv>
<channel id="test_channel"></channel>
<programme start="20250501120000 +0200" stop="20250501130000 +0200" channel="test_channel">
    <title>Program Title</title>
    <desc>Program description</desc>
</programme>
</tv>
'''

        result = parse_epg(xml_content, ["test_channel"])
        assert "test_channel" in result
        assert "logo" not in result["test_channel"]