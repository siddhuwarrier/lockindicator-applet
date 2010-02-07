# Copyright (c) 2010 Siddhu Warrier (http://siddhuwarrier.homelinux.org, 
# siddhuwarrier AT gmail DOT com). 
# 
# This file is part of the typeutils package.
# The utils package is free software: you can redistribute it and/or modify
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

##@mainpage 
# @brief <b>typeutils</b>: Utilities that are useful in multiple projects, and defy description.
#
# This package contains (as of now):
# \li A decorator that performs type-checking for Python functions (and instance methods).
# \li A bunch of user-defined exceptions, as Python's system errors weren't sufficient
# for my purposes.
# \li A simple XKB Wrapper sub-package, that wraps some C functions provided by the XKB library.
#
# @author Siddhu Warrier (siddhuwarrier@gmail.com)
# @date 31/01/2010

#all of the packages available.
__all__ = ['Exceptions', 'TypeChecker', 'XkbWrapper']

from Exceptions import *
from TypeChecker import *
