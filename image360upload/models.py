from django.db import models
from django.utils.translation import gettext_lazy as _


class Image360(models.Model):
    vendor_code = models.CharField(
        verbose_name=_('Product vendor code'),
        max_length=255,
        blank=False,
        null=True
    )
    image_360_path = models.CharField(
        verbose_name=_('Image 360 path'),
        max_length=255,
        blank=False,
        null=True
    )


class Unpack3dModel(models.Model):
    class Meta:
        managed = False



