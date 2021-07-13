import pytest

from xtractmime import _is_match_mime_pattern, WHITESPACE_BYTES


class TestMain:

    input_bytes = b"GIF87a" + bytes.fromhex("401f7017f70000")

    @pytest.mark.parametrize(
        "input_bytes,byte_pattern,pattern_mask,lstrip,expected",
        [
            (input_bytes, b"GIF87a", b"\xff\xff\xff\xff\xff\xff", None, True),
            (input_bytes, b"GIF87a", b"\xff\xff\xff\xff\xff", None, ValueError),
            (b" \t\n\rGIF87a", b"GIF87a", b"\xff\xff\xff\xff\xff\xff", WHITESPACE_BYTES, True),
            (b"GIF", b"GIF87a", b"\xff\xff\xff\xff\xff\xff", None, False),
            (b"\xff\xff\xff\xff\xff\xff", b"GIF87a", b"\xff\xff\xff\xff\xff\xff", None, False),
        ],
    )
    def test_is_match_mime_pattern(
        self, input_bytes, byte_pattern, pattern_mask, lstrip, expected
    ):
        if type(expected) == type and issubclass(expected, Exception):
            with pytest.raises(expected):
                _is_match_mime_pattern(
                    input_bytes=input_bytes,
                    byte_pattern=byte_pattern,
                    pattern_mask=pattern_mask,
                    lstrip=lstrip,
                )
        else:
            assert (
                _is_match_mime_pattern(
                    input_bytes=input_bytes,
                    byte_pattern=byte_pattern,
                    pattern_mask=pattern_mask,
                    lstrip=lstrip,
                )
                == expected
            )
