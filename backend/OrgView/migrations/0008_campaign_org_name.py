# Generated by Django 3.0.5 on 2022-03-31 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OrgView', '0007_merge_20220331_1840'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='org_name',
            field=models.CharField(default='new', max_length=200),
            preserve_default=False,
        ),
    ]
