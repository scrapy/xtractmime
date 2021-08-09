import pytest

from unittest import mock
from xtractmime._utils import is_match_mime_pattern
from xtractmime._patterns import WHITESPACE_BYTES

from xtractmime._utils import (
    contains_binary,
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

    input_bytes = b"GIF87a" + bytes.fromhex("401f7017f70000")

    @pytest.mark.parametrize(
        "input_bytes,byte_pattern,pattern_mask,lstrip,expected",
        [
            (input_bytes, b"GIF87a", bytes.fromhex("ffffffffffff"), None, True),
            (input_bytes, b"GIF87a", bytes.fromhex("ffffffffff"), None, ValueError),
            (b" \t\n\rGIF87a", b"GIF87a", bytes.fromhex("ffffffffffff"), WHITESPACE_BYTES, True),
            (b"GIF", b"GIF87a", bytes.fromhex("ffffffffffff"), None, False),
            (bytes.fromhex("ffffffffffff"), b"GIF87a", bytes.fromhex("ffffffffffff"), None, False),
        ],
    )
    def test_is_match_mime_pattern(
        self, input_bytes, byte_pattern, pattern_mask, lstrip, expected
    ):
        if type(expected) == type and issubclass(expected, Exception):
            with pytest.raises(expected):
                is_match_mime_pattern(
                    input_bytes=input_bytes,
                    byte_pattern=byte_pattern,
                    pattern_mask=pattern_mask,
                    lstrip=lstrip,
                )
        else:
            assert (
                is_match_mime_pattern(
                    input_bytes=input_bytes,
                    byte_pattern=byte_pattern,
                    pattern_mask=pattern_mask,
                    lstrip=lstrip,
                )
                == expected
            )

    @pytest.mark.parametrize(
        "input_bytes,expected",
        [
            ("foo.mp4", True),
            (bytes.fromhex("000000"), False),
            (bytes.fromhex("000000") + b" ftypmp4", False),
            (bytes.fromhex("000000") + b" ftypmp42", False),
            (
                bytes.fromhex("000000")
                + b" testmp42"
                + bytes.fromhex("00000000")
                + b"mp42mp41isomavc1",
                False,
            ),
            (
                bytes.fromhex("000000")
                + b" ftyp2222"
                + bytes.fromhex("00000000")
                + b"2222mp41isomavc1",
                True,
            ),
            (
                bytes.fromhex("000000")
                + b" ftyp2222"
                + bytes.fromhex("00000000")
                + b"22222221isomavc1",
                False,
            ),
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
            (bytes.fromhex("000000"), False),
            (bytes.fromhex("1a") + b"F" + bytes.fromhex("dfa3"), False),
            (
                bytes.fromhex("1a") + b"E" + bytes.fromhex("dfa3") + b"B" + bytes.fromhex("82"),
                False,
            ),
            (
                bytes.fromhex("1a")
                + b"E"
                + bytes.fromhex("dfa3")
                + b"B"
                + bytes.fromhex("82000000"),
                False,
            ),
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
            (417, bytes.fromhex("000000"), False),
            (417, bytes.fromhex("fffb90") + b"d" + bytes.fromhex("00"), False),
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
            (bytes.fromhex("000000"), 0, False),
            (bytes.fromhex("00000000"), 0, False),
            (bytes.fromhex("ffe00000"), 0, False),
            (bytes.fromhex("ffe7f000"), 0, False),
            (bytes.fromhex("ffe70c00"), 0, False),
            (bytes.fromhex("ffe70000"), 0, False),
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
            (bytes.fromhex("fffb90") + b"d" + bytes.fromhex("00"), (3, 128000, 44100, 0)),
            (bytes.fromhex("ff0090") + b"d" + bytes.fromhex("00"), (0, 80000, 11025, 0)),
            (bytes.fromhex("ff1090") + b"d" + bytes.fromhex("00"), (2, 80000, 22050, 0)),
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
            ("foo.mp3", b"audio/mpeg"),
            ("foo.mp4", b"video/mp4"),
            ("foo.webm", b"video/webm"),
            ("NonID3.mp3", b"audio/mpeg"),
            (bytes.fromhex("00000000"), None),
        ],
    )
    def test_audio_video(self, input_bytes, expected):
        if isinstance(input_bytes, str):
            with open(f"tests/files/{input_bytes}", "rb") as input_file:
                input_bytes = input_file.read()
        assert get_audio_video_mime(input_bytes) == expected

    @pytest.mark.parametrize(
        "input_bytes,expected",
        [
            ("foo.html", b"text/html"),
            ("foo.pdf", b"application/pdf"),
            (bytes.fromhex("00000000"), None),
        ],
    )
    def test_text(self, input_bytes, expected):
        if isinstance(input_bytes, str):
            with open(f"tests/files/{input_bytes}", "rb") as input_file:
                input_bytes = input_file.read()
        assert get_text_mime(input_bytes) == expected

    @pytest.mark.parametrize(
        "input_bytes,extra_types,expected",
        [
            ("foo.ps", None, b"application/postscript"),
            (b"test", ((b"test", bytes.fromhex("ffffffff"), None, b"text/test"),), b"text/test"),
            (bytes.fromhex("00000000"), None, None),
        ],
    )
    def test_extra(self, input_bytes, extra_types, expected):
        if isinstance(input_bytes, str):
            with open(f"tests/files/{input_bytes}", "rb") as input_file:
                input_bytes = input_file.read()
        assert get_extra_mime(input_bytes, extra_types) == expected

    def test_image(self):
        assert get_image_mime(self.body_gif) == b"image/gif"
        assert get_image_mime(bytes.fromhex("00000000")) is None

    def test_font(self):
        assert get_font_mime(self.body_ttf) == b"font/ttf"
        assert get_font_mime(bytes.fromhex("00000000")) is None

    def test_archive(self):
        assert get_archive_mime(self.body_zip) == b"application/zip"
        assert get_archive_mime(bytes.fromhex("00000000")) is None

    def test_contains_binary(self):
        assert contains_binary(bytes.fromhex("0001"))
        assert not contains_binary(bytes.fromhex("090a"))
