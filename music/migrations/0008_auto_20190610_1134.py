# Generated by Django 2.1.7 on 2019-06-10 03:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0007_auto_20190603_1055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='mood',
            field=models.CharField(default='Calm', max_length=64),
        ),
    ]
