from Ficha import Casilla
import os
import copy

#Variables:

#Tablero predeterminado para la partida.		
"""tablero =  [[0, Ficha(0, "A2", 0), 0, Ficha(0, "A4", 0), 0, Ficha(0, "A6", 0), 0, Ficha(0, "A8", 0)],

			[Ficha(0, "B1", 0), 0, Ficha(0, "B3", 0), 0, Ficha(0, "B5", 0), 0, Ficha(0, "B7", 0), 0],

			[0, Ficha(0, "C2", 0), 0, Ficha(0, "C4", 0), 0, Ficha(0, "C6", 0), 0, Ficha(0, "C8", 0)],

			[0,          0,          0,          0,          0,          0,          0,          0],

			[0,          0,          0,          0,          0,          0,          0,          0],

			[Ficha(1, "F1", 0), 0, Ficha(1, "F3", 0), 0, Ficha(1, "F5", 0), 0, Ficha(1, "F7", 0), 0],

			[0, Ficha(1, "G2", 0), 0, Ficha(1, "G4", 0), 0, Ficha(1, "G6", 0), 0, Ficha(1, "G8", 0)],

			[Ficha(1, "H1", 0), 0, Ficha(1, "H3", 0), 0, Ficha(1, "H5", 0), 0, Ficha(1, "H7", 0), 0]]"""
