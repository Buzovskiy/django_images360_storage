# Generated by Django 4.0 on 2021-12-19 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('image360upload', '0008_model3darchive_alter_unpack3dmodel_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='model3darchive',
            name='archive',
            field=models.FileField(upload_to='3d_models/archives/imported/'),
        ),
    ]
