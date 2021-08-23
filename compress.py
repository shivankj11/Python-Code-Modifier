from helpers import *

''' --------------------------------------------------------------------------------------------- '''


def removeWhitespace(s, stored):

    if s == '' or s.isspace():
        return ''
    
    symbols =    '''!                   +                   <=                 
                    "                   +=                  <>                  
                    ,                   ==                  |=                 
                    %                   -                   >                   
                    %=                  -=                  >=                  
                    &                   .                   >>                  
                    &=                  ...                 >>=                 
                    '                   /                   @                   
                    //                  ~                                      
                    |                   //=                                    
                    ^=                  /=                  \                   
                    *                   :                                     
                    **                  <                   ^                  
                    **=                 <<                  ^=    '''
    
    operationsList = set()
    for char in symbols:
        if not char.isspace():
            operationsList.add(char)
    
    final = ''
    while s.startswith(' '):
        s = s[1:]
        final += ' '
    s = s.strip()
    i = 0
    while i < len(s):
        if s[i].isspace():
            lastC, nextC = s[i-1], s[i+1]
            if (lastC not in operationsList) and (nextC not in operationsList):
                final += ' '
            # FIXME should work for any space within a string
            elif 'split' in s:
                final += ' '
        else:
            final += s[i]
        i += 1
    return final

def isRemovable(s):
    s = s.strip()
    return s == '' or s[0] == '#'


# uses only strings
def compressLoops(codeString):

    listCodeStrings = []
    for line in codeString.splitlines():
        listCodeStrings.append(line)


    def countIndents(s):
        indent = 0
        if s == '': 
            return indent
        while s[0].isspace():
            indent += 1
            s = s[1:]
        return indent

    changed = False
    i = 0
    while i < len(listCodeStrings) - 2:
        currLine, twoAfterLine = listCodeStrings[i], listCodeStrings[i+2]
        if (currLine.strip().endswith(':') and (currLine.strip().startswith('if') or currLine.strip().startswith('for')
            or currLine.strip().startswith('while') or currLine.strip().startswith('while'))):
            indent = countIndents(currLine)
            indent2 = countIndents(twoAfterLine)
            if (indent >= indent2 and 
            not twoAfterLine.strip().startswith('for') and 
            not twoAfterLine.strip().startswith('while')):
                listCodeStrings[i] = currLine + listCodeStrings[i+1].strip()
                listCodeStrings.pop(i+1)
                changed = True
                i -= 1
        i += 1

    outputCode = ''
    for line in listCodeStrings:
        outputCode += '\n' + line


    return outputCode


class changeName(ast.NodeTransformer):
    # changes node names if specified
    def __init__(self, storage):
        super().__init__()
        self.storage = storage
        
    def visitAll(self, node):
        if isinstance(node, ast.Name): #node.id == 'Name':
            self.name = node.id
            if self.name in self.storage['Names']:
                self.name = self.storage['Names'][self.name]
            node.id = self.name
        
        # FIXME WHY WONT PARAMETERS WORK
        elif isinstance(node, ast.arg):
            newName = False
            for field, val in ast.iter_fields(node):
                oldName = val
                if oldName in self.storage['Names']:
                    newName = self.storage['Names'][oldName]
            if newName:
                node = arg(newName, None, None)

        for field, value in ast.iter_fields(node):
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, ast.AST):
                        self.visitAll(item)
            elif isinstance(value, ast.AST):
                self.visitAll(value)
        return node

