from gi.repository import Gtk


class NewGameVerification(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "Nueva Partida", parent, 0,
                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                             Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.set_default_size(150, 100)

        label = Gtk.Label("Esta seguro de que desea iniciar una nueva partida y perder la actual partida?")

        box = self.get_content_area()
        box.add(label)
        self.show_all()
