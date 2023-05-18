from PyQt5.QtGui import QIcon 
from PyQt5.QtWidgets import QMessageBox,QDialog,QTableWidgetItem ,QMainWindow
from PyQt5.QtCore import QCoreApplication,QTimer,QElapsedTimer, Qt
from PyQt5 import QtWidgets, uic
from datetime import datetime as dt
import sys,sqlite3,os

class NuevaEntrada(QDialog):
    def __init__(self,maquina):
        QDialog.__init__(self)
        uic.loadUi("nueva-entrada.ui",self)
        self.MAQUINA.setText(maquina)
        self.setWindowTitle("Sistema de informacion Stoll - Tina - Digito")
        self.CANCELAR.clicked.connect(self.close)
        self.GUARDAR.clicked.connect(lambda:self.guardar(self.buscarid(maquina)))

    def guardar(self,idmaquina):
        try:
            conexion = sqlite3.connect("STOLL.db")
            conexion.execute("Insert into trabajos values (?,?,?,?,?,?,?)",(idmaquina,self.LOTE.text(),self.ARTICULO.text(),self.TALLE.text(),self.TIPOPIEZA.text(),self.CANTIDADES.text(),self.TIPOHILADO.text(),))
            conexion.commit()
            conexion.close()
            QMessageBox.information(self,"Guardar","Datos almacenados correctamente")
            self.close()
        except Exception as e:
            QMessageBox.information(self,"Error",f"Error al guardar los datos \n{str(e)}")
    def buscarid(self,maq):
        conexion = sqlite3.connect("STOLL.db")
        datos = conexion.execute(f"Select * from maquinas where Nombre='{maq}' ")
        for dato in datos:
            return dato[0]