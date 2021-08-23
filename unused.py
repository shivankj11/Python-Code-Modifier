# Unused Code Segments 
# I either put a lot of work into them or could be useful




# calls inside style editor to go to style shower
elif self.index >= len(self.listChangeables) - 1:
            print('SUGGESTIONSSS ', self.suggestions[0])
            runStyleShower(self.code, self.nonChangeable)# StyleShower(self.master, self.code, self.suggestions, self.index + 1)
        else:
            StyleEditor(self.master, self.suggestions, self.index + 1)



class StyleShower(object):

    def __init__(self, master, suggestions, index=0):

        self.master = master
        master.title("Style Editor")

        self.suggestions = suggestions
        print('SUGGEST', self.suggestions)
        self.index = index


        self.listNonChange = []
        for elem in self.suggestions:
            self.listNonChange.append(elem)
        print('NONCHANGE', self.listNonChange)


        self.cL = Label(master, text='')#self.listNonChange[self.index - len(self.changeable)])
        self.cL.grid(row=2, column=0)
        self.lV = Label(master, text='')#self.nonChangeable[self.listNonChange[self.index - len(self.changeable)]])
        self.lV.grid(row=2, column=1)

    def exit(self):
        self.master.destroy()

    def cont(self):
        StyleShower(self.master, self.code, self.suggestions, self.index + 1)

def runStyleShower(code, suggestions):
        root = Tk()
        StyleShower(root, suggestions)
        root.mainloop()


# old loading
""" for i in range(5):
            canvas.create_arc(app.width * 0.89, app.height * 0.89, 
                              app.width * 0.93, app.height * 0.93, 
                              start=app.loadingPosition , extent=(app.loadingPosition + 72)) """


# attempts at formatting suggestions
for line in a:
        if line.strip().endswith(':'):
            final += '\n' + line.split(':')[0] + '\n    ' + line.split(':')[1]
        else:
            final += '\n' + line
    
    return final

    
    i = 0
    l = final.splitlines()
    while i < len(l):
        line = l[i]
        if line == '' or line.isspace():
            l = l[:i-1] + l[i+1:]
            
        i += 1
    final = l



# original space before function shit

    # newCode = ''
    # i = 1
    # while i < len(code.splitlines()):
    #     line = code.splitlines()[i]
    #     if len(line.strip()) > 3:
    #         if line.strip()[0:3] == 'def':
    #             newCode += '\n'
    #     elif len(line.strip()) > 5:
    #         if line.strip()[0:5] == 'class':
    #             newCode += '\n'
    #     newCode += '\n' + line
    #     i += 1

def oldFunctionClassShorten(line, storage):
    if line.startswith('def') or line.startswith('class'):
        oldName = line.split(' ')[1].split('(')[0].strip()
        if oldName in storage['Names']:
            #FIXME to not replace throughout line
            line = line.replace(oldName, storage['Names'][oldName])
        '''else:
            newName = chr(ord('A') + len(storage['Names'])) 
            if newName > 'Z':
                newName = chr(ord(newName) + ord('a') - ord('A') - (ord('z') - ord('a') + 1))
                """ if newName > 'z':
                print('You have more than 52 variables...Consider restructuring your code')
                newName = oldName """
            else:
                newName = 'abc' + chr(ord('A') + len(storage['Names'])) '''
            # storage['Names'][oldName] = newName
            # line = line.replace(oldName, newName)
    # check for calls to previously shortened 
    # for elem in storage['Names']:
        # if elem in line:
            # line = line.replace(elem, storage['Names'][elem])
    return line


# for compress file to replace var names w/ redbaron
    """ red = redbaron.redbaron.RedBaron(newContents)
    # print('start')
    i = 0
    newContents = ''
    while i < len(red):
        node = str(red[i]).strip()
        if node.startswith('def'):
            name = node.split(' ')[1]
            # print('NAME:',name)
            node.replace(name, 'a')
        newContents += '\n' + node
        try:
            for elem in red[i]:pass
                # print(elem)
        except:
            pass
        i += 1
        # print('BREAK') """


# PARAMETERS WONT DETECT IN DA try:
     """ elif isinstance(node, ast.arguments):
            pass
            # print('PLEASE')
            if 'category' in str_node(node):
                print('bruh please',str_node(node))
            for field, val in (ast.iter_fields(node)):
                if field == 'arg':
                    if val:
                        # print(val)

                        self.name = val
                        if self.name in self.storage['Names']:
                            self.name = self.storage['Names'][self.name]
                        val= self.name
                        # print('reached')
            # print('AHHHHHH', str_node(node)) """
except expression as identifier:
    pass
else:
    pass

# unused
def print_visit(startingNode):
    storeNames = set()
    def ast_visit_print(node, depth):
        # p('  ' * depth + str_node(node))
        for field, value in ast.iter_fields(node):
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, ast.AST):
                        ast_visit_print(item, depth+1)
            elif isinstance(value, ast.AST):
                ast_visit_print(value, depth+1)
            elif isinstance(value, str):
                continue 
                p('THIS: ' + value)
    
    ast_visit_print(startingNode, 0)



