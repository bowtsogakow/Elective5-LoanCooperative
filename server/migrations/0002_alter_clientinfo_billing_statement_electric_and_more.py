# Generated by Django 5.1.3 on 2024-11-22 03:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientinfo',
            name='billing_statement_electric',
            field=models.ImageField(blank=True, null=True, upload_to='billing_statements/'),
        ),
        migrations.AlterField(
            model_name='clientinfo',
            name='billing_statement_water',
            field=models.ImageField(blank=True, null=True, upload_to='billing_statements/'),
        ),
    ]
