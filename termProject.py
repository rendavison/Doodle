# events-example0.py taken from 112 course website
# contained barebones timer, mouse events, keyboard events, and run function

from tkinter import *
from tkinter import messagebox
import random, math, string, copy

####################################
# init
####################################

def init(data):
    data.mode = "splashScreen"
    data.editingRGB = False
    data.editingWeight = False
    data.rgbTyping = ""
    data.weightTyping = ""
    data.selectedRGB = "black"
    data.selectedWeight = "black"
    data.fill = "black"
    data.weight = 1
    data.doodle = Freeform(data.fill, data.weight)
    data.rotatedDoodle = Rotated(data.fill, data.weight)
    data.lines = []
    data.rotatedLines = []
    data.rotation = 3
    data.margin = 20
    data.sides = 3
    data.currentShape = Shape(data.fill, data.sides)
    data.shapes = []
    data.stamp = None
    data.stamps = []
    data.stampFills = ["black", "red", "blue", "green"]
    data.rotated = False
    data.theta = math.pi/12

####################################
# helper functions
####################################

#function taken from 112 course website and modified by me
def rgbString(rgb):
    try:
        colors = rgb.split(",")
        red, green, blue = colors
        red, green, blue = red.strip(), green.strip(), blue.strip()
        for color in [red, green, blue]:
            assert(len(color) <= 3)
        red, green, blue = int(red), int(green), int(blue)
        for color in [red, green, blue]:
            assert(0 <= color <= 250)
        return "#%02x%02x%02x" % (red, green, blue)
    except:
        messagebox.showinfo("Error!", "That is not a valid rgb code!")

#lets the user know what mode they're on
def drawMode(canvas, data):
    canvas.create_text(data.margin/2, data.height-data.margin*1.2, fill="black", \
    anchor="nw", text=data.mode, font="Arial 20 bold")

def drawControls(canvas, data):
    #default colors
    canvas.create_rectangle(data.margin, data.margin, data.margin*2, \
    data.margin*2, fill="black")
    canvas.create_rectangle(data.margin, data.margin*3, data.margin*2, \
    data.margin*4, fill="red")
    canvas.create_rectangle(data.margin, data.margin*5, data.margin*2, \
    data.margin*6, fill="green")
    canvas.create_rectangle(data.margin, data.margin*7, data.margin*2, \
    data.margin*8, fill="blue")
    
    #custom rgb color input
    canvas.create_text(data.margin*3, data.margin, fill="black", anchor="nw", \
    text="Input your own rgb value (rrr, ggg, bbb):")
    canvas.create_rectangle(data.margin*3, data.margin*2, data.margin*10, \
    data.margin*3, fill="white", width=1, outline=data.selectedRGB)
    canvas.create_text(data.margin*3+5, data.margin*2+3, fill="black", \
    text=data.rgbTyping, anchor="nw")
    
    #line weight controls
    canvas.create_text(data.margin*3, data.margin*4, fill="black", anchor="nw", \
    text="Input your line thickness:")
    canvas.create_rectangle(data.margin*3, data.margin*5, data.margin*10, \
    data.margin*6, fill="white", width=1, outline=data.selectedWeight)
    canvas.create_text(data.margin*3+5, data.margin*5+3, fill="black", \
    text=data.weightTyping, anchor="nw")
    
    #update button
    canvas.create_rectangle(data.margin*3, data.margin*7, data.margin*6,\
    data.margin*8, fill="white", width=1)
    canvas.create_text(data.margin*3+4, data.margin*7+3, fill="black", \
    text="UPDATE", anchor="nw")

def selectControls(event, data):
    #click default colors
    if 20 <= event.x <= 40 and 20 <= event.y <= 40: data.fill = "black"
    elif 20 <= event.x <= 40 and 60 <= event.y <= 80: data.fill = "red"
    elif 20 <= event.x <= 40 and 100 <= event.y <= 120: data.fill = "green"
    elif 20 <= event.x <= 40 and 140 <= event.y <= 160: data.fill = "blue"
    
    #input custom values
    elif 60 <= event.x <= 200 and 40 <= event.y <= 60:
        data.editingRGB = True
        data.selectedRGB = "blue"
    elif 60 <= event.x <= 200 and 100 <= event.y <= 120:
        data.editingWeight = True
        data.selectedWeight = "blue"

    #update custom values
    elif (60 <= event.x <= 120 and 140 <= event.y <= 160 or \
    event.keysym == "Return") and data.editingRGB:
        data.editingRGB = False
        data.fill = rgbString(data.rgbTyping)
        data.rgbTyping = ""
        data.selectedRGB = "black"
    elif ((60 <= event.x <= 120 and 140 <= event.y <= 160) or \
    event.keysym == "Return") and data.editingWeight:
        data.editingWeight = False
        try:
            data.weight = int(data.weightTyping)
            assert(data.weight > 0)
            data.weightTyping = ""
            data.selectedWeight = "black"
        except:
            data.weight = 1
            messagebox.showinfo("Error!", "That's not a valid line weight!")
            data.weightTyping = ""
            data.selectedWeight = "black"

