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

Return the [MIME type essence](https://mimesniff.spec.whatwg.org/#mime-type-essence) (e.g. `text/html`) matching the input data, or 
`None` if no match can be found.

The `body` parameter is the byte sequence of which MIME type is to be determined. `xtractmime` only consider first few
bytes of the `body` and the specific number of bytes read is defined in the `xtractmime.RESOURCE_HEADER_BUFFER_LENGTH` constant.

Optional `content_types` argument is a tuple of mime types suitable for using as a `Content-Type` header.
For the cases where the format of the content is unrecognizable for `xtractmime`, it will return
the last mime type in the provided tuple of mime types.

Optional `http_origin` argument is a flag to determine if the resource is retrieved via HTTP or not.
`http_origin` is *`True`* (by default) for HTTP responses else *`False`*.

Optional `no_sniff` argument is a flag which is *`True`* if the user agent does not wish to
perform sniffing on the resource and *`False`* (by default) otherwise. Users may want to set
this parameter to *`True`* if the [`X-Content-Type-Options`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Content-Type-Options) response header is set to `nosniff`. For more info, please refer [here](https://mimesniff.spec.whatwg.org/#no-sniff-flag).

Optional `supported_types` argument is a set of all [MIME types supported by user agent](https://mimesniff.spec.whatwg.org/#supported-by-the-user-agent) and if `supported_types` is not
specified, all MIME types are assumed to be supported. Using this parameter can improve the performance of `xtractmime`.

Optional `extra_types` argument is a tuple which users may implicitly pass to `xtractmime` for considering additional MIME types
in determining the MIME type of the provided content. Each entry in the tuple should follow the format
**(Byte Pattern, Pattern Mask, Leading Bytes, MIME type)**. 

* **Byte Pattern** is a byte sequence used as a template to be matched against in the pattern matching algorithm. 
* **Pattern Mask** is a byte sequence used to determine the significance of bytes being compared against a byte pattern in the pattern matching algorithm.

---
**NOTE**

In a **Pattern Mask**, `b"\xff"` indicates the byte is strictly significant, `b"\xdf"` indicates that the byte is significant in an ASCII case-insensitive way, and `b"\x00"` indicates that the byte is not significant. 

---
* **Leading Bytes** is a set of bytes to be ignored while matching the leading bytes in the content.
* **MIME type** should be returned if the pattern matches.

**Sample `extra_types`:**
```python
extra_types = ((b'test', b'\xff\xff\xff\xff', None, b'text/test'),...)
```

---
**NOTE**

*`xtractmime` apply some [restrictions](https://mimesniff.spec.whatwg.org/#ref-for-mime-type%E2%91%A1%E2%91%A8) to the additional MIME types for security reasons i.e. users should not implicitly include additional byte patterns for any MIME type already present in 
`xtractmime`, as doing so could introduce privilege escalation vulnerabilities.*
---

### function `xtractmime.is_binary_data(input_bytes: bytes) -> bool`

Return *`True`* if the provided byte sequence contains any binary data bytes else *`False`*
 
### MIME type group functions

The following functions return `True` if a given MIME type belongs to a certain 
[MIME type group](https://mimesniff.spec.whatwg.org/#mime-type-groups), or 
`False` otherwise:
```
xtractmime.mimegroups.is_image_mime_type(mime_type: bytes) -> bool
xtractmime.mimegroups.is_audio_video_mime_type(mime_type: bytes) -> bool
xtractmime.mimegroups.is_font_mime_type(mime_type: bytes) -> bool
xtractmime.mimegroups.is_zip_mime_type(mime_type: bytes) -> bool
xtractmime.mimegroups.is_archive_mime_type(mime_type: bytes) -> bool
xtractmime.mimegroups.is_xml_mime_type(mime_type: bytes) -> bool
xtractmime.mimegroups.is_html_mime_type(mime_type: bytes) -> bool
xtractmime.mimegroups.is_scriptable_mime_type(mime_type: bytes) -> bool
xtractmime.mimegroups.is_javascript_mime_type(mime_type: bytes) -> bool
xtractmime.mimegroups.is_json_mime_type(mime_type: bytes) -> bool
```
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
