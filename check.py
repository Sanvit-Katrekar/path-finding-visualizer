''' A* path finding algorithm '''

#matrix = [['0' for j in range(10)] for i in range(10)]
##matrix = [
##        ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
##        ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
##        ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
##        ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
##        ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
##        ['0', '0', '|', 'B', '0', '0', '0', '0', '0', '0'],
##        ['0', '0', '|', '|', '|', '|', '|', '0', '0', '0'],
##        ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
##        ['0', '0', '0', '0', '0', '0', 'A', '0', '0', '0'],
##        ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
##        ]

matrix = [#0   1    2    3    4    5    6    7    8    9
        ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],#0
        ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],#1
        ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],#2
        ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],#3
        ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],#4
        ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],#5
        ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],#6
        ['0', '0', '0', '0', '0', '0', '|', '|', '0', 'B'],#7
        ['0', '0', '0', '0', '0', '0', '0', '|', '0', '0'],#8
        ['0', '0', '0', '0', 'A', '0', '0', '0', '0', '0'] #9
        ]


def displayMatrix():
    print([' X '] + [str(i).center(3, '-') for i in range(len(matrix))])
    for i in range(len(matrix)):
        print([str(i).center(3, '-')] + [str(val).center(3) for val in matrix[i]])

##print('\nStart Point')
##print('-------------')
##while True:
##    try:
##        startPoint = [int(input('\nRow: ')), int(input('\nColumn: '))]
##        matrix[startPoint[0]][startPoint[1]] = 'A'
##        break
##    except Exception:
##        print('\nInvalid coordinates!')
##        print('**********************')
##
##print('\nEnd Point')
##print('----------')
##while True:
##    try:
##        endPoint = [int(input('\nRow: ')), int(input('\nColumn: '))]
##        matrix[endPoint[0]][endPoint[1]] = 'B'
##        break
##    except Exception:
##        print('\nInvalid coordinates!')
##        print('**********************')

from math import sqrt

##aStart = (2, 5)
##b = (8, 9)
##aStart = (8, 6)
##b = (5, 3)
aStart = (9, 4)
b = (7, 9)
startPoint = 'A'
endPoint = 'B'
matrix[aStart[0]][aStart[1]] = startPoint
matrix[b[0]][b[1]] = endPoint

displayMatrix()

locked = 'x'
marked = '@@@'
obstacle = '|'


def getDistance(p1, p2):
    d = int(sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2) * 10)
    return d

def getNeighbours(p, mat):
    row, col = p
    spots = [(row-1, col-1), (row-1, col), (row-1, col+1), (row, col-1),
             (row, col+1), (row+1, col-1), (row+1, col), (row+1, col+1)
             ]
    for spot in list(spots):

        try:
            point = mat[spot[0]][spot[1]]
            if spot[0] < 0 or spot[1] < 0 or point in [locked, marked, startPoint, obstacle]:
                spots.remove(spot)
        except Exception:
            spots.remove(spot)

    return spots
        
path = []
a = aStart
neighbouringSpots = []
origin = {}
while True:
    if a == b:
        matrix[a[0]][a[1]] = endPoint
        print('\n* Search Complete! * \n')
        break

    neighbours = getNeighbours(a, matrix)
    for p in neighbours:
        if p not in origin:
            origin[p] = a #Storing the origin of each node in dictionary
##        else:
##            d1 = 14*(origin[p][1]) + 10*(abs(origin[p][0] - origin[p][1]))
##            d2 = 14*(a[1]) + 10*(abs(a[0] - a[1]))
##        else:
##            d1 = getDistance(aStart, origin[p]) + getDistance(b, origin[p])
##            d2 = getDistance(aStart, a) + getDistance(b, a)
        else:
            d1 = getDistance(origin[p], p)
            d2 = getDistance(origin[p], a)
            print('Hi')
            print(f'd1: {p} -> {d1}')
            print(f'd2: {a} -> {d2}')
            if d1 > d2:
                origin[p] = a
    neighbouringSpots += neighbours
    neighbouringSpots = list(set(neighbouringSpots))
    
    print('Neighbours:', neighbouringSpots)
    gFactors = [getDistance(aStart, spot) for spot in neighbouringSpots]
    hFactors = [getDistance(b, spot) for spot in neighbouringSpots]
    fCosts = [gFactors[i] + hFactors[i] for i in range(len(neighbouringSpots))]

    #Loop to get the optimal node's index
    minIndex = 0
    for i in range(1, len(fCosts)):
        if fCosts[i] < fCosts[minIndex]: minIndex = i
        elif fCosts[i] == fCosts[minIndex]:
            if hFactors[i] < hFactors[minIndex]:
                minIndex = i
        
    point = neighbouringSpots[minIndex]
    matrix[point[0]][point[1]] = locked
    path.append([point, origin[point]])
##    for i in range(len(neighbouringSpots)):
##        print(neighbouringSpots[i], ':', 'G->', gFactors[i], 'H->', hFactors[i], 'F->', fCosts[i])
##    print('Optimal point:', point)
##    print()
##    displayMatrix()
    
    neighbouringSpots.pop(minIndex)

    a = point

print('\n')
displayMatrix()

print('\nPoints explored ---->')
print('----------------')
for point in path:
    print(point)
print('**********')

print('\nPath followed ---->')
print('----------------')
org = b
followed = []
while True:
    for node in path:
        if node[0] == org:
            org = node[1]
            followed.append(org)
            break
    else:
        break
print('Start point:', followed.pop())
followed.reverse()
for point in followed:
    print(point)
    matrix[point[0]][point[1]] = marked
print('End point:', b)

print('\nFinal path ----->')
print('----------------')
displayMatrix()






        
