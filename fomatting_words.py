from helpers import *

words = readFile('words.txt')
english = set()
for word in words.splitlines():
    if word.isalnum() and word[0].isalpha():
        english.add(word.lower())
writeFile('expanded_dictionary.txt', str(english))