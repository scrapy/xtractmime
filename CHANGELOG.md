# Changelog

## 0.2.1 (2024-01-16)

A specified content type is now ignored if it is not a valid MIME type.

## 0.2.0 (2023-08-31)

Dropped Python 3.6 support, added official Python 3.10, 3.11 and PyPy support.

A specified content type is no longer ignored for being a variant of
`plain/text`, unless it is one of the 4 specific variants affected by the old
Apache bug [13986](https://bz.apache.org/bugzilla/show_bug.cgi?id=13986).

## 0.1.0 (2022-06-21)

Initial release.
