##########################
Django Simple Spam Blocker
##########################

.. image:: https://secure.travis-ci.org/moqada/django-simple-spam-blocker.png?branch=master
   :target: http://travis-ci.org/moqada/django-simple-spam-blocker/

Django Simple Spam Blocker is blocking spam by regular expression.

Filtering the following matters.

* Author
* Content
* Email
* IP
* Referer
* URL
* UserAgent

And you can edit regular expression, on Django's admin site.


Installation
============

#. Add the ``simplespamblocker`` directory to your Python path.
#. Add ``simplespamblocker`` to your ``INSTALLED_APPS``.::

       INSTALLED_APPS = (
           # ...
           'simplespamblocker',
           # ...
       )

#. Add the following middleware to your ``MIDDLEWARE_CLASSES``.::

       MIDDLEWARE_CLASSES = (
           # ...
           'simplespamblocker.middleware.SpamBlockMiddleware',
           # ...
       )

#. Add path which you wanto to block spam to ``SIMPLESPAMBLOCKER_PROFILES`` on ``settings.py``.::

       SIMPLESPAMBLOCKER_PROFILES = (
           # Sample for django's comment framework
           (r'^/comments/post/$', {
               'method': 'post',
               'author': lambda request: request.POST.get('name', ''),
               'email': lambda request: request.POST.get('email', ''),
               'url': lambda request: request.POST.get('url', ''),
               'content': lambda request: request.POST.get('comment', ''),
           }),
       )

#. Run syncdb.::

       $ python manage.py syncdb

   **Note**: When your project use South, run the following command.::

       $ python manage.py migrate simplespamblocker

#. Run your server, visit admin site and edit regular expression of Option model.


Settings
========

``SIMPLESPAMBLOCKER_PROFILES``
    The list of tuple -- regular expression of path and block profile --.

``SIMPLESPAMBLOCKER_SPAM_TEMPLATE``
    A path of template file which is rendering after blocking spam
    This key is generated per Option model.

    default: 'simplespamblocker/option/<id>'

``SIMPLESPAMBLOCKER_LOGGER_NAME``
    Python's builtin logger name.
    This logger logs at blocking spam.
    Default value is None. (inactive)


Others
======

This project is Inspired by `django-spaminspector <http://github.com/lambdalisue/django-spaminspector>`_.
