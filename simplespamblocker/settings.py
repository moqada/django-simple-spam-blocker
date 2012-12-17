# -*- coding: utf-8 -*-
from django.conf import settings


# middleware use cache
CACHE_KEY = getattr(settings, 'SIMPLESPAMBLOCKER_CACHE_KEY',
                    'simplespamblocker/option/%(id)s')

# activate logger
LOGGER_NAME = getattr(settings, 'SIMPLESPAMBLOCKER_LOGGER_NAME', None)

# page on blocked spam
SPAM_TEMPLATE = getattr(settings, 'SIMPLESPAMBLOCKER_SPAM_TEMPLATE', None)
