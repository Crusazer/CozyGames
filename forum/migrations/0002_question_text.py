# Generated by Django 5.0.3 on 2024-04-07 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='text',
            field=models.TextField(blank=True, default='', max_length=500),
        ),
    ]
