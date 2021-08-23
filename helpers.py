# File of many helper functions and module imports to help code organization

import copy, math
import sys, os
# from https://docs.python.org/3/library/tkinter.html
from tkinter_modified import *
from tkinter_modified import scrolledtext
# from https://www.cs.cmu.edu/~112
from cmu_112_graphics import *
# from https://github.com/python/cpython/blob/3.8/Lib/ast.py
from ast import *
import ast
# from https://astor.readthedocs.io/en/latest/
import astor
# from https://github.com/python/cpython/blob/3.8/Lib/pprint.py
from pretty_print import pprint as p
# from https://github.com/PyCQA/redbaron
import redbaron
# from https://pypi.org/project/PyDictionary/
import PyDictionary

''' --------------------------------------------------------------------------------------------- '''

# from https://www.cs.cmu.edu/~112/notes/notes-strings.html#basicFileIO
def readFile(path):
    with open(path, "rt") as f:
        return f.read()

def writeFile(path, contents):
    with open(path, "wt") as f:
        f.write(contents)

''' --------------------------------------------------------------------------------------------- '''

# list of english words obtained from https://sourceforge.net/projects/wordlist/
englishWords = readFile('english_dictionary.rst')
englishWords = ast.literal_eval(englishWords)
# comprehensive list from https://github.com/dwyl/english-words/blob/master/words.txt
fullEnglishWords = readFile('expanded_dictionary.txt')
fullEnglishWords = ast.literal_eval(fullEnglishWords)
# both data sets reformatted into usable set form in given file by me

''' --------------------------------------------------------------------------------------------- '''

# returns a tuple: 
# (dictionary of each type of node and values they map to in an AST, tree as list of sequential strings)
def createASTData(parsedCode):

    finalDictTree = dict()
    listTreeStrings = []

    def storeIntoD(line):
        category = line.split('(')[0]
        inside = line.split('(')[1][:-1]
        if inside in builtIns or inside == '__main__':
            return
        if category not in finalDictTree:
            finalDictTree[category] = {inside}
        else:
            finalDictTree[category].add(inside)

    def makeData(node, depth = 0):
        line = '    ' * depth + str_node(node)
        listTreeStrings.append([line])
        storeIntoD(line)
        for name, value in ast.iter_fields(node):   
            if isinstance(value, list):
                for elem in value:
                    if isinstance(elem, ast.AST):
                        makeData(elem, depth + 1)
            elif isinstance(value, ast.AST):
                makeData(value, depth + 1)

    makeData(parsedCode)

    return (finalDictTree, listTreeStrings)


# returns a string version of a node in an AST
# taken from https://stackoverflow.com/questions/1515357/simple-example-of-how-to-use-ast-nodevisitor
def str_node(node):
    if isinstance(node, ast.AST):
        fields = [(name, str_node(val)) for name, val in ast.iter_fields(node) if name not in ('left', 'right')]
        rv = '%s(%s' % (node.__class__.__name__, ', '.join('%s=%s' % field for field in fields))
        return rv + ')'
    else:
        return repr(node)


# prints out an AST
def print_visit(startingNode):
    
    def astVisit(node, depth):
        p('  ' * depth + str_node(node))
        for field, value in ast.iter_fields(node):
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, ast.AST):
                        astVisit(item, depth+1)
            elif isinstance(value, ast.AST):
                astVisit(value, depth+1)
            elif isinstance(value, str):
                continue
                p('THIS: ' + value)
                
    astVisit(startingNode, 0)


# convert code from ast to string - main usage of astor module
def treeToCode(code):
    return astor.to_source(code, indent_with=' ' * 4, add_line_information=False,
                           source_generator_class=astor.SourceGenerator)

# storing python's built-in functions and methods as a set
# next string from https://www.w3schools.com/python/python_ref_functions.asp
builtInsStr = '''
abs()	Returns the absolute value of a number
all()	Returns True if all items in an iterable object are true
any()	Returns True if any item in an iterable object is true
ascii()	Returns a readable version of an object. Replaces none-ascii characters with escape character
bin()	Returns the binary version of a number
bool()	Returns the boolean value of the specified object
bytearray()	Returns an array of bytes
bytes()	Returns a bytes object
callable()	Returns True if the specified object is callable, otherwise False
chr()	Returns a character from the specified Unicode code.
classmethod()	Converts a method into a class method
compile()	Returns the specified source as an object, ready to be executed
complex()	Returns a complex number
delattr()	Deletes the specified attribute (property or method) from the specified object
dict()	Returns a dictionary (Array)
dir()	Returns a list of the specified object's properties and methods
divmod()	Returns the quotient and the remainder when argument1 is divided by argument2
enumerate()	Takes a collection (e.g. a tuple) and returns it as an enumerate object
eval()	Evaluates and executes an expression
exec()	Executes the specified code (or object)
filter()	Use a filter function to exclude items in an iterable object
float()	Returns a floating point number
format()	Formats a specified value
frozenset()	Returns a frozenset object
getattr()	Returns the value of the specified attribute (property or method)
globals()	Returns the current global symbol table as a dictionary
hasattr()	Returns True if the specified object has the specified attribute (property/method)
hash()	Returns the hash value of a specified object
help()	Executes the built-in help system
hex()	Converts a number into a hexadecimal value
id()	Returns the id of an object
input()	Allowing user input
int()	Returns an integer number
isinstance()	Returns True if a specified object is an instance of a specified object
issubclass()	Returns True if a specified class is a subclass of a specified object
iter()	Returns an iterator object
len()	Returns the length of an object
list()	Returns a list
locals()	Returns an updated dictionary of the current local symbol table
map()	Returns the specified iterator with the specified function applied to each item
max()	Returns the largest item in an iterable
memoryview()	Returns a memory view object
min()	Returns the smallest item in an iterable
next()	Returns the next item in an iterable
object()	Returns a new object
oct()	Converts a number into an octal
open()	Opens a file and returns a file object
ord()	Convert an integer representing the Unicode of the specified character
pow()	Returns the value of x to the power of y
print()	Prints to the standard output device
property()	Gets, sets, deletes a property
range()	Returns a sequence of numbers, starting from 0 and increments by 1 (by default)
repr()	Returns a readable version of an object
reversed()	Returns a reversed iterator
round()	Rounds a numbers
set()	Returns a new set object
setattr()	Sets an attribute (property/method) of an object
slice()	Returns a slice object
sorted()	Returns a sorted list
@staticmethod()	Converts a method into a static method
str()	Returns a string object
sum()	Sums the items of an iterator
super()	Returns an object that represents the parent class
tuple()	Returns a tuple
type()	Returns the type of an object
vars()	Returns the __dict__ property of an object
zip()	Returns an iterator, from two or more iterators
'''
builtIns = set()
for line in builtInsStr.strip().splitlines():
    element = line.split('\t')[0]
    builtIns.add(element[:-2])
    builtIns.add(element)
