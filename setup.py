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

# Installation script for dpx.confutils

"""dpx.confutils
"""

from setuptools import setup, find_packages

# define distribution
dist = setup(
        name = 'dpx.confutils',
        version = '1.0',
        namespace_packages = ['dpx'],
        packages = find_packages(),
        zip_safe = False,
        scripts = [],
        data_files = [],
        install_requires = [],
        dependency_links = [],
        entry_points = {
            # define console_scripts here, see setuptools docs for details.
            
        },

        author = 'Simon J.L. Billinge',
        author_email = 'sb2896@columbia.edu',
        description = 'configuration packages for dpx projects',
        license = 'BSD',
        #url = 'http://www.diffpy.org/',
        keywords = 'PDF x-ray Fourier transform',
)

# End of file
