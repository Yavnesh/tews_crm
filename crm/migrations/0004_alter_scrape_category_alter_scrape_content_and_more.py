# Generated by Django 5.0.4 on 2024-04-26 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0003_alter_scrape_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scrape',
            name='category',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='scrape',
            name='content',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='scrape',
            name='sub_category',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='scrape',
            name='sub_title',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='scrape',
            name='title',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='scrape',
            name='url',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='scrape',
            name='url_id',
            field=models.CharField(max_length=10),
        ),
    ]
