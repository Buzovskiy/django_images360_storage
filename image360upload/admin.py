# https://adriennedomingus.com/blog/adding-custom-views-and-templates-to-django-admin

from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path
from .models import Image360, Image360Archive, Website, RemoteUpdateImages360Url
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import filesizeformat
from django.template.response import TemplateResponse
from .management.commands import import_archives, create_photos_360
from django.contrib import messages
from django.conf import settings
from django.utils.safestring import mark_safe
from django.core.exceptions import ObjectDoesNotExist
import urllib.request
from urllib.error import URLError


@admin.register(Image360Archive)
class Model360ArchiveAdmin(admin.ModelAdmin):
    list_display = ['id', '__str__', 'vendor_code', 'file_path', 'archive_size']
    list_display_links = ['__str__']
    actions = ['create_photos_360']
    ordering = ['size']

    @admin.display(description=_('Archive size'))
    def archive_size(self, obj):
        return filesizeformat(obj.archive.size)

    @admin.display(description=_('Path to file'))
    def file_path(self, obj):
        return obj.archive.name

    @admin.action(description=_('Create photos 360'))
    def create_photos_360(self, request, queryset):
        create_photos_360.Command().handle(outer_queryset=queryset, request=request)
        messages.success(request, _('Models 360 are created'))

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import-archives/', self.process_import, name="import_archives"),
        ]
        return my_urls + urls

    def process_import(self, request):
        status = import_archives.Command().handle()
        if status == 'error':
            messages.warning(request, _('Archives no found. Download them on the server'))
        elif status == 'success':
            messages.success(request, _('Archives imported successfully'))
        return HttpResponseRedirect("../")


@admin.register(Image360)
class Image360Admin(admin.ModelAdmin):
    list_display = ['id', 'vendor_code', 'iframe', 'date']
    list_display_links = ['vendor_code']
    fields = ['vendor_code', 'iframe', 'model360', 'date']
    search_fields = ['vendor_code']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        self.my_request = request
        return qs

    @admin.display(description=_('Image 360'))
    def model360(self, obj):
        url = self.my_request.build_absolute_uri(settings.MEDIA_URL + obj.iframe.name)
        context = {'url': url}
        content = TemplateResponse(self.my_request, 'admin/image360upload/image360/iframe.html', context)
        return mark_safe(content.render().content.decode("utf-8"))

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class RemoteUpdateImages360UrlInline(admin.TabularInline):
    model = RemoteUpdateImages360Url
    extra = 0


@admin.register(Website)
class WebsiteAdmin(admin.ModelAdmin):
    list_display = ['website', 'api_key']
    inlines = [RemoteUpdateImages360UrlInline]
    actions = ['send_images_on_sites']

    @admin.action(description=_('Send images 360 on chosen websites'))
    def send_images_on_sites(self, request, queryset):
        websites = queryset.select_related('remoteupdateimages360url')
        for website in websites:
            try:
                urllib.request.urlopen(website.remoteupdateimages360url.url)
            except (ObjectDoesNotExist, URLError) as e:
                messages.warning(request, mark_safe(f'<b>{website.website}</b>: {e}'))
            else:
                messages.success(
                    request,
                    mark_safe(f'<b>{website.website}</b>: {_("Images 360 are successfully sent")}')
                )
