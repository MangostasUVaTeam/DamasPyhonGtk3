from Ficha import Ficha
import os

#Variables:

#Tablero predeterminado para la partida.		

"""tablero =  [[0, Ficha(0, "A2", 0), 0, 			0, 0, Ficha(0, "A6", 0), 0, 					0],

			[Ficha(0, "B1", 0), 0, Ficha(0, "B3", 0), 0, 		0, 0, Ficha(0, "B7", 0), 0],

			[0, 0, 0, Ficha(0, "C4", 0), 0, 0, 0, Ficha(0, "C8", 0)],

			[0,          0,         Ficha(0, "B5", 0),0,Ficha(0, "B5", 0),0,  Ficha(0, "B5", 0),  0],

			[0,          0,          0,          0,          0,          0,          0,          0],

			[Ficha(1, "F1", 0), 0, Ficha(1, "F3", 0), 0, Ficha(0, "F5", 0), 0, Ficha(0, "F7", 0), 0],

			[0, Ficha(1, "G2", 0), 0, Ficha(1, "G4", 0), 0, Ficha(1, "G6", 0), 0, Ficha(1, "G8", 0)],

			[Ficha(1, "H1", 0), 0, Ficha(1, "H3", 0), 0, Ficha(1, "H5", 0), 0, Ficha(1, "H7", 0), 0]]"""

"""tablero =  [[0,          0,          0,          0,          0,          0,          0,          0],

			[0, 0, Ficha(0, "B3", 0), 0, 		0, 0, 0, 0],

			[0, 0, 0,0, 0, 0, 0, 0],

			[0,          0,          0,          0,          Ficha(1, "C4", 0),          0,          0,          0],

			[0,          0,          0,          0,          0,          0,          0,          0],

			[0,          0,          0,          0,          0,          0,          0,          0],

			[0,          0,          0,          0,          0,          0,          0,          0],

			[0,          0,          0,          0,          0,          0,          0,          0]]"""

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

#Esta variable indica si se mueven las fichas blancas o las negras (Blancas = True , Negras =False) turnoColor hace lo mismo, solo que con 0 y 1 respectivamente
turno = "Negras"
turnoColor = 0


#Funciones

#Imprime el tablero en el terminal
def verTablero():
	print "  +-----------------+"
	for y in range(-7, 1):
		linea = ""
		
		#Valor absoluto para hacer una cuenta atras desde 7 a 0
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

	#Comprobamos si el movimiento es solo en diagonal
	if abs(caracter1 - caracter3) != abs(caracter2 - caracter4):

		print "Solo se puede mover en diagonal"
		return False

	#Try-except que captura el caso de que la casilla no tenga ficha
	try:
		#Comprueba que el movimiento de los peones solo es de una unidad
		if (tablero[caracter1][caracter2].tipo == 0) and calcularDistancia(caracter1, caracter3) != 1:

			print "Los peones solo se pueden mover con distancia 1"
			return False

		#Comprueba que no se haya movido la ficha del jugador rival
		if ((tablero [caracter1][caracter2].color == 0) and (turno == "Blancas")) or ((tablero [caracter1][caracter2].color == 1) and (turno == "Negras")): 

			print "No puede mover las fichas del jugador contrario. Tramposo!!"
			return False

		#Comprueba que la ficha que se quiere comer no sea del mismo color que la que come.
		if (tablero[caracter3][caracter4] != 0) and (tablero[caracter1][caracter2].color == tablero[caracter3][caracter4].color):
			print "No se pueden comer fichas propias"
			return False
		
		#Calculamos la distancia y la direccion de las coordenadas (x, y)
		distancia = calcularDistancia(caracter1, caracter3)
		x,y = direcMovimiento(caracter1, caracter2, caracter3, caracter4)

		#Comprueba que las reinas no salten ningún peón
		if (tablero[caracter1][caracter2].tipo == 1) and (distancia != 1):

			i = 1
			while (i != distancia):
			
				lado = i * x
				arriba = i * y			
				i += 1
				
				if tablero[caracter1 + lado][caracter2 + arriba] != 0:
					print "Las reinas no pueden saltar peones."
					return False
	except AttributeError:
		print "La casilla está vacía"
		return False

	#En caso de que no se cumpla ningun caso anterior, quiere decir que la entrada del usuario ha sido correcta, por lo que devuelve verdadero
	return True


#Devuelve la distancia del movimiento realizado
def calcularDistancia(caracter1, caracter3):
	return abs(caracter1 - caracter3)


