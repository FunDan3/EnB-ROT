#! /usr/bin/python3
import argparse, os
script_dir = os.path.dirname(os.path.abspath(__file__))
buffer_size = 1024

def normalize_shift(shift, alphabet):
	while shift >= len(alphabet):
		shift -= len(alphabet)
	return shift
def main():
	parser = argparse.ArgumentParser(
		prog = "E-ROT",
		description = "ROT encryption. Nothing really special. Misses some features but this will do for showcasing the break.\nAs if its that hard to break it...")
	parser.add_argument("input_file", type = argparse.FileType("r"))
	parser.add_argument("output_file", type = argparse.FileType("w"))
	parser.add_argument("-s", "--shift", type = int)
	parser.add_argument("-a", "--alphabet")
	args = parser.parse_args()
	if args.alphabet == None:
		args.alphabet = "english"
	args.alphabet = args.alphabet.lower()
	alphabet_path = os.path.dirname(script_dir)+"/alphabets/"+args.alphabet
	if not os.path.exists(alphabet_path):
		print("No such alphabet '{args.alphabet}'. At path {alphabet_path}")
		return
	with open(alphabet_path) as f:
		alphabet = f.read().replace("\n", "")
	print(f"Loaded alphabet: {alphabet}")
	shift = normalize_shift(args.shift, alphabet)
	if shift == 0:
		print("Program execution stopped: shift is zero or is a multiple of alphabet length, which will not result in any change to plaintext.")
		return
	if shift!=args.shift:
		print(f"Normalized shift {args.shift} to {shift} because it exeeds length of the alphabet ({len(alphabet)})")
	input_chunk = True
	while input_chunk:
		input_chunk = args.input_file.read(buffer_size)
		output_chunk = []
		for input_character in input_chunk:
			if input_character not in alphabet:
				output_chunk.append(input_character)
				continue
			output_chunk.append(alphabet[normalize_shift(alphabet.index(input_character)+shift, alphabet)])
		args.output_file.write("".join(output_chunk))
	print("Encryption compleate.")
if __name__ == "__main__":
	main()
