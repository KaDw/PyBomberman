import sys
import os
import numpy as np
from PyQt5.QtCore import QTimer
from random import randint
from PyQt5 import QtCore, QtGui, QtWidgets
from xml.dom.minidom import *
import queue

# block size
X_SIZE = 20
Y_SIZE = 20
# player size
X_PSIZE = 14
Y_PSIZE = 16
# bot size
X_BSIZE = 14
Y_BSIZE = 18


COL_UP = 1
COL_DOWN = 2
COL_RIGHT = 4
COL_LEFT = 8

KEY_UP = 1
KEY_DOWN = 2
KEY_RIGHT = 4
KEY_LEFT = 8

class Window(QtWidgets.QWidget):
    def __init__(self):
        super(Window, self).__init__() # parent object
        self.setStyleSheet('QWidget { background: #D5D9A9 }')
        self.setFixedSize(500, 500)
        self.setWindowTitle('bombelman')
        self.show()
        self.unlock = 0
        self.frameCounter = 0
        self.replayMode = 0
        self.lf = 0
        self.lf2 = 0
        self.key = 0
        # init timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.gameLoop)
        self.timer.start(30)
    def gameLoop(self):
        if self.replayMode == 0:
            #self.checkMapCollision()
            if checkCollision(player.rect, bots[0].rect):
                restart()
            for bot in bots:
                bot.moveBot()
        elif self.replayMode:
            for i in range(self.lf2, len(replay.tileList)):
                if replay.tileList[i][0] == self.frameCounter: # moze byc kilka zmian w tej samej klatce
                    map.map[replay.tileList[i][1]][replay.tileList[i][2]].id = replay.tileList[i][3]
                else:
                    self.lf2 = i
                    break

            for i in range(self.lf, len(replay.playerList)):
                if replay.playerList[i][0] == self.frameCounter: # moze byc kilka zmian w tej samej klatce
                    player.rect.setRect(replay.playerList[i][1], replay.playerList[i][2], X_PSIZE, Y_PSIZE)
                else:
                    self.lf = i
                    break
        #player.move(0, 1)
        self.handleKeys()
        self.repaint()
        self.frameCounter += 1

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

    def drawBlockD(self, qp, x, y):
        qp.fillRect(map.map[x][y].rect, QtGui.QColor(255, 50, 50, 160))

    def drawBomb(self, qp, x, y):
        qp.fillRect(map.map[x][y].rect, QtGui.QColor(0, 0, 0, 160))

    def drawBombExplode(self, qp, x, y):
        qp.fillRect(map.map[x][y].rect, QtGui.QColor(230, 20, 0, 160))

    def drawPlayer(self, qp):
        qp.fillRect(player.rect, QtGui.QColor(90, 90, 90, 160))
    def drawBot(self, qp):
        bots[0].moveBot()
        qp.fillRect(bots[0].rect, QtGui.QColor(50, 90, 50, 160))

    def drawMap(self, qp):
        self.drawBot(qp)
        for (x, y), value in np.ndenumerate(map.map):
            if value.id == 1:  # destructible block
                self.drawBlockN(qp, x, y)
            elif value.id == 2:  # indestructible block
                self.drawBlockD(qp, x, y)
            elif value.id == 3:  # bomb
                self.drawBomb(qp, x, y)
            elif value.id == 4:  # explode effect
                self.drawBombExplode(qp, x, y)
            # elif value.id == 255:
            #     self.drawPlayer(qp, x, y)

    def handleKeys(self):

        temp_x = player.rect.x()
        temp_y = player.rect.y()

        # if self.key & KEY_UP | KEY_RIGHT and not(self.unlock & COL_UP | COL_RIGHT):
        #     player.rect.setRect(player.rect.x() + 2, player.rect.y() - 2, X_PSIZE, Y_PSIZE)
        # elif self.key & KEY_DOWN | KEY_RIGHT and not(self.unlock & COL_DOWN | COL_RIGHT):
        #     player.rect.setRect(player.rect.x() + 2, player.rect.y() + 2, X_PSIZE, Y_PSIZE)
        # elif self.key & KEY_DOWN | KEY_LEFT and not(self.unlock & COL_DOWN | COL_LEFT):
        #     player.rect.setRect(player.rect.x() - 2, player.rect.y() + 2, X_PSIZE, Y_PSIZE)
        # elif self.key & KEY_UP | KEY_LEFT and not (self.unlock & COL_DOWN | COL_LEFT):
        #     player.rect.setRect(player.rect.x() - 2, player.rect.y() - 2, X_PSIZE, Y_PSIZE)
        if self.key & KEY_UP:
            for i in range(player.grid_x-1, player.grid_x+2):
                testCollision(player.rect, map.map[player.grid_x][player.grid_y - 1].rect)
            if map.map[player.grid_x][player.grid_y-1].id != 0:
                 if not player.rect.top() >= map.map[player.grid_x][player.grid_y-1].rect.bottom()+2:
                    return
            player.rect.setRect(player.rect.x(), player.rect.y() - 2, X_PSIZE, Y_PSIZE)
        elif self.key & KEY_DOWN:
            for i in range(player.grid_x - 1, player.grid_x + 2):
                if map.map[player.grid_x][player.grid_y+1].id != 0:
                    if not player.rect.bottom() <= map.map[player.grid_x][player.grid_y+1].rect.top() - 2:
                        return
            player.rect.setRect(player.rect.x(), player.rect.y() + 2, X_PSIZE, Y_PSIZE)
        elif self.key & KEY_RIGHT:
            #for i in range(player.grid_y - 1, player.grid_y + 2):
            if map.map[player.grid_x+1][player.grid_y].id != 0:
                if not player.rect.right() + 2 <= map.map[player.grid_x+1][player.grid_y].rect.left():
                    return
            player.rect.setRect(player.rect.x() + 2, player.rect.y(), X_PSIZE, Y_PSIZE)
        elif self.key & KEY_LEFT:
            #for i in range(player.grid_y - 1, player.grid_y + 2):
            if map.map[player.grid_x - 1][player.grid_y].id != 0:
                if not player.rect.left() - 2 >= map.map[player.grid_x-1][player.grid_y].rect.right():
                    return
            player.rect.setRect(player.rect.x() - 2, player.rect.y(), X_PSIZE, Y_PSIZE)

        if temp_x != player.rect.x() or temp_y != player.rect.y():
            replay.playerNode = replay.doc.createElement('player')
            replay.root.appendChild(replay.addPlayer(replay.playerNode, player, self.frameCounter))

    def keyReleaseEvent(self, e):
        if e.key() == QtCore.Qt.Key_Up:
            self.key &= ~KEY_UP
        elif e.key() == QtCore.Qt.Key_Down:
            self.key &= ~KEY_DOWN
        elif e.key() == QtCore.Qt.Key_Left:
            self.key &= ~KEY_LEFT
        elif e.key() == QtCore.Qt.Key_Right:
            self.key &= ~KEY_RIGHT
        #self.handleKeys()

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Up:
            self.key |= KEY_UP
        elif e.key() == QtCore.Qt.Key_Down:
            self.key |= KEY_DOWN
        elif e.key() == QtCore.Qt.Key_Left:
            self.key |= KEY_LEFT
        elif e.key() == QtCore.Qt.Key_Right:
            self.key |= KEY_RIGHT
        elif e.key() == QtCore.Qt.Key_Space:
            player.bombList.append(Bomb(player.grid_x, player.grid_y))
            replay.tileNode = replay.doc.createElement('tile')
            replay.root.appendChild(replay.addTile(replay.tileNode, player.grid_x, player.grid_y, 3, GUI.frameCounter))
        elif e.key() == QtCore.Qt.Key_L:
            map.loadMap(None)
        elif e.key() == QtCore.Qt.Key_S:
            map.saveMap()
        elif e.key() == QtCore.Qt.Key_K:
            replay.save()
        elif e.key() == QtCore.Qt.Key_J:
            #bots.clear()
            self.frameCounter = 0
            self.replayMode = 1
            replay.load()
        #self.handleKeys()


