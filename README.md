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

### function `xtractmime.extract_mime(body: bytes, *, content_types: Optional[Tuple[bytes]] = None, http_origin: bool = True, no_sniff: bool = 	False, extra_types: Optional[Tuple[Tuple[bytes, bytes, Optional[Set[bytes]], bytes], ...]] = None, supported_types: Set[bytes] = None) -> Optional[bytes]`

Return `mimetype` as a byte string if the byte sequence in the provided content is recognized by `xtractmime`
else return `None`

Below mentioned is a simple example of using `xtractmime.extract_mime` to 
determine mime type of a text content as input:

```python
>>> from xtractmime import extract_mime
>>> body = b"Sample text content"
>>> extract_mime(body)
b'text/plain'
>>>
```


Optional `content_types` argument is a tuple of mime types suitable for using as a `Content-Type` header.
For the cases where the format of the content is unrecognizalble for `xtractmime`, it will return
the last mime type in the provided tuple of mime types.

Example using `content_types` argument:

```python
>>> from xtractmime import extract_mime
>>> content_types = (b'text/html',)
>>> body = b''
>>> extract_mime(body, content_types=content_types)
b'text/html'
>>> 
```


Optional `http_origin` argument is a flag to determine if the resource is retrieved via HTTP or not.
`http_origin` is *`True`* (by default) for HTTP responses else *`False`*.

Example using `http_origin` argument:

```python
>>> from xtractmime import extract_mime
>>> body = b'\x00\x01\xff'
>>> content_types = (b'text/plain',)
>>> extract_mime(body, content_types=content_types, http_origin=True)
b'application/octet-stream'
>>> extract_mime(body, content_types=content_types, http_origin=False)
b'text/plain'
```


Optional `no_sniff` argument is a flag which is *`True`* if the user agent does not wish to
perform sniffing on the resource and *`False`* (by default) otherwise. The flag is suitable
for using as a `X-Content-Type-Options` header.

Example using `no_sniff` argument:

```python
>>> from xtractmime import extract_mime
>>> body = b'Sample text content'
>>> content_types = (b'text/html',)
>>> extract_mime(body, no_sniff=False)
b'text/plain'
>>> extract_mime(body, content_types=content_types, no_sniff=True)
b'text/html'
>>> 
```
