import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtWidgets, QtCore


class TestForm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("PyQT TEST")
        self.setGeometry(800,400,900,600)

        btn_1 = QPushButton("1" , self)
        btn_2 = QPushButton("2", self)
        btn_3 = QPushButton("3" , self)

        btn_1.move(20, 20)
        btn_2.move(20, 60)
        btn_3.move(20, 100)

        btn_1.clicked.connect(self.btn_1_clicked)
        btn_2.clicked.connect(self.btn_2_clicked)
        btn_3.clicked.connect(QCoreApplication.instance().quit)

        btn_4 = QLabel("4", self)
        btn_5 = QLabel("5", self)

        btn_4.move(140, 300)
        btn_5.move(140, 20)

        self.lineEdit = QLineEdit("", self)
        self.plainEdit = QtWidgets.QPlainTextEdit(self)

        self.lineEdit.move(160, 300)
        self.plainEdit.setGeometry(QtCore.QRect(160, 20, 361, 231))

        self.lineEdit.textChanged.connect(self.lineEditChanged)
        self.lineEdit.returnPressed.connect(self.lineEditEnter)

        #하단 상태바
        self.statusBar = QStatusBar(self)
        self.setStatusBar(self.statusBar)

    def lineEditChanged(self):
        self.statusBar.showMessage(self.lineEdit.text())

    def lineEditEnter(self):
        self.plainEdit.appendPlainText(self.lineEdit.text())
        self.lineEdit.clear()




    def btn_1_clicked(self):
        QMessageBox.about(self, "Message","clicked")

    def btn_2_clicked(self):
        print("button clicked")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TestForm()
    window.show()
    app.exec_()



# app = QApplication(sys.argv)
# #print(sys.argv)
# label = QLabel("QyQT First Test")
#
# label.show()
# app.exec()