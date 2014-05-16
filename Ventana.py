#!/usr/bin/python
from gi.repository import Gtk, Gdk
from Ficha import Casilla

mueveme = ""

#Indica si el juego debe continuar o no
seguir = True

#Esta variable indica si se mueven las fichas blancas o las negras (Blancas = True , Negras =False) turnoColor hace lo mismo, solo que con 0 y 1 respectivamente
turno = "Blancas"
turnoColor = 0

def selecionarMovi(casilla, posicion):

	global mueveme, turno, turnoColor

	if casilla.color == 0 and not casilla.vacia:
		casilla.set_name("FichaNegraSel")
		casilla.seleccionado = True
	if casilla.color == 1 and not casilla.vacia:
		casilla.set_name("FichaBlancaSel")
		casilla.seleccionado = True

	mueveme += posicion
	if len(mueveme) == 4:
		print mueveme
		
		movimiento = mueveme

		if entradaPermitida(movimiento) == True:

			#Conmuta el turno de cada color, y muestra en pantalla a quien le toca
			if turno == "Negras":
				turno = "Blancas"
				turnoColor = 1 
			else:
				turno = "Negras"
				turnoColor = 0
			print "  Turno de las " + turno

			#Divide el movimiento en las componentes de las coordenadas origen y destino

			c1 = ord(movimiento[0]) - 65
			c2 = int(movimiento[1])-1			
			c3 = ord(movimiento[2]) - 65
			c4 = int(movimiento[3])-1

			#es quien elige el tipo de movimiento(mover o comer)
			puedeMover(c1, c2, c3, c4)

		mueveme = ""

		for aa in range(8):
			for bb in range(8):
				if tablero[aa][bb].seleccionado:
					tablero[aa][bb].reset()

"""
def hover(casilla, posicion):
	print posicion
"""

#Ventana
win = Gtk.Window()
ancho = 640
alto = 640
win.set_name('Ventana')
win.set_title('Damas - Python')
win.set_default_size(640, alto)

