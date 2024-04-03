# Generated by Django 5.0.3 on 2024-04-03 08:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cozygames', '0002_alter_reservation_table_alter_reservation_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CardGame',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('min_number_player', models.PositiveIntegerField()),
                ('max_number_player', models.PositiveIntegerField()),
                ('description', models.TextField(blank=True, default='No description.', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Voting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True, unique_for_date=True)),
                ('result', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='votings', to='cozygames.cardgame')),
            ],
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('card_game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='votes', to='cozygames.cardgame')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='votes', to=settings.AUTH_USER_MODEL)),
                ('voting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='votes', to='cozygames.voting')),
            ],
            options={
                'unique_together': {('user', 'date', 'card_game')},
            },
        ),
    ]