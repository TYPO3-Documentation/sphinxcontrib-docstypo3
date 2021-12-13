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

    ; endless list of all of the general simple settings
    ; you can use in 'conf.py'

    author    = TYPO3 Documentation Team
    copyright = 2021, TYPO3 Documentation Team
    language  = en
    project   = EXTKEY or Short Project Name
    release   = 1.2.dev3 or main or BRANCH
    version   = 1.2 or main or BRANCH


    [docstypo3-meta]

    audience    = Developers and editors of TYPO3 documentation
    description = This is a multiline example
       description for a nonexisting
       project.
    doctype     = Technical rendering test example
    language    = English (US)
    license     = CC-BY 4.0 (https://creativecommons.org/licenses/by/4.0/)
    maintainer  = John Doe <john.doe@example.org>
    t3author    = ((deprecated variable name))
    website     = Read online (#)

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
        #
        # Standard Sphinx settings, [general], (prefix: std_)
        "std_author",
        "std_copyright",
        "std_language",  # "en", two-letter-code
        "std_project",
        "std_release",
        "std_version",
        #
        # sphinxcontrib-docstypo3, [docstypo3-meta], (prefix: dt3m_)
        "dt3m_audience",
        "dt3m_description",
        "dt3m_doctype",   # Demo, Tutorial, Reference, Book
        "dt3m_language",  # "English" readable phrase
        "dt3m_license",
        "dt3m_maintainer",
        "dt3m_website",
        #
        # Sphinx html_theme_options, [html_theme_options], (prefix: hto_)
        "hto_bitbucket_host",
        "hto_bitbucket_repo",
        "hto_bitbucket_user",
        "hto_bitbucket_version",
        "hto_github_host",
        "hto_github_repo",
        "hto_github_user",
        "hto_github_version",
        "hto_gitlab_host",
        "hto_gitlab_repo",
        "hto_gitlab_user",
        "hto_gitlab_version",
        "hto_project_contact",
        "hto_project_discussions",
        "hto_project_home",
        "hto_project_issues",
        "hto_project_repository",
    }

RST source example:

.. code-block:: rst

   ============================  ====================================================
   Markup                        Result
   ============================  ======================================================
   |std_author||                 TYPO3 Documentation Team
   |std_copyright|               2021, TYPO3 Documentation Team
   |std_language|                en
   |std_project|                 EXTKEY or Short Project Name
   |std_release|                 1.2.dev3 or main or BRANCH
   |std_version|                 1.2 or main or BRANCH

   |dt3m_audience|               Developers and editors of TYPO3 documentation
   |dt3m_description|            This is a sample project to demonstrate good style.
   |dt3m_doctype|                Technical rendering test example
   |dt3m_language|               English (US)
   |dt3m_license|                `CC-BY 4.0 <https://creativecommons.org/licenses/by/4.0/>`__
   |dt3m_maintainer|             John Doe <john.doe@example.org>
   |dt3m_website|                `Read online <#>`__
   ============================  ======================================================

Unset values will be replaced by the empty string.

Unknown replacements will be left untouched.



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
