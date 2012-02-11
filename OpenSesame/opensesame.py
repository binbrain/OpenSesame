#!/usr/bin/env python

import gtk
import keybinder

from OpenSesame.gui.searchpopup import SearchPopup
from OpenSesame.searchable import Searchable
from OpenSesame.keyring import OpenKeyring
import OpenSesame.password as pw_engine

class Launcher(object):
    
    window = None

    def popup(self):
        ring = OpenKeyring()
        search = Searchable(ring.get_position_searchable())
        if self.window:
            self.window.do_destroy(self.window)
        self.window = SearchPopup(search, ring, pw_engine)
        def showit():
            self.window.present()
            self.window.grab_focus()
        gtk.idle_add(showit)

def main():
    launcher = Launcher()
    keybinder.bind("<Ctrl>k", launcher.popup)
    gtk.main()

if __name__  == "__main__":
    main()
