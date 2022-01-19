"""
Gurtaj Khabra
Dec 2021
----------------
This program was made by me to learn more advanced algorithms
as well as user interfaces using tkinter because cmput274 did
not cover some of the topics I use like A* pathfinding and
the tkinter module.
----------------
This file contains most of the computational code used by
the a* pathfinding algorithm.
Note: the game is unoptimized for big board sizes.
Sizes above 30 rows and 50 columns will not work great.
"""

import interface
import time
import tkinter as tk

global start
global end
global boardSize
global score

green = "#a1f7bc"       # start color
red = "#f79ca3"         # end color
lav = "#f59fee"         # path color

# representation of the board squares
class gridNode:
    def __init__(self, x, y, s, e):
        self.open = True
        self.distS = s                          # distance from start
        self.distE = e                          # distance from end
        self.score = self.distS + self.distE    # a* score
        game.showScore(x, y, self.score)        # shows the score on the ui board
        self.x = x
        self.y = y
    def updateScore(self):                      # updates scores when calculated or recalculated
        self.score = self.distS + self.distE
        game.showScore(self.x, self.y, self.score)

# creates a new user interface
game = interface.App()

pathfind = False
invalid = True

# repeats until start and end are within the bounds of the board
while invalid:
    # repeats until the start button on the ui is clicked
    while not pathfind:
        # updates pathfind
        pathfind = game.waitForPathfind()
        if pathfind == False:
            continue
        # retreives boardsize from the text entry
        boardSize = game.getBoardSize()
        # retreives start point from text entry
        start = game.getStart()
        # checks whether start is in bounds
        if start[0] > boardSize[0] or start[1] > boardSize[1]:
            pathfind = False
            game.displayMessage("Invalid", "Start is not on board\nre-enter start")
            continue
        else:
            validStart = True
        # retreives end point from text entry
        end = game.getEnd()
        # checks whether end is in bounds
        if end[0] > boardSize[0] or end[1] > boardSize[1]:
            pathfind = False
            game.displayMessage("Invalid", "End is not on board\nre-enter end")
            continue
        else:
            validEnd = True
        if validStart and validEnd:
            invalid = False

# calculates distance from start to end using 14 for diagonals, 10 otherwise
xdist = abs(start[0] - end[0])
ydist = abs(start[1] - end[1])
dist = min(xdist, ydist)*14 + abs(ydist - xdist)*10

looking = True
# grid representation of node class objects
grid = []
# initialize grid based on board size
for i in range(boardSize[1]):
    grid.append([None]*boardSize[0])
# tells ui to create the board
game.createBoard(boardSize[0], boardSize[1])
# gives user instructions
game.displayMessage("A* Pathfinding", "Add obstacles by clicking buttons")

# initializes the start point and end point grid node objects
first = gridNode(start[0], start[1], 0, dist)
last = gridNode(end[0], end[1], 0, 0)
grid[first.y - 1][first.x - 1] = first
# sets start to green
game.changeColor(first.x, first.y, green)
grid[last.y - 1][last.x - 1] = last
# sets end to red
game.changeColor(last.x, last.y, red)
# sets current node to start node
current = first
# dictionary used for storing scores
scores = dict()

placing = True
# wait for user to hit start (so they have time to place obstacles)
while game.stillPlacing():
    continue

# initializes obstacles
obstacles = game.getObstacles()

