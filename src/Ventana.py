#!/usr/bin/python/home/adrian/Dropbox/Damas Adri y Sergio/Damas copia 2/css

from gi.repository import Gtk, Gdk
from Ficha import Casilla
from DialogFich import CargaTablero, GuardaTablero
from DialogVerificate import NewGameVerification

""" * * * * * * * * * Variables * * * * * * * * * """
tablero = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]
jugadas = []
jugadasSecuencia = []

# Almacena todos los tipos de mensaje de error
mnsj_error = ["Solo se puede mover en las casillas blancas",
              "Solo se puede mover en diagonal",
              "Los peones solo se pueden mover con distancia 1",
              "No puede mover las fichas del jugador contrario",
              "Las casillas estan vacias",
              "No se pueden comer fichas propias",
              "Las reinas no pueden saltar peones",
              "Ficha fuera de tablero o casilla ocupada",
              "Ficha fuera de tablero"]

# Guarda la cadena con el movimiento que se va a realizar
mueveme = ""
# Indica si se mueven las fichas blancas o las negras (Blancas = 1 , Negras = 0)
turno = 1

ancho = 640
alto = 640

win = Gtk.Window()

botonDeshacer = Gtk.Button("Deshacer")
botonNewGame = Gtk.Button("Nueva Partida")

fix = Gtk.Fixed()
cargar = CargaTablero(win)
guardar = GuardaTablero(win)
fixedAll = Gtk.Fixed()
style_provider = Gtk.CssProvider()

barraBlanca = Gtk.ProgressBar()
barraNegra = Gtk.ProgressBar()

lbl_info = Gtk.Label()
lbl_blancas = Gtk.Label()
lbl_negras = Gtk.Label()
lbl_turno = Gtk.Label()
fichaColor = Gtk.Image()

finalImagen = Gtk.Image()
finalImagen.set_size_request(640, 640)

""" * * * * * * * * * * Metodos * * * * * * * * * * * * """


# Se va a llamar cada vez que se pulse en una casilla
def selecionarMovi(casilla, posicion):
    global mueveme

    if casilla.color == 0 and not casilla.vacia:
        if casilla.tipo == 0:
            casilla.set_name("FichaNegraSel")
            casilla.seleccionado = True
        else:
            casilla.set_name("FichaNegraDamaSel")
            casilla.seleccionado = True

    if casilla.color == 1 and not casilla.vacia:
        if casilla.tipo == 0:
            casilla.set_name("FichaBlancaSel")
            casilla.seleccionado = True
        else:
            casilla.set_name("FichaBlancaDamaSel")
            casilla.seleccionado = True

    if (len(mueveme) == 2) and ((mueveme[0] + mueveme[1]) == (posicion[0] + posicion[1])):

        mueveme = ""

        for aa in range(8):
            for bb in range(8):
                if tablero[aa][bb].seleccionado:
                    tablero[aa][bb].reset()
    else:
        if not (len(mueveme) == 0 and casilla.vacia):
            mueveme += posicion

    if len(mueveme) == 4:
        print(mueveme)

        movimiento = mueveme

        if entradaPermitida(movimiento) == True:

            # Divide el movimiento en las componentes de las coordenadas origen y destino
            c1, c2, c3, c4 = ord(movimiento[0]) - 65, int(movimiento[1]) - 1, ord(movimiento[2]) - 65, int(
                movimiento[3]) - 1

            tableroAnterior = copiarTablero(tablero)

            # Elige el tipo de movimiento(mover o comer)
            if puedeMover(c1, c2, c3, c4):

                jugadas.append(tableroAnterior)
                cambiarTurno()

                jugadasSecuencia.append(mueveme)
                botonDeshacer.set_sensitive(True)

                if (numFichas(1) == 0):
                    finalImagen.set_name("FinalNegras")
                    botonDeshacer.set_sensitive(False)
                elif (numFichas(0) == 0):
                    finalImagen.set_name("FinalBlancas")
                    botonDeshacer.set_sensitive(False)
        mueveme = ""

        for aa in range(8):
            for bb in range(8):
                if tablero[aa][bb].seleccionado:
                    tablero[aa][bb].reset()


