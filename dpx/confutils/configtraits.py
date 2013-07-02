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

'''package for organizing program configurations. It can read/write configurations file, 
parse arguments from command lines, and also parse arguments passed from method/function calling
inside python. 

Note: for python 2.6, argparse and orderedDict is required, install them with easy_install
'''

import ConfigParser
import re
import os
import sys
from functools import partial
import argparse
from collections import OrderedDict

from traits.api import Directory, String, List, Enum, Bool, File, Float, Int, \
                        HasTraits, Property, Range, cached_property, Str, Instance, Array,\
                        Event, CFloat, CInt, on_trait_change
from traitsui.api import Item, Group, View

from dpx.confutils.tools import _configPropertyRad, _configPropertyR, _configPropertyRW, \
                                str2bool, opt2Str, str2Opt, StrConv
from dpx.confutils.config import ConfigBase

class ConfigBaseTraits(HasTraits, ConfigBase):
    '''_optdatalistdefault, _optdatalist are metadata used to initialize the options, see below for examples
    
    options presents in --help (in cmd), config file, and headers have the same order in there three list, so arrange them 
    in right order here. 
    
    optional args to control if the options presents in args, config file or file header: 
        'args': default is 'a'
            if 'a', this option will be available in self.args
            if 'n', this option will not be available in self.args
        'config': default is 'a'
            if 'f', this option will present in self.config and be written to config file only in full mode
            if 'a', this option will present in self.config and be written to config file both in full and short mode
            if 'n', this option will not present in self.config
        'header', default is 'a'
            if 'f', this option will be written to header only in full mode
            if 'a', this option will be written to header both in full and short mode
            if 'n', this option will not be written to header
        so in short mode, all options with 'a' will be written, in full mode, all options with 'a' or 'f' will be written
    '''
    
    # Text to display before the argument help
    _description = \
    '''Description of configurations
    ''' 
    # Text to display after the argument help
    _epilog = \
    '''
    '''
    
    '''optdata contains these keys, see argparse for corresponding keys 
    'f': full, (positional)
    's': short
    'h': help, traits desc information
    't': type
    'a': action
    'n': nargs
    'd': default
    'c': choices
    'r': required
    'de': dest
    'co': const
    
    additional options for traits:
    'tt': traits type
    'l': traits label
    '''
    _optdatanamedict = {'h':'help',
                       't':'type',
                       'a':'action',
                       'n':'nargs',
                       'd':'default',
                       'c':'choices',
                       'r':'required',
                       'de':'dest',
                       'co':'const'}
    _traitstypedict = {
            'str': String,
            'int': CInt,
            'float': CFloat,
            'bool': Bool,
            'file': File,
            'directory': Directory,
            'strlist':List,
            'intlist':List,
            'floatlist':List,
            'boollist':List,
            'array':Array,
            }
    
    #examples, overload it
    _optdatalist_default = [
        ['configfile',{'sec':'Control', 'config':'f', 'header':'n',
            'l':'Config File',
            'tt':'file',
            's':'c',
            'h':'name of input config file',
            'd':'',}],
        ['createconfig',{'sec':'Control', 'config':'n', 'header':'n',
            'h':'create a config file according to default or current values',
            'd':'',}],
        ['createconfigfull',{'sec':'Control', 'config':'n', 'header':'n',
            'h':'create a full configurable config file',
            'd':'',}],
        ]
    #examples, overload it
    _optdatalist = [
        ['tifdirectory',{'sec':'Experiment', 'header':'n',
            'tt':'directory',
            'l':'Tif directory',
            's':'tifdir',
            'h':'directory of raw tif files',
            'd':'currentdir',}],
        ['integrationspace',{'sec':'Experiment',
            'l':'Integration space',
            'h':'integration space, could be twotheta or qspace',
            'd':'twotheta',
            'c':['twotheta','qspace'],}],
        ['wavelength',{'sec':'Experiment',
            'l':'Wavelength',
            'h':'wavelength of x-ray, in A',
            'd':0.1000,}],
        ['rotationd',{'sec':'Experiment',
            'l':'Tilt Rotation',
            's':'rot',
            'h':'rotation angle of tilt plane, in degree',
            'd':0.0,}],
        ['includepattern',{'sec':'Beamline','header':'n','config':'f',
            'l':'Include',
            's':'ipattern',
            'h':'file name pattern for included files',
            'n':'*',
            'd':['*.tif'],}],
        ['excludepattern',{'sec':'Beamline','header':'n','config':'f',
            'l':'Exclude',
            's':'epattern',
            'h':'file name pattern for excluded files',
            'n':'*',
            'd':['*.dark.tif', '*.raw.tif'],}],
        ['fliphorizontal',{'sec':'Beamline','header':'n','config':'f',
            'l':'Filp horizontally',
            'h':'filp the image horizontally',
            'n':'?',
            'co':True,
            'd':False,}],
        ['maskedges',{'sec':'Others','config':'f',
            'tt':'array',
            'l':'Mask edges',
            'h':'mask the edge pixels, first four means the number of pixels masked in each edge \
                (left, right, top, bottom), the last one is the radius of a region masked around the corner',
            'n':5,
            'd':[10,10,10,10,100],}],
        ]
    
    #default config file path and name
    _defaultdata = {'configfile': ['config.cfg'],
                    'headertitle': 'Configuration information' 
                    }
    
    def __init__(self, filename=None, args=None, **kwargs):
        HasTraits.__init__(self)
        ConfigBase.__init__(self, filename, args, **kwargs)
        
        self._postInitTraits()
        return
    
    def _postInitTraits(self):
        '''additional init process called after traits init
        '''
        return
    
    @classmethod
    def _addOptSelfC(cls, optname, optdata):
        #value type
        vtype = cls._getTypeStrC(optname)
        ttype = optdata.get('tt', vtype)
        ttype = cls._traitstypedict[ttype]
        kwargs = {'label':optdata['l'] if optdata.has_key('l') else optname, 
                  'desc':optdata['h'],
                  }
        args = [optdata['d']]
        if optdata.has_key('c'):
            ttype = Enum
            args = [optdata['c']]
            kwargs['value']=optdata['d']
        if ttype == Array:
            args = []
            kwargs['value']=optdata['d']
        obj = ttype(*args, **kwargs)
        cls.add_class_trait(optname, obj)
        return
    
    @classmethod
    def _additionalInitConfigClass(cls):
        '''additional method called in initConfigClass, overload it
        '''
        #obj = Property(fget = lambda self: np.radians(self.tiltd),
        #               fset = lambda self, val: setattr(self, 'rotationd', np.degrees(val)),
        #               depends_on='rotationd')
        #PDFliveConfig.add_class_trait('rotation', obj)
        return

#ConfigBaseTraits.initConfigClass()    

if __name__=='__main__':
    test = ConfigBaseTraits(filename='temp.cfg')
    test.updateConfig()
    test.configure_traits()
