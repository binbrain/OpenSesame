#!/usr/bin/env python

from setuptools import setup

setup(name='OpenSesame',
      version='0.1',
      description='Password management made simple and secure in GNOME',
      author='Jim Pharis',
      author_email='binbrain@gmail.com',
      url='http://github.com/binbrain/OpenSesame',
      entry_points={'console_scripts':
                    ['opensesame=OpenSesame.opensesame:main',
                     'opensesame-manager=OpenSesame.manager:main']                    
                    },
      packages=['OpenSesame', 'OpenSesame.gui'],
      include_package_data=True,
      data_files=[('OpenSesame/gui/', ['OpenSesame/gui/key.png'])],
      zip_safe=True)
