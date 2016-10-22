import sys
from PyQt4 import QtGui, QtCore, uic
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import random
import uuid

servidorUi = uic.loadUiType("servidor2.ui")[0] #Se carga la interfaz de tipo ui del servidor
 
class Servidor(QtGui.QMainWindow, servidorUi):

	def __init__(self, parent=None):#Constructor de la ventana
		QtGui.QMainWindow.__init__(self, parent)
		self.setupUi(self)#Inicializa la interfaz del tipo ui

		self.tableWidget.horizontalHeader().setResizeMode(QHeaderView.Stretch) #Como su nombre lo dice estira a las columnas horizontales para adaptarse a la widget
		self.tableWidget.verticalHeader().setResizeMode(QHeaderView.Stretch) #Lo mismo para las verticales
		self.tableWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff) #Cuando las celdas son bastantes, la scrollbar aparece, este basicamente las hace desaparecer
		self.tableWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff) #Tambien las verticales (Con las de 20 columnas, 20 filas, aparecía)

		self.columnas.setMaximum(99) #Ajusta cuantos se puede recibir como maximo en la spinbox para las columnas
		self.columnas.setMinimum(10) #Ajusta cuantos se puede recibir como minimo en la spinbox para las columnas
		self.columnas.valueChanged.connect(self.ajustaColumnas) #Conecta los valores de la spinbox al metodo

		self.filas.setMaximum(99) #Ajusta cuantos se puede recibir como maximo en la spinbox para las filas
		self.filas.setMinimum(10) #Ajusta cuantos se puede recibir como minimo en la spinbox para las filas

		self.espera.setMaximum(999)
		self.espera.setMinimum(10)
		self.espera.setValue(150)

		self.timeout.valueChanged.connect(self.esperame)

		self.filas.valueChanged.connect(self.ajustaRenglones)
		self.espera.valueChanged.connect(self.speed) #Conecta los valores de la spinbox con el metodo

		self.tableWidget.setColumnCount(self.columnas.value()) #Inicia las columnas en el minimo de la spinbox
		self.tableWidget.setRowCount(self.filas.value()) #Inicia las filas en el minimo de la spinbox
		
		self.tableWidget.keyPressEvent = self.keyPressEvent
		self.iniciajuego.clicked.connect(self.playGameButton)
		self.pushButton_2.clicked.connect(self.termina)
		self.pushButton_2.hide()
		self.serverstart.clicked.connect(self.sirve)
		self.dire= 2
		self.misViboras=[]
		self.misViborasInfo= []
		
	def ajustaColumnas(self, columnas): #Cambia las columnas cuando se cambia el valor de la spinbox
		self.tableWidget.setColumnCount(columnas)

	def ajustaRenglones(self, renglones): #Cambia las filas cuando se cambia el valor de la spinbox
		self.tableWidget.setRowCount(renglones)

	def speed(self, velocidad):
		self.timer.setInterval(velocidad)

	def esperame(self,cuanto):
		self.timeout.setValue(cuanto)

	def matame(self):
		if self.snake.coordenadas[1] == self.snake.coordenadas[9] and self.snake.coordenadas[0] == self.snake.coordenadas[8]:
			return True

		#Inicia el juego
	def playGameButton(self):
		if self.iniciajuego.text() == "Inicia Juego":
			self.snake = self.snakeMaker()
			self.dire= self.snake.direccion
			self.misViboras.append(self.snake.id)
			self.iniciajuego.setText("Pausar el juego")#Cambia el texto del boton

			self.pushButton_2.show()

			self.timer = QTimer()
			self.timer.timeout.connect(self.condicional)
			self.timer.start(150)

			self.espera.setValue(150)

		elif self.iniciajuego.text() == "Pausar el juego":
			self.timer.stop()
			self.iniciajuego.setText("Reanudar juego")
		else: 
			self.timer.start(self.espera.value())
			self.iniciajuego.setText("Pausar el juego")
 

	def caminaDerecha(self):

		self.desaparece(self.snake)
		self.snake.todenuevo()
		self.snake.coordenadas[8], self.snake.coordenadas[9] = self.snake.coordenadas[6], self.snake.coordenadas[7]
		self.snake.coordenadas[6], self.snake.coordenadas[7] = self.snake.coordenadas[4], self.snake.coordenadas[5]
		self.snake.coordenadas[4], self.snake.coordenadas[5] = self.snake.coordenadas[2], self.snake.coordenadas[3]
		self.snake.coordenadas[2], self.snake.coordenadas[3] = self.snake.coordenadas[0], self.snake.coordenadas[1]
		self.snake.coordenadas[0], self.snake.coordenadas[1] = self.snake.coordenadas[0], (self.snake.coordenadas[1] + 1)% self.tableWidget.columnCount()
		self.aparece(self.snake)

	def caminaIzquierda(self):

		self.desaparece(self.snake)
		self.snake.todenuevo()
		self.snake.coordenadas[8], self.snake.coordenadas[9] = self.snake.coordenadas[6], self.snake.coordenadas[7]
		self.snake.coordenadas[6], self.snake.coordenadas[7] = self.snake.coordenadas[4], self.snake.coordenadas[5]
		self.snake.coordenadas[4], self.snake.coordenadas[5] = self.snake.coordenadas[2], self.snake.coordenadas[3]
		self.snake.coordenadas[2], self.snake.coordenadas[3] = self.snake.coordenadas[0], self.snake.coordenadas[1]
		self.snake.coordenadas[0], self.snake.coordenadas[1] = self.snake.coordenadas[0], (self.snake.coordenadas[1] - 1)% self.tableWidget.columnCount()
		self.aparece(self.snake)

	def caminaArriba(self):

		self.desaparece(self.snake)
		self.snake.todenuevo()
		self.snake.coordenadas[8], self.snake.coordenadas[9] = self.snake.coordenadas[6], self.snake.coordenadas[7]
		self.snake.coordenadas[6], self.snake.coordenadas[7] = self.snake.coordenadas[4], self.snake.coordenadas[5]
		self.snake.coordenadas[4], self.snake.coordenadas[5] = self.snake.coordenadas[2], self.snake.coordenadas[3]
		self.snake.coordenadas[2], self.snake.coordenadas[3] = self.snake.coordenadas[0], self.snake.coordenadas[1]
		self.snake.coordenadas[0], self.snake.coordenadas[1] = (self.snake.coordenadas[0]-1)%self.tableWidget.rowCount(), self.snake.coordenadas[1] 
		self.aparece(self.snake)

	def caminaAbajo(self):

		self.desaparece(self.snake)
		self.snake.todenuevo()
		self.snake.coordenadas[8], self.snake.coordenadas[9] = self.snake.coordenadas[6], self.snake.coordenadas[7]
		self.snake.coordenadas[6], self.snake.coordenadas[7] = self.snake.coordenadas[4], self.snake.coordenadas[5]
		self.snake.coordenadas[4], self.snake.coordenadas[5] = self.snake.coordenadas[2], self.snake.coordenadas[3]
		self.snake.coordenadas[2], self.snake.coordenadas[3] = self.snake.coordenadas[0], self.snake.coordenadas[1]
		self.snake.coordenadas[0], self.snake.coordenadas[1] = (self.snake.coordenadas[0]+1)%self.tableWidget.rowCount(), self.snake.coordenadas[1] 
		self.aparece(self.snake)

	def condicional(self):
		if self.dire == 0:
			self.mueveVib(0)
		elif self.dire == 1:
			self.mueveVib(1)
		elif self.dire == 2:
			self.mueveVib(2)
		elif self.dire == 3:  
			self.mueveVib(3)
		if self.matame():
			self.termina()

	def mueveVib(self, dir):
		if dir == 0:
			self.caminaArriba()
		elif dir == 1:
			self.caminaDerecha()
		elif dir == 2:
			self.caminaAbajo()
		elif self.dire == 3:
			self.caminaIzquierda()

	def keyPressEvent(self,event):
		if event.key() == QtCore.Qt.Key_Left and self.dire != 1:
			self.dire= 3
		elif event.key() == QtCore.Qt.Key_Right and self.dire != 3:
			self.dire= 1
		elif event.key() == QtCore.Qt.Key_Up and self.dire != 2:
			self.dire= 0
		elif event.key() == QtCore.Qt.Key_Down and self.dire != 0:
			self.dire= 2
	
	def termina(self):
		self.iniciajuego.setText("Inicia Juego")#Cambia el texto del boton
		self.desaparece(self.snake)
		self.pushButton_2.hide()
		self.timer.stop()

	def sirve(self):
		if self.puerto.value()==0:
			self.servidor = SimpleXMLRPCServer((self.url.text(), 8000), allow_none= True) #Creamos nuestro objeto servidor en la clase
		else:
			self.servidor = SimpleXMLRPCServer((self.url.text(), self.puerto.value()), allow_none= True)

		self.servidor.timeout = self.timeout.value()
		self.servidor.register_function(self.ping)
		self.servidor.register_function(self.yo_juego)
		self.servidor.register_function(self.estado_del_juego)
		self.servidor.register_function(self.camba_direccion)
		self.krusty= QTimer(self)
		self.krusty.timeout.connect(self.cliente)
		self.krusty.start(100)

	#Así como en el ejemplo esta funcion va a escuchar por una llamada del cliente, si la escucha regresara una funcion
	def cliente(self):
		self.servidor.handle_request()

	#Metodo que regresa un pong por cada ping
	def ping(self):
		return "¡Pong!"

	#metodo que devuelve las propiedades de la vibora
	def yo_juego(self):
		vivora = self.snakeMaker()
		self.misViboras.append(vivora)
		return {"id": vivora.id, "color": {"r": vivora.color[0], "g": vivora.color[1], "b": vivora.color[2]}}

	def dentro(self, tekayas):
		for i in range[len(self.misViboras)]:
			if self.misViboras[i].id == tekayas:
				return True

	def camba_direccion(self,identificador,direccioname):
		if self.dentro(identificador):
			if direccioname == 0:
				self.dire = 0
			if direccioname == 1:
				self.dire = 1
			if direccioname == 2:
				self.dire = 2
			if direccioname == 3:
				self.dire = 3
		else:
			return "No esta la serpiente en el juego"

	def estado_del_juego(self):
		return {"espera": self.espera.value(), "tamX": self.tableWidget.columnCount(), "tamY": self.tableWidget.rowCount(), "vivoras":self.misViborasInfo}


	#Creamos el objeto vivora
	def snakeMaker(self):
		id = self.identificadores() #Le damos en forma de string un identificador a la vivora
		color = self.colores()
		coordenadas = self.coordenates()
		vivora = Vivora(id,color,coordenadas,2)
		self.misViborasInfo.append({"id": id, "camino": coordenadas, "color": color})
		return vivora

	def aparece(self,vivora):
		self.tableWidget.setItem(vivora.coordenadas[0], vivora.coordenadas[1], vivora.cabezaSnake)
		self.tableWidget.setItem(vivora.coordenadas[2], vivora.coordenadas[3], vivora.cuerpoSnake1)
		self.tableWidget.setItem(vivora.coordenadas[4], vivora.coordenadas[5], vivora.cuerpoSnake2)
		self.tableWidget.setItem(vivora.coordenadas[6], vivora.coordenadas[7], vivora.cuerpoSnake3)
		self.tableWidget.setItem(vivora.coordenadas[8], vivora.coordenadas[9], vivora.colaSnake)

	def desaparece(self,vivora):
		self.tableWidget.takeItem(vivora.coordenadas[0], vivora.coordenadas[1])
		self.tableWidget.takeItem(vivora.coordenadas[2], vivora.coordenadas[3])
		self.tableWidget.takeItem(vivora.coordenadas[4], vivora.coordenadas[5])
		self.tableWidget.takeItem(vivora.coordenadas[6], vivora.coordenadas[7])
		self.tableWidget.takeItem(vivora.coordenadas[8], vivora.coordenadas[9]) 

	#Dada la exigencia, crea una lista de colores que va de r,g,b y oscila entre 0 y 255, rango de colores de python
	def colores(self):
		r = random.randint(0,255)
		g = random.randint(0,255)
		b = random.randint(0,255)

		return [r,g,b]

	#Le asigna in id unico a la vivora
	def identificadores(self):
		return str(uuid.uuid4())

	#Tenemos una lista con las coordenadas de la vivora
	def coordenates(self):
		laX=random.randint(0,self.tableWidget.columnCount())
		laY=random.randint(0,self.tableWidget.rowCount())
		corCabeza = [laY,laX]
		corCuerpo1 = [laY,(laX-1) % self.tableWidget.columnCount()]
		corCuerpo2 = [laY,(laX-2) % self.tableWidget.columnCount()]
		corCuerpo3 = [laY, (laX-3) % self.tableWidget.columnCount()]
		corCola = [laY,(laX-4) % self.tableWidget.columnCount()]
		return [corCabeza[0],corCabeza[1],corCuerpo1[0],corCuerpo1[1],corCuerpo2[0],corCuerpo2[1],corCuerpo3[0],corCuerpo3[1],corCola[0],corCola[1]]

