import tkinter as tk
from tkinter import messagebox
import time
import sys

''' A* path finding algorithm '''

def resourcePath(fileName):
    if hasattr(sys, '_MEIPASS'):
        return f'{os.path.join(sys._MEIPASS, fileName)}'
    return f'{fileName}'

#Defining colours
NODE_COLOUR = 'white'
START_NODE_COLOUR = 'green3'
END_NODE_COLOUR = 'magenta'
LOCKED_NODE_COLOUR = 'red'
EXPLORED_NODE_COLOUR = 'green'
OBSTACLE_COLOUR = 'black'
PATH_COLOUR = 'deep sky blue'
GRID_FRAME_BG = 'aqua'

#Display strings
searchTermination = '\n' + ' Search Terminated! '.center(50, '*')
searchComplete = '\n' + ' Search Complete! '.center(50, '*')
pathNotFound = '\n' + ' Path to destination does not exist! '.center(51, '*')

class Node:
    def __init__(self, label):
        self.label = label
        info = label.grid_info()
        self.point = (info['row'], info['column'])
        self.updateColour(NODE_COLOUR)

    def __str__(self):

        details = f'''
Node details ---->
-------------
1. Point: {self.point}
2. G-Factor: {self.gFactor}
3. H-Factor: {self.hFactor}
4. F-Cost: {self.fCost}
    '''
        return details
    
    def getCosts(self, startVal):
        self.gFactor = startVal
        self.hFactor = self.getDistance(endNode)
        self.fCost = self.gFactor + self.hFactor

    def updateCosts(self, NODE):
        originalGFactor = NODE.gFactor
        calculatedGFactor = originalGFactor + self.getDistance(NODE)
        self.gFactor = calculatedGFactor
        self.fCost = self.gFactor + self.hFactor

    def updateColour(self, colour):
        self.label['bg'] = colour

    def isObstacle(self):
        return self.label['bg'] == OBSTACLE_COLOUR 

    def isFreeNode(self):
        return self.label['bg'] == NODE_COLOUR
        
    def getNeighbours(self, mat, nodes):
        row, col = self.point
        spots = [(row-1, col-1), (row-1, col), (row-1, col+1), (row, col-1),
                 (row, col+1), (row+1, col-1), (row+1, col), (row+1, col+1)
                 ]
        for spot in list(spots):
            try:
                point = mat[spot[0]][spot[1]]
                if spot[0] < 0 or spot[1] < 0 or point in OCCUPIED:
                    spots.remove(spot)
            except IndexError:
                spots.remove(spot)

        neighbourNodes = []
        for node in nodes:
            for spot in spots:
                if spot == node.point:
                    neighbourNodes.append(node)
                
        return neighbourNodes
    
    def getDistance(self, node, debugging=False):
        distanceRow = abs(self.point[0] - node.point[0])
        distanceCol = abs(self.point[1] - node.point[1])
        debug1 = f'''
***point: {self.point}
distanceRow: {distanceRow}
distanceCol: {distanceCol}
(distanceCol - distanceRow): {(distanceCol - distanceRow)}
distanceRow*14 + (distanceCol - distanceRow)*10: {distanceRow}*14 + {(distanceCol - distanceRow)}*10'''
        debug2 = f'''
***point: {self.point}
distanceRow: {distanceRow}
distanceCol: {distanceCol}
(distanceRow - distanceCol): {(distanceRow - distanceCol)}
distanceCol*14 + (distanceRow - distanceCol)*10: {distanceCol}*14 + {(distanceRow - distanceCol)}*10'''
        if distanceCol > distanceRow:
            if debugging:
                print(debug1)
            return distanceRow*14 + (distanceCol - distanceRow)*10
        if debugging:
            print(debug2)
        return distanceCol*14 + (distanceRow - distanceCol)*10
    def reset(self):
        self.updateColour(NODE_COLOUR)
        if hasattr(self, 'gFactor'):
            del self.gFactor, self.hFactor, self.fCost

