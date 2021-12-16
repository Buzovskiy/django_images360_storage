# https://adriennedomingus.com/blog/adding-custom-views-and-templates-to-django-admin

from django.contrib import admin

from django.contrib import admin
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.urls import path
from django.db import models
from django.shortcuts import render
from django.contrib.admin import AdminSite


class MyAdminSite(AdminSite):
    site_header = 'Monty Python'


# my dummy model
class DummyModel(models.Model):
    # pass
    class Meta:
        verbose_name_plural = 'Dummy Model'
        app_label = 'image360upload'


# def my_custom_view(request):
#     # return HttpResponse('Admin Custom View', )
#     # return render(request, template_name='admin/unpack3dmodels.html')


class DummyModelAdmin(admin.ModelAdmin):
    def get_urls(self):
        view_name = '{}_{}_changelist'.format(
            self.model._meta.app_label, self.model._meta.model_name)
        # view_name = 'Upload 3d models'
        return [
            path('my_admin_path/', self.my_view, name=view_name),
        ]

    def my_view(self, request):
        # ...
        context = dict(
            # Include common variables for rendering the admin template.
            self.admin_site.each_context(request),
            # Anything else you want in the context...
            # key=value,
        )
        return TemplateResponse(request, "sometemplate.html", context)


# admin.site.register(DummyModel, DummyModelAdmin)
# admin.site.register(DummyModel)

# myadminsite = MyAdminSite(name='rrr')
# myadminsite.register(DummyModel)


# class Unpack3dAdmin(admin.ModelAdmin):
#     change_form_template = 'admin/unpack3dmodels.html'
