import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

if __name__ == '__main__':
    app = QApplication(sys.argv)

    model = QDirModel()
    tree = QTreeView()
    tree.setModel(model)
    tree.setWindowTitle("QTreeView")
    tree.resize(640, 480)

    tree.show()
    sys.exit(app.exec_())


class WindowA(QDialog):
    def __init__(self, controller):
        super(WindowA, self).__init__()
        self.controller = controller
        layout = QVBoxLayout()
        self.button = QPushButton('Launch B')
        self.button.clicked.connect(self.controller.launchB)
        layout.addWidget(self.button)
        self.setLayout(layout)
        self.show()