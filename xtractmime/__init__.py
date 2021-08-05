__version__ = "0.0.0"
from typing import Optional, Set, Tuple
from xtractmime._patterns import _APACHE_TYPES, WHITESPACE_BYTES
from xtractmime._utils import (
    contains_binary,
    get_archive_mime,
    get_audio_video_mime,
    get_extra_mime,
    get_image_mime,
    get_text_mime,
)
from xtractmime.mimegroups import is_audio_video_mime_type, is_html_mime_type, is_image_mime_type

RESOURCE_HEADER_BUFFER_LENGTH = 1445


def _find_unknown_mimetype(
    input_bytes: bytes,
    sniff_scriptable: bool,
    extra_types: Optional[Tuple[Tuple[bytes, bytes, Optional[Set[bytes]], bytes], ...]],
) -> Optional[bytes]:
    if sniff_scriptable:
        matched_type = get_text_mime(input_bytes)
        if matched_type:
            return matched_type

    matched_type = get_extra_mime(input_bytes, extra_types=extra_types)
    if matched_type:
        return matched_type

    matched_type = get_image_mime(input_bytes)
    if matched_type:
        return matched_type

    matched_type = get_audio_video_mime(input_bytes)
    if matched_type:
        return matched_type

    matched_type = get_archive_mime(input_bytes)
    if matched_type:
        return matched_type

    if not contains_binary(input_bytes):
        return b"text/plain"

    return b"application/octet-stream"


def _sniff_mislabled_binary(input_bytes: bytes) -> Optional[bytes]:

    if input_bytes[:2] in (b"\xfe\xff", b"\xff\xfe") or input_bytes[:3] == b"\xef\xbb\xbf":
        return b"text/plain"

    if not contains_binary(input_bytes):
        return b"text/plain"

    return b"application/octet-stream"


def _sniff_mislabled_feed(input_bytes: bytes, supplied_type: bytes) -> Optional[bytes]:
    input_size = len(input_bytes)
    index = 0

    if input_bytes[:3] == b"\xef\xbb\xbf":
        index += 3

    while index < input_size:
        while True:
            if not input_bytes[index : index + 1]:
                return supplied_type

            if input_bytes[index : index + 1] == b"<":
                index += 1
                break

            if input_bytes[index : index + 1] not in WHITESPACE_BYTES:
                return supplied_type

            index += 1

        while True:
            loop_break = False
            if not input_bytes[index : index + 1]:
                return supplied_type

            if input_bytes[index : index + 3] == b"!--":
                index += 3
                while True:
                    if not input_bytes[index : index + 1]:
                        return supplied_type

                    if input_bytes[index : index + 3] == b"-->":
                        index += 3
                        loop_break = True
                        break

                    index += 1

            if loop_break:
                break

            if input_bytes[index : index + 1] == b"!":
                index += 1
                while True:
                    if not input_bytes[index : index + 1]:
                        return supplied_type

                    if input_bytes[index : index + 1] == b">":
                        index += 1
                        loop_break = True
                        break

                    index += 1

            if loop_break:
                break

            if input_bytes[index : index + 1] == b"?":
                index += 1
                while True:
                    if not input_bytes[index : index + 1]:
                        return supplied_type

                    if input_bytes[index : index + 2] == b"?>":
                        index += 2
                        loop_break = True
                        break

                    index += 1

            if loop_break:
                break

            if input_bytes[index : index + 3] == b"rss":
                return b"application/rss+xml"

            if input_bytes[index : index + 4] == b"feed":
                return b"application/atom+xml"

            if input_bytes[index : index + 7] == b"rdf:RDF":
                index += 7
                while True:
                    if not input_bytes[index : index + 1]:
                        return supplied_type

                    if input_bytes[index : index + 24] == b"http://purl.org/rss/1.0/":
                        index += 24
                        while True:
                            if not input_bytes[index : index + 1]:
                                return supplied_type

                            if (
                                input_bytes[index : index + 43]
                                == b"http://www.w3.org/1999/02/22-rdf-syntax-ns#"
                            ):
                                return b"application/rss+xml"

                            index += 1

                    if (
                        input_bytes[index : index + 43]
                        == b"http://www.w3.org/1999/02/22-rdf-syntax-ns#"
                    ):
                        index += 43
                        while True:
                            if not input_bytes[index : index + 1]:
                                return supplied_type

                            if input_bytes[index : index + 24] == b"http://purl.org/rss/1.0/":
                                return b"application/rss+xml"

                            index += 1

                    index += 1

            return supplied_type

    return supplied_type


def extract_mime(
    body: bytes,
    *,
    content_types: Optional[Tuple[bytes]] = None,
    http_origin: bool = True,
    no_sniff: bool = False,
    extra_types: Optional[Tuple[Tuple[bytes, bytes, Optional[Set[bytes]], bytes], ...]] = None,
    supported_types: Set[bytes] = None,
) -> Optional[bytes]:
    extra_types = extra_types or tuple()
    supplied_type = content_types[-1] if content_types else b""
    supplied_type = supplied_type.split(b";")[0].strip().lower()
    check_for_apache = http_origin and supplied_type in _APACHE_TYPES
    resource_header = memoryview(body)[:RESOURCE_HEADER_BUFFER_LENGTH]

    if supplied_type in (b"", b"unknown/unknown", b"application/unknown", b"*/*"):
        return _find_unknown_mimetype(resource_header, not no_sniff, extra_types)

    if no_sniff:
        return supplied_type

    if check_for_apache:
        return _sniff_mislabled_binary(resource_header)

    if supplied_type.endswith(b"+xml") or supplied_type in {b"text/xml", b"application/xml"}:
        return supplied_type

    if is_html_mime_type(supplied_type):
        return _sniff_mislabled_feed(resource_header, supplied_type)

    if supported_types:
        if is_image_mime_type(supplied_type):
            matched_type = get_image_mime(resource_header)
            if matched_type in supported_types:
                return matched_type

        if is_audio_video_mime_type(supplied_type):
            matched_type = get_audio_video_mime(resource_header)
            if matched_type in supported_types:
                return matched_type

    return supplied_type
