from helpers import *

''' --------------------------------------------------------------------------------------------- '''
keyWords = [ ['def', 'class', 'for', 'while', 'elif', 'return', 'pass', 'continue', 'break',
                  'try', 'except', 'from', 'await', 'finally', 'global', 'raise', 'range'], 
                 ['in', 'is', 'not'],
                 ['import', 'with', 'if', 'else'] ]


def inString(s, index):
    return False

def removeWhitespace(s):
    global keyWords
    if s == '':
        return '' 
    final = ''
    while s.startswith(' '):
        s = s[1:]
        final += ' '

    s = s.strip()
    i = 0
    for word in s.split(' '):
        if word in keyWords[0]:
            final += word + ' '
        elif word in keyWords[1]:
            final += ' ' + word + ' '
        elif word in keyWords[2]:
            if s.startswith(word):
                final += word + ' '
            else:
                final += ' ' + word + ' '
        else:
            final += word
    return final

def addTastefulWhitespace(s):
    operationsList = ['=', '+', '-', '/', '%', '*', ',', '<', '>', '!']
    new = ''
    i = 0
    while i < len(s): 
        if s[i] in operationsList:
            if s[i-1] in operationsList:
                new += s[i] + ' '
            else:
                new += ' ' + s[i] + ' '
            if i < len(s) - 1:
                if s[i+1] in operationsList:
                    new = new[:-1]
        else:
            new += s[i]
        i += 1
    return new

def fixWhitespace(line):
    if len(line) > 0 and line[0] != '#':
        line = removeWhitespace(line)
        line = addTastefulWhitespace(line)
    return line



