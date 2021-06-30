"""
Section 6.1, step 1
https://mimesniff.spec.whatwg.org/commit-snapshots
/609a3a3c935fbb805b46cf3d90768d695a1dcff2/#matching-an-image-type-pattern
"""
IMAGE_PATTERNS = (
    (b"\x00\x00\x01\x00", b"\xff\xff\xff\xff", None, "image/x-icon"),  # A Windows Icon signature
    (b"\x00\x00\x02\x00", b"\xff\xff\xff\xff", None, "image/x-icon"),  # A Windows Cursor signature
    (b"BM", b"\xff\xff", None, "image/bmp"),  # The string "BM", a BMP signature
    (
        b"GIF87a",
        b"\xff\xff\xff\xff\xff\xff",
        None,
        "image/gif",
    ),  # The string "GIF87a", a GIF signature
    (
        b"GIF89a",
        b"\xff\xff\xff\xff\xff\xff",
        None,
        "image/gif",
    ),  # The string "GIF89a", a GIF signature
    (
        b"RIFF\x00\x00\x00\x00WEBPVP",
        b"\xff\xff\xff\xff\x00\x00\x00\x00\xff\xff\xff\xff\xff\xff",
        None,
        "image/webp",
    ),  # The string "RIFF" followed by four bytes followed by the string "WEBPVP"
    # An error-checking byte followed by the string "PNG" followed by CR LF SUB LF,
    # the PNG signature
    (b"\x89PNG\r\n\x1a\n", b"\xff\xff\xff\xff\xff\xff\xff\xff", None, "image/png",),
    (
        b"\xff\xd8\xff",
        b"\xff\xff\xff",
        None,
        "image/jpeg",
    ),  # The JPEG Start of Image marker followed by the indicator byte of another marker
)

"""
Section 6.2, step 1
https://mimesniff.spec.whatwg.org/commit-snapshots
/609a3a3c935fbb805b46cf3d90768d695a1dcff2/#matching-an-audio-or-video-type-pattern
"""
AUDIO_VIDEO_PATTERNS = (
    (
        b".snd",
        b"\xff\xff\xff\xff",
        None,
        "audio/basic",
    ),  # The string ".snd", the basic audio signature
    # The string "FORM" followed by four bytes followed by the string "AIFF"
    # the AIFF signature
    (
        b"FORM\x00\x00\x00\x00AIFF",
        b"\xff\xff\xff\xff\x00\x00\x00\x00\xff\xff\xff\xff",
        None,
        "audio/aiff",
    ),
    (
        b"ID3",
        b"\xff\xff\xff",
        None,
        "audio/mpeg",
    ),  # The string "ID3", the ID3v2-tagged MP3 signature
    (
        b"OggS\x00",
        b"\xff\xff\xff\xff\xff",
        None,
        "application/ogg",
    ),  # The string "OggS" followed by NUL, the Ogg container signature
    # The string "MThd" followed by four bytes representing the number 6 in 32 bits
    # (big-endian), the MIDI signature
    (b"MThd\x00\x00\x00\x06", b"\xff\xff\xff\xff\xff\xff\xff\xff", None, "audio/midi",),
    # The string "RIFF" followed by four bytes followed by the string "AVI "
    # the AVI signature
    (
        b"RIFF\x00\x00\x00\x00AVI ",
        b"\xff\xff\xff\xff\x00\x00\x00\x00\xff\xff\xff\xff",
        None,
        "video/avi",
    ),
    # The string "RIFF" followed by four bytes followed by the string "WAVE"
    # the WAVE signature
    (
        b"RIFF\x00\x00\x00\x00WAVE",
        b"\xff\xff\xff\xff\x00\x00\x00\x00\xff\xff\xff\xff",
        None,
        "audio/wave",
    ),
)

"""
Section 6.3, step 1
https://mimesniff.spec.whatwg.org/commit-snapshots
/609a3a3c935fbb805b46cf3d90768d695a1dcff2/#matching-a-font-type-pattern
"""
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
    ),  # 34 bytes followed by the string "LP", the Embedded OpenType signature
    (
        b"\x00\x01\x00\x00",
        b"\xff\xff\xff\xff",
        None,
        "font/ttf",
    ),  # 4 bytes representing the version number 1.0, a TrueType signature
    (b"OTTO", b"\xff\xff\xff\xff", None, "font/otf"),  # The string "OTTO", the OpenType signature
    (
        b"ttcf",
        b"\xff\xff\xff\xff",
        None,
        "font/collection",
    ),  # The string "ttcf", the TrueType Collection signature
    (
        b"wOFF",
        b"\xff\xff\xff\xff",
        None,
        "font/woff",
    ),  # The string "wOFF", the Web Open Font Format 1.0 signature
    (
        b"wOF2",
        b"\xff\xff\xff\xff",
        None,
        "font/woff2",
    ),  # The string "wOF2", the Web Open Font Format 2.0 signature
)

"""
Section 6.4, step 1
https://mimesniff.spec.whatwg.org/commit-snapshots
/609a3a3c935fbb805b46cf3d90768d695a1dcff2/#matching-an-archive-type-pattern
"""
ARCHIVE_PATTERNS = (
    (b"\x1f\x8b\x08", b"\xff\xff\xff", None, "application/x-gzip"),  # The GZIP archive signature
    (
        b"PK\x03\x04",
        b"\xff\xff\xff\xff",
        None,
        "application/zip",
    ),  # The string "PK" followed by ETX EOT, the ZIP archive signature
    (
        b"Rar \x1a\x07\x00",
        b"\xff\xff\xff\xff\xff\xff\xff",
        None,
        "application/x-rar-compressed",
    ),  # The string "Rar " followed by SUB BEL NUL, the RAR archive signature
)
