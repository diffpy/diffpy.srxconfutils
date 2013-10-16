dpx.confutils, package for processing configuration

REQUIREMENTS

The software requires Python 2.6 or 2.7 and third-party Python
libraries distribute, NumPy, matplotlib, IPython, PyReadline.
On Linux operating systems they can be obtained from the 
system software package repository.  On Windows and MAC it
is advisable to install either the PythonXY or Enthought Python
distributions, which include all the necessary software.


INSTALLATION

To install the PDFGetX3 software:

    python setup.py install

which should install a Python library diffpy.pdfgetx and two
command-line applications pdfgetx3 and plotdata.

By default the files are installed in the system directories,
which are usually only writeable by the root.  See the usage info
"python setup.py install --help" for options to install as a normal
user to a different location.  Note that installation to non-standard
directories may require adjustments to the PATH and PYTHONPATH
environment variables.

See the included manual for more installation details and for
user instructions.

------------------------------------------------------------------------------

For more information on the GetXgui software contact
Prof. Simon Billinge at sb2896@columbia.edu


dpx.confutils



INSTALLATION

To install the dpx.confutils package:

    python setup.py install

By default the files are installed in the system directories, which are
usually only writeable by the root.  See the usage info "./setup.py install --help" for options to install as a normal user under a different location.  Note that installation to non-standard directories you may require adjustments to the PATH and PYTHONPATH environment variables.

DEPENDENCIES

dpx.pdfgetxgui requires the following Python libraries,
numpy, 
traits,
traitsui,

if python version < 2.7 (these two packages are included in 2.7 but not in 2.6)
ordereddict  
argparse

We recommand to install EPD (Enthought Python Distribution)from http://www.enthought.com/ which include most of them by default. Besides EPD, PDFlive also require these packages:

------------------------------------------------------------------------------

For more information, please email Prof. Simon Billinge at sb2896@columbia.edu