####################################
# line and shape object classes
####################################

#standard free draw line object
class Freeform(object):
    def __init__(self, fill, weight):
        self.coords = []
        self.fill = fill
        self.weight = weight
        self.center = (300, 300)
    
    def getCoordinates(self, x, y):
        self.coords.append((x,y))
    
    def getCoordList(self):
        return self.coords
    
    def drawLine(self, canvas):
        prevX, prevY = None,None
        for coords in range(len(self.coords)):
            if prevX == None or prevY == None:
                prevX = self.coords[coords][0]
                prevY = self.coords[coords][1]
            else:
                x = self.coords[coords][0]
                y = self.coords[coords][1]
                canvas.create_line(prevX, prevY, x, y, fill=self.fill, \
                width=self.weight)
                prevX, prevY = x, y

#rotated lines for rotate mode
class Rotated(Freeform):
    def rotateCoords(self, angles):
        
        def distance(x1, x2, y1, y2):
            return math.sqrt((x2-x1)**2+(y2-y1)**2)
        
        #Thank you to Chris Grossack for helping debug some of my trig errors
        rotatedImage = []
        for pair in self.coords:
            x, y = pair
            cx, cy = self.center
            polarX, polarY = x-cx, y-cy
            r = distance(cx, cy, polarX, polarY)
            circle = 360
            rotation = circle/angles
            theta = math.degrees(math.atan(polarY/polarX))
            for i in range(1, angles+1):
                newX = r*math.cos(math.radians(theta+rotation*i)) + cx
                newY = r*math.sin(math.radians(theta+rotation*i)) + cy
                rotatedImage.append((newX, newY))
        self.coords = rotatedImage

#polygons for shape mode
class Shape(object):
    def __init__(self, fill, sides):
        self.fill = fill
        self.points = [(0,0)]
        self.sideLength = 50
        self.sides = sides
    
    #generalized formula to draw polygon points
    def getPoints(self, x, y):
        circle = 360
        rotation = circle/self.sides
        points = []
        for i in range(self.sides):
            newX = x + self.sideLength*math.cos(math.radians(rotation*i))
            newY = y + self.sideLength*math.sin(math.radians(rotation*i))
            points.append((newX, newY))
        self.points = points
    
    def pointsList(self):
        return self.points
    
    def getFill(self):
        return self.fill
    
    #the center is exactly where the mouse clicks, so:
    def findCenter(self, x, y):
        return (x, y)
    
    #center adjustment code help from      
    #http://stackoverflow.com/questions/28458145/
    #rotate-2d-polygon-without-changing-its-position
    def rotate(self, center, theta):
        newPoints = []
        cx, cy = center
        for point in self.points:
            x, y = point
            cx, cy = center
            x -= cx
            y -= cy
            newX = x*math.cos(theta)-y*math.sin(theta)
            newY = x*math.sin(theta)+y*math.cos(theta)
            newX += cx
            newY += cy
            newPoints.append((newX, newY))
        self.points = newPoints
    
    def drawShape(self, canvas):
        canvas.create_polygon(self.points, fill=self.fill)

#stamps for stamp mode
class Stamp(Shape):  
    def __init__(self, shape, sides, fill):
        self.polygons = shape
        self.sideLength = 50
        self.sides = sides
        self.totalPoints = []
        self.points = [(0, 0)]
        self.fill = fill
  
    def getPointLists(self, x, y):
        refShape = self.polygons[0]
        refX, refY = refShape.pointsList()[0]
        deltaX, deltaY = x-refX, y-refY
        for shape in self.polygons:
            displaced = []
            for coord in shape.pointsList():
                oldX, oldY = coord
                newX, newY = oldX+deltaX, oldY+deltaY
                displaced.append((newX, newY))
            self.totalPoints.append(displaced)
    
    def drawStamp(self, canvas):
        for list in self.totalPoints:
            canvas.create_polygon(list, fill=self.fill)

