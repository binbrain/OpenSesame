"""
Currently best option as-is for FIPS 181 automated password generator

TODO: implement FIPS 181 in Python (or extend existing attempts)
"""

import subprocess

from OpenSesame.secureutils import lookup_path

def create_passwords():
    apg_bin = lookup_path('apg')
    pipe = subprocess.Popen([apg_bin, "-MNS"], stdout=subprocess.PIPE)
    options = list()
    for l in pipe.stdout.xreadlines():
        options.append(l)
    return options