# shortens function/class/method/variable names
# can handle up to 1.24 million unique function/class/method/variable names in a file 
def shortenNames(code, storage, names):

    # helper that stores how many characters are needed to assign a given number of variables
    def makeCharMaxVals():
        charMaxVals = { 1 : 52 }
        for k in range(2, 5):
            charMaxVals[k] = 52 * 62 ** (k - 1) + 52
        return charMaxVals
    charMaxVals = makeCharMaxVals()

    # assignment
    for name in names:

        firstCharOptions = ( [ chr(ord('A') + i) for i in range(26) ] + 
                             [ chr(ord('a') + j) for j in range(26) ] )
        charOptions = firstCharOptions + [ chr(ord('0') + i) for i in range(10) ]

        def getNumChars(length):
            j = 1
            while j <= len(charMaxVals):
                if length < charMaxVals[j]:
                    return j
                j += 1
            print(f'Max number of variables ({charMaxVals[4]}) exceeded')

        numChars = getNumChars(len(storage['Names']))

        newName = ''
        n = len(storage['Names'])
        i = 0
        while i < numChars:
            if i == 0:
                char = firstCharOptions[ n % 51 ]
            else:
                char = charOptions[ (n - 51) // len(charOptions) ** (n) ]
            # idk why but 'J' just breaks everything
            if char == 'J': 
                char = chr(ord('J') + 1)
                i += 1
            newName += char
            i += 1
    
        storage['Names'][name] = newName

    # replacement (assign/replace done in separate steps for efficiency)

    tree = ast.parse(code)

    # uses NodeTransformer subclass to find each name in code and replace it with assigned value
    changer = changeName(storage)
    finalTree = changer.visitAll(tree)
    finalCode = treeToCode(finalTree).strip()
    
    return finalCode

    
    # original alternate variable name assignment
    firstChar = firstCharOptions[len(storage['Names']) % 52]
    valFirstChar = (ord('A') + (len(storage['Names'])))
    firstChar = chr(valFirstChar)
    secChar = False
    if firstChar > 'Z':
        firstChar = chr(ord(firstChar) + ord('a') - ord('A') - (ord('z') - ord('a') + 1))
    if firstChar > 'z':
        firstChar = chr(ord(firstChar) - 23)
        firstChar = chr(ord(firstChar) - (ord('z') - ord('A') + 1) + 1)
        secChar = chr(ord('A') + (len(storage['Names']) // 52 - 1))
    newName = firstChar
    if secChar:
        newName += secChar 
    
    
    # original alternative variable name replacement code
    codeTreeString = ''
    def makeMyTreeString(node):
        codeTreeString + '\n' + str_node(node)
        for field, value in ast.iter_fields(node):
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, ast.AST):
                        makeMyTreeString(item)
            elif isinstance(value, ast.AST):
                makeMyTreeString(value)

    
    listTreeStrings = createASTData(tree)[1]
    
    # replacement (assign/replace done in separate steps for efficiency)
    finalTree = ''
    for elem in listTreeStrings:
        for line in elem:
            # print(line)
            name = False
            if 'id' in line:
                indexId = line.find('id')
                s = line[indexId:]
                name = s.split('=')[1].split(',')[0]
                name = name[1:-1]
            if name:
                if name in storage['Names']:
                    # print(line)
                    line = line.replace(name, storage['Names'][name])
                    print('success')
                    # print(line)
            finalTree += '\n' + line.strip()
    # print(finalTree)
    # finalCode = astor.to_source(finalTree, indent_with='    ', add_line_information=False,)
    # finalCode = treeToCode(finalTree.strip())
    changer = changeName(storage)
    finalTree = changer.visit(tree)
    finalCode = treeToCode(finalTree).strip()

    return finalCode
    
    print(storage['Names'])

    
    newCode = ''
    for line in code.splitlines(): 
        newLine = ''
        for lineSegment in line.split(' '):
            if lineSegment not in storage['Keywords']:
                for name in names:
                    if name in lineSegment:
                        lineSegment = lineSegment.replace(name, storage['Names'][name])
            newLine += lineSegment
        newCode += '\n' + line
        newCode += '\n' + lineSegment
    return newCode


# temporary shortening of parameter names
def shortenParams(code, storage, names):
    
    finalCode = ''
    for line in code.splitlines():
        if line.strip().startswith('def') or line.strip().startswith('class'):
            oldParams = line.split('(')[1].split(')')[0].strip()
            newParams = []
            for oldName in oldParams.split(','):
                oldName = oldName.strip()
                # handling default parameters
                if '=' in oldName:
                    actualName = oldName.split('=')[0]
                    if actualName in storage['Names']:
                        newName = storage['Names'][actualName] + '=' + oldName.split('=')[1]
                        newParams.append(newName)
                elif oldName in storage['Names']:
                    newName = storage['Names'][oldName]
                    newParams.append(newName)
                else:
                    newParams.append(oldName)

            newParams = ','.join(newParams)
            firstPartLine = line.split('(')[0]
            secondPartLine = line.split(')')[1]
            line = firstPartLine + '(' + newParams + ')' + secondPartLine

        finalCode += '\n' + line

    return finalCode.strip()

    
def oldFunctionClassShorten(line, storage):
    if line.startswith('def') or line.startswith('class'):
        oldName = line.split(' ')[1].split('(')[0].strip()
        if oldName in storage['Names']:
            first = line.split(' ')[0]
            end = line.split('(')[1]
            line = first + ' ' + storage['Names'][oldName] + '(' + end
            # line = line.replace(oldName, storage['Names'][oldName])
    return line

def compressLine(line, stored):
    line = oldFunctionClassShorten(line, stored)
    line = removeWhitespace(line, stored)
    return line


def getNames(code, keepFuncClassNames=False):
    tree = ast.parse(code)
    names = set()
    fcNames = set()
    def storeNames(node):
        
        def addToNames(lookup, node, isFCName=False):

            notNames = builtIns
            notNames.add('print')
            notNames.add('AssertionError')

            if lookup in str_node(node):
                indexId = str_node(node).find(lookup)
                temp = str_node(node)[indexId:]
                name = temp.split('=')[1].split(',')[0]
                name = name[1:-1]
                if (not name.startswith('__') 
                    and name not in notNames and not name.isspace()):
                    names.add(name)
                    if isFCName:
                        fcNames.add(name)
                
        for elem in ['id', 'name']:
            if elem == 'name':
                if isinstance(node, ast.FunctionDef) or isinstance(node, ast.ClassDef):
                    addToNames(elem, node, True)
            else:
                addToNames(elem, node)

        for field, value in ast.iter_fields(node):
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, ast.AST):
                        storeNames(item)
            elif isinstance(value, ast.AST):
                storeNames(value)

    storeNames(tree)
    if keepFuncClassNames:
        for name in fcNames:
            if name in names:
                names.remove(name)
    return names


# start of call to compress given code
def compressCode(sourceFileName, goalFileName=False, keepFCNames=False):
    
    stored = { 
        'Names' : dict() ,
        'Keywords' : {'if', 'and', 'with', 'def', 'else', 'except', 'or', 'not', 'in', 'try', 
        'False', 'print', 'while', 'from', 'None', 'continue', 'global', 'pass', 'True', 'raise',
        'del', 'import', 'as', 'assert', 'else', 'is', 'async', 'lambda', 'await', 'finally'
        'nonlocal', 'yield', 'break', 'for', 'class', 'elif', 'return'}
    }
    
    fileContents = readFile(sourceFileName)
    tree = ast.parse(fileContents)
    fileContents = astor.to_source(tree, '    ', add_line_information=False)
    
    
    namesInCode = getNames(fileContents, keepFCNames)

    fileContents = shortenNames(fileContents, stored, namesInCode)
    fileContents = shortenParams(fileContents, stored, namesInCode)

    
    fileContents = compressLoops(fileContents)
    
    newContents = ''
    for line in fileContents.splitlines():
        line = compressLine(line, stored)
        if isRemovable(line): continue     
        newContents += '\n' + line  

    
    if not isinstance(newContents, str): 
        print('Error in Formatting Code')
        return
    newContents = newContents.strip()
    if goalFileName:
        writeFile(goalFileName, newContents)
    else:
        return newContents
