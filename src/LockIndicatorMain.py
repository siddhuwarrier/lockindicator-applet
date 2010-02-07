#! /usr/bin/env python

# Copyright (c) 2010 Siddhu Warrier (http://siddhuwarrier.homelinux.org, 
# siddhuwarrier AT gmail DOT com). 
# 
# This file is part of the lockindicator-applet package.
# The lockindicator-applet package is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# Thank you for using free software!

##@mainpage lockindicator-applet
#
# A wee GNOME applet to indicate when the Caps and Num Lock keys are on. This
# is an alpha which doesn't show Num lock status. Also, the icons are very naff
# If you think  you do me better icons, please please please get in touch.
#
# @defgroup LockIndicatorMain Main Module for the LockIndicator Applet.
# @author Siddhu Warrier (siddhuwarrier@gmail.com)  
# @date 06/02/2010

#imports
import sys

import pygtk
pygtk.require("2.0")
import gtk
import gnomeapplet

from applet import LockIndicator        

##@brief Gnome Panel Applet factory, gets the panel up and running.
# @ingroup LockIndicatorMain
# @author Siddhu Warrier (siddhuwarrier@gmail.com)
# @date 05/02/2010
def lockIndicator_factory(applet, iid):   
    LockIndicator(applet, iid)
    return True

##@brief the main function where program execution starts.
#
# This function can be used to execute the program either as  a GTK application
# or as an applet. For the former, please use the argument run-in-window
# 
# @ingroup LockIndicatorMain
# @author Siddhu Warrier (siddhuwarrier@gmail.com)
# @date 06/02/2010
def main():
    if len(sys.argv) == 2:
        if sys.argv[1] == "run-in-window":
            mainWindow = gtk.Window(gtk.WINDOW_TOPLEVEL)
            mainWindow.set_title("Ubuntu System Panel")
            mainWindow.connect("destroy", gtk.main_quit)
            applet = gnomeapplet.Applet()
            lockIndicator_factory(applet, None)
            applet.reparent(mainWindow)
            mainWindow.show_all()
            gtk.main()
            sys.exit()
    else:
        gnomeapplet.bonobo_factory('OAFIID:LockIndicatorApplet_Factory', 
                                   gnomeapplet.Applet.__gtype__, 
                                   'Lock Indicator Applet', '0.1', 
                                   lockIndicator_factory)

if __name__ == '__main__':
    #start the main function
    main()
