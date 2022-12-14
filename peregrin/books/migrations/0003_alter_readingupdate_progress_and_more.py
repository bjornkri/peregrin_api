# Generated by Django 4.1.2 on 2022-10-18 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_book_first_page_book_last_page'),
    ]

    operations = [
        migrations.AlterField(
            model_name='readingupdate',
            name='progress',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterUniqueTogether(
            name='readingupdate',
            unique_together={('book', 'date')},
        ),
    ]