####################################
# mode dispatcher
####################################

def mousePressed(event, data):
    if (data.mode == "splashScreen"): splashScreenMousePressed(event, data)
    elif (data.mode == "draw"): drawMousePressed(event, data)
    elif (data.mode == "rotate"): rotateMousePressed(event, data)
    elif (data.mode == "shape"): shapeMousePressed(event, data)
    elif (data.mode == "stamp"): stampMousePressed(event, data)
    elif (data.mode == "help"): helpMousePressed(event, data)

def drag(event, data):
    if (data.mode == "splashScreen"): splashScreenDrag(event, data)
    elif (data.mode == "draw"): drawDrag(event, data)
    elif (data.mode == "rotate"): rotateDrag(event, data)
    elif (data.mode == "shape"): shapeDrag(event, data)
    elif (data.mode == "stamp"): stampDrag(event, data)
    elif (data.mode == "help"): helpDrag(event, data)
    
def releaseMouse(event, data):
    if (data.mode == "splashScreen"): splashScreenReleaseMouse(event, data)
    elif (data.mode == "draw"): drawReleaseMouse(event, data)
    elif (data.mode == "rotate"): rotateReleaseMouse(event, data)
    elif (data.mode == "shape"): shapeReleaseMouse(event, data)
    elif (data.mode == "stamp"): stampReleaseMouse(event, data)
    elif (data.mode == "help"): helpReleaseMouse(event, data)

def keyPressed(event, data):
    if (data.mode == "splashScreen"): splashScreenKeyPressed(event, data)
    elif (data.mode == "draw"): drawKeyPressed(event, data)
    elif (data.mode == "rotate"): rotateKeyPressed(event, data)
    elif (data.mode == "shape"): shapeKeyPressed(event, data)
    elif (data.mode == "stamp"): stampKeyPressed(event, data)
    elif (data.mode == "help"): helpKeyPressed(event, data)

def timerFired(data):
    if (data.mode == "splashScreen"): splashScreenTimerFired(data)
    elif (data.mode == "draw"): drawTimerFired(data)
    elif (data.mode == "rotate"): rotateTimerFired(data)
    elif (data.mode == "shape"): shapeTimerFired(data)
    elif (data.mode == "stamp"): stampTimerFired(data)
    elif (data.mode == "help"): helpTimerFired(data)

def redrawAll(canvas, data):
    if (data.mode == "splashScreen"): splashScreenRedrawAll(canvas, data)
    elif (data.mode == "draw"): drawRedrawAll(canvas, data)
    elif (data.mode == "rotate"): rotateRedrawAll(canvas, data)
    elif (data.mode == "shape"): shapeRedrawAll(canvas, data)
    elif (data.mode == "stamp"): stampRedrawAll(canvas, data)
    elif (data.mode == "help"): helpRedrawAll(canvas, data)
    
####################################
# splash screen
####################################

def splashScreenMousePressed(event, data):
    pass
    
def splashScreenDrag(event, data):
    pass

def splashScreenReleaseMouse(event, data):
    pass

def splashScreenKeyPressed(event, data):
    data.mode = "help"

def splashScreenTimerFired(data):
    pass

def splashScreenRedrawAll(canvas, data):
    #background
    canvas.create_rectangle(0, 0, data.width, data.height, fill="lightBlue", \
    width=0)
    
    #welcome text
    canvas.create_text(data.width//2, data.height//2, fill="black", \
    font="Arial 50 bold", text="Welcome to Doodle!")
    canvas.create_text(data.width//2, data.height//2+50, fill="black", \
    font="Arial 30 bold", text="Press any key to begin")

####################################
# help screen
####################################

def helpMousePressed(event, data):
    pass
    
def helpDrag(event, data):
    pass

def helpReleaseMouse(event, data):
    pass

def helpKeyPressed(event, data):
    #go to three different modes
    if event.char == "d": data.mode = "draw"
    elif event.char == "r": data.mode = "rotate"
    elif event.char == "s": data.mode = "shape"

def helpTimerFired(data):
    pass

