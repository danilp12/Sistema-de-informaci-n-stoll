
from PyQt5.QtGui import QIcon 
from PyQt5.QtWidgets import QMessageBox,QDialog,QTableWidgetItem ,QMainWindow
from PyQt5.QtCore import QCoreApplication,QTimer,QElapsedTimer, Qt
from PyQt5 import QtWidgets, uic
from datetime import datetime as dt
import sys,sqlite3,os

class Historial(QDialog):
    def __init__(self,maquina):
        QDialog.__init__(self)
        uic.loadUi("historial.ui",self)
        self.MAQUINA.setText(maquina)
        self.setWindowTitle("Sistema de informacion Stoll - Tina - Digito")
        self.cargartabla(maquina)

    def buscarid(self,maq):
        conexion = sqlite3.connect("STOLL.db")
        datos = conexion.execute(f"Select * from maquinas where Nombre='{maq}' ")
        for dato in datos:
            return dato[0]
    def cargartabla(self,idmaquina):
        conexion = sqlite3.connect("STOLL.db")
        datos = conexion.execute(f"Select * from trabajos_completados where ID = '{self.buscarid(idmaquina)}'")
        self.TABLA.setRowCount(0)
        for dato in datos:
            self.TABLA.insertRow(self.TABLA.rowCount())
            self.TABLA.setItem(self.TABLA.rowCount()-1,0,QTableWidgetItem(dato[1]))
            self.TABLA.setItem(self.TABLA.rowCount()-1,1,QTableWidgetItem(dato[2]))
            self.TABLA.setItem(self.TABLA.rowCount()-1,2,QTableWidgetItem(dato[3]))
            self.TABLA.setItem(self.TABLA.rowCount()-1,3,QTableWidgetItem(dato[4]))
            self.TABLA.setItem(self.TABLA.rowCount()-1,4,QTableWidgetItem(dato[5]))
            self.TABLA.setItem(self.TABLA.rowCount()-1,5,QTableWidgetItem(dato[6]))
            self.TABLA.setItem(self.TABLA.rowCount()-1,6,QTableWidgetItem(dato[7]))
            self.TABLA.setItem(self.TABLA.rowCount()-1,7,QTableWidgetItem(dato[8]))
        conexion.close()
