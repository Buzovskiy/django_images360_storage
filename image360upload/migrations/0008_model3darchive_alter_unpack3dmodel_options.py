# Generated by Django 4.0 on 2021-12-19 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('image360upload', '0007_delete_dummymodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='Model3dArchive',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('archive', models.FileField(upload_to='3d_models/')),
            ],
        ),
        migrations.AlterModelOptions(
            name='unpack3dmodel',
            options={'managed': False, 'verbose_name': 'Unpack 3d model', 'verbose_name_plural': 'Unpack 3d models'},
        ),
    ]
