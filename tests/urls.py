from django import forms
from django.views import generic

try:
    from django.urls import url
except ImportError:
    from django.conf.urls import url

from . import models


class PersonForm(forms.ModelForm):
    class Meta:
        model = models.VIPClient
        exclude = ['data']


urlpatterns = [
    url('^$', generic.FormView.as_view(
        form_class=PersonForm,
        template_name='index.html',
        success_url='/'))
]