#Dado a que las vivoras tienen propiedades como color y id. Se crea una clase que le de a sus objetos, dichos atributos.
class Vivora():
	id = None
	color = []
	coordenadas = []
	direccion = 0
	cabezaSnake = QTableWidgetItem()
	cuerpoSnake1 = QTableWidgetItem()
	cuerpoSnake2 = QTableWidgetItem()
	cuerpoSnake3 = QTableWidgetItem()
	colaSnake = QTableWidgetItem()

	#Se crea una serpiente para añadirla posteriormente al juego
	def __init__(self, id, color, coordenadas, direccion):
		self.id = id
		self.color = [color[0],color[1],color[2]]
		self.coordenadas = coordenadas
		self.direccion = direccion
		self.cabezaSnake.setBackgroundColor(QtGui.QColor(color[0],color[1],color[2]))
		self.cuerpoSnake1.setBackgroundColor(QtGui.QColor(color[0],color[1],color[2]))
		self.cuerpoSnake2.setBackgroundColor(QtGui.QColor(color[0],color[1],color[2]))
		self.cuerpoSnake3.setBackgroundColor(QtGui.QColor(color[0],color[1],color[2]))
		self.colaSnake.setBackgroundColor(QtGui.QColor(color[0],color[1],color[2]))

	def todenuevo(self):
		self.cabezaSnake = QTableWidgetItem()
		self.cuerpoSnake1 = QTableWidgetItem()
		self.cuerpoSnake2 = QTableWidgetItem()
		self.cuerpoSnake3 = QTableWidgetItem()
		self.colaSnake = QTableWidgetItem()
		self.cabezaSnake.setBackgroundColor(QtGui.QColor(self.color[0],self.color[1],self.color[2]))
		self.cuerpoSnake1.setBackgroundColor(QtGui.QColor(self.color[0],self.color[1],self.color[2]))
		self.cuerpoSnake2.setBackgroundColor(QtGui.QColor(self.color[0],self.color[1],self.color[2]))
		self.cuerpoSnake3.setBackgroundColor(QtGui.QColor(self.color[0],self.color[1],self.color[2]))
		self.colaSnake.setBackgroundColor(QtGui.QColor(self.color[0],self.color[1],self.color[2]))

#Inicia la aplicacion.
def main():
	app = QtGui.QApplication(sys.argv)
	win = Servidor()
	win.show()
	app.exec_()
	
main()
