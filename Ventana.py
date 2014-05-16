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

#Layout Fixed con distancias en pixeles
fix = Gtk.Fixed()


#Disponer las casillas vacias y con fichas en el tablero
for a in range(8):
	for b in range(8):
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

win.show_all()
Gtk.main()