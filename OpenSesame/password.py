"""
Currently best option as-is for FIPS 181 automated password generator

TODO: implemented FIPS 181 in Python (or extend existing attempts)
"""

import subprocess

def create_passwords():
    pipe = subprocess.Popen(["apg", "-t"], stdout=subprocess.PIPE)
    options = list()
    for l in pipe.stdout.xreadlines():
        options.append(l.split())
    return options
