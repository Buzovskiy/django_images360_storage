from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class Image360UploadConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'image360upload'
    verbose_name = _('Image 360 upload')
