from Ficha import Ficha

#Variables:

#Tablero predeterminado para la partida.			 
tablero =  [[0, Ficha(0, "A2", 0), 0, Ficha(0, "A4", 0), 0, Ficha(0, "A6", 0), 0, Ficha(0, "A8", 0)],

			[Ficha(0, "B1", 0), 0, Ficha(0, "B3", 0), 0, Ficha(0, "B5", 0), 0, Ficha(0, "B7", 0), 0],

			[0, Ficha(0, "C2", 0), 0, Ficha(0, "C4", 0), 0, Ficha(0, "C6", 0), 0, Ficha(0, "C8", 0)],

			[0,          0,          0,          0,          0,          0,          0,          0],

			[0,          0,          0,          0,          0,          0,          0,          0],

			[Ficha(1, "F1", 0), 0, Ficha(1, "F3", 0), 0, Ficha(1, "F5", 0), 0, Ficha(1, "F7", 0), 0],

			[0, Ficha(1, "G2", 0), 0, Ficha(1, "G4", 0), 0, Ficha(1, "G6", 0), 0, Ficha(1, "G8", 0)],

			[Ficha(1, "H1", 0), 0, Ficha(1, "H3", 0), 0, Ficha(1, "H5", 0), 0, Ficha(1, "H7", 0), 0]]



#Indica si el juego debe continuar o no
seguir = True

#Esta variable indica si se mueven las fichas blancas o las negras (Blancas = True , Negras =False)
turno = "Negras"

#Funciones

#Imprime el tablero en el terminal
def verTablero():
	print "  +-----------------+"
	for y in range(-7, 1):
		linea = ""
		
		#
		y = abs(y)

		#Genera la letra de cada fila
		if y == 7:
			linea += "H "
		elif y == 6:
			linea += "G "
		elif y == 5:
			linea += "F "
		elif y == 4:
			linea += "E "
		elif y == 3:
			linea += "D "
		elif y == 2:
			linea += "C "
		elif y == 1:
			linea += "B "
		else:
			linea += "A "
			
		linea += "| "
		
		#Bucle que recorre el tablero e imprime un guión en el caso de que una casilla esté vacia o la ficha correspondiente.
		for x in range(8):
			if type(tablero[y][x]) == int:
				linea += "- "
			else:
				linea += tablero[y][x].verFicha() + " "
		print linea + "|"

	print "  +-----------------+"
	print "    1 2 3 4 5 6 7 8"

#Comprueba si la entrada del usuario es valida
def entradaPermitida(movimiento):
	
	#Comprueba si la orden está compuesta por 4 caracteres
	longitud = len(movimiento)
	if longitud != 4:
		print "Fallo: Debe introducir 4 caracteres."
		return False


	#Caracter1

	#Convierte el carácter a un número
	caracter1 = ord(movimiento[0]) - 65

	#Comprueba si es una letra mayuscula entre A y H
	if (caracter1 > 7 or caracter1 < 0):
		print "Fallo primer caracter: " + movimiento[0] + " El caracter debe estar entre A y H."
		return False


	#Caracter2

	#Devuelve Falso en caso de que el caracter no sea un entero.
	try:
		caracter2 = int(movimiento[1])-1
	except ValueError:
		print "Fallo segundo caracter: " + movimiento[1] + " El numero debe estar estar entre 1 y 8."
		return False

	#Comprueba si es un número entre 1 y 8
	if caracter2 > 7 or caracter2 < 0:
		print "Fallo segundo caracter: " + movimiento[1] + " El numero debe estar estar entre 1 y 8."
		return False


	#Caracter3

	#Convierte el caracter a un numero
	caracter3 = ord(movimiento[2]) - 65

	#Comprueba si es una letra mayuscula entre A y H
	if (caracter3 > 7 or caracter3 < 0):
		print "Fallo tercer caracter: " + movimiento[2] + " El caracter debe estar entre A y H."
		return False


	#Caracter4

	#Devuelve Falso en caso de que el caracter no sea un entero.
	try:
		caracter4 = int(movimiento[3])-1
	except ValueError:
		print "Fallo cuarto caracter: " + movimiento[3] + " El numero debe estar estar entre 1 y 8."
		return False

	#Comprueba si es un número entre 1 y 8
	if caracter4 > 7 or caracter4 < 0:
		print "Fallo cuarto caracter: " + movimiento[3] + " El numero debe estar estar entre 1 y 8."
		return False

	#Buscamos que el movimiento sea solo en las casillas blancas
	if (abs(caracter3) - caracter4+1) % 2 != 0:
		
		print "Solo se puede mover en las casillas blancas"	
		return False

	if abs(caracter1 - caracter3) != abs(caracter2 - caracter4):

		print "Solo se puede mover en diagonal"
		return False

	if (tablero[caracter1][caracter2].tipo == 0) and calcularDistancia(caracter1, caracter3) != 1:

		print "Los peones solo se pueden mover con distancia 1"
		return False

	if ((tablero [caracter1][caracter2].color == 0) and (turno == "Blancas")) or ((tablero [caracter1][caracter2].color == 1) and (turno == "Negras")): 

		print "No puede mover las fichas del jugador contrario. Tramposo!!"
		return False

	return True

