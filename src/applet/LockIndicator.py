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

import pygtk
pygtk.require("2.0")

import gtk
import keybinder
import pynotify
from xkb import XkbWrapper
from Constants import CAPS_LOCK_MASK, INSTALL_PREFIX

__all__ = ['LockIndicator']

## @brief Class to keep track of whether the Caps and Num locks are on.
# @ingroup LockIndicatorApplet
# @author Siddhu Warrier (siddhuwarrier@gmail.com)
# @date 02/02/2010
class LockIndicator:
    
    ## @brief LockIndicator constructor. 
    # 
    # @date 03/02/2010
    def __init__(self, applet = None, iid = None):
        self.applet = applet
        #self.applet.connect("destroy", self.cleanup)
        #Add an indicator in, and add it to the applet
        #TODO Have the icon resize with panel size changes.
        self.lockIndicatorIcon = gtk.Image()
        self.applet.add(self.lockIndicatorIcon)
        self.applet.show_all()        
        
        #connect the Caps and Num Lock key to a class method
        keybinder.bind("Caps_Lock", self.capsLockPressed)
        #keybinder.bind("Num_Lock", self.capsLockPressed)
        
        #create a notifier to display info.
        #we shall use two separate notifiers; one each for the caps and num lock keys. 
        pynotify.init("lockindicator-applet")
        self.capsLockNotifier = pynotify.Notification("Caps Lock ON", "Your Caps Lock key is on.")
        #TODO Add numLockNotifier. My laptop kb doesn't have NumLock, so I can't test it.
        
        #set up the XKB Wrapper and get the display info
        self.xkbWrapper = XkbWrapper()
        try:
            displayInfo = self.xkbWrapper.openDisplayAndInitXkb(None, 1, 0)
        except OSError as osError:
            print osError.args[0]
        
        self.displayHandle = displayInfo['display_handle']
        self.deviceSpec = self.xkbWrapper.constants_xkb['XkbUseCoreKbd']
        
        #execute capsLockPressed so as to reset everything.
        self.capsLockPressed()

    ## @brief listener method called by keybinder when caps lock key pressed 
    # 
    # @date 03/02/2010            
    def capsLockPressed(self):
        mask = self.xkbWrapper.getIndicatorStates(self.displayHandle, self.deviceSpec).value
        #use bitwise arithmetic to check if the Caps Lock key is on.
        if mask & CAPS_LOCK_MASK:
            print "%s/share/lockindicator-applet/CapsLockIndicator-ON.png"%INSTALL_PREFIX
            self.lockIndicatorIcon.set_from_file("%s/share/lockindicator-applet/CapsLockIndicator-ON.png"%INSTALL_PREFIX)            
            self.lockIndicatorIcon.show()
            self.capsLockNotifier.update("Caps Lock ON", "Your Caps Lock key is on.")
            self.capsLockNotifier.show()
        else:
            self.lockIndicatorIcon.set_from_file("%s/share/lockindicator-applet/CapsLockIndicator-OFF.png"%INSTALL_PREFIX)
            self.capsLockNotifier.update("Caps Lock OFF", "Your Caps Lock key is off.")
            self.capsLockNotifier.show()
            