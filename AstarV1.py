import tkinter as tk
from tkinter import messagebox
import time
from math import sqrt
''' A* path finding algorithm '''

class Node:
    def __init__(self, label):
        self.label = label
        info = label.grid_info()
        self.point = (info['row'], info['column'])
        self.locked = False
        self.explored = False
        self.updateColour('white')

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
    
    def getCosts(self):
        self.gFactor = self.getDistance(startNode)
        self.hFactor = self.getDistance(endNode)
        self.fCost = self.gFactor + self.hFactor

    def updateColour(self, colour):
        self.label['bg'] = colour
        
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
    
    def getDistance(self, node):
        d = int(sqrt((self.point[0] - node.point[0])**2 + (self.point[1] - node.point[1])**2) * 10)
        return d

class CreateToolTip:
    
    def __init__(self, widget, text='widget info'):
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter, add='+')
        self.widget.bind("<Leave>", self.close)

    def enter(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        # creates a toplevel window
        self.tw = tk.Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self.tw, text=self.text, justify='left',
                       bg='yellow', relief='solid', borderwidth=1,
                       font=('Verdana', 15))
        label.pack(ipadx=1)

    def close(self, event=None):
        if self.tw:
            self.tw.destroy()
            
window = tk.Tk()
window.title('A* Path finding algorithm')
window.geometry('660x680+300+50')

nodes = []
matrix = []
def initializeGrid():
    global count
    nodes.clear()
    FONT = ('Times New Roman', 20)
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            label = tk.Label(window, font=FONT, relief = 'sunken', width = 4, height = 2)
            label.grid(row = i, column = j)
            node = Node(label)
            nodes.append(node)
    count = 1

    #Binding all nodes to GUI events
    for node in nodes:
        node.label.bind('<Button-1>', lambda e, n=node: getStartEnd(n))
        node.label.bind('<Button-3>', lambda e, n=node: getObstacles(n))
        node.label.bind('<Enter>', lambda e, n=node: toggledDraw(n))

def initializeMatrix():
    matrix.clear()
    for i in range(10):
        matrix.append(['0' for j in range(10)])

initializeMatrix()
initializeGrid()

