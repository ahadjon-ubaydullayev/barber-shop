# Generated by Django 3.2.9 on 2022-08-21 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_alter_employee_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='styles',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images'),
        ),
    ]
