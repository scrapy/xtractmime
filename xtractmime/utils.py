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
	numbersize = 1

	while numbersize < max_vint_size and numbersize < input_size:
		if input_bytes[index] & mask != 0:
			break
		mask = mask >> 1
		numbersize += 1

	return numbersize


def _is_webm_signature(input_bytes):
	input_size = len(input_bytes)
	if input_size < 4:
		return False

	if input_bytes[0:4] != b"\x1aE\xdf\xa3":
		return False

	Iter = 4

	while Iter < input_size and Iter < 38:
		if input_bytes[Iter:Iter+2] == b"B\x82":
			Iter += 2

			if Iter >= input_size:
				break
			
			numbersize = parse_vint(input_bytes, input_size, Iter)
			Iter += numbersize

			if Iter >= input_size - 4:
				break

			if input_bytes[Iter:Iter+4] == b"webm":
				return True
		Iter += 1

	return False
