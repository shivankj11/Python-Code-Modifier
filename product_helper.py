# Contains most of the Tkinter screens used in user interface

from helpers import *

inputFile = None
targetFile = None


class FileNameCollectScreen(object):

    def __init__(self, master):

        self.master = master
        master.title("File Select")

        self.topLabel = Label(master, text='Please input file names (must be existing directory for source file)', 
                              font='16')
        self.topLabel.grid(row=0, columnspan=2, sticky='w')
        
        self.sourceFileLabel = Label(master, text='Source File Name   ', font='13')
        self.sourceFileLabel.grid(row=1, column=0, sticky='e')

        Label(master, text='Target File Name   ', font='13').grid(row=2, column=0, sticky='e')
        
        self.botLabel = Label(master, text='If no file name saved, sample files will be used', font='16')
        self.botLabel.grid(row=3, columnspan=2, sticky='s')
        
        self.sourceEntry = Entry(master, width=25, bg='#E8DFD8')
        self.sourceEntry.grid(row=1, column=1, sticky='w')

        self.targetEntry = Entry(master, width=25, bg='#E8DFD8')       
        self.targetEntry.grid(row=2, column=1, sticky='w')

        self.saveButton = Button(master, text='Save', font='8', command=self.save, width=15, height=1, background='#E8DFD8')
        self.saveButton.grid(row=4, column=0, sticky='e')

        self.closeButton = Button(master, text="Continue", font='8', command=self.quit, width=15, height=1, background='#E8DFD8')
        self.closeButton.grid(row=4, column=1, sticky='w')

    def save(self):
        global inputFile, targetFile
        inputFile = self.sourceEntry.get()
        targetFile = self.targetEntry.get()
        if inputFile == '' or inputFile.isspace():
            inputFile = None
        if targetFile == '' or targetFile.isspace():
            targetFile = None

    def quit(self):
        self.master.destroy()


class FileNameCollectScreenError(FileNameCollectScreen):

    def __init__(self, master):
        super().__init__(master)
        Label(master, text='Please use a valid source file name or leave field blank!').grid(row=5, columnspan=3, sticky='s')

class FileNameCollectScreenError2(FileNameCollectScreen):

    def __init__(self, master):
        super().__init__(master)
        Label(master, text='Your input file was unable to be parsed! Make sure it \nis written in python and compiles').grid(row=5, columnspan=3, sticky='s')


def runFileNameCollector():
    
    def runFileNameCollectorGUI():
        root = Tk()
        FileNameCollectScreen(root)
        root.mainloop()

    def runErrorVersion():
        root = Tk()
        FileNameCollectScreenError(root)
        root.mainloop()

    def runErrorVersion2():
        root = Tk()
        FileNameCollectScreenError2(root)
        root.mainloop()

    runFileNameCollectorGUI()
    
    global inputFile, targetFile

    def inputWorks(inputFile):
        try:
            readFile(inputFile)
            return True
        except:
            return False

    while not (inputFile == None or inputWorks(inputFile)):
        inputFile = None
        targetFile = None
        runErrorVersion()

    def inputDefinitelyWorks(inputFile):
        try:
            ast.parse(readFile(inputFile))
            redbaron.redbaron.RedBaron(readFile(inputFile))
            return True
        except:
            return False

    while not (inputFile == None or inputDefinitelyWorks(inputFile)):
        inputFile = None
        targetFile = None
        runErrorVersion2()

    return inputFile, targetFile


class previewCodeScreen(object):

    def __init__(self, master, code):
        
        self.master = master
        master.title("Code Preview")

        self.code = code

        self.scroll = scrolledtext.ScrolledText(master, bg='#F5D1EB', width=70, height=20)
        self.scroll.grid(row=0, column=0)
        self.scroll.insert(END, code)

        self.closeButton = Button(master, text="Exit", command=self.quit, width=15, height=2, bg='#E8DFD8')
        self.closeButton.grid(row=1, column=0, sticky='s')
        
    def quit(self):
        self.master.destroy()


def runPreviewGUI(code):
    root = Tk()
    previewCodeScreen(root, code)
    root.mainloop()
