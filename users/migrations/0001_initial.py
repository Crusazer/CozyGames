# Generated by Django 5.0.3 on 2024-04-04 11:41

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('birthday', models.DateTimeField(blank=True, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=13, validators=[django.core.validators.RegexValidator(message='Phone number should start with +375 and consist of 13 digits. For exemple +375291231212 ', regex='^\\+375(24|25|29|33|44)\\d{7}$')])),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
