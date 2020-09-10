#!/usr/bin/env python3

# Required imports
from functools import partial

# The key with which the sound files are encoded (XORed)
KEY = bytes([0x51, 0x23, 0x98, 0x56])

# Length of the key, in bytes
KEY_LENGTH = len(KEY)

# The default chunk size for reading/writing files
DEFAULT_CHUNK_SIZE = (1024 * 1024)

# Returns <value> if <value> is not None, <default_value> otherwise
def value_with_default(value, default_value):
	return (value if (value is not None) else default_value)

# Generator function that reads binary file <input_file> and yields chunks of size <chunk_size> (default: DEFAULT_CHUNK_SIZE)
def read_binary_file_in_chunks(input_file, chunk_size=None):
	chunk_size = value_with_default(chunk_size, DEFAULT_CHUNK_SIZE)
	for chunk in iter(partial(input_file.read, chunk_size), b''):
		yield chunk

# Generator function that encodes or decodes binary chunks from the iterator <chunks_iterator>
def encode_or_decode_chunks(chunks_iterator):
	offset = 0
	for chunk in chunks_iterator:
		chunk_length = len(chunk)
		yield bytes((chunk[chunk_byte_index] ^ KEY[(offset + chunk_byte_index) % KEY_LENGTH]) for chunk_byte_index in range(chunk_length))
		offset += chunk_length

# Encodes or decodes the Audio-Cube sound file <input_file> and writes the output to file <output_file>
def encode_or_decode_file(input_file, output_file, chunk_size=None):
	for transformed_chunk in encode_or_decode_chunks(read_binary_file_in_chunks(input_file=input_file, chunk_size=chunk_size)):
		output_file.write(transformed_chunk)

# ----
# MAIN
# ----
if __name__ == '__main__':
	import argparse
	argument_parser = argparse.ArgumentParser(
		description = 'En-/Decode Audio-Cube sound files',
		formatter_class = argparse.ArgumentDefaultsHelpFormatter,
	)
	argument_parser.add_argument(
		'input_file',
		type = argparse.FileType('rb'),
		help = 'The input file name/path (or "-" for STDIN)',
	)
	argument_parser.add_argument(
		'output_file',
		type = argparse.FileType('wb'),
		help = 'The output file name/path (or "-" for STDOUT)',
	)
	arguments = argument_parser.parse_args()

	encode_or_decode_file(
		input_file=arguments.input_file,
		output_file=arguments.output_file,
	)