class QRectColor:
    def __init__(self, x, y, id):
        self.id = id
        self.rect = QtCore.QRect(x * X_SIZE, y * Y_SIZE, X_SIZE, Y_SIZE)
        self.color = QtGui.QColor(213, 217, 169, 160)


class Map:
    def __init__(self, x, y):
        #self.map = np.array([[QRectColor(i, j, 0) for j in range(x)] for i in range(y)])
        self.map = [[QRectColor(i, j, 0) for j in range(x)] for i in range(y)]
        #self.generateRandomMap()
        self.generateMap()
    #TODO zrobic tablice z typami i kolorami bloczkow

    def getCoordinates(self, x, y):
        return self.map[x][y] # zwraca 4 rogi mapy, top bottom left right

    def generateRandomMap(self):
        for i in range(0, 1600):
            x = randint(0, 39)
            y = randint(0, 39)
            self.map[x][y].id = 1

        for (x, y), value in np.ndenumerate(self.map):
            if x % 4 == 2 and y % 4 == 2:
                self.map[x][y].id = 2
        # brzydko
        self.map[0][0].id = 0
        self.map[0][1].id = 0
        self.map[1][0].id = 0

    def generateMap(self):
        for (x, y), value in np.ndenumerate(self.map):
            if x % 4 == 2 and y % 4 == 2:
                self.map[x][y].id = 2
            if x % 2 == 1 and y % 2 == 1:
                self.map[x][y].id = 1
    def saveMap(self):
        # generowanie nazwy
        path = os.getcwd()
        print(path)
        for i in range(1, 100): # zmienic
            filename = 'map'
            filename += str(i)
            if os.path.isfile(path + '\\' + filename):
                continue
            f = open(filename, 'w')
            for (x, y), value in np.ndenumerate(self.map):
                f.write(str(value.id) + ' ')
                if y % 40 == 39:
                    f.write('\n')
            break
        print('saved')

    def loadMap(self, filename):
        if filename == None:
            filename = input('nazwa pliku: ')
        y = 0
        with open(filename) as f:
            for line in f:
                x = [int(i) for i in line.split()]
                for xx in range(40):
                    self.map[xx][y].id = x[xx]
                y += 1
        print('loaded')

