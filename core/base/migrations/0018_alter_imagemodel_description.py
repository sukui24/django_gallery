# Generated by Django 4.2.3 on 2023-10-07 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0017_alter_imagemodel_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagemodel',
            name='description',
            field=models.TextField(blank=True, default='', max_length=3000),
        ),
    ]
