# Generated by Django 5.1.4 on 2024-12-11 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webserver', '0004_alter_scene_image_alter_scene_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scene',
            name='image',
            field=models.URLField(max_length=500),
        ),
        migrations.AlterField(
            model_name='scene',
            name='timestamp',
            field=models.BigIntegerField(),
        ),
    ]
