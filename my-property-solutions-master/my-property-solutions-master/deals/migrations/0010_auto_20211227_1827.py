# Generated by Django 3.2.7 on 2021-12-27 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deals', '0009_alter_purchase_renovation_required'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Bank',
            new_name='BankNew',
        ),
        migrations.AlterField(
            model_name='purchase',
            name='renovation_required',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], default='Yes', max_length=5, verbose_name='Renovation Required'),
        ),
    ]
