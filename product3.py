from tkinter import *
import sys, os

# citation https://stackoverflow.com/questions/14817210/using-buttons-in-tkinter-to-navigate-to-different-pages-of-the-application

sourceFileName = None
targetFileName = None

class Page(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
    def show(self):
        self.lift()

class fileNameCollector(Page):
    
    def __init__(self, *args, **kwargs):
        
        Page.__init__(self, *args, **kwargs)
        
        self.label = Label(self, text='Please input file names (must be existing directory for source file)\nIf no file name saved, sample files will be used'
                        ).grid(row=0, columnspan=2)

        self.label2 = Label(self, text='Source File Name').grid(row=1, column=0, sticky='e')
        self.inputEntry = Entry(self)
        self.inputEntry.grid(row=1, column=1, sticky='w')
        
        self.label3 = Label(self, text='Target File Name').grid(row=2, column=0, sticky='e')
        self.outputEntry = Entry(self)
        self.outputEntry.grid(row=2, column=1, sticky='w')

        self.label4 = Label(self, text='Save the file names if you want then click continue').grid(row=3, columnspan=2)

        self.saveButton = Button(self, text="Save", command=self.save).grid(row=4, column=0, sticky='e')

        self.continueButton = Button(self, text="Continue", command=self.next).grid(row=4, column=1, sticky='w')

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
            self.lower()
            print('here')

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
    return app.width, app.height, margin


# Main title page
class MainPage(Page):


    def __init__(self, *args, **kwargs):

        Page.__init__(self, *args, **kwargs)
       
        self.canvas = Canvas(self)

        self.canvas.pack(fill=BOTH, expand=YES)

        # self.width, self.height, self.margin = getDimensions(self)
        # drawTitleBG(self.canvas, self.canvas)


class Page3(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)
       label = Label(self, text="This is page 3")
       label.pack(side="top", fill="both", expand=True)

class MainView(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        inputPage = fileNameCollector(self)
        p2 = MainPage(self)
        p3 = Page3(self)

        buttonframe = Frame(self)
        container = Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        inputPage.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p3.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        b1 = Button(buttonframe, text="Page 1", command=inputPage.lift)
        b2 = Button(buttonframe, text="Page 2", command=p2.lift)
        b3 = Button(buttonframe, text="Page 3", command=p3.lift)

        b1.pack(side="left")
        b2.pack(side="left")
        b3.pack(side="left")

        p2.show()
        inputPage.show()

def run():
    root = Tk()
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("400x400")
    root.mainloop()