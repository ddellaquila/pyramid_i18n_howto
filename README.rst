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


6. Compiling the Message Catalog Files
======================================

Pyramid itself ignores the existence of all ``.po`` files. For a running
application to have translations available, you need to compile the
catalogs to ``.mo`` files.

Once your catalog files have been translated, run the following command::

    (env)$ python setup.py compile_catalog

Note
    I usually include ``.mo`` files in the ``.gitignore`` to keep them
    out of the version control system as they are just binaries.
    I added them here just for completeness of this tutorial.


7. Define the Default Local Name
================================

We are now able to see our web application translated, so define your
default locale name in the ``development.ini`` file::

    [app:main]
    #...
    pyramid.default_locale_name = it
    #...

Run the application using the ``pserve`` command::

    (env)$ pserve development.ini

Visit http://localhost:6543 in your browser, you should see your
messages translated.


8. Translating Strings in the Python Code
=========================================

We learn how to translate strings in template files, but we also need
to translate strings inside our Python code and for that we need to use
a localizer [4]_, a ``TranslationStringFactory`` and to add a renderer
globals [5]_ (which is currently deprecated as of Pyramid 1.1, so I will
have to investigate more on this) .

You can use the ``pyramid.i18n.get_localizer()`` function to obtain
a localizer.

Create the following ``pyramid_i18n_howto/i18n.py`` file::

    from pyramid.i18n import get_localizer, TranslationStringFactory


    def add_renderer_globals(event):
        request = event.get('request')
        if request is None:
            request = get_current_request()
        event['_'] = request.translate
        event['localizer'] = request.localizer


    tsf = TranslationStringFactory('pyramid_i18n_howto')


    def add_localizer(event):
        request = event.request
        localizer = get_localizer(request)

        def auto_translate(string):
            return localizer.translate(tsf(string))
        request.localizer = localizer
        request.translate = auto_translate

Then we change the application configuration by adding the
following event subscribers [6]_::

    config.add_subscriber('pyramid_i18n_howto.i18n.add_renderer_globals',
                          'pyramid.events.BeforeRender')
    config.add_subscriber('pyramid_i18n_howto.i18n.add_localizer',
                          'pyramid.events.NewRequest')

Now mark a string for translation in the ``view.py`` module, replace
the following line::

    return {'project': 'pyramid_i18n_howto'}

with::

    _ = request.translate
    return {'project': _('My i18n project')}

here we used the ``_()`` function, which is a convenient way of marking
translations strings.


9. Updating the catalog files
=============================

As we added another translation string, we need to extract again the
messages to the catalog template and update our catalog files::

    (env)$ python setup.py extract_messages
    (env)$ python setup.py update_catalog

Once again a human translator have to translate the messages, and don't
forget to recompile the catalogs files::

    (env)$ python setup.py compile_catalog

Test your application by running it with ``pserve`` command and visit
http://localhost:6543 in your browser, you should be able to read your
messages translated into the language defined by
``pyramid.default_locale_name``.


10. Determine the User Language
===============================

When developing a web application, you may want to determine the user
language. Pyramid doesn't dictate how a locale should be negotiated,
one way to do it is basing your site language on the ``Accept-Language``
header [7]_.

Add the following code to ``i18n.py`` module::

    from pyramid.events import NewRequest
    from pyramid.events import subscriber
    from webob.acceptparse import Accept


    @subscriber(NewRequest)
    def setAcceptedLanguagesLocale(event):
        if not event.request.accept_language:
            return
        accepted = event.request.accept_language
        event.request._LOCALE_ = accepted.best_match(('en', 'es', 'it'), 'it')


11. Using a Custom Locale Negotiator
====================================

Most of the web applications can make use of the default locale
negotiator [8]_, which requires no additional coding or configuration.

Sometimes, the default locale negotiation scheme doesn't fit our web
application needs and it's better to create a custom one.

As an example we modify the original ``default_locale_negotiator()`` by
implementing the check for the ``Accept-Language`` header.

Add the ``custom_locale_negotiator()`` function to the ``i18n.py``
module::

    LOCALES = ('en', 'es', 'it')

    def custom_locale_negotiator(request):
        """ The :term:`custom locale negotiator`. Returns a locale name.

        - First, the negotiator looks for the ``_LOCALE_`` attribute of
          the request object (possibly set by a view or a listener for an
          :term:`event`).

        - Then it looks for the ``request.params['_LOCALE_']`` value.

        - Then it looks for the ``request.cookies['_LOCALE_']`` value.

        - Then it looks for the ``Accept-Language`` header value,
          which is set by the user in his/her browser configuration.

        - Finally, if the locale could not be determined via any of
          the previous checks, the negotiator returns the
          :term:`default locale name`.
        """

        name = '_LOCALE_'
        locale_name = getattr(request, name, None)
        if locale_name is None:
            locale_name = request.params.get(name)
            if locale_name is None:
                locale_name = request.cookies.get(name)
                if locale_name is None:
                    locale_name = request.accept_language.best_match(
                        LOCALES, request.registry.settings.default_locale_name)
                    if not request.accept_language:
                        # If browser has no language configuration
                        # the default locale name is returned.
                        locale_name = request.registry.settings.default_locale_name

        return locale_name


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
.. [4] http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/i18n.html#using-a-localizer
.. [5] http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/hooks.html#adding-renderer-globals
.. [6] http://docs.pylonsproject.org/projects/pyramid/en/latest/api/config.html?highlight=add_subscriber#pyramid.config.Configurator.add_subscriber
.. [7] http://stackoverflow.com/questions/11274420/determine-the-user-language-in-pyramid
.. [8] http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/i18n.html#locale-negotiators
