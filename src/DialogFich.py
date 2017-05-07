# Adrian Calvo Rojo y Sergio Garcia Prado
from gi.repository import Gtk


class CargaTablero(Gtk.Fixed):
    texto = Gtk.Entry()
    button2 = Gtk.Button("Cargar")

    def __init__(self, ventana):
        # Gtk.Window.__init__(self, title="Cargar un tablero")
        super(Gtk.Fixed, self).__init__()
        # super(CargaTablero, self).set_size_request(75,75)

        fixed = Gtk.Fixed()
        self.put(fixed, 1, 1)

        self.ventana = ventana

        label = Gtk.Label("Cargar un fichero: ")
        label.set_name("CargaTablero")
        fixed.put(label, 5, 10)

        fixed.put(self.texto, 10, 30)
        self.texto.set_width_chars(36)

        button1 = Gtk.Button("Archivo origen...")
        button1.connect("clicked", self.on_clicked)
        fixed.put(button1, 10, 65)

        fixed.put(self.button2, 255, 65)

    def on_clicked(self, widget):
        dialog = Gtk.FileChooserDialog("Por favor, selecciona un fichero con movimientos", self.ventana,
                                       Gtk.FileChooserAction.OPEN,
                                       (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        self.add_filters(dialog)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:

            print("Fichero a cargar: " + dialog.get_filename())
            self.texto.set_text(dialog.get_filename())
        elif response == Gtk.ResponseType.CANCEL:
            print("Cargar cancelado")

        dialog.destroy()

    def add_filters(self, dialog):
        filter_text = Gtk.FileFilter()
        filter_text.set_name(".txt")
        filter_text.add_mime_type("text/plain")
        dialog.add_filter(filter_text)

        filter_any = Gtk.FileFilter()
        filter_any.set_name("Todos")
        filter_any.add_pattern("*")
        dialog.add_filter(filter_any)


class GuardaTablero(Gtk.Fixed):
    carpeta = "partidas"
    nombre = Gtk.Entry()
    button2 = Gtk.Button("Guardar")

    def __init__(self, ventana):
        # Gtk.Window.__init__(self, title="Cargar un tablero")
        super(Gtk.Fixed, self).__init__()
        # super(CargaTablero, self).set_size_request(75,75)

        fixed = Gtk.Fixed()
        self.put(fixed, 1, 1)

        self.ventana = ventana

        label = Gtk.Label("Guardar como: ")
        label.set_name("GuardarTablero")
        fixed.put(label, 5, 10)

        fixed.put(self.nombre, 10, 30)
        self.nombre.set_width_chars(36)

        button1 = Gtk.Button("Carpeta destino...")
        button1.connect("clicked", self.on_clicked)
        fixed.put(button1, 10, 65)

        fixed.put(self.button2, 245, 65)

    def on_clicked(self, widget):

        dialog = Gtk.FileChooserDialog("Por favor, selecciona una carpeta", self.ventana,
                                       Gtk.FileChooserAction.SELECT_FOLDER,
                                       (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                        "Seleccionar", Gtk.ResponseType.OK))

        response = dialog.run()
        if response == Gtk.ResponseType.OK:

            print("Carpeta: " + dialog.get_filename())
            self.carpeta = dialog.get_filename()
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancelado guardar")

        dialog.destroy()
