# Generated by Django 5.0.4 on 2024-05-05 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0019_post_image_path_static'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='survey',
            field=models.TextField(default='none'),
        ),
        migrations.AlterField(
            model_name='post',
            name='tags',
            field=models.TextField(default='none'),
        ),
        migrations.AlterField(
            model_name='scrape',
            name='content',
            field=models.TextField(default='none'),
        ),
        migrations.AlterField(
            model_name='scrape',
            name='images',
            field=models.TextField(default='none'),
        ),
        migrations.AlterField(
            model_name='scrape',
            name='title',
            field=models.TextField(default='none'),
        ),
        migrations.AlterField(
            model_name='scrape',
            name='url',
            field=models.TextField(default='none'),
        ),
        migrations.AlterField(
            model_name='twitterpost',
            name='content',
            field=models.TextField(default='none'),
        ),
    ]
