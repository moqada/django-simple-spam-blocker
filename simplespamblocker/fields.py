# -*- coding: utf-8 -*-
from django.db import models
from simplespamblocker import forms


class ValidRegexField(models.TextField):

    def formfield(self, **kwargs):
        defaults = {
            'form_class': forms.ValidRegexField,
        }
        defaults.update(kwargs)
        return super(ValidRegexField, self).formfield(**defaults)
