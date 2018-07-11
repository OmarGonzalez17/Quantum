from PyQt5 import QtCore, QtGui, QtWidgets, QtOpenGL
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys

width = 1000
radius = 100
dog = [1, 1, 1, 1, 1, 1, 1, 1, 1]


#unit = int((width - radius) / 2) #3x3 from 0,0
unit = width - 3*radius #2*2 from r,r
def adj(x, y):
    lin_adj_pairs = []
    dia_adj_pairs = []
    pp_x = [x-unit, x, x + unit]
    pp_y = [y-unit, y, y + unit]

    for a in pp_x:
        for b in pp_y:

            if (a >= 0) and (a <= width-radius):
                if (b >= 0) and (b <= width-radius):
                    if a == x or b == y:
                        lin_adj_pairs.append([a, b])
                    else:
                        dia_adj_pairs.append([a, b])

    lin_adj_pairs.remove([x, y])
    return lin_adj_pairs, dia_adj_pairs

def find_quandrant(a, b):
    quads = [(1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3), (3, 1), (3, 2), (3, 3)]
    if (a >= 0) and (a < width / 3):
        q1 = 1
    elif (a >= width / 3) and (a < width * 2 / 3):
        q1 = 2
    else:
        q1 = 3

    if (b >= 0) and (b < width / 3):
        q2 = 1
    elif (b >= width / 3) and (b < width * 2 / 3):
        q2 = 2
    else:
        q2 = 3

    for i in quads:
        if (q1, q2) == i:
            return quads.index(i)


class Window(QMainWindow):

    def __init__(self):
        super().__init__()

        self.title = "Quantum Measure"
        self.top = 15
        self.left = 20
        self.width = width
        self.height = width
        self.x = 1
        self.y = 1
        self.mode = "3*3"
        self.f = QFont("Times", 15)
        #self.inp = input("Enter which size you want the simulation to be (2*2, 4*4, 8*8, 16*16) : ")

        self.initWindow()

    def mousePressEvent(self, QMouseEvent):
        #print(QMouseEvent.pos())
        variable = QMouseEvent.pos()
        x = int(variable.x())
        y = int(variable.y())

        labelpos = find_quandrant(x, y)

        if dog[labelpos] == 1:
            dog[labelpos] = 0
        else:
            dog[labelpos] = 1


        self.close()
        self.initWindow()

    def mouseReleaseEvent(self, QMouseEvent):
        cursor = QtGui.QCursor()
        variable = cursor.pos()
        #variable.QPoint()

    def initWindow(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.show()

    def paintEvent(self, event):
        #list_coord = [0, int((width - radius)/2), width - radius] #3x3 from 0,0
        list_coord = [radius, width - radius - radius] #2*2 from r,r
        drawn_circles = []
        count = 0
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 8, Qt.SolidLine))
        painter.setFont(self.f)

        for i in list_coord:
            for j in list_coord:
                quadrant_found = find_quandrant(i, j)
                if dog[quadrant_found] == 1:
                    drawn_circles.append([i, j])
                    painter.drawEllipse(i, j, radius, radius)
                    painter.drawRect((i + radius/4), (j + radius/4), (radius/2), (radius/2))
                    painter.drawText((i + radius/2.3), (j + radius/2.8), radius/2, radius/2, True, str(quadrant_found))

                    lin_adj_pairs, dia_adj_pairs = adj(i, j)

                    for k in lin_adj_pairs:
                        if k in drawn_circles:
                            if k[1] < j:
                                painter.drawLine(i + radius/2, j, k[0] + radius/2, k[1] + radius)
                            if k[0] < i:
                                painter.drawLine(i, j + radius/2, k[0] + radius, k[1] + radius/2)
                # if


def main():
    App = QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec_())

main()

