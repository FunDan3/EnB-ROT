#! /usr/bin/python3
import argparse, os, shutil, sys, colorama
sys.path.append("..") # so that guess_tools may be imported
import guess_tools
script_dir = os.path.dirname(os.path.abspath(__file__))

def normalize_shift(shift, alphabet):
	while shift >= len(alphabet):
		shift -= len(alphabet)
	while shift < 0:
		shift += len(alphabet)
	return shift

def main():
	print("Program is not optimized for huge files! If you have gigabytes of encrypted data... Why?")
	parser = argparse.ArgumentParser(
		prog = "D-ROT-bruteforce",
		description = "ROT decryption by bruteforce. Probably the most efficent unless alphabet has like 10k symbols\nDo chineese have 'alphabet'?")
	parser.add_argument("input_file", type = argparse.FileType("r"))
	parser.add_argument("output_file", type = argparse.FileType("w"))
	parser.add_argument("-l", "--language")
	args = parser.parse_args()
	if args.language == None:
		args.language = "english"
		print(f"No language specified. Default selected: {args.language}")
	args.language = args.language.lower()
	alphabet_path = os.path.dirname(os.path.dirname(script_dir))+"/alphabets/"+args.language
	dictionary_path = os.path.dirname(os.path.dirname(script_dir))+"/dictionaries/"+args.language
	if not os.path.exists(alphabet_path):
		print("No such alphabet '{args.language}'. At path {alphabet_path}")
		return
	if not os.path.exists(dictionary_path):
		print("No such dictionary '{args.language}'. At path {dictionary_path}")
		return
	with open(alphabet_path) as f:
		alphabet = f.read().replace("\n", "")
	with open(dictionary_path) as f:
		dictionary = f.read().split("\n")
	print(f"Loaded alphabet: {alphabet}")
	print(f"Loaded {args.language} dictionary. It has {'{:,}'.format(len(dictionary))} words")
	ciphertext = args.input_file.read()
	potential_solutions = []
	term_columns, term_rows = shutil.get_terminal_size()
	for shift in range(1, len(alphabet)):
		potential_solution = []
		for input_character in ciphertext:
			if input_character.lower() not in alphabet:
				potential_solution.append(input_character)
				continue
			character = alphabet[normalize_shift(alphabet.index(input_character.lower())-shift, alphabet)]
			if input_character.isupper():
				character = character.upper()
			potential_solution.append(character)
		potential_solutions.append({
			"content": "".join(potential_solution),
			"content_colored": None,
			"shift": shift,
			"correct_letters_percent": None,
		})
	for potential_solution in potential_solutions:
		potential_solution = guess_tools.guess_solution(potential_solution, dictionary, alphabet)
	potential_solutions.sort(key = lambda solution: solution["correct_letters_percent"], reverse = True)
	correct_shifts = []
	for potential_solution in potential_solutions:
		if potential_solution["correct_letters_percent"] == 0:
			break
		correct_shifts.append(potential_solution["shift"])
		pre_content = f"{potential_solution['shift']} -> "
		post_content = f"... {round(potential_solution['correct_letters_percent'], 2)}%"
		left_characters = term_columns - len(pre_content) - len(post_content)
		content = ""
		for character in potential_solution["content_colored"].replace("\n", " ").replace("\t", " "):
			if left_characters == 0:
				break
			content += character
			if character not in colorama.Style.RESET_ALL+colorama.Fore.LIGHTGREEN_EX+colorama.Fore.LIGHTRED_EX:
				left_characters-=1
		print(pre_content + content + colorama.Style.RESET_ALL + post_content)
	print("Select one of those shifts to save decrypted data")
	chosen_shift = None
	while True:
		try:
			chosen_shift = int(input("Shift: "))
			if chosen_shift not in correct_shifts:
				print("No such shift in potential solutions!")
			else:
				break
		except ValueError:
			print("Not a number!")
	solution = list(filter(lambda potential_solution: potential_solution["shift"]==chosen_shift, potential_solutions))[0]
	args.output_file.write(solution["content"])
	print(solution["content_colored"])
if __name__ == "__main__":
	main()