# class Game:
#     def __init__(self, map, players, mobs):
#         self.map = map
#         self.players = players
#         self.mobs = mobs
#         #self.time


class Player:
    next_id = 0
    def __init__(self, x, y):
        self.id = Player.next_id
        self.aimode = 0
        self.rect = QtCore.QRect(x, y, X_PSIZE, Y_PSIZE)
        #self.rect += QtCore.QMargins(2, 2, 2, 2)
        #self.rect = QRectColor(x, y, 255)
        self.collision = 0
        self.direction = -1
        self.bombList = []
        self.q = queue
        self.bombRange = 0
    @property
    def grid_x(self):
        return int((self.rect.x() + X_PSIZE/2)/X_SIZE)
    @property
    def grid_y(self):
        return int((self.rect.y() + Y_PSIZE/2)/Y_SIZE)

    def move(self, x, y):
        x *= 20
        y *= 20
        speedx = 2
        speedy = 2
        if x < self.rect.x():
            speedx = -2
        if y < self.rect.y():
            speedy = -2
        if self.rect.x() != x:
            self.rect.setRect(self.rect.x() + speedx, self.rect.y(), X_BSIZE, Y_BSIZE)
        elif self.rect.y() != y:
            self.rect.setRect(self.rect.x(), self.rect.y() + speedy, X_BSIZE, Y_BSIZE)





    # def checkCollision(self):
    #     self.rect.center()
        # for (x, y), value in np.ndenumerate(map.map):
        #     if map.map[x][y].id > 0:
        #         if self.rect.intersect(map.map[x][y].rect):
        #             self.direction = 0



class Bot:
    next_id = 0
    def __init__(self, x, y, range_a1, range_a2):
        self.id = Bot.next_id
        Bot.next_id += 1
        self.x = x
        self.y = y
        self.rect = QtCore.QRect(self.x, self.y, X_PSIZE, Y_PSIZE)
        self.range_a1 = range_a1
        self.range_a2 = range_a2
        self.dirx = 1
        self.diry = 1

    @property
    def grid_x(self):
        return int((self.rect.x() + X_BSIZE/2)/X_SIZE)

    @property
    def grid_y(self):
        return int((self.rect.y() + Y_BSIZE/2)/Y_SIZE)

    def get_x(self):
        self.rect.x() + X_BSIZE/2

    def get_y(self):
        self.rect.y() + Y_BSIZE/2

    def move(self, speed, x, y):
        self.rect.setRect(self.rect.x() + speed, self.rect.y() + speed, X_BSIZE, Y_BSIZE)

    def moveBot(self):
        if self.rect.x() == self.range_a2:
            self.dirx = -1
        elif self.rect.x() == self.range_a1:
            self.dirx = 1
        self.rect.setRect(self.rect.x() + self.dirx, self.rect.y(), X_BSIZE, Y_BSIZE)