toolTips = []
class CreateToolTip:
    def __init__(self, widget, text='widget info'):
        self.widget = widget
        self.text = text
        self.bg = 'yellow'
        self.font = ('Verdana', 15)
        self.funcid1 = self.widget.bind('<Enter>', self.enter, add='+')
        self.funcid2 = self.widget.bind('<Leave>', self.close)
        self.removed = False

    def enter(self, event=None):
        if self.removed:
            return
        x = y = 0
        x, y, cx, cy = self.widget.bbox('insert')
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        # creates a toplevel window
        self.tw = tk.Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry('+%d+%d' % (x, y))
        label = tk.Label(self.tw, text=self.text, justify='left',
                       bg=self.bg, relief='solid', borderwidth=1,
                       font=self.font)
        label.pack(ipadx=1)

    def close(self, event=None):
        if not hasattr(self, 'tw') or self.removed:
            return
        if self.tw:
            self.tw.destroy()

#Defining GUI elements
WINDOW_GEOMETRY = '700x700+300+50'
WINDOW_TITLE = 'A* Path finding algorithm'
WINDOW_BG = 'white'
FONT = ('Times New Roman', 20)
bold = ('bold',)
italic = ('italic',)
TEXT_BG = 'orange'
TEXT_FG = 'red'
BUTTON_BG = 'gold'
BUTTON_FG = 'red'
CHECKBTN_BG = 'lime'

window = tk.Tk()
window.title(WINDOW_TITLE)
window.geometry(WINDOW_GEOMETRY)
window.config(bg=WINDOW_BG)
window.resizable(False, False)
window.iconphoto(True, tk.PhotoImage(file=resourcePath('pathfindingIcon.png')))

#Matrix initialization UI
lf = tk.LabelFrame(window, text='Grid Size:', bg=TEXT_BG, fg=TEXT_FG,
                   font=FONT+bold)
lf.columnconfigure(0, weight=2)
lf.columnconfigure(1, weight=1)
DEFAULT_GRID_SIZE = 10
entry = tk.Entry(lf, font=FONT, justify='center', readonlybackground=WINDOW_BG)
entry.insert(0, DEFAULT_GRID_SIZE)
entry['state'] = 'readonly'
entry.grid(row=0, column=0)

def updateEntry(operator):
    result = eval(f'{entry.get()} {operator} 1')
    if result < 10:
        return
    entry['state'] = 'normal'
    entry.delete(0, 'end')
    entry.insert(0, result)
    entry['state'] = 'readonly'

buttonsFrame = tk.Frame(lf, bg=TEXT_BG)
plusBtn = tk.Button(buttonsFrame, bg='white', fg=TEXT_FG, text='+', font=FONT+bold, width=3,
                         command = lambda: updateEntry('+'))
plusBtn.grid(row=1, column=0, padx=20)
window.bind('<Up>', lambda e: updateEntry('+'))
 
minusBtn = tk.Button(buttonsFrame, bg='white', fg=TEXT_FG, text='-', font=FONT+bold, width=3,
                         command = lambda: updateEntry('-'))
minusBtn.grid(row=1, column=2)
window.bind('<Down>', lambda e: updateEntry('-'))
buttonsFrame.grid(row=0, column=1, sticky='w')
def resetWindow(event=None):
    global count, toggle
    msg = 'Window has been reset'
    print('\n' + '='*len(msg))
    print(msg)
    print('='*len(msg))
    count = 1
    toggle = False
    displayLogs['state'] = 'normal'
    gridSize = int(entry.get())
    prevSize = previousGridSize
    resetMsg1 = f'Resetting window...'
    generateMsg1 = f'Generating {gridSize}x{gridSize} grid...'
    tk.messagebox.showinfo('Grid generation', resetMsg1 if prevSize == gridSize else generateMsg1)

    startTime = time.time()
    if prevSize == gridSize:
        for node in nodes:
            node.reset()
        for toolTip in toolTips:
            toolTip.removed = True
        toolTips.clear()
        initializeMatrix(gridSize)
    else:
        beginInitializations(gridSize)
    resetMsg2 = f'Window reset complete!'
    generateMsg2 = f'{gridSize}x{gridSize} grid generation complete!'
    tk.messagebox.showinfo('Grid generation', resetMsg2 if prevSize == gridSize else generateMsg2)
    initString = f'\nInitialization complete in {time.time() - startTime}s\n'
    symbol = '='
    sys.stdout.write('\n\n' + symbol*len(initString) + initString + symbol*len(initString))
    
