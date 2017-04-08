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
X_PSIZE = 14
Y_PSIZE = 18


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
        self.timer.timeout.connect(self.gameLoop)
        self.timer.start(20)
    def gameLoop(self):
        self.repaint()


    def home(self):
        QtGui.QGraphicsRectItem()


    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawMap(qp)
        self.drawPlayer(qp)
        qp.end()

    def drawBlockN(self, qp, x, y):
        qp.fillRect(map.map[x][y].rect, QtGui.QColor(255, 200, 50, 160))
        # qp.setBrush(QtGui.QColor(255, 200, 50, 160))
        # qp.drawRect(X_SIZE * x, Y_SIZE * y, X_SIZE, Y_SIZE)

    def drawBlockD(self, qp, x, y):
        qp.fillRect(map.map[x][y].rect, QtGui.QColor(255, 50, 50, 160))
        # qp.setBrush(QtGui.QColor(255, 50, 50, 160))
        # qp.drawRect(X_SIZE * x, Y_SIZE * y, X_SIZE, Y_SIZE)

    def drawBomb(self, qp, x, y):
        qp.fillRect(map.map[x][y].rect, QtGui.QColor(0, 0, 0, 160))
        # qp.setBrush(QtGui.QColor(0, 0, 0, 160))
        # qp.drawEllipse(X_SIZE * x, Y_SIZE * y, X_SIZE, Y_SIZE)

    def drawBombExplode(self, qp, x, y):
        qp.fillRect(map.map[x][y].rect, QtGui.QColor(230, 20, 0, 160))
        # qp.setBrush(QtGui.QColor(230, 20, 0, 160))
        # qp.drawRect(X_SIZE * x, Y_SIZE * y, X_SIZE, Y_SIZE)

    def drawPlayer(self, qp):
        qp.fillRect(player.rect, QtGui.QColor(90, 90, 90, 160))
        # qp.setBrush(QtGui.QColor(255, 255, 255, 160))
        # qp.drawEllipse(player.x, player.y, X_PSIZE, Y_PSIZE)

    def drawMap(self, qp):
        for (x, y), value in np.ndenumerate(map.map):
            if value.id == 1:  # destructible block
                self.drawBlockN(qp, x, y)
            elif value.id == 3:  # indestructible block
                self.drawBlockD(qp, x, y)
            elif value.id == 2:  # bomb
                self.drawBomb(qp, x, y)
            elif value.id == 4:  # explode effect
                self.drawBombExplode(qp, x, y)
            # elif value.id == 255:
            #     self.drawPlayer(qp, x, y)



    def keyPressEvent(self, e):
       # if not self.isPaused:
            if e.key() == QtCore.Qt.Key_Up: #and self.lastKeyPress != 'UP' and self.lastKeyPress != 'DOWN':
                player.direction = 0
                if ~player.rect.intersect(map.map[int(player.rect.x()/20)][int((player.rect.y()-4/20))]):
                    player.rect.setRect(player.rect.x(), player.rect.y()-4, X_PSIZE, Y_PSIZE)
                #player.rect.setY(player.rect.y()-4)
                #player.y -= 4
                # self.direction("UP")
                # self.lastKeyPress = 'UP'
                #print("up")
            elif e.key() == QtCore.Qt.Key_Down:
                player.direction = 1
                player.rect.setRect(player.rect.x(), player.rect.y() + 4, X_PSIZE, Y_PSIZE)
                #player.rect.setY(player.rect.y() + 4)
                #player.y += 4
                #print("down")
            elif e.key() == QtCore.Qt.Key_Left:
                player.direction = 2
                player.rect.setRect(player.rect.x() - 4, player.rect.y(), X_PSIZE, Y_PSIZE)
                #player.rect.setX(player.rect.x() - 4)
                #player.x -= 4
                #print("left")
            elif e.key() == QtCore.Qt.Key_Right:
                player.direction = 3
                player.rect.setRect(player.rect.x() + 4, player.rect.y(), X_PSIZE, Y_PSIZE)
                #player.rect.setX(player.rect.x() + 4)
                #player.x += 4
                #print("right")
            elif e.key() == QtCore.Qt.Key_Space:
                player.bombList.append(Bomb(int(player.rect.x()/20), int(player.rect.y()/20)))
                #print('added')
            #player.updatePlayer()
            #player.checkCollision()
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
class QRectColor():
    def __init__(self, x, y, id):
        self.id = id
        self.rect = QtCore.QRect(x * X_SIZE, y * Y_SIZE, X_SIZE, Y_SIZE)
        self.color = QtGui.QColor(213, 217, 169, 160)


