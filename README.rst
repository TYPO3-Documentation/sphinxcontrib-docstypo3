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
   copyright = "2021, TYPO3 Documentation Team"
   description = "This is a sample project to demonstrate good style."
   language = "((set by Sphinx))"
   license = "MIT license"
   maintainer = "John Doe <john.doe@example.org>"
   project = "EXTKEY or Short Project Name"
   release = "1.2.dev3 or main or BRANCH"
   t3author = "((deprecated variable name))"
   version = "1.2 or main or BRANCH"

In TYPO3 documentation projects you usually don't deal with file `conf.py`
directly but provide a `Settings.cfg` file that follows the INI-file
conventions. For this example this looks like this:

.. code-block:: ini

   # example file Settings.cfg:

   [general]

   # everything from section [general] is directly added to `conf.py`

   audience    = Developers
   author      = TYPO3 Documentation Team
   t3author    = ((deprecated variable name))
   copyright   = 2021, TYPO3 Documentation Team
   description = This is a sample
      project to demonstrate
      good style.
   language    = ((set by Sphinx))
   license     = MIT license
   maintainer  = John Doe <john.doe@example.org>
   project     = EXTKEY or Short Project Name
   release     = 1.2.dev3 or main or BRANCH
   version     = 1.2 or main or BRANCH

   # urls
   project_contact     =
   project_discussions =
   project_home        =
   project_issues      =
   project_repository  = https://github.com/TYPO3-Documentation/sphinxcontrib-docstypo3
   published           =

To access these configuration values in your documentation you can use the
replacement syntax with the following keys:

.. code-block:: python

   substitution_keys = {
      # configured directly in conf.py
      "cfg_audience",
      "cfg_author",
      "cfg_copyright",
      "cfg_description",
      "cfg_language",
      "cfg_license",
      "cfg_maintainer",
      "cfg_project",
      "cfg_published",
      "cfg_release",
      "cfg_t3author",
      "cfg_version",

      # configured in html_theme_options (hto) in conf.py
      "hto_project_contact",
      "hto_project_discussions",
      "hto_project_home",
      "hto_project_issues",
      "hto_project_repository",
   }

RST source example:

.. code-block:: rst

   ============================  ====================================================
   RST source                    Result
   ============================  ======================================================
   # cfg, directly from conf.py
   |cfg_audience|                Developers
   |cfg_author|                  TYPO3 Documentation Team
   |cfg_copyright|               2021, TYPO3 Documentation Team
   |cfg_description|             This is a sample project to demonstrate good style.
   |cfg_language|                ((set by Sphinx))
   |cfg_license|                 MIT license
   |cfg_maintainer|              John Doe <john.doe@example.org>
   |cfg_project|                 EXTKEY or Short Project Name
   |cfg_published|
   |cfg_release|                  1.2.dev3 or main or BRANCH
   |cfg_t3author|                ((deprecated variable name))
   |cfg_version|                  1.2 or main or BRANCH

   # hto, html_theme_options
   |hto_project_contact|
   |hto_project_discussions|
   |hto_project_home|
   |hto_project_issues|
   |hto_project_repository|
   =============================  ======================================================

Missing values will simply be shown as empty string.

'cfg_author' will fetch the value of 'author'. If empty, 't3author' is
consulted.


Installation
============

Install the latest version as Python module with PIP, the Python packet manager:

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
