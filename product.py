# # # # # # # # # # # # # # # # # # # # # # # #
#                                             #
#               Code Modifier                 #
#                                             #
# # # # # # # # # # # # # # # # # # # # # # # # 

from compress import *
from style import *
from product_helper import *
from product_style_editor import *

inputFile, targetFile = None, None

def run():

    def getFiles():
        global inputFile, targetFile
        inputFile, targetFile = runFileNameCollector()

        # set default files
        if inputFile == None:
            inputFile = 'source_code_test1.py'
        if targetFile == None:
            targetFile = 'product_test.py'

    getFiles()
    CodeModifier(width=600, height=800)


''' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Start of Main User Interface Code~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'''

# default class for each page to inherit from
class Page(App):

    def appStarted(app):
        app.margin = app.getDimensions()
        app.subheader = None
        app.timerDelay = 50
        app.loading = False
        app.bgColor = 'white'
        app.marginColor = 'white'
        app.txtColor = '#000035'
        app.largeFontSize = min(app.width, app.height) // 35
        app.font = f'ComicSansMS {app.largeFontSize} bold'

    # returns margin size
    def getDimensions(app):
        margin = min(app.width, app.height) // 30
        return margin

    # draws background, title, constant shapes
    def drawTitleBG(app, canvas):
        fontSize = min(app.width, app.height) // 25
        canvas.create_rectangle(0, 0, app.width, app.height, fill = app.marginColor)
        canvas.create_rectangle(app.margin, app.margin, app.width - app.margin, 
                                app.height - app.margin, fill = app.bgColor, width = 0)
        canvas.create_text(app.width/2, app.height/9, fill = app.txtColor, font = f'ComicSansMS {fontSize} bold',
                        text = app.title, anchor = 's')
        canvas.create_line(app.margin * 4, app.height/9 + 10, app.width - app.margin * 4, 
                        app.height/9 + 10, fill = app.txtColor, width = 2)
        if app.subheader:
            canvas.create_text(app.width/2, app.height/8 + 20, fill = '#000035', 
                                font = f'ComicSansMS {int(fontSize/2)} bold',
                                text = app.subheader)

    def inBounds(app, bounds, x, y):
        return x >= bounds[0] and x <= bounds[2] and y <= bounds[3] and y >= bounds[1]

    def createButton(app, canvas, coords, text, **kwargs):
        x1, y1, x2, y2 = coords
        if 'color' in kwargs: color = kwargs['color']
        else: color = 'white'
        if 'font' in kwargs: font = kwargs['font']
        else: font = 'Arial 20 bold'
        canvas.create_rectangle(x1, y1, x2, y2, fill=color, width=.5)
        canvas.create_text( (x1 + x2) / 2, (y1 + y2) / 2, text=text, font=font)


    def drawLoading(app, canvas):
        canvas.create_text(app.width * 0.85, app.height * 0.94, text='Loading...', font='14')
        if not app.loading:
            canvas.create_rectangle(app.width * 0.78, app.height * 0.88, 
                                    app.width * 0.94, app.height * 0.96, fill=app.bgColor, width=0)


