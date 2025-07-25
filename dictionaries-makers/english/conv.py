#! /usr/bin/python3
required_letter_count = 4
with open("./__source-dict__/words_alpha.txt") as f:
	words = f.read()
words = words.split("\n")
words = list(filter(lambda word: len(word)>=required_letter_count, words))
print(f"Selected {'{:,}'.format(len(words))} words")
with open("../../dictionaries/english", "w") as f:
	f.write("\n".join(words))
