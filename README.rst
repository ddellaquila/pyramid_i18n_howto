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

.. references:
.. [1] http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/project.html
