#!/usr/bin/python
from gi.repository import Gtk, Gdk
from Ficha import Casilla

mover = ""

def selecionarMovi(casilla, posicion):

	if casilla.color == 0 and not casilla.vacia:
		casilla.set_name("FichaNegraSel")
		casilla.seleccionado = True
	if casilla.color == 1 and not casilla.vacia:
		casilla.set_name("FichaBlancaSel")
		casilla.seleccionado = True

	global mover
	mover += posicion
	if len(mover) == 4:
		print mover
		mover = ""
		for a in range(8):
			for b in range(8):
				if tablero[a][b].seleccionado:
					tablero[a][b].reset()

"""
def hover(casilla, posicion):
	print posicion
"""

#Ventana
win = Gtk.Window()
ancho = 480
alto = 480
win.set_name('Ventana')
win.set_title('Damas - Python')
win.set_default_size(640, alto)

tablero = [[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]

#Layout Fixed con distancias en pixeles
fix = Gtk.Fixed()

#Disponer las casillas vacias y con fichas en el tablero
for a in range(8):
	for b in range(8):
			if (a == 0 or a == 1 or a == 2) and ((a-b)%2 == 0):
				tablero[b][a] = Casilla(1,0, chr(72-a)+str(b+1),False)
			elif (a == 5 or a == 6 or a == 7) and ((a-b)%2 == 0):
				tablero[b][a] = Casilla(0,0, chr(72-a)+str(b+1),False)
			else:
				tablero[b][a] = Casilla(0,0, chr(72-a)+str(b+1),True)
			#Dar los eventos a cada casilla
			tablero[b][a].connect("clicked", selecionarMovi, tablero[b][a].posicion)			
			#tablero[b][a].connect("enter", hover, tablero[b][a].posicion)

#Colocar las casillas dentro del Fixed
for x in range(8):
	for y in range(8):
		if x == 0 and y == 0:
			fix.put(tablero[x][y], 5, 5)

		else:
			fix.put(tablero[x][y], (ancho/8*x)+5, (alto/8*y)+5)

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