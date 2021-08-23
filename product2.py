from tkinter import *
import sys, os
from helpers import readFile 
                
# citation https://www.geeksforgeeks.org/python-gui-tkinter/


sourceFileName = None
targetFileName = None



class Page(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
    def show(self):
        self.lift()



class fileNameCollector(Page):

    def __init__(self, master):
        Page.__init__(self)
        master.title('Code Modifier')

        self.label = Label(master, text='Please input file names (must be existing directory for source file)\nIf no file name saved, sample files will be used'
                        ).grid(row=0, columnspan=2)

        self.label2 = Label(master, text='Source File Name').grid(row=1, column=0, sticky='e')
        self.inputEntry = Entry(master)
        self.inputEntry.grid(row=1, column=1, sticky='w')
        
        self.label3 = Label(master, text='Target File Name').grid(row=2, column=0, sticky='e')
        self.outputEntry = Entry(master)
        self.outputEntry.grid(row=2, column=1, sticky='w')

        self.label4 = Label(master, text='Save the file names if you want then click continue').grid(row=3, columnspan=2)

        self.saveButton = Button(master, text="Save", command=self.save).grid(row=4, column=0, sticky='e')

        self.continueButton = Button(master, text="Continue", command=self.next).grid(row=4, column=1, sticky='w')

    def save(self):
        global sourceFileName, targetFileName
        sourceFileName = self.inputEntry.get()
        targetFileName = self.outputEntry.get()

    def next(self):
        global sourceFileName, targetFileName
        if sourceFileName == None:
            sourceFileName = 'source_code_test1.py'
        try:
            readFile(sourceFileName)
        except:
            root2 = Tk()
            my_gui = fileNameCollectorError(root2)
            root2.mainloop()
        print('here')
        os._exit(0)

class fileNameCollectorError(fileNameCollector):

    def __init__(self, master):
        
        super().__init__(master)

        self.label4 = Label(master, text='Please use a valid file name or leave input file blank!').grid(row=3, columnspan=2)


# draws background, title, constant shapes
def drawTitleBG(app, canvas):
    fontSize = min(app.width, app.height) // 25
    canvas.create_rectangle(0, 0, app.width, app.height, fill = '#BA91BB')
    canvas.create_rectangle(app.margin, app.margin, app.width - app.margin, 
                            app.height - app.margin, fill = '#E2D2E6', width = 0)
    canvas.create_text(app.width/2, app.height/10, fill = '#000035', font = f'ComicSansMS {fontSize} bold',
                    text = app.title, anchor = 's')
    canvas.create_line(app.margin * 4, app.height/10 + 5, app.width - app.margin * 4, 
                    app.height/10 + 5, fill = '#000035', width = 2)
    canvas.create_text(app.width/2, app.height/8 + 10, fill = '#000035', 
                        font = f'ComicSansMS {int(fontSize/1.5)} bold',
                        text = app.subheader)



def getDimensions(app):
    margin = min(app.width, app.height) // 30
    return margin


# Main title page
class MainPage(Page):

    def __init__(self, master):
        pass

    def appStarted(app):
        app.margin = getDimensions(app)
        app.title = 'Code Modifier'
        app.key = 'r'
        app.subheader = '\'Q\' to quit'
    
    def keyPressed(app, event):
        app.key = event.key.lower()
        if app.key == 'q':
            Exit(width=400, height=400)
        elif app.key == 'c':
            Compress(width=600, height=800)
        elif app.key == 'b':
            Style(width=600, height=800)

    def drawTitlePage(app, canvas):
        fontSize = min(app.width, app.height) // 30
        canvas.create_text(app.width/2, app.height/2, anchor = 'c', font = f'ComicSansMS {fontSize}',
                        width = app.width/1.5,
                        text = 'Please select \'c\' to Compress or \'b\' to Beautify Code')

    def redrawAll(app, canvas):
        drawTitleBG(app, canvas)
        app.drawTitlePage(canvas)



class CodeModifier(Frame):

    def __init__(self):
        Frame.__init__(self)
        mainPage = fileNameCollector(self)

        mainPage.show()

app = Tk()
app.title = 'Code Modifier'
app.mainloop()