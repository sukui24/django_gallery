# Generated by Django 4.2.3 on 2023-08-16 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_alter_imagemodel_host'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagemodel',
            name='is_private',
            field=models.BooleanField(default=False),
        ),
    ]
