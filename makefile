all: 
	echo "No need to compile anything, to install run make install"


#################################### INSTALL ###################################
# This install is only for dev use currently, it requires that the amassite    #
# script stay where it is. In the future the python script and all of it's     #
# files will be moved to a local directory that will not be touched by the     #
# user                                                                         #
################################################################################
install:
	ln -s $(CURDIR)/source/amassite.py /usr/bin/amassite

################################### UNINSTALL ##################################
# The uninstall function removes the symlink that the install function created #
################################################################################
uninstall:
	rm /usr/bin/amassite