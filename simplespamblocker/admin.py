# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from simplespamblocker.models import Option


class OptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'site', 'is_block_author', 'is_block_content',
                    'is_block_email', 'is_block_url',
                    'is_block_remote_addr', 'is_block_http_referer',
                    'is_block_http_user_agent', 'created_at', 'updated_at')
    search_fields = ('block_author', 'block_content', 'block_email',
                     'block_url', 'block_remote_addr', 'block_http_referer',
                     'block_http_user_agent')

    def is_block_author(self, obj):
        return bool(obj.block_author)

    def is_block_content(self, obj):
        return bool(obj.block_content)

    def is_block_email(self, obj):
        return bool(obj.block_email)

    def is_block_url(self, obj):
        return bool(obj.block_url)

    def is_block_http_referer(self, obj):
        return bool(obj.block_http_referer)

    def is_block_http_user_agent(self, obj):
        return bool(obj.block_http_user_agent)

    def is_block_remote_addr(self, obj):
        return bool(obj.block_remote_addr)

    is_block_author.short_description = _('block author')
    is_block_content.short_description = _('block content')
    is_block_email.short_description = _('block email')
    is_block_url.short_description = _('block url')
    is_block_http_referer.short_description = _('block http referer')
    is_block_http_user_agent .short_description = _('block http user agent')
    is_block_remote_addr.short_description = _('block IP')
    is_block_author.boolean = True
    is_block_content.boolean = True
    is_block_email.boolean = True
    is_block_url.boolean = True
    is_block_http_referer.boolean = True
    is_block_http_user_agent.boolean = True
    is_block_remote_addr.boolean = True


admin.site.register(Option, OptionAdmin)
