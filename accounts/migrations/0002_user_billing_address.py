# Generated by Django 5.2.3 on 2025-06-14 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='billing_address',
            field=models.TextField(blank=True),
        ),
    ]
