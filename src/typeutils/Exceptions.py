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

from errno import errorcode
import errno

##@defgroup Exceptions User-defined Exception classes
# @brief User-defined exceptions as Python's built-in exceptions are too few.
#
# This package contains several user-defined exception classes to supplement
# Python's all-too-few built-in exceptions.
# @author Siddhu Warrier (siddhuwarrier@gmail.com)  
# @date 10/01/2010

__all__ = ['FileError'] #to prevent inadvertent imports

## @brief Class for FileErrors.
#
# @ingroup Exceptions
# The different kinds of file errors are identified using
# the enumerators which use the errno.h numbers
# @param[in] errcode Error code which should be in the list of error codes in errno module.
# @param[in] strerror Human-readable string describing error.
# @author Siddhu Warrier (siddhuwarrier@gmail.com)  
# @date 10/01/2010
class FileError(Exception):
    ##@brief Constructor for FileError.
    # Gets the error code and strerror and builds a FileError message
    def __init__(self, errcode, strerror):
        if errcode not in errorcode.keys():
            raise Exception(errno.EINVAL, "FileError: Invalid Error Code")
        #set the exception args (errno, strerror)
        self.args = (errcode, "FileError: %s"%strerror)      
            