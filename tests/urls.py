from django import forms
from django.urls import path
from django.views import generic

from . import models


class PersonForm(forms.ModelForm):
    class Meta:
        model = models.VIPClient
        exclude = ['data']


urlpatterns = [
    path('', generic.FormView.as_view(
        form_class=PersonForm,
        template_name='index.html',
        success_url='/'))
]