tablero = [[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]
#Disponer las casillas vacias y con fichas en el tablero
for y in range(8):
	for x in range(8):
		if (y == 0 or y == 1 or y == 2) and ((y-x)%2 != 0):
			tablero[y][x] = Casilla(0,0, chr(65+y)+str(x+1),False)
		elif (y == 5 or y == 6 or y == 7) and ((y-x)%2 != 0):				
			tablero[y][x] = Casilla(1,0, chr(65+y)+str(x+1),False)
		else:
			tablero[y][x] = Casilla(0,0, chr(65+x)+str(x+1),True)
		#Dar los eventos a cada casilla
		#tablero[a][b].connect("clicked", selecionarMovi, tablero[a][b].posicion)
		#tablero[a][b].connect("enter", hover, tablero[a][b].posicion)


#Indica si el juego debe continuar o no
seguir = True

#Esta variable indica si se mueven las fichas blancas o las negras (Blancas = True , Negras =False) turnoColor hace lo mismo, solo que con 0 y 1 respectivamente
turno = "Negras"
turnoColor = 0


#Funciones

#Imprime el tablero en el terminal
def verTablero():	
	
	"""#Sirve para limpiar el terminal en cada pasada, y que así se vea más limpio el tablero.
	if (os.name == "nt"):
		os.system("cls")
	else:
		os.system("clear")"""
		
	print
	print "  Damas - Adrian Calvo Rojo & Sergio Garcia Prado \n"

	print "	Fichas blancas: " + str(numFichas(0)) + "	Fichas negras: " + str(numFichas(1)) + "\n"

	print "		    1 2 3 4 5 6 7 8"
	print "		  +-----------------+"
	for y in range(-7, 1):
		linea = ""
		
		#Valor absoluto para hacer una cuenta atras desde 7 a 0
		y = abs(y)

		#Genera la letra de cada fila
		linea += "		 " + chr(y+65)	
		linea += "| "
		
		#Bucle que recorre el tablero e imprime un guión en el caso de que una casilla esté vacia o la ficha correspondiente.
		for x in range(8):
			if tablero[y][x].vacia == True:
				linea += "- "
			else:
				linea += tablero[y][x].verFicha() + " "
		linea += "|"
		linea += chr(y+65)
		print linea

	print "		  +-----------------+"
	print "		    1 2 3 4 5 6 7 8 \n" 


#Comprueba si la entrada del usuario es valida
def entradaPermitida(movimiento):

	c1 = ord(movimiento[0]) - 65
	c2 = int(movimiento[1]) - 1
	c3 = ord(movimiento[2]) - 65
	c4 = int(movimiento[3]) - 1
	
	#Comprueba si la orden está compuesta por 4 caracteres
	longitud = len(movimiento)
	if longitud != 4:
		print "  Fallo: Debe introducir 4 caracteres. \n"
		return False

	#Buscamos que el movimiento sea solo en las casillas blancas
	if (abs(c3) - c4+1) % 2 != 0:
		
		print "  Solo se puede mover en las casillas blancas. \n"	
		return False

	#Comprobamos si el movimiento es solo en diagonal
	if abs(c1 - c3) != abs(c2 - c4):

		print "  Solo se puede mover en diagonal. \n"
		return False

	
	#Comprueba que el movimiento de los peones solo es de una unidad
	if (tablero[c1][c2].tipo == 0) and calcularDistancia(c1, c3) != 1:

		print "  Los peones solo se pueden mover con distancia 1. \n"
		return False

	#Comprueba que no se haya movido la ficha del jugador rival
	if ((tablero [c1][c2].color == 0) and (turno == "Blancas")) or ((tablero [c1][c2].color == 1) and (turno == "Negras")): 

		print "  No puede mover las fichas del jugador contrario. Tramposo!! \n"
		return False

	#Comprueba que la ficha que se quiere comer no sea del mismo color que la que come.
	if (tablero[c3][c4].vacia == False) and (tablero[c1][c2].color == tablero[c3][c4].color):
		print "  No se pueden comer fichas propias. \n"
		return False
	
	#Calculamos la distancia y la direccion de las coordenadas (x, y)
	distancia = calcularDistancia(c1, c3)
	x,y = direcMovimiento(c1, c2, c3, c4)

	#Comprueba que las reinas no salten ningún peón
	if (tablero[c1][c2].tipo == 1) and (distancia != 1):

		i = 1
		while (i != distancia):
		
			lado = i * x
			arriba = i * y			
			i += 1
			
			if tablero[c1 + lado][c2 + arriba].vacia == False:
				print "  Las reinas no pueden saltar peones. \n"
				return False

	#En caso de que no se cumpla ningun caso anterior, quiere decir que la entrada del usuario ha sido correcta, por lo que devuelve verdadero
	return True


#Devuelve la distancia del movimiento realizado
def calcularDistancia(c1, c3):
	return abs(c1 - c3)

#Función que indica si el movimiento es comiendo o sin comer una ficha
def puedeMover(c1, c2, c3, c4):

	global seguir
	
	#si la posición a la que se mueve está vacia llama a mover, sino llama a comerficha
	if tablero[c3][c4].vacia == True:
		mover(c1, c2, c3, c4)

	else:

		#comprueba que las fichas son de distinto color
		if (tablero[c3][c4].color != tablero[c1][c2].color):
			
			x,y = direcMovimiento(c1, c2, c3, c4)
			
			#llama a comerficha si la posicion siguiente esta vacia si salta un error es porque la ficha se colocaría fuera del tablero, en cuyo caso se captura
			try:
				if (c4 != 0) and (tablero[c3 + x][c4 + y].vacia == True):
				
					comerFicha(c1, c2, c3, c4)
					comerEnCadena(c3 + x,c4 + y)
			
				else:
					print "Movimiento no valido. Ficha fuera de tablero o casilla ocupada"
					seguir = False
			except IndexError:
					print "Movimiento no valido. Ficha fuera de tablero"
					seguir = False
	
#Devuelve la dirección del movimiento en dos variables separadas, la "x" son el eje vertical y la "y" el horizontal
def direcMovimiento(c1, c2, c3, c4):

	x = (c3 - c1)/calcularDistancia(c1, c3)
	y = (c4 - c2)/calcularDistancia(c1, c3)

	return x,y


#función que mueve la ficha
def mover(c1, c2, c3, c4):

	#Pasamos la antigua ficha a la nueva posicion
	tablero[c3][c4].color = tablero[c1][c2].color

	tablero[c3][c4].tipo = tablero[c1][c2].tipo
	
	#Borramos la ficha de la antigua posicion y la agregamos en la nueva
	tablero[c1][c2].vacia = True
	tablero[c3][c4].vacia = False

	

	promociona(c3, c4)

	#ficheroMovs.write(str(chr(c1+65)) + str(c2+1) + str(chr(c3+65)) + str(c4+1) +"\n")


#función que mueve la ficha a la posición siguiente de la indicada y elimina la ficha de la posición marcada, es decir, la come-
def comerFicha(c1, c2, c3, c4):
	
	x,y = direcMovimiento(c1, c2, c3, c4)
	

	#Pasamos la antigua ficha a la nueva posicion
	tablero[c3+x][c4+y].color = tablero[c1][c2].color

	tablero[c3+x][c4+y].tipo = tablero[c1][c2].tipo

	#Borramos la posicion antigua y la de la ficha que se ha comido y agregamos la nueva
	tablero[c1][c2].vacia = True
	tablero[c3][c4].vacia = True
	

	tablero[c3+x][c4+y].vacia = False


	promociona(c3 + x, c4 + y)
	
	#ficheroMovs.write(str(chr(c1+65)) + str(c2+1) + str(chr(c3+65)) + str(c4+1) +"\n")

	
#función que es llamada después de comer una ficha, come el mayor número de fichas posibles automáticamente
def comerEnCadena(c3,c4):

	#posibles es una lista que almacena todas las posibles combinaciones de movimientos que se pueden dar. Para calcular los posibles movimientos se llama a calcularPosibles
	posibles = []
	posibles = calcularPosibles(c3,c4)

	#En el caso de que haya algúna combinación de movimientos, se  elige el  más largo de todos y se guarda en posibles.
	if len(posibles) > 0:
	
		a = len(posibles[0])
		movimientos = posibles[0]
		
		for i in posibles:
			b = len(i)
			
			if (a <= b):
				movimientos = i
				a = b
				
		#Se inicializan caracter 1 y 2 con los valores de caracter 3 y 4 respectivamente.
		distancia = len(movimientos)
		c1=c3
		c2=c4

		#se recorre la lista que guarda la combinación movimientos mientras se va llamando a comerFicha cada vez, caracter 3 y 4 son los valores de la lista, mientras que caracter 1 y 2 son la casilla siguiente a estos en el ciclo anterior.
		for recorrido in range(distancia):	

			c3 = int(movimientos[recorrido][0])
			c4 = int(movimientos[recorrido][1])
			
			comerFicha(c1,c2,c3,c4)

			x,y = direcMovimiento(c1, c2, c3, c4)
			c1 = c3 + x
			c2 = c4 + y


#Función que convierte en reina a una ficha cuando llega a la primera linea del color contrario.
def promociona(c3, c4):
	if ((tablero[c3][c4].color == 0) and c3 == 7) or ((tablero[c3][c4].color == 1) and c3 == 0):
	
		tablero[c3][c4].tipo = 1

#Función que devuelve la lista de los posibles movimientos que puede hacer la ficha.
def calcularPosibles(c3,c4):
	#Creamos posibles y posibles copia, "posibles" será donde se almacenarán los posibles movimientos, "posiblesCopia" sirve para que si no ha cambiado nada en la siguiente iteración termine de buscar posibilidades, ya que no hay más.
	posibles = []
	posiblesCopia = []
	
	#Es el primer valor, y desde donde se empezarán a analizar las posibles opciones.
	original = str(c3) + str(c4)
	posibles.append([original])
	#tableroPosibles = tablero[:]
	tableroPosibles = [[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]

	for y in range(8):
		for x in range(8):
				tableroPosibles[y][x] = Casilla(0,0, chr(65+y)+str(x+1),False)

				tableroPosibles[y][x].color = tablero[y][x].color

				tableroPosibles[y][x].tipo = tablero[y][x].tipo

				tableroPosibles[y][x].vacia = tablero[y][x].vacia
			

	tableroPosibles[c3][c4].vacia = True
	
	#Comprueba que "posibles" no sea igual que en la anterior pasaad
	while (posibles != posiblesCopia):
		posiblesCopia = posibles[:]

		#Recorre las cuatro direcciones
		for x in range (1,-2,-2):
			for y in range(1,-2,-2):

				#Recorre cada una de las posibilidades (listas dentro de posibles)
				for i in posibles:

					#Copia la iteracion en lista, y extrae el último valor en "lista1" y "lista2" y si estos son mayores que 0 sigue con el flujo del programa.
					lista = i[:]
					valor = lista.pop()
					valor1 = int(valor[0])
					valor2 = int(valor[1])

					#Recorre todos los movimientos
					for r in i:

						#Si encuentra que una ficha es o se ha transformado en reina, recorre la diagonal, sino solo mira la posicion siguiente.
						if (turnoColor == 1 and  r[0] == "1") or (turnoColor == 0 and r[0] == "6") or (tablero[c3][c4].tipo == 1):
						
							for j in range(5):
								superX = x * j
								superY = y * j

								#Si encuentra una ficha del mismo color que el de la que está comiendo, deja de comprobar en esa direccion.
								try: 
									if tableroPosibles[valor1+x+superX][valor2+y+superY].vacia == False and tablero[c3][c4].color == tableroPosibles[valor1+x+superX][valor2+y+superY].color:
										break
								except IndexError:
										break

								addPosibles(valor1,valor2, x,y, lista,posibles, superX, superY, tableroPosibles)

						else:	
							addPosibles(valor1,valor2, x,y, lista,posibles, 0, 0, tableroPosibles)

						
	#Elimina el oltimo valor de cada una de las listas de movimientos dentro de posibles, ya que este es "sig", es decir, la próxima casilla a analizar(que en este caso no hay)						
	for sigDelete in posibles:
		sigDelete.pop()

	return posibles


def addPosibles(valor1,valor2, x,y, lista,posibles, superX, superY,tableroPosibles):
	if (valor1 >= 0) and (valor2 >= 0):

		#Captura el caso de comprobar una casilla fuera del rango de la lista
		try:
			#En el caso de que cumpla las condicciones para que la posición pueda ser comida también comprueba 
			if (tableroPosibles[valor1+x+superX][valor2+y+superY].vacia == False) and (tableroPosibles[valor1+(2*x+superX)][valor2+(2*y+superY)].vacia == True) and (tableroPosibles[valor1+x+superX][valor2+y+superY].color != turnoColor):
				
				if (valor1+2*x+superX >= 0) and (valor2+2*y+superY >= 0):

					#"movi" es el valor que se usará para comer la ficha mientras que "sig" es la casilla siguiente que se comprobará(después de usarse queda eliminado de la lista)
					movi = str(valor1+x+superX)+ str (valor2+y+superY)
					sig = str(valor1+(2*x+superX))+ str (valor2+(2*y+superY))
				

					#si "movi" no pertenece a la lista de movimientos, se añaden
					if (perteneceALista(movi, lista) == False):
						lista.append(movi)
						lista.append(sig)

						#Si ya hay una lista con los mismos valores dentro de posibles, esta se descarta, sino, se añade.
						if (perteneceALista(lista, posibles) == False):
							posibles.append(lista)
							
		except IndexError:
			pass

	return posibles


#Función booleana, si el primer parametro pertenece al segundo parámetro.
def perteneceALista(movi, posibles):
	try:
		posibles.index(movi)
		return True
		
	except ValueError:
		return False

#Función que devuelve las fichas que quedan del color que se indica.
def numFichas(turnoColor):
	fichas = 0 

	#Recorre la lista y va incrementando "fichas" por cada ficha del jugador contrario que se encuentra
	for x in range(8):
		for y in range (8):
			if tablero[x][y] != 0:
				if turnoColor != tablero[x][y].color:
					fichas = fichas + 1

	return fichas


#Carga un fichero con movimientos desde un archivo de texto con el nombre introducido por el usuario
fichero = str(raw_input("  Indique el fichero desde el que se carga la partida: ")) + ".txt"
try:
	fich = open("partidas/" + fichero, "r")
except IOError:

	print
	print "  No existe un fichero con ese nombre."
	print

	fich = ""


#Crea un archivo con los movimientos de la partida, en el caso de que no se introduzca nombre se crea como default
ficheroMovsNombre = str(raw_input("  Indique el fichero donde se guarda la partida: ")) + ".txt"

if ficheroMovsNombre != "":
	ficheroMovs = open("partidas/default.txt", "w")
else:
	ficheroMovs = open("partidas/" + ficheroMovsNombre, "w")



#Programa
jugadas =[]
#Controla la continuidad de la aplicacion.
while seguir == True:

	jugadas.append(tablero)

	verTablero()
	
	

	#Conmuta el turno de cada color, y muestra en pantalla a quien le toca
	if turno == "Negras":
		turno = "Blancas"
		turnoColor = 1
	else:
		turno = "Negras"
		turnoColor = 0
	print "  Turno de las " + turno

	print

	#Lee la siguiente linea del fichero, en el caso de que este vacia o no se haya introducido fichero, pide por teclado el movimiento
	if fich != "":
		cad = fich.readline(4)
		fich.readline()
		if cad != "":
			movimiento = cad
		else:
			movimiento = str(raw_input("  Indique el movimiento: ")).upper()

	else:
		movimiento = str(raw_input("  Indique el movimiento: ")).upper()

	
	ficheroMovs.write(movimiento +"\n")

	#Si el movimiento que se pretende realizar no es válido se salta el resto del flujo del programa y se termina.
	if entradaPermitida(movimiento) == True:

		#Divide el movimiento en las componentes de las coordenadas origen y destino
		c1 = ord(movimiento[0]) - 65
		c2 = int(movimiento[1]) - 1
		c3 = ord(movimiento[2]) - 65
		c4 = int(movimiento[3]) - 1

		#es quien elige el tipo de movimiento(mover o comer)
		puedeMover(c1, c2, c3, c4)

		#Comprueba si el juego a terminado o no.
		if numFichas(turnoColor) == 0:
		
			seguir = False
			verTablero()
			print "  Enhorabuena! Las " + turno + " ganan la partida, el jugador contrario se ha quedado sin fichas. \n"

	else:
		seguir = False

	"""if deshacer == True:
		if jugadas >0:
			tablero = jugadas.pop()
		else:
			print "No se puede deshacer mas veces"
	"""

print "  El juego ha terminado \n"
ficheroMovs.close()