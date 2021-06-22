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
		bytes_read += 4

	return False


def parse_vint(input_bytes, input_size, index):
	mask = 128
	max_vint_size = 8
	number_size = 1

	while number_size < max_vint_size and number_size < input_size:
		if input_bytes[index] & mask != 0:
			break
		mask = mask >> 1
		number_size += 1

	return number_size


def _is_webm_signature(input_bytes):
	input_size = len(input_bytes)
	if input_size < 4:
		return False

	if input_bytes[0:4] != b"\x1aE\xdf\xa3":
		return False

	index = 4

	while index < input_size and index < 38:
		if input_bytes[index:index+2] == b"B\x82":
			index += 2

			if index >= input_size:
				break
			
			number_size = parse_vint(input_bytes, input_size, index)
			index += number_size

			if index >= input_size - 4:
				break

			if input_bytes[index:index+4] == b"webm":
				return True
		index += 1

	return False
