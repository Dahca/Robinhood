#! /usr/bin/python

def add_import_path():
  # This added the Robinhood package to the path so that modules from the root
  # directory and submodules can be imported when these examples are being run
  # in regular, non-package mode.
  from os import sys, path
  from os.path import dirname
  sys.path.append(dirname(dirname(dirname(path.abspath(__file__)))))

if __name__ != "__main__":
  add_import_path()
else:
  print("""
    The setup module contains some helper functions that are used in the
    example scripts that are in this directory. Try running those instead
    of this one!
  """)
