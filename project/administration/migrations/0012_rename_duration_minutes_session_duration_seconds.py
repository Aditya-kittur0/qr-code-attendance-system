# Generated by Django 5.1.3 on 2024-11-28 20:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0011_session_order'),
    ]

    operations = [
        migrations.RenameField(
            model_name='session',
            old_name='duration_minutes',
            new_name='duration_seconds',
        ),
    ]
