# Generated by Django 5.0.4 on 2024-05-11 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0006_review_route'),
    ]

    operations = [
        migrations.AddField(
            model_name='wall',
            name='last_updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
