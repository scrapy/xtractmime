import pytest

from xtractmime import extract_mime


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
