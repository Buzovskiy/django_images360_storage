# https://adriennedomingus.com/blog/adding-custom-views-and-templates-to-django-admin

from django.contrib import admin

from django.contrib import admin
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.urls import path
from django.db import models
from .models import Unpack3dModel, Image360
from django.shortcuts import render
from django.contrib.admin import AdminSite
from django.views.generic import TemplateView


@admin.register(Image360)
class Image360Admin(admin.ModelAdmin):
    pass

# @admin.register(Image360)
# class Unpack3dModelAdmin(admin.ModelAdmin):
#     def get_urls(self):
#
#         # get the default urls
#         urls = super(Unpack3dModelAdmin, self).get_urls()
#         print('hello')
#         # define security urls
#         security_urls = [
#             path('configuration/', self.admin_site.admin_view(self.security_configuration))
#             # Add here more urls if you want following same logic
#         ]
#
#         # Make sure here you place your added urls first than the admin default urls
#         return security_urls + urls
#
#     # Your view definition fn
#     def security_configuration(self, request):
#         context = dict(
#             self.admin_site.each_context(request), # Include common variables for rendering the admin template.
#             something="test",
#         )
#         return TemplateResponse(request, "change_list.html", context)


# class MyAdminSite(AdminSite):
#     site_header = 'Monty Python'
#
#
# my dummy model
class DummyModel(models.Model):
    # pass
    class Meta:
        verbose_name_plural = 'Dummy Model'
        app_label = 'image360upload'


# def my_custom_view(request):
#     # return HttpResponse('Admin Custom View', )
#     # return render(request, template_name='admin/unpack3dmodels.html')


# @admin.register(Unpack3dModel)
# class DummyModelAdmin(admin.ModelAdmin):
#     def get_urls(self):
#         # view_name = '{}_{}_changelist'.format(
#         #     self.model._meta.app_label, self.model._meta.model_name)
#         # # view_name = 'Upload 3d models'
#         # return [
#         #     path('', self.my_view, name=view_name),
#         # ]
#         urls = super().get_urls()
#         my_urls = [
#             path('', self.admin_site.admin_view(self.my_view)),
#         ]
#         return my_urls + urls
#
#     def my_view(self, request):
#         # ...
#         context = dict(
#             # Include common variables for rendering the admin template.
#             self.admin_site.each_context(request),
#             # Anything else you want in the context...
#             # opts=Unpack3dModel._meta,
#         )
#         return TemplateResponse(request, "admin/sometemplate.html", context)

@admin.register(Unpack3dModel)
class DummyModelAdmin(admin.ModelAdmin):
    def get_urls(self):
        # view_name = '{}_{}_changelist'.format(
        #     self.model._meta.app_label, self.model._meta.model_name)
        # # view_name = 'Upload 3d models'
        # return [
        #     path('', self.my_view, name=view_name),
        # ]
        urls = super().get_urls()
        opts = self.model._meta
        # context = dict(
        #     # Include common variables for rendering the admin template.
        #     self.admin_site.each_context(self.get_request()),
        #     # Anything else you want in the context...
        #     # opts=Unpack3dModel._meta,
        # )
        # print(self.get_request())
        my_urls = [
            path('', self.admin_site.admin_view(self.my_view)),
        ]
        return my_urls + urls


    def my_view(self, request):
        # ...
        # cl = self.get_changelist_instance(request)
        context = dict(
            # Include common variables for rendering the admin template.
            self.admin_site.each_context(request),
            # Anything else you want in the context...
            opts=self.model._meta,

        )
        print(self.model._meta.app_label)
        return TemplateResponse(request, "admin/sometemplate.html", context)




# admin.site.register(Unpack3dModel, DummyModelAdmin)
# admin.site.register(DummyModel, DummyModelAdmin)
# admin.site.register(DummyModel)

# myadminsite = MyAdminSite(name='rrr')
# myadminsite.register(DummyModel)


# class Unpack3dAdmin(admin.ModelAdmin):
#     change_form_template = 'admin/unpack3dmodels.html'