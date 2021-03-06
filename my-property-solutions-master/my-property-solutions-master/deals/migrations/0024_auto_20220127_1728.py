# Generated by Django 3.2.7 on 2022-01-27 17:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0002_initial'),
        ('deals', '0023_auto_20220118_1118'),
    ]

    operations = [
        migrations.AddField(
            model_name='mypurchasedetails',
            name='agent1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='agent1', to='deals.agent'),
        ),
        migrations.AlterField(
            model_name='mypurchasedetails',
            name='agent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='my_agent_details', to='contacts.contact'),
        ),
    ]
