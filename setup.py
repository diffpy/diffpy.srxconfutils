#!/usr/bin/env python

# Installation script for dpx.confutils

"""dpx.confutils
"""

from setuptools import setup, find_packages

# define distribution
dist = setup(
        name = 'dpx.confutils',
        version = '0.1',
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