#Función que indica si el movimiento es comiendo o sin comer una ficha
def puedeMover(caracter1, caracter2, caracter3, caracter4):

	global seguir
	
	#si la posición a la que se mueve está vacia llama a mover, sino llama a comerficha
	if tablero[caracter3][caracter4] == 0:
		mover(caracter1, caracter2, caracter3, caracter4)

	else:

		#comprueba que las fichas son de distinto color
		if (tablero[caracter3][caracter4].color != tablero[caracter1][caracter2].color):
			
			x,y = direcMovimiento(caracter1, caracter2, caracter3, caracter4)
			
			#llama a comerficha si la posicion siguiente esta vacia si salta un error es porque la ficha se colocaría fuera del tablero, en cuyo caso se captura
			try:
				if (caracter4 != 0) and (tablero[caracter3 + x][caracter4 + y] == 0):
				
					comerFicha(caracter1, caracter2, caracter3, caracter4)
					comerEnCadena(caracter3+x,caracter4+y)
			
				else:
					print "Movimiento no valido. Ficha fuera de tablero o casilla ocupada"
					seguir = False
			except IndexError:
					print "Movimiento no valido. Ficha fuera de tablero"
					seguir = False

		
#Devuelve la dirección del movimiento en dos variables separadas, la "x" son el eje vertical y la "y" el horizontal
def direcMovimiento(caracter1, caracter2, caracter3, caracter4):

	x = (caracter3 - caracter1)/calcularDistancia(caracter1, caracter3)
	y = (caracter4 - caracter2)/calcularDistancia(caracter1, caracter3)

	return x,y


#función que mueve la ficha
def mover(caracter1, caracter2, caracter3, caracter4):

	#Pasamos la antigua ficha a la nueva posicion
	tablero[caracter3][caracter4] = tablero[caracter1][caracter2]
	
	#Borramos la ficha de la antigua posicion
	tablero[caracter1][caracter2] = 0

	#posiNueva es el nombre de la posición en la que se colocará la ficha.
	posiNueva = str(caracter3+65) + str(caracter4+1)
	#Damos al atributo posicion de la ficha la nueva posicion
	tablero[caracter3][caracter4].posicion = posiNueva

	promociona(caracter3, caracter4)


#función que mueve la ficha a la posición siguiente de la indicada y elimina la ficha de la posición marcada, es decir, la come-
def comerFicha(caracter1, caracter2, caracter3, caracter4):
	
	x,y = direcMovimiento(caracter1, caracter2, caracter3, caracter4)
	
	#Pasamos la antigua ficha a la nueva posicion
	tablero[caracter3 + x][caracter4 + y] = tablero[caracter1][caracter2]

	#Borramos la posicion antigua y la de la ficha que se ha comido
	tablero[caracter3][caracter4] = 0
	tablero[caracter1][caracter2] = 0

	#posiNueva es el nombre de la posición en la que se colocará la ficha.
	posiNueva = str(caracter3+x+65) + str(caracter4+y+1)
	#Damos al atributo posicion de la ficha la nueva posicion
	tablero[caracter3+x][caracter4+y].posicion = posiNueva

	promociona(caracter3 + x, caracter4 + y)
	
	
#función que es llamada después de comer una ficha, come el mayor número de fichas posibles automáticamente
def comerEnCadena(caracter3,caracter4):
	
	#posibles es una lista que almacena todas las posibles combinaciones de movimientos que se pueden dar. Para calcular los posibles movimientos se llama a calcularPosibles
	posibles=[]
	posibles = calcularPosibles(caracter3,caracter4)
	
	"""posibles.append(["47","36","16"])
	posibles.append(["47","36","34","32","12"])
	posibles.append(["47","36","34","54"])"""

	#En el caso de que haya algúna combinación de movimientos, se  elige el  más largo de todos y se guarda en posibles.
	if (len(posibles)>0):
		a = len(posibles[0])
		movimientos = posibles[0]
		for i in posibles:
			b = len(i)
			if (a<=b):
				movimientos = i
				a = b

		#Se inicializan caracter 1 y 2 con los valores de caracter 3 y 4 respectivamente.
		distancia = len(movimientos)
		caracter1=caracter3
		caracter2=caracter4

		#se recorre la lista que guarda la combinación movimientos mientras se va llamando a comerFicha cada vez, caracter 3 y 4 son los valores de la lista, mientras que caracter 1 y 2 son la casilla siguiente a estos en el ciclo anterior.
		for recorrido in range(distancia):	

			caracter3=int(movimientos[recorrido][0])
			caracter4=int(movimientos[recorrido][1])
			
			comerFicha(caracter1,caracter2,caracter3,caracter4)

			x,y = direcMovimiento(caracter1, caracter2, caracter3, caracter4)
			caracter1 = caracter3+x
			caracter2 = caracter4+y


#Función que convierte en reina a una ficha cuando llega a la primera linea del color contrario.
def promociona(caracter3, caracter4):
	if ((tablero[caracter3][caracter4].color == 0) and caracter3 ==7) or ((tablero[caracter3][caracter4].color == 1) and caracter3 ==0):
		tablero[caracter3][caracter4].tipo = 1


