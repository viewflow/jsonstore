from django.contrib import admin
from . import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    exclude = ['data']


@admin.register(models.Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'salary', 'department']
    exclude = ['data']


@admin.register(models.Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'city', 'data']
    exclude = ['data']
