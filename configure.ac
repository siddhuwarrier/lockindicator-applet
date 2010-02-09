#configure.ac file for lockindicator-applet
AC_INIT(lockindicator-applet, version-1.0.0)
AC_SUBST(VERSION, version-1.0.0)
#check for python version 2.6. setup.py does this check as well
#but this will tell us where python is located. This is useful for
#the makefile
AM_PATH_PYTHON([2.6])


######### USER OPTIONS ################
#check if the user specifies a specific Doxygen config file
AC_ARG_ENABLE(deb-install, 
	[  --enable-deb-install         Enable Debian-style Python installs (into dist-packages).])
#check if the user specifies the caps lock mask
AC_ARG_WITH(capslock-mask, 
	[  --with-capslock-mask         Specify Caps Lock mask if different from default.])
#check if the user specifies the num lock mask
AC_ARG_WITH(numlock-mask, 
	[  --with-numlock-mask         Specify Num Lock mask if different from default.])
AC_ARG_ENABLE(doxygen-gen, 
	[  --disable-doxygen-gen         Disable Doxygen-style comment generation.])

########OPTION CHECKING##############
#check if the deb-install flag has been enabled.
if test "$enable_deb_install" == "yes"
then
	AC_MSG_NOTICE([Enabling debian install...])
	AC_SUBST(DEBIAN_FLAG, "--install-layout=deb")
else
	AC_SUBST(DEBIAN_FLAG, "")
fi 

if test "$enable_doxygen_gen" == "no"
then
	AC_MSG_NOTICE([Disabling Doxygen doc generation...])
	#add the data files such that doxygen docs are missing
	AC_SUBST(DATA_FILES, ["[
                    ('share/doc/lockindicator-applet/',['COPYING', 
                                               'README', 'NEWS', 'AUTHORS']), #documentation
                    ('share/lockindicator-applet/',['share/lockindicator-applet/CapsLockIndicator-OFF.png', 
                    'share/lockindicator-applet/CapsLockIndicator-ON.png', 'share/lockindicator-applet/NumLockIndicator.png']), #images
             		('/usr/lib/bonobo/servers',['servers/LockIndicatorApplet.server']) #the server.
             		#wont work unless it is in /usr/lib/bonobo/servers                                               
                    ]"])
     #add the build dependencies such that doxygen is missing
     AC_SUBST(BUILD_DEPS, "")
else
	#check for doxygen program
	AC_PATH_PROG([DOXYGEN_BINARY], [doxygen])
	AC_SUBST(DATA_FILES, ["[
                    ('share/doc/lockindicator-applet/',['doxygen-docs/latex/refman.pdf', 'COPYING', 
                                               'README', 'NEWS', 'AUTHORS']), #documentation
                    ('share/lockindicator-applet/',['share/lockindicator-applet/CapsLockIndicator-OFF.png', 
                    'share/lockindicator-applet/CapsLockIndicator-ON.png', 'share/lockindicator-applet/NumLockIndicator.png']), #images
             		('/usr/lib/bonobo/servers',['servers/LockIndicatorApplet.server']) #the server.
             		#wont work unless it is in /usr/lib/bonobo/servers                                               
                    ]"])
	AC_SUBST(BUILD_DEPS, "doxygen build-docs")
fi

#check if the user has specified a cpas lock mask.
if test "$with_capslock_mask" == "yes"
then
	AC_MSG_ERROR([Please specify value of Caps Lock mask.])
elif test "$with_capslock_mask" != ""
then
	AC_SUBST(CAPS_LOCK_MASK, $with_capslock_mask)
else
	AC_SUBST(CAPS_LOCK_MASK, "0x01")
fi

#check if the user has specified a num lock mask
if test "$with_numlock_mask" == "yes"
then
	AC_MSG_ERROR([Please specify value of Num Lock mask.])
elif test "$with_numlock_mask" != ""
then
	AC_SUBST(NUM_LOCK_MASK, $with_capslock_mask)
else
	AC_SUBST(NUM_LOCK_MASK, "0x02")
fi

#check if the user has specified a prefix
if test "$prefix" != NONE
then
	AC_SUBST(PREFIX_FLAG, "--prefix="$prefix)
	if test "$prefix" == "/usr/local"
	then
		AC_SUBST(PY_PKG_DIR, $prefix"/lib/python"$PYTHON_VERSION"/dist-packages")
	elif test "$enable_deb_install" == "yes"
	then
		AC_SUBST(PY_PKG_DIR, $prefix"/lib/python"$PYTHON_VERSION"/dist-packages")
	else
		AC_SUBST(PY_PKG_DIR, $prefix"/lib/python"$PYTHON_VERSION"/site-packages")
	fi
else
	AC_SUBST(PREFIX_FLAG, "")
	AC_SUBST(PY_PKG_DIR, "/usr/local/lib/python"$PYTHON_VERSION"/dist-packages")
fi

#substituted flags for Make.

#output all of this into Makefile.in, producing Makefile.
AC_OUTPUT(Makefile)
#produce setup.py
AC_OUTPUT(setup.py)
AC_OUTPUT(src/applet/Constants.py)
AC_OUTPUT(servers/LockIndicatorApplet.server)
