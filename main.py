from typing import List, Union

_APACHE_TYPES = ["text/plain", "text/plain; charset=ISO-8859-1", 
                "text/plain; charset=iso-8859-1", 
                "text/plain; charset=UTF-8"]

#handling resource metadata
def _get_resource_metadata(content_types, http_origin):
    if http_origin:
        if content_types[-1] in _APACHE_TYPES:
            return True

    return False


#main function
def extract_mime(body: bytes, *, content_types: List[Union[str, bytes]]=[], http_origin: bool=True, no_sniff: bool=False) -> str:
    supplied_type = content_types[-1]

    check_for_apache = _get_resource_metadata(supplied_type, http_origin)
    
    pass