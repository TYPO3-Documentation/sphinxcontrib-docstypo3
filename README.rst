=======================
sphinxcontrib-docstypo3
=======================

.. image: : https://travis-ci.org/TYPO3-Documentation/sphinxcontrib-docstypo3.svg?branch=master
    :target: https://travis-ci.org/TYPO3-Documentation/sphinxcontrib-docstypo3

Sphinx extension for specific features of TYPO3 documentation.


Overview
========

At the moment the extension provides replacements to insert configuration
values into the documentation.


What does it do?
================

Substitutions
-------------

The extension provides some substitutions. Consider this `conf.py` configuration
file:

.. code-block:: python

   # example file conf.py:

   audience = "Developers"
   author = "TYPO3 Documentation Team"
   t3author = "((deprecated variable name))"
   copyright = "2021, TYPO3 Documentation Team"
   description = "This is a sample project to demonstrate good style."
   language = "((set by Sphinx))"
   license = "MIT license"
   project = "EXTKEY or Short Project Name"
   release = "1.2.dev3 or main or BRANCH"
   version = "1.2 or main or BRANCH"

To access these configuration values in your documentation you can use the
replacement syntax with the following keys:

.. code-block:: python

   substitution_keys = {
       "cfg_audience",
       "cfg_author",
       "cfg_t3author",
       "cfg_copyright",
       "cfg_description",
       "cfg_language",
       "cfg_license",
       "cfg_project",
       "cfg_release",
       "cfg_version",
   }

RST source example:

.. code-block:: rst

   ================= ======================================================
   RST source        Result
   ================= ======================================================
   |cfg_audience|    Developers
   |cfg_author|      TYPO3 Documentation Team
   |cfg_t3author|    ((deprecated variable name))
   |cfg_copyright|   2021, TYPO3 Documentation Team
   |cfg_description| This is a sample project to demonstrate good style.
   |cfg_language|    ((set by Sphinx))
   |cfg_license|     MIT license
   |cfg_project|     EXTKEY or Short Project Name
   |cfg_release|     1.2.dev3 or main or BRANCH
   |cfg_version|     1.2 or main or BRANCH
   ================= ======================================================

Undefined values will be return the empty string.

`cfg_author` returns `author` or `t3author` or the empty string in this order.



Installation
============

Install the latest version:

.. code-block:: shell

   pip install https://github.com/TYPO3-Documentation/sphinxcontrib-docstypo3/archive/refs/heads/main.zip


Extend the list of Sphinx extensions to be loaded in file `conf.py` of your
documentation project:

.. code-block:: python

   extensions = [
      # ...,
       "sphinxcontrib.docstypo3",
      # ...,
   ]


Links
=====

- Source: https://github.com/TYPO3-Documentation/sphinxcontrib-docstypo3
- Bugs: https://github.com/TYPO3-Documentation/sphinxcontrib-docstypo3/issues
