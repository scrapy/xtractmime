from unittest import TestCase

from xtractmime.main import (
    _should_check_for_apache_bug,
    _is_match_mime_pattern,
    _read_resource_header,
)


class TestMain(TestCase):

    file = open("tests/files/foo.pdf", "rb")
    body = file.read()
    file.close()

    input_bytes = b"GIF87a@\x1fp\x17\xf7\x00\x00"

    def test_should_check_for_apache_bug(self):
        self.assertEqual(
            _should_check_for_apache_bug(supplied_type="text/plain", http_origin=True),
            True,
        )
        self.assertEqual(
            _should_check_for_apache_bug(supplied_type="text/plain", http_origin=False),
            False,
        )
        self.assertEqual(
            _should_check_for_apache_bug(
                supplied_type="application/pdf", http_origin=True
            ),
            False,
        )
        self.assertEqual(
            _should_check_for_apache_bug(
                supplied_type="application/pdf", http_origin=False
            ),
            False,
        )

    def test_is_match_mime_pattern(self):
        self.assertEqual(
            _is_match_mime_pattern(
                input_bytes=self.input_bytes,
                byte_pattern=b"GIF87a",
                pattern_mask=b"\xff\xff\xff\xff\xff\xff",
            ),
            True,
        )
        self.assertEqual(
            _is_match_mime_pattern(
                input_bytes=b" \t\n\rGIF87a",
                byte_pattern=b"GIF87a",
                pattern_mask=b"\xff\xff\xff\xff\xff\xff",
                lead_whitespace=1,
            ),
            True,
        )
        self.assertEqual(
            _is_match_mime_pattern(
                input_bytes=b"GIF",
                byte_pattern=b"GIF87a",
                pattern_mask=b"\xff\xff\xff\xff\xff\xff",
            ),
            False,
        )
        self.assertEqual(
            _is_match_mime_pattern(
                input_bytes=b"\xff\xff\xff\xff\xff\xff",
                byte_pattern=b"GIF87a",
                pattern_mask=b"\xff\xff\xff\xff\xff\xff",
            ),
            False,
        )

    def test_read_resource_header(self):
        self.assertEqual(_read_resource_header(body=self.body), self.body[:1445])
        self.assertEqual(_read_resource_header(body=self.input_bytes), self.input_bytes)
