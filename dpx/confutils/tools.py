#!/usr/bin/env python
##############################################################################
#
# dpx.pdfgetxgui    by Simon J. L. Billinge group
#                   (c) 2012 Trustees of the Columbia University
#                   in the City of New York.  All rights reserved.
#
# File coded by:    Xiaohao Yang
#
# See AUTHORS.txt for a list of people who contributed.
# See LICENSE.txt for license information.
#
##############################################################################

import numpy as np
import re

def _configPropertyRad(nm):
    '''helper function of options delegation, rad 2 degree'''
    rv = property(fget = lambda self: np.radians(getattr(self, nm)), 
                  fset = lambda self, val: setattr(self, nm, np.degrees(val)), 
                  fdel = lambda self: delattr(self, nm))
    return rv

def _configPropertyR(name):
    '''Create a property that forwards self.name to self.config.name.
    '''
    rv = property(fget = lambda self: getattr(self.config, name),
            doc='attribute forwarded to self.config, read-only')
    return rv

def _configPropertyRW(name):
    '''Create a property that forwards self.name to self.config.name.
    '''
    rv = property(fget = lambda self: getattr(self.config, nm), 
                  fset = lambda self, value: setattr(self.config, nm, value),
                  fdel = lambda self: delattr(self, nm),
                  doc='attribute forwarded to self.config, read/write')
    return rv

def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")

def opt2Str(opttype, optvalue):
    '''trun the value of one option to string, according to the option type
    list of values are truned into "value1, value2, value3..."
    
    param opttype: string, type of opitons, for example 'str' or 'intlist'
    param optvalue: value of the option
    
    return: string, stored in ConfigBase.config
    '''
    
    if opttype.endswith('list'):
        rv = ', '.join(map(str, optvalue))
    else:
        rv = str(optvalue)
    return rv

def StrConv(opttype):
    '''get the type (or converter function) according to the opttype
    
    the function don't care the list 
    '''
    if opttype.startswith('str'):
        conv = str
    elif opttype.startswith('int'):
        conv = int
    elif opttype.startswith('float'):
        conv = float
    elif opttype.startswith('bool'):
        conv = str2bool
    else:
        conv = None
    return conv

def str2Opt(opttype, optvalue):
    '''convert the string to value of one option, according to the option type
    
    param opttype: string, type of opitons, for example 'str' or 'intlist'
    param optvalue: string, value of the option
    
    return: value of the option stored in ConfigBase.config
    '''
    #base converter
    conv = StrConv(opttype)
    if opttype.endswith('list'):
        temp = re.split('\s*,\s*', optvalue)
        rv = map(conv, temp) if len(temp)>0 else []
    else:
        rv = conv(optvalue)
    return rv