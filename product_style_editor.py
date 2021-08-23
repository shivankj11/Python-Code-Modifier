# Contains files specific to GUI for suggestions part of Style section

from helpers import *
from product_helper import previewCodeScreen
from compress import changeName, getNames, oldFunctionClassShorten

finalCode = ''
listToReplace = dict()


class StylePreview(previewCodeScreen):

    def __init__(self, master, code, readable, usable):
        
        self.master = master
        master.title('Style Suggestions')

        self.code = code
        self.readable = readable
        self.usable = usable

        self.scroll = scrolledtext.ScrolledText(master, bg='#F5D1EB', width=70, height=20)
        self.scroll.grid(row=0, columnspan=2)
        self.scroll.insert(END, self.readable)
        
        self.closeButton = Button(master, text='Exit', command=self.quit, width=15, height=2, bg='#E8DFD8')
        self.closeButton.grid(row=1, column=0, sticky='s')

        self.contButton = Button(master, text='Make Edits', command=self.cont, width=15, height=2, bg='#E8DFD8')
        self.contButton.grid(row=1, column=1, sticky='s')

    def quit(self):
        self.master.destroy()

    def cont(self):
        self.quit()
        if len(self.usable) > 0:
            runStyleEditor(self.usable)


class StyleEditor(object):

    def __init__(self, master, suggestions, index=0):
        
        self.master = master
        master.title("Style Editor")

        global finalCode
        self.code = finalCode
        self.suggestions = suggestions
        self.index = index

        self.listChangeables = []
        for elem in suggestions:
            self.listChangeables.append(elem)

        self.categoryTitle = self.listChangeables[self.index]

        self.title = Label(master, text=self.categoryTitle + ':', font='ComicSansMS 16 bold')
        self.title.grid(row=0, columnspan=6)

        self.errors = scrolledtext.ScrolledText(master, bg='#F5D1EB', width=60, height=8, font='ComicSansMS 10 bold')
        self.errors.grid(row=1, columnspan=6)
        self.errors.insert(END, str(self.suggestions[self.categoryTitle])[1:-1])

        self.instructions = Label(master, font='ComicSansMS 10 bold',
                                  text='If you wish to change any names in your code:\nEnter the old name and your desired new name and select save')
        self.instructions.grid(row=2, columnspan=6)

        self.oldNameLabel = Label(master, text='Old Name', font='ComicSansMS 12 bold')
        self.oldNameLabel.grid(row=3, column=0, columnspan=3)
        self.oldName = Entry(master, width=30, bg='#E8DFD8')
        self.oldName.grid(row=4, column=0, columnspan=3)

        self.newNameLabel = Label(master, text='New Name', font='ComicSansMS 12 bold')
        self.newNameLabel.grid(row=3, column=3, columnspan=3)
        self.newName = Entry(master, width=30, bg='#E8DFD8')
        self.newName.grid(row=4, column=3, columnspan=3)

        self.spacer = Label(master).grid(row=5, columnspan=6)

        self.saveButton = Button(master, text='Save Change', command=self.save, width=20, height=2, bg='#E8DFD8')
        self.saveButton.grid(row=6, column=2, sticky='s', columnspan=2)

        self.continueButton = Button(master, text='Next', command=self.cont, width=15, height=2, bg='#E8DFD8')
        self.continueButton.grid(row=6, column=4, sticky='s', columnspan=2)

        self.exitButton = Button(master, text='Exit', command=self.exit, width=15, height=2, bg='#E8DFD8')
        self.exitButton.grid(row=6, column=0, sticky='s', columnspan=2)

        self.spacer2 = Label(master).grid(row=7, columnspan=6)

    def exit(self):
        self.master.destroy()

    def save(self):
        global finalCode
        old = self.oldName.get()
        new = self.newName.get()
        
        for elem in [old, new]:
            if elem == '' or elem == None or elem.isspace(): return

        def checkIfOldNameValid(code, old):
            if old not in finalCode:
                return False
            return old in getNames(finalCode)
                
        if not checkIfOldNameValid(finalCode, old):
            StyleEditorError(self.master, self.suggestions, self.index)
        elif not new.isalnum() or not new[0].isalpha():
            StyleEditorError2(self.master, self.suggestions, self.index)
        else:
            global listToReplace
            listToReplace[old] = new
            StyleEditor(self.master, self.suggestions, self.index)


    def cont(self):
        if self.index >= len(self.listChangeables) - 1:
            self.master.destroy()
        else:
            StyleEditor(self.master, self.suggestions, self.index + 1)


class StyleEditorError(StyleEditor):

    def __init__(self, master, suggestions, index=0):
        super().__init__(master, suggestions, index)
        self.oldMaster = self.master

        self.notValidName = Label(self.master, text='That old name wasn\'t a variable/function/class in your code')
        self.notValidName.grid(row=8, columnspan=6)

    def save(self):
        global finalCode
        old = self.oldName.get()
        new = self.newName.get()
        
        for elem in [old, new]:
            if elem == '' or elem == None or elem.isspace(): return

        def checkIfOldNameValid(code, old):
            if old not in finalCode:
                return False
            return old in getNames(finalCode)
                
        if not checkIfOldNameValid(finalCode, old):
            StyleEditorError(self.oldMaster, self.suggestions, self.index)
        elif not new.isalnum() or not new[0].isalpha():
            StyleEditorError2(self.oldMaster, self.suggestions, self.index)
        else:
            global listToReplace
            listToReplace[old] = new
            StyleEditor(self.oldMaster, self.suggestions, self.index)

    def cont(self):
        if self.index >= len(self.listChangeables) - 1:
            self.master.destroy()
        else:
            StyleEditor(self.oldMaster, self.suggestions, self.index + 1)


class StyleEditorError2(StyleEditor):

    def __init__(self, master, suggestions, index=0):
        super().__init__(master, suggestions, index)

        self.notValidName = Label(self.master, text='That new name wasn\'t valid (must be alphanumeric, cannot start with number)')
        self.notValidName.grid(row=8, columnspan=6)

    def cont(self):
        if self.index >= len(self.listChangeables) - 1:
            self.master.destroy()
        else:
            StyleEditor(self.oldMaster, self.suggestions, self.index + 1)

def runStyleEditor(analysis):
    root = Tk()
    StyleEditor(root, analysis)
    root.mainloop()


def runAllStyle(codeInput, analysis):

    global finalCode
    finalCode = codeInput
    
    def runStylePreview(code, analysis):
        readableAnalysis, dictionaryAnalysis = analysis
        root = Tk()
        StylePreview(root, code, readableAnalysis, dictionaryAnalysis)
        root.mainloop()
    
    runStylePreview(finalCode, analysis)

    global listToReplace
    p(listToReplace)
    storage = { 'Names' : listToReplace }   

    # node transformer and function/class name shortener from compress 
    def replaceAllNames(finalCode, storage):
        tree = ast.parse(finalCode)
        changer = changeName(storage)
        finalTree = changer.visitAll(tree)
        finalCode = treeToCode(finalTree).strip()

        actualFinal = ''
        for line in finalCode.splitlines():
            line = oldFunctionClassShorten(line, storage)
            actualFinal += '\n' + line
        return actualFinal.strip()

    finalCode = replaceAllNames(finalCode, storage)
        
    return finalCode
