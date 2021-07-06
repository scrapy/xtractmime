from struct import unpack
from typing import Tuple, Union

from xtractmime import _is_match_mime_pattern
from xtractmime._patterns import (
    ARCHIVE_PATTERNS,
    AUDIO_VIDEO_PATTERNS,
    FONT_PATTERNS,
    IMAGE_PATTERNS,
)

SAMPLE_RATES = (44100, 48000, 32000)
MP25_RATES = (
    0,
    8000,
    16000,
    24000,
    32000,
    40000,
    48000,
    56000,
    64000,
    80000,
    96000,
    112000,
    128000,
    144000,
    160000,
)
MP3_RATES = (
    0,
    32000,
    40000,
    48000,
    56000,
    64000,
    80000,
    96000,
    112000,
    128000,
    160000,
    192000,
    224000,
    256000,
    320000,
)


def is_mp4_signature(input_bytes: bytes) -> bool:
    input_size = len(input_bytes)
    if input_size < 12:
        return False

    box_size = unpack(">I", input_bytes[0:4])[0]

    if input_size < box_size or box_size % 4:
        return False

    if input_bytes[4:8] != b"ftyp":
        return False

    if input_bytes[8:11] == b"mp4":
        return True

    bytes_read = 16
    while bytes_read < box_size:
        if input_bytes[bytes_read : bytes_read + 3] == b"mp4":  # noqa: E203
            return True
        bytes_read += 4

    return False


def parse_vint_number_size(input_bytes: memoryview) -> int:
    """Return an integer value by which the index in the current input bytes of a
    WebM file should be incremented

    Based on https://mimesniff.spec.whatwg.org/commit-snapshots/609a3a3c935fbb805b46cf3d90768d695a1dcff2/#signature-for-webm,  # noqa: E501
    This implementation doesn't compute the value for "parsed number" as there is
    no specific use of it in implementing the function "is_webm_signature()".
    """
    input_size = len(input_bytes)
    mask = 128
    max_vint_size = 8
    limit = min(max_vint_size, input_size)
    first_byte = input_bytes[0]
    for number_size in range(1, limit):
        if first_byte & mask:
            return number_size
        mask >>= 1
    return limit


def is_webm_signature(input_bytes: bytes) -> bool:
    """Return True if the input bytes belong to a WebM file, or False otherwise.

    Based on https://mimesniff.spec.whatwg.org/commit-snapshots/609a3a3c935fbb805b46cf3d90768d695a1dcff2/#signature-for-webm,  # noqa: E501
    This implementation has been slightly changed according to the
    https://github.com/whatwg/mimesniff/issues/93 which suggests that index can
    never be more than 38, and input_size can be as much as 1445 according to the
    standards which means that "less than" mentioned on line 6.1.5 should actually
    read "greater than or equal to".
    """
    input_size = len(input_bytes)
    if input_size < 4:
        return False

    if input_bytes[:4] != b"\x1aE\xdf\xa3":
        return False

    index = 4

    limit = min(input_size, 38)
    while index < limit:
        if input_bytes[index : index + 2] == b"B\x82":  # noqa: E203
            index += 2

            if index >= input_size:
                break

            number_size = parse_vint_number_size(memoryview(input_bytes)[index:])
            index += number_size

            if index >= input_size - 4:
                break

            if input_bytes[index : index + 4] == b"webm":  # noqa: E203
                return True
        index += 1

    return False


def match_mp3_header(input_bytes: bytes, input_size: int, index: int) -> bool:
    if input_size < 4:
        return False

    if (
        input_bytes[index : index + 1] != b"\xff"  # noqa: E203
        or bytes([input_bytes[index + 1] & 224]) != b"\xe0"
    ):
        return False

    layer = (input_bytes[index + 1] & 6) >> 1
    if layer == 0:
        return False

    bit_rate = (input_bytes[index + 2] & 240) >> 4

    if bit_rate == 15:
        return False

    sample_rate = (input_bytes[index + 2] & 12) >> 2
    if sample_rate == 3:
        return False

    final_layer = (input_bytes[index + 1] & 6) >> 1

    if 4 - final_layer != 3:
        return False

    return True


def parse_mp3_frame(input_bytes: bytes) -> Tuple[int, int, int, int]:
    version = (input_bytes[1] & 24) >> 3
    bit_rate_index = (input_bytes[2] & 240) >> 4

    if version & 1:
        bit_rate = MP3_RATES[bit_rate_index]
    else:
        bit_rate = MP25_RATES[bit_rate_index]

    sample_rate_index = (input_bytes[2] & 12) >> 2
    freq = SAMPLE_RATES[sample_rate_index]

    if version == 2:
        freq >>= 1
    elif version == 0:
        freq >>= 2

    pad = (input_bytes[2] & 2) >> 1

    return version, bit_rate, freq, pad


def mp3_framesize(version, bit_rate, freq, pad) -> int:
    if (version & 1) == 0:
        scale = 72
    else:
        scale = 144

    size = bit_rate * scale / freq

    if pad:
        size += 1

    return int(size)


def is_mp3_non_ID3_signature(input_bytes: bytes) -> bool:
    """Return True if the input bytes belong to an MP3 file without ID3
    metadata, or False otherwise.

    This implementation does not match with standards due to various
    problems with the algorithm according to https://github.com/whatwg/mimesniff/issues/70.

    The current implementation follows
    https://dxr.mozilla.org/mozilla-central/source/toolkit/components/mediasniffer/mp3sniff.c
    as the algorithm for MP3 without ID3 sniffing mentioned in standards is originally
    based on mp3sniff.c.
    """
    input_size = len(input_bytes)
    index = 0

    if not match_mp3_header(input_bytes, input_size, index):
        return False

    version, bit_rate, freq, pad = parse_mp3_frame(input_bytes)

    skipped_bytes = mp3_framesize(version, bit_rate, freq, pad)

    if skipped_bytes < 4 or skipped_bytes + 4 >= input_size:
        return False

    index += skipped_bytes

    if match_mp3_header(input_bytes, input_size, index):
        return True
    else:
        return False


def is_image(input_bytes: bytes) -> Union[str, None]:
    for pattern in IMAGE_PATTERNS:
        if _is_match_mime_pattern(input_bytes, pattern[0], pattern[1], pattern[2]):
            return pattern[3]

    return None


def is_audio_video(input_bytes: bytes) -> Union[str, None]:
    for pattern in AUDIO_VIDEO_PATTERNS:
        if _is_match_mime_pattern(input_bytes, pattern[0], pattern[1], pattern[2]):
            return pattern[3]

    if is_mp4_signature(input_bytes):
        return "video/mp4"

    if is_webm_signature(input_bytes):
        return "video/webm"

    if is_mp3_non_ID3_signature(input_bytes):
        return "audio/mpeg"

    return None


def is_font(input_bytes: bytes) -> Union[str, None]:
    for pattern in FONT_PATTERNS:
        if _is_match_mime_pattern(input_bytes, pattern[0], pattern[1], pattern[2]):
            return pattern[3]

    return None


def is_archive(input_bytes: bytes) -> Union[str, None]:
    for pattern in ARCHIVE_PATTERNS:
        if _is_match_mime_pattern(input_bytes, pattern[0], pattern[1], pattern[2]):
            return pattern[3]

    return None
