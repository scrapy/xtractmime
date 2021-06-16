from typing import List, Union

_APACHE_TYPES_STR = [
    "text/plain",
    "text/plain; charset=ISO-8859-1",
    "text/plain; charset=iso-8859-1",
    "text/plain; charset=UTF-8",
]

_APACHE_TYPES_BYTES = [
    "746578742f706c61696e",
    "746578742f706c61696e3b20636861727365743d49534f2d383835392d31",
    "746578742f706c61696e3b20636861727365743d69736f2d383835392d31",
    "746578742f706c61696e3b20636861727365743d5554462d38",
]


_WHITESPACE_BYTES = [b"\t", b"\r", b"\x0c", b"\n", b" "]


# handling resource metadata
def _should_check_for_apache_bug(supplied_type, http_origin):
    if http_origin and (
        supplied_type in _APACHE_TYPES_STR
        or supplied_type in _APACHE_TYPES_BYTES
    ):
        return True

    return False

# reading resource header
def _read_resource_header(body):
    buffer = b""
    if len(body) < 1445:
        buffer = body
    else:
        buffer = body[:1445]
    return buffer


# Matching a MIME type pattern
def _is_match_mime_pattern(input_bytes, byte_pattern, pattern_mask, lead_whitespace=None):
    input_size, pattern_size, mask_size = len(input_bytes), len(byte_pattern), len(pattern_mask)

    assert pattern_size == mask_size, "pattern's length should match mask's length"

    if input_size < pattern_size:
        return False

    input_index, pattern_index = 0, 0

    if lead_whitespace:
        while input_index < input_size and bytes([input_bytes[input_index]]) in _WHITESPACE_BYTES :
            input_index += 1

    while pattern_index < pattern_size:
        masked_byte = bytes([input_bytes[input_index] & pattern_mask[pattern_index]])
        if masked_byte != bytes([byte_pattern[pattern_index]]):
            return False
        input_index += 1
        pattern_index += 1

    return True


# main function
def extract_mime(
    body: bytes,
    *,
    content_types: List[Union[str, bytes]] = [],
    http_origin: bool = True,
    no_sniff: bool = False
) -> str:
    supplied_type = None
    if content_types:
        supplied_type = content_types[-1]

    check_for_apache = _should_check_for_apache_bug(supplied_type, http_origin)
    resource_header = _read_resource_header(body)

    return "mimetype"
