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

def get_active_window():
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
    xdotool_cmd = 'xdotool search "%s" windowactivate --sync  key --clearmodifiers ctrl+v' % active_win
    print xdotool_cmd
    p = subprocess.Popen(xdotool_cmd, stdout=subprocess.PIPE ,stderr=subprocess.PIPE, shell=True)
    output, errors = p.communicate()
    clip = gtk.clipboard_get()
    clip.clear()
    print output
    print errors
    print "buffer cleared"
