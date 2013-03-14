==================
Pyramid i18n HOWTO
==================


This repository is a tutorial about Pyramid Internationalization and
Localization, you can follow along the commits to see step by step
how to implement i18n into your web application.

This tutorial is the result of my experiments done while studying
Pyramid, a Python web application development framework, and it is a
practical how to, so I'm not going in deep with any explanation but
I invite you to read the references I used in order to have a better
understanding of Pyramid internationalization and localization.


1. Creating a Pyramid Project
=============================

We start off with a new Pyramid project [1]_, for this you will need
Python and Pyramid installed, see `Installing Pyramid`_ for the details::

    (env)$ pcreate -t starter pyramid_i18n_howto
    (env)$ cd pyramid_i18n_howto/
    (env)$ python setup.py develop
    (env)$ python setup.py test -q
    (env)$ pserve development.ini

Browse to your project by visiting http://localhost:6543 in your browser.


2. Setup Internationalization and Localization
==============================================

To setup Internationalization and Localization [2]_ you need to install
``Babel`` and ``lingua`` packages in your virtual environment::

    (env)$ easy_install Babel lingua

Then edit the ``setup.py`` file in order to generate ``gettext`` files
from your application.

In particular, add the Babel and lingua distributions to the ``requires``
list and insert a set of references to Babel *message extractors*::

    # ...
    requires = [
        # ...
        'Babel',
        'lingua',
        ]

    setup(name="mypackage",
          # ...
          message_extractors = { '.': [
                ('**.py', 'lingua_python', None ),
                ('**.pt', 'lingua_xml', None ),
                ]},
          )

The ``message_extractors`` stanza placed into the ``setup.py`` file causes
the Babel message catalog extraction machinery to also consider ``*.pt``
files when doing message id extraction.

If you use Mako templates you may also want to add the following in the
``message_extractors`` [3]_::

    # ...
    message_extractors = { '.': [
          # ...
          ('templates/**.html', 'mako', None),
          ('templates/**.mako', 'mako', None),
          ('static/**', 'ignore', None)
          ]},

Then you need to add your ``locale`` directory to your project’s
configuration, edit ``pyramid_i18n_howto/__init__.py`` file::

    def main(...):
        # ...
        config.add_translation_dirs('pyramid_i18n_howto:locale')


3. Mark Messages for Translation
================================

Now it's time to mark some messages that need to be translated in our
template, but first add a namespace and the *i18n:domain* to the
``templates/mytemplate.pt`` template file::

    <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en"
          xmlns:tal="http://xml.zope.org/namespaces/tal"
          xmlns:i18n="http://xml.zope.org/namespaces/i18n"
          i18n:domain="pyramid_i18n_howto">

Then we mark some messages for translation, for simplicity we edit only
the *Search documentation* string::

    <h2 i18n:translate="search_documentation">Search documentation</h2>


4. Extracting Messages from a Template
======================================

We follow by extracting the messages from a template, run these commands
in your project’s directory::

    (env)$ mkdir pyramid_i18n_howto/locale
    (env)$ python setup.py extract_messages

Last command it creates the message catalog template named
``pyramid_i18n_howto/locale/pyramid_i18n_howto.pot``.


5. Initializing the Message Catalog Files
=========================================

Then initialize the catalogs for each language that you want to use::

    (env)$ python setup.py init_catalog -l en
    (env)$ python setup.py init_catalog -l es
    (env)$ python setup.py init_catalog -l it

The message catalogs ``.po`` files will end up in::

    pyramid_i18n_howto/locale/en/LC_MESSAGES/pyramid_i18n_howto.po
    pyramid_i18n_howto/locale/es/LC_MESSAGES/pyramid_i18n_howto.po
    pyramid_i18n_howto/locale/it/LC_MESSAGES/pyramid_i18n_howto.po

Once the files are there, they can be worked on by a human translator.
One tool that may help you with this is `Poedit`_.


----

To read the original blog post of this tutorial visit
http://danilodellaquila.com/blog/pyramid-internationalization-howto

This tutorial is licensed under the Creative Commons
Attribution-ShareAlike 3.0 Unported License. To view a copy of this
license, visit http://creativecommons.org/licenses/by-sa/3.0/.

The `pyramid_i18n_howto`_ source code is free software: you can
redistribute it and/or modify it under the terms of the GNU
General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option)
any later version.

.. links:
.. _`pyramid_i18n_howto`: https://github.com/ddellaquila/pyramid_i18n_howto
.. _`Installing Pyramid`: http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/install.html#installing-chapter
.. _`Poedit`: http://www.poedit.net/


.. references:
.. [1] http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/project.html
.. [2] http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/i18n.html
.. [3] http://docs.pylonsproject.org/projects/pyramid_cookbook/en/latest/templates/mako_i18n.html