# wack

class fileNameCollector(object):

    def __init__(self, master):

        Label(master, 
        text='Please input file names (must be existing directory for source file)').grid(row=0, columnspan=2, sticky='w')
        Label(master, text='Source File Name').grid(row=1, column=0)
        Label(master, text='Target File Name').grid(row=2, column=0)
        Label(master, text='If no file name / invalid file name saved, sample files will be used').grid(row=3, columnspan=2, sticky='w')

        self.e1 = Entry(master)
        self.e2 = Entry(master)

        self.e1.grid(row=1, column=1)
        self.e2.grid(row=2, column=1)


        Button(master, text='Save', command=self.save).grid(row=4, column=0, sticky='w')
                                                       
        Button(master, text='Continue', command=exit).grid(row=4, column=1, sticky='e')

    def save(self):
        global inputFile, targetFile
        inputFile = self.e1.get()
        targetFile = self.e2.get()

    def exit(self):
        self.lower()
        
# bruh idek why this didnt work
""" class CodeModifier(App):

    

    def appStarted(app):
        app.margin = getDimensions(app)
        app.title = 'Code Modifier'
        app.key = 't'
        app.page = 'title'
        app.input = None
        app.code = ''
        app.analysis = ''
        
        app.acceptableInputs = ['q', 't', 'b', 'c']
        
        app.popOut = ScrolledText(bg='white', height=5, font='20')
        app.popOut.insert(END, app.code)
        app.popOut.pack(fill=BOTH, side=LEFT, expand=True)
        app.popOut.focus_set()

    def getCode(app):
        if app.key == 'c':
            app.code = compressCode(inputFile)
        elif app.key == 'b':
            app.code, app.analysis = doStyle(inputFile)
            

    def timerFired(app):
        app.margin = getDimensions(app)
        # app.createCodeBox()

    def createCodeBox(app):
        if app.page != 'compress' and app.page != 'beautify':
            return
        app.popOut
        




    def keyPressed(app, event):
        if event.key.lower() not in app.acceptableInputs or event.key.lower() == app.key:
            return
        app.key = event.key.lower()
        if app.key == 'q':
            app.quit()
        elif app.key == 'b':
            app.page = 'beautify'
        elif app.key == 'c':
            app.page = 'compress'
            # app._canvas.delete(ALL)

            Compress(width=600, height=800)



    def mousePressed(app, event):
        app.x, app.y = event.x, event.y
        
    

    
    def drawCurrentPage(app, canvas):
        if app.page == 'title':
            app.drawTitlePage(canvas)
        elif app.page == 'compress':
            app.drawCompressPage(canvas)
        elif app.page == 'beautify':
            app.drawBeautifyPage(canvas)
    
    def drawTitlePage(app, canvas):
        fontSize = min(app.width, app.height) // 30
        canvas.create_text(app.width/2, app.height/2, anchor = 'c', font = f'ComicSansMS {fontSize}',
                           width = app.width/1.5,
                           text = 'Please select \'c\' to Compress or \'b\' to Beautify Code')

    def drawCompressPage(app, canvas):
        canvas.create_text(app.width/2, app.height/2, anchor = 'c', font = 'ComicSansMS 20',
                           width = app.width/1.5,
                           text = 'Would you like to write this code to a file?')
        

        if inputFile:
            compressCode(inputFile)


    def drawBeautifyPage(app, canvas):
        canvas.create_text(app.width/2, app.height/3, anchor = 'c', font = 'ComicSansMS 20',
                           width = app.width/1.5,
                           text = 'Some Style Pointers:')
        # code, analysis = doStyle(inputFile)
        analysis ='asdf'
        canvas.create_text(app.width/2, app.height/2, anchor = 'c', font = 'fixedsys 10',
                           width = app.width/1.5, text = analysis)

    def redrawAll(app, canvas):
        drawTitleBG(app, canvas)
        
        app.drawCurrentPage(canvas)

        canvas.create_text(app.width/2, app.height - 50, text = app.key, font = '25') """


# for product file
""" key = ''
while key != 'q':
    key = input(inputStatement)
    while not (key == 'q' or key == 'compress' or key == 'beautify'):
        key = input(inputStatement)
    if key == 'compress':
        print(outputStatement + compressCode(inputFile))
        while not (key == 'n' or key == 'y'):
            key = input('Would you like to store this code into a file? (y/n): ')
            if key == 'y':
                key = input('Please type the name of your target file with the ending: ')
                compressCode(inputFile, key)
                break
            
    elif key == 'beautify':
        print(outputStatement + doStyle(inputFile))
        while not (key == 'n' or key == 'y'):
            key = input('Would you like to store this code into a file? (y/n): ')
            if key == 'y':
                key = input('Please type the name of your target file with the ending including the ending: ')
                compressCode(inputFile, key)
                break """