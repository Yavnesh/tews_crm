# Generated by Django 5.0.4 on 2024-04-30 22:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0017_delete_url_scrape_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scrape',
            name='count',
        ),
    ]
