#: Section 6.1, step 1
#: https://mimesniff.spec.whatwg.org/commit-snapshots/609a3a3c935fbb805b46cf3d90768d695a1dcff2/#matching-an-image-type-pattern  # noqa: E501
IMAGE_PATTERNS = (
    (b"\x00\x00\x01\x00", b"\xff\xff\xff\xff", None, "image/x-icon"),
    (b"\x00\x00\x02\x00", b"\xff\xff\xff\xff", None, "image/x-icon"),
    (b"BM", b"\xff\xff", None, "image/bmp"),
    (b"GIF87a", b"\xff\xff\xff\xff\xff\xff", None, "image/gif",),
    (b"GIF89a", b"\xff\xff\xff\xff\xff\xff", None, "image/gif",),
    (
        b"RIFF\x00\x00\x00\x00WEBPVP",
        b"\xff\xff\xff\xff\x00\x00\x00\x00\xff\xff\xff\xff\xff\xff",
        None,
        "image/webp",
    ),
    (b"\x89PNG\r\n\x1a\n", b"\xff\xff\xff\xff\xff\xff\xff\xff", None, "image/png",),
    (b"\xff\xd8\xff", b"\xff\xff\xff", None, "image/jpeg",),
)

#: Section 6.2, step 1
#: https://mimesniff.spec.whatwg.org/commit-snapshots/609a3a3c935fbb805b46cf3d90768d695a1dcff2/#matching-an-audio-or-video-type-pattern  # noqa: E501
AUDIO_VIDEO_PATTERNS = (
    (b".snd", b"\xff\xff\xff\xff", None, "audio/basic",),
    (
        b"FORM\x00\x00\x00\x00AIFF",
        b"\xff\xff\xff\xff\x00\x00\x00\x00\xff\xff\xff\xff",
        None,
        "audio/aiff",
    ),
    (b"ID3", b"\xff\xff\xff", None, "audio/mpeg",),
    (b"OggS\x00", b"\xff\xff\xff\xff\xff", None, "application/ogg",),
    (b"MThd\x00\x00\x00\x06", b"\xff\xff\xff\xff\xff\xff\xff\xff", None, "audio/midi",),
    (
        b"RIFF\x00\x00\x00\x00AVI ",
        b"\xff\xff\xff\xff\x00\x00\x00\x00\xff\xff\xff\xff",
        None,
        "video/avi",
    ),
    (
        b"RIFF\x00\x00\x00\x00WAVE",
        b"\xff\xff\xff\xff\x00\x00\x00\x00\xff\xff\xff\xff",
        None,
        "audio/wave",
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
        "application/vnd.ms-fontobject",
    ),
    (b"\x00\x01\x00\x00", b"\xff\xff\xff\xff", None, "font/ttf",),
    (b"OTTO", b"\xff\xff\xff\xff", None, "font/otf"),
    (b"ttcf", b"\xff\xff\xff\xff", None, "font/collection",),
    (b"wOFF", b"\xff\xff\xff\xff", None, "font/woff",),
    (b"wOF2", b"\xff\xff\xff\xff", None, "font/woff2",),
)

#: Section 6.4, step 1
#: https://mimesniff.spec.whatwg.org/commit-snapshots/609a3a3c935fbb805b46cf3d90768d695a1dcff2/#matching-an-archive-type-pattern  # noqa: E501
ARCHIVE_PATTERNS = (
    (b"\x1f\x8b\x08", b"\xff\xff\xff", None, "application/x-gzip"),
    (b"PK\x03\x04", b"\xff\xff\xff\xff", None, "application/zip",),
    (b"Rar \x1a\x07\x00", b"\xff\xff\xff\xff\xff\xff\xff", None, "application/x-rar-compressed",),
)

#: Section 7.1, step 1
#: https://mimesniff.spec.whatwg.org/commit-snapshots/609a3a3c935fbb805b46cf3d90768d695a1dcff2/#identifying-a-resource-with-an-unknown-mime-type  # noqa: E501
TEXT_PATTERNS = (

    )
