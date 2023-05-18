

from PyQt5.QtGui import QIcon 
from PyQt5.QtWidgets import QMessageBox,QDialog,QTableWidgetItem ,QInputDialog
from PyQt5.QtCore import QCoreApplication,QTimer,QElapsedTimer, Qt
from PyQt5 import QtWidgets, uic
from datetime import datetime as dt
import sys,sqlite3,os
from nueva_entrada import NuevaEntrada
from historial import Historial

class Maquinas(QDialog):
    def __init__(self,maquina):
        QDialog.__init__(self)
        uic.loadUi("form-trabajo.ui",self)
        self.Maquina.setText(maquina)
        self.setWindowTitle("Sistema de informacion Stoll - Tina - Digito")
        self.maquina = maquina
        self.NUEVO.clicked.connect(self.nuevo)
        self.HISTORIAL.clicked.connect(self.historial)
        self.GUARDAR_ANOTACIONES.clicked.connect(lambda: self.guarda_anotaciones(self.buscarid(maquina)))
        self.ELIMINAR.clicked.connect(lambda: self.eliminar(self.buscarid(maquina)))
        self.PASAR_ACTUAL.clicked.connect(lambda : self.pasarActual(self.buscarid(maquina)))
        self.PASAR_SIGUIENTE.clicked.connect(lambda : self.pasarSiguiente(self.buscarid(maquina)))
        self.COMPLETADO.clicked.connect(lambda : self.pasarCompletado(self.buscarid(maquina)))
        self.cargartablasiguiente(self.maquina)
        self.cargartablaactual(self.maquina)
        self.carga_anotaciones(self.maquina)
    def guarda_anotaciones(self,idmaquina):
        conexion = sqlite3.connect("STOLL.db")
        conexion.execute(f"Update anotaciones set anotacion = '{self.ANOTACIONES.toPlainText()}' where ID = '{idmaquina}'")
        conexion.commit()
        conexion.close()
        QMessageBox.information(self,"Anotaciones","Anotaciones Guardadas")
    def carga_anotaciones(self,idmaquina):
        conexion = sqlite3.connect("STOLL.db")
        datos = conexion.execute(f"select * from anotaciones where ID = '{self.buscarid(idmaquina)}'")
        for dato in datos:
            self.ANOTACIONES.setText(dato[1])
    def pasarCompletado(self,idmaquina):
        if self.ACTUAL.currentRow() != -1:
            tejedor,ok = QInputDialog.getText(self,"Responsable Tejedor","Ingresar el Responsable del tejido")
            if ok:
                try:
                    conexion = sqlite3.connect("STOLL.db")
                    conexion.execute("Insert into trabajos_completados values (?,?,?,?,?,?,?,?,?)",(idmaquina,self.ACTUAL.item(self.ACTUAL.currentRow(),0).text(),self.ACTUAL.item(self.ACTUAL.currentRow(),1).text(),self.ACTUAL.item(self.ACTUAL.currentRow(),2).text(),self.ACTUAL.item(self.ACTUAL.currentRow(),3).text(),self.ACTUAL.item(self.ACTUAL.currentRow(),4).text(),self.ACTUAL.item(self.ACTUAL.currentRow(),5).text(),str(dt.now())[:19],tejedor))
                    conexion.execute(f"Delete from trabajos_actual where (ID = '{idmaquina}') and (lote='{self.ACTUAL.item(self.ACTUAL.currentRow(),0).text()}') and (articulo = '{self.ACTUAL.item(self.ACTUAL.currentRow(),1).text()}') and (talle='{self.ACTUAL.item(self.ACTUAL.currentRow(),2).text()}') and (tipopieza='{self.ACTUAL.item(self.ACTUAL.currentRow(),3).text()}') and (cantidades='{self.ACTUAL.item(self.ACTUAL.currentRow(),4).text()}')")
                    conexion.commit()
                    conexion.close()
                except Exception as e:
                    QMessageBox.information(self,"Error",str(e))
        self.cargartablaactual(self.maquina)
        self.cargartablasiguiente(self.maquina)
    def pasarActual(self,idmaquina):
        if self.SIGUIENTE.currentRow() != -1:
            try:
                conexion = sqlite3.connect("STOLL.db")
                conexion.execute("Insert into trabajos_actual values (?,?,?,?,?,?,?)",(idmaquina,self.SIGUIENTE.item(self.SIGUIENTE.currentRow(),0).text(),self.SIGUIENTE.item(self.SIGUIENTE.currentRow(),1).text(),self.SIGUIENTE.item(self.SIGUIENTE.currentRow(),2).text(),self.SIGUIENTE.item(self.SIGUIENTE.currentRow(),3).text(),self.SIGUIENTE.item(self.SIGUIENTE.currentRow(),4).text(),self.SIGUIENTE.item(self.SIGUIENTE.currentRow(),5).text()))
                conexion.execute(f"Delete from trabajos where (ID = '{idmaquina}') and (lote='{self.SIGUIENTE.item(self.SIGUIENTE.currentRow(),0).text()}') and (articulo = '{self.SIGUIENTE.item(self.SIGUIENTE.currentRow(),1).text()}') and (talle='{self.SIGUIENTE.item(self.SIGUIENTE.currentRow(),2).text()}') and (tipopieza='{self.SIGUIENTE.item(self.SIGUIENTE.currentRow(),3).text()}') and (cantidades='{self.SIGUIENTE.item(self.SIGUIENTE.currentRow(),4).text()}')")
                conexion.commit()
                conexion.close()
            except Exception as e:
                QMessageBox.information(self,"Error",str(e))
        self.cargartablaactual(self.maquina)
        self.cargartablasiguiente(self.maquina)
    def pasarSiguiente(self,idmaquina):
        if self.ACTUAL.currentRow() != -1:
            try:
                conexion = sqlite3.connect("STOLL.db")
                conexion.execute("Insert into trabajos values (?,?,?,?,?,?,?)",(idmaquina,self.ACTUAL.item(self.ACTUAL.currentRow(),0).text(),self.ACTUAL.item(self.ACTUAL.currentRow(),1).text(),self.ACTUAL.item(self.ACTUAL.currentRow(),2).text(),self.ACTUAL.item(self.ACTUAL.currentRow(),3).text(),self.ACTUAL.item(self.ACTUAL.currentRow(),4).text(),self.ACTUAL.item(self.ACTUAL.currentRow(),5).text()))
                conexion.execute(f"Delete from trabajos_actual where (ID = '{idmaquina}') and (lote='{self.ACTUAL.item(self.ACTUAL.currentRow(),0).text()}') and (articulo = '{self.ACTUAL.item(self.ACTUAL.currentRow(),1).text()}') and (talle='{self.ACTUAL.item(self.ACTUAL.currentRow(),2).text()}') and (tipopieza='{self.ACTUAL.item(self.ACTUAL.currentRow(),3).text()}') and (cantidades='{self.ACTUAL.item(self.ACTUAL.currentRow(),4).text()}')")
                conexion.commit()
                conexion.close()
            except Exception as e:
                QMessageBox.information(self,"Error",str(e))
        self.cargartablaactual(self.maquina)
        self.cargartablasiguiente(self.maquina)
    def buscarid(self,maq):
        conexion = sqlite3.connect("STOLL.db")
        datos = conexion.execute(f"Select * from maquinas where Nombre='{maq}' ")
        for dato in datos:
            return dato[0]
    def nuevo(self):
        nue = NuevaEntrada(self.maquina)
        nue.exec_()
        self.cargartablasiguiente(self.maquina)
    def historial(self):
        hist = Historial(self.maquina)
        hist.exec_()
    def eliminar(self,idmaquina):
        if self.SIGUIENTE.currentRow() != -1:
            if QMessageBox.question(self,"Eliminar","Seguro que desea eliminar el tejido seleccionado?",QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes):
                try:
                    conexion = sqlite3.connect("STOLL.db")
                    conexion.execute(f"Delete from trabajos where (ID = '{idmaquina}') and (lote='{self.SIGUIENTE.item(self.SIGUIENTE.currentRow(),0).text()}') and (articulo = '{self.SIGUIENTE.item(self.SIGUIENTE.currentRow(),1).text()}') and (talle='{self.SIGUIENTE.item(self.SIGUIENTE.currentRow(),2).text()}') and (tipopieza='{self.SIGUIENTE.item(self.SIGUIENTE.currentRow(),3).text()}') and (cantidades='{self.SIGUIENTE.item(self.SIGUIENTE.currentRow(),4).text()}')")
                    conexion.commit()
                    conexion.close()
                    QMessageBox.information(self,"Eliminar","Datos eliminados")
                except Exception as e:
                    QMessageBox.information(self,"Error",f"Error al eliminar \n {str(e)}")
            self.cargartablaactual(self.maquina)
            self.cargartablasiguiente(self.maquina)
    def cargartablasiguiente(self,maquina):
        conexion = sqlite3.connect("STOLL.db")
        datos = conexion.execute(f"Select * from trabajos where ID={self.buscarid(maquina)}")
        self.SIGUIENTE.setRowCount(0)
        for dato in datos:
            self.SIGUIENTE.insertRow(self.SIGUIENTE.rowCount())
            self.SIGUIENTE.setItem(self.SIGUIENTE.rowCount()-1,0,QTableWidgetItem(dato[1]))
            self.SIGUIENTE.setItem(self.SIGUIENTE.rowCount()-1,1,QTableWidgetItem(dato[2]))
            self.SIGUIENTE.setItem(self.SIGUIENTE.rowCount()-1,2,QTableWidgetItem(dato[3]))
            self.SIGUIENTE.setItem(self.SIGUIENTE.rowCount()-1,3,QTableWidgetItem(dato[4]))
            self.SIGUIENTE.setItem(self.SIGUIENTE.rowCount()-1,4,QTableWidgetItem(dato[5]))
            self.SIGUIENTE.setItem(self.SIGUIENTE.rowCount()-1,5,QTableWidgetItem(dato[6]))
        conexion.close()
    def cargartablaactual(self,maquina):
        conexion = sqlite3.connect("STOLL.db")
        datos = conexion.execute(f"Select * from trabajos_actual where ID={self.buscarid(maquina)}")
        self.ACTUAL.setRowCount(0)
        for dato in datos:
            self.ACTUAL.insertRow(self.ACTUAL.rowCount())
            self.ACTUAL.setItem(self.ACTUAL.rowCount()-1,0,QTableWidgetItem(dato[1]))
            self.ACTUAL.setItem(self.ACTUAL.rowCount()-1,1,QTableWidgetItem(dato[2]))
            self.ACTUAL.setItem(self.ACTUAL.rowCount()-1,2,QTableWidgetItem(dato[3]))
            self.ACTUAL.setItem(self.ACTUAL.rowCount()-1,3,QTableWidgetItem(dato[4]))
            self.ACTUAL.setItem(self.ACTUAL.rowCount()-1,4,QTableWidgetItem(dato[5]))
            self.ACTUAL.setItem(self.ACTUAL.rowCount()-1,5,QTableWidgetItem(dato[6]))
        conexion.close()