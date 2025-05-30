# Generated by Django 5.1.7 on 2025-05-15 05:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RegAndAuth', '0003_profile_avatar'),
    ]

    operations = [
        migrations.CreateModel(
            name='Family',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('code', models.CharField(max_length=12, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='family',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='members_profiles', to='RegAndAuth.family'),
        ),
        migrations.CreateModel(
            name='FamilyMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('joined_at', models.DateTimeField(auto_now_add=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('family', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='members', to='RegAndAuth.family')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='families', to='RegAndAuth.profile')),
            ],
        ),
    ]
