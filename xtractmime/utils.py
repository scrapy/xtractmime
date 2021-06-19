from struct import unpack

def _is_mp4_signature(input_bytes):
	input_size = len(input_bytes)
	if input_size < 12:
		return False

	box_size = unpack(">I", input_bytes[0:4])[0]

	if (input_size < box_size) or (box_size % 4 != 0):
		return False

	if input_bytes[4:8] != b"ftyp":
		return False

	if input_bytes[8:11] == b"mp4":
		return True

	bytes_read = 16
	while bytes_read < box_size:
		if input_bytes[bytes_read:bytes_read+3] == b"mp4":
			return True
		bytes_read += 1

	return False