# Deja el juego tal y como estaba al principio
def reinicializarTablero(self):
    global turno
    turno = 1

    # Reset
    for a in range(8):
        for b in range(8):
            if (a == 0 or a == 1 or a == 2) and ((a - b) % 2 != 0):
                tablero[a][b].color = 0
                tablero[a][b].tipo = 0
                tablero[a][b].posicion = chr(65 + a) + str(b + 1)
                tablero[a][b].vacia = False
                tablero[a][b].set_name('FichaNegra')
            elif (a == 5 or a == 6 or a == 7) and ((a - b) % 2 != 0):
                tablero[a][b].color = 1
                tablero[a][b].tipo = 0
                tablero[a][b].posicion = chr(65 + a) + str(b + 1)
                tablero[a][b].vacia = False
                tablero[a][b].set_name('FichaBlanca')
            else:
                tablero[a][b].posicion = chr(65 + a) + str(b + 1)
                tablero[a][b].setVacia()

    actualizaturno(turno)
    finalImagen.set_name("")


# Lee desde un fichero una serie de jugadas y simula el movimiento de las fichas
def cargarJugada(boton):
    print(cargar.texto.get_text())

    reinicializarTablero("")

    # Carga un fichero con movimientos desde un archivo de texto con el nombre introducido por el usuario
    fichero = cargar.texto.get_text()
    try:
        fich = open(fichero, "r")
    except IOError:
        fich = ""

    if fich != "":
        cad = fich.readline(4)
        fich.readline()

        while cad != "":
            if entradaPermitida(cad):

                # Divide el movimiento en las componentes de las coordenadas origen y destino
                c1, c2, c3, c4 = ord(cad[0]) - 65, int(cad[1]) - 1, ord(cad[2]) - 65, int(cad[3]) - 1

                tableroAnterior = copiarTablero(tablero)

                # Elige el tipo de movimiento(mover o comer)
                if puedeMover(c1, c2, c3, c4):
                    jugadas.append(tableroAnterior)
                    cambiarTurno()
                    jugadasSecuencia.append(cad)
                    botonDeshacer.set_sensitive(True)

            cad = fich.readline(4)
            fich.readline()


# Guarda en un fichero la sucesion de jugadas para dejar el tablero en la situacion actual
def guardarJugada(boton):
    carpeta = guardar.carpeta
    nombre = guardar.nombre.get_text()

    ruta = carpeta + "/"

    if nombre == "":
        fichero = open(ruta + "damasDefaut.txt", "w")
    else:
        fichero = open(ruta + nombre + ".txt", "w")

    for movimiento in jugadasSecuencia:
        fichero.write(movimiento)
        fichero.write("\r\n")

    fichero.close()


# Conmuta el turno de cada color
def cambiarTurno():
    global turno

    if turno == 0:
        turno = 1
    else:
        turno = 0

    actualizaturno(turno)
    botonNewGame.set_sensitive(True)


# En funcion del valor que tome la variable "turno", cambia la etiqueta y el color de la ficha de jugador al que toque. tambien las ProgressBar
def actualizaturno(turno):
    barraNegra.set_text(str(numFichas(0)))
    barraNegra.set_fraction(0.0833 * numFichas(0))

    barraBlanca.set_text(str(numFichas(1)))
    barraBlanca.set_fraction(0.0833 * numFichas(1))

    if turno == 1:
        fichaColor.set_name("FichaBlanca")
        lbl_turno.set_text("Turno de las fichas blancas")
    else:
        fichaColor.set_name("FichaNegra")
        lbl_turno.set_text("Turno de las fichas negras")


