# Generated by Django 4.2.2 on 2023-06-20 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('company', models.CharField(max_length=100)),
                ('trade_type', models.CharField(choices=[('BUY', 'Buy'), ('SELL', 'Sell'), ('SPLIT', 'Split')], max_length=5)),
                ('qty', models.IntegerField(blank=True, default=0, null=True)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('avg_buy_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('balance_qty', models.IntegerField(blank=True, null=True)),
            ],
        ),
    ]
