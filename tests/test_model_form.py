from django import forms
from django.test import TestCase

from .models import Person, Client, VIPClient


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        exclude = ['data']


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        exclude = ['data']


class VIPClientForm(forms.ModelForm):
    class Meta:
        model = VIPClient
        exclude = ['data']


class Test(TestCase):
    def test_person_form(self):
        form = PersonForm()
        self.assertIn('name', form.fields)

    def test_client_form(self):
        form = ClientForm()
        self.assertIn('name', form.fields, "Inherited field 'name' not found")
        # self.assertIn('business_phone', form.fields, "Field 'business_phone' not found")

    def test_vipclient_form(self):
        form = VIPClientForm()
        self.assertIn('name', form.fields, 'Inherited field name not found')
        # self.assertIn('personal_phone', form.fields, "Field 'personal_phone' not found")