# Funciones
# Comprueba si la entrada del usuario es valida
def entradaPermitida(movimiento):
    c1 = ord(movimiento[0]) - 65
    c2 = int(movimiento[1]) - 1
    c3 = ord(movimiento[2]) - 65
    c4 = int(movimiento[3]) - 1

    # Buscamos que el movimiento sea solo en las casillas blancas
    if (abs(c3) - c4 + 1) % 2 != 0:
        lbl_info.set_text(mnsj_error[0])
        return False

    # Comprobamos si el movimiento es solo en diagonal
    if abs(c1 - c3) != abs(c2 - c4):
        lbl_info.set_text(mnsj_error[1])
        return False

    # Comprueba que el movimiento de los peones solo es de una unidad
    if (tablero[c1][c2].tipo == 0) and calcularDistancia(c1, c3) != 1:
        lbl_info.set_text(mnsj_error[2])
        return False

    # Comprueba que no se haya movido la ficha del jugador rival
    if ((tablero[c1][c2].color == 0) and (turno == 1)) or ((tablero[c1][c2].color == 1) and (turno == 0)):
        lbl_info.set_text(mnsj_error[3])
        return False

    if tablero[c1][c2].vacia:
        lbl_info.set_text(mnsj_error[4])
        return False

    # Comprueba que la ficha que se quiere comer no sea del mismo color que la que come.
    if (not tablero[c3][c4].vacia) and (tablero[c1][c2].color == tablero[c3][c4].color):
        lbl_info.set_text(mnsj_error[5])
        return False

    # Calculamos la distancia y la direccion de las coordenadas (x, y)
    distancia = calcularDistancia(c1, c3)
    x, y = direcMovimiento(c1, c2, c3, c4)

    # Comprueba que las reinas no salten ningun peon
    if (tablero[c1][c2].tipo == 1) and (distancia != 1):

        i = 1
        while (i != distancia):

            lado = i * x
            arriba = i * y
            i += 1

            if not tablero[c1 + lado][c2 + arriba].vacia:
                lbl_info.set_text(mnsj_error[6])
                return False

    # En caso de que no se cumpla ningun caso anterior, quiere decir que la entrada del usuario ha sido correcta, por lo que devuelve verdadero
    return True


# Devuelve la distancia del movimiento realizado
def calcularDistancia(c1, c3):
    return abs(c1 - c3)


# Funcion que indica si el movimiento es comiendo o sin comer una ficha
def puedeMover(c1, c2, c3, c4):
    seguir = True

    # si la posicion a la que se mueve esta vacia llama a mover, sino llama a comerficha
    if tablero[c3][c4].vacia:
        mover(c1, c2, c3, c4)

    else:

        # comprueba que las fichas son de distinto color
        if (tablero[c3][c4].color != tablero[c1][c2].color):

            x, y = direcMovimiento(c1, c2, c3, c4)

            # llama a comerficha si la posicion siguiente esta vacia
            # si salta un error es porque la ficha se colocaria fuera del tablero, en cuyo caso se captura
            try:
                if (c4 != 0) and tablero[c3 + x][c4 + y].vacia:

                    comerFicha(c1, c2, c3, c4)
                    comerEnCadena(c3 + x, c4 + y)

                else:
                    lbl_info.set_text(mnsj_error[7])
                    seguir = False
            except IndexError:
                lbl_info.set_text(mnsj_error[8])
                seguir = False
    return seguir


# Devuelve la direccion del movimiento en dos variables separadas, la "x" son el eje vertical y la "y" el horizontal
def direcMovimiento(c1, c2, c3, c4):
    return (c3 - c1) / calcularDistancia(c1, c3), (c4 - c2) / calcularDistancia(c1, c3)


# Mueve la ficha de una casilla a otra cuando esta segunda esta vacia
def mover(c1, c2, c3, c4):
    # Pasamos la antigua ficha a la nueva posicion
    tablero[c1][c2].mov(tablero[c3][c4])
    promociona(c3, c4)


