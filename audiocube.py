#!/usr/bin/env python3

CHUNK_SIZE = 0x10000

def value_with_default(value, default_value):
	return (value if (value != None) else default_value)

def read_file_in_chunks(input_file):
	while True:
		chunk = input_file.read(CHUNK_SIZE)
		if (not chunk):
			break
		yield chunk

def convert_file(input_file, output_file, convert_chunk_function):
	offset = 0
	for input_file_chunk in read_file_in_chunks(input_file):
		output_file_chunk = bytearray(len(input_file_chunk))
		convert_chunk_function(input_file_chunk, output_file_chunk, offset)
		output_file.write(output_file_chunk)
		offset += len(input_file_chunk)

def convert_file_path(input_file_path, output_file_path, convert_chunk_function):
	with open(input_file_path, 'rb') as input_file:
		with open(output_file_path, 'wb') as output_file:
			convert_file(input_file, output_file, convert_chunk_function)

def convert_file_paths(input_file_paths, output_file_pattern, convert_chunk_function):
	from os import path
	for input_file_path in input_file_paths:
		input_file_path_without_extension, input_file_extension = path.splitext(input_file_path)
		output_file_path = output_file_pattern.format(
			name = input_file_path_without_extension,
			extension = input_file_extension,
		)
		print('"{input_file_path}" -> "{output_file_path}"... '.format(
			input_file_path = input_file_path,
			output_file_path = output_file_path,
		))
		convert_file_path(input_file_path, output_file_path, convert_chunk_function)

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
		default = '{{name}}{default_extension}'.format(
			default_extension = default_extension,
		),
		help = 'Pattern for the output filenames',
	)

class Device_Type:
	def __init__(self, id, name):
		self.id = id
		self.name = name
	def add_commands(self, command_subparsers):
		raise NotImplementedError('add_commands() not implemented')

class Encrypted_File_Device_Type(Device_Type):
	def __init__(self, id, name, encrypted_file_extension=None, decrypted_file_extension=None):
		super().__init__(id, name)
		self.encrypted_file_extension = value_with_default(encrypted_file_extension, '.SMP')
		self.decrypted_file_extension = value_with_default(decrypted_file_extension, '.mp3')
	def add_commands(self, command_subparsers):
		encrypt_argument_parser = command_subparsers.add_parser(
			'encrypt',
			description = 'Encrypt audio file(s)',
			formatter_class = ArgumentDefaultsHelpFormatter,
		)
		add_input_file_paths_argument(encrypt_argument_parser)
		add_output_file_pattern_argument(encrypt_argument_parser, self.encrypted_file_extension)
		encrypt_argument_parser.set_defaults(func=self.encrypt)
		decrypt_argument_parser = command_subparsers.add_parser(
			'decrypt',
			description = 'Decrypt audio file(s)',
			formatter_class = ArgumentDefaultsHelpFormatter,
		)
		add_input_file_paths_argument(decrypt_argument_parser)
		add_output_file_pattern_argument(decrypt_argument_parser, self.decrypted_file_extension)
		decrypt_argument_parser.set_defaults(func=self.decrypt)
	def encrypt_chunk(self, input_chunk, output_chunk, offset):
		raise NotImplementedError('encrypt_chunk() not implemented')
	def encrypt(self, args):
		convert_file_paths(args.input_file_paths, args.output_file_pattern, self.encrypt_chunk)
		#import cProfile
		#input_file_paths = args.input_file_paths
		#output_file_paths = args.output_file_pattern
		#encrypt_chunk = self.encrypt_chunk
		#cProfile.run('convert_file_paths(input_file_paths, output_file_pattern, encrypt_chunk)')
	def decrypt_chunk(self, input_chunk, output_chunk, offset):
		raise NotImplementedError('decrypt_chunk() not implemented')
	def decrypt(self, args):
		convert_file_paths(args.input_file_paths, args.output_file_pattern, self.decrypt_chunk)

class Simple_Encrypted_File_Device_Type(Encrypted_File_Device_Type):
	def __init__(self, id, name, xor_key, rotate_bits=None, encrypted_file_extension=None, decrypted_file_extension=None):
		super().__init__(id, name, encrypted_file_extension, decrypted_file_extension)
		self.xor_key = bytes(xor_key)
		self.rotate_bits = (value_with_default(rotate_bits, 0) % 8)
	def encrypt_chunk(self, input_chunk, output_chunk, offset):
		xor_key = self.xor_key
		xor_key_length = len(xor_key)
		rotate_bits = self.rotate_bits
		index = (len(input_chunk) - 1)
		while (index >= 0):
			output_byte = input_chunk[index]
			if (rotate_bits != 0):
				output_byte = (((output_byte >> rotate_bits) | (output_byte << (8 - rotate_bits))) & 0xFF)
			output_chunk[index] = (output_byte ^ xor_key[(offset + index) % xor_key_length])
			index -= 1
	def decrypt_chunk(self, input_chunk, output_chunk, offset):
		xor_key = self.xor_key
		xor_key_length = len(xor_key)
		rotate_bits = self.rotate_bits
		index = (len(input_chunk) - 1)
		while (index >= 0):
			output_byte = (input_chunk[index] ^ xor_key[(offset + index) % xor_key_length])
			if (rotate_bits != 0):
				output_byte = (((output_byte << rotate_bits) | (output_byte >> (8 - rotate_bits))) & 0xFF)
			output_chunk[index] = output_byte
			index -= 1

class Audiocube(Simple_Encrypted_File_Device_Type):
	def __init__(self):
		super().__init__('audiocube', 'Audiocube', [0x51, 0x23, 0x98, 0x56], 0, '.SMP', '.mp3')

class LIDL_Storyland(Simple_Encrypted_File_Device_Type):
	def __init__(self):
		super().__init__('storyland', 'LIDL Storyland', [0x01, 0x80, 0x04, 0x04], 3, '.SMP', '.mp3')

class Migros_Storybox(Simple_Encrypted_File_Device_Type):
	def __init__(self):
		super().__init__('storybox', 'Migros Storybox', [0x66], 0, '.smp', '.mp3')

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
			description = 'Toolbox for "{device_type_name}"'.format(
				device_type_name = device_type.name,
			),
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
