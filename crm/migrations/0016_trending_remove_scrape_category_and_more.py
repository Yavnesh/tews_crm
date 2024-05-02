# Generated by Django 5.0.4 on 2024-04-30 02:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0015_alter_twitterpost_content_alter_twitterpost_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trending',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('topic', models.TextField(default='none')),
                ('related_topics_rising', models.TextField(default='none')),
                ('related_topics_top', models.TextField(default='none')),
                ('related_query_rising', models.TextField(default='none')),
                ('related_query_top', models.TextField(default='none')),
                ('status', models.CharField(default='none', max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Trending',
            },
        ),
        migrations.RemoveField(
            model_name='scrape',
            name='category',
        ),
        migrations.RemoveField(
            model_name='scrape',
            name='sub_category',
        ),
        migrations.RemoveField(
            model_name='scrape',
            name='sub_title',
        ),
        migrations.RemoveField(
            model_name='scrape',
            name='url_id',
        ),
        migrations.AddField(
            model_name='scrape',
            name='images',
            field=models.TextField(default='NoNE'),
        ),
        migrations.AddField(
            model_name='scrape',
            name='trending_id',
            field=models.CharField(default='none', max_length=250),
        ),
        migrations.AlterField(
            model_name='scrape',
            name='content',
            field=models.TextField(default='NoNE'),
        ),
        migrations.AlterField(
            model_name='scrape',
            name='title',
            field=models.TextField(default='NoNE'),
        ),
        migrations.AlterField(
            model_name='scrape',
            name='url',
            field=models.TextField(default='NoNE'),
        ),
    ]
