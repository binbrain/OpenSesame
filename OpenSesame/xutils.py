"""
Utilities to assist with desktop related tasks
"""

import wnck
import gtk
import glib
import subprocess

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

def secured_clipboard(item):
    """This clipboard only allows 1 paste 
    """
    def set_text(clipboard, selectiondata, info, data):
        selectiondata.set_text(item.get_secret())
        clipboard.clear()
    def clear(clipboard, data):
        #TODO verify buffer is empty
        pass
    targets = [ ("STRING", 0, 0),
              ("TEXT", 0, 1),
              ("COMPOUND_TEXT", 0, 2),
              ("UTF8_STRING", 0, 3) ]
    cp = gtk.clipboard_get()
    cp.set_with_data(targets, set_text, clear)
        
def get_active_window():
    """Get the currently focused window
    """
    active_win = None
    default = wnck.screen_get_default()
    while gtk.events_pending():
        gtk.main_iteration(False)
    window_list = default.get_windows()
    if len(window_list) == 0:
        print "No Windows Found"
    for win in window_list:
        if win.is_active():
            active_win = win.get_name()
    return active_win

def paste(active_win):
    paste_cmd = 'ctrl+v'
    xdo_cmd = 'xdotool search "%s" windowactivate --sync key --clearmodifiers %s'
    p = subprocess.Popen(xdo_cmd % (active_win, paste_cmd)
                        ,stdout=subprocess.PIPE 
                        ,stderr=subprocess.PIPE
                        ,shell=True)
    output, errors = p.communicate()