# funcion que mueve la ficha a la posicion siguiente de la indicada y elimina la ficha de la posicion marcada, es decir, la come-
def comerFicha(c1, c2, c3, c4):
    x, y = direcMovimiento(c1, c2, c3, c4)
    # Pasamos la antigua ficha a la nueva posicion
    tablero[c1][c2].mov(tablero[c3 + x][c4 + y])
    # Borramos la posicion antigua y la de la ficha que se ha comido
    tablero[c3][c4].setVacia()
    promociona(c3 + x, c4 + y)


# funcion que es llamada despues de comer una ficha, come el mayor numero de fichas posibles automaticamente
def comerEnCadena(c3, c4):
    # posibles es una lista que almacena todas las posibles combinaciones de movimientos que se pueden dar. Para calcular los posibles movimientos se llama a calcularPosibles
    posibles = calcularPosibles(c3, c4)

    # En el caso de que haya alguna combinacion de movimientos, se  elige el  mas largo de todos y se guarda en posibles.
    if len(posibles) > 0:

        a = len(posibles[0])
        movimientos = posibles[0]

        for i in posibles:
            b = len(i)

            if (a <= b):
                movimientos = i
                a = b

        # Se inicializan caracter 1 y 2 con los valores de caracter 3 y 4 respectivamente.
        distancia = len(movimientos)
        c1 = c3
        c2 = c4

        # se recorre la lista que guarda la combinacion movimientos mientras se va llamando a comerFicha cada vez, caracter 3 y 4 son los valores de la lista, mientras que caracter 1 y 2 son la casilla siguiente a estos en el ciclo anterior.
        for recorrido in range(distancia):
            c3 = int(movimientos[recorrido][0])
            c4 = int(movimientos[recorrido][1])

            comerFicha(c1, c2, c3, c4)

            x, y = direcMovimiento(c1, c2, c3, c4)
            c1 = c3 + x
            c2 = c4 + y


# Funcion que convierte en reina a una ficha cuando llega a la primera linea del color contrario.
def promociona(c3, c4):
    if ((tablero[c3][c4].color == 0) and c3 == 7) or ((tablero[c3][c4].color == 1) and c3 == 0):
        tablero[c3][c4].promociona()


# Funcion que devuelve la lista de los posibles movimientos que puede hacer la ficha.
def calcularPosibles(c3, c4):
    # Creamos posibles y posibles copia, "posibles" sera donde se almacenaran los posibles movimientos, "posiblesCopia" sirve para que si no ha cambiado nada en la siguiente iteracion termine de buscar posibilidades, ya que no hay mas.
    posibles = []
    posiblesCopia = []

    # Es el primer valor, y desde donde se empezaran a analizar las posibles opciones.
    original = str(c3) + str(c4)
    posibles.append([original])

    tablero[c3][c4].vacia = True

    # Comprueba que "posibles" no sea igual que en la anterior pasaad
    while (posibles != posiblesCopia):
        posiblesCopia = posibles[:]
        # Recorre las cuatro direcciones
        for x in range(1, -2, -2):
            for y in range(1, -2, -2):

                # Recorre cada una de las posibilidades (listas dentro de posibles)
                for i in posibles:

                    # Copia la iteracion en lista, y extrae el ultimo valor en "lista1" y "lista2" y si estos son mayores que 0 sigue con el flujo del programa.
                    lista = i[:]
                    valor = lista.pop()
                    valor1 = int(valor[0])
                    valor2 = int(valor[1])

                    # Recorre todos los movimientos
                    for r in i:

                        # Si encuentra que una ficha es o se ha transformado en reina, recorre la diagonal, sino solo mira la posicion siguiente.
                        if (turno == 1 and r[0] == "1") or (turno == 0 and r[0] == "6") or (tablero[c3][c4].tipo == 1):

                            for j in range(5):
                                superX = x * j
                                superY = y * j

                                # Si encuentra una ficha del mismo color que el de la que esta comiendo, deja de comprobar en esa direccion.
                                try:
                                    if not tablero[valor1 + x + superX][valor2 + y + superY].vacia:
                                        addPosibles(valor1, valor2, x, y, lista, posibles, superX, superY)
                                        break
                                except IndexError:
                                    break


                        else:
                            addPosibles(valor1, valor2, x, y, lista, posibles, 0, 0)

    # Elimina el ultimo valor de cada una de las listas de movimientos dentro de posibles, ya que este es "sig", es decir, la proxima casilla a analizar(que en este caso no hay)
    for sigDelete in posibles:
        sigDelete.pop()

    tablero[c3][c4].vacia = False

    return posibles


