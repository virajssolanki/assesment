# Generated by Django 4.2.2 on 2023-06-20 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_remove_transaction_company_transaction_split_ratio_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='total_holding_qty',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]