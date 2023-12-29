import pytest

from xtractmime import (
    _find_unknown_mimetype,
    _sniff_mislabled_binary,
    _sniff_mislabled_feed,
    extract_mime,
    is_binary_data,
)


class TestMain:

    sample_xml1 = b"""<?xml version = "1.0" encoding = "UTF-8" ?>
                        <!--Sample xml comment-->
                        <rss version="2.0">
                        <class_list>
                           <student>
                              <name>XYZ</name>
                              <grade>A</grade>
                           </student>
                        </class_list>"""

    sample_xml2 = b"""<?xml version = "1.0" encoding = "UTF-8" ?>
                        <feed xmlns="http://www.w3.org/2005/Atom">
                        <class_list>
                           <student>
                              <name>XYZ</name>
                              <grade>A</grade>
                           </student>
                        </class_list>"""

    sample_xml3 = b"""<?xml version = "1.0" encoding = "UTF-8" ?>
                        <!ELEMENT spec (front, body, back?)>
                        <class_list>
                           <student>
                              <name>XYZ</name>
                              <grade>A</grade>
                           </student>
                        </class_list>"""

    sample_xml4 = b"""<?xml version="1.0" encoding="utf-8"?>
                        <rdf:RDF
                          xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
                          xmlns:content="http://purl.org/rss/1.0/modules/content/"
                          xmlns="http://purl.org/rss/1.0/"
                        >
                        </rdf:RDF>"""

    sample_xml5 = b"""<?xml version="1.0" encoding="utf-8"?>
                        <rdf:RDF
                          xmlns:content="http://purl.org/rss/1.0/modules/content/"
                          xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
                          xmlns="http://purl.org/rss/1.0/"
                        >
                        </rdf:RDF>"""

    extra_types = ((b"test", b"\xff\xff\xff\xff", None, b"text/test"),)

    @pytest.mark.parametrize(
        "body,content_types,http_origin,no_sniff,extra_types,supported_types,expected",
        [
            ("foo.pdf", None, True, False, None, None, b"application/pdf"),
            ("foo.gif", (b"image/gif",), True, True, None, None, b"image/gif"),
            ("foo.txt", (b"text/plain",), True, False, None, None, b"text/plain"),
            ("foo.xml", (b"text/xml",), True, False, None, None, b"text/xml"),
            ("foo.html", (b"text/html",), True, False, None, None, b"text/html"),
            ("foo.gif", (b"image/gif",), True, False, None, (b"image/gif",), b"image/gif"),
            ("foo.mp4", (b"video/mp4",), True, False, None, (b"video/mp4",), b"video/mp4"),
            (b"GIF87a", (b"image/gif",), True, False, None, (b"image/x-icon",), b"image/gif"),
            (b"ID3", (b"audio/mpeg",), True, False, None, (b"audio/basic",), b"audio/mpeg"),
            (b"\x00\x00\x00\x00", (b"text/test",), True, False, None, None, b"text/test"),
            (b"", (b"text/html; charset=utf-8",), True, False, None, None, b"text/html"),
            (b"", (b"text/htmlpdfthing",), True, False, None, None, b"text/htmlpdfthing"),
            (b"", None, True, False, None, None, b"text/plain"),
            (
                b"test",
                None,
                True,
                False,
                extra_types,
                None,
                b"text/test",
            ),
            (
                b"TEST",
                None,
                True,
                False,
                extra_types,
                None,
                b"text/plain",
            ),
            # Even if the body is binary, if the Content-Type says it is text,
            # we interpret it as text, as long as the Content-Type is not one
            # of the 4 affected by the Apache bug.
            #
            # https://mimesniff.spec.whatwg.org/#interpreting-the-resource-metadata
            *(
                (
                    b"\x00\x01\xff",
                    (supplied_content_type,),
                    True,
                    False,
                    None,
                    None,
                    expected_content_type,
                )
                for (supplied_content_type, expected_content_type) in (
                    (b"text/json", b"text/json"),
                    *(
                        (supplied_content_type, b"text/plain")
                        for supplied_content_type in (
                            b"text/plain; charset=Iso-8859-1",
                            b"text/plain; charset=utf-8",
                            b"text/plain; charset=windows-1252",
                        )
                    ),
                    *(
                        (supplied_content_type, b"application/octet-stream")
                        for supplied_content_type in (
                            b"text/plain",
                            b"text/plain; charset=ISO-8859-1",
                            b"text/plain; charset=iso-8859-1",
                            b"text/plain; charset=UTF-8",
                        )
                    ),
                )
            ),
            # Malformed MIME type
            *(
                (b"...", (mime_type,), True, False, None, None, b"text/plain")
                for mime_type in (
                    b"javascript charset=UTF-8",
                    b"a/b/c",
                    b"a/[",
                    b"[/a",
                )
            ),
        ],
    )
    def test_extract_mime(
        self, body, content_types, http_origin, no_sniff, extra_types, supported_types, expected
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
                extra_types=extra_types,
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

    @pytest.mark.parametrize(
        "input_bytes,supplied_type,expected",
        [
            ("foo.xml", b"text/xml", b"text/xml"),
            (sample_xml1, b"application/rss+xml", b"application/rss+xml"),
            (sample_xml2, b"application/atom+xml", b"application/atom+xml"),
            (sample_xml3, b"text/xml", b"text/xml"),
            (sample_xml4, b"application/rss+xml", b"application/rss+xml"),
            (sample_xml5, b"application/rss+xml", b"application/rss+xml"),
            (b"test", b"text/test", b"text/test"),
            (b" ", None, None),
            (b"<", None, None),
            (b"<!--", None, None),
            (b"<!", None, None),
            (b"<?", None, None),
            (b"<rdf:RDF", None, None),
            (b"<rdf:RDF xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#'", None, None),
            (b"<rdf:RDF xmlns:content='http://purl.org/rss/1.0/modules/content/'", None, None),
            (b"", None, None),
        ],
    )
    def test_sniff_mislabled_feed(self, input_bytes, supplied_type, expected):
        if isinstance(input_bytes, str):
            with open(f"tests/files/{input_bytes}", "rb") as input_file:
                input_bytes = input_file.read()
        assert _sniff_mislabled_feed(input_bytes, supplied_type) == expected

    def test_is_binary_data(self):
        assert is_binary_data(b"\x00\x01")
        assert not is_binary_data(b"\x09\x0a")
