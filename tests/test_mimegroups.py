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
        # MIME type types
        (b"image/foo", {"image"}),
        (b"audio/foo", {"audio_video"}),
        (b"video/foo", {"audio_video"}),
        (b"font/foo", {"font"}),
        # MIME types subtype suffixes
        (b"application/foo+zip", {"zip"}),
        (b"application/foo+xml", {"xml", "scriptable"}),
        (b"application/foo+json", {"json"}),
        # 4.6. MIME type groups, audio or video MIME type
        # https://mimesniff.spec.whatwg.org/commit-snapshots/609a3a3c935fbb805b46cf3d90768d695a1dcff2/#audio-or-video-mime-type
        (b"application/ogg", {"audio_video"}),
        # 4.6. MIME type groups, font MIME type
        # https://mimesniff.spec.whatwg.org/commit-snapshots/609a3a3c935fbb805b46cf3d90768d695a1dcff2/#font-mime-type
        (b"application/font-cff", {"font"}),
        (b"application/font-off", {"font"}),
        (b"application/font-sfnt", {"font"}),
        (b"application/font-ttf", {"font"}),
        (b"application/font-woff", {"font"}),
        (b"application/vnd.ms-fontobject", {"font"}),
        (b"application/vnd.ms-opentype", {"font"}),
        # 4.6. MIME type groups, zip-based MIME type
        # https://mimesniff.spec.whatwg.org/commit-snapshots/609a3a3c935fbb805b46cf3d90768d695a1dcff2/#zip-based-mime-type
        (b"application/zip", {"zip", "archive"}),
        # 4.6. MIME type groups, archive MIME type
        # https://mimesniff.spec.whatwg.org/commit-snapshots/609a3a3c935fbb805b46cf3d90768d695a1dcff2/#archive-mime-type
        (b"application/x-rar-compressed", {"archive"}),
        (b"application/zip", {"zip", "archive"}),
        (b"application/x-gzip", {"archive"}),
        # 4.6. MIME type groups, xml MIME type
        # https://mimesniff.spec.whatwg.org/commit-snapshots/609a3a3c935fbb805b46cf3d90768d695a1dcff2/#xml-mime-type
        (b"text/xml", {"xml", "scriptable"}),
        (b"application/xml", {"xml", "scriptable"}),
        # 4.6. MIME type groups, html MIME type
        # https://mimesniff.spec.whatwg.org/commit-snapshots/609a3a3c935fbb805b46cf3d90768d695a1dcff2/#html-mime-type
        (b"text/html", {"html", "scriptable"}),
        # 4.6. MIME type groups, scriptable MIME type
        # https://mimesniff.spec.whatwg.org/commit-snapshots/609a3a3c935fbb805b46cf3d90768d695a1dcff2/#scriptable-mime-type
        (b"application/pdf", {"scriptable"}),
        # 4.6. MIME type groups, javascript MIME type
        # https://mimesniff.spec.whatwg.org/commit-snapshots/609a3a3c935fbb805b46cf3d90768d695a1dcff2/#javascript-mime-type
        (b"application/ecmascript", {"javascript"}),
        (b"application/javascript", {"javascript"}),
        (b"application/x-ecmascript", {"javascript"}),
        (b"application/x-javascript", {"javascript"}),
        (b"text/ecmascript", {"javascript"}),
        (b"text/javascript", {"javascript"}),
        (b"text/javascript1.0", {"javascript"}),
        (b"text/javascript1.1", {"javascript"}),
        (b"text/javascript1.2", {"javascript"}),
        (b"text/javascript1.3", {"javascript"}),
        (b"text/javascript1.4", {"javascript"}),
        (b"text/javascript1.5", {"javascript"}),
        (b"text/jscript", {"javascript"}),
        (b"text/livescript", {"javascript"}),
        (b"text/x-ecmascript", {"javascript"}),
        (b"text/x-javascript", {"javascript"}),
        # 4.6. MIME type groups, json MIME type
        # https://mimesniff.spec.whatwg.org/commit-snapshots/609a3a3c935fbb805b46cf3d90768d695a1dcff2/#json-mime-type
        (b"application/json", {"json"}),
        (b"text/json", {"json"}),
        # 5.1. Interpreting resource metadata
        # https://mimesniff.spec.whatwg.org/commit-snapshots/609a3a3c935fbb805b46cf3d90768d695a1dcff2/#interpreting-the-resource-metadata
        (b"text/plain", {}),
        (b"text/plain; charset=ISO-8859-1", {}),
        (b"text/plain; charset=iso-8859-1", {}),
        (b"text/plain; charset=UTF-8", {}),
        # 6.1. Matching an image type pattern
        # https://mimesniff.spec.whatwg.org/commit-snapshots/609a3a3c935fbb805b46cf3d90768d695a1dcff2/#matching-an-image-type-pattern
        (b"image/x-icon", {"image"}),
        (b"image/bmp", {"image"}),
        (b"image/gif", {"image"}),
        (b"image/webp", {"image"}),
        (b"image/png", {"image"}),
        (b"image/jpeg", {"image"}),
        # 6.2. Matching an audio or video type pattern
        # https://mimesniff.spec.whatwg.org/commit-snapshots/609a3a3c935fbb805b46cf3d90768d695a1dcff2/#matching-an-audio-or-video-type-pattern
        (b"audio/basic", {"audio_video"}),
        (b"audio/aiff", {"audio_video"}),
        (b"audio/mpeg", {"audio_video"}),
        (b"application/ogg", {"audio_video"}),
        (b"audio/midi", {"audio_video"}),
        (b"video/avi", {"audio_video"}),
        (b"audio/wave", {"audio_video"}),
        (b"video/mp4", {"audio_video"}),
        (b"video/webm", {"audio_video"}),
        (b"audio/mpeg", {"audio_video"}),
        # 6.3. Matching a font type pattern
        # https://mimesniff.spec.whatwg.org/commit-snapshots/609a3a3c935fbb805b46cf3d90768d695a1dcff2/#matching-a-font-type-pattern
        (b"application/vnd.ms-fontobject", {"font"}),
        (b"font/ttf", {"font"}),
        (b"font/otf", {"font"}),
        (b"font/collection", {"font"}),
        (b"font/woff", {"font"}),
        (b"font/woff2", {"font"}),
        # 6.4. Matching an archive type pattern
        # https://mimesniff.spec.whatwg.org/commit-snapshots/609a3a3c935fbb805b46cf3d90768d695a1dcff2/#matching-an-archive-type-pattern
        (b"application/x-gzip", {"archive"}),
        (b"application/zip", {"zip", "archive"}),
        (b"application/x-rar-compressed", {"archive"}),
        # 7. Determining the computed mime type of a resource
        # https://mimesniff.spec.whatwg.org/commit-snapshots/609a3a3c935fbb805b46cf3d90768d695a1dcff2/#determining-the-computed-mime-type-of-a-resource
        (b"unknown/unknown", {}),
        (b"application/unknown", {}),
        (b"*/*", {}),
        # 7.1. Identifying a resource with an unknown MIME type
        # https://mimesniff.spec.whatwg.org/commit-snapshots/609a3a3c935fbb805b46cf3d90768d695a1dcff2/#identifying-a-resource-with-an-unknown-mime-type
        (b"text/html", {"html", "scriptable"}),
        (b"application/postscript", {}),
        (b"text/plain", {}),
        (b"application/octet-stream", {}),
        # 7.3. Sniffing a mislabeled feed
        # https://mimesniff.spec.whatwg.org/commit-snapshots/609a3a3c935fbb805b46cf3d90768d695a1dcff2/#sniffing-a-mislabeled-feed
        (b"application/rss+xml", {"xml", "scriptable"}),
        (b"application/atom+xml", {"xml", "scriptable"}),
        # 8.8. Sniffing in a text track context
        # https://mimesniff.spec.whatwg.org/commit-snapshots/609a3a3c935fbb805b46cf3d90768d695a1dcff2/#sniffing-in-a-text-track-context
        (b"text/vtt", {}),
        # 8.9. Sniffing in a cache manifest context
        # https://mimesniff.spec.whatwg.org/commit-snapshots/609a3a3c935fbb805b46cf3d90768d695a1dcff2/#sniffing-in-a-cache-manifest-context
        (b"text/cache-manifest", {}),
    ],
)
def test_mime_group(mime_type, mime_groups):
    assert all(
        is_in_mime_group(mime_type) == (mime_group in mime_groups)
        for mime_group, is_in_mime_group in ALL_MIME_GROUPS.items()
    )
