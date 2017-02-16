# (c) 2016 Open Source Geospatial Foundation - all rights reserved
# (c) 2014 - 2015 Centre for Maritime Research and Experimentation (CMRE)
# (c) 2013 - 2014 German Aerospace Center (DLR)
# This code is licensed under the GPL 2.0 license, available at the root
# application directory.

__author__ = "Alessio Fabiani"
__copyright__ = "Copyright 2016 Open Source Geospatial Foundation - all rights reserved"
__license__ = "GPL"

#todo: one arg, two arg, etc is really ugly => find more pythoninc way

def get_class_no_arg( class_name ):
    parts = class_name.split('.')
    module = parts[0]
    m = __import__( module )
    for comp in parts[1:]:
        m = getattr(m, comp)         
    return m()

def get_class_one_arg( class_name, par1 ):
    parts = class_name.split('.')
    module = parts[0]
    m = __import__( module )
    for comp in parts[1:]:
        m = getattr(m, comp)
    return m(par1)

def get_class_two_arg( class_name, par1, par2 ):
    parts = class_name.split('.')
    module = parts[0]
    m = __import__( module )
    for comp in parts[1:]:
        m = getattr(m, comp)
    return m(par1, par2)

def get_class_three_arg( class_name, par1, par2, par3 ):
    parts = class_name.split('.')
    module = parts[0]
    m = __import__( module )
    for comp in parts[1:]:
        m = getattr(m, comp)
    return m(par1, par2, par3)

def get_class_four_arg( class_name, par1, par2, par3, par4 ):
    parts = class_name.split('.')
    module = parts[0]
    m = __import__( module )
    for comp in parts[1:]:
        m = getattr(m, comp)
    return m(par1, par2, par3, par4)