import json

long_word_file = open("long-words.txt", "r")
medium_word_file = open("medium-words.txt", "r")
json_file = open("wordlist.json", "w")
data = []

for row in long_word_file:
    data.append(row.strip())

for row in medium_word_file:
    data.append(row.strip())

json.dump(data, json_file, indent=2)