def helpRedrawAll(canvas, data):
    drawMode = """Free draw by dragging the mouse. You can change the color of your line by selecting\nthe default colors on the left side of the screen, or by inputting a valid RGB color value.\nYou can also change the weight of the line by inputting a number in the line weight box.\nYou can clear what you've drawn at any time by hitting 'c' and undo you last line by\nhitting 'u'. Draw mode is the default mode. You can access it at any time by hitting 'd'."""
    
    rotateMode = """Access this mode by hitting 'r'. The basic controls in rotate mode are the same as those\nin draw mode.  Additionally, you can select the number of points of rotational symmetry\nby hitting the numbers 2-6 on your keyboard."""
    
    shapeMode = """Access this mode by hitting 's'. Shape/stamp mode allows you to use regular polygons to\ngenerate stamps. Shapes appear on click. Press 3-6 on your keyboard to change\nthe number of sides and rotate the angle of the polygon by hitting your spacebar.\nWhen you like what you've made, hit Enter and stamp away! Press 'c' to clear and hit\nany other button to go back to shape mode."""
    
    canvas.create_text(data.width//2, data.margin*2, fill="black", \
    font="Arial 35 bold", text="Instructions")
    
    canvas.create_text(data.margin, data.margin*4.5, fill="black", anchor="nw", \
    font="Arial 20 bold", text="Draw Mode:")
    canvas.create_text(data.margin, data.margin*6, fill="black", anchor="nw", \
    font="Arial 15", text=drawMode)
    
    canvas.create_text(data.margin, data.margin*11.5, fill="black", anchor="nw", \
    font="Arial 20 bold", text="Rotate Mode:")
    canvas.create_text(data.margin, data.margin*13, fill="black", anchor="nw", \
    font="Arial 15", text=rotateMode)
    
    canvas.create_text(data.margin, data.margin*17, fill="black", anchor="nw", \
    font="Arial 20 bold", text="Shape/Stamp Mode:")
    canvas.create_text(data.margin, data.margin*18.5, fill="black", anchor="nw", \
    font="Arial 15", text=shapeMode)
    
    canvas.create_text(data.width//2, data.margin*26, fill="black", \
    font="Arial 20 bold", text="Select any mode to go back.\nAccess this " + \
    "screen at any time by hitting 'h'.")
    
####################################
# draw mode
####################################

def drawMousePressed(event, data):
    data.doodle = Freeform(data.fill, data.weight)
    selectControls(event, data)

def drawDrag(event, data):
    data.doodle.getCoordinates(event.x, event.y)

def drawReleaseMouse(event, data):
    data.lines.append(data.doodle)
    #resets lines to take more inputs
    data.doodle = Freeform(data.fill, data.weight)

def drawKeyPressed(event, data):
    selectControls(event, data)
    
    #code that allows typing
    if data.editingRGB:
        data.rgbTyping += event.char
        if event.keysym == "BackSpace":
            data.rgbTyping = data.rgbTyping[:-2]
    elif data.editingWeight:
        data.weightTyping += event.char
        if event.keysym == "BackSpace":
            data.weightTyping = data.weightTyping[:-2]
    
    #switch modes, clear, undo
    else:
        if event.char == "c": data.lines = []
        elif event.char == "u": data.lines.pop()
        elif event.char == "h": data.mode = "help"
        elif event.char == "r": data.mode = "rotate"
        elif event.char == "s": data.mode = "stamp"
    
def drawTimerFired(data):
    pass

def drawRedrawAll(canvas, data):
    drawMode(canvas, data)
    
    #this draws along with you
    data.doodle.drawLine(canvas)
    
    #this draws previous lines
    for line in data.lines:
        line.drawLine(canvas)
    
    drawControls(canvas, data)
    
####################################
# rotate mode
####################################

def rotateMousePressed(event, data):
    data.rotatedDoodle = Rotated(data.fill, data.weight)
    selectControls(event, data)
    
def rotateDrag(event, data):
    data.rotatedDoodle.getCoordinates(event.x, event.y)

def rotateReleaseMouse(event, data):
    data.rotatedDoodle.rotateCoords(data.rotation)
    data.rotatedLines.append(data.rotatedDoodle)
    #resets line to take more inputs
    data.rotatedDoodle = Rotated(data.fill, data.weight)

def rotateKeyPressed(event, data):
    selectControls(event, data)
    
    #code that allows typing
    if data.editingRGB:
        data.rgbTyping += event.char
        if event.keysym == "BackSpace":
            data.rgbTyping = data.rgbTyping[:-2]
    elif data.editingWeight:
        data.weightTyping += event.char
        if event.keysym == "BackSpace":
            data.weightTyping = data.weightTyping[:-2]
   
    #switch modes, clears, undos and points of rotational symmetry
    else:
        if event.char == "c": data.rotatedLines = []
        elif event.char == "u": data.rotatedLines.pop()
        elif event.char == "d": data.mode = "draw"
        elif event.char == "h": data.mode = "help"
        elif event.char == "s": data.mode = "shape"
        elif event.char == "2": data.rotation = 2
        elif event.char == "3": data.rotation = 3
        elif event.char == "4": data.rotation = 4
        elif event.char == "5": data.rotation = 5
        elif event.char == "6": data.rotation = 6

