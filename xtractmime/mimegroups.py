from xtractmime._patterns import (
    ARCHIVE_TYPES,
    FONT_TYPES,
    JAVASCRIPT_TYPES,
)


def is_image_mime_type(mime_type: bytes) -> bool:
    return mime_type.startswith(b"image/")


def is_audio_video_mime_type(mime_type: bytes) -> bool:
    video_types = (b"audio/", b"video/")
    return mime_type.startswith(video_types) or mime_type == b"application/ogg"


def is_font_mime_type(mime_type: bytes) -> bool:
    return mime_type.startswith(b"font/") or mime_type in FONT_TYPES


def is_zip_mime_type(mime_type: bytes) -> bool:
    return mime_type.endswith(b"+zip") or mime_type == b"application/zip"


def is_archive_mime_type(mime_type: bytes) -> bool:
    return mime_type in ARCHIVE_TYPES


def is_xml_mime_type(mime_type: bytes) -> bool:
    return mime_type.endswith(b"+xml") or mime_type in (b"text/xml", b"application/xml")


def is_html_mime_type(mime_type: bytes) -> bool:
    return mime_type == b"text/html"


def is_scriptable_mime_type(mime_type: bytes) -> bool:
    if is_xml_mime_type(mime_type):
        return True

    if is_html_mime_type(mime_type):
        return True

    return mime_type == b"application/pdf"


def is_javascript_mime_type(mime_type: bytes) -> bool:
    return mime_type.lower() in JAVASCRIPT_TYPES


def is_json_mime_type(mime_type: bytes) -> bool:
    return mime_type.endswith(b"+json") or mime_type in (b"application/json", b"text/json")
