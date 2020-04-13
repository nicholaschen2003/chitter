# Generated by Django 3.0.3 on 2020-03-04 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_auto_20200304_0854'),
    ]

    operations = [
        migrations.AddField(
            model_name='poster',
            name='poster_handle',
            field=models.CharField(default=None, max_length=200),
        ),
        migrations.AlterField(
            model_name='post',
            name='post_content',
            field=models.CharField(default=None, max_length=200),
        ),
        migrations.AlterField(
            model_name='poster',
            name='poster_name',
            field=models.CharField(default=None, max_length=200),
        ),
    ]
