#! /usr/bin/python3
required_letter_count = 4
targets = [
	"./__source-dict__/adjectives.csv",
	"./__source-dict__/nouns.csv",
	"./__source-dict__/verbs.csv",
	"./__source-dict__/others.csv"]
with open("../../alphabets/russian", "r") as f:
	alphabet = f.read().replace("\n", "")
words = []
for target in targets:
	with open(target) as f:
		data = f.readline()
		while data:
			data = f.readline()
			words.append(data.split("\t")[0])

words = list(filter(lambda word: len(word)>=required_letter_count and sum([word.lower().count(letter) for letter in alphabet])==len(word), words))
print(f"Selected {'{:,}'.format(len(words))} words")
with open("../../dictionaries/russian", "w") as f:
	f.write("\n".join(words))
