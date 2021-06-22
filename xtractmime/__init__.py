from typing import List, Union, Tuple

_APACHE_TYPES = [
    b"text/plain",
    b"text/plain; charset=ISO-8859-1",
    b"text/plain; charset=iso-8859-1",
    b"text/plain; charset=UTF-8",
]


_WHITESPACE_BYTES = {b"\t", b"\r", b"\x0c", b"\n", b" "}


# handling resource metadata
def _should_check_for_apache_bug(supplied_type, http_origin):
    return http_origin and supplied_type in _APACHE_TYPES


# reading resource header
def _read_resource_header(body):
    buffer = memoryview(body)
    if len(body) < 1445:
        return buffer
    else:
        return buffer[:1445]
    


# Matching a MIME type pattern
def _is_match_mime_pattern(
    input_bytes, byte_pattern, pattern_mask, lead_whitespace=None
):
    input_size = len(input_bytes)
    pattern_size = len(byte_pattern)
    mask_size = len(pattern_mask)

    if pattern_size != mask_size:
        raise ValueError("pattern's length should match mask's length")

    if input_size < pattern_size:
        return False

    input_index, pattern_index = 0, 0

    if lead_whitespace:
        while (
            input_index < input_size
            and input_bytes[input_index:input_index+1] in _WHITESPACE_BYTES
        ):
            input_index += 1

    while pattern_index < pattern_size:
        masked_byte = bytes([input_bytes[input_index] & pattern_mask[pattern_index]])
        if masked_byte != byte_pattern[pattern_index:pattern_index+1]:
            return False
        input_index += 1
        pattern_index += 1

    return True


# main function
def extract_mime(
    body: bytes,
    *,
    content_types: List[bytes] = [],
    http_origin: bool = True,
    no_sniff: bool = False,
    extra_types: List[Tuple[Union[str,bytes]]] = [],
) -> str:
    supplied_type = content_types[-1] if content_types else None

    check_for_apache = _should_check_for_apache_bug(supplied_type, http_origin)
    resource_header = _read_resource_header(body)

    return "mimetype"
 