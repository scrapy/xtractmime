__version__ = "0.0.0"
from typing import Optional, Set, Tuple, Union

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
        while (
            input_index < input_size
            and input_bytes[input_index : input_index + 1] in lstrip  # noqa: E203
        ):
            input_index += 1

    while pattern_index < pattern_size:
        masked_byte = bytes([input_bytes[input_index] & pattern_mask[pattern_index]])
        if masked_byte != byte_pattern[pattern_index : pattern_index + 1]:  # noqa: E203
            return False
        input_index += 1
        pattern_index += 1

    return True


def extract_mime(
    body: bytes,
    *,
    content_types: Optional[Tuple[Union[bytes, str]]] = None,
    http_origin: bool = True,
    no_sniff: bool = False,
    extra_types: Optional[Tuple[Tuple[bytes, bytes, Set[bytes], Union[bytes, str]], ...]] = None,
) -> bytes:

    return b"mimetype"
