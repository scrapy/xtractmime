import unittest

import pytest

from xtractmime import (
    _should_check_for_apache_bug,
    _is_match_mime_pattern,
    _read_resource_header,
)

from xtractmime.utils import _is_mp4_signature


class TestMain:

    with open("tests/files/foo.pdf", "rb") as fp:
        body = fp.read()

    input_bytes = b"GIF87a" + bytes.fromhex("401f7017f70000")

    @pytest.mark.parametrize("supplied_type,http_origin,expected",[
        (b"text/plain",True,True),
        (b"text/plain",False,False),
        (b"application/pdf",True,False),
        (b"application/pdf",False,False),
        ])
    def test_should_check_for_apache_bug(self, supplied_type, http_origin, expected):
        assert _should_check_for_apache_bug(supplied_type=supplied_type, http_origin=http_origin) == expected

    
    @pytest.mark.parametrize("input_bytes,byte_pattern,pattern_mask,whitespace,expected",[
        (input_bytes,b"GIF87a",b"\xff\xff\xff\xff\xff\xff",None,True),
        (input_bytes,b"GIF87a",b"\xff\xff\xff\xff\xff",None,ValueError),
        (b" \t\n\rGIF87a",b"GIF87a",b"\xff\xff\xff\xff\xff\xff",True,True),
        (b"GIF",b"GIF87a",b"\xff\xff\xff\xff\xff\xff",None,False),
        (b"\xff\xff\xff\xff\xff\xff",b"GIF87a",b"\xff\xff\xff\xff\xff\xff",None,False),
        ])
    def test_is_match_mime_pattern(self, input_bytes, byte_pattern, pattern_mask, whitespace, expected):
        if type(expected) == type and issubclass(expected, Exception):
            with pytest.raises(expected):
                _is_match_mime_pattern(input_bytes=input_bytes,byte_pattern=byte_pattern,pattern_mask=pattern_mask, lead_whitespace = whitespace)
        else:
            assert _is_match_mime_pattern(input_bytes=input_bytes,byte_pattern=byte_pattern,pattern_mask=pattern_mask, lead_whitespace = whitespace) == expected

        
    @pytest.mark.parametrize("body,expected",[(body,body[:1445]),(input_bytes,input_bytes)])
    def test_read_resource_header(self, body, expected):
        assert _read_resource_header(body=body) == expected
