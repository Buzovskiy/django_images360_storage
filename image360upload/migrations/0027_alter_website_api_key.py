# Generated by Django 4.0 on 2021-12-24 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('image360upload', '0026_alter_website_api_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='website',
            name='api_key',
            field=models.CharField(blank=True, help_text='Enter api key for image 360 access or live it empty in order the system generated it automatically', max_length=255, verbose_name='Api key'),
        ),
    ]