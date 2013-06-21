#!/usr/bin/env python
##############################################################################
#
# File coded by:    Xiaohao Yang
#
# See AUTHORS.txt for a list of people who contributed.
# See LICENSENOTICE.txt for license information.
#
##############################################################################

# package version
from dpx.confutils.version import __version__

# some convenience imports
from dpx.confutils.config import ConfigBase, ConfigBase

# unit tests
def test():
    '''Execute all unit tests for the diffpy.pdfgetx package.
    Return a unittest TestResult object.
    '''
    from dpx.confutils.tests import test
    return test()


# End of file
