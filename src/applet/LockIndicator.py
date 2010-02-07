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
from Constants import *

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
        self.mask = 0x00 #the original mask. Neither caps nor num lock is on.
        self.applet = applet
        self.appletContainer = gtk.Table(1,2, True)
        #self.applet.connect("destroy", self.cleanup)
        #Add an indicator in, and add it to the applet
        #TODO Have the icon resize with panel size changes.
        self.capsLockIndicatorIcon = gtk.Image()
        self.capsLockIndicatorIcon.set_tooltip_text("Indicates the state of the Caps Lock key.")
        self.appletContainer.attach(self.capsLockIndicatorIcon,0,1,0,1)
        
        #set up the num lock icon
        self.numLockIndicatorIcon = gtk.Image()
        self.numLockIndicatorIcon.hide()
        self.numLockIndicatorIcon.set_tooltip_text("Num Lock key on.") 
        self.appletContainer.attach(self.numLockIndicatorIcon, 1,2,0,1)
        
        #create a notifier to display info.
        #we shall use one notifier because Ubuntu's notification system sucks.         
        pynotify.init("lockindicator-applet")
        self.lockNotifier = pynotify.Notification("None", "None") #random values.
        self.applet.add(self.appletContainer)
        self.applet.show_all()        
        
        #connect the Caps and Num Lock key to a class method
        keybinder.bind("Caps_Lock", self.lockPressed)
        keybinder.bind("Num_Lock", self.lockPressed)
        
        #set up the XKB Wrapper and get the display info
        self.xkbWrapper = XkbWrapper()
        try:
            displayInfo = self.xkbWrapper.openDisplayAndInitXkb(None, 1, 0)
        except OSError as osError:
            print osError.args[0]
        
        self.displayHandle = displayInfo['display_handle']
        self.deviceSpec = self.xkbWrapper.constants_xkb['XkbUseCoreKbd']
        
        #get the first starting state. Don't bother notification icons.
        self.mask = self.xkbWrapper.getIndicatorStates(self.displayHandle, self.deviceSpec).value
        if self.mask & CAPS_LOCK_MASK:
            self.capsLockIndicatorIcon.set_from_file("%s/share/lockindicator-applet/CapsLockIndicator-ON.png"
                                                         %INSTALL_PREFIX)
            self.capsLockIndicatorIcon.show()
        else:
            self.capsLockIndicatorIcon.set_from_file("%s/share/lockindicator-applet/CapsLockIndicator-OFF.png"
                                                         %INSTALL_PREFIX)
            self.capsLockIndicatorIcon.show()
        
        #do the same for num lock            
        if self.mask & NUM_LOCK_MASK:
            self.numLockIndicatorIcon.set_from_file("%s/share/lockindicator-applet/NumLockIndicator.png"
                                                    %INSTALL_PREFIX)
            self.numLockIndicatorIcon.show()
            
    ## @brief listener method called by keybinder when caps lock key pressed 
    # 
    # @date 03/02/2010            
    def lockPressed(self):
        mask = self.xkbWrapper.getIndicatorStates(self.displayHandle, self.deviceSpec).value
        bitChanged = mask ^ self.mask #find out which bit has changed since the last execution
        
        if bitChanged & CAPS_LOCK_MASK:
            if mask & CAPS_LOCK_MASK:
                self.capsLockIndicatorIcon.set_from_file("%s/share/lockindicator-applet/CapsLockIndicator-ON.png"
                                                         %INSTALL_PREFIX)
                self.capsLockIndicatorIcon.show()
                #now check the num lock state to know the relative positions of num and caps.
                if mask & NUM_LOCK_MASK:
                    self.lockNotifier.update("Caps Lock ON, Num Lock ON", 
                                                 "Your Caps Lock key was turned on.")
                else:
                    self.lockNotifier.update("Caps Lock ON, Num Lock OFF", 
                                                 "Your Caps Lock key was turned on.")
            else:
                self.capsLockIndicatorIcon.set_from_file("%s/share/lockindicator-applet/CapsLockIndicator-OFF.png"
                                                         %INSTALL_PREFIX)
                self.capsLockIndicatorIcon.show()
                #now check the num lock state to display whether num lock is on.
                if mask & NUM_LOCK_MASK:
                    self.lockNotifier.update("Caps Lock OFF, Num Lock ON", 
                                                 "Your Caps Lock key was turned off.")
                else:
                    self.lockNotifier.update("Caps Lock OFF, Num Lock OFF", 
                                                 "Your Caps Lock key was turned off.")
        #else if it is the num lock key that has been pressed.
        elif bitChanged & NUM_LOCK_MASK:
            if mask & NUM_LOCK_MASK:
                self.numLockIndicatorIcon.set_from_file("%s/share/lockindicator-applet/NumLockIndicator.png"%INSTALL_PREFIX)
                self.numLockIndicatorIcon.show()
                if mask & CAPS_LOCK_MASK:
                    self.lockNotifier.update("Caps Lock ON, Num Lock ON", 
                                                 "Your Num Lock key was turned on.")
                else:
                    self.lockNotifier.update("Caps Lock OFF, Num Lock ON", 
                                                 "Your Num Lock key was turned on.")
            else:
                self.numLockIndicatorIcon.hide()
                if mask & CAPS_LOCK_MASK:
                    self.lockNotifier.update("Caps Lock ON, Num Lock OFF", 
                                                 "Your Num Lock key was turned off.")
                else:
                    self.lockNotifier.update("Caps Lock OFF, Num Lock OFF", 
                                                 "Your Num Lock key was turned off.")                
        
        #show the notification
        self.lockNotifier.show()
        self.mask = mask #update self.mask with the previous mask value.
            