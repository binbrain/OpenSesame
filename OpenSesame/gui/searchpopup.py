import gtk
import cairo
from gtk.gdk import keyval_name
from math import pi as M_PI

from OpenSesame.xutils import secured_clipboard


class SearchPopup(gtk.Window):
    def __init__(self, search, ring, pw_engine):
        super(SearchPopup, self).__init__()
        self.search = search
        self.ring = ring
        self.pw_engine = pw_engine
        self.set_decorated(False)
        self.set_position(gtk.WIN_POS_CENTER)
        self.set_size_request(505, 90)
        self.set_app_paintable(True)
        self.set_colormap(self.get_screen().get_rgba_colormap())
        self.set_property("resizable", False)
        self.set_skip_taskbar_hint(True)
        self.set_skip_pager_hint(True)
        self.connect("expose-event", self.do_expose_event) 
        self.connect("key-press-event", self.key_pressed)

    def do_expose_event(self, widget, event):
        cr = widget.window.cairo_create()
        # Sets the operator to clear which deletes everything below where an 
        # object is drawn
        cr.set_operator(cairo.OPERATOR_CLEAR)
        # Makes the mask fill the entire window
        cr.rectangle(0, 0, *widget.get_size())
        # Deletes everything in the window (since the compositing operator is
        # clear and mask fills the entire window
        cr.fill()
        # Set the compositing operator back to the default
        cr.set_operator(cairo.OPERATOR_OVER)
        cr.set_source_rgba(.1,.1,.1,.5)
        self._rounded_edge_draw(cr, 4, 4, 480, 75)
        self._inside_frame(cr, 11)
        self._inside_right_frame(cr)

    def _inside_right_frame(self, cr):
        self._inside_frame(cr, 247, r=.2, g=.2, b=.2)
        cr.select_font_face("Monospace")
        cr.set_font_size(15.0)
        cr.move_to(260, 47)
        cr.set_source_rgb(1, 1, 1)
        best_guess_desc = self.search.best_guess()[1]
        if best_guess_desc:
            cr.move_to(258, 51)
            cr.set_font_size(26.0)
            cr.set_source_rgb(.1, 1, .1)
            cr.show_text(best_guess_desc)
        else:
            if len(self.search.string) > 0:
                cr.show_text("<SpaceBar> new password")
            else:
                cr.show_text("  <Ctrl>-k configure")
        cr.stroke()

    def _inside_frame(self, cr, x, r=.1, g=.1, b=.1):
        cr.set_source_rgba(r, g, b, 1)
        self._rounded_edge_draw(cr, x, 8, 230, 66)

    def _rounded_edge_draw(self, cr, x, y, width, height):
        aspect = 1.0
        corner_radius = height/10.0
        radius = corner_radius/aspect
        degrees = M_PI/180.0
        cr.arc(x+width-radius, y+radius, radius, -90*degrees, 0*degrees)
        cr.arc(x+width-radius, y+height-radius, radius, 0*degrees, 90*degrees)
        cr.arc(x+radius, y+height-radius, radius, 90*degrees, 180*degrees)
        cr.arc(x+radius, y+radius, radius, 180*degrees, 270*degrees)
        cr.close_path()
        cr.fill()

    def _check_input(self, key_pressed):
        close = False
        if keyval_name(key_pressed) == 'BackSpace':
            self.search.pop()
        elif keyval_name(key_pressed) == 'Return':
            best_guess_pos = self.search.best_guess()[0]
            if best_guess_pos:
                secured_clipboard(self.ring.get_password(best_guess_pos))
                close = True
        elif keyval_name(key_pressed) == 'space':
            if len(self.search.string) > 0:
                # TODO unsecured memory
                pw, phonetic = self.pw_engine.create_passwords()[0]
                self.ring.save_password(pw
                                       ,searchable=self.search.string
                                       ,phonetic=phonetic)
                secured_clipboard(pw)
                close = True
        elif keyval_name(key_pressed) == 'Escape':
            close = True
        elif key_pressed < 256 and key_pressed > 32:
            self.search.push(chr(key_pressed))
        return close
                
    def _redraw_left_frame(self, widget, key_pressed):
        cr = widget.window.cairo_create()
        self._inside_frame(cr, 11)
        cr.set_source_rgb(1, 1, 1)
        cr.select_font_face("Monospace")
        cr.set_font_size(26.0)
        cr.move_to(25, 51)
        cr.set_source_rgb(1, 1, 1)
        for i,c in enumerate(self.search.string):
            if len(self.search.candidate_keys) == 0:
                cr.set_source_rgb(1, .1, .1)
            cr.show_text(c)
        cr.stroke()
    
    def _redraw_right_frame(self, widget, key_pressed):
        cr = widget.window.cairo_create()
        self._inside_right_frame(cr)

    def key_pressed(self, widget, event):
        if not self._check_input(event.keyval):
            self._redraw_left_frame(widget, event.keyval)
            self._redraw_right_frame(widget, event.keyval)
        else:
            self.emit("copied-event")
