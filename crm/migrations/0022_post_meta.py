# Generated by Django 5.0.4 on 2024-05-06 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0021_rename_image_path_static_post_image_crm_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='meta',
            field=models.TextField(default='none'),
        ),
    ]