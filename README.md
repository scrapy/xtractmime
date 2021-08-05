# xtractmime

`xtractmime` is a [BSD-licensed](https://opensource.org/licenses/BSD-3-Clause)
Python 3.6+ implementation of the [MIME Sniffing
Standard](https://mimesniff.spec.whatwg.org/).

Install from [`PyPI`](https://pypi.python.org/pypi/xtractmime):

```
pip install xtractmime
```

---

## Basic usage

Below mentioned are some simple examples of using `xtractmime.extract_mime`:

```python
>>> from xtractmime import extract_mime
>>> extract_mime(b'Sample text content')
b'text/plain'
>>> extract_mime(b'', content_types=(b'text/html',))
b'text/html'
```

Additional functionality to check if a MIME type belongs to a specific MIME type group using 
methods mentioned in `xtractmime.mimegroups`:

```python
>>> from xtractmime.mimegroups import is_html_mime_type, is_image_mime_type
>>> mime_type = b'text/html'
>>> is_html_mime_type(mime_type)
True
>>> is_image_mime_type(mime_type)
False
```

---

## API Reference

### function `xtractmime.extract_mime : Optional[bytes]`

Return `mimetype` as a byte string if the byte sequence in the provided content is recognized by `xtractmime`
else return `None`

#### Parameters

* `body: bytes`
* `content_types: Optional[Tuple[bytes]], default = None`
* `http_origin: bool, default = True`
* `no_sniff: bool, default = False`
* `extra_types: Optional[Tuple[Tuple[bytes, bytes, Optional[Set[bytes]], bytes], ...]], default = None`
* `supported_types: Set[bytes], default = None`

Optional `content_types` argument is a tuple of mime types suitable for using as a `Content-Type` header.
For the cases where the format of the content is unrecognizalble for `xtractmime`, it will return
the last mime type in the provided tuple of mime types.

**Example**

```python
>>> from xtractmime import extract_mime
>>> content_types = (b'text/xml',)
>>> body = b''
>>> extract_mime(body, content_types=content_types)
b'text/xml'
>>> 
```

Optional `http_origin` argument is a flag to determine if the resource is retrieved via HTTP or not.
`http_origin` is *`True`* (by default) for HTTP responses else *`False`*.

**Example**

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

**Example**

```python
>>> from xtractmime import extract_mime
>>> body = b"""<?xml version="1.0" encoding="utf-8"?>
                        <rdf:RDF
                          xmlns:content="http://purl.org/rss/1.0/modules/content/"
                          xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
                          xmlns="http://purl.org/rss/1.0/"
                        >
                        </rdf:RDF>"""
>>> content_types = (b'text/html',)
>>> extract_mime(body, content_types=content_types, no_sniff=False)
b'application/rss+xml'
>>> extract_mime(body, content_types=content_types, no_sniff=True)
b'text/html'
>>>
```