def doAnalysis(code):

    codeTree = ast.parse(code)
    finalDictTree, finalListStrings = createASTData(codeTree)

    global englishWords, fullEnglishWords

    def getMagicNumbers(category, treeDict):
        magicNumbers = []
        for elem in finalDictTree[category]:
                if elem[0] == 'v':
                    try:
                        num = ast.literal_eval(elem.split(',')[0].split('=')[1])
                        notMagics = [-1, 0, 0.5, 1, 2, 10]
                        if hash(num) not in notMagics and not str(num).isspace() and num != '__main__':
                            magicNumbers.append(num)
                    except:
                        continue
        return magicNumbers

    def camelCase(s):
            
        def checkRest(s):  
            if s.islower() or len(s) < 2:
                return True
            else:
                if s[0].isupper():
                    if s[1].isupper(): 
                        return False
                    else: 
                        return checkRest(s[1:])
                else:
                    return checkRest(s[1:])

        if s == '' or s[0].isupper():
            return False
        else:
            return checkRest(s[1:]) 

    def realWords(s):
        if s.islower():
            return s in englishWords or s in fullEnglishWords
        
        listWords = []
        i = 0
        last = 0
        while i < len(s):
            if s[i].isupper():
                part = s[last:i].lower()
                listWords.append(part)
                last = i
            i += 1
        listWords.append(s[last:].lower())
        for elem in listWords:
            if elem not in englishWords:
                if elem not in fullEnglishWords:
                    return False
        return True

    def getBadNames(category, treeDict):
        badNames = {'Camel Case Issues' : set() , 'Not Recognized English' : set()}
        nonDescriptiveNames = ['value', 'val']
        for elem in finalDictTree[category]:
            if elem[0] == 'i':
                nameStore = ast.literal_eval(elem.split(',')[0].split('=')[1])
                if not camelCase(nameStore):
                    badNames['Camel Case Issues'].add(nameStore)
                elif (len(nameStore) < 3
                      or nameStore.lower() in nonDescriptiveNames
                      or not realWords(nameStore)):
                    if nameStore != 'i' and nameStore != 'j' and nameStore != 'k':
                        badNames['Not Recognized English'].add(nameStore)
        return badNames

    def getBadFunctions(category, finalDictTree):
        badFunctions = {'Camel Case Issues' : set() , 'Not Recognized English' : set()}
        for elem in finalDictTree[category]:
            name = elem.split('=')[1].split(',')[0][1:-1]
            if not camelCase(name):
                badFunctions['Camel Case Issues'].add(name)
            elif not realWords(name) or len(name) < 3 or 'function' in name.lower():
                badFunctions['Not Recognized English'].add(name)
        return badFunctions

    def getRepeats(category, finalDictTree):
        return

    def getLongLines(code):
        longLines = set()
        i = 0
        while i < len(code.splitlines()):
            line = code.splitlines()[i]
            if line != '' and not line.isspace(): 
                if len(line) > 80:
                    longLines.add(i+1)
            i += 1
        return longLines
    
    def getNoCommentFunctions(code):
        noCommentFuncs = set()
        if code.splitlines()[0].startswith('def') or code.splitlines()[0].startswith('class'):
            noCommentFuncs.add(code.splitlines()[0].split(' ')[1].strip().split('(')[0].strip())
        i = 1
        while i < len(code.splitlines()):
            line = code.splitlines()[i]
            prev = code.splitlines()[i-1]
            if line.strip().startswith('def') or line.strip().startswith('class'):
                if not prev.strip().startswith('#') or prev.strip().startswith('\''):
                    noCommentFuncs.add(line.split(' ')[1].strip().split('(')[0].strip())
            i += 1
        return noCommentFuncs

    def getGlobals(code):
        globalList = set()
        i = 0
        while i < len(code.splitlines()):
            line = code.splitlines()[i]
            if line != '' and not line.isspace():
                if not line[0].isspace():
                    try:
                        tree = redbaron.redbaron.RedBaron(line)
                        for elem in tree:
                            if isinstance(elem, redbaron.nodes.AssignmentNode):
                                var = str(elem).split('=')[0].strip()
                                globalList.add(var)
                    except:
                        pass  
            i += 1
        return globalList


    def getSuggestions():
        suggestions = dict()
        for category in finalDictTree:
            if 'Constant' in category:
                suggestions['Magics'] = getMagicNumbers(category, finalDictTree)
            elif 'FunctionDef' in category:
                suggestions['Bad Functions'] = getBadFunctions(category, finalDictTree)
            elif 'Name' in category:
                suggestions['Bad Variable Names'] = getBadNames(category, finalDictTree) 
        suggestions['Repeated Code'] = getRepeats(category, finalDictTree) # not yet implemented
        suggestions['noCommentFuncs'] = getNoCommentFunctions(code)
        suggestions['Long Lines'] = getLongLines(code)
        suggestions['Global Variables'] = getGlobals(code)

        return suggestions
    

    def formatSuggestions(suggestions):
        try:
            for elem in suggestions['Bad Variable Names']:
                        for name in elem:
                            for elem2 in suggestions['Bad Functions']:
                                if name in elem2:
                                    elem.remove(name)
        except: # in case code contains no functions/classes
            pass

        # gets rid of test functions without comments
        deleteThese = set()
        for elem in suggestions['noCommentFuncs']:
            if elem.startswith('test'):
                deleteThese.add(elem)
        
        for elem in deleteThese:
            suggestions['noCommentFuncs'].remove(elem)

        # FIXME delete empty sets (replaces w/ space for now)
        deleteThese = set()
        for elem in suggestions:
            if suggestions[elem] == set():
                deleteThese.add(elem)
         
        for elem in deleteThese:
            suggestions[elem] = ''

        return suggestions

    
    suggestions = formatSuggestions(getSuggestions())


    analysis = ('Found these magic numbers in your code:\n    ' + str(suggestions['Magics']) +
                    '\nThese variable names are questionable:\n' + 
                            '    Camel Case Issues: ' + str(suggestions['Bad Variable Names']['Camel Case Issues']) + 
                            '\n    Not Recognized English: ' + str(suggestions['Bad Variable Names']['Not Recognized English']) +
                    '\nThese function names have problems:\n' + 
                            '    Camel Case Issues: ' + str(suggestions['Bad Functions']['Camel Case Issues']) + 
                            '\n    Not Recognized English: ' + str(suggestions['Bad Functions']['Not Recognized English']) + 
                    '\nThese lines are too long (greater than 80 characters):\n    ' + str(suggestions['Long Lines'])+
                    '\nThese functions do not have comments describing them:\n    ' + str(suggestions['noCommentFuncs']) +
                    '\nThese are global variables found in your code:\n    ' + str(suggestions['Global Variables']) )
    
    readableAnalysis  = ''
    for char in analysis: 
        if not (char == '{' or char == '}' or char == '[' or char == ']'):
            readableAnalysis += char
    readableAnalysis = readableAnalysis.replace('set()', 'None Detected')
    

    def makeDictAnalysis(suggestions):
        dictionaryAnalysis = { 0 : dict(), 1 : dict() }
        # changeable
        dictionaryAnalysis[0]['Function Names with Camel Case Issues'] = suggestions['Bad Functions']['Camel Case Issues']
        dictionaryAnalysis[0]['Function Names not Recognized as English'] = suggestions['Bad Functions']['Not Recognized English']
        dictionaryAnalysis[0]['Variable Names with Camel Case Issues'] = suggestions['Bad Variable Names']['Camel Case Issues']
        dictionaryAnalysis[0]['Variable Names not Recognized as English'] = suggestions['Bad Variable Names']['Not Recognized English']
        # non-changeable
        dictionaryAnalysis[1]['Global Variables'] = suggestions['Global Variables']
        dictionaryAnalysis[1]['Long Lines'] = suggestions['Long Lines']
        dictionaryAnalysis[1]['Magic Numbers'] = suggestions['Magics']
        dictionaryAnalysis[1]['Functions without Comments'] = suggestions['noCommentFuncs']
        
        toDel = set()
        for n in dictionaryAnalysis:
            for elem in dictionaryAnalysis[n]:
                if dictionaryAnalysis[n][elem] == set(): 
                    toDel.add( (n, elem) )

        for n, elem in toDel:
            del dictionaryAnalysis[n][elem]

        return dictionaryAnalysis

    dictionaryAnalysis = makeDictAnalysis(suggestions)

    usableDictionaryAnalysis = dictionaryAnalysis[0]

    return readableAnalysis, usableDictionaryAnalysis
    
    

