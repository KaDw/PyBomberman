# classes
# map
# player
# bomb
# bot

import sys
import numpy as np
import xml.etree.ElementTree
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QTimer
import threading
import time

X_SIZE = 20
Y_SIZE = 20


class Window(QtGui.QWidget):
    #isPaused = 0
    def __init__(self):
        super(Window, self).__init__() # parent object
        self.setStyleSheet("QWidget { background: #D5D9A9 }")
        self.setFixedSize(500, 500)
        self.setWindowTitle("CZbombelman")
        self.show()
        # init timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.repaint)
        self.timer.start(20)

    def home(self):
        QtGui.QGraphicsRectItem()


    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawMap(qp)
        self.drawPlayer(qp)
        qp.end()

    def drawBlockN(self, qp, x, y):
        qp.setBrush(QtGui.QColor(255, 200, 50, 160))
        qp.drawRect(X_SIZE * x, Y_SIZE * y, X_SIZE, Y_SIZE)

    def drawBlockD(self, qp, x, y):
        qp.setBrush(QtGui.QColor(255, 50, 50, 160))
        qp.drawRect(X_SIZE * x, Y_SIZE * y, X_SIZE, Y_SIZE)

    def drawBomb(self, qp, x, y):
        qp.setBrush(QtGui.QColor(0, 0, 0, 160))
        qp.drawEllipse(X_SIZE * x, Y_SIZE * y, X_SIZE, Y_SIZE)

    def drawBombExplode(self, qp, x, y):
        qp.setBrush(QtGui.QColor(230, 20, 0, 160))
        qp.drawRect(X_SIZE * x, Y_SIZE * y, X_SIZE, Y_SIZE)

    def drawPlayer(self, qp):
        qp.setBrush(QtGui.QColor(255, 255, 255, 160))
        for player in players:
            qp.drawEllipse(player.x, player.y, 14, 18)

    def drawMap(self, qp):
        for (x, y), value in np.ndenumerate(map.map):
            if value == 1: # destructible block
                self.drawBlockN(qp, x, y)
            elif value == 3:  # indestructible block
                self.drawBlockD(qp, x, y)
            elif value == 2:
                self.drawBomb(qp, x, y)
            elif value == 4:
                self.drawBombExplode(qp, x, y)



    def keyPressEvent(self, e):
       # if not self.isPaused:
            if e.key() == QtCore.Qt.Key_Up: #and self.lastKeyPress != 'UP' and self.lastKeyPress != 'DOWN':
                players[0].direction = 0
                players[0].y -= 4
                # self.direction("UP")
                # self.lastKeyPress = 'UP'
                print("up")
            elif e.key() == QtCore.Qt.Key_Down:
                players[0].direction = 1
                players[0].y += 4
                print("down")
            elif e.key() == QtCore.Qt.Key_Left:
                players[0].direction = 2
                players[0].x -= 4
                print("left")
            elif e.key() == QtCore.Qt.Key_Right:
                players[0].direction = 3
                players[0].x += 4
                print("right")
            elif e.key() == QtCore.Qt.Key_Space:
                players[0].bombList.append(Bomb(int(players[0].x/20), int(players[0].y/20)))
            players[0].checkCollision()
            #GUI.repaint()
            # elif e.key() == QtCore.Qt.Key_Down and self.lastKeyPress != 'DOWN' and self.lastKeyPress != 'UP':
            #     self.direction("DOWN")
            #     self.lastKeyPress = 'DOWN'
            # elif e.key() == QtCore.Qt.Key_Left and self.lastKeyPress != 'LEFT' and self.lastKeyPress != 'RIGHT':
            #     self.direction("LEFT")
            #     self.lastKeyPress = 'LEFT'
            # elif e.key() == QtCore.Qt.Key_Right and self.lastKeyPress != 'RIGHT' and self.lastKeyPress != 'LEFT':
            #     self.direction("RIGHT")
            #     self.lastKeyPress = 'RIGHT'
            # elif e.key() == QtCore.Qt.Key_P:
            #     self.pause()
         # elif e.key() == QtCore.Qt.Key_P:
         #     self.start()
        # elif e.key() == QtCore.Qt.Key_Space:
        #     self.newGame()
        # elif e.key() == QtCore.Qt.Key_Escape:
        #     self.close()
    #def checkCollision(self):


