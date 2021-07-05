__version__ = "0.0.0"
from typing import Optional, Set, Tuple
from xtractmime._utils import (
    contains_binary,
    get_archive_mime,
    get_audio_video_mime,
    get_extra_mime,
    get_font_mime,
    get_image_mime,
    get_text_mime,
)

_APACHE_TYPES = [
    b"text/plain",
    b"text/plain; charset=ISO-8859-1",
    b"text/plain; charset=iso-8859-1",
    b"text/plain; charset=UTF-8",
]
WHITESPACE_BYTES = {b"\t", b"\r", b"\x0c", b"\n", b" "}



def _is_match_mime_pattern(
    input_bytes: bytes, byte_pattern: bytes, pattern_mask: bytes, lstrip: Set[bytes] = None
) -> bool:
    input_size = len(input_bytes)
    pattern_size = len(byte_pattern)
    mask_size = len(pattern_mask)

    if pattern_size != mask_size:
        raise ValueError("pattern's length should match mask's length")

    if input_size < pattern_size:
        return False

    input_index, pattern_index = 0, 0

    if lstrip:
        while input_index < input_size and input_bytes[input_index : input_index + 1] in lstrip:
            input_index += 1

    while pattern_index < pattern_size:
        masked_byte = bytes([input_bytes[input_index] & pattern_mask[pattern_index]])
        if masked_byte != byte_pattern[pattern_index : pattern_index + 1]:
            return False
        input_index += 1
        pattern_index += 1

    return True


def _find_unknown_mimetype(input_bytes: bytes, sniff_scriptable: bool, extra_types: Optional[Tuple[Tuple[bytes, bytes, Set[bytes], str], ...]]) -> str:
    if sniff_scriptable:
        return get_text_mime(input_bytes)

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
        return "text/plain"
    
    return "application/octet-stream"


def _sniff_mislabled_binary(input_bytes: bytes) -> str:
    input_size = len(input_bytes)
    
    if input_size >= 2 and input_bytes.startswith((b"\xfe\xff",b"\xff\xfe",b"\xef\xbb\xbf")):
        return "text/plain"
    
    if not contains_binary(input_bytes):
        return "text/plain"
    
    return "application/octet-stream"


def _sniff_mislabled_feed(input_bytes: bytes, supplied_type: Optional[Tuple[bytes]]) -> str:
    input_size = len(input_bytes)
    index = 0

    if input_bytes[:3] == b"\xef\xbb\xbf":
        index += 3

    while index < input_size:
        while True:
            if not input_bytes[index:index+1]:
                return supplied_type

            if input_bytes[index:index+1] == b"<":
                index += 1
                break

            if input_bytes[index:index+1] not in WHITESPACE_BYTES:
                return supplied_type

            index += 1
    
        while True:
            loop_break = False
            if not input_bytes[index:index+1]:
                return supplied_type

            if input_bytes[index:index+3] == b"!--":
                index += 3
                while True:
                    if not input_bytes[index:index+1]:
                        return supplied_type

                    if input_bytes[index:index+3] == b"-->":
                        index += 3
                        loop_break = True
                        break

                    index += 1

            if loop_break:
                break

            if input_bytes[index:index+1] == b"!":
                index += 1
                while True:
                    if not input_bytes[index:index+1]:
                        return supplied_type

                    if input_bytes[index:index+3] == b">":
                        index += 1
                        loop_break = True
                        break

                    index += 1

            if loop_break:
                break

            if input_bytes[index:index+1] == b"?":
                index += 1
                while True:
                    if not input_bytes[index:index+1]:
                        return supplied_type

                    if input_bytes[index:index+2] == "?>":
                        index += 2
                        loop_break = True
                        break

                    index += 1

            if loop_break:
                break

            if input_bytes[index:index+3] == b"rss":
                return b"application/rss+xml"

            if input_bytes[index:index+4] == b"feed":
                return b"application/atom+xml"

            if input_bytes[index:index+7] == b"rdf:RDF":
                index += 7
                while True:
                    if not input_bytes[index:index+1]:
                        return supplied_type

                    if input_bytes[index:index+24] == b"http://purl.org/rss/1.0/":
                        index += 24
                        while True:
                            if not input_bytes[index:index+1]:
                                return supplied_type

                            if input_bytes[index:index+43] == b"http://www.w3.org/1999/02/22-rdf-syntax-ns#":
                                return b"application/rss+xml"

                            index += 1

                    if input_bytes[index:index+43] == b"http://www.w3.org/1999/02/22-rdf-syntax-ns#":
                        index += 43
                        while True:
                            if not input_bytes[index:index+1]:
                                return supplied_type

                            if input_bytes[index:index+24] == b"http://purl.org/rss/1.0/":
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
    extra_types: Optional[Tuple[Tuple[bytes, bytes, Set[bytes], str], ...]] = None,
    supported_types: Set[str] = None,
) -> str:
    extra_types = extra_types or tuple()
    supplied_type = content_types[-1] if content_types else None
    check_for_apache = http_origin and supplied_type in _APACHE_TYPES
    resource_header = memoryview(body)[:1445]

    if supplied_type in (None, "unknown/unknown", "application/unknown", "*/*"):
        _find_unknown_mimetype(resource_header, not no_sniff, extra_types)

    if no_sniff:
        return supplied_type

    if check_for_apache:
        return _sniff_mislabled_binary(resource_header)

    if supplied_type.endswith("+xml") or supplied_type in {"text/xml", "application/xml"}:
        return supplied_type

    if supplied_type == "text/html":
        return _sniff_mislabled_feed(resource_header)

    if supplied_type.startswith("image/"):
        matched_type = get_image_mime(resource_header)
        if matched_type in supported_types:
            return matched_type

    video_types = ("audio/","video/")
    if supplied_type.startswith(video_types) or supplied_type == "application/ogg":
        matched_type = get_audio_video_mime(resource_header)
        if matched_type in supported_types:
            return matched_type

    return supplied_type
