import cairo
import gtk
import os

from OpenSesame.xutils import yieldsleep

class KeyFade(gtk.Window):
    def __init__(self, active_win):
        super(KeyFade, self).__init__()
        self.active_win = active_win
        self.set_app_paintable(True)
        self.set_decorated(False)
        self.set_property("resizable", False)
        self.set_size_request(240, 105)
        self.set_colormap(self.get_screen().get_rgba_colormap())
        self.set_position(gtk.WIN_POS_CENTER)
        self.set_skip_taskbar_hint(True)
        self.set_skip_pager_hint(True)
        self.set_keep_above(True)
        self.connect("expose-event", self.do_expose_event)
        self.image = os.path.dirname(__file__)+"/key.png"
        if not os.path.exists(self.image):
            print "couldn't find the key image in {0}".format(self.image)
        self.key_image = cairo.ImageSurface.create_from_png(self.image)

    @yieldsleep
    def do_expose_event(self, widget, event):
        if os.path.exists(self.image):
            timer = range(0,18)
            timer.reverse()
            fadealpha = 0.9
            for i in timer:
                yield i/4*i
                fadealpha -= .05
                cr = widget.window.cairo_create()
                cr.set_operator(cairo.OPERATOR_CLEAR)
                cr.rectangle(0, 0, *widget.get_size())
                cr.fill()
                cr.set_operator(cairo.OPERATOR_OVER)
                cr.set_source_surface(self.key_image, 0, 0)
                cr.paint_with_alpha(fadealpha)
            self.fading = False
            self.hide()
