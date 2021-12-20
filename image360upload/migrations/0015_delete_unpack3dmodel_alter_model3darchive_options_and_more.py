# Generated by Django 4.0 on 2021-12-20 15:59

from django.db import migrations, models
import image360upload.models
import image360upload.validators


class Migration(migrations.Migration):

    dependencies = [
        ('image360upload', '0014_alter_model3darchive_size'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Unpack3dModel',
        ),
        migrations.AlterModelOptions(
            name='model3darchive',
            options={'verbose_name': 'Archive', 'verbose_name_plural': 'Archives'},
        ),
        migrations.AlterField(
            model_name='model3darchive',
            name='archive',
            field=models.FileField(storage=image360upload.models.MyFileStorage(), unique=True, upload_to='3d_models/archives/imported/', validators=[image360upload.validators.validate_file_extension], verbose_name='Archive'),
        ),
        migrations.AlterField(
            model_name='model3darchive',
            name='size',
            field=models.CharField(default=1000, editable=False, max_length=255, verbose_name='Archive size'),
        ),
    ]