def storeComments(code):
    commentList = dict()
    codeList = code.splitlines()
    codeListClean = []
    for line in codeList:
        if not line.isspace() and line != '':
            codeListClean.append(line)
    codeList = codeListClean
    i = 0
    while i < len(codeList):
        if len(codeList[i]) > 0 and codeList[i][0] == '#':
            commentList[i] = codeList[i]
        i += 1
    return commentList

def addCommentsBack(code, comments):
    finalCode = ''
    codeList = code.splitlines()
    i = 0
    while i < len(codeList):
        if i in comments:
            finalCode += comments[i] + '\n'
            comments.pop(i)
        else:
            finalCode += codeList[i] + '\n'
            i += 1
    return finalCode


def formatCode(codeString):
    
    red = redbaron.redbaron.RedBaron(codeString)

    formattedCode = ''
    for node in red:
        # p(node)
        # print(type(node))
        if isinstance(node, redbaron.nodes.CommentNode):
            formattedCode += '\n' + str(node)
            continue
        else:
            if '#' not in str(node):
                nodeTree = ast.parse(str(node))
                nodeCode = treeToCode(nodeTree)
                formattedCode += '\n' + nodeCode
            else:
                for line in str(node).splitlines():
                    if '#' not in str(node):
                        line = removeWhitespace(str(line))
                        line = addTastefulWhitespace(line)
                    formattedCode += '\n' + line


    red = redbaron.redbaron.RedBaron(formattedCode)

    allVars = dict()
    for node in red:
        if isinstance(node, redbaron.nodes.CommentNode):
            continue # print(node.value)
        
        if isinstance(node, redbaron.nodes.AtomtrailersNode):
            for kid in node:
                # print(kid, type(kid))
                # print('Value of kid:', kid.value)
                if isinstance(kid, redbaron.nodes.CallNode):
                    for child in kid:
                        pass
                        # print(child, type(child))
        elif isinstance(node, redbaron.nodes.AssignmentNode):
            if node.target in allVars:
                if isinstance(allVars[node.target], tuple):
                    allVars[node.target] = node.value
                else:
                    allVars[node.target] = node.value
            else:
                allVars[node.target] = node.value
    # p(allVars)
    return formattedCode


def stylize(sourceFileName):

    fileContents = readFile(sourceFileName)
    code = formatCode(fileContents)

    finalList = []
    for line in code.splitlines():
        if line.strip() == '': continue
        newLine = fixWhitespace(line)
        if line.strip().startswith('def') or line.strip().startswith('class'):
            if finalList[-1].startswith('#'):
                last = finalList.pop()
                finalList.extend(['', last, line])
            else:
                finalList.extend(['', line])
        else:
            finalList.append(line)
    
    final = ''
    for elem in finalList:
        final += '\n' + elem

    return final


def doStyle(sourceFileName, goalFileName=False):
    newContents = stylize(sourceFileName).strip()
    assert(isinstance(newContents, str)) # jus making sure
    analysis = doAnalysis(newContents)
    if goalFileName:
        writeFile(goalFileName, newContents)
    else:
        return newContents, analysis

