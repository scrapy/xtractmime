# xtractmime

The `xtractmime` is a python module based on the complete implementation of 
[MIME Sniffing Standards](https://mimesniff.spec.whatwg.org/). The module 
provides simple function to determine the mime type or the content's format of the
body in a web request or a web response by analyzing the byte sequences in it.


Additionally, `xtractmime` provides various methods to determine if any mime type
belongs to a specific mime group or not. For instance, HTML Mime types, XML Mime types
and many more...

---

## Requirements

* Python 3.6+

---

## Installation

---

## License

`xtractmime` is distributed under a [BSD-3](https://opensource.org/licenses/BSD-3-Clause) license.

---

## Basic usage

### funtion `xtractmime.extract_mime(body: bytes, *, content_types: Optional[Tuple[bytes]] = None, http_origin: bool = True, no_sniff: bool = 	False, extra_types: Optional[Tuple[Tuple[bytes, bytes, Optional[Set[bytes]], bytes], ...]] = None, supported_types: Set[bytes] = None) -> Optional[bytes]`

Return `mimetype` as a byte string if the byte sequence in the provided content is recognized by `xtractmime`
else return `None`

Below mentioned is a simple example of using `xtractmime.extract_mime` to 
determine mime type of a text content as input.

```python
>>> from xtractmime import extract_mime
>>> body = b"Sample text content"
>>> extract_mime(body)
b'text/plain'
>>>
```
