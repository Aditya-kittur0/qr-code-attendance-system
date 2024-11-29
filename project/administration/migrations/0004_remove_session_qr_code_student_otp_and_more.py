# Generated by Django 5.1.3 on 2024-11-18 20:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0003_session_qr_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='session',
            name='qr_code',
        ),
        migrations.AddField(
            model_name='student',
            name='otp',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administration.session'),
        ),
    ]
