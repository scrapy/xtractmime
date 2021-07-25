import pytest

from xtractmime import mimegroups


ALL_MIME_GROUPS = {
    name[3:-10]: getattr(mimegroups, name)
    for name in dir(mimegroups)
    if name.startswith("is_") and name.endswith("_mime_type")
}


@pytest.mark.parametrize(
    "mime_type,mime_groups",
    [
        (b"image/foo", {"image"}),
        (b"image/x-icon", {"image"}),
        (b"audio/foo", {"audio_video"}),
        (b"audio/basic", {"audio_video"}),
        (b"video/foo", {"audio_video"}),
        (b"video/avi", {"audio_video"}),
        (b"application/ogg", {"audio_video"}),
        (b"font/foo", {"font"}),
        (b"application/vnd.ms-fontobject", {"font"}),
        (b"application/font-cff", {"font"}),
        (b"application/foo+zip", {"zip"}),
        (b"application/zip", {"zip", "archive"}),
        (b"application/x-gzip", {"archive"}),
        (b"application/foo+xml", {"xml", "scriptable"}),
        (b"text/xml", {"xml", "scriptable"}),
        (b"text/html", {"html", "scriptable"}),
        (b"application/pdf", {"scriptable"}),
        (b"application/ecmascript", {"javascript"}),
        (b"application/foo+json", {"json"}),
        (b"text/json", {"json"}),
        (b"application/postscript", {"text"}),
        (b"text/plain", {"text"}),
        (b"text/plain; charset=ISO-8859-1", {"text"}),
    ],
)
def test_mime_group(mime_type, mime_groups):
    assert all(
        is_in_mime_group(mime_type) == (mime_group in mime_groups)
        for mime_group, is_in_mime_group in ALL_MIME_GROUPS.items()
    )
