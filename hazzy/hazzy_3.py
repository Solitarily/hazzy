#!/usr/bin/env python

#   An attempt at a new UI for LinuxCNC that can be used
#   on a touch screen without any lost of functionality.
#   The code is written in python and glade and is almost a
#   complete rewrite, but was influenced mainly by Gmoccapy
#   and Touchy, with some code adapted from the HAL VCP widgets.

#   Copyright (c) 2017 Kurt Jacobson
#       <kurtcjacobson@gmail.com>
#
#   This file is part of Hazzy.
#
#   Hazzy is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   Hazzy is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with Hazzy.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys
import linuxcnc
import gi

gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject


# Setup paths to files
BASE = os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), ".."))
INIFILE = sys.argv[2]                               # Path to .ini file
CONFIGDIR = os.path.dirname(INIFILE)                # Path to config dir


# Path to TCL for external programs eg. halshow
if sys.argv[1] != "-ini":
    raise SystemExit, "-ini must be first argument{0}".format(TCLPATH=os.environ['LINUXCNC_TCL_DIR'])

# Get actual paths so we can run from any location
HAZZYDIR = os.path.dirname(os.path.realpath(__file__))
UIDIR = os.path.join(HAZZYDIR, 'ui')
MODULEDIR = os.path.join(HAZZYDIR, 'modules')
MAINDIR = os.path.dirname(HAZZYDIR)

# Set system path so we can find our own modules
if HAZZYDIR not in sys.path:
    sys.path.insert(1, HAZZYDIR)

# Import our own modules
from utilities import logger
log = logger.get('HAZZY')

from utilities import status
from modules.dro.dro import Dro


class LinuxCNC():

    def __init__(self):

        # UI setup
        gladefile = os.path.join(UIDIR, 'hazzy_3.ui')
        self.builder = Gtk.Builder()
        self.builder.add_from_file(gladefile)
        self.builder.connect_signals(self)

        self.window = self.builder.get_object('window')
        titlebar = self.builder.get_object('titlebar')
        self.window.set_titlebar(titlebar)

        btn = self.builder.get_object('btn1')

        self.dro = Dro()


        self.status = status.Status


        self.status.monitor('tool_in_spindle', self.test)
        self.status.monitor('tool_in_spindle', self.test2)
        self.status.monitor('g92_offset', self.g92)

        # Connect stat
        self.status.connect('update-axis-positions', self.update_position)
        self.status.connect('active-codes-changed', self.update_codes)

        self.window.show()

    def test(self, widget, data=None):
        pass

    def test2(self, widget, data=None):
        pass

    def g92(self, widget, data):
        pass

    def update_position(self, widget, pos, rel, dtg):
        label = self.builder.get_object('label')
        label.set_text(str(rel[1]))

    def update_codes(self, widget, gcodes, mcodes):
        print gcodes
        print mcodes


    def on_window_delete_event(self, widget, data=None):
        print "Quiting"
        Gtk.main_quit()


def main():
    Gtk.main()

if __name__ == "__main__":
    ui = LinuxCNC()
    main()