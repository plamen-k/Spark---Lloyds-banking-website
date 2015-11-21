# Code written by Plamen Kolev

from django import forms
from help.models import FormQuestion

class FormQuestinForm(forms.ModelForm):
    # taken from http://stackoverflow.com/questions/430592/django-admin-charfield-as-textarea    def formfield_for_dbfield(self, db_field, **kwargs):


    class Meta:
        model = FormQuestion
        exclude = ("answered",)