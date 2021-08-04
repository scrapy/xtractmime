from typing import Optional, Set, Tuple


#: Section 3
#: https://mimesniff.spec.whatwg.org/commit-snapshots/609a3a3c935fbb805b46cf3d90768d695a1dcff2/#terminology  # noqa: E501
BINARY_BYTES = (
    b"\x00",
    b"\x01",
    b"\x02",
    b"\x03",
    b"\x04",
    b"\x05",
    b"\x06",
    b"\x07",
    b"\x08",
    b"\x0b",
    b"\x0e",
    b"\x0f",
    b"\x10",
    b"\x11",
    b"\x12",
    b"\x13",
    b"\x14",
    b"\x15",
    b"\x16",
    b"\x17",
    b"\x18",
    b"\x19",
    b"\x1a",
    b"\x1c",
    b"\x1d",
    b"\x1e",
    b"\x1f",
)
WHITESPACE_BYTES = {b"\t", b"\r", b"\x0c", b"\n", b" "}

#: Section 4.6
#: https://mimesniff.spec.whatwg.org/commit-snapshots/609a3a3c935fbb805b46cf3d90768d695a1dcff2/#mime-type-groups  # noqa: E501
FONT_TYPES = [
    b"application/font-cff",
    b"application/font-off",
    b"application/font-sfnt",
    b"application/font-ttf",
    b"application/font-woff",
    b"application/vnd.ms-fontobject",
    b"application/vnd.ms-opentype",
]
ARCHIVE_TYPES = [
    b"application/x-rar-compressed",
    b"application/zip",
    b"application/x-gzip",
]
JAVASCRIPT_TYPES = [
    b"application/ecmascript",
    b"application/javascript",
    b"application/x-ecmascript",
    b"application/x-javascript",
    b"text/ecmascript",
    b"text/javascript",
    b"text/javascript1.0",
    b"text/javascript1.1",
    b"text/javascript1.2",
    b"text/javascript1.3",
    b"text/javascript1.4",
    b"text/javascript1.5",
    b"text/jscript",
    b"text/livescript",
    b"text/x-ecmascript",
    b"text/x-javascript",
]

#: Section 5.1, step 2
#: https://mimesniff.spec.whatwg.org/commit-snapshots/609a3a3c935fbb805b46cf3d90768d695a1dcff2/#interpreting-the-resource-metadata  # noqa: E501
_APACHE_TYPES = [
    b"text/plain",
    b"text/plain; charset=ISO-8859-1",
    b"text/plain; charset=iso-8859-1",
    b"text/plain; charset=UTF-8",
]

#: Section 6.1, step 1
#: https://mimesniff.spec.whatwg.org/commit-snapshots/609a3a3c935fbb805b46cf3d90768d695a1dcff2/#matching-an-image-type-pattern  # noqa: E501
IMAGE_PATTERNS = (
    (b"\x00\x00\x01\x00", b"\xff\xff\xff\xff", None, b"image/x-icon"),
    (b"\x00\x00\x02\x00", b"\xff\xff\xff\xff", None, b"image/x-icon"),
    (b"BM", b"\xff\xff", None, b"image/bmp"),
    (b"GIF87a", b"\xff\xff\xff\xff\xff\xff", None, b"image/gif",),
    (b"GIF89a", b"\xff\xff\xff\xff\xff\xff", None, b"image/gif",),
    (
        b"RIFF\x00\x00\x00\x00WEBPVP",
        b"\xff\xff\xff\xff\x00\x00\x00\x00\xff\xff\xff\xff\xff\xff",
        None,
        b"image/webp",
    ),
    (b"\x89PNG\r\n\x1a\n", b"\xff\xff\xff\xff\xff\xff\xff\xff", None, b"image/png",),
    (b"\xff\xd8\xff", b"\xff\xff\xff", None, b"image/jpeg",),
)

#: Section 6.2, step 1
#: https://mimesniff.spec.whatwg.org/commit-snapshots/609a3a3c935fbb805b46cf3d90768d695a1dcff2/#matching-an-audio-or-video-type-pattern  # noqa: E501
AUDIO_VIDEO_PATTERNS = (
    (b".snd", b"\xff\xff\xff\xff", None, b"audio/basic",),
    (
        b"FORM\x00\x00\x00\x00AIFF",
        b"\xff\xff\xff\xff\x00\x00\x00\x00\xff\xff\xff\xff",
        None,
        b"audio/aiff",
    ),
    (b"ID3", b"\xff\xff\xff", None, b"audio/mpeg",),
    (b"OggS\x00", b"\xff\xff\xff\xff\xff", None, b"application/ogg",),
    (b"MThd\x00\x00\x00\x06", b"\xff\xff\xff\xff\xff\xff\xff\xff", None, b"audio/midi",),
    (
        b"RIFF\x00\x00\x00\x00AVI ",
        b"\xff\xff\xff\xff\x00\x00\x00\x00\xff\xff\xff\xff",
        None,
        b"video/avi",
    ),
    (
        b"RIFF\x00\x00\x00\x00WAVE",
        b"\xff\xff\xff\xff\x00\x00\x00\x00\xff\xff\xff\xff",
        None,
        b"audio/wave",
    ),
)

