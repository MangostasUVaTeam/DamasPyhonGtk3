
#Adrian Calvo Rojo y Sergio Garcia Prado
#!/usr/bin/python
from gi.repository import Gtk

class Casilla(Gtk.Button):
	
	#Inicializar cada objeto
	def __init__(self, color, tipo, posicion, vacia):

		super(Casilla, self).__init__()
		super(Casilla, self).set_size_request(75,75)
		
		#Las fichas negras = 0 y las blancas = 1
		self.color = color
		
		#Las fichas = 0 y las damas = 1
		self.tipo = tipo

		self.posicion = posicion

		self.seleccionado = False

		self.vacia = vacia

		if vacia:
			super(Casilla, self).set_name('Vacia')
		else:
			if color  == 0:
				if tipo == 0:
					super(Casilla, self).set_name('FichaNegra')
				else:
					super(Casilla, self).set_name('FichaNegraDama')
			if color  == 1:
				if tipo == 0:
					super(Casilla, self).set_name('FichaBlanca')
				else:
					super(Casilla, self).set_name('FichaBlancaDama')

	def setVacia(self):
		self.set_name('Vacia')
		self.vacia = True

	def mov(self, Casilla):

		Casilla.color = self.color
		Casilla.tipo = self.tipo
		Casilla.set_name(self.get_name())
		self.setVacia()
		Casilla.vacia = False
		Casilla.posicion = self.posicion
		Casilla.reset()


	def reset(self):
		self.seleccionado = False
		if not self.vacia:
			if self.color  == 0:
				if self.tipo == 0:
					self.set_name('FichaNegra')
				else:
					self.set_name('FichaNegraDama')
			if self.color  == 1:
				if self.tipo == 0:
					self.set_name('FichaBlanca')
				else:
					self.set_name('FichaBlancaDama')
		else:
			self.set_name('Vacia')

	def ver(self):

		if self.vacia:
			ver = "Vacia"
		else:
			ver = self.posicion
			if self.color == 1:
				ver += ", Blanca"
			else:
				ver += ", Negra"

		print ver