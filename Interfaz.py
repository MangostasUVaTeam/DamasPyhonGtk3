
import gtk
import cairo
import math
from Ficha import Ficha

Width = 640
Height = 480
TokenSize = 60
AllTokens = Width * Height / (TokenSize * TokenSize)

"""class Board(gtk.DrawingArea):

	def __init__(self):
		super(Board, self).__init__()

		self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(0, 0, 0))
		self.set_size_request(Width, Height)

		self.connect("expose-event", self.expose)

		self.init_game()

	def init_game(self):

		self.tokens = 24"""
class Casilla(gtk.DrawingArea):

	def __init__(self):
		gtk.DrawingArea.__init__(self)
		self.add_events(gtk.gdk.BUTTON_PRESS_MASK |
				gtk.gdk.BUTTON1_MOTION_MASK)
		
		self.connect("expose_event", self.expose)
		self.connect("button_press_event", self.pressing)
		
		#Desplazamiento
		self.desp = 0

	def pressing(self, widget, event):
		self.pressing_x = event.x
		print "Hola"

	def moving(self, widget, event):
		#Determinamos si nos movemos a la izquierda
		#o hacia la derecha
		if (self.pressing_x - event.x) > 1:
			self.desp = self.desp + 0.1
		else:
			self.desp = self.desp - 0.1
		
		self.pressing_x = event.x
		
		#Volvemos a dibujar el contexto
		self.draw(self.context)
		#Redibujamos el widget
		self.queue_draw()

	def expose(self, widget, event):
		self.context = widget.window.cairo_create()
		
		self.context.rectangle(event.area.x, event.area.y,
				event.area.width, event.area.height)
		self.context.clip()
	
		self.draw(self.context)
		return False

	def draw(self, context):
		rect = self.get_allocation()
		x = rect.x + rect.width / 2
		y = rect.y + rect.height / 2

		radius = min(rect.width / 2, rect.height / 2) - 5
		
		context.arc(x, y, radius, 0 + self.desp ,
				(1 * math.pi) + self.desp)
		
		context.set_source_rgb(0.7, 0.8, 0.1)
		context.fill_preserve()
		
		context.set_source_rgb(0, 0, 0)
		context.stroke()

def main():
	window = gtk.Window()
	drawing_area = gtk.DrawingArea()
	casilla = Casilla()
	
	"""for i in range(24):
		drawing_area.add(casilla)
		drawing_area.connect("destroy", gtk.main_quit)"""
	
	drawing_area.set_size_request(Width, Height)
	window.add(casilla)
	window.show_all()
	
	gtk.main()

if __name__ == "__main__":
	main()





