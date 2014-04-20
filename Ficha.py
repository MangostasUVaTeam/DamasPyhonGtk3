class Ficha:
	""" Clase Ficha de la que se van a crear objetos """
	""" Cada objeto Ficha representa un peon o dama del tablero colocados en una posicion del mismo."""
	
	#Inicializar cada objeto
	def __init__(self, color, posicion, tipo):

		#Las fichas negras = 0 y las blancas = 1
		self.color = color

		self.posicion = posicion
		
		#Las fichas = 0 y las damas = 1
		self.tipo = tipo


	#Funcion que devuelve las fichas para ser impresas
	def verFicha(self):

		if self.color == 0:
			if self.tipo == 0:
				return "*"
			else:
				return "X"
		else:
			if self.tipo == 0:
				return "o"
			else:
				return "8"