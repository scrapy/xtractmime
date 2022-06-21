from typing import Optional, Set, Tuple


#: Section 3
#: https://mimesniff.spec.whatwg.org/commit-snapshots/609a3a3c935fbb805b46cf3d90768d695a1dcff2/#terminology  # noqa: E501
BINARY_BYTES = tuple(
    bytes.fromhex(byte)
    for byte in (
        "00",
        "01",
        "02",
        "03",
        "04",
        "05",
        "06",
        "07",
        "08",
        "0B",
        "0E",
        "0F",
        "10",
        "11",
        "12",
        "13",
        "14",
        "15",
        "16",
        "17",
        "18",
        "19",
        "1A",
        "1C",
        "1D",
        "1E",
        "1F",
    )
)
WHITESPACE_BYTES = {b"\t", b"\r", bytes.fromhex("0c"), b"\n", b" "}

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
    (bytes.fromhex("00000100"), bytes.fromhex("ffffffff"), None, b"image/x-icon"),
    (bytes.fromhex("00000200"), bytes.fromhex("ffffffff"), None, b"image/x-icon"),
    (b"BM", bytes.fromhex("ffff"), None, b"image/bmp"),
    (
        b"GIF87a",
        bytes.fromhex("ffffffffffff"),
        None,
        b"image/gif",
    ),
    (
        b"GIF89a",
        bytes.fromhex("ffffffffffff"),
        None,
        b"image/gif",
    ),
    (
        b"RIFF" + bytes.fromhex("00000000") + b"WEBPVP",
        bytes.fromhex("ffffffff00000000ffffffffffff"),
        None,
        b"image/webp",
    ),
    (
        bytes.fromhex("89") + b"PNG\r\n" + bytes.fromhex("1a") + b"\n",
        bytes.fromhex("ffffffffffffffff"),
        None,
        b"image/png",
    ),
    (
        bytes.fromhex("ffd8ff"),
        bytes.fromhex("ffffff"),
        None,
        b"image/jpeg",
    ),
)

#: Section 6.2, step 1
#: https://mimesniff.spec.whatwg.org/commit-snapshots/609a3a3c935fbb805b46cf3d90768d695a1dcff2/#matching-an-audio-or-video-type-pattern  # noqa: E501
AUDIO_VIDEO_PATTERNS = (
    (
        b".snd",
        bytes.fromhex("ffffffff"),
        None,
        b"audio/basic",
    ),
    (
        b"FORM" + bytes.fromhex("00000000") + b"AIFF",
        bytes.fromhex("ffffffff00000000ffffffff"),
        None,
        b"audio/aiff",
    ),
    (
        b"ID3",
        bytes.fromhex("ffffff"),
        None,
        b"audio/mpeg",
    ),
    (
        b"OggS" + bytes.fromhex("00"),
        bytes.fromhex("ffffffffff"),
        None,
        b"application/ogg",
    ),
    (
        b"MThd" + bytes.fromhex("00000006"),
        bytes.fromhex("ffffffffffffffff"),
        None,
        b"audio/midi",
    ),
    (
        b"RIFF" + bytes.fromhex("00000000") + b"AVI ",
        bytes.fromhex("ffffffff00000000ffffffff"),
        None,
        b"video/avi",
    ),
    (
        b"RIFF" + bytes.fromhex("00000000") + b"WAVE",
        bytes.fromhex("ffffffff00000000ffffffff"),
        None,
        b"audio/wave",
    ),
)

