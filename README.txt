
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Code Modifier ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Usage:
1) Open the 'product.py' file
3) Run the program and follow instructions

Two options:
1 - Take in source code and compress it while maintaining structure and python form
2 - Take in source code, improve spacing / basic style guidelines and then provide
    suggestions to further improve style based on CMU 15-112 class guidelines


IMPORTANT NOTES/LIMITATIONS:
    Program will not work correctly with imports that are more than one file deep 
        (ex: Source file inherits and uses methods from a file which inherits them from another file)
    Program may fail to work correctly if triple apostrophe strings are used


Specific Features:

    Compress
        - removes all non-essential whitespace
        - replaces each variable/function/class/parameter name with a shorter name 
            (at most 2 characters for up to 3224 unique names)
        - compresses loops/conditionals that can be shortened 
            ex: if True:
                    return 
                shortens to 
                if True:return
        - removes comments and triple apostrophe strings (non-python text)
    
    Style
        - returns code with consistent spacing and whitespace
        
        Optional Suggestions 'Code Modifier' finds:
            - magic numbers
            - variable/function/class names without camelCase
            - checks if each individual word in a function/variable with camelCase is in the English dictionary
            - lines that are longer than 80 characters
            - functions and classes that do not have comments describing them
            - global variables


Required Files and Installations:

    Files Required in folder:
        - ast.py
        - cmu_112_graphics.py
        - pretty_print.py
        - compress.py
        - style.py
        - english_dictionary.rst
        - expanded_dictionary.txt
        - helpers.py
        - product_helper.py
        - product.py
        - product_style_editor.py
        - source_code_test1.py (default source code for product)
        - product_test.py (default target file for product)

    Required Modules and Libraries
        - ast (provided as file)
        - astor (provided as file)
        - redbaron (provided as file)
        - tkinter_modified (provided as file)
        - tkinter
        - pretty_print
        - PyDictionary


Files that I have written for this project but are not used:
    - formatting_words.py
    - formatting_dictionary.py
    - lil_testing.py
    - unused.py
    - product2.py
    - product3.py