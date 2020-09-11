#!/usr/bin/env python3

# The key with which the sound files are encoded (XORed)
CRYPT_KEY = bytes([0x51, 0x23, 0x98, 0x56])

# Length of the key, in bytes
CRYPT_KEY_LENGTH = len(CRYPT_KEY)

# The default chunk size for reading/writing files
DEFAULT_CHUNK_SIZE = (1024 * 1024)

# The bytes in a Mifare Classic sector trailer block
SECTOR_TRAILER_BLOCK_BYTES = bytes([0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x07, 0x80, 0x69, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])

# The bytes in a Mifare Classic block that only contains zeros
ZERO_BLOCK_BYTES = bytes(16)

# The string to use for newlines
NEWLINE = '\n'

# Returns <value> if <value> is not None, <default_value> otherwise
def value_with_default(value, default_value):
	return (value if (value is not None) else default_value)

# Generator function that reads binary file <input_file> and yields chunks of size <chunk_size> (default: DEFAULT_CHUNK_SIZE)
def read_file_in_chunks(input_file, chunk_size=None):
	chunk_size = value_with_default(chunk_size, DEFAULT_CHUNK_SIZE)
	while True:
		chunk = input_file.read(chunk_size)
		if (not chunk):
			break
		yield chunk

# Generator function that encrypts or decrypts chunks from the iterator <chunks_iterator>
def crypt_chunks(chunks_iterator):
	offset = 0
	for chunk in chunks_iterator:
		yield bytes((chunk[chunk_byte_index] ^ CRYPT_KEY[(offset + chunk_byte_index) % CRYPT_KEY_LENGTH]) for chunk_byte_index in range(len(chunk)))
		offset += len(chunk)

# Encrypts or decrypts the sound file <input_file> and writes the output to file <output_file>
def crypt_file(input_file, output_file, chunk_size=None):
	for crypted_chunk in crypt_chunks(read_file_in_chunks(input_file=input_file, chunk_size=chunk_size)):
		output_file.write(crypted_chunk)

# Encrypts or decrypts a sound file
def crypt_file_command(args):
	crypt_file(input_file=args.input_file, output_file=args.output_file)

# Generator function that slices <sliceable> into equal-sized chunks of size <chunk_size>
def generate_chunks(sliceable, chunk_size):
	for index in range(0, len(sliceable), chunk_size):
		yield sliceable[index:(index + chunk_size)]

# Convert the content of a Mifare Classic NFC tag <nfc_bytes> into the content of a .mct file
def create_mct(nfc_bytes):
	return NEWLINE.join(f"+Sector: {sector_index}{NEWLINE}{NEWLINE.join(block_bytes.hex().upper() for block_bytes in generate_chunks(sector_bytes, 16))}" for sector_index, sector_bytes in enumerate(generate_chunks(nfc_bytes, 64)))

# Create the content of a Mifare Classic NFC tag for an audio file with directory ID <directory_id> and file ID <file_id>
def create_nfc_bytes(directory_id, file_id):
	id_block_bytes = bytes([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0x19, 0x01, 0x01, directory_id, (file_id >> 8), (file_id & 0xFF)])
	return (ZERO_BLOCK_BYTES + id_block_bytes + ZERO_BLOCK_BYTES + SECTOR_TRAILER_BLOCK_BYTES + id_block_bytes + ZERO_BLOCK_BYTES + ZERO_BLOCK_BYTES + SECTOR_TRAILER_BLOCK_BYTES)

# Create a Mifare Classic NFC tag content file
def nfc_content_command(args):
	nfc_bytes = create_nfc_bytes(directory_id=int(args.directory_id, 16), file_id=int(args.file_id, 16))
	args.output_file.write(create_mct(nfc_bytes))

# ----
# MAIN
# ----
if __name__ == '__main__':
	# Set up the argument parser
	import argparse
	argument_parser = argparse.ArgumentParser(
		description = 'Toolbox for Audio-Cube',
		formatter_class = argparse.ArgumentDefaultsHelpFormatter,
	)
	subparsers = argument_parser.add_subparsers(
		required = True,
		dest = 'action',
		help = 'The action to perform',
	)

	# Set up the "crypt_file" action/subcommand
	crypt_file_parser = subparsers.add_parser(
		'crypt_file',
		description = 'Encrypt/decrypt a sound file',
		formatter_class = argparse.ArgumentDefaultsHelpFormatter,
	)
	crypt_file_parser.add_argument(
		'input_file',
		type = argparse.FileType('rb'),
		help = 'the input file to read from ("-" for STDIN)',
	)
	crypt_file_parser.add_argument(
		'output_file',
		type = argparse.FileType('wb'),
		help = 'the output file to write to ("-" for STDOUT)',
	)
	crypt_file_parser.set_defaults(func=crypt_file_command)

	# Set up the "nfc_content" action/subcommand
	nfc_content = subparsers.add_parser(
		'nfc_content',
		description = 'Generate a .mct NFC tag content file',
		formatter_class = argparse.ArgumentDefaultsHelpFormatter,
	)
	nfc_content.add_argument(
		'directory_id',
		type = str,
		nargs = '?',
		default = '01',
		help = 'The directory ID, a hexadecimal string in range 00...FF',
	)
	nfc_content.add_argument(
		'file_id',
		type = str,
		help = 'The file ID, a hexadecimal string in range 0000...FFFF',
	)
	nfc_content.add_argument(
		'output_file',
		type = argparse.FileType('w'),
		help = 'the output file to write to ("-" for STDOUT)',
	)
	nfc_content.set_defaults(func=nfc_content_command)

	# Parse the arguments
	args = argument_parser.parse_args()
	# If there was no error parsing the arguments, perform the chosen action/subcommand
	args.func(args)
