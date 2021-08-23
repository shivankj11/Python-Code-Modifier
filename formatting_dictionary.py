from helpers import *

words = readFile('en_US.dic')
english = set()
for line in words.splitlines():
    english.add(line.split('/')[0])
writeFile('english_dictionary.rst', str(english))