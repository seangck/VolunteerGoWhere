# Generated by Django 3.0.5 on 2022-03-21 17:41

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('OrgView', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='campaign',
            name='date',
        ),
        migrations.RemoveField(
            model_name='campaign',
            name='status',
        ),
        migrations.RemoveField(
            model_name='campaign',
            name='time',
        ),
        migrations.AddField(
            model_name='campaign',
            name='date_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]