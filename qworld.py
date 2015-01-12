from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.Qt import Qt

class WorldView(QtWidgets.QWidget):
    def __init__(self, scale, parent):
        super(WorldView, self).__init__(parent)

        self.world = parent.world
        self.resize(self.world.area[0], self.world.area[1])

        self.scale = scale
        self.food_scale = scale * 0.5

        self.mooses = []
        self.flip_mooses = []
        self.food = None

        self.load_images()

    def load_images(self):
        self.mooses.append(QtGui.QImage('img/moose1.png'))
        self.mooses.append(QtGui.QImage('img/moose2.png'))
        self.mooses.append(QtGui.QImage('img/moose3.png'))
        self.mooses.append(QtGui.QImage('img/moose4.png'))
        self.food = QtGui.QImage('img/food.png')

        self.mooses = [x.scaled(int(x.width() * self.scale), int(x.height() * self.scale)) for x in self.mooses]
        self.flip_mooses = [x.copy().mirrored(horizontal=True, vertical=False) for x in self.mooses]
        self.food = self.food.scaled(int(self.food.width() * self.food_scale), int(self.food.height() * self.food_scale))

    def paintEvent(self, event):
        paint = QtGui.QPainter()
        paint.begin(self)

        paint.fillRect(QtCore.QRectF(QtCore.QPointF(0, 0), QtCore.QPointF(self.width(), self.height())), QtGui.QColor(0, 100, 0, 255))
        for food in self.world.food:
            if not food.active:
                continue
            paint.drawImage(QtCore.QPointF(food.x, food.y), self.food)

        for moose in self.world.animals:
            if not moose.item.alive:
                continue
            if moose.xspeed > 0:
                moo = self.flip_mooses[int(moose.item.shape, 2)]
            else:
                moo = self.mooses[int(moose.item.shape, 2)]
            paint.drawImage(QtCore.QPointF(moose.x, moose.y + moose.yshift), moo)

        paint.end()


class QWorld(QtWidgets.QWidget):
    def __init__(self, world, scale=1.0):
        super(QWorld, self).__init__()

        self.world = world

        self._layout = QtWidgets.QHBoxLayout()

        self._view = WorldView(scale, self)

        self.resize(800, 600)
        self.setWindowTitle('Mooses')

        self._layout.addWidget(self._view)
        self.setLayout(self._layout)

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self._view.update)
        self.timer.start(100)
