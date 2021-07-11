import pytest

from xtractmime import _find_unknown_mimetype, _sniff_mislabled_binary, extract_mime


class TestMain:
    @pytest.mark.parametrize(
        "body,content_types,http_origin,no_sniff,supported_types,expected",
        [
            ("foo.pdf", None, True, False, None, b"application/pdf"),
            ("foo.gif", (b"image/gif",), True, True, None, b"image/gif"),
            ("foo.txt", (b"text/plain",), True, False, None, b"text/plain"),
            ("foo.xml", (b"text/xml",), True, False, None, b"text/xml"),
            ("foo.html", (b"text/html",), True, False, None, b"text/html"),
            ("foo.gif", (b"image/gif",), True, False, (b"image/gif",), b"image/gif"),
            ("foo.mp4", (b"video/mp4",), True, False, (b"video/mp4",), b"video/mp4"),
            (b"\x00\x00\x00\x00", (b"text/test",), True, False, None, b"text/test"),
        ],
    )
    def test_extract_mime(
        self, body, content_types, http_origin, no_sniff, supported_types, expected
    ):
        if isinstance(body, str):
            with open(f"tests/files/{body}", "rb") as input_file:
                body = input_file.read()
        assert (
            extract_mime(
                body,
                content_types=content_types,
                http_origin=http_origin,
                no_sniff=no_sniff,
                supported_types=supported_types,
            )
            == expected
        )

    @pytest.mark.parametrize(
        "input_bytes,expected",
        [
            ("foo.txt", b"text/plain"),
            ("foo.exe", b"application/octet-stream"),
            (b"\xfe\xff", b"text/plain"),
        ],
    )
    def test_sniff_mislabled_binary(self, input_bytes, expected):
        if isinstance(input_bytes, str):
            with open(f"tests/files/{input_bytes}", "rb") as input_file:
                input_bytes = input_file.read()
        assert _sniff_mislabled_binary(input_bytes) == expected

    @pytest.mark.parametrize(
        "input_bytes,sniff_scriptable,extra_types,expected",
        [
            ("foo.pdf", True, None, b"application/pdf"),
            ("foo.gif", False, None, b"image/gif"),
            ("foo.mp4", False, None, b"video/mp4"),
            ("foo.zip", False, None, b"application/zip"),
            ("foo.txt", False, None, b"text/plain"),
            ("foo.exe", False, None, b"application/octet-stream"),
            (b"test", False, ((b"test", b"\xff\xff\xff\xff", None, b"text/test"),), b"text/test"),
        ],
    )
    def test_find_unknown_mimetype(self, input_bytes, sniff_scriptable, extra_types, expected):
        if isinstance(input_bytes, str):
            with open(f"tests/files/{input_bytes}", "rb") as input_file:
                input_bytes = input_file.read()
        assert _find_unknown_mimetype(input_bytes, sniff_scriptable, extra_types) == expected
