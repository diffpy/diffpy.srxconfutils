#!/usr/bin/env python
##############################################################################
#
# dpx.confutils     by Simon J. L. Billinge group
#                   (c) 2013 Trustees of the Columbia University
#                   in the City of New York.  All rights reserved.
#
# File coded by:    Xiaohao Yang
#
# See AUTHORS.txt for a list of people who contributed.
# See LICENSENOTICE.txt for license information.
#
##############################################################################

# package version
from diffpy.srxconfutils.version import __version__


# unit tests
def test():
    """Execute all unit tests for the diffpy.pdfgetx package.

    Return a unittest TestResult object.
    """
    from dpx.confutils.tests import test

    return test()


# silence the pyflakes syntax checker
assert __version__ or True

# End of file
