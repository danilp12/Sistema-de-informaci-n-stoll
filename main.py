
from PyQt5.QtGui import QIcon 
from PyQt5.QtWidgets import QMessageBox,QDialog,QTableWidgetItem ,QMainWindow
from PyQt5.QtCore import QCoreApplication,QTimer,QElapsedTimer, Qt
from PyQt5 import QtWidgets, uic
from datetime import datetime as dt
import sys,sqlite3,os
from maquinas import Maquinas
timer = QTimer()

class Ventana(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("mainwindow.ui",self)
        self.setWindowTitle("Sistema de informacion Stoll - Tina - Digito")
        self.bms.clicked.connect(lambda : self.abrirdialogo(self.bms.text()))
        self.cms340.clicked.connect(lambda : self.abrirdialogo(self.cms340.text()))
        self.cmsg5.clicked.connect(lambda : self.abrirdialogo(self.cmsg5.text()))
        self.cms12.clicked.connect(lambda : self.abrirdialogo(self.cms12.text()))
        self.tc433.clicked.connect(lambda : self.abrirdialogo(self.tc433.text()))
        self.hp822.clicked.connect(lambda : self.abrirdialogo(self.hp822.text()))
        self.tc4.clicked.connect(lambda : self.abrirdialogo(self.tc4.text()))
        self.tiempo()
    def abrirdialogo(self,maquina):
        maq = Maquinas(maquina)
        maq.exec_()
    def tiempo(self):
        timer.start(1000)
        timer.timeout.connect(self.actualizar_tiempo)
    def actualizar_tiempo(self):
        self.FECHA.setText(str(dt.now())[:19])
        

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ventana = Ventana()
    ventana.show()
    sys.exit(app.exec_())