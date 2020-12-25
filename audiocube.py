#!/usr/bin/env python3

CHUNK_SIZE = 0x10000

def read_file_in_chunks(input_file):
	while True:
		chunk = input_file.read(CHUNK_SIZE)
		if (not chunk):
			break
		yield chunk

def convert_file(input_file, output_file, convert_byte_function):
	offset = 0
	for input_file_chunk in read_file_in_chunks(input_file):
		output_file_chunk = bytearray()
		for input_byte in input_file_chunk:
			output_byte = convert_byte_function(input_byte, offset)
			output_file_chunk.append(output_byte)
			offset += 1
		output_file.write(output_file_chunk)

def convert_file_path(input_file_path, output_file_path, convert_byte_function):
	with open(input_file_path, 'rb') as input_file:
		with open(output_file_path, 'wb') as output_file:
			convert_file(input_file, output_file, convert_byte_function)

def convert_file_paths(input_file_paths, output_file_pattern, convert_byte_function):
	from os import path
	for input_file_path in input_file_paths:
		input_file_path_without_extension, input_file_extension = path.splitext(input_file_path)
		output_file_path = output_file_pattern.format(
			name = input_file_path_without_extension,
			extension = input_file_extension,
		)
		print(f'"{input_file_path}" -> "{output_file_path}"')
		convert_file_path(input_file_path, output_file_path, convert_byte_function)

def rotate_byte_left(byte, number_of_bits):
	number_of_bits = (number_of_bits % 8)
	return (byte if (number_of_bits == 0) else  (((byte << number_of_bits) | (byte >> (8 - number_of_bits))) & 0xFF))

def rotate_byte_right(byte, number_of_bits):
	return rotate_byte_left(byte, -number_of_bits)

def add_input_file_paths_argument(argument_parser):
	argument_parser.add_argument(
		'input_file_paths',
		metavar = 'input_file',
		nargs = '+',
		type = str,
		help = 'The input file(s) to read from',
	)

def add_output_file_pattern_argument(argument_parser, default_extension):
	argument_parser.add_argument(
		'--output_file_pattern', '-ofp',
		type = str,
		default = f'{{name}}{default_extension}',
		help = 'Pattern for the output filenames',
	)

class Device_Type:
	def __init__(self, id, name):
		self.id = id
		self.name = name
	def add_commands(self, command_subparsers):
		raise NotImplementedError('add_commands() not implemented')

class Encrypted_File_Device_Type(Device_Type):
	def __init__(self, id, name, encrypted_file_extension, decrypted_file_extension):
		super().__init__(id, name)
		self.encrypted_file_extension = encrypted_file_extension
		self.decrypted_file_extension = decrypted_file_extension
	def encrypt_byte(self, input_byte, offset):
		raise NotImplementedError('encrypt_byte() not implemented')
	def encrypt(self, args):
		convert_file_paths(args.input_file_paths, args.output_file_pattern, self.encrypt_byte)
	def decrypt_byte(self, input_byte, offset):
		raise NotImplementedError('decrypt_byte() not implemented')
	def decrypt(self, args):
		convert_file_paths(args.input_file_paths, args.output_file_pattern, self.decrypt_byte)
	def add_commands(self, command_subparsers):
		encrypt_argument_parser = command_subparsers.add_parser(
			'encrypt',
			description = f'Encrypt audio file(s)',
			formatter_class = ArgumentDefaultsHelpFormatter,
		)
		add_input_file_paths_argument(encrypt_argument_parser)
		add_output_file_pattern_argument(encrypt_argument_parser, self.encrypted_file_extension)
		encrypt_argument_parser.set_defaults(func=self.encrypt)
		decrypt_argument_parser = command_subparsers.add_parser(
			'decrypt',
			description = f'Decrypt audio file(s)',
			formatter_class = ArgumentDefaultsHelpFormatter,
		)
		add_input_file_paths_argument(decrypt_argument_parser)
		add_output_file_pattern_argument(decrypt_argument_parser, self.decrypted_file_extension)
		decrypt_argument_parser.set_defaults(func=self.decrypt)

class Simple_Encrypted_File_Device_Type(Encrypted_File_Device_Type):
	def __init__(self, id, name, encrypted_file_extension, decrypted_file_extension, xor_key, rotate_bits):
		super().__init__(id, name, encrypted_file_extension, decrypted_file_extension)
		self.xor_key = bytes(xor_key)
		self.rotate_bits = rotate_bits
		self.xor_key_length = len(xor_key)
	def encrypt_byte(self, input_byte, offset):
		return (rotate_byte_right(input_byte, self.rotate_bits) ^ self.xor_key[offset % self.xor_key_length])
	def decrypt_byte(self, input_byte, offset):
		return rotate_byte_left((input_byte ^ self.xor_key[offset % self.xor_key_length]), self.rotate_bits)

class Audiocube(Simple_Encrypted_File_Device_Type):
	def __init__(self):
		super().__init__('audiocube', 'Audiocube', '.SMP', '.mp3', [0x51, 0x23, 0x98, 0x56], 0)

class LIDL_Storyland(Simple_Encrypted_File_Device_Type):
	def __init__(self):
		super().__init__('storyland', 'LIDL Storyland', '.SMP', '.mp3', [0x01, 0x80, 0x04, 0x04], 3)

class Migros_Storybox(Simple_Encrypted_File_Device_Type):
	def __init__(self):
		super().__init__('storybox', 'Migros Storybox', '.smp', '.mp3', [0x66], 0)

DEVICE_TYPES = [
	Audiocube(),
	LIDL_Storyland(),
	Migros_Storybox(),
]

# ----
# MAIN
# ----
if __name__ == '__main__':
	from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
	argument_parser = ArgumentParser(
		description = 'Toolbox for Audio-Cubes. For more information, see https://github.com/oyooyo/audiocube',
		formatter_class = ArgumentDefaultsHelpFormatter,
	)
	device_type_subparsers = argument_parser.add_subparsers(
		required = True,
		dest = 'device_type',
		help = 'The device type',
	)
	for device_type in DEVICE_TYPES:
		device_type_argument_parser = device_type_subparsers.add_parser(
			device_type.id,
			description = f'Toolbox for "{device_type.name}"',
			formatter_class = ArgumentDefaultsHelpFormatter,
		)
		device_type_command_subparsers = device_type_argument_parser.add_subparsers(
			required = True,
			dest = 'command',
			help = 'The command to execute',
		)
		device_type.add_commands(device_type_command_subparsers)
	args = argument_parser.parse_args()
	args.func(args)
