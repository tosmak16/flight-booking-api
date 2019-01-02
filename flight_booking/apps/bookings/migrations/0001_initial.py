# Generated by Django 2.1.4 on 2019-01-02 00:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flight_from', models.CharField(max_length=100)),
                ('flight_to', models.CharField(max_length=100)),
                ('departing_date', models.DateField(default=django.utils.timezone.now)),
                ('returning_date', models.DateField(blank=True, default=django.utils.timezone.now, null=True)),
                ('type', models.CharField(choices=[('ONE', 'O'), ('ROUND', 'R')], default='ONE', max_length=10)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requester', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
