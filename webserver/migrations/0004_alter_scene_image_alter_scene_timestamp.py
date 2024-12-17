# Generated by Django 5.1.4 on 2024-12-11 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webserver', '0003_geometry_scene_delete_dataentry_geometry_scene'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scene',
            name='image',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='scene',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
