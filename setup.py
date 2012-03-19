#!/usr/bin/env python

from setuptools import setup
import os

README = os.path.join(os.path.dirname(__file__), "README")

setup(name="OpenSesame",
      version="1.0",
      description="Password management made simple and secure in GNOME",
      long_description=open(README).read()+"\n",
      author="Jim Pharis",
      author_email="binbrain@gmail.com",
      url="http://binbrain.github.com/OpenSesame/",
      entry_points={"console_scripts":
                    ["opensesame=OpenSesame.opensesame:main"]                    
                    },
      license="GPL",
      classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: X11 Applications :: Gnome",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Topic :: Desktop Environment :: Gnome",
        "Topic :: Security",
        "Topic :: Utilities"],
      packages=["OpenSesame", "OpenSesame.gui"],
      include_package_data=True,
      zip_safe=True)
      #data_files=[("OpenSesame/gui/", ["OpenSesame/gui/key.png"]),
      #            ("/etc/xdg/autostart/", ["opensesame.desktop"])],
