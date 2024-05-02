# Generated by Django 5.0.4 on 2024-04-27 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0006_post_image_prompt_alter_post_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='selected_image',
            field=models.CharField(default='none', max_length=250),
        ),
        migrations.AlterField(
            model_name='post',
            name='image_path',
            field=models.TextField(default='none'),
        ),
    ]