class Map:
    def __init__(self, x, y):
        self.map = np.zeros((x, y))
        self.generateMap()
        #self.xml_file = None
    #TODO zrobic tablice z typami i kolorami bloczkow
    #dodac wczytywanie map

    def getCoordinates(self, x, y):
        return self.map[x][y] # zwraca 4 rogi mapy, top bottom left right

    def generateMap(self):
        for (x, y), value in np.ndenumerate(self.map):
            if x % 4 == 2 and y % 4 == 2:
                self.map[x][y] = 3
            if x % 2 == 1 and y % 2 == 1:
                self.map[x][y] = 1
    # def loadMap(self):
    #     self.xml_file = xml.etree.ElementTree.parse('game.xml').getroot()
    # def saveMap(self):



# class Game:
#     def __init__(self, map, players, mobs):
#         self.map = map
#         self.players = players
#         self.mobs = mobs
#         #self.time


class Player():

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = -1;
        self.bombList = []
        # self.top = self.x
        # self.bottom
        # self.left
        # self.right
        # self.bombRange = 0
    def checkCollision(self):
         if map.map[int(self.x/20)][int(self.y/20)] != 0:
             print('collision')
        # if (block.bottom() >= ball.top()) // kolizja z dolu klocka
        #     ball.velocity.y = ballVelo;
        #
        # else if (block.right() >= ball.left()) // kolzija z prawej klocka
        #     ball.velocity.x = ballVelo;
        #
        # else if (block.left() >= ball.right()) // kolizja z lewej klocka
        #     ball.velocity.x = -ballVelo;
        #
        # else if (block.top() <= ball.bottom()) // kolizja z gory klocka
        #     ball.velocity.x = ballVelo;


class Bomb():
    # pole wspolne dla wszystkich bomb
    tick_time = 3000
    explode_anim = 500
    def __init__(self, x, y):
        self.x = x
        self.y = y
        map.map[x][y] = 2
        self.bomb_timer = QTimer()
        self.bomb_timer.timeout.connect(self.bombTrigger)
        self.bomb_timer.start(Bomb.tick_time)
        self.bomb_timer.setSingleShot(True)
        self.bombRange = 4
        # self.bombRange = 0
    def bombTrigger(self):
        self.bomb_timer.timeout.connect(self.bombExplode)
        self.bomb_timer.start(Bomb.explode_anim)
        # nie wyglada ladnie
        for x1 in range(self.x - self.bombRange + 1, self.x + self.bombRange):
            if map.map[x1][self.y] < 3:
                map.map[x1][self.y] = 4
        for y1 in range(self.y - self.bombRange + 1, self.y + self.bombRange):
            if map.map[self.x][y1] < 3:
                map.map[self.x][y1] = 4
        # for x in range(self.x-1, self.x+2):
        #     for y in range(self.y-1, self.y + 2):
        #         if map.map[x][y] == 0 or map.map[x][y] == 1 or  map.map[x][y] == 3:
        #             map.map[x][y] = 4
    def bombExplode(self):
        # nie wyglada ladnie
        for x1 in range(self.x - self.bombRange + 1, self.x + self.bombRange):
            if map.map[x1][self.y] == 4:
                map.map[x1][self.y] = 0
        for y1 in range(self.y - self.bombRange + 1, self.y + self.bombRange):
            if map.map[self.x][y1] == 4:
                map.map[self.x][y1] = 0
        #if
        # for x in range(self.x-1, self.x+2):
        #     for y in range(self.y-1, self.y + 2):
        #         if map.map[x][y] == 4:
        #             map.map[x][y] = 0
    # def checkBomb(self, x):
    #     for x1 in range(x - self.bombRange + 1, x + self.bombRange):
    #         if map.map[x1] == 0 or map.map[x1] == 1 or map.map[x1] == 3:


players = []
bots = []
players.append(Player(0, 0))
map = Map(40, 40)
app = QtGui.QApplication(sys.argv)
GUI = Window()

sys.exit(app.exec_())