class Bomb:
    # pole wspolne dla wszystkich bomb
    tick_time = 3000
    explode_anim = 500
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.bombRange = 4
        self.bomb_timer = QTimer()
        self.explode_timer = QTimer()
        if  map.map[x][y].id != 3:
            map.map[x][y].id = 3
        self.bomb_timer.timeout.connect(self.bombTrigger)
        #self.bomb_timer.setSingleShot(True)
        self.bomb_timer.start(Bomb.tick_time)
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
                replay.tileNode = replay.doc.createElement('tile')
                replay.root.appendChild(replay.addTile(replay.tileNode, (self.x - x1), self.y, 4, GUI.frameCounter))
                break
        for x1 in range(1, self.bombRange):
            if map.map[self.x + x1][self.y].id == 0:
                map.map[self.x + x1][self.y].id = 4
            elif map.map[self.x + x1][self.y].id == 1:
                map.map[self.x + x1][self.y].id = 4
                replay.tileNode = replay.doc.createElement('tile')
                replay.root.appendChild(replay.addTile(replay.tileNode, (self.x + x1), self.y, 4, GUI.frameCounter))
                break

        for x1 in range(1, self.bombRange):
            if map.map[self.x][self.y + x1].id == 0:
                map.map[self.x][self.y + x1].id = 4
            elif map.map[self.x][self.y + x1].id == 1:
                map.map[self.x][self.y + x1].id = 4
                replay.tileNode = replay.doc.createElement('tile')
                replay.root.appendChild(replay.addTile(replay.tileNode, self.x, (self.y + x1), 4, GUI.frameCounter))
                break
        for x1 in range(1, self.bombRange):
            if map.map[self.x][self.y - x1].id == 0:
                map.map[self.x][self.y - x1].id = 4
            elif map.map[self.x][self.y - x1].id == 1:
                map.map[self.x][self.y - x1].id = 4
                replay.tileNode = replay.doc.createElement('tile')
                replay.root.appendChild(replay.addTile(replay.tileNode, self.x, (self.y - x1), 4, GUI.frameCounter))
                break
        # for x1 in range(self.x - self.bombRange + 1, self.x + self.bombRange):
        #     if map.map[x1][self.y] == 0:
        #         map.map[x1][self.y] = 4
        #     elif map.map[x1][self.y] == 1:
        #         map.map[x1][self.y].id = 4
        #         replay.tileNode = replay.doc.createElement('tile')
        #         replay.root.appendChild(replay.addTile(replay.tileNode, x1, self.y, 4, GUI.frameCounter))
        #         break
        # for y1 in range(self.y - self.bombRange + 1, self.y + self.bombRange):
        #     if map.map[self.x][y1] == 0:
        #         map.map[self.x][y1] = 4
        #     elif map.map[self.x][y1] == 1:
        #         map.map[self.x][y1].id = 4
        #         replay.tileNode = replay.doc.createElement('tile')
        #         replay.root.appendChild(replay.addTile(replay.tileNode, self.x, y1, 4, GUI.frameCounter))
        #         break
        # for x in range(self.x-1, self.x+2):
        #     for y in range(self.y-1, self.y + 2):
        #         if map.map[x][y] == 0 or map.map[x][y] == 1 or  map.map[x][y] == 3:
        #             map.map[x][y] = 4
    def bombExplode(self):
        # nie wyglada ladnie
        map.map[self.x][self.y].id = 0
        replay.tileNode = replay.doc.createElement('tile')
        replay.root.appendChild(replay.addTile(replay.tileNode, self.x, self.y, 0, GUI.frameCounter))
        for x1 in range(self.x - self.bombRange + 1, self.x + self.bombRange):
            if map.map[x1][self.y].id == 4:
                replay.tileNode = replay.doc.createElement('tile')
                replay.root.appendChild(replay.addTile(replay.tileNode, x1, self.y, 0, GUI.frameCounter))
                map.map[x1][self.y].id = 0
        for y1 in range(self.y - self.bombRange + 1, self.y + self.bombRange):
            if map.map[self.x][y1].id == 4:
                replay.tileNode = replay.doc.createElement('tile')
                replay.root.appendChild(replay.addTile(replay.tileNode, self.x, y1, 0, GUI.frameCounter))
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

