#Adrian Calvo Rojo y Sergio Garcia Prado
#!/usr/bin/python
import gtk

class Casilla(gtk.Button):
	
	#Inicializar cada objeto
	def __init__(self, color, tipo, posicion, vacia):
		super(Casilla, self).__init__()
		#Las fichas negras = 0 y las blancas = 1
		self.color = color
		
		#Las fichas = 0 y las damas = 1
		self.tipo = tipo

		self.posicion = posicion

		self.seleccionado = False

		self.vacia = vacia

		super(Casilla, self).set_size_request(60,60)

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