generateBtn = tk.Button(lf, bg=BUTTON_BG, fg=BUTTON_FG, text='Generate Grid', font=FONT,
                         activeforeground=BUTTON_FG, activebackground=BUTTON_BG,
                         command=resetWindow)
generateBtn.grid(row=1, column=0)

DISPLAY_LOGS = tk.IntVar()
tempFunction = lambda *args: None
print = None
def toggleDisplayLogs():
    global print
    display_state = 'Enabled' if DISPLAY_LOGS.get() else 'Disabled'
    sys.stdout.write(f'*** Display logs: {display_state} ***\n')
    print = tempFunction
    if DISPLAY_LOGS.get():
        del print
displayLogs = tk.Checkbutton(lf, bg=CHECKBTN_BG, fg=BUTTON_FG, text='Display logs in console',
                              disabledforeground=BUTTON_FG,
                              activebackground=CHECKBTN_BG, activeforeground=BUTTON_FG,
                              font=FONT, onvalue=1, offvalue=0, variable=DISPLAY_LOGS,
                              command=toggleDisplayLogs)
displayLogs.grid(row=1, column=1, sticky='sw')
lf.pack(fill='both')
toolsFrame = tk.Frame(window, bg=GRID_FRAME_BG)
choices = ['Draw Obstacles', 'Erase Obstacles']
DRAW_MODE = tk.StringVar(value=choices[0])
toolsBox = tk.OptionMenu(window, DRAW_MODE, *choices)
toolsBox.config(bg=TEXT_BG, fg=TEXT_FG, font=FONT)
menu = window.nametowidget(toolsBox.menuname)
menu.config(font=FONT, bg=BUTTON_BG, fg=BUTTON_FG)  # Set the dropdown menu's font
toolsBox.pack(fill='both')
toolsFrame.pack()
gridFrame = tk.Frame()
displayLabel = tk.Label(window, bg=GRID_FRAME_BG, fg=TEXT_FG, font=FONT, text='Initializing grid....')

nodes = []
matrix = []
def initializeGrid(gridSize):
    global count, gridFrame
    nodes.clear()
    gridFrame.destroy()
    displayLabel.pack(fill='both', expand=1)
    window.update()
    gridFrame = tk.Frame(window, bg=GRID_FRAME_BG, padx=20, pady=20)
    gridFrame.rowconfigure([i for i in range(gridSize)], weight=1)
    gridFrame.columnconfigure([j for j in range(gridSize)], weight=1)
    #Temporary message display label
    for i in range(gridSize):
        for j in range(gridSize):
            label = tk.Label(gridFrame, relief='sunken')
            label.grid(row=i, column=j, sticky='nsew')
            node = Node(label)
            nodes.append(node)
    count = 1
    
    #Binding all nodes to GUI events
    for node in nodes:
        node.label.bind('<Button-1>', lambda e, n=node: getStartEnd(n))
        node.label.bind('<Button-3>', lambda e, n=node: drawObstacles(n))
        node.label.bind('<Enter>', lambda e, n=node: getDrawMode(n))
    displayLabel.forget()
    gridFrame.pack(fill='both', expand=1)

DEFAULT_MATRIX_VAL = '0'
def initializeMatrix(gridSize):
    matrix.clear()
    for i in range(gridSize):
        matrix.append([DEFAULT_MATRIX_VAL for j in range(gridSize)])

previousGridSize = None        
def beginInitializations(gridSize):
    global previousGridSize
    initializeMatrix(gridSize)
    initializeGrid(gridSize)
    previousGridSize = gridSize
    
beginInitializations(DEFAULT_GRID_SIZE)
toggleDisplayLogs()
#GUI controls display
prompt = '''
Instructions
------------
Left-Click --> To select start/end points
Right-Click --> Draw an obstacle
Space --> Toggle obstacle draw, to enable drawing multiple obstacles
Enter --> Reset window/Generate Grid
Q/Esc --> Quit
F11 --> Full Screen
'''
messagebox.showinfo('GUI Controls - A* path finding', prompt)

window.focus_force()

