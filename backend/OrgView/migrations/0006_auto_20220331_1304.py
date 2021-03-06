# Generated by Django 3.0.5 on 2022-03-31 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OrgView', '0005_orgnotif_campaign_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='acceptedusers',
            name='campaign_name',
            field=models.CharField(default=' ', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='acceptedusers',
            name='org_name',
            field=models.CharField(default=' ', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='acceptedusers',
            name='phone_number',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='acceptedusers',
            name='user_name',
            field=models.CharField(default=' ', max_length=200),
            preserve_default=False,
        ),
    ]