#Función que devuelve la lista de los posibles movimientos que puede hacer la ficha.
def calcularPosibles(caracter3,caracter4):
	#Creamos posibles y posibles copia, "posibles" será donde se almacenarán los posibles movimientos, "posiblesCopia" sirve para que si no ha cambiado nada en la siguiente iteración termine de buscar posibilidades, ya que no hay más.
	posibles=[]
	posiblesCopia=[]
	
	#Es el primer valor, y desde donde se empezarán a analizar las posibles opciones.
	original= str(caracter3)+str(caracter4)
	posibles.append([original])
	
	#Comprueba que "posibles" no sea igual que en la anterior pasaad
	while (posibles != posiblesCopia):
		posiblesCopia = posibles[:]

		#Recorre las cuatro direcciones
		for x in range (1,-2,-2):
			for y in range(1,-2,-2):

				#Recorre cada una de las posibilidades (listas dentro de posibles)
				for i in posibles:

					#Copia la iteración en lista, y extrae el último valor en "lista1" y "lista2" y si estos son mayores que 0 sigue con el flujo del programa.
					lista = i[:]
					valor = lista.pop()
					valor1 = int(valor[0])
					valor2 = int(valor[1])
					if (valor1>=0) and (valor2 >=0):

						#Captura el caso de comprobar una casilla fuera del rango de la lista
						try:
							#En el caso de que cumpla las condicciones para que la posición pueda ser comida también comprueba 
							if (tablero[valor1+x][valor2+y] != 0) and (tablero[valor1+(2*x)][valor2+(2*y)] == 0) and (tablero[valor1+x][valor2+y].color != turnoColor):
								
								if (valor1+2*x >= 0) and (valor2+2*y >= 0):

									#"movi" es el valor que se usará para comer la ficha mientras que "sig" es la casilla siguiente que se comprobará(después de usarse queda eliminado de la lista)
									movi = str(valor1+x)+ str (valor2+y)
									sig = str(valor1+(2*x))+ str (valor2+(2*y))

									#si "movi" no pertenece a la lista de movimientos, se añaden
									if (perteneceALista(movi,lista)==False):
										lista.append(movi)
										lista.append(sig)

										#Si ya hay una lista con los mismos valores dentro de posibles, esta se descarta, sino, se añade.
										if (perteneceALista(lista, posibles)==False):
											posibles.append(lista)
									
						except IndexError:
							x=x
						
	#Elimina el último valor de cada una de las listas de movimientos dentro de posibles, ya que este es "sig", es decir, la próxima casilla a analizar(que en este caso no hay)						
	for sigDelete in posibles:
		sigDelete.pop()

	return posibles


#Función booleana, si el primer parametro pertenece al segundo parámetro.
def perteneceALista(movi,posibles):
	try:
		posibles.index(movi)
		return True
	except ValueError:
		return False


#Función que booleana para comprobar si se el jugador contrario se ha quedado sin fichas.
def sinFichas(tablero, turnoColor):
	fichas = 0 

	#Recorre la lista y va incrementando "fichas" por cada ficha del jugador contrario que se encuentra
	for y in range(8):
		for x in range (8):
			if tablero[y][x] != 0:
				if turnoColor != tablero[y][x].color:
					fichas = fichas + 1

	#Si no ha encontrado ninguna devuelve verdadero, sino, devuelve falso
	if fichas == 0:
		return True
	else:
		return False


#Programa

#Controla la continuidad de la aplicacion.
while seguir == True:

	#Sirve para limpiar el terminal en cada pasada, y que así se vea más limpio el tablero.
	"""if (os.name == "nt"):
		os.system("cls")
	else:
		os.system("clear")"""

	verTablero()

	#Conmuta el turno de cada color, y muestra en pantalla a quien le toca
	if turno == "Negras":
		turno = "Blancas"
		turnoColor = 1 
	else:
		turno = "Negras"
		turnoColor = 0
	print "Turno de las " + turno

	#Pregunta al usuario por el movimiento a realizar y convierte todos los caracteres a letras mayusculas, en el caso de que el usuario las haya introducido en minúsculas
	movimiento = str(raw_input("Indique el movimiento: ")).upper()

	#Si el movimiento que se pretende realizar no es válido se salta el resto del flujo del programa y se termina.
	if entradaPermitida(movimiento) == True:

		#Divide el movimiento en las componentes de las coordenadas origen y destino
		caracter1 = ord(movimiento[0]) - 65
		caracter2 = int(movimiento[1]) - 1
		caracter3 = ord(movimiento[2]) - 65
		caracter4 = int(movimiento[3]) - 1

		#es quien elige el tipo de movimiento(mover o comer)
		puedeMover(caracter1, caracter2, caracter3, caracter4)

		#Comprueba si el juego a terminado o no.
		if sinFichas(tablero, turnoColor) == True:
			seguir = False
			verTablero()
			print "Enhorabuena! Las " + turno + " ganan la partida, el jugador contrario se ha quedado sin fichas."

	else:
		seguir = False

print "El juego ha terminado"