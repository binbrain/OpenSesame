"""
Security related utils
"""

import os

def lookup_path(bin_name):
    """Calls to external binaries can't depend on $PATH
    """
    paths = ('/usr/local/sbin/', '/usr/local/bin/', '/usr/sbin/', '/usr/bin/')
    for p in paths:
        fq_path = p + bin_name
        found = os.path.isfile(fq_path) and os.access(fq_path, os.X_OK)
        if found:
            return fq_path
    return False
