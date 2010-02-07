import sys

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

##@defgroup TypeChecker Decorator for type checking function arguments.
# @brief The TypeChecker module provides a decorator, require, to check the validity
# of arguments to a Python function.
#
# @author Siddhu Warrier (siddhuwarrier@gmail.com)  
# @date 17/01/2010

__all__ = ["require"]

## @brief Decorator for type checking.
# 
# This method performs type checking for Python function arguments.
# This code is modified from Per Vognsen's ActiveState recipe 454322
# http://code.activestate.com/recipes/454322/
# Vognsen's code has been cleaned up and modified in order to 
# support checking multiple kwargs.
# It also performs checks as to whether the kwarg provided is valid.
#
# Example:
# @code
#from sidutils.TypeChecker import require
#
#@require(validKwargs = ['z'], x = int, y = (int, float), z = str) #x can only be int, y can be int or float.
#def foo(x, y, **kwargs):
#        pass
#if __name__ == "__main__":
#    foo(3,5.6) #will work
#    foo(3, 5) #will work
#    foo(x = 3, y = 5) #will work
#    try:
#        foo(x = "string", y = 2) #TypeError
#    except TypeError as typeError:
#        print typeError.args[0]
#    foo(x = 23, y = 5, z = "ss") #will work
#    foo(23, 5, z = "superman") #will work
#    try:
#        foo(5,5, m = "xd") #NameError
#    except NameError as nameError:
#        print nameError.args[0]
# @endcode
#
# @ingroup TypeChecker
# @param validKwargs (list): The list of valid keyword arguments for the method/function being
# decorated.
# @param kwargsCompulsory (boolean): Set to indicate whether the function's keyword arguments 
# (in validKwargs) should be compulsory or not. Default: False.
# @param typeMap (dictionary of tuples/strings): The typemap is a dictionary of the argument names
# for which we want to perform type checking. Each key specifies the acceptable type(s) for the 
# argument specified in the key. If there is more than one type, the key contains a tuple; if not,
# it may contain either a tuple or a string. 
# @throws NameError When argument invalid, or required argument not found.
# @throws TypeError When argument type does not match argument type expected.
# @author Siddhu Warrier (siddhuwarrier@gmail.com)
# @date 17/01/2010
def require(validKwargs, kwargsCompulsory = False, **typeMap):
    def makeWrapper(functionName):
        #when functionName is the function to decorate
        if hasattr(functionName, "wrapped_args"):
            print functionName, "has attr wrapped_args:", getattr(functionName, "wrapped_args")
            wrapped_args = getattr(functionName, "wrapped_args")
            
        #when functionName is the nested wrapper function.
        else:
            code = functionName.func_code
            wrapped_args = list(code.co_varnames[:code.co_argcount]) #adds everything except kwargs
            #print wrapped_args
            if 'args' in functionName.func_code.co_varnames:
                sys.stderr.write("Warning: Variable length args cannot be type-checked.")

        #wrapper function
        def wrapper(*args, **kwargs):
            for kwArgName in kwargs.keys():
                #remember, we can specify the positional arguments as kwargs as well.
                if kwArgName not in validKwargs and kwArgName not in wrapped_args:
                    validKwargList = " or ".join(str(validKwarg) for validKwarg in validKwargs)
                    raise NameError, "Invalid keyword argument %s. \
                    Supported keyword arguments (not inclusive of the positional arguments): %s."\
                    %(kwArgName, validKwargList)
                if kwArgName not in wrapped_args:
                    wrapped_args.append(kwArgName)
            
            errorMsg = "Expected '%s' to be %s; was %s."
            for argumentNameToCheck in typeMap.keys():
                #get the argument index
                try:
                    argIdx = wrapped_args.index(argumentNameToCheck)
                except ValueError:
                    if argumentNameToCheck in validKwargs and kwargsCompulsory == False:
                        print "Warning: Cannot find keyword argument %s.\n"%argumentNameToCheck
                        continue
                    else:
                        raise NameError, "Cannot find argument %s."%argumentNameToCheck
                
                #define the error message
                try:
                    typeList = " or ".join(str(allowedType) for allowedType in typeMap[argumentNameToCheck])
                except TypeError: #if there is only one argument, it does not have to be a tuple.
                    typeList = typeMap[argumentNameToCheck]
                
                #first check the positional arguments
                if len(args) > argIdx:
                    arg = args[argIdx]
                else: #check if it is a keyword argument
                    #if in keyword args, run the check
                    try:
                        arg = kwargs[argumentNameToCheck]
                    except:
                        raise NameError, "Compulsory argument %s missing."\
                        %argumentNameToCheck
                
                raiseTypeError = True #raise type error unless we are able to match
                #the type of the arg to the allowed types
                try: #we assume we have multiple allowable types for each entry. 
                    for allowedType in typeMap[argumentNameToCheck]:
                        #can be done: make this more permissive.
                        if isinstance(arg, allowedType):
                            raiseTypeError = False
                            break
                except TypeError: #the typeMap[argumentNameToCheck is not a tuple;
                    #i.e., it has only one entry
                    if isinstance(arg, typeMap[argumentNameToCheck]):
                        raiseTypeError = False
                
                #if none of the allowed types matched, then sod it, raise a TypeError
                if raiseTypeError:
                    raise TypeError, errorMsg%(str(argumentNameToCheck), typeList, type(arg))
                
            #remove all the optional keyword arguments for if another instance of the same class is instantiated
            #the other arguments are added in when the class is first read by the interpreter.
            for kwargName in validKwargs:
                if kwargName in wrapped_args:
                    wrapped_args.remove(kwargName)
                      
                        
            #call the function and return
            return functionName(*args, **kwargs)
        #return from make_wrapper
        return wrapper
    #return from require
    return makeWrapper