count = 1
startNode = None
endNode = None
startPoint = 'A'
endPoint = 'B'
locked = 'x'
marked = '@@@'
obstacle = '|'
DEFAULT_MATRIX_VAL = '0'
OCCUPIED = [locked, marked, startPoint, obstacle]

def resetStart(event):
    global count, startNode, endNode
    startNode = endNode = None
    count = 1

def getDrawMode(node):
    if DRAW_MODE.get() == 'Draw Obstacles':
        toggledDraw(node)
    elif DRAW_MODE.get() == 'Erase Obstacles':
        eraseToggle(node)
    

def eraseToggle(node):
    if not toggle:
        return
    try:
        eraseObstacles(node)
    except RecursionError:
        sys.stdout.write('\nRecursion Error')
        entry['state'] = 'normal'
        entry.delete(0, 'end')
        entry.insert(0, DEFAULT_GRID_SIZE)
        resetWindow()
        
def eraseObstacles(node):
    global count
    #Alternative check: matrix[node.point[0]][node.point[1]] in OCCUPIED
    if count == 10 or (not node.isFreeNode):
        return
    node.updateColour(NODE_COLOUR)
    matrix[node.point[0]][node.point[1]] = DEFAULT_MATRIX_VAL
    window.update()
    
def getStartEnd(node):
    global count, startNode, endNode
    displayLogs['state'] = 'disabled'
    
    if count > 2 or (not node.isFreeNode()):
        return
    
    if count == 1:
        startNode = node
        startNode.updateColour(START_NODE_COLOUR)
        print('\nStart point:', startNode.point)
        print()
        matrix[startNode.point[0]][startNode.point[1]] = startPoint
        count += 1
        
    elif count == 2:
        endNode = node
        endNode.updateColour(END_NODE_COLOUR)
        print('End Point:', endNode.point)
        matrix[endNode.point[0]][endNode.point[1]] = endPoint

        print('\n* Start and End points selected! *')
        for node in nodes:
            node.getCosts(float('inf'))
            if node == startNode:
                node.getCosts(0)
        window.update()
        count = 10
        main()
    
toggle = False
def toggleObstacleDraw(event):
    global toggle
    toggle = not toggle
    print('Obstacle Draw:', 'Enabled' if toggle else 'Disabled')
def toggledDraw(node):
    if not toggle:
        return
    try:
        drawObstacles(node)
    except RecursionError:
        sys.stdout.write('\nRecursion Error')
        entry['state'] = 'normal'
        entry.delete(0, 'end')
        entry.insert(0, DEFAULT_GRID_SIZE)
        resetWindow()
        
        
def drawObstacles(node):
    ''' Drawing obstacles on the matrix '''
    global count
    #Alternative check: matrix[node.point[0]][node.point[1]] in OCCUPIED
    if count == 10 or (not node.isFreeNode):
        return
    node.updateColour(OBSTACLE_COLOUR)
    matrix[node.point[0]][node.point[1]] = obstacle
    window.update()

fullScreenToggle = True
LABEL = tk.Label(window, bg=TEXT_BG, fg=TEXT_FG, font=FONT, text='Full Screen Mode')
def toggleFullScreen(event):
    global fullScreenToggle
    window.resizable(True, True)
    window.attributes('-fullscreen', fullScreenToggle)
    if fullScreenToggle:
        LABEL.pack(fill='both')
    else:
        LABEL.forget()
    fullScreenToggle = not fullScreenToggle
    window.resizable(False, False)
        
window.bind('<Return>', resetWindow)
window.bind('<space>', toggleObstacleDraw)
window.bind('<space>', )
window.bind('<Key>', lambda e: window.destroy() if e.char == 'q' else False)
window.bind('<Escape>', lambda e: window.destroy())
window.bind('<F11>', toggleFullScreen)

