#!/usr/bin/env python
##############################################################################
#
# File coded by:    Xiaohao Yang
#
# See AUTHORS.txt for a list of people who contributed.
# See LICENSENOTICE.txt for license information.
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

from dpx.confutils.tools import _configPropertyRad, _configPropertyR, _configPropertyRW, \
                                str2bool, opt2Str, str2Opt, StrConv

class ConfigBase(object):
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
    'h': help
    't': type
    'a': action
    'n': nargs
    'd': default
    'c': choices
    'r': required
    'de': dest
    'co': const
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
    
    #examples, overload it
    _optdatalist_default = [
        ['configfile',{'sec':'Control', 'config':'n', 'header':'n',
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
            's':'tifdir',
            'h':'directory of raw tif files',
            'd':'currentdir',}],
        ['integrationspace',{'sec':'Experiment',
            'h':'integration space, could be twotheta or qspace',
            'd':'twotheta',
            'c':['twotheta','qspace'],}],
        ['wavelength',{'sec':'Experiment',
            'h':'wavelength of x-ray, in A',
            'd':0.1000,}],
        ['rotationd',{'sec':'Experiment',
            's':'rot',
            'h':'rotation angle of tilt plane, in degree',
            'd':0.0,}],
        ['includepattern',{'sec':'Beamline',
            's':'ipattern',
            'h':'file name pattern for included files',
            'n':'*',
            'd':['*.tif'],}],
        ['excludepattern',{'sec':'Beamline',
            's':'epattern',
            'h':'file name pattern for excluded files',
            'n':'*',
            'd':['*.dark.tif', '*.raw.tif'],}],
        ['fliphorizontal',{'sec':'Beamline',
            'h':'filp the image horizontally',
            'n':'?',
            'co':True,
            'd':False,}],
        ['regulartmatrixenable',{'sec':'Others',
            'h':'normalize tmatrix in splitting method',
            'n':'?',
            'co':True,
            'd':False,}],
        ['maskedges',{'sec':'Others', 'config':'f', 'header':'f',
            'h':'mask the edge pixels, first four means the number of pixels masked in each edge \
                (left, right, top, bottom), the last one is the radius of a region masked around the corner',
            'n':5,
            'd':[1,1,1,1,50],}],
        ]
    
    #default config file path and name
    _defaultdata = {'configfile': ['config.cfg'],
                    'headertitle': 'Configuration information' 
                    }
    

    def __init__(self, filename=None, args=None, **kwargs):
        '''init the class and update the values of options if specified in 
        filename/args/kwargs
        
        param filename: str, file name of config file
        param filename: list of str, args passed from cmd
        param kwargs: optional kwargs
        '''
        #call self._preInit
        self._preInit(**kwargs)
        
        #updata config, first detect if a default config should be load
        filename = self._findDefaultConfigFile(filename, args, **kwargs)
        rv = self.updateConfig(filename, args, **kwargs)
        return rv
    
    #example, overload it
    def _preInit(self, **kwargs):
        '''method called in init process, overload it!
        
        this method will be called after all options in self._optdata are processed, 
        i.e. all options are created and before reading config from file/args/kwargs
        '''
        for name in ['rotation']:
            setattr(self.__class__, name, _configPropertyRad(name+'d'))
        self._configlist['Experiment'].extend(['rotation'])
        return
    
    ###########################################################################
    
    def _findConfigFile(self, filename=None, args=None, **kwargs):
        '''find config file, if any config is specified in filename/args/kwargs
        then return the filename of config. 
        
        param filename: str, file name of config file
        param filename: list of str, args passed from cmd
        param kwargs: optional kwargs
        
        return: name of config file if found, otherwise None 
        '''
        rv = None
        if (filename!=None):
            rv = filename
        if (args!=None):
            if ('--configfile' in args) or ('-c' in args):
                obj = self.args.parse_args(pargs)
                rv = obj.configfile
        if kwargs.has_key('configfile'):
            flag = True
        return rv
    
    def _findDefaultConfigFile(self, filename=None, args=None, **kwargs):
        '''find default config file, if any config is specified in filename/args/kwargs
        or in self._defaultdata['configfile'], then return the filename of config. 
        
        param filename: str, file name of config file
        param filename: list of str, args passed from cmd
        param kwargs: optional kwargs
        
        return: name of config file if found, otherwise None 
        '''
        rv = self._findConfigFile(filename, args, **kwargs)
        if rv == None:
            for dconf in self._defaultdata['configfile']:
                if (os.path.exists(dconf))and(rv == None):
                    rv = dconf
        return rv
    
    ###########################################################################
        
    def _updateSelf(self, optnames=None, **kwargs):
        '''update the options value, then copy the values in the self.'options' to self.config
        param optnames: str or list of str, name of options whose value has been changed, if None, update all options
        '''
        #so some check right here
        self._preUpdataSelf(**kwargs)
        #copy value to self.config
        self._copySelftoConfig(optnames)
        #so some check right here
        self._postUpdataSelf(**kwargs)
        return
    
    #example, overload it
    def _preUpdataSelf(self, **kwargs):
        '''additional process called in self._updateSelf, this method is called before 
        self._copySelftoConfig(), i.e. before copy options value to self.config (config file)
        '''
        return
    
    def _postUpdataSelf(self, **kwargs):
        '''additional process called in self._updateSelf, this method is called before 
        self._copySelftoConfig(), i.e. before copy options value to self.config (config file)
        '''
        return
    
    ###########################################################################
    
    def _getTypeStr(self, optname):
        '''detect the type of option
        param optname: str, name of option
        
        return: string of type 
        '''
        opttype =self._getTypeStrC(optname)
        return opttype
    
    @classmethod
    def _getTypeStrC(cls, optname):
        '''detect the type of option 
        param optname: str, name of option
        
        return: string of type 
        '''
        optdata = cls._optdata[optname]
        if optdata.has_key('t'):
            opttype = optdata['t']
        else:
            value = optdata['d']
            if isinstance(value, str):
                opttype = 'str'
            elif isinstance(value, float):
                opttype = 'float'
            elif isinstance(value, int):
                opttype = 'int'
            elif isinstance(value, bool):
                opttype = 'bool'
            elif isinstance(value, list):
                if len(value)==0:
                    opttype = 'strlist'
                elif isinstance(value[0], str):
                    opttype = 'strlist'
                elif isinstance(value[0], float):
                    opttype = 'floatlist'
                elif isinstance(value[0], int):
                    opttype = 'intlist'
                elif isinstance(value[0], bool):
                    opttype = 'boollist'
        return opttype
    
    ###########################################################################
    
    def _detectAddSections(self):
        '''detect sections present in self._optdata and add them to self.config
        also add it to self._configlist
        '''
        self._detectAddSectionsC(self)
        return
    
    @classmethod
    def _detectAddSectionsC(cls):
        '''detect sections present in self._optdata and add them to self.config
        also add it to self._configlist
        param cls: class, class to configurate
        '''
        #seclist = [self._optdata[key]['sec'] for key in self._optdata.keys()]
        seclist = [cls._optdata[opt[0]]['sec'] for opt in cls._optdatalist]
        secdict = OrderedDict.fromkeys(seclist)
        #for sec in set(seclist):
        for sec in secdict.keys():
            cls.config.add_section(sec)
            cls._configlist[sec] = []
        return
    
    def _addOpt(self, optname):
        '''add options to self.config and self.args and self.'optname',
        this will read metadata in self._optdatalist
        
        param optname: string, name of option
        '''
        self._addOptC(self, optname)
        return
    
    @classmethod
    def _addOptC(cls, optname):
        '''add options to self.config and self.args and self.'optname',
        this will read metadata in self._optdatalist
        
        param optname: string, name of option
        '''
        optdata = cls._optdata[optname]
        opttype = cls._getTypeStrC(optname)
        
        #replace currentdir in default to os.getcwd()
        if optdata['d'] =='currentdir':
            optdata['d'] = os.getcwd()
        
        #add to cls.'optname'
        cls._addOptSelfC(optname, optdata)
        
        #add to cls.config
        secname =  optdata['sec'] if optdata.has_key('sec') else 'Others'
        cls._configlist[secname].append(optname)
        if optdata.get('config', 'a')!='n':
            strvalue = ', '.join(map(str, optdata['d'])) if type(optdata['d'])==list else str(optdata['d'])
            cls.config.set(secname, optname, strvalue)
        #add to cls.args
        if optdata.get('args', 'a')!='n':
            #transform optdata to a dict that can pass to add_argument method
            pargs = dict()
            for key in optdata.keys():
                if cls._optdatanamedict.has_key(key):
                    pargs[cls._optdatanamedict[key]] = optdata[key]
            pargs['default'] = argparse.SUPPRESS
            pargs['type'] = StrConv(opttype)
            #add args
            if optdata.has_key('f'):
                cls.args.add_argument(optname, **pargs)
            elif optdata.has_key('s'):
                cls.args.add_argument('--'+optname, '-'+optdata['s'], **pargs)
            else:
                cls.args.add_argument('--'+optname, **pargs)
        return
    
    @classmethod
    def _addOptSelfC(cls, optname, optdata):
        setattr(cls, optname, optdata['d'])
        return
    
    def _copyConfigtoSelf(self, optnames=None):
        '''copy the values in self.config to self.'options'
        
        param optname: str or list of str, names of options whose value copied from self.config to self.'optname'. 
        Set None to update all
        '''
        if optnames!=None:
            optnames = optnames if type(optnames)==list else [optnames]
        else:
            optnames = []
            for secname in self.config.sections():
                optnames += self.config.options(secname) 
                    
        for optname in optnames:
            if self._optdata.has_key(optname):
                secname = self._optdata[optname]['sec']
                opttype = self._getTypeStr(optname)
                optvalue = self.config.get(secname, optname)
                setattr(self, optname, str2Opt(opttype, optvalue))
        return
    
    def _copySelftoConfig(self, optnames=None):
        '''copy the value in self.'options' to self.config
        
        param optname: str or list of str, names of options whose value copied from self.'optname' to self.config. 
        Set None to update all
        '''
        if optnames!=None:
            optnames = optnames if type(optnames)==list else [optnames]
        else:
            optnames = []
            for secname in self.config.sections():
                optnames += self.config.options(secname) 
        
        for optname in optnames:
            if self._optdata.has_key(optname):
                secname = self._optdata[optname]['sec']
                opttype = self._getTypeStr(optname)
                optvalue = getattr(self, optname)
                self.config.set(secname, optname, opt2Str(opttype, optvalue))
        return
    
    ###########################################################################
    
    def parseArgs(self, pargs):
        '''parse args and update the value in self.'optname', this will call the self.args to parse args,
        
        param pargs: list of string, pargs to parse, usually be sys.argv
        '''
        obj = self.args.parse_args(pargs)
        changedargs = obj.__dict__.keys()
        for optname in changedargs:
            if self._optdata.has_key(optname):
                setattr(self, optname, getattr(obj, optname))
        #update self
        if len(changedargs)>0:
            self._updateSelf(changedargs)
        return obj
    
    def parseKwargs(self, **kwargs):
        '''update self.'optname' values according to the kwargs
        
        param kwargs: keywords=value
        '''
        if kwargs!={}:
            changedargs = []
            for optname, optvalue in kwargs.iteritems():
                if self._optdata.has_key(optname):
                    setattr(self, optname, optvalue)
                    changedargs.append(optname)
            #update self
            self._updateSelf(changedargs)
        return

    def parseConfigFile(self, filename):
        '''read a config file and update the self.'optname'
        
        param filename: str, file name of config file
        '''
        if filename!=None:
            if os.path.exists(filename):
                self._copySelftoConfig()
                self.config.read(filename)
                self._copyConfigtoSelf()
                self._updateSelf()
        return
    
    def updateConfig(self, filename=None, args=None, **kwargs):
        '''update config according to config file, args(from sys.argv) or **kwargs
        
        first process file/args/kwargs passed to this method, 
        then read a configfile if specified in args or kwargs
        then call self._postProcessing()
            call self._additionalPostProcessing()
            then write config file if specified in args/kwargs
        
        param filename: string, name of config file
        param args: list of str, usually be sys.argv
        param **kwargs: you can use like 'xbeamcenter=1024' or a dict to update the value of xbeamcenter
        
        return True if anything updated, False if nothing updated
        '''
        # call self._preUpdateConfig
        self._preUpdateConfig(**kwargs)
        
        filename = self._findConfigFile(filename, args, **kwargs)
        if filename!=None:
            rv = self.parseConfigFile(filename)
        if args!=None:
            rv = self.parseArgs(args)
        if kwargs!={}:
            rv = self.parseKwargs(**kwargs)
            
        if (filename==None)and(args==None)and(kwargs=={}):
            rv = self._updateSelf()
        
        # call self._callbackUpdateConfig
        self._postUpdateConfig(**kwargs)
        
        # write config file
        self._createConfigFile()
        return rv
    
    def _preUpdateConfig(self, **kwargs):
        '''Method called before parsing args or kwargs or config file, in self.updateConfig
        param kwargs: keywords=value
        '''
        return
    
    def _postUpdateConfig(self, **kwargs):
        '''Method called after parsing args or kwargs or config file, in self.updateConfig
        param kwargs: keywords=value
        '''
        return
    
    ###########################################################################
    def _createConfigFile(self):
        '''write output config file if specfied in configuration
        '''
        if (self.createconfig!='')and(self.createconfig!=None):
            self.writeConfig(self.createconfig, 'short')
            self.createconfig = ''
        if (self.createconfigfull!='')and(self.createconfigfull!=None):
            self.writeConfig(self.createconfigfull, 'full')
            self.createconfigfull = ''
        return
    
    def writeConfig(self, filename, mode='short'):
        '''write config to file
        
        param filename: string, name of file
        param mode: string, 'short' or 'full' ('s' or 'f'). 
            'short', options with 'config'=='f' will not be written into config file
            'full', all available options in self.config will be written to config file
        '''
        self._updateSelf()
        # func decide if wirte the option to config according to mode
        # options not present in self._optdata will not be written to config
        if mode.startswith('s'):
            mcond = lambda optname: self._optdata.get(optname, {'config':'n'}).get('config', 'a')=='a'
        else:
            mcond = lambda optname: self._optdata.get(optname, {'config':'n'}).get('config', 'a')!='n'
        
        lines = []        
        for section in self.config._sections:
            tlines = []
            for (key, value) in self.config._sections[section].items():
                if (key != "__name__") and mcond(key):
                    tlines.append("%s = %s" %(key, str(value).replace('\n', '\n\t')))
            if len(tlines)>0:
                lines.append("[%s]" % section)
                lines.extend(tlines)
                lines.append('')
        rv = "\n".join(lines) + "\n"
        fp = open(filename, 'w')
        fp.write(rv)
        fp.close()
        return
    
    def getHeader(self, title=None, mode='short'):
        '''get a header of configurations values, 
        
        by default, all options are written to a header, it can be disabled by 
        set 'header' to False in self._optdata
        
        param title: str, title of header
        param mode: string, 'short' or 'full' ('s' or 'f'). 
            'short', options with 'config'=='f' will not be written into config file
            'full', all available options in self.config will be written to config file
        
        return: string, lines that can be directly writen to a text file
        '''
        
        lines = []
        title = '# %s #' % (self._defauldata['theaderline'] if title==None else title)
        lines.append(title)
        #func decide if wirte the option to header according to mode
        #options not present in self._optdata will not be written to header
        if mode.startswith('s'):
            mcond = lambda optname: self._optdata.get(optname, {'config':'n'}).get('config', 'a')=='a'
        else:
            mcond = lambda optname: self._optdata.get(optname, {'config':'n'}).get('config', 'a')!='n'
    
        for secname in self._configlist.keys():
            tlines = []
            for optname in self._configlist[secname]:
                if mcond(optname):
                    value = getattr(self, optname)
                    strvalue = ', '.join(map(str, value)) if type(value)==list else str(value)
                    tlines.append("%s = %s" % (optname, strvalue))
            if len(tlines)>0:
                lines.append("[%s]" % secname)
                lines.extend(tlines)
                lines.append('')         
        rv = "\n".join(lines) + "\n"
        return rv
    
    ###########################################################################
    #IMPORTANT call this method if you want to add options as class attributes!!!
    @classmethod
    def initConfigClass(cls):
        '''init config class and add options to class
        this funtion should be executed to generate options according to metadata defined in class
        '''
        cls.config = ConfigParser.ConfigParser(dict_type = OrderedDict)
        cls.args = argparse.ArgumentParser(description=cls._description, 
                                              epilog=cls._epilog,
                                              formatter_class=argparse.RawDescriptionHelpFormatter)
        cls._configlist = OrderedDict({})
        
        cls._optdatalist = cls._optdatalist_default + cls._optdatalist
        cls._optdata = dict(cls._optdatalist)
        cls._detectAddSectionsC()
        for opt in cls._optdatalist:
            key = opt[0]
            cls._addOptC(key)
        return
    
    @classmethod
    def _additionalInitConfigClass(cls):
        '''additional method called in initConfigClass
        '''
        return
        

#VERY IMPORTANT!!!
#add options to class
#initConfigClass(ConfigBase)
ConfigBase.initConfigClass()

if __name__=='__main__':

    6
    test = ConfigBase()
    test.updateConfig()
