# Generated by Django 4.0 on 2021-12-20 00:22

from django.db import migrations, models
import image360upload.models
import image360upload.validators


class Migration(migrations.Migration):

    dependencies = [
        ('image360upload', '0010_alter_model3darchive_archive'),
    ]

    operations = [
        migrations.AlterField(
            model_name='model3darchive',
            name='archive',
            field=models.FileField(storage=image360upload.models.MyFileStorage(), unique=True, upload_to='3d_models/archives/imported/', validators=[image360upload.validators.validate_file_extension]),
        ),
    ]
