# Generated by Django 3.2.8 on 2021-10-22 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='identifier_record',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='client',
            name='is_register',
            field=models.BooleanField(default=False),
        ),
    ]