prompt = '''
Instructions
------------
Left-Click --> To select start/end points
Right-Click --> Draw an obstacle
Space --> Toggle obstacle draw, to enable drawing multiple obstacles
Enter --> Clear Screen
Q/Esc --> Quit
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
OCCUPIED = [locked, marked, startPoint, obstacle]

def getStartEnd(node):
    global count, startNode, endNode
    if count > 2 or matrix[node.point[0]][node.point[1]] in OCCUPIED:
        return
    node.updateColour('deep sky blue')
    if count == 1:
        startNode = node
        print('\nStart point:', startNode.point)
        print()
        node.label['text'] = startPoint
        matrix[startNode.point[0]][startNode.point[1]] = startPoint
        count += 1
    elif count == 2:
        endNode = node
        print('End Point:', endNode.point)
        node.label['text'] = endPoint
        matrix[endNode.point[0]][endNode.point[1]] = endPoint

        print('\n* Start and End points selected! *')
        for node in nodes:
            node.getCosts()
            if node not in [startNode, endNode]:
                node_details = f'G-factor: {node.gFactor}\nH-factor: {node.hFactor}\nF-Cost: {node.fCost}'
                CreateToolTip(node.label, text=node_details)
        window.update()
        count = 10
        main()
    
toggle = False
def toggleObstacleDraw(event):
    global toggle
    toggle = not bool(toggle)
    print('Obstacle Draw:', 'Enabled' if toggle else 'Disabled')

def toggledDraw(node):
    if not toggle:
        return
    getObstacles(node)
        
def getObstacles(node):
    global count
    if count == 10 or matrix[node.point[0]][node.point[1]] in OCCUPIED:
        return
    node.updateColour('black')
    matrix[node.point[0]][node.point[1]] = obstacle
    window.update()

def resetWindow(event):
    global count, toggle
    msg = 'Window has been reset'
    print('\n' + '='*len(msg))
    print(msg)
    print('='*len(msg))
    count = 1
    toggle = False
    initializeMatrix()
    initializeGrid()
    
window.bind('<Return>', resetWindow)
window.bind('<space>', toggleObstacleDraw)
window.bind('<Key>', lambda e: window.destroy() if e.char == 'q' else False)
window.bind('<Escape>', lambda e: window.destroy())

def main():
    
    global count
    
    NODE = startNode
    neighbouringSpots = []
    origin = {}
    path = []

    while True:
        if NODE == endNode:
            matrix[NODE.point[0]][NODE.point[1]] = endPoint
            NODE.updateColour('deep sky blue')
            print('\n' + ' Search Complete! '.center(50, '*'))
            break

        neighbours = NODE.getNeighbours(matrix, nodes)
        for n in neighbours:
            if n not in origin:
                origin[n] = NODE #Storing the origin of each node in dictionary
##            else:
##                d1 = n.getDistance(origin[n].point) + origin[n].getDistance(startNode.point)
##                d2 = NODE.getDistance(origin[n].point) + NODE.getDistance(startNode.point)
##                print(f'd1: {n} -> {d1}')
##                print(f'd2: {NODE} -> {d2}')
##                print(f'Actual origin: {origin[n]}')
##                if d1 < d2:
##                    origin[n] = NODE
##                    print(f'Updated origin: {origin[n]}')
        neighbouringSpots.extend(neighbours)
        neighbouringSpots = list(set(neighbouringSpots))

        #Displaying message if there is no possible path i.e path doesn't exist
        #neighbouringSpots is empty => path doesn't exist
        if not neighbouringSpots:
            print('\n' + ' Path to destination does not exist! '.center(51, '*'))
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
                print('\n' + ' Search Terminated! '.center(50, '*'))
                return #Terminating from the main function
            node.updateColour('green')
            
        window.update()

        optimalNode = neighbouringSpots[0]
        for i in range(1, len(neighbouringSpots)):
            if neighbouringSpots[i].fCost < optimalNode.fCost:
                optimalNode = neighbouringSpots[i]
            elif neighbouringSpots[i].fCost == optimalNode.fCost:
                if neighbouringSpots[i].hFactor < optimalNode.hFactor:
                    optimalNode = neighbouringSpots[i]
            
        point = optimalNode.point
        matrix[point[0]][point[1]] = locked
        optimalNode.updateColour('red')
        optimalNode.locked = True
        path.append([optimalNode, origin[optimalNode]])
        print('Optimal point:', point)
        print()
        neighbouringSpots.remove(optimalNode) #Has been marked as a locked node
        NODE = optimalNode

        optimalNeighbours = optimalNode.getNeighbours(matrix, nodes)
##        for n in optimalNeighbours:
##            d1 = n.getDistance(origin[NODE].point) + origin[NODE].getDistance(startNode.point)
##            d2 = NODE.getDistance(origin[NODE].point) + NODE.getDistance(startNode.point)
##            print(f'd1: {n.point} -> {d1}')
##            print(f'd2: {NODE.point} -> {d2}')
##            if n == endNode:
##                NODE = n
##                break
##            if abs(n.fCost - NODE.fCost) <= 10 and n.hFactor < NODE.hFactor:
##                print('HHHHeeelooo')
##                NODE = n
##        if NODE == endNode:
##            break

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

    for node in neighbouringSpots:
        node.updateColour('white')
    for node in [n[0] for n in path]:
        node.updateColour('white')
        
    endNode.updateColour('deep sky blue')
    print('\nFinal path ----->')
    print('----------------')
    print('Start point:-')
    followed.reverse()
    for node in followed:
        print(node)
        point = node.point
        matrix[point[0]][point[1]] = marked
        node.updateColour('deep sky blue')
        window.update()

    print('End point-:', endNode)

    print('*' * 50)
    

window.mainloop()
        






            

