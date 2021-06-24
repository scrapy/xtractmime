import unittest
import pytest

from unittest import mock

from xtractmime.utils import (
    _is_mp4_signature,
    _is_webm_signature,
    _is_mp3_non_ID3_signature,
    _parse_vint,
    _match_mp3_header,
    _parse_mp3_frame,
    _mp3_framesize,
)


class TestUtils:

    with open("tests/files/foo.mp4", "rb") as fp:
        body_mp4 = fp.read()

    with open("tests/files/foo.webm", "rb") as fp:
        body_webm = fp.read()

    with open("tests/files/NonID3.mp3", "rb") as fp:
        body_mp3 = fp.read()

    @pytest.mark.parametrize(
        "input_bytes,expected",
        [
            (body_mp4, True),
            (b"\x00\x00\x00", False),
            (b"\x00\x00\x00 ftypmp4", False),
            (b"\x00\x00\x00 ftypmp42", False),
            (b"\x00\x00\x00 testmp42\x00\x00\x00\x00mp42mp41isomavc1", False),
            (b"\x00\x00\x00 ftyp2222\x00\x00\x00\x002222mp41isomavc1", True),
            (b"\x00\x00\x00 ftyp2222\x00\x00\x00\x0022222221isomavc1", False),
        ],
    )
    def test_is_mp4_signature(self, input_bytes, expected):
        assert _is_mp4_signature(input_bytes) == expected

    @pytest.mark.parametrize(
        "input_bytes,expected",
        [
            (body_webm, True),
            (b"\x00\x00\x00", False),
            (b"\x1aF\xdf\xa3", False),
            (b"\x1aE\xdf\xa3B\x82", False),
            (b"\x1aE\xdf\xa3B\x82\x00\x00\x00", False),
        ],
    )
    def test_is_webm_signature(self, input_bytes, expected):
        assert _is_webm_signature(input_bytes) == expected

    def test_parse_vint(self):
        assert _parse_vint(self.body_webm, len(self.body_webm), 6) == 8
        assert _parse_vint(self.body_webm, len(self.body_webm), 30) == 1

    @pytest.mark.parametrize(
        "input_bytes,expected",
        [
            (body_mp3, True),
            (b"\x00\x00\x00", False),
            (b"\xff\xfb\x90d\x00", False),
            (body_mp3[:50], False),
        ],
    )
    @mock.patch("xtractmime.utils._mp3_framesize")
    def test_is_mp3_non_ID3_signature(self, mock_framesize, input_bytes, expected):
        if input_bytes == self.body_mp3[:50]:
            mock_framesize.return_value = 10
            assert _is_mp3_non_ID3_signature(input_bytes) == expected
        else:
            mock_framesize.return_value = 417
            assert _is_mp3_non_ID3_signature(input_bytes) == expected

    @pytest.mark.parametrize(
        "input_bytes,input_size,index,expected",
        [
            (body_mp3, len(body_mp3), 0, True),
            (b"\x00\x00\x00", 3, 0, False),
            (b"\x00\x00\x00\x00", 4, 0, False),
            (b"\xff\xe0\x00\x00", 4, 0, False),
            (b"\xff\xe7\xf0\x00", 4, 0, False),
            (b"\xff\xe7\x0c\x00", 4, 0, False),
            (b"\xff\xe7\x00\x00", 4, 0, False),
        ],
    )
    def test_match_mp3_header(self, input_bytes, input_size, index, expected):
        assert _match_mp3_header(input_bytes, input_size, index) == expected

    @pytest.mark.parametrize(
        "input_bytes,expected",
        [
            (b"\xff\xfb\x90d\x00", (3, 128000, 44100, 0)),
            (b"\xff\x00\x90d\x00", (0, 80000, 11025, 0)),
            (b"\xff\x10\x90d\x00", (2, 80000, 22050, 0)),
        ],
    )
    def test_parse_mp3_frame(self, input_bytes, expected):
        assert _parse_mp3_frame(input_bytes) == expected

    def test_mp3_framesize(self):
        assert _mp3_framesize(1, 0, 44100, 1) == 1
        assert _mp3_framesize(0, 0, 44100, 1) == 1
