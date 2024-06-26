# Generated by Django 5.0.4 on 2024-04-28 08:35

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Centre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.TextField(max_length=500)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Employer', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Climber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('following', models.ManyToManyField(related_name='followers', to='tracker.centre')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Climber', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='centre',
            name='setters',
            field=models.ManyToManyField(related_name='employers', to='tracker.climber'),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('writer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='tracker.climber')),
            ],
        ),
        migrations.CreateModel(
            name='Wall',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('centre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='walls', to='tracker.centre')),
            ],
        ),
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('wall', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='routes', to='tracker.wall')),
            ],
        ),
    ]