def rotateTimerFired(data):
    pass

def rotateRedrawAll(canvas, data):
    drawMode(canvas, data)
    
    #rotation label
    canvas.create_text(data.margin*3.2, data.height-data.margin*1.2, fill="black", \
    anchor="nw", text=": " + str(data.rotation), font="Arial 20 bold")
    
    #shows your current unrotated line as you draw
    data.rotatedDoodle.drawLine(canvas)
    
    #draws your previous rotated lines
    for line in data.rotatedLines:
        line.drawLine(canvas)
    
    drawControls(canvas, data)

####################################
# shape mode
####################################

def shapeMousePressed(event, data):
    data.currentShape = Shape(data.fill, data.sides)
    data.currentShape.getPoints(event.x, event.y)
    data.theta = math.pi/12

def shapeDrag(event, data):
    data.currentShape.getPoints(event.x, event.y)
    if data.rotated:
        cx, cy = data.currentShape.findCenter(event.x, event.y)
        data.currentShape.rotate((cx, cy), data.theta)
    
def shapeReleaseMouse(event, data):
    data.shapes.append(data.currentShape)
    
    #resets shape to take in a potentially different shape
    data.currentShape = Shape(data.fill, data.sides)
    
    data.rotated = False
    data.theta = math.pi/12

def shapeKeyPressed(event, data):
    
    #switches modes, clears, undos
    if event.char == "c": data.shapes = [] 
    elif event.char == "u": data.shapes.pop()
    elif event.char == "h": data.mode = "help"
    elif event.char == "d": data.mode = "draw"
    elif event.char == "r": data.mode = "rotate"
    
    #change number of polygon sides
    elif event.char == "3": 
        data.sides = 3
        data.fill = "black"
    elif event.char == "4": 
        data.sides = 4
        data.fill = "blue"
    elif event.char == "5": 
        data.sides = 5
        data.fill = "green"
    elif event.char == "6": 
        data.sides = 6
        data.fill = "red"
    
    #rotation
    elif event.keysym == "space":
        data.theta += math.pi/12
        data.currentShape.rotate(data.currentShape.findCenter(event.x, event.y), \
        data.theta)
        data.rotated = True
    
    #switch to stamp mode
    elif event.keysym == "Return":
        data.mode = "stamp"

def shapeTimerFired(data):
    pass

def shapeRedrawAll(canvas, data):
    #see the shape as your drag it
    data.currentShape.drawShape(canvas)

    #draws previous shapes
    for shape in data.shapes:
        shape.drawShape(canvas)
    
    drawMode(canvas, data)
    
    #shape label
    canvas.create_text(data.margin*3.35, data.height-data.margin*1.2, fill="black", \
    anchor="nw", text=": " + str(data.sides) + " sides", font="Arial 20 bold")
    
####################################
# stamp mode
####################################

def stampMousePressed(event, data):
    num = random.randint(0, len(data.stampFills)-1)
    data.stamp = Stamp(data.shapes, data.sides, data.stampFills[num])
    data.stamp.getPointLists(event.x, event.y)

def stampDrag(event, data):
    pass
    
def stampReleaseMouse(event, data):
    data.stamps.append(data.stamp)
    
def stampKeyPressed(event, data):
    #clears and goes back
    if event.char == "c": data.stamps = []
    else: data.mode = "shape"

def stampTimerFired(data):
    pass

def stampRedrawAll(canvas, data):
    #draws previous stamps    
    for stamp in data.stamps:
        stamp.drawStamp(canvas)
    
    drawMode(canvas, data)

####################################
# run function
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def dragWrapper(event, canvas, data):
        drag(event, data)
        redrawAllWrapper(canvas, data)
        
    def releaseMouseWrapper(event, canvas, data):
        releaseMouse(event, data)
        redrawAllWrapper(canvas, data)
    
    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<B1-Motion>", lambda event:
                             dragWrapper(event, canvas, data))
                            
    root.bind("<ButtonRelease-1>", lambda event:
                                   releaseMouseWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(600, 600)