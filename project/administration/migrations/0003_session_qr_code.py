# Generated by Django 5.1.3 on 2024-11-18 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0002_session_remove_attendance_session_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='qr_code',
            field=models.ImageField(blank=True, null=True, upload_to='qrcodes/'),
        ),
    ]
