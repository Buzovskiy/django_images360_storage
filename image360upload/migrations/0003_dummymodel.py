# Generated by Django 4.0 on 2021-12-15 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('image360upload', '0002_alter_image360_image_360_path_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DummyModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name_plural': 'Dummy Model',
            },
        ),
    ]