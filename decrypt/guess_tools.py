import colorama
colorama.init()
def guess_solution(solution, dictionary, alphabet):
	data = solution["content"]
	incorrect_letters = 0
	correct_letters = 0
	words = []
	letter_sequence = data[0].lower() in alphabet #not separator really
	word = ""
	for character in data: #probably not the shortest way to do it but its quite readable i guess
		if letter_sequence:
			if character.lower() in alphabet:
				word += character
			else:
				if word.lower() in dictionary:
					correct_letters += len(word)
					word_color = colorama.Fore.LIGHTGREEN_EX
				else:
					incorrect_letters += len(word)
					word_color = colorama.Fore.LIGHTRED_EX
				words.append(word_color + word + colorama.Style.RESET_ALL)
				word = character
				letter_sequence = False
		else:
			if character.lower() in alphabet:
				words.append(word)
				word = character
				letter_sequence = True
			else:
				word += character
	solution["content_colored"] = "".join(words)
	solution["correct_letters_percent"] = correct_letters/incorrect_letters*100
	return solution
