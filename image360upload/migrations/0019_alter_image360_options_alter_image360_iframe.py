# Generated by Django 4.0 on 2021-12-23 11:49

from django.db import migrations, models
import image360upload.models


class Migration(migrations.Migration):

    dependencies = [
        ('image360upload', '0018_rename_image_360_path_image360_iframe'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='image360',
            options={'verbose_name': 'Model 360', 'verbose_name_plural': 'Models 360'},
        ),
        migrations.AlterField(
            model_name='image360',
            name='iframe',
            field=models.FileField(max_length=255, null=True, upload_to=image360upload.models.iframe_upload_to_function, verbose_name='Image 360 path'),
        ),
    ]
