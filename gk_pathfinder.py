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

class gridNode:
    def __init__(self, x, y, s, e):
        self.open = True
        self.distS = s
        self.distE = e
        self.score = self.distS + self.distE
        game.showScore(x, y, self.score)
        self.x = x
        self.y = y
    def updateScore(self):
        self.score = self.distS + self.distE
        game.showScore(self.x, self.y, self.score)

game = interface.App()

pathfind = False
invalid = True
while invalid:
    while not pathfind:
        pathfind = game.waitForPathfind()
        if pathfind == False:
            continue
        boardSize = game.getBoardSize()
        start = game.getStart()
        if start[0] > boardSize[0] or start[1] > boardSize[1]:
            pathfind = False
            game.displayMessage("Invalid", "Start is not on board\nre-enter start")
            continue
        else:
            validStart = True
        end = game.getEnd()
        if end[0] > boardSize[0] or end[1] > boardSize[1]:
            pathfind = False
            game.displayMessage("Invalid", "End is not on board\nre-enter end")
            continue
        else:
            validEnd = True
        if validStart and validEnd:
            invalid = False

xdist = abs(start[0] - end[0])
ydist = abs(start[1] - end[1])
dist = min(xdist, ydist)*14 + abs(ydist - xdist)*10

looking = True
grid = []
for i in range(boardSize[1]):
    grid.append([None]*boardSize[0])
game.createBoard(boardSize[0], boardSize[1])
game.displayMessage("A* Pathfinding", "Add obstacles by clicking buttons")

first = gridNode(start[0], start[1], 0, dist)
last = gridNode(end[0], end[1], 0, 0)
grid[first.y - 1][first.x - 1] = first
game.changeColor(first.x, first.y, green)
grid[last.y - 1][last.x - 1] = last
game.changeColor(last.x, last.y, red)
current = first
scores = dict()

placing = True
while game.stillPlacing():
    continue

obstacles = game.getObstacles()

def updateNode(x, y, s):
    if [x,y] in obstacles:
        return
    elif grid[y-1][x-1] == None:
        xdist = abs(last.x - x)
        ydist = abs(last.y - y)
        e = min(xdist, ydist)*14 + abs(ydist - xdist)*10
        grid[y-1][x-1] = gridNode(x, y, s, e)
        score = grid[y-1][x-1].score
        if score in scores:
            scores[score].append(grid[y-1][x-1])
        else:
            scores[score] = [grid[y-1][x-1]]
    elif grid[y-1][x-1] == last:
        scores[0] = [last]
    elif isinstance(grid[y-1][x-1], gridNode) and grid[y-1][x-1].open:
        old = grid[y-1][x-1].score
        if old in scores and grid[y-1][x-1] in scores[old]:
            scores[old].remove(grid[y-1][x-1])
        grid[y-1][x-1].distS = min(grid[y-1][x-1].distS, s)
        grid[y-1][x-1].updateScore()
        score = grid[y-1][x-1].score
        if score in scores:
            scores[score].append(grid[y-1][x-1])
        else:
            scores[score] = [grid[y-1][x-1]]

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

path = []
checked = []

def backtrackPath():
    current = last
    while current != first:
        neighbourScores = {}
        for node in checked:
            if abs(node.x - current.x) < 2 and abs(node.y-current.y) < 2:
                if node.score in neighbourScores:
                    neighbourScores[node.score].append(node)
                else:
                    neighbourScores[node.score] = [node]
        if len(neighbourScores[min(neighbourScores)])==1:
            current = neighbourScores[min(neighbourScores)][0]
        else:
            options = []
            for node in neighbourScores[min(neighbourScores)]:
                options.append(node.distS)
            for node in neighbourScores[min(neighbourScores)]:
                if node.distS == min(options):
                    current = node
        path.append([current.x, current.y])

while looking:
    checkNeighbours(current)
    current.open = False
    checked.append(current)
    while len(scores[min(scores)]) == 0:
        del scores[min(scores)]
    if len(scores[min(scores)]) == 1:
        previous = current
        current = scores[min(scores)][0]
        del scores[min(scores)]
    else:
        nodes = scores[min(scores)]
        ends = []
        for x in nodes:
            ends.append(x.distE)
        for x in nodes:
            if x.distE == min(ends):
                previous = current
                current = x
                scores[min(scores)].remove(x)
    if current == last:
        backtrackPath()
        for x,y in path:
            if x == first.x and y == first.y:
                continue
            else:
                game.changeColor(x,y,lav)
        looking = False