def addPosibles(valor1, valor2, x, y, lista, posibles, superX, superY):
    if (valor1 >= 0) and (valor2 >= 0):

        # Captura el caso de comprobar una casilla fuera del rango de la lista
        try:

            # En el caso de que cumpla las condicciones para que la posicion pueda ser comida tambien comprueba
            if (not tablero[valor1 + x + superX][valor2 + y + superY].vacia) and (
                    tablero[valor1 + (2 * x + superX)][valor2 + (2 * y + superY)].vacia) and (
                        tablero[valor1 + x + superX][valor2 + y + superY].color != turno):

                if (valor1 + 2 * x + superX >= 0) and (valor2 + 2 * y + superY >= 0):

                    # "movi" es el valor que se usara para comer la ficha mientras que "sig" es la casilla siguiente que se comprobara(despues de usarse queda eliminado de la lista)
                    movi = str(valor1 + x + superX) + str(valor2 + y + superY)
                    sig = str(valor1 + (2 * x + superX)) + str(valor2 + (2 * y + superY))

                    # si "movi" no pertenece a la lista de movimientos, se anaden
                    if not perteneceALista(movi, lista):
                        lista.append(movi)
                        lista.append(sig)

                        # Si ya hay una lista con los mismos valores dentro de posibles, esta se descarta, sino, se anade.
                        if not perteneceALista(lista, posibles):
                            posibles.append(lista)

        except IndexError:
            pass

    return posibles


# Funcion booleana, si el primer parametro pertenece al segundo parametro.
def perteneceALista(movi, posibles):
    try:
        posibles.index(movi)
        return True

    except ValueError:
        return False


# Funcion que devuelve las fichas que quedan del color que se indica.
def numFichas(turno):
    fichas = 0

    # Recorre la lista y va incrementando "fichas" por cada ficha del jugador contrario que se encuentra
    for x in range(8):
        for y in range(8):
            if turno == tablero[x][y].color:
                fichas = fichas + 1

    return fichas


# Carga el ultimo tablero del array "tablerodeshacer" y sustituye al actual
def deshacerJugada(self):
    if jugadas != []:

        tablerodeshacer = jugadas.pop()
        jugadasSecuencia.pop()

        for y in range(8):
            for x in range(8):
                tablero[y][x].tipo = tablerodeshacer[y][x].tipo
                tablero[y][x].color = tablerodeshacer[y][x].color
                tablero[y][x].vacia = tablerodeshacer[y][x].vacia
                tablero[y][x].set_name(tablerodeshacer[y][x].get_name())

        cambiarTurno()

        if jugadas == []:
            botonDeshacer.set_sensitive(False)
            botonNewGame.set_sensitive(False)


def copiarTablero(tableroOriginal):
    tableroNuevo = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]
    for y in range(8):
        for x in range(8):
            tableroNuevo[y][x] = Casilla(tableroOriginal[y][x].color, tableroOriginal[y][x].tipo,
                                         chr(65 + y) + str(x + 1), tableroOriginal[y][x].vacia)

    return tableroNuevo


def partidaNueva(self):
    global jugadas

    dialog = NewGameVerification(win)
    response = dialog.run()

    if response == Gtk.ResponseType.OK:
        reinicializarTablero(self)
        jugadas = []
        botonNewGame.set_sensitive(False)
        botonDeshacer.set_sensitive(False)

    dialog.destroy()