# updates nodes as their scores are calculated
def updateNode(x, y, s):
    # if the node is an obstacle, do nothing
    if [x,y] in obstacles:
        return
    # if the node does not exist, create a node
    elif grid[y-1][x-1] == None:
        xdist = abs(last.x - x)
        ydist = abs(last.y - y)
        e = min(xdist, ydist)*14 + abs(ydist - xdist)*10
        # creates gridnode in the grid
        grid[y-1][x-1] = gridNode(x, y, s, e)
        score = grid[y-1][x-1].score
        # adds/increments node score in dictionary
        if score in scores:
            scores[score].append(grid[y-1][x-1])
        else:
            scores[score] = [grid[y-1][x-1]]
    # if the node checked is the final node, add a 0 score to the dictionary
    elif grid[y-1][x-1] == last:
        scores[0] = [last]
    # if the node already exists and is open, updates the score
    elif isinstance(grid[y-1][x-1], gridNode) and grid[y-1][x-1].open:
        old = grid[y-1][x-1].score
        # removes grid node from old score in dictionary
        if old in scores and grid[y-1][x-1] in scores[old]:
            scores[old].remove(grid[y-1][x-1])
        grid[y-1][x-1].distS = min(grid[y-1][x-1].distS, s)
        # updates grid node with new score
        grid[y-1][x-1].updateScore()
        score = grid[y-1][x-1].score
        # adds score to dictionary
        if score in scores:
            scores[score].append(grid[y-1][x-1])
        else:
            scores[score] = [grid[y-1][x-1]]

# checks the 8 surrounding neighbours of the node
def checkNeighbours(node):
    # North neighbour if there is one
    if node.y != 1:
        updateNode(node.x, node.y-1, node.distS+10)
    if node.y != 1 and node.x != boardSize[0]:              # north east
        updateNode(node.x+1, node.y-1, node.distS+14)
    if node.x != boardSize[0]:                              # east
        updateNode(node.x+1, node.y, node.distS+10)
    if node.x != boardSize[0] and node.y != boardSize[1]:   # south east
        updateNode(node.x+1, node.y+1, node.distS+14)
    if node.y != boardSize[1]:                              # south
        updateNode(node.x, node.y+1, node.distS+10)
    if node.x != 1 and node.y != boardSize[1]:              # south west
        updateNode(node.x-1, node.y+1, node.distS+14)
    if node.x != 1:                                         # west
        updateNode(node.x-1, node.y, node.distS+10)
    if node.x != 1 and node.y != 1:                         # north west
        updateNode(node.x-1, node.y-1, node.distS+14)

# list of nodes representing the path from start to end
path = []
# list of nodes that have been checked
checked = []

# traces the path after the end node is reached
def backtrackPath():
    # starting from the end point
    current = last
    # repeats until the start point is reached
    while current != first:
        # dictionary containing neighbour scores
        neighbourScores = {}
        for node in checked:
            # if the checked node is a neighbour to the current node, add score to dictionary
            if abs(node.x - current.x) < 2 and abs(node.y-current.y) < 2:
                if node.score in neighbourScores:
                    neighbourScores[node.score].append(node)
                else:
                    neighbourScores[node.score] = [node]
        # takes the smallest neighbour score as the new current.
        if len(neighbourScores[min(neighbourScores)])==1:
            current = neighbourScores[min(neighbourScores)][0]
        else:
            options = []
            for node in neighbourScores[min(neighbourScores)]:
                options.append(node.distS)
            for node in neighbourScores[min(neighbourScores)]:
                if node.distS == min(options):
                    current = node
        # adds the current node to the path
        path.append([current.x, current.y])

while looking:
    checkNeighbours(current)
    current.open = False
    checked.append(current)
    # deletes dictionary keys with no values
    while len(scores[min(scores)]) == 0:
        del scores[min(scores)]
    # sets current to an open node with the smallest score
    if len(scores[min(scores)]) == 1:
        previous = current
        current = scores[min(scores)][0]
        del scores[min(scores)]
    else:
        # for multiple nodes with same score, sets current to node closest to endpoint
        nodes = scores[min(scores)]
        ends = []
        for x in nodes:
            ends.append(x.distE)
        for x in nodes:
            if x.distE == min(ends):
                previous = current
                current = x
                scores[min(scores)].remove(x)
    # path to endpoint has been found
    if current == last:
        backtrackPath()
        # sets each grid location that is in path to purple
        for x,y in path:
            if x == first.x and y == first.y:
                continue
            else:
                game.changeColor(x,y,lav)
        looking = False
