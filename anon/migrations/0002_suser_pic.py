# Generated by Django 3.2.6 on 2021-09-13 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anon', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='suser',
            name='pic',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]
