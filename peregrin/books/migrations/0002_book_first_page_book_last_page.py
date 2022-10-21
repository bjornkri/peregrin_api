# Generated by Django 4.1.2 on 2022-10-17 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='first_page',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='book',
            name='last_page',
            field=models.IntegerField(default=100),
            preserve_default=False,
        ),
    ]