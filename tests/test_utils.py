import unittest
import pytest

from xtractmime.utils import _is_mp4_signature, _is_webm_signature

class TestUtils:

    with open("tests/files/foo.mp4", "rb") as fp:
        body_mp4 = fp.read()

    with open("tests/files/foo.webm", "rb") as fp:
        body_webm = fp.read()

    @pytest.mark.parametrize("input_bytes,expected",[
        (body_mp4,True),
        (b"\x00\x00\x00",False),
        (b"\x00\x00\x00 ftypmp4",False),
        (b"\x00\x00\x00 ftypmp42",False),
        (b"\x00\x00\x00 testmp42\x00\x00\x00\x00mp42mp41isomavc1",False),
        (b"\x00\x00\x00 ftyp2222\x00\x00\x00\x002222mp41isomavc1",True),
        (b"\x00\x00\x00 ftyp2222\x00\x00\x00\x0022222221isomavc1",False),
        ])
    def test_is_mp4_signature(self, input_bytes, expected):
        assert _is_mp4_signature(input_bytes) == expected

    @pytest.mark.parametrize("input_bytes,expected",[
        (body_webm, True),
        (b"\x00\x00\x00",False),
        (b"\x1aF\xdf\xa3",False),
        (b"\x1aE\xdf\xa3B\x82",False),
        (b"\x1aE\xdf\xa3B\x82\x00\x00\x00",False),
        ])
    def test_is_webm_signature(self, input_bytes, expected):
        assert _is_webm_signature(input_bytes) == expected