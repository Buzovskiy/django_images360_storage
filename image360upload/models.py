import os
import pathlib
import datetime
import shutil
import secrets

from django.db import models
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.core.files.storage import FileSystemStorage
from .validators import validate_file_extension


def iframe_upload_to_function(instance, filename):
    """ this function has to return the location to upload the file """
    now = datetime.date.today()
    return f'3d_models/models/{now:%Y/%m/%d}/{instance.vendor_code}/{filename}'


class Image360(models.Model):
    vendor_code = models.CharField(
        verbose_name=_('Product vendor code'),
        max_length=255,
        blank=False,
        null=True,
        unique=True,
        editable=False,
    )
    iframe = models.FileField(
        verbose_name=_('Image 360 path'),
        max_length=255,
        blank=False,
        null=True,
        upload_to=iframe_upload_to_function,
    )
    date = models.DateTimeField(verbose_name=_('The date of creation'), auto_now_add=True, null=True)

    def __str__(self):
        return f"{_('Model 360')} {self.vendor_code}"

    class Meta:
        verbose_name = _('Model 360')
        verbose_name_plural = _('Models 360')


@receiver(post_delete, sender=Image360)
def post_delete_image360(sender, instance, *args, **kwargs):
    """When we delete image360 instance, delete old image360 file and parent directory"""
    try:
        # Remember path to parent directory
        parent = pathlib.Path(instance.iframe.path).parent
        # Remove record
        instance.iframe.delete(save=False)
        print(parent)
        # Remove parent
        shutil.rmtree(parent)
    except:
        pass


class MyFileStorage(FileSystemStorage):
    # This method is actually defined in Storage
    def get_available_name(self, name, max_length):
        archive_objects = Image360Archive.objects.filter(archive__endswith=os.path.basename(name)).all()
        if archive_objects.count():
            for archive_object in archive_objects:
                if os.path.basename(name) == os.path.basename(archive_object.archive.name):
                    archive_object.delete()

        return name # simply returns the name passed


class Image360Archive(models.Model):
    vendor_code = models.CharField(
        _('Vendor code'),
        max_length=255,
        unique=True,
        null=True,
    )
    archive = models.FileField(
        upload_to='3d_models/archives/imported/',
        validators=[validate_file_extension],
        null=False,
        blank=False,
        storage=MyFileStorage(),
        unique=True,
        verbose_name=_('Archive'),
    )
    size = models.CharField(
        max_length=255,
        editable=False,
        null=False,
        blank=False,
        default=1000,
        verbose_name=_('Archive size')
    )

    def save(self, *args, **kwargs):
        self.size = self.archive.size
        super().save(*args, **kwargs)

    def __str__(self):
        return os.path.basename(self.archive.name)

    class Meta:
        verbose_name = _('Archive')
        verbose_name_plural = _('Archives')


@receiver(post_delete, sender=Image360Archive)
def post_delete_archive(sender, instance, *args, **kwargs):
    """When we delete archive instance, delete old archive file """
    try:
        instance.archive.delete(save=False)
    except:
        pass


@receiver(pre_save, sender=Image360Archive)
def pre_save_archive(sender, instance, *args, **kwargs):
    """When update archive, delete old archive file.Instance old archive file will delete from os """
    try:
        old_file = instance.__class__.objects.get(pk=instance.id).archive.path
        try:
            new_file = instance.archive.path
        except:
            new_file = None
        if new_file != old_file:
            if os.path.exists(old_file):
                os.remove(old_file)
    except:
        pass


class Website(models.Model):
    website = models.CharField(
        verbose_name=_('Web site'),
        max_length=255,
        unique=True,
        help_text=_('Enter website domain you want to provide images 360 access for. E.g., example.com'),
    )
    api_key = models.CharField(
        verbose_name=_('Api key'),
        max_length=255,
        blank=True,
        unique=True,
        help_text=_('Enter API key for image 360 access or live it empty in order the system generated it '
                    'automatically')
    )

    def __str__(self):
        return self.website

    def save(self, *args, **kwargs):
        if not self.api_key:
            self.api_key = secrets.token_hex(16)
            # Iterate until get unique api_key
            while Website.objects.filter(api_key=self.api_key).count():
                self.api_key = secrets.token_hex(16)
        super(Website, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('Web site')
        verbose_name_plural = _('Web sites')


class RemoteUpdateImages360Url(models.Model):
    website = models.OneToOneField(Website, on_delete=models.CASCADE)
    url = models.CharField(max_length=255, blank=True, null=True)