class Map:
    def __init__(self, x, y):
        self.map = [[QRectColor(i, j, 0) for j in range(x)] for i in range(y)]
        self.generateMap()
        #self.xml_file = None
    #TODO zrobic tablice z typami i kolorami bloczkow
    #dodac wczytywanie map

    def getCoordinates(self, x, y):
        return self.map[x][y] # zwraca 4 rogi mapy, top bottom left right

    def generateMap(self):
        for (x, y), value in np.ndenumerate(self.map):
            if x % 4 == 2 and y % 4 == 2:
                self.map[x][y].id = 3
            if x % 2 == 1 and y % 2 == 1:
                self.map[x][y].id = 1
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
        self.rect = QtCore.QRect(x, y, X_PSIZE, Y_PSIZE)
        #self.rect = QRectColor(x, y, 255)
        self.direction = -1;
        self.bombList = []
        self.bombRange = 0
    def checkCollision(self): # slow
        for (x, y), value in np.ndenumerate(map.map):
            if map.map[x][y].id > 0:
                if self.rect.intersect(map.map[x][y].rect):
                    self.direction = 0
    def checkCollision(self):
        self.rect.center()
        # for (x, y), value in np.ndenumerate(map.map):
        #     if map.map[x][y].id > 0:
        #         if self.rect.intersect(map.map[x][y].rect):
        #             self.direction = 0


class Bomb():
    # pole wspolne dla wszystkich bomb
    tick_time = 3000
    explode_anim = 500
    def __init__(self, x, y):
        self.x = x
        self.y = y
        if  map.map[x][y].id != 2:
            map.map[x][y].id = 2
        self.bomb_timer = QTimer()
        self.explode_timer = QTimer()
        self.bomb_timer.timeout.connect(self.bombTrigger)
        #self.bomb_timer.setSingleShot(True)
        self.bomb_timer.start(Bomb.tick_time)
        self.bombRange = 4
        # self.bombRange = 0
    def bombTrigger(self): # po 3 sekundach bomba wybocuha, malujemy na czerwono
        self.bomb_timer.stop()
        self.explode_timer.timeout.connect(self.bombExplode)
        self.explode_timer.start(Bomb.explode_anim)
        # nie wyglada ladnie
        for x1 in range(1, self.bombRange):
            if map.map[self.x - x1][self.y].id == 0:
                map.map[self.x - x1][self.y].id = 4
            elif map.map[self.x - x1][self.y].id == 1:
                map.map[self.x - x1][self.y].id = 4
                break
        for x1 in range(1, self.bombRange):
            if map.map[self.x + x1][self.y].id == 0:
                map.map[self.x + x1][self.y].id = 4
            elif map.map[self.x + x1][self.y].id == 1:
                map.map[self.x + x1][self.y].id = 4
                break

        for x1 in range(1, self.bombRange):
            if map.map[self.x][self.y + x1].id == 0:
                map.map[self.x][self.y + x1].id = 4
            elif map.map[self.x][self.y + x1].id == 1:
                map.map[self.x][self.y + x1].id = 4
                break
        for x1 in range(1, self.bombRange):
            if map.map[self.x][self.y - x1].id == 0:
                map.map[self.x][self.y - x1].id = 4
            elif map.map[self.x][self.y - x1].id == 1:
                map.map[self.x][self.y - x1].id = 4
                break
        # for x1 in range(self.x - self.bombRange + 1, self.x + self.bombRange):
        #     if map.map[x1][self.y] < 2:
        #         map.map[x1][self.y] = 4
        # for y1 in range(self.y - self.bombRange + 1, self.y + self.bombRange):
        #     if map.map[self.x][y1] < 3:
        #         map.map[self.x][y1] = 4
        # for x in range(self.x-1, self.x+2):
        #     for y in range(self.y-1, self.y + 2):
        #         if map.map[x][y] == 0 or map.map[x][y] == 1 or  map.map[x][y] == 3:
        #             map.map[x][y] = 4
    def bombExplode(self):
        # nie wyglada ladnie
        map.map[self.x][self.y].id = 0
        for x1 in range(self.x - self.bombRange + 1, self.x + self.bombRange):
            if map.map[x1][self.y].id == 4:
                map.map[x1][self.y].id = 0
        for y1 in range(self.y - self.bombRange + 1, self.y + self.bombRange):
            if map.map[self.x][y1].id == 4:
                map.map[self.x][y1].id = 0
        self.bomb_timer.stop()
        player.bombList.pop(0)
        #if
        # for x in range(self.x-1, self.x+2):
        #     for y in range(self.y-1, self.y + 2):
        #         if map.map[x][y] == 4:
        #             map.map[x][y] = 0
    # def checkBomb(self, x):
    #     for x1 in range(x - self.bombRange + 1, x + self.bombRange):
    #         if map.map[x1] == 0 or map.map[x1] == 1 or map.map[x1] == 3:



bots = []
map = Map(40, 40)
player = Player(0, 0)
app = QtGui.QApplication(sys.argv)
GUI = Window()

sys.exit(app.exec_())