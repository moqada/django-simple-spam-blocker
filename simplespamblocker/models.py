# -*- coding: utf-8 -*-
import re
from django.contrib.sites.models import Site
from django.core.cache import cache
from django.db import models
from django.utils.translation import ugettext_lazy as _
from simplespamblocker.fields import ValidRegexField
from simplespamblocker.settings import CACHE_KEY


class Option(models.Model):
    """ Spam block option per Site
    """
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    site = models.OneToOneField(Site)
    block_author = ValidRegexField(
        _('block author'), blank=True, help_text=_('input regexp'))
    block_content = ValidRegexField(
        _('block content'), blank=True, help_text=_('input regexp'))
    block_email = ValidRegexField(
        _('block email'), blank=True, help_text=_('input regexp'))
    block_url = ValidRegexField(
        _('block url'), blank=True, help_text=_('input regexp'))
    block_remote_addr = ValidRegexField(
        _('block IP'), blank=True, help_text=_('input regexp'))
    block_http_referer = ValidRegexField(
        _('block http referer'), blank=True, help_text=_('input regexp'))
    block_http_user_agent = ValidRegexField(
        _('block http user agent'), blank=True, help_text=_('input regexp'))

    block_fields = ('author', 'content', 'email', 'url',
                    'remote_addr', 'http_referer', 'http_user_agent')

    class Meta:
        app_label = 'simplespamblocker'
        verbose_name = _('option')
        verbose_name_plural = _('options')

    def __unicode__(self):
        return u'Option for %s' % self.site

    def save(self, **kwargs):
        super(Option, self).save(**kwargs)
        cache.delete(self.get_cache_key(self.site))

    def compile_regexes(self):
        regexes = {}
        for key in self.block_fields:
            regex = getattr(self, 'block_%s' % key)
            regexes[key] = re.compile(regex, re.IGNORECASE) if regex else None
        return regexes

    @classmethod
    def get_cache_key(cls, site):
        return CACHE_KEY % {'id': site.id, 'domain': site.domain, 'name': site.name}


try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ['^simplespamblocker\.fields\.ValidRegexField'])
except ImportError:
    pass
