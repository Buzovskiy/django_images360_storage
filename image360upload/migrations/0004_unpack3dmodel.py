# Generated by Django 4.0 on 2021-12-17 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('image360upload', '0003_dummymodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='Unpack3dModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'managed': False,
            },
        ),
    ]
