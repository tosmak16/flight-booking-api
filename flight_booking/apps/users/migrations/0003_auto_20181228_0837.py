# Generated by Django 2.1.4 on 2018-12-28 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_passport_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='passport_url',
        ),
        migrations.AddField(
            model_name='user',
            name='passport',
            field=models.FileField(default='', upload_to=''),
        ),
    ]