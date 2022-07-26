# Generated by Django 3.2.9 on 2022-07-23 20:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BotUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(unique=True)),
                ('first_name', models.CharField(blank=True, max_length=256, null=True)),
                ('tel_number', models.CharField(blank=True, max_length=512, null=True)),
                ('active', models.BooleanField(default=False)),
                ('permission', models.CharField(blank=True, max_length=255, null=True)),
                ('cr_on', models.DateTimeField(auto_now_add=True)),
                ('cr_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
