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
**Parameters:**

* `body: bytes`
* `content_types: Optional[Tuple[bytes]], default = None`
* `http_origin: bool, default = True`
* `no_sniff: bool, default = False`
* `extra_types: Optional[Tuple[Tuple[bytes, bytes, Optional[Set[bytes]], bytes], ...]], default = None`
* `supported_types: Set[bytes], default = None`

Return the [MIME type essence](https://mimesniff.spec.whatwg.org/#mime-type-essence) (e.g. `text/html`) if the byte sequence 
in the provided content is recognized by `xtractmime` else return `None`


Optional `content_types` argument is a tuple of mime types suitable for using as a `Content-Type` header.
For the cases where the format of the content is unrecognizalble for `xtractmime`, it will return
the last mime type in the provided tuple of mime types.

**Example using `content_types` argument:**

```python
>>> from xtractmime import extract_mime
>>> content_types = (b'text/xml',)
>>> body = b''
>>> extract_mime(body, content_types=content_types)
b'text/xml'
```

Optional `http_origin` argument is a flag to determine if the resource is retrieved via HTTP or not.
`http_origin` is *`True`* (by default) for HTTP responses else *`False`*.

**Example using `http_origin` argument:**

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

**Example using `no_sniff` argument:**

```python
>>> from xtractmime import extract_mime
>>> body = b'''<?xml version="1.0" encoding="utf-8"?>
                        <rdf:RDF
                          xmlns:content="http://purl.org/rss/1.0/modules/content/"
                          xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
                          xmlns="http://purl.org/rss/1.0/"
                        >
                        </rdf:RDF>'''
>>> content_types = (b'text/html',)
>>> extract_mime(body, content_types=content_types, no_sniff=False)
b'application/rss+xml'
>>> extract_mime(body, content_types=content_types, no_sniff=True)
b'text/html'
```

Optional `extra_types` argument is a tuple which users may implicitly pass to `xtractmime` for considering additional MIME types
in determining the MIME type of the provided content. Each entry in the tuple should follow the format
**(Byte Pattern, Pattern Mask, Leading Bytes, MIME type)**

* **Byte Pattern** is a byte sequence used as a template to be matched against in the pattern matching algorithm. 
* **Pattern Mask** is a byte sequence used to determine the significance of bytes being compared against a byte pattern in the pattern matching algorithm.
* **Leading Bytes** is set of bytes to be ignored while matching the leading bytes in the content.

---
**NOTE**

In a pattern mask, `0xFF` indicates the byte is strictly significant, `OxDF` indicates that the byte is significant in an ASCII case-insensitive way, and 0x00 indicates that the byte is not significant. 

---

**Example using `extra_types` argument:**
```python
>>> from xtractmime import extract_mime
>>> extra_types = ((b'test', b'\xff\xff\xff\xff', None, b'text/test'),)
>>> extract_mime(b'test', extra_types=extra_types)
b'text/test'
>>> extract_mime(b"test")
b'text/plain'
```

Optional `supported_types` argument is a set of MIME types that are supported by the user agent.

**Example using `supported_types` argument:**
```python
>>> from xtractmime import extract_mime
>>> content_types = (b'image/gif',)
>>> supported_types = (b'image/gif',)
>>> extract_mime(b'GIF87a', content_types=content_types, supported_types=supported_types)
b'image/gif'
>>> supported_types = (b'audio/mpeg',)
>>> extract_mime(b'GIF87a', content_types=content_types, supported_types=supported_types)
b'image/gif'
```

### function `xtractmime._find_unknown_mimetype : Optional[bytes]`
**Parameters:**

* `input_bytes: bytes`
* `sniff_scriptable: bool`
* `extra_types: Optional[Tuple[Tuple[bytes, bytes, Optional[Set[bytes]], bytes], ...]]`

Return a recognized MIME type essence if the format of the content is identified else return a binary MIME type essence. The function is called by `xtractmime.extract_mime` when *Content-Type* headers are unknown (i.e. `content_types` argument is `None`)

### function `xtractmime._sniff_mislabled_binary : Optional[bytes]`
**Parameters:**

* `input_bytes: bytes`

Return a text or a binary MIME type essence. The function determines whether a binary resource has been mislabeled as plain text.
The function is related to a bug in some older installations of *Apache* that causes the provided byte sequences to supply
one of the *Content-Type* headers mentioned in [Section 5.1](https://mimesniff.spec.whatwg.org/commit-snapshots/609a3a3c935fbb805b46cf3d90768d695a1dcff2/#interpreting-the-resource-metadata) of MIME sniffing standards when serving files with unrecognized MIME types.

### function `xtractmime._sniff_mislabled_feed : Optional[bytes]:`
**Parameters:**

* `input_bytes: bytes`
* `supplied_type: bytes`

Return a MIME type essence if the content is identified as a XML-based RSS feed or an Atom feed else return supplied MIME type. The function determines whether a feed has been mislabeled as HTML.

### MIME group functions

These functions provide an additional functionality to determine whether a MIME type belongs to a specific MIME type group or not.
Supported MIME type groups include *Image MIME type*, *Audio or Video MIME type*, *Font MIME type*, *ZIP-Based MIME type*, *Archive MIME type*, *XML MIME type*, *HTML MIME type*, *Scriptable MIME type* (includes *XML MIME type*, *HTML MIME type*, or any MIME type whose essence is "application/pdf"), *JavaScript MIME type*, *JSON MIME type*.

**List of available functions:**

* `xtractmime.mimegroups.is_image_mime_type(mime_type: bytes) -> bool`
* `xtractmime.mimegroups.is_audio_video_mime_type(mime_type: bytes) -> bool`
* `xtractmime.mimegroups.is_font_mime_type(mime_type: bytes) -> bool`
* `xtractmime.mimegroups.is_zip_mime_type(mime_type: bytes) -> bool`
* `xtractmime.mimegroups.is_archive_mime_type(mime_type: bytes) -> bool`
* `xtractmime.mimegroups.is_xml_mime_type(mime_type: bytes) -> bool`
* `xtractmime.mimegroups.is_html_mime_type(mime_type: bytes) -> bool`
* `xtractmime.mimegroups.is_scriptable_mime_type(mime_type: bytes) -> bool`
* `xtractmime.mimegroups.is_javascript_mime_type(mime_type: bytes) -> bool`
* `xtractmime.mimegroups.is_json_mime_type(mime_type: bytes) -> bool`

**Example**
```python
>>> from xtractmime.mimegroups import is_html_mime_type, is_image_mime_type, is_zip_mime_type
>>> mime_type = b'text/html'
>>> is_html_mime_type(mime_type)
True
>>> is_image_mime_type(mime_type)
False
>>> is_zip_mime_type(mime_type)
False
```