class Replay:

    def __init__(self):
        # self.f = open("filename.xml", "wb")
        self.playerList = []
        self.tileList = []
        self.doc = Document()
        self.root = self.doc.createElement('game')
        self.root.setAttribute('map', 'map1')
        #dodawanie pozycji botow
        self.botNode = self.doc.createElement('bot')
        self.root.appendChild(self.addBot(self.botNode, bots[0]))

        self.playerNode = self.doc.createElement('player')
        self.tileNode = self.doc.createElement('tile')

    def addBot(self, botNode, bot):
        botNode.setAttribute('id', str(bot.id)) # str(bot.id)
        position = str(bot.x) + ',' + str(bot.y) + ',' + str(bot.range_a1) + ',' + str(bot.range_a2)
        botNode.appendChild(self.doc.createTextNode(position))
        return botNode

    def addPlayer(self, playerNode, player, frame):
        playerNode.setAttribute('frame', str(frame))
        position = str(player.rect.x()) + ',' + str(player.rect.y())
        playerNode.appendChild(self.doc.createTextNode(position))
        return playerNode


    def addTile(self, tileNode, x, y, value, frame):
        tileNode.setAttribute('frame', str(frame))
        position = str(x) + ',' + str(y) + ',' + str(value)
        tileNode.appendChild(self.doc.createTextNode(position))
        return tileNode


    def save(self):
        self.root.appendChild(self.doc.createTextNode(''))
        self.doc.appendChild(self.root)
        self.doc.writexml(open('data.xml', 'w'),
                     indent="  ",
                     addindent="  ",
                     newl='\n')

        self.doc.unlink()
        # self.f.close()
        print('saved')
    def load(self):
        dom = parse('data.xml')
        root = dom.documentElement
        map.loadMap(root.getAttribute('map'))
        for i in dom.childNodes[0].getElementsByTagName("bot"):
            print(i.getAttribute('id')) # wartosc atrybutu
            botParam = i.firstChild.data.split(',') # wartosci ze srodka
            bots.append(Bot(int(botParam[0]), int(botParam[1]), int(botParam[2]), int(botParam[3]))) # dodajemy bota
        for i in dom.childNodes[0].getElementsByTagName("player"):
            playerxy = i.firstChild.data.split(',')
            self.playerList.append([int(i.getAttribute('frame')), int(playerxy[0]), int(playerxy[1])])
        print(self.playerList)
        for i in dom.childNodes[0].getElementsByTagName("tile"):
            i.getAttribute('frame')
            tilexyv = i.firstChild.data.split(',')
            self.tileList.append([int(i.getAttribute('frame')), int(tilexyv[0]), int(tilexyv[1]), int(tilexyv[2])])
        print(self.tileList)


# def checkCollision(object1, object2):  # slow
#     if object1.rect.intersects(object2.rect):
#         if object1.rect.y() <= object2.rect.y():
#             return 1
#         if object1.rect.y() >= object2.rect.y():
#             return 2
#         if object1.rect.x() <= object2.rect.x():
#             return 3
#         if object1.rect.x() >= object2.rect.x():
#             return 4
#     return 0
def testCollision(a, b):
    return a.right() >= b.left() and a.left() <= b.right() and a.bottom() >= b.top() and a.top() <= b.bottom();

def testPlayerCollision(a, b):
    return a.right() >= b.left()-2 and a.left() <= b.right()+2 and a.bottom() >= b.top()-2 and a.top() <= b.bottom()+2;

def checkCollision(p1, p2):
    if not testCollision(p1, p2):
        return 0

    if (p1.bottom() >= p2.top()): #z dolu
        return 1

    elif (p1.right() >= p2.left()): #z prawej
        return 2

    elif (p1.left() >= p2.right()): # z lewej
        return 3

    elif (p1.top() <= p2.bottom()): #z gory
        return 4


def restart():
    bots.clear()
    bots.append(Bot(100, 320, 0, 300))
    map.generateMap()
    player.rect.setRect(0, 0, X_PSIZE, Y_PSIZE)
    GUI.repaint()

bots = []
bots.append(Bot(100, 320, 0, 300))
map = Map(40, 40)
player = Player(0, 0)
#player.q.heappush()
app = QtWidgets.QApplication(sys.argv)
GUI = Window()
replay = Replay()
sys.exit(app.exec_())

