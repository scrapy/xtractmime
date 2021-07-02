__version__ = "0.0.0"
from typing import Optional, Set, Tuple
from xtractmime._utils import (
    is_archive,
    is_audio_video,
    is_font,
    is_image,
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


def _find_unknown_mimetype(input_bytes: bytes, sniff_scriptable: bool):
    # TODO
    pass


def _sniff_mislabled_binary(input_bytes: bytes):
    # TODO
    pass


def _compare_feed_html(input_bytes: bytes):
    # TODO
    pass


def extract_mime(
    body: bytes,
    *,
    content_types: Optional[Tuple[bytes]] = None,
    http_origin: bool = True,
    no_sniff: bool = False,
    extra_types: Optional[Tuple[Tuple[bytes, bytes, Set[bytes], str], ...]] = None,
) -> str:
    extra_types = extra_types or tuple()
    supplied_type = content_types[-1] if content_types else None
    check_for_apache = http_origin and supplied_type in _APACHE_TYPES
    resource_header = memoryview(body) if len(body) < 1445 else memoryview(body)[:1445]

    if supplied_type in (None, "unknown/unknown", "application/unknown", "*/*"):
        _find_unknown_mimetype(body, not no_sniff)

    if no_sniff:
        return supplied_type

    if check_for_apache:
        return _sniff_mislabled_binary(body)

    if supplied_type[-4:] is "+xml" or supplied_type in ("text/xml", "application/xml"):
        return supplied_type

    if supplied_type is "text/html":
        return _compare_feed_html(body)

    matched_type = is_image(resource_header)

    if matched_type:
        return matched_type

    matched_type = is_audio_video(resource_header)

    if matched_type:
        return matched_type

    return supplied_type
