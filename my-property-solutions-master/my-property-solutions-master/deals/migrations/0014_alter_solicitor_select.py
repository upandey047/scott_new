# Generated by Django 3.2.7 on 2022-01-05 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deals', '0013_solicitor_select'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitor',
            name='select',
            field=models.BooleanField(default=True),
        ),
    ]