#: Section 6.3, step 1
#: https://mimesniff.spec.whatwg.org/commit-snapshots/609a3a3c935fbb805b46cf3d90768d695a1dcff2/#matching-a-font-type-pattern  # noqa: E501
FONT_PATTERNS = (
    (
        (
            b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00LP"
        ),
        (
            b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff"
        ),
        None,
        b"application/vnd.ms-fontobject",
    ),
    (b"\x00\x01\x00\x00", b"\xff\xff\xff\xff", None, b"font/ttf",),
    (b"OTTO", b"\xff\xff\xff\xff", None, b"font/otf"),
    (b"ttcf", b"\xff\xff\xff\xff", None, b"font/collection",),
    (b"wOFF", b"\xff\xff\xff\xff", None, b"font/woff",),
    (b"wOF2", b"\xff\xff\xff\xff", None, b"font/woff2",),
)

#: Section 6.4, step 1
#: https://mimesniff.spec.whatwg.org/commit-snapshots/609a3a3c935fbb805b46cf3d90768d695a1dcff2/#matching-an-archive-type-pattern  # noqa: E501
ARCHIVE_PATTERNS = (
    (b"\x1f\x8b\x08", b"\xff\xff\xff", None, b"application/x-gzip"),
    (b"PK\x03\x04", b"\xff\xff\xff\xff", None, b"application/zip",),
    (b"Rar \x1a\x07\x00", b"\xff\xff\xff\xff\xff\xff\xff", None, b"application/x-rar-compressed",),
)

#: Section 7.1, step 1
#: https://mimesniff.spec.whatwg.org/commit-snapshots/609a3a3c935fbb805b46cf3d90768d695a1dcff2/#identifying-a-resource-with-an-unknown-mime-type  # noqa: E501
TEXT_PATTERNS = tuple(
    (prefix + suffix, mask, WHITESPACE_BYTES, b"text/html")
    for prefix, mask, in (
        (b"<!DOCTYPE HTML", b"\xff\xff\xdf\xdf\xdf\xdf\xdf\xdf\xdf\xff\xdf\xdf\xdf\xdf\xff"),
        (b"<HTML", b"\xff\xdf\xdf\xdf\xdf\xff"),
        (b"<HEAD", b"\xff\xdf\xdf\xdf\xdf\xff"),
        (b"<SCRIPT", b"\xff\xdf\xdf\xdf\xdf\xdf\xdf\xff"),
        (b"<IFRAME", b"\xff\xdf\xdf\xdf\xdf\xdf\xdf\xff"),
        (b"<H1", b"\xff\xdf\xff\xff"),
        (b"<DIV", b"\xff\xdf\xdf\xdf\xff"),
        (b"<FONT", b"\xff\xdf\xdf\xdf\xdf\xff"),
        (b"<TABLE", b"\xff\xdf\xdf\xdf\xdf\xdf\xff"),
        (b"<A", b"\xff\xdf\xff"),
        (b"<STYLE", b"\xff\xdf\xdf\xdf\xdf\xdf\xff"),
        (b"<TITLE", b"\xff\xdf\xdf\xdf\xdf\xdf\xff"),
        (b"<B", b"\xff\xdf\xff"),
        (b"<BODY", b"\xff\xdf\xdf\xdf\xdf\xff"),
        (b"<BR", b"\xff\xdf\xdf\xff"),
        (b"<P", b"\xff\xdf\xff"),
        (b"<!--", b"\xff\xff\xff\xff\xff"),
    )
    for suffix in (b"\x20", b"\x3E")
) + (
    (b"<?xml", b"\xff\xff\xff\xff\xff", WHITESPACE_BYTES, b"text/xml"),
    (b"%PDF-", b"\xff\xff\xff\xff\xff", None, b"application/pdf"),
)

#: Section 7.1, step 2
#: https://mimesniff.spec.whatwg.org/commit-snapshots/609a3a3c935fbb805b46cf3d90768d695a1dcff2/#identifying-a-resource-with-an-unknown-mime-type  # noqa: E501
EXTRA_PATTERNS: Tuple[Tuple[bytes, bytes, Optional[Set[bytes]], bytes], ...] = (
    (
        b"%!PS-Adobe-",
        b"\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff",
        None,
        b"application/postscript",
    ),
    (b"\xfe\xff\x00\x00", b"\xff\xff\x00\x00", None, b"text/plain"),
    (b"\xff\xfe\x00\x00", b"\xff\xff\x00\x00", None, b"text/plain"),
    (b"\xef\xbb\xbf\x00", b"\xff\xff\xff\x00", None, b"text/plain"),
)
