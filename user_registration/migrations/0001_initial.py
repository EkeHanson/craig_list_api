# Generated by Django 5.0.2 on 2024-02-17 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('reset_token', models.CharField(blank=True, max_length=100, null=True)),
                ('reset_token_expires', models.DateTimeField(blank=True, null=True)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('bio', models.TextField(max_length=255)),
                ('email', models.EmailField(max_length=80, unique=True)),
                ('date_of_birth', models.DateField()),
                ('user_type', models.CharField(choices=[('owner', 'Owner'), ('admin', 'Admin'), ('client', 'Client')], max_length=10)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