tablero = [[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]

#Layout Fixed con distancias en pixeles
fix = Gtk.Fixed()

#Disponer las casillas vacias y con fichas en el tablero
for a in range(8):
	for b in range(8):
		if (a == 0 or a == 1 or a == 2) and ((a-b)%2 != 0):
			tablero[a][b] = Casilla(0,0, chr(65+a)+str(b+1),False)
		elif (a == 5 or a == 6 or a == 7) and ((a-b)%2 != 0):				
			tablero[a][b] = Casilla(1,0, chr(65+a)+str(b+1),False)
		else:
			tablero[a][b] = Casilla(0,0, chr(65+a)+str(b+1),True)
		#Dar los eventos a cada casilla
		tablero[a][b].connect("clicked", selecionarMovi, tablero[a][b].posicion)
		#tablero[a][b].connect("enter", hover, tablero[a][b].posicion)

#Colocar las casillas dentro del Fixed
for x in range(-7,1):
	for y in range(8):
		fix.put(tablero[abs(x)][abs(y)], (alto/8*abs(y))+5, (ancho/8*(7-abs(x)))+5)


#Anadir el Fixed a la ventana
win.add(fix)

#Evento de cerrar al cerrar la ventana
win.connect("delete-event", Gtk.main_quit)

#Cargar estilos de un fichero
style_provider = Gtk.CssProvider()

css = open('css/estilo.css', 'rb')
css_data = css.read()
css.close()

style_provider.load_from_data(css_data)
Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

#Funciones


#Comprueba si la entrada del usuario es valida
def entradaPermitida(movimiento):

	c1 = ord(movimiento[0]) - 65
	c2 = int(movimiento[1]) - 1
	c3 = ord(movimiento[2]) - 65
	c4 = int(movimiento[3]) - 1
	
	#Comprueba si la orden esta compuesta por 4 caracteres
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

	#Comprueba que las reinas no salten ningun peon
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

#Funcion que indica si el movimiento es comiendo o sin comer una ficha
def puedeMover(c1, c2, c3, c4):

	global seguir
	
	#si la posicion a la que se mueve esta vacia llama a mover, sino llama a comerficha
	if tablero[c3][c4].vacia == True:
		mover(c1, c2, c3, c4)

	else:

		#comprueba que las fichas son de distinto color
		if (tablero[c3][c4].color != tablero[c1][c2].color):
			
			x,y = direcMovimiento(c1, c2, c3, c4)
			
			#llama a comerficha si la posicion siguiente esta vacia si salta un error es porque la ficha se colocaria fuera del tablero, en cuyo caso se captura
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
	
#Devuelve la direccion del movimiento en dos variables separadas, la "x" son el eje vertical y la "y" el horizontal
def direcMovimiento(c1, c2, c3, c4):

	x = (c3 - c1)/calcularDistancia(c1, c3)
	y = (c4 - c2)/calcularDistancia(c1, c3)

	return x,y


#funcion que mueve la ficha
def mover(c1, c2, c3, c4):

	#Pasamos la antigua ficha a la nueva posicion

	tablero[c1][c2].mov(tablero[c3][c4])
	promociona(c3, c4)


#funcion que mueve la ficha a la posicion siguiente de la indicada y elimina la ficha de la posicion marcada, es decir, la come-
def comerFicha(c1, c2, c3, c4):
	
	x,y = direcMovimiento(c1, c2, c3, c4)
	
	#Pasamos la antigua ficha a la nueva posicion
	tablero[c1][c2].mov(tablero[c3 + x][c4 + y])

	#Borramos la posicion antigua y la de la ficha que se ha comido
	tablero[c3][c4].setVacia()

	promociona(c3 + x, c4 + y)
	
	
#funcion que es llamada despues de comer una ficha, come el mayor numero de fichas posibles automaticamente
def comerEnCadena(c3,c4):

	#posibles es una lista que almacena todas las posibles combinaciones de movimientos que se pueden dar. Para calcular los posibles movimientos se llama a calcularPosibles
	posibles = []
	posibles = calcularPosibles(c3,c4)

	#En el caso de que haya alguna combinacion de movimientos, se  elige el  mas largo de todos y se guarda en posibles.
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

		#se recorre la lista que guarda la combinacion movimientos mientras se va llamando a comerFicha cada vez, caracter 3 y 4 son los valores de la lista, mientras que caracter 1 y 2 son la casilla siguiente a estos en el ciclo anterior.
		for recorrido in range(distancia):	

			c3 = int(movimientos[recorrido][0])
			c4 = int(movimientos[recorrido][1])
			
			comerFicha(c1,c2,c3,c4)

			x,y = direcMovimiento(c1, c2, c3, c4)
			c1 = c3 + x
			c2 = c4 + y


#Funcion que convierte en reina a una ficha cuando llega a la primera linea del color contrario.
def promociona(c3, c4):
	if ((tablero[c3][c4].color == 0) and c3 == 7) or ((tablero[c3][c4].color == 1) and c3 == 0):
	
		tablero[c3][c4].tipo = 1

#Funcion que devuelve la lista de los posibles movimientos que puede hacer la ficha.
def calcularPosibles(c3,c4):
	#Creamos posibles y posibles copia, "posibles" sera donde se almacenaran los posibles movimientos, "posiblesCopia" sirve para que si no ha cambiado nada en la siguiente iteracion termine de buscar posibilidades, ya que no hay mas.
	posibles = []
	posiblesCopia = []
	
	#Es el primer valor, y desde donde se empezaran a analizar las posibles opciones.
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

					#Copia la iteracion en lista, y extrae el ultimo valor en "lista1" y "lista2" y si estos son mayores que 0 sigue con el flujo del programa.
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

								#Si encuentra una ficha del mismo color que el de la que esta comiendo, deja de comprobar en esa direccion.
								try: 
									if tableroPosibles[valor1+x+superX][valor2+y+superY].vacia == False and tablero[c3][c4].color == tableroPosibles[valor1+x+superX][valor2+y+superY].color:
										break
								except IndexError:
										break

								addPosibles(valor1,valor2, x,y, lista,posibles, superX, superY, tableroPosibles)

						else:	
							addPosibles(valor1,valor2, x,y, lista,posibles, 0, 0, tableroPosibles)

						
	#Elimina el ultimo valor de cada una de las listas de movimientos dentro de posibles, ya que este es "sig", es decir, la proxima casilla a analizar(que en este caso no hay)						
	for sigDelete in posibles:
		sigDelete.pop()

	return posibles


def addPosibles(valor1,valor2, x,y, lista,posibles, superX, superY,tableroPosibles):
	if (valor1 >= 0) and (valor2 >= 0):

		#Captura el caso de comprobar una casilla fuera del rango de la lista
		try:

			#En el caso de que cumpla las condicciones para que la posicion pueda ser comida tambien comprueba 
			if (tableroPosibles[valor1+x+superX][valor2+y+superY].vacia == False) and (tableroPosibles[valor1+(2*x+superX)][valor2+(2*y+superY)].vacia == True) and (tableroPosibles[valor1+x+superX][valor2+y+superY].color == turnoColor):
				
				if (valor1+2*x+superX >= 0) and (valor2+2*y+superY >= 0):

					#"movi" es el valor que se usara para comer la ficha mientras que "sig" es la casilla siguiente que se comprobara(despues de usarse queda eliminado de la lista)
					movi = str(valor1+x+superX)+ str (valor2+y+superY)
					sig = str(valor1+(2*x+superX))+ str (valor2+(2*y+superY))
				

					#si "movi" no pertenece a la lista de movimientos, se anaden
					if (perteneceALista(movi, lista) == False):
						lista.append(movi)
						lista.append(sig)

						#Si ya hay una lista con los mismos valores dentro de posibles, esta se descarta, sino, se anade.
						if (perteneceALista(lista, posibles) == False):
							posibles.append(lista)
							
		except IndexError:
			pass

	return posibles


#Funcion booleana, si el primer parametro pertenece al segundo parametro.
def perteneceALista(movi, posibles):
	try:
		posibles.index(movi)
		return True
		
	except ValueError:
		return False

#Funcion que devuelve las fichas que quedan del color que se indica.
def numFichas(turnoColor):
	fichas = 0 

	#Recorre la lista y va incrementando "fichas" por cada ficha del jugador contrario que se encuentra
	for x in range(8):
		for y in range (8):
			if tablero[x][y] != 0:
				if turnoColor != tablero[x][y].color:
					fichas = fichas + 1

	return fichas

win.show_all()
Gtk.main()