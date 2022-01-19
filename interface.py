"""
Gurtaj Khabra
Dec 2021
----------------
This program was made by me to learn more advanced algorithms
as well as user interfaces using tkinter because cmput274 did
not cover some of the topics I use like A* pathfinding and
the tkinter module.
----------------
This file contains most of the user interface code from tkinter.
"""

import tkinter as tk
import threading

class App(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.start()
        self.pathFind = False
        self.placingObstacles = True
    
    def callback(self):
        self.window.quit()

    def run(self):
        self.obstacles = []         # coordinates of added obstacles
        self.boardSize = [0,0]
        self.start = [0,0]
        self.end = [0,0]
        self.window = tk.Tk()
        self.window.title("A* Pathfinding")
        self.window.geometry("500x200")
        self.window.resizable(False, False)
        self.window.title = "A* Pathfinder"
        boardPrompt = tk.Label(self.window, text="Enter the board size (rows,cols): ", font="fixedsys 15")
        boardPrompt.place(relx=0.5, rely=0.17, anchor="center")
        self.boardEntry = tk.Entry(self.window, width=7, justify="center", bg="white", font="fixedsys 11")
        self.boardEntry.place(relx=0.5, rely=0.271, anchor="center")
        startPrompt = tk.Label(self.window, text="Enter the start (x,y): ", font="fixedsys 15")
        startPrompt.place(relx=0.5, rely=0.39, anchor="center")
        self.startEntry = tk.Entry(self.window, width=7, justify="center", bg="white", font="fixedsys 11")
        self.startEntry.place(relx=0.5, rely=0.491, anchor="center")
        endPrompt = tk.Label(self.window, text="Enter the end (x,y): ", font="fixedsys 15")
        endPrompt.place(relx=0.5, rely=0.61, anchor="center")
        self.endEntry = tk.Entry(self.window, width=7, justify="center", bg="white", font="fixedsys 11")
        self.endEntry.place(relx=0.5, rely=0.711, anchor="center")
        go = tk.Button(self.window, text="Find path", width=9, font="fixedsys 12", command=self.clicked)
        go.place(relx=0.5, rely=0.85, anchor="center")
        self.window.mainloop()

    # initializes the boardsize, start point, and end point
    def clicked(self):
        self.boardSize = list(map(int, self.boardEntry.get().split(sep=",")))
        self.start = list(map(int, self.startEntry.get().split(sep=",")))
        self.end = list(map(int, self.endEntry.get().split(sep=",")))
        self.pathFind = True
    
    # various methods for the game code to interact with
    # and obtain interface information
    def waitForPathfind(self):  
        return(self.pathFind)
    
    def stillPlacing(self):
        return(self.placingObstacles)
    
    def getBoardSize(self):
        return(self.boardSize)
    
    def getStart(self):
        return(self.start)
    
    def getEnd(self):
        return(self.end)
    
    def getObstacles(self):
        return(self.obstacles)

    # used for displaying popup messages, for example, error messages
    def displayMessage(self, title, message):
        self.popup = tk.Tk()
        msgSize = message.split('\\\\n')[0]
        self.popup.geometry(f"{len(msgSize*12)}x100")
        self.popup.title(title)
        self.popup.attributes('-topmost',1)
        message = tk.Label(self.popup, text=message, font = "fixedsys 15")
        message.place(relx = 0.5, rely = 0.3, anchor="center")
        ok = tk.Button(self.popup, font = "fixedsys 10", text="Ok", width=9, command=self.reset)
        ok.place(relx=0.5, rely = 0.7, anchor="center")
        self.popup.mainloop()

    # sets the clicked button to an obstacle if it is not the start or end point
    def obstacle(self, x, y):
        purple = "#340936"
        if x == self.start[0] and y == self.start[1] or x == self.end[0] and y == self.end[1]:
            pass
        elif self.placingObstacles:
            self.obstacles.append([x,y])
            self.changeColor(x,y,purple)

    def startGame(self):
        self.placingObstacles = False

    # creates the board using buttons as squares in a grid
    def createBoard(self, x, y):
        self.board = []
        for i in range(y):
            self.board.append([None]*x)
        # clears the window showing menu objects
        for widget in self.window.winfo_children():
            widget.destroy()
        # adds buttons to represent the board
        for i in range(y):
            for j in range(x):
                self.board[i][j] = tk.Button(self.window, font="fixedsys 12", width=int(98/x), height=int(49/x), command= lambda x=j+1, y=i+1: self.obstacle(x,y))
                self.board[i][j].grid(row=j, column=i)
        w = self.board[0][0].winfo_width()
        h = self.board[0][0].winfo_height()
        # adds a start button
        start = tk.Button(self.window, width=1, text="Start", font="fixedsys 12", command=self.startGame)
        start.grid(row=x, column=0, sticky='nesw')
        # adds an exit button
        leave = tk.Button(self.window, width=1, text="Exit", font="fixedsys 12", command = self.quitGame)
        leave.grid(row=x, column=y-1, sticky='nesw')
        # sets the window size
        self.window.geometry(f'{y*w}x{x*h+20}')
        self.window.title = "A* Pathfinder"

    # changes the color of a square on the board
    def changeColor(self, x, y, color):
        if self.board[y-1][x-1] != None:
            self.board[y-1][x-1].configure(bg=color)

    # shows the A* pathfinding score on the grid square
    def showScore(self, x, y, score):
        self.board[y-1][x-1].configure(text=score)

    # restarts the game
    def restart(self):
        self.pathFind = False
        self.window.destroy()
        self.run()
    
    # quits the game
    def quitGame(self):
        self.window.destroy()
        quit()

    def reset(self):
        self.pathFind = False
        self.popup.destroy()
