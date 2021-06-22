
IMAGE_PATTERNS = (
	(b"\x00\x00\x01\x00",b"\xff\xff\xff\xff","image/x-icon"), # A Windows Icon signature
	(b"\x00\x00\x02\x00",b"\xff\xff\xff\xff","image/x-icon"), # A Windows Cursor signature
	(b"BM",b"\xff\xff","image/bmp"), # The string "BM", a BMP signature
	(b"GIF87a",b"\xff\xff\xff\xff\xff\xff","image/gif"), # The string "GIF87a", a GIF signature
	(b"GIF89a",b"\xff\xff\xff\xff\xff\xff","image/gif"), # The string "GIF89a", a GIF signature
	(b"RIFF\x00\x00\x00\x00WEBPVP",b"\xff\xff\xff\xff\x00\x00\x00\x00\xff\xff\xff\xff\xff\xff","image/webp"), # The string "RIFF" followed by four bytes followed by the string "WEBPVP"
	(b"\x89PNG\r\n\x1a\n",b"\xff\xff\xff\xff\xff\xff\xff\xff","image/png"), # An error-checking byte followed by the string "PNG" followed by CR LF SUB LF, the PNG signature
	(b"\xff\xd8\xff",b"\xff\xff\xff","image/jpeg") # The JPEG Start of Image marker followed by the indicator byte of another marker
)

AUDIO_VIDEO_PATTERNS = (
    (b".snd",b"\xff\xff\xff\xff","audio/basic"), # The string ".snd", the basic audio signature
    (b"FORM\x00\x00\x00\x00AIFF",b"\xff\xff\xff\xff\x00\x00\x00\x00\xff\xff\xff\xff","audio/aiff"), # The string "FORM" followed by four bytes followed by the string "AIFF", the AIFF signature
    (b"ID3",b"\xff\xff\xff","audio/mpeg"), # The string "ID3", the ID3v2-tagged MP3 signature
    (b"OggS\x00",b"\xff\xff\xff\xff\xff","application/ogg"), # The string "OggS" followed by NUL, the Ogg container signature
    (b"MThd\x00\x00\x00\x06",b"\xff\xff\xff\xff\xff\xff\xff\xff","audio/midi"), # The string "MThd" followed by four bytes representing the number 6 in 32 bits (big-endian), the MIDI signature
    (b"RIFF\x00\x00\x00\x00AVI ",b"\xff\xff\xff\xff\x00\x00\x00\x00\xff\xff\xff\xff","video/avi"), # The string "RIFF" followed by four bytes followed by the string "AVI ", the AVI signature
    (b"RIFF\x00\x00\x00\x00WAVE",b"\xff\xff\xff\xff\x00\x00\x00\x00\xff\xff\xff\xff","audio/wave") # The string "RIFF" followed by four bytes followed by the string "WAVE", the WAVE signature
)

FONT_PATTERNS = (
    (b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00LP",b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff"
,"application/vnd.ms-fontobject"), # 34 bytes followed by the string "LP", the Embedded OpenType signature
    (b"\x00\x01\x00\x00",b"\xff\xff\xff\xff","font/ttf"), # 4 bytes representing the version number 1.0, a TrueType signature
    (b"OTTO",b"\xff\xff\xff\xff","font/otf"), # The string "OTTO", the OpenType signature
    (b"ttcf",b"\xff\xff\xff\xff","font/collection"), # The string "ttcf", the TrueType Collection signature
    (b"wOFF",b"\xff\xff\xff\xff","font/woff"), # The string "wOFF", the Web Open Font Format 1.0 signature
    (b"wOF2",b"\xff\xff\xff\xff","font/woff2") # The string "wOF2", the Web Open Font Format 2.0 signature
)

ARCHIVE_PATTERNS = (
    (b"\x1f\x8b\x08",b"\xff\xff\xff","application/x-gzip"), # The GZIP archive signature
    (b"PK\x03\x04",b"\xff\xff\xff\xff","application/zip"), # The string "PK" followed by ETX EOT, the ZIP archive signature
    (b"Rar \x1a\x07\x00",b"\xff\xff\xff\xff\xff\xff\xff","application/x-rar-compressed") # The string "Rar " followed by SUB BEL NUL, the RAR archive signature
)
