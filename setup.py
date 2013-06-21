#!/usr/bin/env python

# Installation script for diffpy.pdfgetx

"""dpx.pdfgetxgui
"""

from setuptools import setup, find_packages

# define distribution
dist = setup(
        name = 'dpx.pdfgetxgui',
        version = '0.1',
        namespace_packages = ['dpx'],
        packages = find_packages(),
        scripts = [],
        data_files = [],
        install_requires = [],
        dependency_links = [],
        entry_points = {
            # define console_scripts here, see setuptools docs for details.
            'console_scripts' : ['dpx = dpx.pdfgetxgui.pdfliveui:main'
                                 ],
        },

        author = 'Simon J.L. Billinge',
        author_email = 'sb2896@columbia.edu',
        description = 'GUI for PDFgetX3, a program calculating PDF from raw x-ray intensities.',
        license = 'BSD',
        #url = 'http://www.diffpy.org/',
        keywords = 'PDF x-ray Fourier transform',
)

# End of file
