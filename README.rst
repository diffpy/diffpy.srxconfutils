|Icon| |title|_
===============

.. |title| replace:: diffpy.srxconfutils
.. _title: https://diffpy.github.io/diffpy.srxconfutils

.. |Icon| image:: https://avatars.githubusercontent.com/diffpy
        :target: https://diffpy.github.io/diffpy.srxconfutils
        :height: 100px

|PythonVersion| |PR|

|Black| |Tracking|

.. |Black| image:: https://img.shields.io/badge/code_style-black-black
        :target: https://github.com/psf/black

.. |PR| image:: https://img.shields.io/badge/PR-Welcome-29ab47ff
        :target: https://github.com/diffpy/diffpy.srxconfutils/pulls

.. |PythonVersion| image:: https://img.shields.io/badge/python-3.11%20|%203.12%20|%203.13-blue

.. |Tracking| image:: https://img.shields.io/badge/issue_tracking-github-blue
        :target: https://github.com/diffpy/diffpy.srxconfutils/issues

Configuration utilities for diffpy project. Part of xPDFsuite.

For more information about the diffpy.srxconfutils library, please consult our `online documentation <https://diffpy.github.io/diffpy.srxconfutils>`_.

Citation
--------

If you use diffpy.srxconfutils in a scientific publication, we would like you to cite this package as

        Xiaohao Yang, Pavol Juhas, Christopher L. Farrow and Simon J. L. Billinge, xPDFsuite: an end-to-end
        software solution for high throughput pair distribution function transformation, visualization and
        analysis, arXiv 1402.3163 (2014)

Installation
------------
``diffpy.srxconfutils`` is normally installed as part of the ``xpdfsuite`` software, so please refer to the
installation instructions detailed in the ``README.rst`` file of ``xpdfsuite`` `here <https://github.com/diffpy/diffpy.xpdfsuite/blob/main/README.rst>`_.

Independent Installation
------------------------
You can also install ``diffpy.srxconfutils`` independently for yourself.

Assuming you have a wheel file in the current working directory, in an active conda environment please type

    pip install ./diffpy.srxconfutils-VERSION.whl

where you replace VERSION with the actual version you have so the command matches the filename of the
wheel file you have.

The commands to create and activate the conda environment with name "conf-env" is

    conda create -n conf-env python=3.13
    conda activate conf-env

If you don't have conda installed, we recomment you install `miniconda
<https://docs.conda.io/projects/miniconda/en/latest/miniconda-install.html>`_
To install this software from a Python wheel distribution format execute

    pip install ./diffpy.srxconfutils-VERSION.whl

If you are a developer, you can also install this package from sources. First, obtain the source archive
from `GitHub <https://github.com/diffpy/diffpy.srxconfutils/>`_.
Install the packages in ``./requirements/conda.txt`` and ``./requirements/tests.txt``
using the `--file`` command:

    conda activate conf-env
    conda install --file ./requirements/conda.txt
    conda install --file ./requirements/tests.txt
    pip install -e .    # assuming you are in the top level directory of the package

After installing the dependencies, ``cd`` into your ``diffpy.srxconfutils`` directory
and run the following ::

        pip install .

This package also provides command-line utilities. To check the software has been installed correctly, type ::

        diffpy.srxconfutils --version

You can also type the following command to verify the installation. ::

        python -c "import diffpy.srxconfutils; print(diffpy.srxconfutils.__version__)"


To view the basic usage and available commands, type ::

        diffpy.srxconfutils -h


Contact
-------

For more information on diffpy.srxconfutils please visit the project `web-page <https://diffpy.github.io/>`_ or email Simon J.L. Billinge group at sb2896@columbia.edu.

Acknowledgements
----------------

``diffpy.srxconfutils`` is built and maintained with `scikit-package <https://scikit-package.github.io/scikit-package/>`_.
