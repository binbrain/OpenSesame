#!/usr/bin/env python

import gtk
import gobject
import keybinder

from OpenSesame.gui.searchpopup import SearchPopup
from OpenSesame.gui.unlocked import KeyFade
from OpenSesame.xutils import paste
from OpenSesame.xutils import get_active_window
from OpenSesame.searchable import Searchable
from OpenSesame.keyring import OpenKeyring
import OpenSesame.password as pw_engine


class Launcher(gobject.GObject):
    def __init__(self):
        self.__gobject_init__()
        gobject.signal_new("copied-event", SearchPopup, gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, ())

    def copied_to_buffer(self, widget):
        widget.hide()
        widget.destroy()
        paste(self.active_win)
        self.emit("pasted-event")

    def do_keyfade(self, widget):
        def showit():
            self.keyfade = KeyFade(self.active_win)
            self.keyfade.present()
        gtk.idle_add(showit)

    def popup(self):
        self.active_win = get_active_window()[0:20]
        ring = OpenKeyring()
        search = Searchable(ring.get_position_searchable())
        def showit():
            self.popup = SearchPopup(search, ring, pw_engine)
            self.popup.connect("copied-event", self.copied_to_buffer)
            self.popup.present()
        gtk.idle_add(showit)

def main():
    launcher = Launcher()
    gobject.signal_new("pasted-event", Launcher, gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, ())
    launcher.connect("pasted-event", launcher.do_keyfade)
    keybinder.bind("<Ctrl>k", launcher.popup)
    gtk.main()

if __name__  == "__main__":
    main()
