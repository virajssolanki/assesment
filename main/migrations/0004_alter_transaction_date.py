# Generated by Django 4.2.2 on 2023-06-22 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_transaction_total_holding_qty'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='date',
            field=models.DateField(default=None),
        ),
    ]
