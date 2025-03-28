# Generated by Django 5.1.7 on 2025-03-09 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0003_alter_logentry_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='logentry',
            name='legal_warning',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='logentry',
            name='remaining_hours',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='logentry',
            name='total_hours',
            field=models.FloatField(default=0.0),
        ),
    ]
