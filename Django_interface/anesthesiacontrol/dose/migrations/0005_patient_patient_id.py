# Generated by Django 5.1.5 on 2025-01-25 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dose', '0004_remove_patient_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='patient_id',
            field=models.CharField(blank=True, max_length=10, unique=True),
        ),
    ]
