# -*- coding: utf-8 -*-
try:
    from django.conf.urls import url, patterns, include
except ImportError:
    # compatible under django 1.3
    from django.conf.urls.defaults import url, patterns, include


urlpatterns = patterns(
    '',
    url(r'^comments/', include('django.contrib.comments.urls')),
)
