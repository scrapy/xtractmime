import os
import pytest

from unittest import mock
from xtractmime._utils import is_match_mime_pattern
from xtractmime._patterns import WHITESPACE_BYTES

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

    def get_byte_seq(self, seq):
        if isinstance(seq, tuple):
            byte_seq = b"".join(
                value if isinstance(value, bytes) else bytes.fromhex(value) for value in seq
            )
        elif isinstance(seq, bytes):
            byte_seq = seq
        elif os.path.isfile(f"tests/files/{seq}"):
            with open(f"tests/files/{seq}", "rb") as input_file:
                byte_seq = input_file.read()
        else:
            byte_seq = bytes.fromhex(seq)

        return byte_seq

    @pytest.mark.parametrize(
        "input_bytes,byte_pattern,pattern_mask,lstrip,expected",
        [
            ((b"GIF87a", "401f7017f70000"), b"GIF87a", "ffffffffffff", None, True),
            ((b"GIF87a", "401f7017f70000"), b"GIF87a", "ffffffffff", None, ValueError),
            ((b" \t\n\rGIF87a",), b"GIF87a", "ffffffffffff", WHITESPACE_BYTES, True),
            ((b"GIF",), b"GIF87a", "ffffffffffff", None, False),
            (("ffffffffffff",), b"GIF87a", "ffffffffffff", None, False),
        ],
    )
    def test_is_match_mime_pattern(
        self, input_bytes, byte_pattern, pattern_mask, lstrip, expected
    ):
        input_bytes = self.get_byte_seq(input_bytes)
        pattern_mask = bytes.fromhex(pattern_mask)
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
            ("000000", False),
            (("000000", b" ftypmp4"), False),
            (("000000", b" ftypmp42"), False),
            (("000000", b" testmp42", "00000000", b"mp42mp41isomavc1"), False),
            (("000000", b" ftyp2222", "00000000", b"2222mp41isomavc1"), True),
            (("000000", b" ftyp2222", "00000000", b"22222221isomavc1"), False),
        ],
    )
    def test_is_mp4_signature(self, input_bytes, expected):
        input_bytes = self.get_byte_seq(input_bytes)
        assert is_mp4_signature(input_bytes) == expected

    @pytest.mark.parametrize(
        "input_bytes,expected",
        [
            ("foo.webm", True),
            ("000000", False),
            ("1a 46 df a3", False),
            ("1a 45 df a3 42 82", False),
            ("1a 45 df a3 42 82 00 00 00", False),
        ],
    )
    def test_is_webm_signature(self, input_bytes, expected):
        input_bytes = self.get_byte_seq(input_bytes)
        assert is_webm_signature(input_bytes) == expected

    def test_parse_vint_number_size(self):
        assert parse_vint_number_size(memoryview(self.body_webm)[6:]) == 8
        assert parse_vint_number_size(memoryview(self.body_webm)[30:]) == 1

    @pytest.mark.parametrize(
        "framesize,input_bytes,expected",
        [
            (417, "NonID3.mp3", True),
            (417, "000000", False),
            (417, "ff fb 90 64 00", False),
            (10, "NonID3.mp3", False),
        ],
    )
    @mock.patch("xtractmime._utils.mp3_framesize")
    def test_is_mp3_non_ID3_signature(self, mock_framesize, framesize, input_bytes, expected):
        input_bytes = self.get_byte_seq(input_bytes)
        mock_framesize.return_value = framesize
        assert is_mp3_non_ID3_signature(input_bytes) == expected

    @pytest.mark.parametrize(
        "input_bytes,index,expected",
        [
            ("NonID3.mp3", 0, True),
            ("000000", 0, False),
            ("00000000", 0, False),
            ("ff e0 00 00", 0, False),
            ("ff e7 f0 00", 0, False),
            ("ff e7 0c 00", 0, False),
            ("ff e7 00 00", 0, False),
        ],
    )
    def test_match_mp3_header(self, input_bytes, index, expected):
        input_bytes = self.get_byte_seq(input_bytes)
        assert match_mp3_header(input_bytes, len(input_bytes), index) == expected

    @pytest.mark.parametrize(
        "input_bytes,expected",
        [
            ("ff fb 90 64 00", (3, 128000, 44100, 0)),
            ("ff 00 90 64 00", (0, 80000, 11025, 0)),
            ("ff 10 90 64 00", (2, 80000, 22050, 0)),
        ],
    )
    def test_parse_mp3_frame(self, input_bytes, expected):
        assert parse_mp3_frame(bytes.fromhex(input_bytes)) == expected

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
            ("00000000", None),
        ],
    )
    def test_audio_video(self, input_bytes, expected):
        input_bytes = self.get_byte_seq(input_bytes)
        assert get_audio_video_mime(input_bytes) == expected

    @pytest.mark.parametrize(
        "input_bytes,expected",
        [("foo.html", b"text/html"), ("foo.pdf", b"application/pdf"), ("00000000", None)],
    )
    def test_text(self, input_bytes, expected):
        input_bytes = self.get_byte_seq(input_bytes)
        assert get_text_mime(input_bytes) == expected

    @pytest.mark.parametrize(
        "input_bytes,extra_types,expected",
        [
            ("foo.ps", None, b"application/postscript"),
            (b"test", ((b"test", bytes.fromhex("ffffffff"), None, b"text/test"),), b"text/test"),
            ("00000000", None, None),
        ],
    )
    def test_extra(self, input_bytes, extra_types, expected):
        input_bytes = self.get_byte_seq(input_bytes)
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
