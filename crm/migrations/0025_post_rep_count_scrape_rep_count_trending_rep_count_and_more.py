# Generated by Django 5.0.4 on 2024-05-18 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0024_scrape_short_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='rep_count',
            field=models.TextField(default='0'),
        ),
        migrations.AddField(
            model_name='scrape',
            name='rep_count',
            field=models.TextField(default='0'),
        ),
        migrations.AddField(
            model_name='trending',
            name='rep_count',
            field=models.TextField(default='0'),
        ),
        migrations.AddField(
            model_name='twitterpost',
            name='rep_count',
            field=models.TextField(default='0'),
        ),
    ]