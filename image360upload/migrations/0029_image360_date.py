# Generated by Django 4.0 on 2021-12-24 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('image360upload', '0028_alter_website_api_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='image360',
            name='date',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='The date of creation'),
        ),
    ]