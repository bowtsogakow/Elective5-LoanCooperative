# Generated by Django 5.1.3 on 2024-12-03 15:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0003_rename_total_payed_loan_total_amount_paid_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='loan',
            name='date_end',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='loan',
            name='date_created',
            field=models.DateField(default=datetime.date(2024, 12, 3)),
        ),
        migrations.AlterField(
            model_name='payment',
            name='date',
            field=models.DateField(default=datetime.date(2024, 12, 3)),
        ),
    ]