def main():
    
    global count
    
    NODE = startNode
    neighbouringSpots = []
    origin = {}
    path = []

    while True:
        if NODE == endNode:
            matrix[NODE.point[0]][NODE.point[1]] = endPoint
            NODE.updateColour(END_NODE_COLOUR)
            print(searchComplete)
            break

        neighbours = NODE.getNeighbours(matrix, nodes)
        for n in neighbours:
            try:
                nodeDetails = (n.gFactor, n.hFactor, n.fCost)
            except AttributeError:
                print(searchTermination)
                return
            if n not in origin:
                origin[n] = NODE #Storing the origin of each node in dictionary
                n.updateCosts(NODE)
            else:
                nodeDetails = (n.gFactor, n.hFactor, n.fCost)
                try:
                    n.updateCosts(NODE)
                except AttributeError:
                    print(searchTermination)
                    return 
                if n.fCost < nodeDetails[2] or all([n.fCost == nodeDetails[2], n.hFactor < nodeDetails[1]]):
                    print('Success!')
                    print('Node in question:', n.point)
                    print('Previous neighbour:', origin[n])
                    print('*Original node values:', nodeDetails)
                    origin[n] = NODE
                    print('Updated Neighbour:', NODE)
                    print('*Updated node:', n)
                else:
                    print('Operation Fail!!')
                    print('Node in question:', n.point)
                    print('Failed neigbour:', NODE)
                    print('*Failed node values:', n)
                    s = f'Now: is n.fcost({n.fCost}) < origin[n].fcost({origin[n].fCost}) --> {n.fCost < origin[n].fCost}'
                    print(s)
                    n.gFactor, n.hFactor, n.fCost = nodeDetails
                    print('Actual neighbour:', origin[n])
                    print('*Original node values:', n)
                    

        neighbouringSpots.extend(neighbours)
        neighbouringSpots = list(set(neighbouringSpots))

        #Displaying message if there is no possible path i.e path doesn't exist
        #neighbouringSpots is empty => path doesn't exist
        if not neighbouringSpots:
            print(pathNotFound)
            messagebox.showerror('Path Not Found', 'Path to destination does not exist!')
            return #Terminating from the main function

        #Displaying Neigbouring points
        else:
            print('\n****** Neighbours: *******')
            
        for node in neighbouringSpots:
            #Try block used to check if screen has been cleared
            try:
                print(node)
            except AttributeError:
                print(searchTermination)
                return #Terminating from the main function
            node.updateColour(EXPLORED_NODE_COLOUR)
            
        window.update()

        optimalNode = neighbouringSpots[0]
        for i in range(1, len(neighbouringSpots)):
            n = neighbouringSpots[i]
            if n.fCost < optimalNode.fCost:
                optimalNode = n
            elif n.fCost == optimalNode.fCost:
                if n.hFactor < optimalNode.hFactor:
                    optimalNode = n
            
        point = optimalNode.point
        matrix[point[0]][point[1]] = locked
        optimalNode.updateColour(LOCKED_NODE_COLOUR)
        optimalNode.locked = True
        path.append([optimalNode, origin[optimalNode]])
        print('Optimal point:', point)
        print()
        neighbouringSpots.remove(optimalNode) #Has been marked as a locked node
        NODE = optimalNode

        optimalNeighbours = optimalNode.getNeighbours(matrix, nodes)

    org = endNode
    followed = []
    while True:
        for node in path:
            if node[0] == org:
                org = node[1]
                followed.append(org)
                break
        else:
            break

    #Resetting node the locked and explored nodes
    for node in neighbouringSpots:
        node.updateColour(NODE_COLOUR)
    for node in [n[0] for n in path]:
        node.updateColour(NODE_COLOUR)

    startNode.updateColour(START_NODE_COLOUR)        
    endNode.updateColour(END_NODE_COLOUR)

    #Displaying the shortest path
    print('\nFinal path ----->')
    print('----------------')
    print('Start point:-')
    followed.reverse()
    for i in range(1, len(followed)):
        node = followed[i]
        print(node)
        point = node.point
        matrix[point[0]][point[1]] = marked
        node.updateColour(PATH_COLOUR)
        window.update()

    print('End point-:', endNode)

    print('*' * 50)
    try:
        for node in nodes:
            if not node.isObstacle():
                node_details = f'''\
Point: {node.point}
G-factor: {node.gFactor}
H-factor: {node.hFactor}
F-Cost: {node.fCost}'''
                toolTips.append(CreateToolTip(node.label, text=node_details))
    except AttributeError:
        print(searchTermination)
    

window.mainloop()
        






            

