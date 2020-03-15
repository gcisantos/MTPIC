# -*- coding: utf-8 -*-
"""
Created on Thu Oct  4 23:10:12 2018

@author: GCISANTOS
"""

from django import forms

class NameForm(forms.Form):
    texto = forms.Textarea()