#: Section 6.3, step 1
#: https://mimesniff.spec.whatwg.org/commit-snapshots/609a3a3c935fbb805b46cf3d90768d695a1dcff2/#matching-a-font-type-pattern  # noqa: E501
FONT_PATTERNS = (
    (
        (
            bytes.fromhex("00000000000000000000000000000000000000000000000000000000000000000000")
            + b"LP"
        ),
        (
            bytes.fromhex(
                "00000000000000000000000000000000000000000000000000000000000000000000ffff"
            )
        ),
        None,
        b"application/vnd.ms-fontobject",
    ),
    (
        bytes.fromhex("00010000"),
        bytes.fromhex("ffffffff"),
        None,
        b"font/ttf",
    ),
    (b"OTTO", bytes.fromhex("ffffffff"), None, b"font/otf"),
    (
        b"ttcf",
        bytes.fromhex("ffffffff"),
        None,
        b"font/collection",
    ),
    (
        b"wOFF",
        bytes.fromhex("ffffffff"),
        None,
        b"font/woff",
    ),
    (
        b"wOF2",
        bytes.fromhex("ffffffff"),
        None,
        b"font/woff2",
    ),
)

#: Section 6.4, step 1
#: https://mimesniff.spec.whatwg.org/commit-snapshots/609a3a3c935fbb805b46cf3d90768d695a1dcff2/#matching-an-archive-type-pattern  # noqa: E501
ARCHIVE_PATTERNS = (
    (bytes.fromhex("1f8b08"), bytes.fromhex("ffffff"), None, b"application/x-gzip"),
    (
        b"PK" + bytes.fromhex("0304"),
        bytes.fromhex("ffffffff"),
        None,
        b"application/zip",
    ),
    (
        b"Rar " + bytes.fromhex("1a0700"),
        bytes.fromhex("ffffffffffffff"),
        None,
        b"application/x-rar-compressed",
    ),
)

#: Section 7.1, step 1
#: https://mimesniff.spec.whatwg.org/commit-snapshots/609a3a3c935fbb805b46cf3d90768d695a1dcff2/#identifying-a-resource-with-an-unknown-mime-type  # noqa: E501
TEXT_PATTERNS = tuple(
    (prefix + suffix, bytes.fromhex(mask), WHITESPACE_BYTES, b"text/html")
    for prefix, mask, in (
        (b"<!DOCTYPE HTML", "ffffdfdfdfdfdfdfdfffdfdfdfdfff"),
        (b"<HTML", "ffdfdfdfdfff"),
        (b"<HEAD", "ffdfdfdfdfff"),
        (b"<SCRIPT", "ffdfdfdfdfdfdfff"),
        (b"<IFRAME", "ffdfdfdfdfdfdfff"),
        (b"<H1", "ffdfffff"),
        (b"<DIV", "ffdfdfdfff"),
        (b"<FONT", "ffdfdfdfdfff"),
        (b"<TABLE", "ffdfdfdfdfdfff"),
        (b"<A", "ffdfff"),
        (b"<STYLE", "ffdfdfdfdfdfff"),
        (b"<TITLE", "ffdfdfdfdfdfff"),
        (b"<B", "ffdfff"),
        (b"<BODY", "ffdfdfdfdfff"),
        (b"<BR", "ffdfdfff"),
        (b"<P", "ffdfff"),
        (b"<!--", "ffffffffff"),
    )
    for suffix in (b" ", bytes.fromhex("3E"))
) + (
    (b"<?xml", bytes.fromhex("ffffffffff"), WHITESPACE_BYTES, b"text/xml"),
    (b"%PDF-", bytes.fromhex("ffffffffff"), None, b"application/pdf"),
)

#: Section 7.1, step 2
#: https://mimesniff.spec.whatwg.org/commit-snapshots/609a3a3c935fbb805b46cf3d90768d695a1dcff2/#identifying-a-resource-with-an-unknown-mime-type  # noqa: E501
EXTRA_PATTERNS: Tuple[Tuple[bytes, bytes, Optional[Set[bytes]], bytes], ...] = (
    (
        b"%!PS-Adobe-",
        bytes.fromhex("ffffffffffffffffffffff"),
        None,
        b"application/postscript",
    ),
    (bytes.fromhex("feff0000"), bytes.fromhex("ffff0000"), None, b"text/plain"),
    (bytes.fromhex("fffe0000"), bytes.fromhex("ffff0000"), None, b"text/plain"),
    (bytes.fromhex("efbbbf00"), bytes.fromhex("ffffff00"), None, b"text/plain"),
)
