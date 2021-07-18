from _patterns import ARCHIVE_TYPES, FONT_TYPES, JAVASCRIPT_TYPES


def is_image_mime_type(mime_type: bytes) -> bool:
    if mime_type.startswith(b"image/"):
        return True

    return False


def is_audio_video_mime_type(mime_type: bytes) -> bool:
    video_types = (b"audio/", b"video/")
    if mime_type.startswith(video_types) or mime_type == b"application/ogg":
        return True

    return False


def is_font_mime_type(mime_type: bytes) -> bool:
    if mime_type.startswith(b"font/") or mime_type in FONT_TYPES:
        return True

    return False


def is_zip_based_mime_type(mime_type: bytes) -> bool:
    if mime_type.endswith(b"+zip") or mime_type == b"application/zip":
        return True

    return False


def is_archive_mime_type(mime_type: bytes) -> bool:
    if mime_type in ARCHIVE_TYPES:
        return True

    return False


def is_xml_mime_type(mime_type: bytes) -> bool:
    if mime_type.endswith(b"+xml") or mime_type in (b"text/xml", b"application/xml"):
        return True

    return False


def is_html_mime_type(mime_type: bytes) -> bool:
    if mime_type == b"text/html":
        return True

    return False


def is_scriptable_mime_type(mime_type: bytes) -> bool:
    if is_xml_mime_type(mime_type):
        return True

    if is_html_mime_type(mime_type):
        return True

    if mime_type == b"application/pdf":
        return True

    return False


def is_javascript_mime_type(mime_type: bytes) -> bool:
    if mime_type.lower() in JAVASCRIPT_TYPES:
        return True

    return False


def is_json_mime_type(mime_type: bytes) -> bool:
    if mime_type.endswith(b"+json") or mime_type in (b"application/json", b"text/json"):
        return True

    return False
