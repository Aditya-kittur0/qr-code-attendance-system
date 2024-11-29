# Generated by Django 5.1.3 on 2024-11-24 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0006_attendance_device_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='device_id',
        ),
        migrations.AddField(
            model_name='student',
            name='mac_address',
            field=models.CharField(blank=True, max_length=17, null=True),
        ),
    ]