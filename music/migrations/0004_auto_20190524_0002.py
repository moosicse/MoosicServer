# Generated by Django 2.1.7 on 2019-05-23 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0003_auto_20190523_2352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='music'),
        ),
    ]