# Main title page
class CodeModifier(Page):

    def appStarted(app):
        super().appStarted()
        app.title = 'Code Modifier'
        app.subheader = 'a programming tool by Shivank Joshi'
        app.bgColor = '#EFC9AF'
        app.marginColor = '#BB8C6B'
        app.key = 'r'

        app.compressButton = (app.width * .15, app.height * 0.19, app.width * .85, app.height * 0.34)
        app.styleButton = (app.width * .15, app.height * 0.38, app.width * .85, app.height * 0.53)
        app.fileButton = (app.width * .15, app.height * 0.57, app.width * .85, app.height * 0.72)
        app.quitButton = (app.width * .15, app.height * 0.76, app.width * .85, app.height * 0.91)
    
    def timerFired(app):
        if app.loading:
            if app.key == 'c':
                Compress(width=600, height=800)
            elif app.key == 'b':
                Style(width=600, height=800)

    def keyPressed(app, event):
        app.key = event.key.lower()
        if app.key == 'q':
            Exit(width=400, height=400)
        elif app.key == 'c':
            app.loading = True
        elif app.key == 'b':
            app.loading = True

    def mousePressed(app, event):
        if app.inBounds(app.compressButton, event.x, event.y):
            app.loading = True
            app.key = 'c'
        elif app.inBounds(app.styleButton, event.x, event.y):
            app.loading = True
            app.key = 'b'
        elif app.inBounds(app.quitButton, event.x, event.y):
            Exit(width=400, height=400)
        elif app.inBounds(app.fileButton, event.x, event.y):
            run()
            

    def drawTitlePage(app, canvas):
        app.createButton(canvas, app.compressButton, 'Compress',
                        font=f'ComicSansMS {app.largeFontSize + 5} bold', color='#6DD47E')
        app.createButton(canvas, app.styleButton, 'Stylize', 
                        font=f'ComicSansMS {app.largeFontSize + 5} bold', color='#41B0C2')
        app.createButton(canvas, app.quitButton, 'Quit', 
                        font=f'ComicSansMS {app.largeFontSize + 5} bold', color='#D85454')
        app.createButton(canvas, app.fileButton, 'Change Files',
                        font=f'ComicSansMS {app.largeFontSize + 5} bold', color='#EDAFE3')
        

    def redrawAll(app, canvas):
        app.drawTitleBG(canvas)
        app.drawLoading(canvas)
        app.drawTitlePage(canvas)


# Compress Page
class Compress(Page):

    def appStarted(app):
        super().appStarted()
        app.title = 'Compress'
        app.bgColor = '#FFA781'
        app.marginColor = '#CA8669'
        app.key = 'r'
        app.inputFile = inputFile
        app.code = compressCode(inputFile)
        app.codeAlt = compressCode(inputFile, False, True)

        app.previewButton = (app.width * .15, app.height * 0.2, app.width * .85, app.height * 0.38)
        app.writeButton = (app.width * .15, app.height * 0.42, app.width * .48, app.height * 0.6)
        app.writeButton2 = (app.width * .52, app.height * 0.42, app.width * .85, app.height * 0.6)
        app.backButton = (app.width * .15, app.height * 0.64, app.width * .48, app.height * 0.82)
        app.quitButton = (app.width * .52, app.height * 0.64, app.width * .85, app.height * 0.82)
   
    
    def keyPressed(app, event):
        app.key = event.key.lower()
                

    def mousePressed(app, event):
        if app.inBounds(app.previewButton, event.x, event.y):
            runPreviewGUI(app.code)
        elif app.inBounds(app.writeButton, event.x, event.y):
            writeFile(targetFile, app.code)
            SuccessCompress(width=400, height=400)
        elif app.inBounds(app.writeButton2, event.x, event.y):
            writeFile(targetFile, app.codeAlt)
            SuccessCompress(width=400, height=400)
        elif app.inBounds(app.quitButton, event.x, event.y):
            Exit(width=400, height=400)
        elif app.inBounds(app.backButton, event.x, event.y):
            CodeModifier(width=600, height=800)


    def redrawAll(app, canvas):
        app.drawTitleBG(canvas)
        app.createButton(canvas, app.previewButton, 'Preview Compressed Code', font=app.font, color='#96A7D3')
        app.createButton(canvas, app.writeButton, 'Write Code to\n   Target File', 
                        font='ComicSansMS 14 bold', color='#D572A4')
        app.createButton(canvas, app.writeButton2, ' Write Code To\n    Target File\n (keep function \n       names)', 
                        font='ComicSansMS 14 bold', color='#D572A4')
        app.createButton(canvas, app.quitButton, 'Quit', font=app.font, color='#D85454')
        app.createButton(canvas, app.backButton, '   Back to\nMain Menu', font=app.font, color='#9E9794')
       

