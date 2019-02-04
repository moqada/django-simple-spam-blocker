# -*- coding: utf-8 -*-
import re
from django import forms


class ValidRegexField(forms.CharField):

    def clean(self, value):
        value = super(ValidRegexField, self).clean(value)
        if value:
            try:
                re.compile(value)
            except re.error as e:
                raise forms.ValidationError('Please input valid regexp: %s' % e)
        return value
