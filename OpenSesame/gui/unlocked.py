import cairo
import gtk
import glib
import os

def yieldsleep(func):
    def start(*args, **kwds):
        iterable = func(*args, **kwds)
        def step(*args, **kwds):
            try:
                secs = next(iterable)
                glib.timeout_add(secs, step)
            except StopIteration:
                pass
        glib.idle_add(step)
    return start

class KeyFade(gtk.Window):

    def __init__(self):
        super(KeyFade, self).__init__()
        self.connect("expose-event", self.do_expose_event)
        self.set_app_paintable(True)
        self.set_decorated(False)
        self.set_property("resizable", False)
        self.set_size_request(240, 105)
        self.set_colormap(self.get_screen().get_rgba_colormap())
        self.set_position(gtk.WIN_POS_CENTER)
        self.set_skip_taskbar_hint(True)
        self.set_skip_pager_hint(True)
        self.show_all()

    @yieldsleep
    def do_expose_event(self, widget, event): 
        timer = range(0,20)
        timer.reverse()
        fadealpha = 1.0
        for i in timer:
            yield i/4*i
            fadealpha -= .1
            cr = widget.window.cairo_create()
            cr.set_operator(cairo.OPERATOR_CLEAR)
            cr.rectangle(0, 0, *widget.get_size())
            cr.fill()
            cr.set_operator(cairo.OPERATOR_OVER)
            key_image = cairo.ImageSurface.create_from_png(os.path.dirname(__file__)+"/key.png")
            cr.set_source_surface(key_image, 0, 0)
            cr.paint_with_alpha(fadealpha)
        self.hide()