# Style page
class Style(Page):

    def appStarted(app):
        super().appStarted()
        app.title = 'Style'
        app.bgColor = '#82B089'
        app.marginColor = '#678A6D'
        app.txtColor = '#000035'
        app.key = 'r'
        app.code, app.analysis = doStyle(inputFile)

        app.previewButton = (app.width * .15, app.height * 0.17, app.width * .85, app.height * 0.32)
        app.analysisButton = (app.width * .15, app.height * 0.36, app.width * .85, app.height * 0.51)
        app.writeButton = (app.width * .15, app.height * 0.55, app.width * .85, app.height * 0.7)
        app.quitButton = (app.width * .52, app.height * 0.74, app.width * .85, app.height * 0.89)
        app.backButton = (app.width * .15, app.height * 0.74, app.width * .48, app.height * 0.89)
    
    def keyPressed(app, event):
        app.key = event.key.lower()
        
    def mousePressed(app, event):
        if app.inBounds(app.previewButton, event.x, event.y):
            runPreviewGUI(app.code)
        elif app.inBounds(app.analysisButton, event.x, event.y):
            app.code = runAllStyle(app.code, app.analysis)
        elif app.inBounds(app.writeButton, event.x, event.y):
            writeFile(targetFile, app.code)
            SuccessStyle(width=400, height=400)
        elif app.inBounds(app.quitButton, event.x, event.y):
            Exit(width=400, height=400)
        elif app.inBounds(app.backButton, event.x, event.y):
            CodeModifier(width=600, height=800)

    
    def redrawAll(app, canvas):
        app.drawTitleBG(canvas)
        
        app.createButton(canvas, app.previewButton, 'Preview Stylized Code', 
                        font=app.font, color='#55B2A5')
        app.createButton(canvas, app.analysisButton, 'View More Suggestions',
                        font=app.font, color='#BBA6D5')
        app.createButton(canvas, app.writeButton, 'Write Code to Target File', 
                        font=app.font, color='#E3AFC4')
        app.createButton(canvas, app.quitButton, 'Quit', 
                        font=app.font, color='#D85454')
        app.createButton(canvas, app.backButton, '   Back to\nMain Menu', 
                        font=app.font, color='#9E9794')


# successful write screen
class SuccessCompress(Page):

    def appStarted(app):
        super().appStarted()
        app.title = 'Code Successfully Written To Target File!'
    
    def mousePressed(app, event):
        Compress(width=600, height=800)

    def keyPressed(app, event):
        Compress(width=600, height=800)

    def redrawAll(app, canvas):
        canvas.create_rectangle(0, 0, app.width, app.height, fill = '#BA91BB')
        canvas.create_rectangle(app.margin, app.margin, app.width - app.margin, 
                                app.height - app.margin, fill = '#E2D2E6', width = 0)
        canvas.create_text(app.width/2, app.height/2, text = app.title, width = app.width/1.5, 
                           font = 'ComicSansMS 20 bold', fill = '#000035')


class SuccessStyle(SuccessCompress):

    def timerFired(app):
        if app.loading:
            Style(width=600, height=800)

    def mousePressed(app, event):
        app.loading = True
        
    def keyPressed(app, event):
        app.loading = True

    def redrawAll(app, canvas):
        super().redrawAll(canvas)
        if app.loading:
            app.drawLoading(canvas)

# exit / thank you screen
class Exit(Page):

    def appStarted(app):
        super().appStarted()
        app.title = 'Thank you, Come Again!'
        app.caption = 'Special Thanks To:\n Mukundh Balajee'
    
    def mousePressed(app, event):
        app.quit()
        os._exit(0) # used to suppress errors

    def keyPressed(app, event):
        app.quit()
        os._exit(0) # used to suppress errors

    def redrawAll(app, canvas):
        canvas.create_rectangle(0, 0, app.width, app.height, fill = '#322D3C')
        canvas.create_rectangle(app.margin, app.margin, app.width - app.margin, 
                                app.height - app.margin, fill = '#C28AA3', width = 0)
        canvas.create_text(app.width/2, app.height/2 - 10, text = app.title, anchor = 's',
                            font = 'ComicSansMS 20 bold', fill = '#322D3C')
        canvas.create_text(app.width/2, app.height/2 + 35, text = app.caption,
                            font = 'ComicSans 16 bold', fill = '#322D3C')


run()