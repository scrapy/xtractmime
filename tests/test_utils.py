import pytest

from unittest import mock

from xtractmime._utils import (
    get_archive_mime,
    get_audio_video_mime,
    get_extra_mime,
    get_font_mime,
    get_image_mime,
    get_text_mime,
    is_mp3_non_ID3_signature,
    is_mp4_signature,
    is_webm_signature,
    match_mp3_header,
    mp3_framesize,
    parse_mp3_frame,
    parse_vint_number_size,
)


class TestUtils:

    with open("tests/files/foo.webm", "rb") as fp:
        body_webm = fp.read()

    with open("tests/files/foo.ttf", "rb") as fp:
        body_ttf = fp.read()

    with open("tests/files/foo.zip", "rb") as fp:
        body_zip = fp.read()

    with open("tests/files/foo.gif", "rb") as fp:
        body_gif = fp.read()

    @pytest.mark.parametrize(
        "input_bytes,expected",
        [
            ("foo.mp4", True),
            (b"\x00\x00\x00", False),
            (b"\x00\x00\x00 ftypmp4", False),
            (b"\x00\x00\x00 ftypmp42", False),
            (b"\x00\x00\x00 testmp42\x00\x00\x00\x00mp42mp41isomavc1", False),
            (b"\x00\x00\x00 ftyp2222\x00\x00\x00\x002222mp41isomavc1", True),
            (b"\x00\x00\x00 ftyp2222\x00\x00\x00\x0022222221isomavc1", False),
        ],
    )
    def test_is_mp4_signature(self, input_bytes, expected):
        if isinstance(input_bytes, str):
            with open(f"tests/files/{input_bytes}", "rb") as input_file:
                input_bytes = input_file.read()
        assert is_mp4_signature(input_bytes) == expected

    @pytest.mark.parametrize(
        "input_bytes,expected",
        [
            ("foo.webm", True),
            (b"\x00\x00\x00", False),
            (b"\x1aF\xdf\xa3", False),
            (b"\x1aE\xdf\xa3B\x82", False),
            (b"\x1aE\xdf\xa3B\x82\x00\x00\x00", False),
        ],
    )
    def test_is_webm_signature(self, input_bytes, expected):
        if isinstance(input_bytes, str):
            with open(f"tests/files/{input_bytes}", "rb") as input_file:
                input_bytes = input_file.read()
        assert is_webm_signature(input_bytes) == expected

    def test_parse_vint_number_size(self):
        assert parse_vint_number_size(memoryview(self.body_webm)[6:]) == 8
        assert parse_vint_number_size(memoryview(self.body_webm)[30:]) == 1

    @pytest.mark.parametrize(
        "framesize,input_bytes,expected",
        [
            (417, "NonID3.mp3", True),
            (417, b"\x00\x00\x00", False),
            (417, b"\xff\xfb\x90d\x00", False),
            (10, "NonID3.mp3", False),
        ],
    )
    @mock.patch("xtractmime._utils.mp3_framesize")
    def test_is_mp3_non_ID3_signature(self, mock_framesize, framesize, input_bytes, expected):
        if isinstance(input_bytes, str):
            with open(f"tests/files/{input_bytes}", "rb") as input_file:
                input_bytes = input_file.read()
        mock_framesize.return_value = framesize
        assert is_mp3_non_ID3_signature(input_bytes) == expected

    @pytest.mark.parametrize(
        "input_bytes,index,expected",
        [
            ("NonID3.mp3", 0, True),
            (b"\x00\x00\x00", 0, False),
            (b"\x00\x00\x00\x00", 0, False),
            (b"\xff\xe0\x00\x00", 0, False),
            (b"\xff\xe7\xf0\x00", 0, False),
            (b"\xff\xe7\x0c\x00", 0, False),
            (b"\xff\xe7\x00\x00", 0, False),
        ],
    )
    def test_match_mp3_header(self, input_bytes, index, expected):
        if isinstance(input_bytes, str):
            with open(f"tests/files/{input_bytes}", "rb") as input_file:
                input_bytes = input_file.read()
        assert match_mp3_header(input_bytes, len(input_bytes), index) == expected

    @pytest.mark.parametrize(
        "input_bytes,expected",
        [
            (b"\xff\xfb\x90d\x00", (3, 128000, 44100, 0)),
            (b"\xff\x00\x90d\x00", (0, 80000, 11025, 0)),
            (b"\xff\x10\x90d\x00", (2, 80000, 22050, 0)),
        ],
    )
    def test_parse_mp3_frame(self, input_bytes, expected):
        assert parse_mp3_frame(input_bytes) == expected

    def test_mp3_framesize(self):
        assert mp3_framesize(1, 0, 44100, 1) == 1
        assert mp3_framesize(0, 0, 44100, 1) == 1

    @pytest.mark.parametrize(
        "input_bytes,expected",
        [
            ("foo.mp3", "audio/mpeg"),
            ("foo.mp4", "video/mp4"),
            ("foo.webm", "video/webm"),
            ("NonID3.mp3", "audio/mpeg"),
            (b"\x00\x00\x00\x00", None),
        ],
    )
    def test_audio_video(self, input_bytes, expected):
        if isinstance(input_bytes, str):
            with open(f"tests/files/{input_bytes}", "rb") as input_file:
                input_bytes = input_file.read()
        assert get_audio_video_mime(input_bytes) == expected

    def test_image(self):
        assert get_image_mime(self.body_gif) == "image/gif"
        assert get_image_mime(b"\x00\x00\x00\x00") is None

    def test_font(self):
        assert get_font_mime(self.body_ttf) == "font/ttf"
        assert get_font_mime(b"\x00\x00\x00\x00") is None

    def test_archive(self):
        assert get_archive_mime(self.body_zip) == "application/zip"
        assert get_archive_mime(b"\x00\x00\x00\x00") is None
