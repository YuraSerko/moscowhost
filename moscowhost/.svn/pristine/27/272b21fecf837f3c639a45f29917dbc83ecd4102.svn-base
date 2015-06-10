from django.forms.formsets import BaseFormSet
from django.forms.formsets import formset_factory
from django import forms
from django.utils.translation import ugettext_lazy as _
from lib.forms.widgets import JqCalendar
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from account.models import get_all_user_choices

class PhoneForm(forms.Form):
    number_id = forms.IntegerField(widget=forms.HiddenInput)
    login = forms.CharField(label=_(u"Login"))
    number = forms.CharField(label=_(u"Number"))
    password = forms.CharField(label=_(u"Password"))


def phone_set_fields():
    return tuple(PhoneForm.base_fields.keys())

def pack_form(form):
    return dict(map(\
                   lambda x: (x, form.cleaned_data.get(x)), \
                       phone_set_fields()))

def pack_formset(formset):
    return [pack_form(form) for form in formset]

def unpack_formset(data):
    extra = len(data)
    initial = dict(map(lambda x: zip(phone_set_fields(), x), data))
    PhoneFormset = formset_factory(PhoneForm, extra=extra)
    return PhoneFormset(initial=initial)

class FirstPhoneForm(forms.Form):
    login = forms.CharField(label=_(u"Login"), required=False, help_text=_(u"You can leave this field empty."))
    password = forms.CharField(label=_(u"Password"))

from account.forms import first_date, last_date, first_date_new, first_date_last