#Devuelve la distancia del movimiento realizado
def calcularDistancia(caracter1, caracter3):
	return abs(caracter1 - caracter3)


def puedeMover(movimiento, caracter1, caracter2, caracter3, caracter4):
	if tablero[caracter3][caracter4] == 0:
		mover(movimiento, caracter1, caracter2, caracter3, caracter4)

	else:
		try:
			if (tablero[caracter3][caracter4].color != tablero[caracter1][caracter2].color):
				
				x,y = direcMovimiento(caracter1, caracter2, caracter3, caracter4)
				
				if (tablero[caracter3+y][caracter4+x] == 0):
					#comerFicha(caracter1, caracter2, caracter3, caracter4)

					comerFicha(movimiento, caracter1, caracter2, caracter3, caracter4)

		except IndexError:
			print "El movimiento no está permitido"

#Devuleve la dirección del movimiento
def direcMovimiento(caracter1, caracter2, caracter3, caracter4):
	x = (caracter4 - caracter2)/calcularDistancia(caracter1, caracter3)
	y = (caracter3 - caracter1)/calcularDistancia(caracter1, caracter3)
	return x,y


def mover(movimiento, caracter1, caracter2, caracter3, caracter4):

	posiNueva = "" + movimiento[2] + movimiento[3]

	#Pasamos la antigua ficha a la nueva posicion
	tablero[caracter3][caracter4] = tablero[caracter1][caracter2]
	#Damos al atributo posicion de la ficha la nueva posicion
	tablero[caracter3][caracter4].posicion = posiNueva
	#Borramos la ficha de la antigua posicion
	tablero[caracter1][caracter2] = 0

	promociona(caracter3, caracter4)


def comerFicha(movimiento, caracter1, caracter2, caracter3, caracter4):
	
	x,y = direcMovimiento(caracter1, caracter2, caracter3, caracter4)
	

	#posiNueva = "" + movimiento[2] + movimiento[3]


	#Pasamos la antigua ficha a la nueva posicion
	tablero[caracter3+y][caracter4+x] = tablero[caracter1][caracter2]

	#Borramos la posicion antigua y la de la ficha que se ha comido
	tablero[caracter3][caracter4] = 0
	tablero[caracter1][caracter2] = 0

	promociona(caracter3+y, caracter4+x)

	#Damos al atributo posicion de la ficha la nueva posicion
	#tablero[caracter3+y][caracter4+x].posicion = posiNueva
	
	

#def comerEnCadena():


def promociona(caracter3, caracter4):
	if ((tablero[caracter3][caracter4].color == 0) and caracter3 ==7) or ((tablero[caracter3][caracter4].color == 1) and caracter3 ==0):
		tablero[caracter3][caracter4].tipo = 1


#Programa

#Controla la continuidad de la aplicacion.
while seguir == True:

	verTablero()

	if turno == "Negras":
		turno = "Blancas"

	else:
		turno = "Negras"
	
	print "Turno de las " + turno

	#Pregunta al usuario por el movimiento a realizar y convierte todos los caracteres a letras mayusculas, en el caso de que el usuario las haya introducido en minúsculas
	movimiento = str(raw_input("Indique el movimiento: ")).upper()


	#Si el movimiento que se pretende realizar no es válido se salta el resto del flujo del programa y se termina.
	if entradaPermitida(movimiento) == True:

		caracter1 = ord(movimiento[0]) - 65
		caracter2 = int(movimiento[1]) - 1
		caracter3 = ord(movimiento[2]) - 65
		caracter4 = int(movimiento[3]) - 1

		puedeMover(movimiento, caracter1, caracter2, caracter3, caracter4)

		


	else:
		seguir = False




print "El juego ha terminado"



