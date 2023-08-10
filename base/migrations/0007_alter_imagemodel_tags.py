# Generated by Django 4.2.3 on 2023-08-10 10:09

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0005_auto_20220424_2025'),
        ('base', '0006_alter_imagemodel_host'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagemodel',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
