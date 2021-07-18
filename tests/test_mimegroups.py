from xtractmime.mimegroups import (
    is_archive_mime_type,
    is_audio_video_mime_type,
    is_font_mime_type,
    is_html_mime_type,
    is_image_mime_type,
    is_javascript_mime_type,
    is_json_mime_type,
    is_scriptable_mime_type,
    is_xml_mime_type,
    is_zip_based_mime_type,
)


class TestMimegroups:
    def test_is_archive_mime_type(self):
        assert is_archive_mime_type(b"application/zip")
        assert not is_archive_mime_type(b"text/test")

    def test_is_audio_video_mime_type(self):
        assert is_audio_video_mime_type(b"video/mp4")
        assert not is_audio_video_mime_type(b"text/test")

    def test_is_font_mime_type(self):
        assert is_font_mime_type(b"application/font-cff")
        assert not is_font_mime_type(b"text/test")

    def test_is_html_mime_type(self):
        assert is_html_mime_type(b"text/html")
        assert not is_html_mime_type(b"text/test")

    def test_is_image_mime_type(self):
        assert is_image_mime_type(b"image/gif")
        assert not is_image_mime_type(b"text/test")

    def test_is_javascript_mime_type(self):
        assert is_javascript_mime_type(b"application/javascript")
        assert not is_javascript_mime_type(b"text/test")

    def test_is_json_mime_type(self):
        assert is_json_mime_type(b"text/json")
        assert not is_json_mime_type(b"text/test")

    def test_is_scriptable_mime_type(self):
        assert is_scriptable_mime_type(b"text/html")
        assert is_scriptable_mime_type(b"text/xml")
        assert is_scriptable_mime_type(b"application/pdf")
        assert not is_scriptable_mime_type(b"text/test")

    def test_is_xml_mime_type(self):
        assert is_xml_mime_type(b"text/xml")
        assert not is_xml_mime_type(b"text/test")

    def test_is_zip_based_mime_type(self):
        assert is_zip_based_mime_type(b"application/zip")
        assert not is_zip_based_mime_type(b"text/test")
