# Generated by Django 3.2.7 on 2022-01-05 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deals', '0012_auto_20220103_1428'),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitor',
            name='select',
            field=models.BooleanField(default=False),
        ),
    ]
