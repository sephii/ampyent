import sys
from PySide import QtGui

class Example(QtGui.QMainWindow):

    def __init__(self):
        super(Example, self).__init__()

        self.initUI()

    def initUI(self):
        self.init_menu()
        self.init_toolbar()

        #topleft = QtGui.QFrame(self)
        #topleft.setFrameShape(QtGui.QFrame.StyledPanel)
        hbox = QtGui.QHBoxLayout()
        l = QtGui.QListWidget(self)
        #hbox.addWidget(l)
        #hbox.addWidget(topleft)

        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('Cleanlooks'))

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Toolbar')
        self.show()

    def init_menu(self):
        loadAction = QtGui.QAction(QtGui.QIcon('data/icons/play.png'), 'Load', self)
        loadAction.triggered.connect(QtGui.qApp.quit)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(loadAction)


    def init_toolbar(self):
        playAction = QtGui.QAction(QtGui.QIcon('data/icons/play.png'), 'Play', self)
        playAction.setShortcut('Ctrl+P')
        playAction.triggered.connect(QtGui.qApp.quit)

        self.toolbar = self.addToolBar('Scene')
        self.toolbar.addAction(playAction)


def main():

    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