# Disponer las casillas vacias y con fichas en el tablero
for a in range(8):
    for b in range(8):
        if (a == 0 or a == 1 or a == 2) and ((a - b) % 2 != 0):
            tablero[a][b] = Casilla(0, 0, chr(65 + a) + str(b + 1), False)
        elif (a == 5 or a == 6 or a == 7) and ((a - b) % 2 != 0):
            tablero[a][b] = Casilla(1, 0, chr(65 + a) + str(b + 1), False)
        else:
            tablero[a][b] = Casilla(None, None, chr(65 + a) + str(b + 1), True)
        # Dar los eventos a cada casilla
        tablero[a][b].connect("clicked", selecionarMovi, tablero[a][b].posicion)
        tablero[a][b].set_tooltip_text(tablero[a][b].posicion)

# Colocar las casillas dentro del Fixed
for x in range(-7, 1):
    for y in range(8):
        fix.put(tablero[abs(x)][abs(y)], (alto / 8 * abs(y)), (ancho / 8 * (7 - abs(x))))

"""  * * * * * * * * * * * Propiedades * * * * * * * * * * * """
win.set_name('Ventana')
win.set_title('Damas - Python')
win.set_default_size(1080, 720)
win.connect("delete-event", Gtk.main_quit)

fichaColor.set_size_request(75, 75)
fichaColor.set_name("FichaBlanca")

botonDeshacer.set_name("BotonDeshacer")
botonDeshacer.set_size_request(320, 60)
botonDeshacer.connect("clicked", deshacerJugada)
botonDeshacer.set_sensitive(False)

botonNewGame.set_size_request(320, 30)
botonNewGame.connect("clicked", partidaNueva)
botonNewGame.set_sensitive(False)

cargar.button2.connect("clicked", cargarJugada)
guardar.button2.connect("clicked", guardarJugada)

lbl_info.set_name("lbl")
lbl_info.set_width_chars(41)

barraBlanca.set_size_request(145, 150)
barraBlanca.set_show_text(True)
barraBlanca.set_text(str(numFichas(1)))
barraBlanca.set_fraction(0.0833 * numFichas(1))
barraBlanca.set_inverted(True)
barraBlanca.set_orientation(Gtk.Orientation.VERTICAL)

barraNegra.set_size_request(145, 150)
barraNegra.set_show_text(True)
barraNegra.set_text(str(numFichas(0)))
barraNegra.set_fraction(0.0833 * numFichas(0))
barraNegra.set_inverted(True)
barraNegra.set_orientation(Gtk.Orientation.VERTICAL)

lbl_blancas.set_text("Blancas")
lbl_blancas.set_name("lbl")
lbl_blancas.set_width_chars(10)

lbl_negras.set_text("Negras")
lbl_negras.set_name("lbl")
lbl_negras.set_width_chars(10)

lbl_turno.set_text("Turno de las fichas blancas")
lbl_turno.set_name("lbl")
lbl_turno.set_width_chars(20)

fixedAll.put(lbl_blancas, 775, 330)
fixedAll.put(lbl_negras, 945, 330)
fixedAll.put(lbl_turno, 740, 75)

fixedAll.put(barraNegra, 915, 165)
fixedAll.put(barraBlanca, 740, 165)

fixedAll.put(fix, 40, 40)
fixedAll.put(fichaColor, 950, 50)
fixedAll.put(botonDeshacer, 740, 390)
fixedAll.put(botonNewGame, 740, 680)
fixedAll.put(cargar, 740, 470)
fixedAll.put(guardar, 740, 570)
fixedAll.put(lbl_info, 740, 10)
fixedAll.put(finalImagen, 40, 40)
win.add(fixedAll)

css = open('css/estilo.css', 'rb')
css_data = css.read()
css.close()

style_provider.load_from_data(css_data)
Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), style_provider,
                                         Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

win.show_all()
Gtk.main()
