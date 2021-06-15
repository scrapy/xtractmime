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


# handling resource metadata
def _should_check_for_apache_bug(supplied_type, http_origin):
    if http_origin and (
        supplied_type in _APACHE_TYPES_STR
        or supplied_type in _APACHE_TYPES_BYTES
    ):
        return True

    return False


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

    return "mimetype"
